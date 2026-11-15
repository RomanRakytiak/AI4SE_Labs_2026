"""Solve the missing repository methods with retrieval-augmented generation."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from retrieve_chunks import retrieve


ALLOWED_MODELS = {
    "gpt-6-luna",
    "gpt-5.6-luna",
    "gpt-5.4-nano",
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-4.1-nano",
    "gpt-4o-mini",
}
DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_TASKS = (
    DEFAULT_REPOSITORY.parent / "Assignments" / "missing_code.json"
)


def build_prompt(task: dict[str, str], matches: list[dict[str, object]]) -> str:
    """Build a prompt that asks for one complete Python method."""
    context = "\n\n".join(
        f"### {match['chunk']['file']}:{match['chunk']['start_line']}-"
        f"{match['chunk']['end_line']}\n{match['chunk']['content']}"
        for match in matches
    )
    return f"""Role:
You are a careful Python maintainer working on an existing repository.

Task:
Implement the missing method specified below. Use the retrieved repository
context as evidence and preserve the existing project conventions.

Target file: {task["file"]}
Target class: {task["class"]}
Target method: {task["method"]}
Method documentation:
{task["docstring"]}

Relevant repository context:
{context}

Format:
Return only the complete Python method definition, including its decorators,
signature, docstring, and body. Do not use Markdown fences or explanations.
Preserve the existing method signature.
"""


def response_text(response: object) -> str:
    """Extract text from a LangChain response."""
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    raise TypeError("LLM response content is not text")


def clean_method(text: str) -> str:
    """Remove accidental Markdown fences from an otherwise valid response."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:python)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def method_range(source: str, class_name: str, method_name: str) -> tuple[int, int]:
    """Return zero-based source line bounds for a method in a named class."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name != class_name:
            continue
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if child.name == method_name:
                    start = min(
                        [child.lineno]
                        + [decorator.lineno for decorator in child.decorator_list]
                    )
                    return start - 1, child.end_lineno
    raise LookupError(f"Could not find {class_name}.{method_name}")


def replace_method(
    path: Path,
    class_name: str,
    method_name: str,
    generated_method: str,
) -> None:
    """Replace one method while preserving the surrounding source file."""
    source = path.read_text(encoding="utf-8")
    start, end = method_range(source, class_name, method_name)
    original_lines = source.splitlines(keepends=True)
    indentation = re.match(r"\s*", original_lines[start]).group(0)
    replacement = generated_method.strip("\n")
    replacement_lines = replacement.splitlines()
    if not replacement_lines or not replacement_lines[0].lstrip().startswith(
        ("def ", "async def ", "@")
    ):
        raise ValueError(f"LLM did not return a method for {class_name}.{method_name}")
    if not replacement_lines[0].startswith(indentation):
        replacement = "\n".join(
            indentation + line if line.strip() else line
            for line in replacement_lines
        )
    updated = original_lines[:start] + [replacement + "\n"] + original_lines[end:]
    path.write_text("".join(updated), encoding="utf-8")


def solve_task(
    task: dict[str, str],
    repository: Path,
    model: ChatOpenAI,
) -> None:
    """Retrieve context, call the model, and write one implementation."""
    matches = retrieve(
        "Implement "
        f"{task['class']}.{task['method']}: {task['docstring']}",
        top_k=5,
    )
    response = model.invoke(
        [
            SystemMessage(
                content=(
                    "You are a careful Python maintainer. Return only valid "
                    "source code for the requested method."
                )
            ),
            HumanMessage(content=build_prompt(task, matches)),
        ]
    )
    target = repository / task["file"]
    replace_method(target, task["class"], task["method"], clean_method(response_text(response)))


def run_tests(repository: Path) -> subprocess.CompletedProcess[str]:
    """Run the cloned project's tests and return the completed process."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_*.py",
        ],
        cwd=repository / "playground",
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--model", default=os.getenv("TASK_SOLVER_MODEL", DEFAULT_MODEL))
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()
    if args.model not in ALLOWED_MODELS:
        parser.error(f"--model must be one of: {', '.join(sorted(ALLOWED_MODELS))}")
    model_options: dict[str, object] = {"model": args.model}
    if os.getenv("OPENAI_BASE_URL"):
        model_options["base_url"] = os.environ["OPENAI_BASE_URL"]
    model = ChatOpenAI(**model_options)
    tasks = json.loads(args.tasks.read_text(encoding="utf-8"))

    for task in tasks:
        print(f"Solving {task['class']}.{task['method']}...")
        solve_task(task, args.repository, model)

    if not args.skip_tests:
        result = run_tests(args.repository)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()