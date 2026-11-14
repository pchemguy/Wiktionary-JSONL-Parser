# Edition boundary amendment

Revision `005_d0f14dd` branched from `d0f14dd30c12fd778d003e3336605ed325abfada` on the paused `feature/003_24f121f-parallel-importer-redesign` branch after T-019. It establishes the internal edition contract before T-020.

The importer resolves one edition. Fresh workers receive the edition identifier, and assembly receives the selected definition. The Russian package owns mapped-table DDL, record mapping and parent-first parameterized inserts. The shared pipeline creates and commits `batch_log` with the same keys and tuple values as before. The CLI and library continue to convert the Russian edition with their existing signatures.

A focused test used different table names, fields and dependencies to verify the worker and merger independently of the Russian definition. The Russian tests cover exact assembled DDL, subprocess arguments, merge, transaction behavior, and the established CLI and library. The SQLiteICUex suite passed 105 tests. Both tests skipped on that runtime passed separately with standard SQLite. Ruff, format checks and mypy passed. Installed CLI and library output matched byte for byte, and both standalone tools ran with the refreshed wheel. The wheel and source distribution include the edition resources. Package and release-bundle checks passed.

The [refreshed candidate](../../../../../features/003_24f121f-parallel-importer-redesign/candidate.md#candidate-after-the-edition-boundary-amendment) records the pinned product tree, packages, unchanged Russian output and repeated full-sample timing. T-019 remains complete with refreshed evidence. T-020 is the next task, and the comprehensive review, its corrections, and release remain pending. Execution evidence is from Linux.
