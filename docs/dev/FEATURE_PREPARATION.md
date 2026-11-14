# Parallel importer redesign preparation

## Identity and request

- Campaign `003_24f121f` starts at `24f121f3f328aa575d52121acaf079f83d5a7a5c` on `main`. Preparation branch `design-docs/003_24f121f-parallel-importer-redesign` returns to `main`. The intended implementation branch is `feature/003_24f121f-parallel-importer-redesign`, from the published preparation merge.
- Open an architectural redesign campaign based on the benchmarked parallel path. Keep the 10,000-line default. Schedule comprehensive prerelease review, fixes, and re-verification before the final campaign release.
- The affected main sources are the [project brief](PROJECT.md), [architecture](ARCHITECTURE.md), [decomposition](DECOMPOSITION.md), [specification](SPEC.md), and [delivery plan](PLAN.md). The [benchmark](reports/importer-performance.md#seven-concurrent-imports-with-ids-assigned-during-insertion) and [batch-size sweep](reports/importer-performance.md#batch-size-sweep-with-seven-concurrent-workers) supply the measured baseline.

## Current control

Interactive, one pass, with strict delivery. The request opens the campaign and schedules the release gate. The first stop is feature brief acceptance. All nine issues and their association with [milestone 9](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/9) were verified before the branch or documents were created. The repository already has the manual provenance scaffolding under `docs/ai-logs/`.

## Decisions and evidence

- The user's benchmark directions supply the starting scheme: byte-balanced chunks, fresh Windows-compatible worker processes, `os.cpu_count() - 2` workers, chunk-local progress, IDs assigned before merge, and run-wide abort on failure. The 10,000-line default is confirmed for this feature.
- FDOCS-006 and FDOCS-008 must schedule comprehensive review on the exact release candidate, repair of confirmed in-scope findings, and re-verification before final release. The user requested this release gate. Execution belongs to the eventual implementation and release range.
- FDOCS-001 establishes the campaign context. FDOCS-002 covers the brief and its first acceptance.
