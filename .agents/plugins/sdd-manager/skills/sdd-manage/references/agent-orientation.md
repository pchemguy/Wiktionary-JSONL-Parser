# Maintain a concise root AGENTS.md

During authorized SDD adoption/bootstrap, ensure root `AGENTS.md` provides accurate agent orientation. For main preparation, apply [DOCS-001](main-preparation.md#docs-001-initialize-root-guidance): copy the initial AGENTS template only when absent and preserve existing files unchanged at that checkpoint. Outside that initialization, create it if absent; otherwise read its controlling instructions and integrate required navigation without overwriting human-authored content. Coordinate maintenance when material project structure, check/setup commands, governing sources, active execution ownership or workflow constraints change, before finalizing the affected handoff/checkpoint. Respect explicit write/path limits; report a scope conflict rather than widening them. **sdd-orient** reads and reports missing/stale guidance without mutation.

## Plugin source and target-project entries

The SDD Manager source/package uses [PLUGIN.md](../../../PLUGIN.md) as its composition entry. Its source-only root AGENTS.md covers development and points to acceptance/AGENTS.md for contributor checks; neither contributor entry is shipped. This separation does not replace AGENTS.md in target projects: their existing controlling instructions and the adoption requirements below remain applicable.

## Required orientation content

| Slot | Content from actual project evidence |
| --- | --- |
| Purpose and locations | Established project purpose and real source, test and document entry points. |
| Governing inputs | Links to present PROJECT/design/SPEC/PLAN/layout/TASKS owners; state missing inputs only where relevant, without fabricating files or requirements. |
| Active ownership | A dedicated continuity section pointing to `docs/dev/HANDOFF.md` and coordinator recovery, plus current task/feature owner and archive transfer navigation. The handoff is a checkpoint; later owning records/Git supply the delta. No duplicated checklist or branch/HEAD snapshot in AGENTS. |
| Setup and checks | Declared and validated commands, working directory, supported environment/shell constraints and concrete evidence limits. Do not invent a command or claim an unrun setup is validated. |
| Workflow constraints | Durable verification, the [task commit contract](../../sdd-implement/references/completion-and-checkpoints.md#task-commit-contract) for task-list execution, scoped commit/publication and user stopping-boundary expectations under established authority; link detailed policy. |
| Instruction discovery | Read applicable nested instructions for selected paths. Explicitly load this file when the host does not discover it; promise no universal host-discovery mechanism. |

Keep operational instructions distinguishable from document navigation. Link detailed canonical rules instead of restating them. No secret, credential-file contents or transient helper/installation path belongs here.

Point routine orientation to current main owners and the active campaign, not a reading queue of earlier campaign documents. Historical identity/path discovery requires no content loading; read selected prior records only for a specific task need. Maintain root/current navigation within scope without rewriting a closed package's README, historical links or status.

## Preserve and reconcile

1. Read root/applicable nested instructions before editing. Establish file ownership, write scope and any symlink destination; do not follow symlinks to edit an external file/directory.
2. Reuse accurate existing content. Add or update only needed orientation within authorized scope, using a clearly bounded maintained section where that preserves manual content. Generated navigation cannot weaken controlling instructions or manufacture user decisions. Resolve genuine conflicts under the instruction hierarchy before the affected edit.
3. Check actual links, current owner/archive associations and declared commands against project evidence. Run relevant commands when selected verification requires them; otherwise label their evidence status accurately. Do not rewrite unchanged content or make a gratuitous commit on clean startup.
4. Include affected orientation in its owning preparation/implementation/steering/documentation checkpoint; commit, push and verify remote containment before handing off or advancing, under [per-commit publication](git-workflows.md#publish-each-commit). On interruption, inspect retained files/Git before resuming; preserve manual/unrelated work. Create nested AGENTS.md only for genuine path-specific guidance.

**sdd-docs** maintains concise instructions/navigation and command/link accuracy. **sdd-plan** accounts for physical ownership; **sdd-integrate-feature** updates active/archive owner navigation. **sdd-implement** and **sdd-steer** include affected orientation in their verified checkpoints. Governing-policy conflicts return to the owner; this maintenance reference does not redefine scope or approve source changes.
