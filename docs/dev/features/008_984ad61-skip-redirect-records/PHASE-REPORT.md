# Phase 4 — Standalone redirect handling

The Russian edition recognizes standalone redirect objects after decoding. Workers skip their mapping while retaining the original source position, batch counts and progress. CLI and library signatures and SQLite DDL are intact.

| Verification | Result |
| --- | --- |
| Classification and accounting | 17 new tests passed. Coverage includes mixed and redirect-only input, ID gaps and child keys, batch rows and progress, malformed records, and the chunk line limit. |
| Platform and regression | Linux ran 129 SQLiteICUex tests and the two separate checks against standard SQLite. Ruff and mypy passed. Native Windows execution remains unverified. |
| Full-extract import | The installed candidate read all 2,729,136 raw lines, imported 1,726,212 entries, and skipped 1,002,924 redirects. Every entry ID and batch row matched an independent source scan. All 19,062,746 mapped rows matched after aligning IDs. Progress completed for each chunk. Integrity and foreign keys passed. |
| Distribution | Installed CLI and library passed. The source archive rebuilt the tested wheel byte for byte. The release build verified the artifact inventory and checksums. |

See the [full-extract report](full-extract.md) for elapsed time, methodology, and candidate artifact hashes. The [main specification](../../SPEC.md), [decomposition](../../DECOMPOSITION.md), [delivery plan](../../PLAN.md), and [tasks](../../TASKS.md) incorporate the feature. The archived preparation documents preserve the approved design and evidence.
