# Comprehensive review revision report

Campaign `010_380e014` reviews baseline `380e014b5118ab34c7a292c43be0fc3120440abc` and targets `main`. See the [review report](REVIEW-REPORT.md) for original observations and the [revision plan](REVISION-PLAN.md) for acceptance checks.

## V-001 — Windows launcher

R-001 is corrected. The launcher uses its checkout, preserves the adjacent-file default, accepts explicit CLI arguments, and scopes environment changes to its own execution. A copied launcher can select the checkout with a root override. The previous source failed the workstation-path assertion. The corrected source passed the static checks, and equivalent uninstalled CLI invocation from a separate directory worked with spaces in both the source checkout and input path. Native CMD execution is unavailable here.

## V-002 — Manual merge publication

R-002 is verified. The manual merge prepares the closed database in same-filesystem staging before calling the importer's no-overwrite publication. The regression failed in all three baseline cases because the output was already visible. On the corrected tool, success preserved keys and source bytes, a duplicate key left no destination, and a simulated competitor retained its contents. All 11 manual merge and importer assembly tests passed.
