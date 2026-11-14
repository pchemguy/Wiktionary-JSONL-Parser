# Parallel importer architecture

The [parallel importer](FEATURE.md) converts one local JSONL file into one SQLite database. It uses the existing mapping and SQLite schema. Workers read the original file and write independent SQLite databases. The importing process assembles the completed databases and publishes one output.

## Process and data ownership

| Participant | Responsibility |
| --- | --- |
| CLI or library caller | Supplies the source, destination, and import options to the importing process. |
| Importing process | Owns bootstrap, worker count and merge group decisions, partitioning, child process lifetime, staging, and final publication. |
| Worker process | Opens the shared input file for reading, owns one contiguous range of complete lines, and writes its own staged SQLite database. It assigns final IDs during row construction and reports its own progress after batch commits. |
| Merge, in the importing process | Opens the staged output as `main`, attaches completed worker databases read-only, and copies their rows into the staged output in source chunk order. |

The importing process probes the SQLiteICUex runtime and uses the effective attachment limit to plan the run. When workers exceed that limit, it warns before starting them and applies the [worker count and merge policy](FEATURE.md#worker-count-and-attachment-limit). With zero attachment capacity and multiple requested workers, a confirmed fallback uses the one-worker path. The importing process splits the file at complete line boundaries and passes each worker its byte range and chunk identity. Fresh Python processes own their file handles and SQLite connections on every supported platform. The process boundary carries configuration, progress, and diagnostics. Mapped rows move through the worker databases.

## Write and publication boundaries

A worker uses the shared decoder, mapper, and SQLite schema. It commits each batch and its log row together, with parent rows written before their dependents. Disjoint ID ranges let the merge copy the stored keys and their references directly. The importing process waits for successful worker exits before merging, so worker connections have closed before the merge reads their results.

When one worker processes the whole input, the importing process publishes that worker database directly. With multiple workers, it merges into a single staged destination, processing consecutive groups within the available attachment slots. Each group attaches its sources, copies parent and dependent tables with foreign-key enforcement, and detaches the sources before the next group. The destination becomes visible only after all groups succeed.

The importing process owns cancellation and cleanup. If a worker fails, it stops and joins the remaining workers before cleaning up. Any failure during worker execution or merging, including ID-range overflow, aborts the import and leaves the requested destination unpublished. Staging sits on the destination filesystem to support publication as a single file operation.
