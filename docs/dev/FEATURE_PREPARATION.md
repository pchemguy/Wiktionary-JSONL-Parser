# Skip redirect records preparation

## Identity and request

- Campaign `008_984ad61` starts at `984ad613614670f969df054c60bf56f6b494ada2` on `main`. Preparation branch `design-docs/008_984ad61-skip-redirect-records` returns to `main`. The intended implementation branch is `feature/008_984ad61-skip-redirect-records`, created from the published preparation merge.
- The user requested a feature campaign to skip redirect records and explicitly required IDs to count skipped records for source mapping.
- The [current specification](SPEC.md), [architecture](ARCHITECTURE.md), [decomposition](DECOMPOSITION.md), [Russian mapping contract](spec/mapping.md), [delivery plan](PLAN.md), and [implementation tasks](TASKS.md) establish the baseline.

## Current control

Interactive, one pass, with strict delivery. The first stop is the feature brief approval. All nine issue identities and associations on [milestone 14](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/14) were verified before creating the branch or documents. Existing manual provenance scaffolding is present under `docs/ai-logs/`.

## Decisions and evidence

- Scanning the complete extracted Kaikki Russian dump found 2,729,136 records. All 1,002,924 records with a top-level redirect had keys `title`, `redirect`, and `pos`, a string target and `pos` of `hard-redirect`. None had `word`, `lang`, or `lang_code`. The downloaded gzip SHA-256 is `fdcb978c76b660e0e43977bbf7487c812e6d42e965b0a73e3f5b4ba6981174c4`.
- The unfiltered CLI failed on a standalone redirect. Filtering those records out of a separate input allowed the existing importer to commit all 1,726,212 entries. The feature should handle those source lines in place so later entry keys retain their original chunk and line positions.
- FDOCS-001 establishes the campaign context. FDOCS-002 owns the brief and its first acceptance.

## Brief proposal

- FDOCS-002 published [the feature brief](FEATURE.md) at Git blob `a918c00e1b220942e1dc96bc2b3ecc8a657662ac` for approval. The user confirmed source-position ID numbering, including skipped lines.
- The proposal uses the classification already exercised on the full extract: a top-level string `redirect` and none of the three entry keys. Mixed or malformed records continue under normal validation. Redirects count toward source-line batching, the chunk line limit, and byte progress. Redirect-only batches keep the batch log.
- Validate the feature on mixed records, redirect-only batches and files, valid and invalid edge cases, and the original unfiltered full extract. Architecture and implementation decisions follow brief acceptance.

- FDOCS-002 accepted the published brief (blob `a918c00e1b220942e1dc96bc2b3ecc8a657662ac`). The user approved all remaining checkpoints. Continue the interactive preparation workflow under that preapproval through package QC and preparation integration.

## Design and specification decisions

- FDOCS-003 reuses the [main architecture](ARCHITECTURE.md). Redirect classification belongs to the selected edition inside the existing worker and does not change process roles, ownership of line positions, the merger, or publication. No architecture overlay is needed.
- FDOCS-004 accepted the [feature decomposition](FEATURE-DECOMPOSITION.md) under preapproval. The optional edition predicate keeps format knowledge out of the shared worker. Classification follows decoding and position accounting and precedes mapping. The benchmark shares this worker and must use source-line counts for its rate.
- FDOCS-005 accepted the [specification](FEATURE-SPEC.md) and its [review](FEATURE-SPEC-REVIEW-REPORT.md) under preapproval. The exact rule includes empty redirect strings and treats null entry fields as present.
