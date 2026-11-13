# Skill and plugin discovery protocol

Discover and load repository-provided skill and plugin entries using the protocol below. Report their purposes and capabilities in chat according to the report template.

## Strict execution constraints

These constraints apply during discovery.

- **Read-only discovery and chat reporting only.** Do not create, modify or delete files.
- **No Git operations**, commits, pull requests or hosted-object changes.
- Load complete `SKILL.md` and `PLUGIN.md` entry instructions.
- Do NOT read `references/*.md` referenced from `SKILL.md`.
- Do NOT execute their workflows during discovery or treat loading an entry as authorization to act.
- Do NOT install packages.
- **Report discovery in chat.** Do not create a report file, commit or formal submission for discovery.

## Discovery procedure

All discovery paths below are relative to the repository root.

### Skill Discovery

Enumerate skill directories. For each `SKILL.md`:

- Load the complete entry and extract its declared `name` and `description`.
- Identify its capabilities and scope from that entry.

Apply to:

- Standalone skills
    - **Discovery root**: `.agents/skills/`
    - **Entry pattern**: `.agents/skills/{skill}/SKILL.md`
- Bundled skills for each plugin `{plugin}` during **Plugin Discovery**
    - **Discovery root**: `.agents/plugins/{plugin}/skills/`
    - **Entry pattern**: `.agents/plugins/{plugin}/skills/{skill}/SKILL.md`

### Plugin Discovery

Enumerate plugin directories `.agents/plugins/{plugin}/`. For each plugin:

- Read its manifest in full (`.agents/plugins/{plugin}/plugin.json` or vendor-specific) and extract declared `name`, `description`, and `displayName`, where present.
- Load `PLUGIN.md` in full when present. If it defines a coordinator skill, load its `SKILL.md` entry before other bundled skills.
- Apply the **Skill Discovery** procedure to `.agents/plugins/{plugin}/skills/`.

## Report template

The report should be generated in **chat only** using the following template. Use declared names for headings. Report absent categories explicitly; include only fields supported by the inspected sources.

```markdown
# Skill and plugin discovery report

## Standalone skills

### {skill name}

- **Path:** {actual repository-relative SKILL.md path}
- **Description:** {declared description}
- **Capabilities and scope:** {entry-derived summary}

## Plugins

### {plugin name}

- **Display name:** {when declared in manifest}
- **Manifest:** {actual repository-relative manifest path}
- **Description:** {declared description}
- **Shared entry:** {actual PLUGIN.md path or absence}
- **Coordinator skill:** {if defined in PLUGIN.md}
- **Capabilities and scope:** {concise PLUGIN.md-derived summary, when available}

#### Bundled skills

##### {skill name}

- **Path:** {actual repository-relative SKILL.md path}
- **Description:** {declared description}
- **Capabilities and scope:** {entry-derived summary}
```
