# Diagnose Vite development-worker loading failures

Load when a Vite-served module worker fails to start, especially from a Windows linked checkout. Follow the project's supported environments, browser policies and selected repair scope; this module does not select Vite, SQLite or a browser matrix.

## Context and manifestation

Reported case: Windows/CMD, npm run dev, TypeScript module worker, Vite 8.3.5 and sql.js 1.15.1 with local WASM; project Node requirement ≥24. The supplied case reports Chromium/Firefox checks on Windows and Linux. These are incident details, not plugin requirements or independently reproduced results.

SQLite Save/Restore used a worker; JSON ran on the main thread without that worker or WASM. JSON success therefore did not exercise SQLite's loading path. The generated `/@fs/<drive>:/…/sqlite.worker.ts?worker_file&type=module` entry returned HTML. The browser rejected its MIME type before worker execution or sql.js initialization; the application's wrapper reported “SQLite worker failed to communicate”. The project-relative entry returned compiled JavaScript.

Classify the observed HTML entry as a development-path/worker-bootstrap failure. It does not establish a sql.js codec defect or a general failure of all symlinks or Vite versions. The precise upstream canonicalization mechanism was not established.

## Diagnose before changing code

1. Record commit, browser, Node/Vite/library versions, launch command, dev versus built execution, and physical versus linked paths/drives.
2. Capture Console and Network evidence: worker URL, status, Content-Type and response body. Inspect the actual HTTP response, not source-mapped TypeScript.
3. Compare the generated filesystem entry with the project-relative entry. Require compiled JavaScript, rewritten imports and appropriate worker environment code. Then verify dependency and WASM requests.
4. Distinguish entry rejection, import failure, WASM fetch/initialization, worker protocol and data validation. A generic worker error alone identifies none of these stages. Diagnose optimizer-triggered page reloads separately.

## Apply a narrow resolution

Prefer launching from the physical checkout when that is an acceptable working path. Check the installed Vite version's documented worker-loading forms before adopting an internal route. If a source workaround remains necessary and the project route is independently confirmed, use it only in development and retain statically detectable production bundling.

The following factory and paths are illustrative; adapt them to the actual project. The `worker_file` query is a version-sensitive implementation detail, not a public compatibility guarantee. Verify it against the installed Vite version and retest on upgrades.

```ts
function createTaskWorker() {
    if (import.meta.env.DEV) {
        return new Worker(
            `${import.meta.env.BASE_URL}src/workers/task.worker.ts?worker_file&type=module`,
            { type: 'module' },
        );
    }
    return new Worker(new URL('./task.worker.ts', import.meta.url), {
        type: 'module',
    });
}
```

Replace the existing construction call with the factory. Preserve required lazy/local WASM loading, protocol, application deadlines and cleanup. Do not relabel HTML as JavaScript or disable filesystem/CORS protections. This bypasses the affected development entry route; it does not repair sql.js or guarantee linked-checkout support.

When logs establish that late dependency discovery causes re-optimization and reload, explicitly pre-bundle that dependency, for example `optimizeDeps: { include: ['sql.js'] }` in the reported case. This addresses a separate development failure; it does not fix an HTML worker entry.

## Regression proof and return

Select the project's required platforms/browsers and affected operations; do not add Windows, SQLite or two-browser coverage to unrelated projects. A Windows filesystem claim needs native Windows evidence. Coordinate fixtures/test design with **sdd-tdd**, checks with **sdd-verify** and authorized repairs with the active workflow.

1. Use isolated environments and fresh browser contexts/server optimizer caches. Vary only the route workaround; freeze versions, pre-bundling and data fixtures.
2. **Native reproduction:** compare physical and affected linked launches without interception. Capture the failing URL/MIME, then retest with the workaround. Report unavailable native reproduction explicitly.
3. **Deterministic model:** link an owned app copy's worker-source directory to trusted external source and return HTML only for the filesystem worker entry. Retain real project-route compilation, imports, worker and downstream runtime. Require the affected entry to be requested during the failing baseline; otherwise the fixture missed the condition.
4. **Fail → pass → remove fix:** reproduce the worker/MIME failure without the workaround, require successful exact-data operations with it, and fail again when only the workaround is removed. For the reported SQLite case, exercise first Save and Restore, unchanged session data on failure, successful JSON controls, independent inspection of SQLite downloads, lazy/local WASM, no reload/state loss and worker cleanup. Do not fake the Worker.
5. Check ordinary-path controls and the actual production build at root and any supported base path, including local worker/WASM assets. Test cold-cache optimizer reload separately from MIME rejection.
6. Keep owned fixtures outside watched source roots with narrow filesystem allowance. Derive UI assertion budgets from the actual application deadline plus bounded scheduling margin; preserve the application deadline rather than shortening it to fit a test.

Return evidence and the repair/blocker to the active workflow. Distinguish native reproduction, modeled failure, automated success and user confirmation in existing task evidence. Modeled HTML establishes regression sensitivity, not reproduction of an underlying Windows filesystem defect.

Sources: [Vite workers](https://vite.dev/guide/features#web-workers), [Windows cross-drive limitations](https://vite.dev/guide/troubleshooting#cross-drive-links-on-windows), [dependency pre-bundling](https://vite.dev/guide/dep-pre-bundling).
