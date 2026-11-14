# Milestone 5.1 — CLI timing and verification

The CLI now measures its synchronous import call with a monotonic clock and reports a single successful elapsed time to three decimal places on stderr. It reports after progress and publication. Quiet mode suppresses the line and the batch updates. Failures, interruption and help omit the timing line.

The new timing expectations failed against the original CLI and passed with the change. Deterministic tests verify exact formatting, an existing destination at the end clock read, normal batch ordering, empty and redirect-only inputs, quiet mode, failed batches, interruption, and help. The full Linux SQLiteICUex suite, Ruff and mypy passed. The library continues to run silently without a callback.
