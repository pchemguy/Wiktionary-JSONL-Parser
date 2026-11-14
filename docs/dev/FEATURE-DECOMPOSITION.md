# Redirect-skipping decomposition

The [main architecture](ARCHITECTURE.md) supplies the process and publication boundaries. The [main decomposition](DECOMPOSITION.md) supplies the existing edition, worker, and merger interfaces.

The Russian edition owns the standalone-redirect predicate. The edition definition may provide a predicate over a decoded object. Editions without one process every decoded object through their mapper. Each worker uses its selected edition's predicate after successful JSON decoding and before mapping. The worker advances its local source position and checks the ID range for every line, including a redirect.

The worker includes each accepted line in the batch line and byte counts. The existing batch writer commits the log row even when the batch has no mapped rows. The merger copies the resulting rows and logs using the existing table order. Chunk boundaries, worker startup, batching, and publishing use the same paths for both redirect-containing and entry-only inputs.

The parallel benchmark uses the same worker. Report source-line throughput using the number of processed source lines, available from the completed database's `batch_log`. Count imported entries separately if reported.
