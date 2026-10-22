from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


TEXT_SUFFIXES = {".txt", ".eml", ".md", ".rst", ".csv", ".json", ".xml"}
MAX_REVIEW_ROUNDS = 2
MAX_JSON_ATTEMPTS = 3

def _progress(message: str) -> None:
    """Print concise, flushed progress messages for interactive runs."""
    print(message, flush=True)


REVIEW_PROMPT = """ROLE: You are senior software analyst.

TASK:
Review the proposed requirements as a quality gate. Do not rewrite them.

Report only:
1. missing source traces or capabilities from the candidates;
2. contradictions, vague wording, or unsupported claims;
3. exact semantic duplicates.

Keep independent capabilities separate. Different actors, workflows, data,
rules, permissions, or acceptance tests mean the requirements must stay separate.
Do not report a merge just because two requirements belong to the same product.

FORMAT:
Return only:
{{"issues":["short actionable issue"],
"merge_groups":[{{"keep":"exact name","merge":["exact name"],
"reason":"why these are exact duplicates"}}]}}
Use empty arrays when there are no problems.
"""

CONSOLIDATION_PROMPT = """ROLE: You are senior software analyst.

TASK:
Create a requirements document from the candidates and current draft.

Rules:
- On the first pass, consolidate candidates into requirements.
- On a revision pass, preserve the current draft and make only changes required
  by the feedback. Do not split requirements or increase their number unless
  the feedback identifies a missing capability.
- Keep one requirement for each independent capability or constraint.
- Merge only exact semantic duplicates: same actor, action, data, and outcome.
- Keep separate items with different actors, workflows, data, rules,
  permissions, or acceptance tests.
- Do not create requirements from examples, questions, implementation details,
  wishes, or unsupported claims.
- Keep an ambiguous but real capability and mention the unresolved detail.
  Ambiguity, missing detail, or "too broad" are NOT reasons to discard.
- Put only contradictory (name the conflicting item), nonsensical, unsupported,
  or example-only items in discarded with a reason.
- Never silently drop a candidate: every candidate must end up in a requirement,
  merged_items, or discarded.
- Do not bundle several independent capabilities into one requirement.
- Preserve every source path. Do not invent facts or technical decisions.
- Use only Critical, High, Medium, or Low priorities.

FORMAT:
Return only:
{{"requirements":[{{"key":"stable-key","name":"short name","explanation":"one paragraph",
"priority":"High","sources":["relative/path"]}}],
"merged_items":[{{"source_statement":"...","merged_into":"requirement name",
"reason":"...","sources":["relative/path"]}}],
"discarded":[{{"statement":"...","reason":"...","sources":["relative/path"]}}]}}

Every kept requirement needs a name, paragraph explanation, priority, and source.
Do not use a catch-all umbrella requirement.
"""

EXTRACTION_PROMPT = """ROLE: You are senior software analyst.

TASK:
Extract requirement candidates from this one source document.

Create one candidate for each distinct capability, business rule, constraint,
or documentation obligation. Group details belonging to the same capability.
Do not create candidates for examples, questions, wishes, implementation ideas,
or individual acceptance-test details. Do not invent missing facts.

For each candidate, record its type, quality, confidence, exact source path,
short evidence quote, and any concern. Normally return no more than 8
candidates and try not to create more than 12.

FORMAT:
Return only:
{{"candidates":[{{"name":"short name","statement":"source-grounded requirement",
"type":"functional|non-functional|constraint|documentation|assumption|unresolved",
"sources":["relative/path"],"evidence":["short exact quote"],
"confidence":"explicit|implied|uncertain",
"quality":"valid|ambiguous|contradictory|nonsensical|unsupported|example-only",
"concern":""}}]}}
"""


class NetworkState(TypedDict, total=False):
    input_dir: str
    documents: list[dict[str, str]]
    candidates: list[dict[str, Any]]
    consolidated: dict[str, Any]
    discarded_history: list[dict[str, Any]]
    merged_history: list[dict[str, Any]]
    validation: dict[str, Any]
    feedback: list[str]
    review_issues: list[str]
    round: int
    output: dict[str, Any]


def _model(name: str) -> ChatOpenAI:
    kwargs: dict[str, Any] = {"model": name, "temperature": 0}
    if os.getenv("OPENAI_BASE_URL"):
        kwargs["base_url"] = os.environ["OPENAI_BASE_URL"]
    return ChatOpenAI(**kwargs)


def _json_response(model: ChatOpenAI, instruction: str) -> dict[str, Any]:
    correction = ""
    for attempt in range(1, MAX_JSON_ATTEMPTS + 1):
        response = model.invoke([
            SystemMessage(content=(
                f"{correction}Return only valid JSON. Do not use markdown fences."
            )),
            HumanMessage(content=instruction),
        ])
        content = response.content if isinstance(response.content, str) else str(response.content)
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE)
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            correction = f"Error: invalid JSON ({exc}). Return JSON only. "
            _progress(f"|-> model returned invalid JSON; retry {attempt}/{MAX_JSON_ATTEMPTS}")
            continue
        if not isinstance(parsed, dict):
            correction = "Error: the top-level JSON value must be an object. "
            _progress(f"|-> model returned the wrong JSON shape; retry {attempt}/{MAX_JSON_ATTEMPTS}")
            continue
        return parsed
    raise RuntimeError(
        f"Model did not return a JSON object after {MAX_JSON_ATTEMPTS} attempts"
    )


def _compact_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep consolidation context complete while removing extraction noise."""
    compacted: list[dict[str, Any]] = []
    for candidate in candidates:
        compacted.append({
            key: str(candidate.get(key, ""))
            for key in ("name", "statement", "type", "sources", "evidence", "quality", "concern")
            if candidate.get(key) not in (None, "", [])
        })
    return compacted


def _normalise_sources(value: Any, fallback: str = "") -> list[str]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = [str(item).strip() for item in value]
    else:
        values = []
    return list(dict.fromkeys(item for item in values if item)) or ([fallback] if fallback else [])


def _normalise_model_lists(result: dict[str, Any]) -> dict[str, Any]:
    """Prevent malformed model fields from breaking rendering and validation."""
    for key in ("requirements", "merged_items", "discarded", "candidates", "issues", "merge_groups"):
        if not isinstance(result.get(key), list):
            result[key] = []
    for key in ("requirements", "merged_items", "discarded", "candidates", "merge_groups"):
        if not all(isinstance(item, dict) for item in result[key]):
            raise ValueError(f"Model returned a non-object item in {key}")
    if not all(isinstance(item, str) for item in result["issues"]):
        raise ValueError("Model returned a non-string review issue")
    for requirement in result["requirements"]:
        requirement["sources"] = _normalise_sources(requirement.get("sources"))
    for item in result["merged_items"]:
        item["sources"] = _normalise_sources(item.get("sources"))
    for item in result["discarded"]:
        item["sources"] = _normalise_sources(item.get("sources"))
    return result


def load_documents(state: NetworkState) -> NetworkState:
    """Deterministically load supported files and preserve relative paths."""
    root = Path(state.get("input_dir","")).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {root}")
    documents: list[dict[str, str]] = []
    paths = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
    _progress(f"Loading documents from {root}")
    _progress(f"|-> found {len(paths)} supported files")
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        documents.append({"path": path.relative_to(root).as_posix(), "text": text})
    if not documents:
        raise ValueError(f"No supported text documents found in {root}")
    return {"documents": documents, "discarded_history": [], "merged_history": [], "round": 0}


def extract_candidates(state: NetworkState) -> NetworkState:
    model = _model(os.getenv("REQUIREMENTS_EXTRACTION_MODEL", "gpt-5.6-luna"))
    candidates: list[dict[str, Any]] = []
    _progress("Extracting candidates file by file")
    for document in state.get("documents", []):
        path = document["path"]
        _progress(f"...inspecting {path}")
        result = _json_response(model, f"""{EXTRACTION_PROMPT}

SOURCE PATH: {path}

DOCUMENT TEXT:
{document["text"]}""")
        file_candidates = _normalise_model_lists(result).get("candidates", [])
        if not all(isinstance(candidate, dict) for candidate in file_candidates):
            raise ValueError(f"Model returned a non-object candidate for {path}")
        for candidate in file_candidates:
            candidate["sources"] = _normalise_sources(candidate.get("sources"), path)
        candidates.extend(file_candidates)
        _progress(f"   |-> {len(file_candidates)} candidates")
    _progress(
        f"|-> found {len(candidates)} candidates "
        f"({sum(bool(candidate.get('concern')) for candidate in candidates)} with concerns)"
    )
    return {"candidates": candidates}


def consolidate_requirements(state: NetworkState) -> NetworkState:
    model = _model(os.getenv("REQUIREMENTS_CONSOLIDATION_MODEL", "gpt-5.4-nano"))
    pass_number = state.get("round", 0) + 1
    _progress(f"Consolidating requirements (pass {pass_number})")
    feedback_items = state.get("feedback", [])
    feedback = "\nFEEDBACK:\n" + "\n".join(feedback_items) if feedback_items else ""
    is_revision = bool(state.get("consolidated"))
    candidate_context = [] if is_revision else _compact_candidates(state.get("candidates", []))
    revision_note = (
        "REVISION PASS: treat CURRENT DRAFT as the source of truth. "
        "Only fix the listed feedback; do not reconsider all candidates."
        if is_revision
        else
        "FIRST PASS: use CANDIDATES as the source material."
    )
    result = _normalise_model_lists(_json_response(model, f"""{CONSOLIDATION_PROMPT}

{revision_note}
{feedback}

CURRENT DRAFT:
{json.dumps(state.get('consolidated', {}), ensure_ascii=False)}

CANDIDATES:
{json.dumps(candidate_context, ensure_ascii=False)}"""
))
    current_discarded = result.get("discarded", [])
    discarded_history = list(state.get("discarded_history", []))
    seen_discarded = {
        item.get("statement", "").strip().lower()
        for item in discarded_history
    }
    for item in current_discarded:
        key = item.get("statement", "").strip().lower()
        if key not in seen_discarded:
            discarded_history.append(item)
            seen_discarded.add(key)
    current_merged = result.get("merged_items", [])
    merged_history = list(state.get("merged_history", []))
    seen_merged = {
        (item.get("source_statement", "").strip().lower(), item.get("merged_into", "").strip().lower())
        for item in merged_history
    }
    for item in current_merged:
        key = (item.get("source_statement", "").strip().lower(), item.get("merged_into", "").strip().lower())
        if key not in seen_merged:
            merged_history.append(item)
            seen_merged.add(key)
    _progress(f"|-> discarded {len(current_discarded)} this pass")
    _progress(f"|-> blacklist history: {len(discarded_history)} unique entries")
    _progress(f"|-> merged history: {len(merged_history)} unique entries")
    return {"consolidated": result, "discarded_history": discarded_history, "merged_history": merged_history}


def deterministic_validate(state: NetworkState) -> NetworkState:
    """Check required fields, priorities, traces, and obvious duplicate names."""
    _progress("Deterministic validation")
    requirements = state.get("consolidated", {}).get("requirements", [])
    issues: list[str] = []
    seen_names: dict[str, int] = {}
    priorities = {"Critical", "High", "Medium", "Low"}
    if not isinstance(requirements, list):
        return {"validation": {"issues": ["requirements must be a list"], "valid": False}}
    for i, requirement in enumerate(requirements):
        if not isinstance(requirement, dict):
            issues.append(f"requirement {i} is not an object")
            continue
        name = str(requirement.get("name", "")).strip()
        normalized = re.sub(r"\W+", " ", name.lower()).strip()
        if not name or len(name) > 160 or not requirement.get("explanation"):
            issues.append(f"requirement {i} lacks a name or explanation")
        if requirement.get("priority") not in priorities:
            issues.append(f"requirement {i} has an invalid priority")
        if not _normalise_sources(requirement.get("sources")):
            issues.append(f"requirement {i} has no source trace")
        if normalized and normalized in seen_names:
            issues.append(f"requirements {seen_names[normalized]} and {i} appear duplicated")
        if normalized:
            seen_names[normalized] = i
    _progress(f"|-> found {len(requirements)} requirements and {len(issues)} issues")
    return {"validation": {"issues": issues, "valid": not issues}}


def review_consistency(state: NetworkState) -> NetworkState:
    model = _model(os.getenv("REQUIREMENTS_REVIEW_MODEL", "gpt-5-mini"))
    _progress(f"Reviewing consistency (round {state.get('round', 0) + 1})")
    result = _normalise_model_lists(_json_response(model, f"""{REVIEW_PROMPT}

DOCUMENT:
{json.dumps(state.get('consolidated', {}), ensure_ascii=False)}

CANDIDATES:
{json.dumps(_compact_candidates(state.get('candidates', [])), ensure_ascii=False)}"""))
    issues = list(state.get("validation", {}).get("issues", [])) + result.get("issues", [])
    for merge_group in result.get("merge_groups", []):
        issues.append(
            "Merge " + ", ".join(merge_group.get("merge", []))
            + f" into {merge_group.get('keep', 'the retained requirement')}: {merge_group.get('reason', '')}"
        )
    issues = [str(issue).strip() for issue in issues if str(issue).strip()]
    _progress(f"|-> found {len(issues)} review issues")
    return {
        "feedback": issues,
        "review_issues": issues,
        "round": state.get("round", 0) + 1,
    }


def should_revise(state: NetworkState) -> str:
    revise = bool(state.get("feedback")) and state.get("round", 0) < MAX_REVIEW_ROUNDS
    _progress("Should revise again?" if revise else "Final review complete")
    return "revise" if revise else "finalize"


def finalize_document(state: NetworkState) -> NetworkState:
    _progress("Finalizing document")
    document = state.get("consolidated", {})
    requirements = document.get("requirements", [])
    for index, requirement in enumerate(requirements, start=1):
        requirement["id"] = f"REQ-{index:03d}"
        requirement.pop("key", None)
    for discarded in state.get("discarded_history", []):
        discarded.setdefault("sources", [])
        discarded.setdefault("reason", "Rejected during refinement")
    return {"output": {
        "title": "Refined Software Requirements",
        "priority_scale": {
            "Critical": "Required for the system to be viable or safe.",
            "High": "Important for the primary workflow; omission causes major impact.",
            "Medium": "Valuable requirement that can follow the primary workflow.",
            "Low": "Useful enhancement with limited impact if deferred.",
        },
        "requirements": requirements,
        "blacklist": state.get("discarded_history", []),
        "merged_items": state.get("merged_history", []),
        "metadata": {
            "source_document_count": len(state.get("documents", [])),
            "review_rounds": state.get("round", 0),
            "unresolved_review_issues": state.get("review_issues", []),
        },
    }}


def build_graph():
    graph = StateGraph(NetworkState)
    graph.add_node("load_documents", load_documents)
    graph.add_node("extract_candidates", extract_candidates)
    graph.add_node("consolidate_requirements", consolidate_requirements)
    graph.add_node("deterministic_validate", deterministic_validate)
    graph.add_node("review_consistency", review_consistency)
    graph.add_node("finalize_document", finalize_document)
    graph.add_edge(START, "load_documents")
    graph.add_edge("load_documents", "extract_candidates")
    graph.add_edge("extract_candidates", "consolidate_requirements")
    graph.add_edge("consolidate_requirements", "deterministic_validate")
    graph.add_edge("deterministic_validate", "review_consistency")
    graph.add_conditional_edges("review_consistency", should_revise, {"revise": "consolidate_requirements", "finalize": "finalize_document"})
    graph.add_edge("finalize_document", END)
    return graph.compile()


def render_markdown(output: dict[str, Any]) -> str:
    """Render every part of the structured result as one Markdown document."""
    lines = [f"# {output['title']}", "", "## Priority Scale", ""]
    for priority, description in output["priority_scale"].items():
        lines.append(f"- **{priority}**: {description}")
    lines.extend(["", "## Requirements", ""])
    for requirement in output["requirements"]:
        lines.extend([
            f"### {requirement['id']}: {requirement['name']}",
            "",
            f"**Priority:** {requirement['priority']}",
            "",
            "**Derived from:**",
        ])
        lines.extend(f"- `{source}`" for source in requirement["sources"])
        lines.extend(["", requirement["explanation"], ""])
    lines.extend(["## Blacklist", ""])
    blacklist = output.get("blacklist", [])
    if blacklist:
        for item in blacklist:
            lines.extend([
                f"### Discarded: {item.get('statement', 'Unspecified candidate')}",
                "",
                f"**Reason:** {item.get('reason', 'No reason supplied')}",
                "",
                "**Sources:**",
            ])
            lines.extend(f"- `{source}`" for source in item.get("sources", []))
            lines.append("")
    else:
        lines.append("No requirements were discarded by the consolidation stage.")
        lines.append("")
    merged_items = output.get("merged_items", [])
    lines.extend(["## Merged Candidate Trace", ""])
    if merged_items:
        for item in merged_items:
            lines.extend([
                f"- **Merged into `{item.get('merged_into', 'unspecified')}`:** {item.get('source_statement', 'Unspecified candidate')}",
                f"  - Reason: {item.get('reason', 'No reason supplied')}",
            ])
            lines.extend(f"  - Source: `{source}`" for source in item.get("sources", []))
    else:
        lines.append("No merge provenance was returned by the consolidation stage.")
    lines.append("")
    metadata = output.get("metadata", {})
    lines.extend([
        "## Generation Metadata",
        "",
        f"- Source documents: {metadata.get('source_document_count', 'unknown')}",
        f"- Review rounds: {metadata.get('review_rounds', 'unknown')}",
    ])
    if metadata.get("unresolved_review_issues"):
        lines.extend(["", "## Unresolved Review Issues", ""])
        lines.extend(f"- {issue}" for issue in metadata["unresolved_review_issues"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing the requirements corpus")
    parser.add_argument("--output", type=Path, default=Path("requirements.md"))
    args = parser.parse_args()
    _progress("Starting requirements refinement network")
    result = build_graph().invoke({"input_dir": str(args.input_dir)})
    output = result["output"]
    args.output.write_text(render_markdown(output), encoding="utf-8")
    _progress(f"Wrote {len(output['requirements'])} requirements to {args.output}")


if __name__ == "__main__":
    main()
