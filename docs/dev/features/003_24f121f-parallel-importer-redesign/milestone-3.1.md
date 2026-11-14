# Milestone 3.1 — Run planning and worker execution

Worker policy tests cover exact fits, reduced worker counts, equality at the 1.5 limit, one-slot merge groups, and zero-slot confirmation. The Linux SQLiteICUex build exposes 100 attachment slots. A connection with a lowered runtime limit verified that bootstrap reads the effective limit. Byte partition tests cover long lines, one-byte and empty input, CRLF, a BOM, coincident boundaries, and an unterminated final line.

The worker tests confirm final entry and batch keys, the SQLite integer boundary, preserved duplicates and child references, progress after visible commits, and rollback on a batch-log insertion failure. Review traced the shared write path from the bounded line reader through mapping into a single batch transaction. Existing parameter-binding and parent-order tests exercise the same writer.

The SQLiteICUex suite passed with 87 tests and two expected skips for checks specific to standard SQLite. Ruff and mypy passed. Milestone 3.2 connects the worker to process supervision, merge, and publication.
