# Comprehensive review revision plan

Campaign `010_380e014` started at `380e014b5118ab34c7a292c43be0fc3120440abc` and returns to `main`. The [review report](REVIEW-REPORT.md) records the baseline observations. The request authorizes corrections to confirmed findings and a patch release for codebase changes.

| Action | Finding | Correction | Recheck |
| --- | --- | --- | --- |
| V-001 | R-001 | Make the Windows no-install launcher select the checkout relative to its own location. Keep the adjacent JSONL as its default and forward supplied arguments to the CLI. Document the runtime and usage. | Inspect environment scope, path quoting, default input, argument forwarding and exit status. Exercise equivalent checkout-based CLI usage on Linux and report native Windows availability. |
| V-002 | R-002 | Stage the manual merge in the destination directory and publish with the importer's existing no-overwrite operation only after success. Preserve schema validation, row order and the single copy transaction. | Verify the output stays hidden during the merge, success preserves all rows, and a duplicate key or concurrent destination leaves no partial output. |
| V-003 | R-003 | Use shared worker cancellation in the benchmark. Preserve the initial failing chunk and reap the other children when signalling races or raises. | Reproduce the signalling race before repair, rerun it afterward, and exercise normal and malformed-input benchmark runs. |
| V-004 | R-001–R-003 | Package and publish patch version 0.4.2 from the verified merge into `main`. | Run the full suite and static checks, verify wheel and source distribution construction, run installed CLI/tool checks, and verify complete hosted inventory and downloaded checksums. |

The importer, schema and mapping contracts remain applicable. Repairs are confined to the three tools, their documentation and regression coverage, and release metadata. Keep the original observations and record rechecks in a separate revision report. Publish each verified action before proceeding.
