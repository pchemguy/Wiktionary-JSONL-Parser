# Software documentation

## Scope and authority

Apply conventions for READMEs, tutorials, procedures, API references, architecture documents, and docstrings. Check alignment with inspected implementation and intended reader tasks. This is a documentation workflow, not authority to implement software, execute commands, or claim tested behavior.

## Inputs and missing information

Use the documentation, intended users, code/configuration/API/version where supplied, and requested scope. Record which implementation and examples were inspected. If code is unavailable, improve the text and flag behavior needing confirmation. Never infer runtime guarantees merely from names or illustrative pseudocode.

## Procedure

1. Identify the document's job: orientation, task completion, reference lookup, conceptual explanation, or maintenance. Separate these when mixing them creates reader burden; do not mandate one repository layout.
2. Establish prerequisites, supported versions, platform assumptions, inputs, expected outputs, and necessary setup. Check the reader has needed context before each step.
3. Compare documented interfaces with inspected definitions: names, signatures, defaults, types, return values, exceptions, side effects, ordering, concurrency, persistence, and constraints as relevant. Inspect implementations as well as declarations when claims depend on behavior. Mark discrepancies and uncertainty.
4. Check procedures and examples for complete context, coherent order, valid names, and described outcomes. Static inspection is not execution. Run examples only if execution is separately authorized, facilities are available, and effects are appropriate; record exact checks and results. Do not claim examples were run from textual plausibility.
5. Apply genre-specific criteria below, then selected [composition](composition-analysis.md), [terminology](terminology-consistency.md), and [language](language-revision.md) workflows.
6. Preserve code blocks, identifiers, command flags, paths, and machine-readable syntax. Propose technical corrections separately when authority or behavior is unclear. Do not repair the implementation under the guise of editing its description.
7. After substantive documentation changes, or supplied-code changes made under separate authority, recheck affected docstrings using the sequence below. This workflow does not authorize implementing or executing software.
8. Verify revised claims against inspected material and report unresolved behavior, version, or execution questions through [revision check](revision-check.md).

## Docstring maintenance

1. Identify affected callables and check semantic drift and completeness against inspected signatures and behavior.
2. Follow the project's declared style or consistently established convention. For Python without a governing convention, use Google style. Use the predominant language/project convention elsewhere; preserve established formatting during focused edits.
3. Cover parameters, returns, raises, side effects, and constraints where applicable. Use meaningful summaries and appropriate detail without repeating obvious names or inventing behavior or exceptions.

## Genre checks

| Form | Check |
|---|---|
| README | Purpose, intended users, honest status, minimal useful example, prerequisites, navigation, and maintenance context appropriate to the project. |
| Tutorial/procedure | Goal, starting state, ordered steps, expected outcomes, recovery guidance for material failures, and a clear completion condition. |
| API reference | Exact names/signatures, parameters/defaults, returns, errors, constraints, side effects, version scope, and useful examples. |
| Architecture | Responsibilities, interfaces, dependencies, invariants, trade-offs, and consistency with inspected structure; separate proposed design from implementation. |
| Docstrings | Agreement with the callable's behavior and signature, meaningful summaries, appropriate detail, and consistent project style. |

## Outputs and examples

Return revised documentation or a discrepancy review as requested, plus inspected scope and unperformed checks. A signature says `batch_id` first but an example reverses the arguments: flag and correct the documentation if the inspected definition establishes order. A method described as atomic but implemented through several commits requires a substantive discrepancy finding, not smoother prose. A tutorial using platform-specific commands must state its platform assumptions rather than claim cross-platform execution.

If execution fails, report the observed failure and available explanation; do not assert an implementation fix without authorized investigation. If the task names an external current API but supplies no docs, evidence mode governs retrieval; model memory is not current verification.

## Completion checks

Documentation serves its genre and reader task, names align with inspected code, prerequisites and outcomes are clear, and docstrings reflect supplied behavior. Execution and static inspection are explicitly distinguished. No software change, invented guarantee, or unperformed test is presented as completed.
