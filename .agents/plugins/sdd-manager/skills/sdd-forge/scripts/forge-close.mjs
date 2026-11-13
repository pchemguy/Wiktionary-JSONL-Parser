/**
 * Bounded GitHub completion mechanics for SDD implementation tasks/milestones.
 *
 * Node >=22; native Git and protected-token.mjs. Imports/help do not read a
 * credential or invoke Git/network. The CLI consumes an explicit root/remote
 * and versioned JSON handoff; see forge-close.md for the full contract.
 *
 * Callers establish real authority, acceptance, publication and exclusive
 * execution across machines. JSON assertions are not proof of those facts.
 * This module validates target/hosted identity and evidence, reconciles only
 * completed closure and returns safe known/unknown effects. It never creates
 * issues/milestones, changes Git/configuration, installs tools, reopens work,
 * retires tasks, deletes comments or blindly retries a mutation.
 */
import { ForgeError, GitHubTransport, fail, positive, text, keys, repositoryName, phaseLabelsMatch } from './github-client.mjs';
import { requestFile, acquireLock, failure, containsCredential, createContext, protectedToken, isMain } from './forge-runtime.mjs';
export { ForgeError };

const OID = /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/;
const TASK_ID = /^T-\d{3,}$/;
const MILESTONE_ID = /^[1-9]\d*(?:\.[1-9]\d*)+$/;
const USAGE = 'task|milestone --repo PATH --remote NAME --request FILE [--token-file gh.tkn] [--timeout-ms 60000] [--request-timeout-ms 15000] [--reconcile-only]';

function reportPath(value) {
  if (!text(value, 1024) || value.includes('\\') || value.includes(':') || value.startsWith('/')
      || value.split('/').some(part => !part || part === '.' || part === '..')) fail('invalid_report');
}
function milestoneInput(value) {
  keys(value, ['id', 'number', 'title', 'description']);
  if (!text(value.id, 80) || !MILESTONE_ID.test(value.id) || !positive(value.number) || !text(value.title, 255)
      || !value.title.startsWith('sdd-' + value.id + '-') || value.title === 'sdd-' + value.id + '-'
      || !(value.description === null || text(value.description, 16000, true))) fail('invalid_milestone');
}
const normalizedSummary = value => typeof value === 'string' ? value.replace(/\r\n/g, '\n') : value;
function taskInput(value) {
  keys(value, ['id', 'issue', 'title', 'commit', 'branch', 'verification', 'report']);
  if (!TASK_ID.test(value.id) || !positive(value.issue) || !text(value.title, 255)
      || !value.title.startsWith('[' + value.id + '] ') || value.title === '[' + value.id + '] '
      || !OID.test(value.commit) || !text(value.branch, 255) || /[\s~^:?*\\[\]]/.test(value.branch)
      || value.branch.includes('@{')
      || !text(normalizedSummary(value.verification), 16000, true)) fail('invalid_task');
  if (value.report !== null) reportPath(value.report);
}

/**
 * Validate a caller assertion and exact object/evidence schema, without I/O.
 * @param {object} input Parsed UTF-8 JSON request, not an authorization grant.
 * @param {'task'|'milestone'} operation Completed-closure operation.
 * @returns {object} Independent normalized request; invalid/unsupported scope throws.
 */
export function validateRequest(input, operation) {
  const base = ['schema_version', 'repository', 'phase_label', 'milestone', 'eligibility'];
  if (!['task', 'milestone'].includes(operation)) fail('invalid_operation');
  keys(input, [...base, ...(operation === 'task' ? ['task'] : ['kind', 'tasks', 'review_task', 'report', 'predecessors'])]);
  if (input.schema_version !== 1 || !text(input.phase_label, 100)) fail('invalid_schema');
  const repository = repositoryName(input.repository);
  keys(input.eligibility, ['tracking', 'verified', 'published', 'exclusive']);
  if (Object.values(input.eligibility).some(value => value !== true)) fail('eligibility_not_established');
  milestoneInput(input.milestone);
  if (operation === 'task') taskInput(input.task);
  else {
    if (!['delivery', 'phase-review'].includes(input.kind) || !Array.isArray(input.tasks)
        || input.tasks.length < 1 || input.tasks.length > 1000 || !Array.isArray(input.predecessors)
        || input.predecessors.length > 1000) fail('invalid_milestone_scope');
    input.tasks.forEach(taskInput);
    if (new Set(input.tasks.map(item => item.id)).size !== input.tasks.length
        || new Set(input.tasks.map(item => item.issue)).size !== input.tasks.length) fail('duplicate_expected_task');
    const review = input.tasks.find(item => item.id === input.review_task);
    reportPath(input.report);
    if (!review || review.report !== input.report) fail('review_report_missing');
    input.predecessors.forEach(milestoneInput);
    const all = [input.milestone, ...input.predecessors];
    if (new Set(all.map(item => item.id)).size !== all.length || new Set(all.map(item => item.number)).size !== all.length) fail('duplicate_milestone');
    if ((input.kind === 'delivery' && input.predecessors.length)
        || (input.kind === 'phase-review' && (input.tasks.length !== 1 || !input.predecessors.length))) fail('invalid_review_dependencies');
  }
  const result = { ...structuredClone(input), repository };
  for (const task of operation === 'task' ? [result.task] : result.tasks) task.verification = normalizedSummary(task.verification);
  return result;
}

/** Parse the narrow CLI with no file/credential access. Help is side-effect free. */
export function parseCli(args) {
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) return { help: true };
  if (!['task', 'milestone'].includes(args[0])) fail('invalid_operation');
  const result = { operation: args[0], tokenFile: 'gh.tkn', timeoutMs: 60000, requestTimeoutMs: 15000, reconcileOnly: false };
  const names = { '--repo': 'repo', '--remote': 'remote', '--request': 'requestFile', '--token-file': 'tokenFile', '--timeout-ms': 'timeoutMs', '--request-timeout-ms': 'requestTimeoutMs' };
  const seen = new Set();
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--reconcile-only') {
      if (seen.has('reconcileOnly')) fail('invalid_arguments');
      seen.add('reconcileOnly'); result.reconcileOnly = true; continue;
    }
    const name = names[args[i]], value = args[++i];
    if (!name || seen.has(name) || !text(value, 4096) || value.startsWith('--')) fail('invalid_arguments');
    seen.add(name); result[name] = value;
  }
  if (!['repo', 'remote', 'requestFile'].every(key => seen.has(key))) fail('missing_scope');
  if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(result.remote)) fail('invalid_remote');
  for (const [key, min, max] of [['timeoutMs', 1000, 300000], ['requestTimeoutMs', 100, 60000]]) {
    if (!/^\d+$/.test(String(result[key])) || Number(result[key]) < min || Number(result[key]) > max) fail('invalid_timeout');
    result[key] = Number(result[key]);
  }
  return result;
}

/** Canonical managed evidence for one verified task/commit, without I/O. */
export function evidenceComment(task) {
  taskInput(task);
  return '<!-- sdd-forge:completion task=' + task.id + ' commit=' + task.commit + ' -->\nTask: ' + task.id
    + '\nCommit: ' + task.commit + '\nBranch: ' + task.branch + '\nVerification:\n' + normalizedSummary(task.verification) + '\nReport: ' + (task.report || 'None');
}

/** Completion-only transport; its public API remains available here. */
export class GitHubClient extends GitHubTransport {
  constructor(options) { super({ ...options, capability: 'completion' }); }
}

function managedTask(issue, expected, request) {
  if (!issue || !positive(issue.id) || issue.number !== expected.issue || issue.title !== expected.title
      || issue.pull_request || !['open', 'closed'].includes(issue.state)
      || !phaseLabelsMatch(issue.labels, request.phase_label)
      || issue.milestone?.number !== request.milestone.number || typeof issue.body !== 'string') fail('issue_identity_conflict', 'identity');
  const raw = [...issue.body.matchAll(/<!--\s*(\/?)sdd-forge:task-id=([^>]*?)\s*-->/g)];
  const openings = raw.filter(item => !item[1]), closings = raw.filter(item => item[1]);
  if (openings.length !== 1 || openings[0][2] !== expected.id || closings.length > 1
      || closings.some(item => item[2] !== expected.id || item.index < openings[0].index)) fail('issue_identity_conflict', 'identity');
  // A conservative generated prefix avoids interpreting quoted/fenced/HTML
  // copies as ownership. Other legitimate layouts use the existing backend.
  const opening = issue.body.split(/\r?\n/).find(line => line.trim());
  if (!opening || !/^(?:#{1,6} [^<>\r\n]* )?<!-- sdd-forge:task-id=T-\d{3,} -->\s*$/.test(opening)) fail('issue_identity_conflict', 'identity');
  if (issue.state === 'closed' && issue.state_reason !== 'completed') fail('closure_reason_conflict', 'identity');
}
function managedMilestone(value, expected) {
  if (!value || !positive(value.id) || value.number !== expected.number || value.title !== expected.title
      || value.description !== expected.description || !['open', 'closed'].includes(value.state)
      || !Number.isSafeInteger(value.open_issues) || value.open_issues < 0) fail('milestone_identity_conflict', 'identity');
}
function uniqueMilestone(all, expected) {
  const matches = all.filter(item => typeof item.title === 'string' && item.title.startsWith('sdd-' + expected.id + '-'));
  if (matches.length !== 1) fail('ambiguous_milestone', 'lookup');
  managedMilestone(matches[0], expected); return matches[0];
}
function uniqueIssue(all, expected, request) {
  const marker = new RegExp('sdd-forge:task-id=' + expected.id + '(?=\\s*-->)');
  const matches = all.filter(item => !item.pull_request && (typeof item.title === 'string' && item.title.startsWith('[' + expected.id + ']')
    || typeof item.body === 'string' && marker.test(item.body)));
  if (matches.length !== 1) fail('ambiguous_issue', 'lookup');
  managedTask(matches[0], expected, request); return matches[0];
}
async function freshIssue(client, expected, request, identity) {
  const { data } = await client.request('GET', '/issues/' + expected.issue);
  managedTask(data, expected, request);
  if (identity && data.id !== identity) fail('issue_identity_changed', 'identity');
  return data;
}
async function freshMilestone(client, expected, identity) {
  const { data } = await client.request('GET', '/milestones/' + expected.number);
  managedMilestone(data, expected);
  if (identity && data.id !== identity) fail('milestone_identity_changed', 'identity');
  return data;
}
async function evidence(client, task) {
  const comments = await client.list('/issues/' + task.issue + '/comments');
  if (comments.some(item => typeof item.body !== 'string')) fail('invalid_response', 'evidence');
  const body = evidenceComment(task), marker = body.split('\n')[0];
  const matches = comments.filter(item => item.body.includes(marker));
  if (matches.length > 1 || matches.some(item => item.body !== body)) fail('evidence_conflict', 'evidence');
  return matches[0] || null;
}
function outcome(ok, code, request, operation, effects, details = {}) {
  return { schema_version: 1, ok, code, stage: 'readback', repository: request.repository,
    object: { type: operation, number: operation === 'task' ? request.task.issue : request.milestone.number },
    remote_state: ok ? 'verified' : 'pending', effects: { ...effects }, ...details };
}
/**
 * Reconcile one validated caller assertion against bounded hosted state.
 * @param {'task'|'milestone'} operation Completed-closure mode.
 * @param {object} input Full request; eligibility remains the caller's assertion.
 * @param {GitHubClient} client Authorized repository-bound transport.
 * @param {{reconcileOnly?: boolean}} options Read-only recovery when true.
 * @returns {Promise<object>} Versioned safe outcome, including partial/unknown effects.
 */
export async function reconcileClosure(operation, input, client, { reconcileOnly = false } = {}) {
  const effects = { comment: 'not_attempted', closure: 'not_attempted' };
  const audited = value => ({ ...value, read_retries: client.readRetries, retry_failures: [...client.retryFailures] });
  let request, recovered = false;
  try {
    request = validateRequest(input, operation);
    if (client.repository !== request.repository) fail('repository_mismatch', 'preflight');
    if (containsCredential(request, client.token)) fail('credential_in_request', 'preflight');
    await client.identify();
    const milestones = await client.list('/milestones', { state: 'all' });
    const selected = uniqueMilestone(milestones, request.milestone);
    if (operation === 'task') {
      const issues = await client.list('/issues', { state: 'all' });
      const selectedIssue = uniqueIssue(issues, request.task, request);
      let current = await freshIssue(client, request.task, request, selectedIssue.id);
      await freshMilestone(client, request.milestone, selected.id);
      let comment = await evidence(client, request.task);
      if (!comment && reconcileOnly) return audited(outcome(false, 'reconciliation_pending', request, operation, effects));
      if (!comment) {
        await freshIssue(client, request.task, request, selectedIssue.id);
        effects.comment = 'unknown';
        let acknowledged = false;
        try {
          const response = await client.request('POST', '/issues/' + request.task.issue + '/comments', { body: evidenceComment(request.task) });
          if (!positive(response.data?.id) || response.data.body !== evidenceComment(request.task)) fail('invalid_mutation_response', 'evidence', { uncertain: true });
          acknowledged = true;
        }
        catch (error) {
          if (!error.uncertain) { effects.comment = 'not_applied'; throw error; }
          effects.comment = 'unknown'; recovered = true;
        }
        comment = await evidence(client, request.task);
        if (!comment) {
          effects.comment = 'unknown'; fail('comment_outcome_unknown', 'evidence');
        }
        effects.comment = acknowledged ? 'created' : 'observed_after_error';
      } else effects.comment = 'existing';
      current = await freshIssue(client, request.task, request, selectedIssue.id);
      if (current.state === 'open' && reconcileOnly) return audited(outcome(false, 'reconciliation_pending', request, operation, effects));
      if (current.state === 'open') {
        effects.closure = 'unknown';
        try {
          const response = await client.request('PATCH', '/issues/' + request.task.issue, { state: 'closed', state_reason: 'completed' });
          managedTask(response.data, request.task, request);
        }
        catch (error) {
          if (error instanceof ForgeError && error.stage === 'identity') error.uncertain = true;
          if (!error.uncertain) { effects.closure = 'not_applied'; throw error; }
          effects.closure = 'unknown'; recovered = true;
        }
      } else effects.closure = 'existing';
      current = await freshIssue(client, request.task, request, selectedIssue.id);
      if (current.state !== 'closed') {
        effects.closure = 'unknown'; fail('closure_outcome_unknown', 'readback');
      }
      if (!await evidence(client, request.task)) fail('evidence_missing', 'readback');
      if (effects.closure === 'unknown') effects.closure = recovered ? 'observed_after_error' : 'changed';
      await freshMilestone(client, request.milestone, selected.id);
    } else {
      const issues = await client.list('/issues', { milestone: String(request.milestone.number), state: 'all' });
      if (issues.length !== request.tasks.length || issues.some(item => item.pull_request)) fail('milestone_membership_conflict', 'eligibility');
      for (const task of request.tasks) {
        const issue = uniqueIssue(issues, task, request);
        const current = await freshIssue(client, task, request, issue.id);
        if (current.state !== 'closed' || !await evidence(client, task)) fail('task_completion_missing', 'eligibility');
      }
      for (const predecessor of request.predecessors) {
        const item = uniqueMilestone(milestones, predecessor);
        const current = await freshMilestone(client, predecessor, item.id);
        if (current.state !== 'closed' || current.open_issues !== 0) fail('predecessor_not_closed', 'eligibility');
      }
      let current = await freshMilestone(client, request.milestone, selected.id);
      if (current.open_issues !== 0) fail('milestone_has_open_issues', 'eligibility');
      if (current.state === 'open' && reconcileOnly) return audited(outcome(false, 'reconciliation_pending', request, operation, effects));
      if (current.state === 'open') {
        effects.closure = 'unknown';
        try {
          const response = await client.request('PATCH', '/milestones/' + current.number, { state: 'closed' });
          managedMilestone(response.data, request.milestone);
        }
        catch (error) {
          if (error instanceof ForgeError && error.stage === 'identity') error.uncertain = true;
          if (!error.uncertain) { effects.closure = 'not_applied'; throw error; }
          effects.closure = 'unknown'; recovered = true;
        }
      } else effects.closure = 'existing';
      current = await freshMilestone(client, request.milestone, selected.id);
      if (current.state !== 'closed' || current.open_issues !== 0) {
        effects.closure = 'unknown'; fail('closure_outcome_unknown', 'readback');
      }
      if (effects.closure === 'unknown') effects.closure = recovered ? 'observed_after_error' : 'changed';
      const after = await client.list('/issues', { milestone: String(request.milestone.number), state: 'all' });
      if (after.length !== issues.length || after.some(item => !issues.some(before => before.id === item.id))) fail('milestone_membership_changed', 'readback');
      for (const task of request.tasks) {
        const item = uniqueIssue(after, task, request);
        if (item.state !== 'closed' || !await evidence(client, task)) fail('task_completion_changed', 'readback');
      }
      for (const predecessor of request.predecessors) {
        const item = uniqueMilestone(milestones, predecessor);
        const after = await freshMilestone(client, predecessor, item.id);
        if (after.state !== 'closed' || after.open_issues !== 0) fail('predecessor_not_closed', 'readback');
      }
      effects.comment = 'not_needed';
    }
    return audited(outcome(true, recovered ? 'verified_after_error' : effects.closure === 'existing' && ['existing', 'not_needed'].includes(effects.comment) ? 'already_verified' : 'closed_verified', request, operation, effects));
  } catch (error) {
    const result = failure(error, effects);
    if (request) Object.assign(result, { repository: request.repository, object: { type: operation, number: operation === 'task' ? request.task.issue : request.milestone.number } });
    return audited(result);
  }
}

/**
 * Execute an explicit CLI-equivalent scope with real local protection/locking.
 * @param {object} options parseCli output; programmatic callers use the same fields.
 * @param {{fetchImpl?: Function}} dependencies Optional controlled HTTP transport.
 * @returns {Promise<object>} Safe outcome. Pre-lock invalid local scope may throw.
 */
export async function run(options, { fetchImpl } = {}) {
  if (Number(process.versions.node.split('.')[0]) < 22) fail('node_22_required');
  const started = performance.now();
  const parsed = parseCli([options.operation, '--repo', options.repo, '--remote', options.remote, '--request', options.requestFile,
    '--token-file', options.tokenFile || 'gh.tkn', '--timeout-ms', String(options.timeoutMs ?? 60000),
    '--request-timeout-ms', String(options.requestTimeoutMs ?? 15000), ...(options.reconcileOnly ? ['--reconcile-only'] : [])]);
  const request = validateRequest(requestFile(parsed.requestFile), parsed.operation);
  const context = createContext(parsed, request.repository, started);
  const { checked, common } = context;
  for (const branch of new Set((parsed.operation === 'task' ? [request.task] : request.tasks).map(item => item.branch))) checked(['check-ref-format', '--branch', branch]);
  const release = acquireLock(common);
  let result;
  try {
    const token = protectedToken(context, parsed.tokenFile);
    const remaining = parsed.timeoutMs - (performance.now() - started);
    if (remaining <= 0) fail('deadline_exceeded');
    const client = new GitHubClient({ repository: request.repository, token, timeoutMs: remaining, requestTimeoutMs: parsed.requestTimeoutMs, ...(fetchImpl ? { fetchImpl } : {}) });
    result = await reconcileClosure(parsed.operation, request, client, { reconcileOnly: parsed.reconcileOnly });
  } catch (error) { result = failure(error); }
  finally {
    try { release(); }
    catch { result = { ...result, ok: false, code: 'lock_cleanup_failed', stage: 'lock', lock: 'retained' }; }
  }
  return result;
}

if (isMain(import.meta.url)) {
  (async () => {
    const options = parseCli(process.argv.slice(2));
    if (options.help) { process.stdout.write(USAGE + '\n'); return; }
    const result = await run(options);
    process.stdout.write(JSON.stringify(result) + '\n');
    process.exitCode = result.ok ? 0 : ['unknown', 'pending'].includes(result.remote_state) ? 2 : 1;
  })().catch(error => { process.stdout.write(JSON.stringify(failure(error)) + '\n'); process.exitCode = 1; });
}
