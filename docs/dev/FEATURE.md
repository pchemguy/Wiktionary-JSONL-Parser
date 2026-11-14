# CLI total processing time

Report one total elapsed wall-clock duration after a successful CLI import. The duration covers the import call from startup through completion, including input handling, worker processing, assembly, publication and staging cleanup. A successful empty import also reports its duration.

Write the summary to stderr after the importer returns, following any batch progress and import warnings. Use seconds with three decimal places. `--no-progress` suppresses the duration and batch progress. Failed, interrupted and rejected invocations retain their usual diagnostics and exit status. The library API, database schema and import behavior are unaffected.
