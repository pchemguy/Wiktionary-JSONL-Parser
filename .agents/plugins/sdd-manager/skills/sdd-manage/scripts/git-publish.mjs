/**
 * Supervised single-ref HTTPS publication. Node 22+, Python 3.11+, native Git.
 * Imports have no effects. See git-auth-recover.md for scope, budgets and results.
 * No credentials cross the controller/worker protocol. Blocking Git runs only
 * inside a worker owned by git-process-supervisor.py, never on this event loop.
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { performance } from 'node:perf_hooks';
import { parseCli, recover, RecoveryError } from './git-auth-recover.mjs';

const SCRIPT = fileURLToPath(import.meta.url);
const BACKEND = fileURLToPath(new URL('./git-process-supervisor.py', import.meta.url));
const USAGE = 'push|readback --repo PATH --remote NAME --url HTTPS_URL --ref FULL_REF --expect FULL_OBJECT_ID [--auth auto|token|existing] [--credential-repo PATH] [--token-file gh.tkn] [--timeout-ms 60000] [--python EXECUTABLE] [--progress]';
const failure = code => ({ schema_version: 1, ok: false, code, stage: 'preflight',
  remote_state: 'unknown', push_attempted: false });
const safeError = error => error instanceof RecoveryError ?
  { ...failure(error.code), stage: error.stage || 'preflight' } : failure('local_io_failed');
const notAttempted = () => ({ code: 'not_attempted', exit_status: null, signal: null });

/** Parse the public interface, keeping the core's narrower per-child timeout. */
function optionsFor(args, defaultAuth) {
  let timeoutMs = 60000, python = 'python', progress = false;
  const core = [], seen = new Set();
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (['--timeout-ms', '--python', '--progress'].includes(key)) {
      if (seen.has(key)) throw new RecoveryError('invalid_arguments');
      seen.add(key);
      if (key === '--progress') { progress = true; continue; }
      const value = args[++i];
      if (!value || value.startsWith('--')) throw new RecoveryError('invalid_arguments');
      if (key === '--timeout-ms') timeoutMs = Number(value);
      else python = value;
    } else core.push(key);
  }
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1000 || timeoutMs > 600000)
    throw new RecoveryError('invalid_timeout');
  if (!core.includes('--auth')) core.push('--auth',
    core.includes('--token-file') || core.includes('--credential-repo') ? 'token' : defaultAuth);
  const options = parseCli([...core, '--timeout-ms', '30000']);
  const selectedToken = core.includes('--token-file') || core.includes('--credential-repo');
  if (options.auth === 'existing' && selectedToken)
    throw new RecoveryError('conflicting_auth_options');
  if (options.auth === 'auto' && selectedToken) options.auth = 'token';
  return { options, timeoutMs, python, progress };
}

/** Private worker: bounded input, fixed protocol, one network operation only. */
async function worker() {
  const emit = value => process.stdout.write(JSON.stringify(value) + '\n');
  try {
    let input = '';
    for await (const chunk of process.stdin) {
      input += chunk;
      if (Buffer.byteLength(input) > 60000) throw new RecoveryError('invalid_arguments');
    }
    const { options } = JSON.parse(input);
    const result = recover(options, undefined, { singleOperation: true,
      onStage: value => emit({ kind: 'stage', ...value }) });
    emit({ kind: 'result', result });
  } catch (error) { emit({ kind: 'result', result: safeError(error) }); process.exitCode = 1; }
}

/**
 * Own one Python supervisor. Resolve on its exit, independently of pipe close;
 * inherited pipes cannot hold the public command open. Confirmed cleanup is
 * required before any subsequent network operation. Output is private/bounded.
 */
function attempt(options, python, budget, cancelled, progress) {
  return new Promise(resolve => {
    const cleanupMs = Math.min(3000, Math.max(100, Math.floor(budget / 5)));
    const margin = Math.min(150, Math.floor(budget / 10));
    let child, text = '', bytes = 0, final, supervision, stage, mode;
    let problem, done = false, watchdog, hardTimer;
    const settle = () => {
      if (done) return;
      done = true; clearTimeout(watchdog); clearTimeout(hardTimer);
      cancelled.removeEventListener('abort', cancel);
      child?.stdin.destroy(); child?.stdout.destroy(); child?.stderr.destroy(); child?.unref();
      resolve({ result: final, stage, mode, code: problem || supervision?.code || 'supervisor_unavailable',
        cleanup: supervision?.cleanup === 'confirmed' ? 'confirmed' : 'unconfirmed' });
    };
    const cancel = () => {
      problem ||= 'cancelled';
      if (child?.stdin.writable) child.stdin.write('cancel\n', () => {});
    };
    const stop = code => { problem ||= code; cancel(); };
    const frame = line => {
      let value;
      try { value = JSON.parse(line); } catch { stop('invalid_worker_output'); return; }
      if (value.kind === 'stage' && ['push', 'readback'].includes(value.stage) &&
          ['token', 'existing'].includes(value.auth_mode)) {
        stage = value.stage; mode = value.auth_mode;
        if (progress) process.stderr.write(JSON.stringify({ stage, auth_mode: mode }) + '\n');
      } else if (value.kind === 'result' && !final && value.result?.schema_version === 1) {
        // This channel is written only by our worker. Arbitrary Git output is
        // captured there and never forwarded into this protocol.
        final = value.result;
      } else if (value.kind === 'supervisor' && !supervision &&
          ['worker_exit', 'cancelled', 'process_timeout', 'supervision_unavailable'].includes(value.code) &&
          ['confirmed', 'unconfirmed'].includes(value.cleanup)) supervision = value;
      else if (!(value.kind === 'started' && Number.isInteger(value.worker_pid))) stop('invalid_worker_output');
    };
    try {
      child = spawn(python, ['-u', BACKEND], { stdio: ['pipe', 'pipe', 'pipe'],
        windowsHide: true, shell: false });
      child.stdin.on('error', () => {});
      child.stdout.setEncoding('utf8');
      child.stdout.on('data', chunk => {
        bytes += Buffer.byteLength(chunk);
        if (bytes > 1024 * 1024) { stop('process_output_limit'); return; }
        text += chunk;
        let index;
        while ((index = text.indexOf('\n')) >= 0) {
          frame(text.slice(0, index)); text = text.slice(index + 1);
        }
      });
      child.stderr.on('data', chunk => {
        bytes += chunk.length;
        if (bytes > 1024 * 1024) stop('process_output_limit');
      });
      child.on('error', () => {
        problem ||= 'supervisor_unavailable';
        supervision = { cleanup: 'confirmed' }; // spawn failed; no worker exists
        settle();
      });
      child.on('exit', status => {
        if (status !== 0) problem ||= 'supervisor_failed';
        // Drain already delivered pipe events before final disposition, without
        // waiting indefinitely for inherited descriptors to close.
        setImmediate(settle);
      });
      cancelled.addEventListener('abort', cancel, { once: true });
      if (cancelled.aborted) cancel();
      child.stdin.write(JSON.stringify({ command: [process.execPath, SCRIPT, '--worker'],
        input: JSON.stringify({ options }), timeout_ms: Math.max(100, budget - margin),
        cleanup_ms: cleanupMs }) + '\n');
      // Leave stdin open: EOF tells the backend its owner has disappeared.
      watchdog = setTimeout(() => stop('process_timeout'), Math.max(1, budget - cleanupMs));
      hardTimer = setTimeout(() => {
        problem ||= 'process_timeout'; child.kill('SIGKILL'); settle();
      }, budget);
    } catch { problem = 'supervisor_unavailable'; settle(); }
  });
}

function failedAttempt(step, pushAttempted) {
  const code = step.cleanup !== 'confirmed' ? 'cleanup_unconfirmed' :
    step.code === 'worker_exit' ? 'worker_failed' : step.code;
  const result = { ...failure(code), stage: step.stage || 'preflight', push_attempted: pushAttempted };
  if (step.stage) result[step.stage + '_result'] = { code: step.code === 'process_timeout' ?
    'process_timeout' : 'worker_failed', exit_status: null, signal: null };
  return result;
}

/** Public controller; at most one push and one readback share one deadline. */
export async function runCli(args, { defaultAuth = 'auto' } = {}) {
  if (args.length === 1 && args[0] === '--help') { process.stdout.write(USAGE + '\n'); return; }
  const started = performance.now(), abort = new AbortController();
  const onSignal = () => abort.abort();
  process.once('SIGINT', onSignal); process.once('SIGTERM', onSignal);
  let result, timeoutMs = 60000, cleanup = 'not_started', authMode = 'unknown';
  try {
    if (Number(process.versions.node.split('.')[0]) < 22) throw new RecoveryError('node_22_required');
    const selected = optionsFor(args, defaultAuth);
    ({ timeoutMs } = selected);
    let { options, python, progress } = selected;
    const remaining = () => Math.max(0, Math.floor(timeoutMs - (performance.now() - started)));
    const reserve = options.operation === 'push' ? Math.min(15000, Math.floor(timeoutMs / 4)) : 0;
    const first = await attempt(options, python, Math.max(100, remaining() - reserve), abort.signal, progress);
    cleanup = first.cleanup; authMode = first.mode || first.result?.auth_mode || 'unknown';
    const attempted = first.stage === 'push';
    if (first.cleanup !== 'confirmed' || abort.signal.aborted ||
        !['worker_exit', 'process_timeout'].includes(first.code)) result = failedAttempt(first, attempted);
    else if (options.operation === 'readback' || !attempted) result = first.result || failedAttempt(first, false);
    else {
      const pushResult = first.result?.push_result || { code: first.code === 'process_timeout' ?
        'process_timeout' : 'worker_failed', exit_status: null, signal: null };
      if (remaining() < 150) result = { ...failedAttempt(first, true), code: 'process_timeout' };
      else {
        // Pin the selected account/credential route; never switch on retry.
        options = { ...options, operation: 'readback', auth: authMode };
        const second = await attempt(options, python, remaining(), abort.signal, progress);
        cleanup = second.cleanup;
        result = second.cleanup === 'confirmed' && second.code === 'worker_exit' && second.result
          ? second.result : failedAttempt(second, true);
        if (result.stage !== 'readback') {
          result.local_error = { code: result.code, stage: result.stage };
          result.stage = 'readback';
        }
        result.push_attempted = true; result.push_result = pushResult;
        if (result.ok && pushResult.code !== 'succeeded') result.code = 'verified_after_push_error';
      }
    }
  } catch (error) { result = safeError(error); }
  finally { process.removeListener('SIGINT', onSignal); process.removeListener('SIGTERM', onSignal); }
  if (abort.signal.aborted) result = { ...result, ok: false, code: 'cancelled' };
  result ||= failure('worker_failed');
  if (cleanup !== 'confirmed') result.ok = false;
  result = { ...result, auth_mode: authMode, elapsed_ms: Math.ceil(performance.now() - started),
    timeout_ms: timeoutMs, cleanup_state: cleanup,
    next_action: result.ok ? 'continue' : cleanup === 'unconfirmed' ? 'resolve_cleanup_before_retry' :
      result.remote_state === 'different' ? 'reconcile_remote' :
        result.push_attempted ? 'diagnose_then_readback' : 'correct_local_input_or_auth' };
  result.push_result ||= notAttempted(); result.readback_result ||= notAttempted();
  process.stdout.write(JSON.stringify(result) + '\n');
  process.exitCode = result.ok ? 0 : cleanup === 'unconfirmed' ||
    ['process_timeout', 'cancelled', 'worker_failed', 'supervisor_failed', 'process_output_limit', 'invalid_worker_output'].includes(result.code) ? 3 :
      result.stage === 'readback' ? 2 : 1;
  return result;
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT) {
  if (process.argv[2] === '--worker') await worker();
  else await runCli(process.argv.slice(2));
}
