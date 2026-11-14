# Comprehensive review plan

Campaign `010_380e014` starts from `380e014b5118ab34c7a292c43be0fc3120440abc` on `main`. The revision branch is `revision/010_380e014-comprehensive-review` and returns to `main`. The published comparison is v0.4.1 at `5c39fe13108f13f17b5d96c5590a7012583fdeaf`. The baseline includes a later Windows launcher example.

Review the maintained Russian-edition converter, public entry points and tools, and the release as downloaded. Inspect the current design, contracts, implementation, tests, setup and usage docs, and distribution configuration. Historical campaign packages and bundled development tooling are outside the converter review. They are inspected only where they affect current onboarding or the release package boundary.

| Unit | Scope | Evidence and scenarios |
| --- | --- | --- |
| U-001 | Converter and test coverage | Trace input, partitioning, mapping, IDs, transactions, worker coordination, merge and publication. Run the suite with SQLiteICUex and check missing-collation behavior with standard SQLite. Exercise relevant failure and equivalence cases. |
| U-002 | Consumer interfaces, tools and docs | Compare the CLI and library to the current contracts. Review setup, pytest guidance, and tool usage. Exercise documented examples and check maintained relative links. Windows launcher assessment is static on this Linux host. |
| U-003 | Distribution and hosted release | Check package build, asset naming, checksums, metadata, package boundaries, installed wheel and rebuilt source. Verify the published release against its own tag and check the reviewed baseline for release readiness. |

Commit and publish the report after each unit. Repair confirmed defects under the current contracts, rerun affected checks and the regression suite, and integrate the verified campaign. Codebase changes require a patch release. New product behavior and deferred features remain outside this request.

Review results will be recorded in `REVIEW-REPORT.md`.
