# Windows test portability revision report

Campaign `007_13c6351` started from `main` at `13c63511ebe5b57a3ac791c660c3dcf64e6ef007`. See the [revision plan](REVISION-PLAN.md) for the supplied Windows evidence.

## A-001 — Test IDs and subprocess environment

The Linux run used pytest 9.0.3 to reproduce the two oversized node IDs at 300,061 and 300,055 characters. An isolated test runner enforcing the Windows environment-variable limit reproduced four setup and teardown errors and the downstream persistence-test setup failure. With explicit IDs, all seven partition cases and the following persistence test passed under that same limit. The persistence case also passed when selected directly.

The suite-wide `PYTHONPATH` fixture and a redundant environment copy in an isolated child launch were removed. The worker provenance regression and three supervision tests passed with pytest 9.0.3. The runner's dependency path is scoped to the test command. Native Windows execution has not been performed.

## A-002 — Missing-input diagnostic

The Windows run showed Python's OS exception rendering the filename with escaped backslashes. A Linux pytest run with a literal backslash in its temporary directory reproduced the same assertion failure. The test now checks the exact filename representation used by the exception. It avoids localized error wording and still verifies the failure exit code, absent output and preservation of an existing destination. The focused regression and CLI suite passed.

## A-003 — Destination symlink coverage

The supplied Windows log shows the expected POSIX traversal result was absent. The test now exercises a simple symlinked destination parent on every platform that can create the link and exercises the original `symlink/..` case on POSIX. Each case checks that the output lands in the resolved directory and that staging is cleaned up. Both variants and the assembly regressions passed on Linux with pytest 9.0.3. The Windows path was assessed from the attached run and platform path semantics.

## A-004 — Exact schema line endings

In a disposable checkout with `core.autocrlf=true`, both SQL files checked out as CRLF and the exact schema assertion failed. Path-specific `text eol=lf` attributes made both files check out as LF with the same Git setting. The unmodified byte-for-byte assertion passed. A fresh wheel installation also matched the canonical DDL byte for byte, including the raw packaged schema resource.

## Verification

On Linux, CPython 3.12.14 with SQLiteICUex and pytest 9.0.3 passed 112 tests with two standard-SQLite-specific skips. Both skipped checks passed separately with standard SQLite. Ruff lint and formatting and mypy passed. The Windows environment-variable limit and CRLF checkout were reproduced separately. A native Windows rerun of the revision remains unverified.
