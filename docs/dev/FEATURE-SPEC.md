# CLI total processing time specification

The [existing CLI contract](SPEC.md) defines import invocation, warnings, diagnostics and exit status.

Use a monotonic elapsed clock immediately before and after the synchronous import call. Measure wall-clock duration across the whole call, including planning, workers, assembly, publication and staging cleanup. Argument parsing and printing the timing message are outside the interval.

After the call returns successfully, write and flush one line to stderr using `Total processing time: 12.345 s`, with the actual duration rendered to three decimal places. Report it for empty and redirect-only inputs as well. Preserve stdout as empty. With `--no-progress`, suppress batch progress and the timing line while retaining warnings and diagnostics. A failed import, interruption, invalid command line or help request does not emit the timing line. Library calls use the existing API and output behavior.
