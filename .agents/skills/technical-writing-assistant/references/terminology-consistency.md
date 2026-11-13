# Terminology consistency

## Scope and authority

Reconcile terms, definitions, abbreviations, notation, naming, units, and recurring expressions across inspected material. Use for focused consistency checks or substantial revision. Consistent repetition does not establish technical correctness; do not merge distinct concepts for stylistic variety.

## Inputs and missing information

Use the text, supplied glossary or standards, project naming, audience, and scope. Treat authoritative definitions and identifiers as protected. If two apparently synonymous terms may denote different concepts, inspect context or ask before global replacement. Without full-document access, report the checked boundary.

## Procedure

1. Extract recurring concepts and candidate inconsistencies. For substantial work, maintain a compact record: concept, preferred term, definition/source, permitted variants, and unresolved decisions. For a paragraph, inspect directly.
2. Identify authority and usage: user instructions, applicable house/project terminology, inspected standards, source definitions, and conventional usage. Do not invent a standard or override a formal name from model recollection.
3. Distinguish true variants from different concepts: latency versus throughput, accuracy versus precision, risk versus uncertainty, or similarly consequential pairs. Explain distinctions where needed.
4. Reconcile abbreviations. Expand unfamiliar forms at first relevant use; consider independently read sections. Use consistent expansions and plural forms, avoid unnecessary acronyms, and provide a glossary where it helps.
5. Check symbols, variable names, units, prefixes, capitalization, subscripts, and numerical conventions. Conversions require a verified basis and correct arithmetic, not just consistent typography. Do not change code identifiers or equation variables without corresponding authorized changes.
6. Check names and definitions across headings, prose, tables, captions, figures supplied for inspection, examples, and references. Preserve official names and quotation wording. Identify contradictions rather than choosing one silently.
7. Apply targeted replacements in editable prose, accounting for grammatical form and context. Avoid blind global substitution; recheck every consequential occurrence and cross-reference.
8. Report unresolved technical correctness questions separately. Use [evidence review](evidence-review.md) for support or [software documentation](software-documentation.md) for identifier/implementation alignment when relevant.

## Outputs

Return corrected text or located findings, with a terminology record only if useful. Explain consequential normalizations and concepts deliberately kept distinct. Report unavailable figures or omitted sections as limits, not inspected consistency.

## Examples and failure handling

- A document defines "MFC" as mass-flow controller, then uses it for mass-flow control. Confirm whether the device or operation is intended before standardizing.
- "Response time" and "throughput" are not interchangeable. Repeating either does not justify replacing it with the other for variety.
- `process_batch` in code must not become `processBatch` because prose uses camel case elsewhere.
- "m" and "mm" cannot be normalized by changing the unit symbol alone; the value must be converted with a justified basis.
- If a formal standard's terminology conflicts with author shorthand, propose the resolution and explain its effect rather than assume a source from memory is authoritative.

## Completion checks

The same concept uses stable wording, different concepts remain distinct, abbreviations and notation are traceable, and protected names survive. Changes are context-sensitive, not blind substitutions. Technical correctness and consistency claims remain separate.
