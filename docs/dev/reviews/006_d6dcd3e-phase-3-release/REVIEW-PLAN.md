# Phase 3 prerelease review

Review the 0.3.0 product tree `d3e1ceba4b866f9f08c987b8588316e84b682074` and the exact packages pinned in the [candidate report](../../features/003_24f121f-parallel-importer-redesign/candidate.md#candidate-after-the-edition-boundary-amendment). Campaign baseline is `d6dcd3e7e49482e95888494a333da04ea44e7d86`.

| Area | Checks |
| --- | --- |
| Import contract | Trace bootstrap, edition selection, framing, stable IDs, parent-first writes, progress, grouped assembly and direct publication through specification, code and tests. |
| Process and file boundaries | Exercise startup from installed code, termination and reaping, path resolution, destination races, cleanup, diagnostics, and both library and CLI entry points. |
| Output and performance | Verify exact schema, field and ID semantics, translated serial comparisons, SQLite integrity, and full-size timings. |
| Documentation and distribution | Check README, build recipe, CLI/tool invocation, wheel and sdist contents and exclusions, inventory and hashes. Verify canonical document incorporation at phase review. |

Use the Linux SQLiteICUex runtime and its standard SQLite counterpart. Record Windows assessment and the absence of native Windows execution. The repository uses direct release publication. Review the bundled release tool and its naming gate. Preserve published historical campaign records.
