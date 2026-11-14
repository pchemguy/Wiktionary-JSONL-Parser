# SQLite attachment limit revision report

Campaign `004_1c1297a` opened in `e07a89e9e99ef48eb1bd8acad18e53aa023f9c68` from the [parent feature checkpoint](../../HANDOFF.md) at `1c1297a5181cfac3ed1492904061ba3afcc4ad19`. The [revision plan](REVISION-PLAN.md) defines the one documentation action.

A-001 adds `-DSQLITE_MAX_ATTACHED=100` to the compilation of `sqlite3.c` in the [Linux setup recipe](../../../linux-sqlite-icuex-setup.md). The recipe describes omitting the flag for SQLite's default and includes verification through Python's `Connection.getlimit()`.

Recompiled and linked the recipe's pinned SQLite 3.54.1 and SQLiteICUex sources on Debian 13 with ICU 76. A private copy of the validated CPython 3.12.14 installation was pointed at the rebuilt shared library. The documented checks passed for the project schema, ICUex collations, and attachment limit of 100. A separate probe attached 100 in-memory databases and rejected the 101st. The full CPython build was reused for this check.

The revision returns to `design-docs/003_24f121f-parallel-importer-redesign` at the parent's pending feature brief acceptance.
