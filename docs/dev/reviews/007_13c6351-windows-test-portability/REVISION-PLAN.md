# Windows test portability

Campaign `007_13c6351` starts at `13c63511ebe5b57a3ac791c660c3dcf64e6ef007`. The branch is `revision/007_13c6351-windows-test-portability`, created from `main` for eventual integration into `main`. The campaign is open at the revision plan.

## Evidence

The supplied Windows log reports Python 3.14.5, pytest 9.0.3, 104 passed, three skipped, three failures, and five errors. The log contains four setup and teardown errors on two 300,000-byte partition cases. Pytest used the byte payloads in generated test IDs and tried to assign those IDs to `PYTEST_CURRENT_TEST`, exceeding the 32,767-character limit reported by Windows. The following persistence test failed during setup because the preceding test did not tear down. The three independent failures concern missing-input path formatting, symlink and parent traversal, and schema line endings.

A disposable checkout with `core.autocrlf=true` reproduced the schema assertion failure on Linux. A second disposable checkout passed 111 tests, with two standard-SQLite-specific skips, after removing the global `PYTHONPATH` fixture. The available Linux runtime uses pytest 9.2.0, which produced short automatic IDs for the long inputs during collection. The Windows IDs and errors come from the supplied pytest 9.0.3 log.

## Revision actions

| Action | Scope and expected result |
| --- | --- |
| A-001 | Give the long partition cases short explicit pytest IDs while preserving their original payloads and assertions. Remove the global `PYTHONPATH` mutation in `tests/conftest.py`. Keep coverage for launching a worker with the caller's package and verify short collected IDs with pytest 9.0.3 where available. Run the persistence test directly and after the partition tests. |
| A-002 | Check for the correct missing-input path in the representation used by Python's OS error, without matching localized OS wording. Verify the destination stays absent and the subsequent existing-destination check still preserves the file. |
| A-003 | Verify symlinked destination parents using platform-native path resolution. Preserve the Linux `symlink/..` staging regression as a platform-specific case. Exercise a direct symlinked parent on Windows where symlink creation is available. |
| A-004 | Pin LF checkout endings for the canonical and packaged schema files with path-specific Git attributes, preserving the exact-byte schema check. Verify a fresh checkout with `core.autocrlf=true` and confirm the installed schema still matches the canonical DDL. |

Run the Linux SQLiteICUex suite and both standard-SQLite rejection checks. Confirm collection and sequential execution of the affected tests on Windows with Python 3.14.5 and pytest 9.0.3 when that host is available, and record native and simulated checks separately. Keep the revision scoped to the tests and the two schema checkout paths.
