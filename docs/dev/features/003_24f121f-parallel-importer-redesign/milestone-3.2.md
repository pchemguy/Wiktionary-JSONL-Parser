# Milestone 3.2 — End-to-end parallel import

Fresh Python subprocesses ran the installed worker module on Linux. Tests observed progress on the calling thread, verified decoded failure and unexpected exit diagnostics, cancelled a sleeping sibling, and checked that every owned child was reaped. Grouped merge tests cover single-source and multi-source groups and copy the complete schema with SQLite foreign-key enforcement. Direct publication bypasses merger setup with one worker. Publication tests cover a concurrently created destination and staging cleanup after worker, merge, and publication failures.

CLI checks verify the 10,000-line default, per-chunk progress on stderr, quiet operation, and interactive acceptance, refusal, EOF and noninteractive input with zero attachment capacity. Warning, confirmation and progress callback exceptions leave no destination. Both missing-collation checks passed using standard SQLite. The installed console command and library call produced identical SQLite database bytes from a separate working directory.

The Linux SQLiteICUex suite passed with 103 tests and two standard-SQLite-only skips. Lint, formatting checks and type checks passed. The subprocess protocol runs without fork or POSIX-only process and pipe APIs. Windows-native execution remains to be verified on a Windows host.
