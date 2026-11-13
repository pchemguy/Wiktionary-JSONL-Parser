# Shared Markdown style

Apply these rules whenever SDD Manager authors, revises or reviews Markdown. They cover all document types: main and feature development documents and focused children, active reports, README and guides, AGENTS.md, skill instructions and references, templates, release notes and hosted Markdown drafts. Direct skill calls use the same rules as coordinated workflows. Respect controlling human/project instructions; surface a real conflict rather than silently choosing an incompatible format.

## Document names

Use ARCHITECTURE and DECOMPOSITION for document references and normal prose case for concepts and activities. Preserve literal paths, identifiers and quotations.

## Heading separation

Place a blank line after every Markdown heading, including ATX (`#` through `######`) and Setext headings (text followed by an `=` or `-` underline). This applies before prose, another heading, a list, a table or a fenced block. Separate headings from preceding content with a blank line as well; the beginning of a document or template needs no leading blank line. A heading at the end of a file still has a following blank line.

## List separation

Place a blank line before and after each entire top-level, non-indented list. Treat its nested items and continuation blocks as part of that list. Do not require blank lines around nested lists or between ordinary list items; compact nesting is preferred when the content permits it. No leading blank line is needed when a list begins the document; a final list has a trailing blank line.

## Indentation and lists

Use spaces, never tabs, for Markdown structural indentation. Use **four spaces per indentation level**, including nested bulleted, numbered, mixed and task lists. Start a top-level list at its container's left margin; indent each child list four additional spaces relative to its parent. Keep siblings at the same indentation and preserve their intended parentage.

Use **exactly one ordinary ASCII space after each list marker**, at every nesting level: `- item`, `* item`, `+ item`, `1. item` and `1) item`. Do not pad markers with multiple spaces or tabs to align their text. In a task item such as `- [ ] task`, this separator is the space between the bullet and checkbox. Indentation before the marker still follows the four-space nesting rule.

Indent continuation paragraphs and nested blocks to stay attached to their list item. Normally this uses the next four-space level; when a wide ordered-list marker requires more space, use the smallest additional four-space level that reaches the item's content column. Do not trade valid Markdown attachment for a mechanically fixed absolute column. TASKS retains its phase/milestone/task checklist semantics with its owner; this reference supplies the common spacing rule.

````markdown
## Supported variants

- Linux
    - x64
        - Command-line launcher
    - arm64
- Windows
    1. Extract the archive.
    2. Start the launcher.

1. Prepare the package.
    - Verify its contents.

    Keep the checksum beside the package.

    ```text
    package.zip
    package.zip.sha256
    ```

2. Publish the verified assets.

````

## Code-block separation

Place a blank line before and after code blocks, including fenced and indented blocks. Apply this separation to blocks nested in list items as well, keeping them attached to their item. Blank separator lines do not change the code's contents or relative indentation. No leading blank line is needed when a code block begins the document; a final block has a trailing blank line.

## Literal content and templates

Apply the rules inside Markdown examples and templates intended to produce documents, including fenced `markdown`/`md` samples. Preserve literal source code, data and verbatim quotations according to their own syntax and fidelity requirements. Do not interpret a shell comment or Python string inside a code fence as a Markdown heading, or reindent YAML/Python as though it were a list. Adjust a nested code fence's Markdown container indentation when needed without changing its relative internal code indentation.

## Scoped review

Check heading separation, top-level list and code-block separation, single-space list-marker separators, and list nesting/continuations in the selected current documents and active records, using syntax-aware inspection or rendering where attachment is uncertain. Text searches help discover candidates but do not prove correct parsing. Check examples/templates as well as surrounding prose. Repairs remain with the authorized artifact owner; this convention does not authorize edits or introduce a new human acceptance gate, formatter or dependency.

Follow the [closed campaign record boundary](review-campaigns.md#closed-campaign-records). Closed records are excluded from routine style checks and repairs; consult them only for a specific historical need, without a maintenance obligation. Current source checks do not validate live agent behavior.
