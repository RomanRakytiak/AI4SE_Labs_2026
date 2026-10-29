# ADR-NNN: [Decision title]

- **Status:** Proposed
- **Date:** [YYYY-MM-DD]
- **Decision owners:** [team or role]

## Context

[Describe the project, the decision scope, the important requirements, and the
constraints that make this decision necessary.]

## Decision drivers and assumptions

| Driver | Why it matters | Weight (1-5) | Evidence or assumption |
|---|---|---:|---|
| [driver] | [project-specific reason] | [n] | [evidence] |

## Decision

[State the selected architecture in one clear paragraph.]

### Selected architecture

[Describe the deployable units, module or service boundaries, data ownership,
communication paths, and important consistency, authorization, and failure behavior.]

## Decision matrix

| Criterion | Weight | Candidate A | Candidate B | Candidate C |
|---|---:|---:|---:|---:|
| [criterion] | [n] | [1/3/5] | [1/3/5] | [1/3/5] |
| **Weighted total** |  | **[total]** | **[total]** | **[total]** |

[Explain important scores, assumptions, and any weakness of the leading candidate.]

## Requirement coverage

| Requirement group | Responsible boundary | Key invariant or behavior |
|---|---|---|
| [requirements] | [module/service] | [invariant] |

## Component and data-flow view

```text
[client] -> [API/application boundary] -> [selected components] -> [data/integrations]
```

[Explain the most important request, event, or failure flow.]

## Alternatives considered

### [Candidate A]

**Benefits:** [what it would provide for this project]

**Why not selected now:** [why the benefits do not justify the costs under the
current assumptions]

**Costs and risks:** [specific project consequences]

**Reconsider when:** [observable trigger]

### [Candidate B]

**Benefits:** [...]

**Why not selected now:** [...]

**Costs and risks:** [...]

**Reconsider when:** [...]

## Consequences

### Benefits

- [benefit]

### Costs and risks

- [cost or risk]

### Mitigations and evolution path

- [mitigation or future extraction/change path]

## Validation and review triggers

[State how the decision will be validated and list measurable or observable
conditions that should cause a review.]

## Open implementation questions

- [Question that belongs in a later design or implementation document]
