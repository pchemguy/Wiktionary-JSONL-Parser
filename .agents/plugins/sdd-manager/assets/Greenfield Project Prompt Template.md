# Greenfield Project Prompt Template

Replace the placeholders, then copy the prompt below.

Supply a GitHub token when existing authenticated tools cannot perform all required repository and tracking operations; omit the token line only when sufficient access is already available.

Git access and GitHub API access are separate. A token can address missing authentication or permissions; an unsupported adapter operation still needs another supported execution path, such as a direct API request. SDD Manager should report unsupported operations or missing permissions.

## Minimal Template

``````markdown
Help me develop the following project using $sdd-manager.

**Project repo and credentials**:

GitHub repository: https://github.com/{OWNER}/{REPO}
GitHub token: {FINE_GRAINED_GH_TOKEN}

**Project description**:

```
A browser-based Tetris game.
```
``````

## Extended Template

````text
Help me develop the following project using $sdd-manager.

GitHub repository: https://github.com/{OWNER}/{REPO}
GitHub token: {FINE_GRAINED_GH_TOKEN}

Throughout this conversation, I authorize the repository operations required by SDD Manager within the agreed project scope and available permissions, including branches, commits, pushes, merges and GitHub tracking updates. Do not request separate or repeated authorization for these operations. Preserve SDD Manager's required human document reviews and execution boundaries, and follow any later instructions that change this scope.

Enable and maintain GitHub tracking for phase labels, milestones and task issues. Apply sdd-manage’s phase activation workflow before implementing each eligible phase: create or reconcile its required tracking objects and verify their associations by readback. If this prerequisite cannot be satisfied, report the blocker and stop affected implementation.

Preliminary project description:

```
{PROJECT_DESCRIPTION}
```

````

