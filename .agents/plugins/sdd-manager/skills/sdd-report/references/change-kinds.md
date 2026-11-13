# Change kinds and evidence

Start with the actual outcome, reason, checks performed, and result. Select only the fields that improve understanding of this change; the labels below are examples, not a fixed questionnaire. Keep a planned issue in future or acceptance language and a completed report in past or present evidence language. The icon column offers optional PR title prefixes when the project uses them.

| Icon | Kind | Add to the shared core when relevant | Evidence boundary |
| --- | --- | --- | --- |
| ✨ | Feature or behavior | User-visible capability, changed contract, acceptance conditions | Distinguish specified behavior from verified implementation. |
| 🐛 | Bug fix | Reproduction, cause, affected behavior, regression check | Say whether the original failure was reproduced. |
| 🧹 | Code health or refactor | Maintainability problem, preserved behavior, ownership or coupling improvement | Cite checks supporting behavior preservation; do not promise it without evidence. |
| ⚡ | Performance | Baseline/current measurements, input size, environment, method, relative change | State uncertainty, simulated conditions, or absence of a meaningful gain. |
| 🔒 | Security | Risk, affected guarantee, solution, regression checks | Avoid credentials and unnecessary exploit detail; distinguish mitigation from proof. |
| 🧪 | Testing | Gap, added scenarios, coverage or failure-path result | Describe scenarios rather than inventing a coverage percentage. |
| 📝 | Documentation | Audience, corrected guidance, links or examples reviewed | Do not claim runtime verification for a text-only check. |
| 🔧 | Build, packaging, or tooling | Affected environments, reproducibility, installation or build checks | Name platforms actually exercised and those still untested. |
| 🔄 | Integration or migration | Cross-component effect, compatibility, transition and rollback conditions | Identify data or API assumptions and the checks that exercised them. |

Choose the dominant change; an icon does not certify the work.

Use these labels when relevant to the requested report and the project's style:

| Icon | Label | Domain | Description |
| --- | --- | --- | --- |
| 🎯 | What | | Actual or intended change. |
| 💡 | Why | | Underlying need or governing rule. |
| ✅ | Verification | | Commands, inspection, and outcomes actually observed. |
| ✨ | Result | | Supported effect and limitations. |
| 📊 | Measured Improvement | Performance | Baseline and current measurements, method, environment, and uncertainty; only when measured. |
| ⚡ | No meaningful gain | Performance | State upfront in a PR or completion summary; explain the rationale. |
| ⚠️ | Risk | Security | Potential impact and remaining exposure. |
| 🛡️ | Solution | Security | Mitigation, how it addresses the risk, and relevant checks. |
| 📊 | Coverage | Testing | Prior gap, added scenarios, and coverage evidence. |

## Examples

These illustrate completed-summary formats. Their details are scenario-specific and must be replaced with evidence from the current task.

### Code health

```markdown
- 🎯 **What:** Renamed `common.py` to `fs.py` and documented its filesystem responsibility in the layout.
- 💡 **Why:** The project assigns each module a focused owner and disallows generic dumping-ground modules.
- ✅ **Verification:** Inspected the updated layout and references, ran layout checks, and passed `pytest tests/unit`.
- ✨ **Result:** Shared filesystem utility ownership is explicit; the cited checks support behavior preservation within their scope.

```

### Performance

```markdown
- 🎯 **What:** Used `array.frombytes()`, `array.tobytes()`, and `array.byteswap()` for little-endian unsigned 64-bit conversion.
- 💡 **Why:** Big-endian hosts need the little-endian format without slow per-item packing and unpacking.
- 📊 **Measured Improvement:** In an ad-hoc simulated big-endian run of one million values, decode fell from 0.154 s to 0.008 s (reported as roughly 18×), and encode from 0.415 s to 0.013 s (roughly 30×). The simulation and rounded values limit the claim.
- ✅ **Verification:** The local timing script measured speed only; portability and round-trip correctness still need separate checks.

```

For omission or recovery reports, separate instruction, actual user grant/choice, observed state, failure cause and evidence limits. Cite the actual basis for a diagnosis; an agent-authored inactive-mode line is not a user refusal, and a supplied token is not confirmation of an optional capability.
