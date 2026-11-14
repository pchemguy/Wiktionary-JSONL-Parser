# Comprehensive review revision report

Campaign `010_380e014` reviews baseline `380e014b5118ab34c7a292c43be0fc3120440abc` and targets `main`. See the [review report](REVIEW-REPORT.md) for original observations and the [revision plan](REVISION-PLAN.md) for acceptance checks.

## V-001 — Windows launcher

R-001 is corrected. The launcher uses its checkout, preserves the adjacent-file default, accepts explicit CLI arguments, and scopes environment changes to its own execution. A copied launcher can select the checkout with a root override. The previous source failed the workstation-path assertion. The corrected source passed the static checks, and equivalent uninstalled CLI invocation from a separate directory worked with spaces in both the source checkout and input path. Native CMD execution is unavailable here.

## V-002 — Manual merge publication

R-002 is verified. The manual merge prepares the closed database in same-filesystem staging before calling the importer's no-overwrite publication. The regression failed in all three baseline cases because the output was already visible. On the corrected tool, success preserved keys and source bytes, a duplicate key left no destination, and a simulated competitor retained its contents. All 11 manual merge and importer assembly tests passed.

## V-003 — Benchmark worker cleanup

R-003 is verified. The benchmark delegates cancellation and reaping to the importer's shared routine, preserving the first exception and attaching cleanup errors as diagnostic notes. Both regressions failed on the baseline with a masked primary exception. Both passed after the fix. The affected supervision and release regression suite passed. A real seven-worker benchmark succeeded on the fixture. A malformed input failed with the chunk diagnostic and left neither a destination nor an owned staging directory.

## V-004 — Patch release verification

Version 0.4.2 retains the 0.4 minor version. The release builds include the repaired launcher and tools in the source archive. All 137 SQLiteICUex tests passed, with the two standard SQLite checks passing separately. Ruff lint, formatting, and mypy passed. The executed asset gate passed all 38 vectors, and both staged asset names and the ZIP checksum passed.

The installed wheel built and queried a fixture with SQLiteICUex, reported elapsed time by default, and suppressed output in quiet mode. The benchmark and manual merge executed from the extracted source archive against the installed wheel, and the output passed integrity and foreign-key checks. The wheel rebuilt from that source archive matched byte for byte. The converter sources and mapping and schema contracts match the full-extract baseline. Native Windows execution remains unverified.
