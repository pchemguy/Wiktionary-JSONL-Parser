# In-code documentation

Inspect the selected modules and their callers, tests, and accepted contracts before writing. Documentation must explain the code that exists without presenting an implementation discrepancy as a revised requirement.

## Select a style

1. Use the style specified by project instructions or documentation policy, including language-specific rules and tooling requirements.
2. If no style is specified, use an established professional convention suitable for the language and documentation generator. Google-style docstrings are an appropriate Python default; other languages use their established documentation comments or equivalent.
3. Apply the selected style consistently within the edited scope. Preserve compatible existing conventions and report conflicting styles or requirements rather than converting unrelated modules.

## Module and API coverage

| Element | Documentation to assess |
| --- | --- |
| Every project-owned code module in scope | Purpose, canonical responsibility, and relevant usage, constraints, or collaborators. Use a module docstring or the language's equivalent. |
| Public classes and interfaces | Responsibility, contracts, invariants, lifecycle, and important public attributes. |
| Public functions and methods | Behavior, parameters, return values, exceptions, side effects, and relevant preconditions or guarantees. |
| Consequential internal interfaces | Non-obvious contracts, assumptions, ordering, ownership, and failure behavior needed by maintainers. |
| Implementation comments | Reasons for consequential decisions, workarounds, or constraints that the code alone does not explain. |

Include applicable details rather than filling every possible section. For example, document resource ownership, concurrency, cancellation, units, encoding, or persistence semantics when those affect correct use. A small module may need only a precise responsibility statement; a complex API may need examples and operational constraints. Avoid narrating obvious statements, repeating signatures without explanation, or asserting guarantees that the code and evidence do not support.

## Maintain and check

- Review affected module and API documentation after substantive code changes, including changed signatures, errors, defaults, ownership, and side effects.
- Check names and contracts against inspected implementation, callers, tests, and accepted requirements. Report requirement conflicts to the user under the skill's amendment protocol.
- Use declared documentation lint, syntax, generation, or example checks when relevant and available. Report unrun checks and distinguish inspection from execution.
- Inspect the final diff for unintended behavior changes. Preserve annotations, executable statements, and public signatures; route necessary code repairs to the implementation workflow.

