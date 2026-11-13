# Main documentation preparation record

## Current control

- Mode and decision source — Interactive, one pass, as directed by the project instructions.
- Current scope — Main development documents for the single-process Russian Wiktionary JSONL-to-SQLite converter.
- Approval basis — Each applicable document checkpoint requires explicit acceptance. No checkpoint has been preapproved.
- Tracking and publication — Repository policy enables GitHub preparation tracking. [Milestone #1](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/1) and all nine DOCS issues were verified before branch creation.
- Next boundary — Review the published PROJECT proposal before ARCHITECTURE.

## Decisions and document evidence

| Task | Evidence |
| --- | --- |
| DOCS-001 | Initialization result below. |
| DOCS-002 | [PROJECT.md](PROJECT.md) is proposed at Git blob `d8a4bec734edea6bd9f2b133a183bcdfa077ff17`. Brief coverage and the legacy fixture/rollback probes were reviewed. Human acceptance is pending. |
| DOCS-003 through DOCS-009 | Pending. |

The initial input is the local, extracted Kaikki Russian Wiktionary JSONL file. The converter uses the legacy relational schema and mapping, runs in one process, and processes configurable batches measured in source lines. The user identified `batch_log` as a candidate for adaptation. Resume behavior, the required collation runtime, and treatment of source fields outside the legacy mapping remain project-brief decisions.

## Initialization

- Retained root files — `AI_DISCLOSURE.md`, `SDD-MANAGER.md`, `AGENTS.md`, and `SKILL_DISCOVERY_PROTOCOL.md`. Blob identities matched the baseline for all four. No root files needed copying.
- Continuation — All four root files were present at entry. Proceed to the brief proposal.
- Manual provenance — Existing instructions and records were preserved. The missing bundled template was added on `design-docs/ai-logs` at `8cd2a2fcfcbc793fe2c80669d288b64854ca0b8a`, based on `da8e87a03ec7e84a5b3021fe7ca772f3caadd251`, and merged into `main` at `c0bff86d0c13a611c930e18a040d23b42d5141e7`. The merge and exact template blob were read back from GitHub.
- Current reset — None.

## Pending transitions

Await human acceptance of the [PROJECT proposal](PROJECT.md). GitHub readback verified [DOCS-001](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/1) closed as completed. [DOCS-002](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/2) remains open.
