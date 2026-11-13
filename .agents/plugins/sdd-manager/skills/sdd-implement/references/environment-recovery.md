# Establish execution capabilities and recover blockers

Load for the selected technology's execution setup or when installation, provisioning or runtime behavior prevents the selected task/checks. Technical investigation stays with the affected execution workflow; **sdd-manage** coordinates decisions and scope under its recovery policy. A host policy denial follows [Git recovery](../../sdd-manage/references/git-workflows.md#platform-authorization-rejection); retain the pending operation rather than treating the denial as an installation obstacle.

## Establish applicable guidance

Inspect declared tooling, setup commands and applicable project instructions before dependent setup or diagnosis. Use maintained official guidance for the selected environment. Verification remains read-only unless repairs are separately authorized.

Before classifying missing target-OS execution as a blocker, apply [cross-platform artifact and native-verification scope](../../sdd-verify/references/check-selection.md#cross-platform-artifacts-and-native-verification). Unavailable native verification is excluded by default; continue feasible artifact work and the authorized implementation range without requesting another waiver. Distinguish an actual cross-build failure from an unavailable native runtime check.

## Investigate and return

1. Preserve valid partial work and record the exact attempted check, environment, artifact and observed failure. Distinguish missing tool/dependency, malformed download, incompatible executable, runtime configuration and insufficient evidence.
2. Inspect declared setup/check commands and actual requirements. Validate the artifact's format/content and executable compatibility rather than trusting HTTP success or a package-install exit code. Avoid exposing secrets or modifying unrelated tooling.
3. Investigate reasonable supported alternatives within the existing scope: another supported distribution/source, declared compatible tool version, configuration or test facility. Match the alternative to the required capability and record why it is suitable. Respect network, filesystem, project and host constraints; no transport/account switching to evade a denial.
4. Select representative probes from **sdd-verify**'s capability-based check selection. Installation success or one trivial launch establishes only that narrow result. Repeat affected checks after a material environment change, preserving the actual evidence boundary.
5. Return the working alternative or remaining blocker, attempts/outcomes, substitutions, constraints and coverage to the manager. A substitution that changes accepted behavior, supported platform, trust/source requirements or required evidence needs the established decision process. Bound investigation by concrete scope, costs and constraints; do not invent an arbitrary retry quota or keep retrying unchanged failures.

For a browser blocker, follow the project's browser development policies and declared setup; any alternative must preserve their constraints and required acceptance coverage. CLI/engine-only tasks do not acquire browser, font or Canvas prerequisites.
