# Import progress delivery plan

Phase 2 delivers byte-based CLI progress on top of the released SQLiteICUex converter.

| Milestone | Scope | Exit evidence |
| --- | --- | --- |
| 2.1 — Progress logging | Add the importer callback and default CLI reporter with quiet mode. Update user-facing CLI guidance. | Exact byte counts after SQLite writes, no advancement on failed batches, and no progress for empty or quiet imports. Run the focused and regression checks. |
| 2.2 — Phase review | Review the complete change and build the wheel and source archive for version 0.2.0. | Verify the installed CLI, repeat the regression checks, and validate the release bundle. |

The implementation belongs in `importer.py`, `cli.py`, existing CLI tests plus focused progress tests under `tests/`, and the README. The existing repository layout and release tools cover these paths. Publish the release after the verified phase is integrated into the default branch.
