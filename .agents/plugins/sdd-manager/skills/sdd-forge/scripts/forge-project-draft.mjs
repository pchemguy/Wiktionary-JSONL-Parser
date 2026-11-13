/**
 * Local canonical-list-to-JSON draft authoring; Node >=22 and native Git.
 * No credential or hosted access. Phase semantic fields stay null; docs-main
 * copies fixed package content, preferring the repository's DOCS_TASKS owner.
 * Remote defaults to origin. Eligibility stays false. Stdout is default;
 * explicit output is exclusively created, never
 * overwritten. Before docs-main's pre-write gate, keep output outside repo.
 * See forge-project-input.md; this is not an activation or dependency engine.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fail, text } from './github-client.mjs';
import { createContext, inspectSource, inspectDocsSource, failure, isMain } from './forge-runtime.mjs';
import { parseOwner, draftProjection } from './projection-input.mjs';

const USAGE = 'phase|docs-main --repo PATH [--remote origin] [--tasks FILE] [--phase ID] [--output FILE]\ndocs-main defaults to docs/dev/DOCS_TASKS.md, or the bundled template when absent.';

/**
 * Parse explicit local authoring scope without I/O.
 * @param {string[]} args CLI arguments without executable/script.
 * @returns {object} Draft scope or standalone help.
 * @throws {Error} Safe invalid/missing scope classification.
 */
export function parseCli(args) {
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) return { help: true };
  if (!['phase', 'docs-main'].includes(args[0])) fail('invalid_operation');
  const result = { kind: args[0], remote: 'origin', timeoutMs: 30000 }, seen = new Set();
  const names = { '--repo': 'repo', '--remote': 'remote', '--tasks': 'tasks', '--phase': 'phase', '--output': 'output' };
  for (let i = 1; i < args.length; i++) {
    const name = names[args[i]], value = args[++i];
    if (!name || seen.has(name) || !text(value, 4096) || value.startsWith('--')) fail('invalid_arguments');
    seen.add(name); result[name] = value;
  }
  if (!result.repo || !result.remote || !/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(result.remote)
      || (result.kind === 'phase' && (!result.tasks || !/^[1-9]\d*$/.test(result.phase || '')))
      || (result.kind === 'docs-main' && result.phase !== undefined)) fail('missing_scope');
  return result;
}

/**
 * Produce an unapproved template; native root/remote identify the destination.
 * @param {object} options Parsed kind/root/remote/source and optional new output.
 * @returns {object} Draft JSON; phase semantics unresolved, docs content fixed.
 * @throws {Error} Native source/output failures; no hosted effects occur.
 */
export function run(options) {
  if (Number(process.versions.node.split('.')[0]) < 22) fail('node_22_required');
  const parsed = parseCli([options.kind, '--repo', options.repo, '--remote', options.remote ?? 'origin',
    ...(options.tasks ? ['--tasks', options.tasks] : []), ...(options.phase ? ['--phase', options.phase] : []),
    ...(options.output ? ['--output', options.output] : [])]);
  const context = createContext(parsed);
  const inspected = parsed.kind === 'docs-main' ? inspectDocsSource(context, parsed.tasks)
    : inspectSource(context, { root: 'repo', path: parsed.tasks.replaceAll('\\', '/') });
  const inventory = parseOwner(inspected.content, parsed.kind, parsed.phase);
  const draft = draftProjection(context.repository, inspected.source, inventory);
  if (parsed.output) {
    const parent = fs.realpathSync(path.dirname(path.resolve(parsed.output))), target = path.join(parent, path.basename(parsed.output));
    const relative = path.relative(context.repo, target);
    if (parsed.kind === 'docs-main' && relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative)) fail('docs_draft_requires_external_output');
    fs.writeFileSync(target, JSON.stringify(draft, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
  }
  return draft;
}

if (isMain(import.meta.url)) {
  try {
    const options = parseCli(process.argv.slice(2));
    if (options.help) process.stdout.write(USAGE + '\n');
    else {
      const draft = run(options);
      process.stdout.write(JSON.stringify(options.output ? { schema_version: 1, ok: true, code: 'draft_written' } : draft, null, 2) + '\n');
    }
  } catch (error) { process.stdout.write(JSON.stringify(failure(error)) + '\n'); process.exitCode = 1; }
}
