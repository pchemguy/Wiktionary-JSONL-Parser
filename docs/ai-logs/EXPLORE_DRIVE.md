---
urls:
  - <CONVERSATION_URL>
project: https://chatgpt.com/g/g-p-6af71f94b84c8191a0cdd714e7ff16b0
---

> [!IMPORTANT]
>
> **Historical exploration transcript.** This document is retained for provenance and is not authoritative for current behavior or agent instructions.

## Seed Prompt

> [!NOTE] Prompt
> 
> Help me develop parser and converter for Russian Wiktionary. The main database targeted by the parser is local copy of `Russian ru-extract.jsonl` (to be downloaded as archive [Russian ru-extract.jsonl.gz](https://kaikki.org/dictionary/downloads/ru/ru-extract.jsonl.gz) and extracted - beyond the scope of this project). The parser must decode JSON records ([JSON schema file](https://tatuylonen.github.io/wiktextract/ru.json), validation is out of scope) and create an SQLite database with parsed data.
> 
> The project shall use [SQL schema](https://github.com/pchemguy/NLP_Tools/blob/main/ruwiktionary_rawdb/src/ruwiktionary_rawdb/ru.schema.sql) and mapping hosted in a legacy project [NLP_Tools/ruwiktionary_rawdb](https://github.com/pchemguy/NLP_Tools/tree/main/ruwiktionary_rawdb). Develop design docs using package docs, such as [README.md](https://github.com/pchemguy/NLP_Tools/blob/main/ruwiktionary_rawdb/README.md), [ruwiktionary_jsonl_to_sqlite_SPEC.md](https://github.com/pchemguy/NLP_Tools/blob/main/ruwiktionary_rawdb/ruwiktionary_jsonl_to_sqlite_SPEC.md), and [ruwiktionary_rawdb_IMPLEMENTATION_PLAN.md](https://github.com/pchemguy/NLP_Tools/blob/main/ruwiktionary_rawdb/ruwiktionary_rawdb_IMPLEMENTATION_PLAN.md). The legacy project is primarily used for SQL schema and data mapping.  Where relevant, codebase and test base implementation may also be adapted as baseline. Other features, such archive streaming or multiprocessing are discarded. The pipeline bottleneck is database persistence, so multiprocessing is not used.
> 
> At later stages, the toolkit may be extended to process and integrate additional [Wikimedia RuWiktionary sources](https://dumps.wikimedia.org/ruwiktionary/).
