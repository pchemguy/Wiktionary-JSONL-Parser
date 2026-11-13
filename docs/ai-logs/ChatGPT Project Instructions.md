---
project: https://chatgpt.com/g/g-p-6af586bb7bc08191bcee9b798c23b57e
---
> [!IMPORTANT]
>
> **Historical exploration transcript.** This document is retained for provenance and is not authoritative for current behavior or agent instructions.

## 📗 ChatGPT Project Instruction

Use SDD Manager for project development. Where not explicitly requested otherwise, use the `autodoc` mode.

`https://github.com/pchemguy/Wiktionary-JSONL-Parser` is the authoritative home for this project, including all supporting project artifacts. As the project agent, create, revise, and maintain codebase, tests, project files, documentation, concise repository onboarding instructions (e.g., AGENTS.md), and any other applicable project artifacts directly in the repository. For GitHub tracking and other operations not supported by any available GitHub connector, use this GitHub token:

{FINE_GRAINED_GH_TOKEN}

Use `tools/` at the repository root as the default location for project tools, utilities, and support scripts. Include documentation with each tool by default. Explain its purpose, how to run it, and what inputs, outputs, dependencies, or side effects users should expect, where applicable. Keep the documentation current when behavior changes.

### Project Description



### Versioning and releases

Manage the project's versioning, choosing an appropriate initial version and increasing it to reflect delivered changes. After each implementation phase is completed, verified and integrated, create and publish a new GitHub release with the corresponding version tag and release notes.

### Design clarification

During preparation, resolve important interactions and boundary cases. Surface decisions that materially affect runtime application behavior and user interaction before implementation.
