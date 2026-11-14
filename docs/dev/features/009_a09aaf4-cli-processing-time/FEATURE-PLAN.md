# CLI total processing time delivery plan

## Phase 5 — CLI processing time

| Milestone | Delivery and exit evidence |
| --- | --- |
| 5.1 — CLI timing and verification | Instrument the CLI around the existing synchronous import call. Verify the exact format and order, successful empty input, quiet mode, failure, interruption, and CLI help. Update usage documentation. |
| 5.2 — Phase review | Reconcile governing documents, verify regressions and installed CLI behavior, and check the package inventory. Publish patch release `0.4.1` from the verified default-branch revision. |

The existing [layout](../../layout.md) applies. The CLI owns clock reads and formatting. Tests belong in the existing CLI and progress coverage. The library importer, worker protocol and database schema retain their current roles.
