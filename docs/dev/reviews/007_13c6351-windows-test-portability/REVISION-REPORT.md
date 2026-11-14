# Windows test portability revision report

Campaign `007_13c6351` started from `main` at `13c63511ebe5b57a3ac791c660c3dcf64e6ef007`. See the [revision plan](REVISION-PLAN.md) for the supplied Windows evidence.

## A-001 — Test IDs and subprocess environment

The Linux run used pytest 9.0.3 to reproduce the two oversized node IDs at 300,061 and 300,055 characters. An isolated test runner enforcing the Windows environment-variable limit reproduced four setup and teardown errors and the downstream persistence-test setup failure. With explicit IDs, all seven partition cases and the following persistence test passed under that same limit. The persistence case also passed when selected directly.

The suite-wide `PYTHONPATH` fixture and a redundant environment copy in an isolated child launch were removed. The worker provenance regression and three supervision tests passed with pytest 9.0.3. The runner's dependency path is scoped to the test command. Native Windows execution has not been performed.
