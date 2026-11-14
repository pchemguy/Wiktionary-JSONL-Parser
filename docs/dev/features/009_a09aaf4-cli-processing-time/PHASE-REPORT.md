# Phase 5 — CLI processing time

The CLI measures elapsed wall-clock time around the synchronous import and writes one flushed stderr line after success. The interval includes assembly, publication, and cleanup. Quiet mode suppresses the line along with batch progress. The release is the patch increment from 0.4.0 to 0.4.1.

The [implementation review](milestone-5.1.md) records deterministic timing and regression coverage. Linux verification passed 132 SQLiteICUex tests and two separate standard-SQLite checks. The installed command verified normal, quiet, and failing imports, empty input, and help. The source archive reproduced the tested wheel byte for byte. The package inventory and checksums passed. Native Windows execution remains unverified.
