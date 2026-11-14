# Document the custom SQLite attachment limit

Campaign `004_1c1297a` starts at `1c1297a5181cfac3ed1492904061ba3afcc4ad19` on parent campaign `003_24f121f`. Revision branch `revision/004_1c1297a-sqlite-attachment-limit` returns to `design-docs/003_24f121f-parallel-importer-redesign`. The parent is paused at first brief acceptance.

Action A-001 documents the optional `SQLITE_MAX_ATTACHED=100` build setting in the [Linux SQLiteICUex recipe](../../../linux-sqlite-icuex-setup.md) and shows how to check the limit through the custom Python interpreter. Verify with the pinned SQLite and SQLiteICUex sources. The requested scope ends at nested revision closure and return to the parent checkpoint.
