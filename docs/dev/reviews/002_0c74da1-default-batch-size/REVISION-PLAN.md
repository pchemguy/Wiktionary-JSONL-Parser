# Set the default import batch size to 10,000 lines

Campaign `002_0c74da1` starts at `0c74da116be8a6014c05835ad8aa6ecd508f80b7`. The revision branch is `revision/002_0c74da1-default-batch-size`, created from `main` for integration back into `main`.

The user authorized this focused change and campaign closure. `A-001` sets the CLI default to 10,000 source lines per batch and updates help, the README, the [current specification](../../SPEC.md), and the existing default-batch-size test. Explicit batch-size overrides remain supported.

Verify the default through the CLI tests, check the generated help, and run the import regression suite. Confirm the actual batch counts on the local Kaikki entry sample with the batch-size argument omitted.
