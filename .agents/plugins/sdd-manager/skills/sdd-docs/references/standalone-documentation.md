# README and standalone documentation

Identify the intended reader and selected documentation targets. Follow the project's layout and documentation conventions. Maintain existing focused guides instead of duplicating their content in README or creating guides without a demonstrated need.

## Align content

| Area | Review |
| --- | --- |
| README | Project purpose, supported capabilities, prerequisites, installation, quick start, examples, limitations, and links to deeper documentation. |
| Usage and configuration | Actual API or CLI behavior, option names, defaults, units, required inputs, and relevant examples. |
| Development guidance | Declared setup, build, test, documentation, and packaging commands; contribution guidance when present. |
| Troubleshooting | Supported diagnosis and corrective steps for documented failure cases. |
| Migration guidance | Verified compatibility changes, affected users, transition steps, and limitations when relevant. |
| Navigation and structure | Valid paths and links, discoverable entry points, coherent headings, and focused ownership of detailed explanations. |

Align README and guides with accepted scope and the supported implementation. Label planned or incomplete capabilities explicitly. Keep important limitations visible where users make decisions. Report conflicts that require changes to governing design, SPEC, PLAN, or layout to the user rather than resolving them through a documentation rewrite.

## Examples and checks

- Verify snippets against actual imports, signatures, options, paths, and prerequisites. Use current project facts rather than copying scenario-specific details from another project.
- Run examples or relevant documentation checks where practical within the authorized environment. Distinguish inspected examples from executed examples and record expected versus observed outcomes.
- Check local links and referenced files in maintained documentation and active records; assess external links when relevant to the requested work and access permits. Report links that could not be checked within that scope. Exclude closed campaign artifacts from current link validation and repair; do not report their compatibility with later changes.
- Remove stale references and unnecessary duplication within scope. Follow layout rules for placement; propose a layout amendment to the user if the required organization cannot fit them.
- Check the shared [Markdown style](../../sdd-conventions/references/markdown-style.md), including blank lines after headings and around top-level lists and code blocks, four-space list nesting, single-space marker separators, continuation attachment and Markdown examples/templates. Preserve embedded code/data syntax.

## Agent orientation

Apply the manager's [agent orientation](../../sdd-manage/references/agent-orientation.md) when material source/layout/check commands, governing links or active task/feature ownership changes within this workflow. Preserve controlling manual instructions and update affected root AGENTS.md with the verified owned checkpoint. Feature archive/transfer keeps current canonical owner links accurate; historical checklists are not duplicated as executable owners. Explicit path limits or real policy conflicts return to the manager. An unchanged startup requires no rewrite.
