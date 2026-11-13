/**
 * Optional bounded GitHub tracking projection, not phase activation authority.
 * Node >=22 and native Git. Explicit root; remote defaults to origin. docs-main
 * builds its fixed request in memory unless --request is supplied. Phase uses
 * reviewed JSON. --check previews authored
 * payloads without credentials/API. --apply creates absent managed objects and
 * reuses exact matches; --reconcile-only never writes hosted state. No editing,
 * closing, reopening, deletion, implicit output file or mutation replay.
 * See forge-project.md and forge-project-input.md for contracts and limits.
 */
import { createHash } from 'node:crypto';
import { ForgeError, GitHubTransport, fail, text, positive, phaseLabelsMatch } from './github-client.mjs';
import { createContext, inspectSource, inspectDocsSource, requestFile, acquireLock, protectedToken, containsCredential, failure, isMain } from './forge-runtime.mjs';
import { parseOwner, draftProjection, validateProjection, renderProjection } from './projection-input.mjs';

const USAGE = 'phase|docs-main --repo PATH [--remote origin] [--request FILE] [--tasks FILE] (--check|--apply|--reconcile-only) [--confirm-eligibility] [--token-file gh.tkn] [--timeout-ms 120000] [--request-timeout-ms 15000]\nphase requires --request. docs-main without --request uses docs/dev/DOCS_TASKS.md (bundled template when absent); --apply then requires --confirm-eligibility.';
export { ForgeError };

/**
 * Validate full scope/mode without I/O.
 * @param {string[]} args CLI arguments without executable/script.
 * @returns {object} Parsed scope or harmless help.
 * @throws {ForgeError} Missing, ambiguous or unsupported arguments.
 */
export function parseCli(args) {
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) return { help: true };
  if (!['phase', 'docs-main'].includes(args[0])) fail('invalid_operation');
  const result = { kind: args[0], remote: 'origin', timeoutMs: 120000, requestTimeoutMs: 15000, tokenFile: 'gh.tkn' }, seen = new Set();
  const names = { '--repo': 'repo', '--remote': 'remote', '--request': 'requestFile', '--tasks': 'tasks', '--token-file': 'tokenFile', '--timeout-ms': 'timeoutMs', '--request-timeout-ms': 'requestTimeoutMs' };
  for (let i = 1; i < args.length; i++) {
    if (['--check', '--apply', '--reconcile-only'].includes(args[i])) {
      if (result.mode) fail('invalid_execution_mode'); result.mode = args[i].slice(2); continue;
    }
    if (args[i] === '--confirm-eligibility') {
      if (result.confirmEligibility) fail('invalid_arguments');
      result.confirmEligibility = true; continue;
    }
    const name = names[args[i]], value = args[++i];
    if (!name || seen.has(name) || !text(value, 4096) || value.startsWith('--')) fail('invalid_arguments');
    seen.add(name); result[name] = value;
  }
  if (!result.mode || !result.repo || !result.remote || (result.kind === 'phase' && !result.requestFile)
      || !/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(result.remote)) fail('missing_scope');
  if ((result.tasks && (result.kind !== 'docs-main' || result.requestFile))
      || (result.confirmEligibility && (result.kind !== 'docs-main' || result.requestFile || result.mode !== 'apply'))) fail('invalid_arguments');
  if (result.mode === 'apply' && !result.requestFile && !result.confirmEligibility) fail('eligibility_not_established');
  for (const [key, min, max] of [['timeoutMs', 1000, 300000], ['requestTimeoutMs', 100, 60000]]) {
    if (!/^\d+$/.test(String(result[key])) || Number(result[key]) < min || Number(result[key]) > max) fail('invalid_timeout');
    result[key] = Number(result[key]);
  }
  return result;
}

const lf = value => typeof value === 'string' ? value.replace(/\r\n/g, '\n') : value;

/**
 * Resolve observed audience without collapsing explicit internal visibility.
 * @param {{private:boolean,visibility?:string}} metadata Repository response.
 * @param {string} [stage='lookup'] Error stage for initial/final metadata.
 * @returns {'public'|'private'|'internal'} Explicit audience or absence fallback.
 * @throws {ForgeError} Malformed or contradictory public/private metadata.
 */
function repositoryVisibility(metadata, stage = 'lookup') {
  if (typeof metadata.private !== 'boolean') fail('invalid_response', stage);
  if (!Object.hasOwn(metadata, 'visibility')) return metadata.private ? 'private' : 'public';
  if (!['public', 'private', 'internal'].includes(metadata.visibility)
      || (metadata.visibility === 'public' && metadata.private)
      || (metadata.visibility === 'private' && !metadata.private)) fail('invalid_response', stage);
  return metadata.visibility;
}

async function collection(client, type) {
  const all = await client.list('/' + type, type === 'labels' ? {} : { state: 'all' });
  for (const item of all) {
    if (type === 'labels') {
      if (typeof item.name !== 'string' || typeof item.color !== 'string'
          || !(item.description === null || typeof item.description === 'string')) fail('invalid_response', 'lookup');
    } else if (!positive(item.number) || typeof item.title !== 'string' || !['open', 'closed'].includes(item.state)
        || (type === 'issues' && !(item.body === null || typeof item.body === 'string'))
        || (type === 'milestones' && !(item.description === null || typeof item.description === 'string'))) fail('invalid_response', 'lookup');
  }
  return all;
}
function select(all, type, expected, parents, label) {
  const prefix = type === 'labels' ? expected.name.match(/^sdd-phase-[1-9]\d*-/)[0]
    : type === 'milestones' && expected.key !== 'docs-main' ? 'sdd-' + expected.key + '-' : null;
  const marker = type === 'issues' ? new RegExp('sdd-forge:task-id=' + expected.key + '(?=\\s*-->)') : null;
  const matches = all.filter(item => type === 'labels' ? item.name.toLowerCase().startsWith(prefix.toLowerCase())
    : type === 'milestones' ? prefix ? item.title.toLowerCase().startsWith(prefix.toLowerCase())
      : ['sdd-docs-main', 'docs-main'].includes(item.title.toLowerCase()) || /<!--\s*sdd-forge:docs-milestone=docs-main\s*-->/.test(item.description || '')
      : !item.pull_request && (item.title.startsWith('[' + expected.key + ']') || marker.test(item.body || '')));
  if (matches.length > 1) fail('ambiguous_' + type, 'lookup');
  if (!matches.length) return null;
  const item = matches[0];
  if (type === 'labels') {
    if (item.name !== expected.name || item.color.toLowerCase() !== expected.color || item.description !== expected.description || item.archived_at) fail('label_content_conflict', 'identity');
  } else if (type === 'milestones') {
    if (item.title !== expected.title || lf(item.description) !== expected.description) fail('milestone_content_conflict', 'identity');
  } else {
    const body = lf(item.body), tail = typeof body === 'string' && body.slice(expected.body.length);
    const markers = typeof body === 'string' ? [...body.matchAll(/<!--\s*(\/?)sdd-forge:task-id=([^>]*?)\s*-->/g)] : [];
    const scopes = typeof body === 'string' ? [...body.matchAll(/<!--\s*sdd-forge:docs-scope=/g)] : [];
    const expectedParent = parents.get(expected.milestone_id);
    if (item.title !== expected.title || typeof body !== 'string' || !body.startsWith(expected.body)
        || (tail && !tail.startsWith('\n')) || markers.length !== 2
        || markers.some(value => value[2] !== expected.key) || markers[0][1] || markers[1][1] !== '/'
        || scopes.length !== (label ? 0 : 1) || !expectedParent || item.milestone?.number !== expectedParent.number
        || !phaseLabelsMatch(item.labels, label ? label.name : null)) fail('issue_content_or_parent_conflict', 'identity');
  }
  return item;
}
async function snapshot(client, rendered) {
  return {
    labels: rendered.label ? await collection(client, 'labels') : [],
    milestones: await collection(client, 'milestones'), issues: await collection(client, 'issues'),
  };
}
function inspectAll(state, rendered) {
  const label = rendered.label && select(state.labels, 'labels', rendered.label);
  const parents = new Map(rendered.milestones.map(expected => [expected.key, select(state.milestones, 'milestones', expected)]));
  const issues = new Map(rendered.issues.map(expected => [expected.key, select(state.issues, 'issues', expected, parents, rendered.label)]));
  if (rendered.label && !label && [...issues.values()].some(Boolean)) fail('parent_label_missing', 'identity');
  return { label, parents, issues };
}
function payload(type, expected, parents) {
  if (type === 'labels') return { name: expected.name, color: expected.color, description: expected.description };
  if (type === 'milestones') return { title: expected.title, state: 'open', description: expected.description };
  return { title: expected.title, body: expected.body, labels: expected.labels, milestone: parents.get(expected.milestone_id).number };
}
function effect(type, expected, item, status) {
  return { type, key: expected.key || expected.name, status, id: item?.id,
    ...(type === 'labels' ? { name: expected.name } : { number: item?.number, state: item?.state }),
    verified: Boolean(item) };
}

/**
 * Reconcile a source-bound handoff; caller owns eligibility/content/ownership.
 * The lower-level API requires an inspected inventory and authorized transport;
 * normal callers use run for native source/protection/locking checks.
 * @param {object} input Complete schema-v1 caller handoff.
 * @param {object} inventory parseOwner result from the actual selected source.
 * @param {GitHubTransport} client Repository-bound projection capability.
 * @param {{reconcileOnly?:boolean}} options Read-only hosted inspection when true.
 * @returns {Promise<object>} Safe observed effects, associations and outcome.
 */
export async function reconcileProjection(input, inventory, client, { reconcileOnly = false } = {}) {
  const effects = [], associations = []; let visibility = 'not_checked';
  const audited = result => ({ ...result, visibility, effects, associations,
    repository: client.repository, read_retries: client.readRetries, retry_failures: [...client.retryFailures] });
  try {
    const request = validateProjection(input, inventory, !reconcileOnly);
    if (request.repository !== client.repository || client.capability !== 'projection') fail('repository_or_capability_mismatch');
    if (containsCredential(request, client.token)) fail('credential_in_request');
    const metadata = await client.identify();
    visibility = repositoryVisibility(metadata);
    const rendered = renderProjection(request), initial = inspectAll(await snapshot(client, rendered), rendered);
    const parents = initial.parents;
    const objects = [
      ...(rendered.label ? [['labels', rendered.label, initial.label]] : []),
      ...rendered.milestones.map(item => ['milestones', item, parents.get(item.key)]),
      ...rendered.issues.map(item => ['issues', item, initial.issues.get(item.key)]),
    ];
    let missing = false;
    for (const [type, expected, existing] of objects) {
      let item = existing, record;
      if (!item) item = select(await collection(client, type), type, expected, parents, rendered.label);
      if (item) { record = effect(type, expected, item, 'reused'); effects.push(record); }
      else if (reconcileOnly) { effects.push(effect(type, expected, null, 'missing')); missing = true; continue; }
      else {
        record = effect(type, expected, null, 'unknown'); effects.push(record);
        let acknowledged;
        try {
          const response = await client.request('POST', '/' + type, payload(type, expected, parents));
          if (positive(response.data?.id) && (type === 'labels' || positive(response.data?.number))) {
            acknowledged = response.data; Object.assign(record, effect(type, expected, acknowledged, 'created'), { verified: false });
          } else fail('invalid_mutation_response', 'projection', { uncertain: true });
        } catch (error) {
          if (!error.uncertain) { record.status = 'not_applied'; throw error; }
          record.interrupted_by = error.code;
          if (error.http_status) record.http_status = error.http_status;
          if (error.request_id) record.request_id = error.request_id;
        }
        item = select(await collection(client, type), type, expected, parents, rendered.label);
        if (!item) { record.status = 'unknown'; fail('projection_outcome_unknown', 'readback'); }
        if (acknowledged && acknowledged.id !== item.id) fail('object_identity_changed', 'readback');
        Object.assign(record, effect(type, expected, item, acknowledged ? 'created' : 'observed_after_error'));
      }
      if (type === 'milestones') parents.set(expected.key, item);
      if (type === 'issues') associations.push({ task_id: expected.key, issue_number: item.number, milestone_number: item.milestone.number,
        state: item.state, state_reason: item.state_reason ?? null, url: 'https://github.com/' + request.repository + '/issues/' + item.number });
    }
    if (missing) return audited({ schema_version: 1, ok: false, code: 'projection_pending', stage: 'readback', remote_state: 'pending' });
    const final = inspectAll(await snapshot(client, rendered), rendered);
    for (const [type, expected] of objects) {
      const item = type === 'labels' ? final.label : (type === 'milestones' ? final.parents : final.issues).get(expected.key);
      const record = effects.find(value => value.type === type && value.key === (expected.key || expected.name));
      if (!item) { record.status = 'unknown'; fail('projection_outcome_unknown', 'readback'); }
      if (record.id !== item.id) fail('object_identity_changed', 'readback');
      if (type === 'issues') {
        const row = associations.find(value => value.task_id === expected.key);
        Object.assign(row, { state: item.state, state_reason: item.state_reason ?? null, milestone_number: item.milestone.number });
      }
    }
    const after = await client.identify();
    if (after.id !== metadata.id || after.private !== metadata.private || repositoryVisibility(after, 'readback') !== visibility)
      fail('repository_identity_or_visibility_changed', 'readback');
    return audited({ schema_version: 1, ok: true, code: 'projection_verified', stage: 'readback', remote_state: 'verified' });
  } catch (error) {
    const result = failure(error);
    return audited({ ...result, remote_state: effects.some(item => item.status === 'unknown') ? 'unknown' : result.remote_state });
  }
}

/**
 * Run native binding/locking/protection or a credential-free local preview.
 * @param {object} options parseCli fields; scope is validated again.
 * @param {{fetchImpl?:Function}} dependencies Optional controlled HTTP boundary.
 * @returns {Promise<object>} Safe result; pre-lock local errors may throw.
 */
export async function run(options, { fetchImpl } = {}) {
  if (Number(process.versions.node.split('.')[0]) < 22) fail('node_22_required');
  const started = performance.now();
  if (options.confirmEligibility !== undefined && typeof options.confirmEligibility !== 'boolean') fail('invalid_arguments');
  const parsed = parseCli([options.kind, '--repo', options.repo, '--remote', options.remote ?? 'origin',
    ...(options.requestFile !== undefined ? ['--request', options.requestFile] : []),
    ...(options.tasks !== undefined ? ['--tasks', options.tasks] : []),
    ...(options.confirmEligibility ? ['--confirm-eligibility'] : []),
    '--' + options.mode, '--token-file', options.tokenFile || 'gh.tkn', '--timeout-ms', String(options.timeoutMs ?? 120000),
    '--request-timeout-ms', String(options.requestTimeoutMs ?? 15000)]);
  let input = parsed.requestFile ? requestFile(parsed.requestFile) : undefined;
  if (parsed.requestFile && input?.kind !== parsed.kind) fail('operation_mismatch');
  const context = createContext(parsed, input?.repository, started);
  const requirements = { committed: parsed.mode !== 'check' };
  const inspected = input ? inspectSource(context, input.source, requirements) : inspectDocsSource(context, parsed.tasks, requirements);
  const inventory = parseOwner(inspected.content, parsed.kind, input?.phase?.id);
  if (!input) {
    input = draftProjection(context.repository, inspected.source, inventory);
    if (parsed.confirmEligibility) Object.keys(input.eligibility).forEach(key => { input.eligibility[key] = true; });
  }
  const request = validateProjection(input, inventory, parsed.mode === 'apply');
  const digest = createHash('sha256').update(JSON.stringify(request)).digest('hex');
  if (parsed.mode === 'check') return {
    schema_version: 1, ok: true, code: 'input_verified', stage: 'preview', remote_state: 'not_checked',
    repository: request.repository, request_sha256: digest, visibility: 'not_checked', effects: [],
    payloads: renderProjection(request),
  };
  const release = acquireLock(context.common); let result;
  try {
    const token = protectedToken(context, parsed.tokenFile);
    if (containsCredential(request, token)) fail('credential_in_request');
    inspectSource(context, request.source, { committed: true });
    if (context.remainingMs() <= 0) fail('deadline_exceeded');
    const client = new GitHubTransport({ repository: request.repository, token, capability: 'projection',
      timeoutMs: context.remainingMs(), requestTimeoutMs: parsed.requestTimeoutMs, ...(fetchImpl ? { fetchImpl } : {}) });
    result = await reconcileProjection(request, inventory, client, { reconcileOnly: parsed.mode === 'reconcile-only' });
    inspectSource(context, request.source, { committed: true });
  } catch (error) {
    const effects = result?.effects || [];
    result = { ...result, ...failure(error), effects };
    if (effects.some(item => item.status === 'unknown')) result.remote_state = 'unknown';
  } finally {
    try { release(); } catch { result = { ...result, ok: false, code: 'lock_cleanup_failed', stage: 'lock', lock: 'retained' }; }
  }
  return { ...result, repository: request.repository, request_sha256: digest };
}

if (isMain(import.meta.url)) {
  (async () => {
    const options = parseCli(process.argv.slice(2));
    if (options.help) { process.stdout.write(USAGE + '\n'); return; }
    const result = await run(options); process.stdout.write(JSON.stringify(result) + '\n');
    process.exitCode = result.ok ? 0 : ['unknown', 'pending'].includes(result.remote_state) ? 2 : 1;
  })().catch(error => { process.stdout.write(JSON.stringify(failure(error)) + '\n'); process.exitCode = 1; });
}
