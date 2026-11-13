# Browser development policy

Apply this policy before selecting or using browsers, including agent browser tools, project automation and remote/container facilities. Browser-independent work and document-only planning require no browser installation.

Selection and isolation rules are mandatory; capability checks apply only where relevant to the selected work.

## Browser selection

- **Project documents govern browser priorities, requirements and test coverage**, including objectives established with the user during document design. Apply the defaults below only to unspecified choices.
- **When a browser is needed and none is specified, prioritize Chromium.** Include Firefox in the default browser environment. This does not require every individual check to run on both; select checks from the task's acceptance criteria and documented matrix.
- **Other browsers are prohibited by default.** Use them when project documents explicitly define the corresponding priority or requirement. Do not select another browser simply because it is available.
- Use the project's declared automation framework and compatible browser builds. A browser target does not itself select Playwright or add supported platforms.

## Environment isolation

Use a dedicated environment with identifiable browser binaries and isolated profiles, caches and downloads. Its binary location must be assigned to the project, execution job or disposable container, with a known distribution/version compatible with the runner. Reuse an existing contained installation when these conditions are established; downloading again for each task is unnecessary.

Do not search for or use personal/system browser installations, attach to personal sessions, or reuse personal profiles, cookies or extensions. Do not install, replace or reconfigure a global browser. Keep generated binaries/state outside tracked source and production assets; add ignore rules for repository-local generated paths. Clean up only owned sessions and artifacts.

For agent tools and remote facilities, establish the browser identity, dedicated installation and isolated state before use. Tool availability or an isolated profile alone is insufficient. If those conditions cannot be established, treat that facility as unavailable and select a compliant alternative or report the affected browser work blocked.

## Setup

1. Inspect project documents, dependencies, lockfile, runner configuration and declared commands. Establish the required browsers, modes and capabilities for the actual execution host.
2. Provision missing assets from official browser/framework distributions within the authorized environment. Keep browser and runner versions compatible; preserve unrelated toolchains and caches. Host dependencies must remain within the authorized setup scope.
3. Configure binary/state locations consistently for installation and execution, including CI and separate tool processes. Follow the host's shell policies. Put setup sequences in temporary shell files with explicit failure handling; stop after a failed prerequisite before running dependent tests.
4. Exercise the actual project runner/application path. Retain reproducible setup commands, versions, installation location, launch mode and evidence limits in existing project documentation or task evidence.

## Playwright execution

When Playwright is selected, use the project's pinned runner and matching managed browser revisions. Use one absolute, dedicated `PLAYWRIGHT_BROWSERS_PATH` consistently for installation and every automation process; an unexamined per-user cache does not establish ownership. Firefox requires Playwright's managed patched build.

Default to Chromium headless shell for application execution, interaction, Canvas and screenshots; these capabilities do not require a visible GUI. Use full Chromium or headed mode only when project criteria require it. Separate checks supported by working modes from checks requiring a full-browser mode. When the execution environment prevents full-browser execution after bounded diagnosis and permitted recovery, checks requiring that unavailable mode are out of scope by default; continue authorized implementation, packaging and releases with working headless modes and feasible artifact checks. Report excluded full-browser behavior as unverified, not passed. Only an explicit human instruction retaining those checks despite the known limitation overrides this default; other feasible required checks remain required. Report the effective executable/mode.

Provision missing assets proactively from official distributions, approved mirrors or compatible version-matched official images. Verify artifact integrity and runner/host compatibility. Do not install unpinned tools merely to retry, use global branded-browser installers, disable TLS verification, guess mirrors or evade a host denial.

A Firefox content-sandbox override requires a diagnosed content-process environment issue and must be limited to trusted local application tests in a dedicated environment, consistent with project policies. Keep it process-local, document its scope and re-evaluate on host changes. If the required security boundary cannot be retained, use a compatible approved environment instead of changing host restrictions or silently dropping browser coverage.

Use finite operation timeouts and a whole-process deadline covering page/context creation and cleanup. Stop only owned processes on expiry and confirm disposition before retrying. Verify launch, repeated isolated context/page cycles, interaction, required rendering and teardown through the actual project runner/application.

## Verification and recovery

Select evidence required by the task and record effective versions/modes, settings, commands, outcomes and limits in existing task evidence.

| Capability | Evidence |
| --- | --- |
| Provisioning | Compatible binary, trusted distribution and valid downloaded artifacts; a successful HTTP response alone is insufficient. Exercise fresh owned provisioning when reproducibility is required. |
| Sessions | The repeated context/page lifecycle and teardown used by the actual suite. |
| Visible output | Inspect screenshots or suitable pixel/shape/glyph assertions when rendering matters; DOM text does not prove font or Canvas rasterization. |
| Native events | Exercise actual focus, visibility or input delivery where required. Keep modeled handler checks separate from native evidence; headless input does not prove OS-window focus behavior. |
| Application acceptance | Execute the relevant tests through the actual runner/server path. A synthetic page establishes environment capability; installation, launch and interactive agent browsing do not prove application acceptance or its automated harness. |

On failure, retain the attempted command and observed error. Classify the failing stage: download, integrity/extraction, revision, host dependency, launch, session/page, rendering or application. Investigate supported remedies within the browser requirements and isolation rules; record material substitutions and rerun affected checks. Do not repeat unchanged failures, re-download sound binaries for session errors or retry rejected escalation. Apply the unavailable-full-browser scope above without waiving other required coverage.

Report verified behavior, omissions, precise missing capabilities and tested alternatives separately. Missing evidence prevents the corresponding acceptance claim; explicitly excluded full-browser checks do not block the remaining authorized work or become phase/release dependencies. Preserve requested artifacts and correct agent-generated gates within the authorized scope. Real build defects and failed feasible required checks retain their affected-work gates.
