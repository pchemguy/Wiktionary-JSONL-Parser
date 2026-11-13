/**
 * HTTPS credential/validation core and compatibility entry. Node >=22.
 * Public execution delegates to git-publish.mjs (Python >=3.11 supervisor).
 *
 * Main entry: push|readback --repo PATH --remote NAME --url HTTPS_URL
 *   --ref refs/heads/NAME|refs/tags/NAME --expect FULL_OBJECT_ID
 *   [--auth auto|token|existing] [--credential-repo PATH] [--token-file gh.tkn] [--timeout-ms 60000]
 *
 * Policy/authorization belongs to sdd-manage/references/credentials.md. This
 * utility validates one destination/ref, supplies credentials through Git's
 * helper protocol and returns JSON. It never installs helpers, edits Git config,
 * persists credentials, force-pushes, deletes refs, or retries a push in a loop.
 * Imports have no effects. See git-auth-recover.md for the complete CLI contract.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { ProtectedInputError as RecoveryError, sameDirectory, childEnv, readToken } from './protected-token.mjs';
export { ProtectedInputError as RecoveryError, validateToken, readToken } from './protected-token.mjs';

const SCRIPT = fileURLToPath(import.meta.url);
const OID = /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/;
const USAGE = 'push|readback --repo PATH --remote NAME --url HTTPS_URL --ref FULL_REF --expect FULL_OBJECT_ID [--auth auto|token|existing] [--credential-repo PATH] [--token-file gh.tkn] [--timeout-ms 60000] [--python EXECUTABLE] [--progress]';

const fail = (code, stage) => { throw new RecoveryError(code, stage); };
const HELPER_MARKER = 'SDD_GIT_AUTH_HELPER ';
const HELPER_CODES = new Set(['helper_failed', 'helper_context_mismatch', 'repo_must_be_root',
  'invalid_helper_arguments', 'invalid_credential_request', 'invalid_url', 'relocated_git_environment',
  'token_outside_repository', 'token_symlink', 'invalid_token_file', 'token_not_ignored',
  'token_tracked_or_unknown', 'token_changed', 'invalid_token', 'credential_repository_mismatch',
  'process_timeout', 'process_unavailable', 'process_signal', 'git_failed']);
const HELPER_STAGES = new Set(['preflight', 'helper', 'repository', 'token']);
const SIGNALS = new Set(Object.keys(os.constants.signals));
const PROCESS_ERRORS = new Map([['ETIMEDOUT', 'process_timeout'], ['ENOENT', 'process_unavailable'], ['ENOBUFS', 'process_output_limit']]);

/** Accept only the fixed private diagnostic shape; never retain unknown text. */
function validHelperDiagnostic(value) {
  return value && typeof value === 'object' && !Array.isArray(value) &&
    Object.keys(value).length === 2 && Object.hasOwn(value, 'code') && Object.hasOwn(value, 'stage') &&
    HELPER_CODES.has(value.code) && HELPER_STAGES.has(value.stage);
}

/** Error messages/stacks may carry paths or secrets; only known codes survive. */
function helperFailure(error) {
  const value = error instanceof RecoveryError ? { code: error.code, stage: error.stage } : null;
  return validHelperDiagnostic(value) ? value : { code: 'helper_failed', stage: 'helper' };
}

/**
 * Parse a bounded advisory diagnostic from captured Git stderr. Git/provider text
 * can spoof stderr, so this is not authentication or authority evidence. Unknown,
 * malformed, extra-field or conflicting reports are discarded without echoing.
 */
function helperDiagnostic(stderr) {
  if (typeof stderr !== 'string' || Buffer.byteLength(stderr) > 1024 * 1024) return;
  let selected;
  for (const line of stderr.split(/\r?\n/)) {
    if (!line.startsWith(HELPER_MARKER)) continue;
    if (line.length > 240) return;
    let value;
    try { value = JSON.parse(line.slice(HELPER_MARKER.length)); } catch { return; }
    if (!validHelperDiagnostic(value)) return;
    if (selected && (selected.code !== value.code || selected.stage !== value.stage)) return;
    selected = { code: value.code, stage: value.stage };
  }
  return selected;
}

/** Summarize process mechanics independently of remote state; no output/argv. */
function processSummary(result, attempted = true) {
  let code = attempted ? 'process_error' : 'not_attempted';
  if (attempted && result) {
    if (result.error) code = PROCESS_ERRORS.get(result.error.code) || 'process_error';
    else if (result.signal) code = 'process_signal';
    else if (result.status === 0) code = 'succeeded';
    else if (Number.isInteger(result.status) && result.status > 0) code = 'git_failed';
  }
  const summary = { code, exit_status: Number.isInteger(result?.status) && result.status >= 0 && result.status <= 0xffffffff ? result.status : null,
    signal: SIGNALS.has(result?.signal) ? result.signal : null };
  const diagnostic = helperDiagnostic(result?.stderr);
  if (diagnostic) summary.helper_error = diagnostic;
  return summary;
}

/**
 * Parse and validate the narrow CLI without I/O.
 * @param {string[]} args Operation and explicit options, excluding node/script.
 * @returns {object} Validated scope, defaults and bounded timeout.
 * @throws {RecoveryError} Invalid or incomplete scope; never embeds input values.
 */
export function parseCli(args) {
  if (!['push', 'readback'].includes(args[0])) fail('invalid_operation');
  const options = { operation: args[0], tokenFile: 'gh.tkn', timeoutMs: 30000, auth: 'token' };
  const names = { '--repo': 'repo', '--remote': 'remote', '--url': 'url', '--ref': 'ref',
    '--expect': 'expect', '--token-file': 'tokenFile', '--timeout-ms': 'timeoutMs',
    '--auth': 'auth', '--credential-repo': 'credentialRepo' };
  const seen = new Set();
  for (let i = 1; i < args.length; i += 2) {
    const key = names[args[i]], value = args[i + 1];
    if (!key || seen.has(key) || !value || value.startsWith('--')) fail('invalid_arguments');
    seen.add(key); options[key] = value;
  }
  if (!['repo', 'remote', 'url', 'ref', 'expect'].every(key => seen.has(key))) fail('missing_scope');
  if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(options.remote) || !OID.test(options.expect)) fail('invalid_scope');
  if (!/^refs\/(heads|tags)\/.+/.test(options.ref) || /[\x00-\x20\x7f]/.test(options.ref)) fail('invalid_ref');
  options.timeoutMs = Number(options.timeoutMs);
  if (!Number.isInteger(options.timeoutMs) || options.timeoutMs < 100 || options.timeoutMs > 120000) fail('invalid_timeout');
  if (!['auto', 'token', 'existing'].includes(options.auth)) fail('invalid_auth_mode');
  validateTargetUrl(options.url);
  return options;
}

/**
 * @param {string} value Exact canonical HTTPS destination from the coordinator.
 * @returns {URL} Parsed credential-free URL; no network or rewrite is performed.
 * @throws {RecoveryError} Unsafe, noncanonical or unsupported URL.
 */
export function validateTargetUrl(value) {
  let url, credentialPath;
  try { url = new URL(value); credentialPath = gitCredentialPath(url); }
  catch { fail('invalid_url'); }
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash ||
      !url.hostname || !credentialPath || /[\s\x00-\x1f\x7f]/.test(value) ||
      /[\x00-\x1f\x7f]/.test(credentialPath) || url.href !== value) fail('invalid_url');
  return url;
}

/** Match Git: strip literal leading slashes, decode once, trim trailing slashes. */
function gitCredentialPath(url) {
  return decodeURIComponent(url.pathname.replace(/^\/+/, '')).replace(/\/+$/, '');
}

/**
 * Build Git's documented shell-helper command; credentials are never arguments.
 * @param {string} node Actual Node executable path.
 * @param {string} script Installed script path.
 * @param {string[]} args Repository, token-file path and selected URL only.
 * @param {string} platform Platform used to normalize native executable paths.
 * @returns {string} Command-local helper setting with shell-quoted arguments.
 */
export function helperCommand(node, script, args, platform = process.platform) {
  const quote = value => "'" + String(value).replaceAll("'", "'\\''") + "'";
  const executable = value => platform === 'win32' ? value.replaceAll('\\', '/') : value;
  return '!' + [executable(node), executable(script), '--credential-helper', ...args].map(quote).join(' ');
}

/** Direct executable launch with bounded captured output; caller never prints it. */
function processResult(executable, args, { cwd, env, timeoutMs = 30000, input } = {}) {
  return spawnSync(executable, args, { cwd, env, input, encoding: 'utf8', shell: false,
    windowsHide: true, timeout: timeoutMs, killSignal: 'SIGKILL', maxBuffer: 1024 * 1024 });
}
function checked(result, stage) {
  if (result.error) fail(result.error.code === 'ETIMEDOUT' ? 'process_timeout' : 'process_unavailable', stage);
  if (result.signal) fail('process_signal', stage);
  if (result.status !== 0) fail('git_failed', stage);
  return result.stdout || '';
}

/** Parse only security-relevant credential fields; do not log protocol input. */
export function credentialRequest(input) {
  if (Buffer.byteLength(input) > 65536) fail('invalid_credential_request', 'helper');
  const result = {};
  for (const line of input.split(/\r?\n/)) {
    if (!line) break;
    const split = line.indexOf('=');
    if (split < 1) fail('invalid_credential_request', 'helper');
    const key = line.slice(0, split);
    if (!['protocol', 'host', 'path', 'username'].includes(key)) continue;
    if (Object.hasOwn(result, key)) fail('invalid_credential_request', 'helper');
    result[key] = line.slice(split + 1);
  }
  return result;
}

/** Exact ref readback. Ref object IDs, including annotated tag objects, are literal. */
export function remoteOid(stdout, ref) {
  const rows = stdout.trim() ? stdout.trim().split(/\r?\n/) : [];
  if (!rows.length) return null;
  if (rows.length !== 1) fail('ambiguous_readback', 'readback');
  const [oid, name, extra] = rows[0].split(/\s+/);
  if (!OID.test(oid) || name !== ref || extra) fail('invalid_readback', 'readback');
  return oid;
}

/** Bind a credential source to the same actual Git common directory.
 * @param {string} repo Destination worktree's canonical root.
 * @param {string|undefined} selected Explicit source root; defaults to repo.
 * @param {Function} gitAt Root-bound, bounded local Git adapter factory.
 * @returns {{repo: string, git: Function}} Source root and its local adapter.
 * @throws {RecoveryError|Error} Invalid root or unrelated repository identity.
 */
function credentialContext(repo, selected, gitAt) {
  const source = selected ? fs.realpathSync(selected) : repo;
  const git = gitAt(source);
  if (!sameDirectory(checked(git(['rev-parse', '--show-toplevel']), 'token').trim(), source))
    fail('repo_must_be_root', 'token');
  if (!sameDirectory(repo, source)) {
    const common = root => path.resolve(root,
      checked(gitAt(root)(['rev-parse', '--git-common-dir']), 'token').trim());
    if (!sameDirectory(common(repo), common(source))) fail('credential_repository_mismatch', 'token');
  }
  return { repo: source, git };
}

/** Prepare one bound context; credential bytes never enter the returned object. */
function prepare(options, execute) {
  const env = childEnv(), repo = fs.realpathSync(options.repo);
  const gitAt = root => (args, auth = []) => execute('git', ['-C', root, ...auth, ...args],
    { cwd: root, env, timeoutMs: options.timeoutMs });
  const git = gitAt(repo);
  const root = checked(git(['rev-parse', '--show-toplevel']), 'repository').trim();
  if (!sameDirectory(root, repo)) fail('repo_must_be_root');
  checked(git(['check-ref-format', options.ref]), 'ref');
  if (options.operation === 'push') {
    const source = checked(git(['show-ref', '--verify', '--hash', options.ref]), 'ref').trim();
    if (source !== options.expect) fail('source_mismatch');
  } else checked(git(['cat-file', '-e', options.expect]), 'ref');
  const target = validateTargetUrl(options.url);
  const destination = () => {
    const vcs = git(['config', '--get-all', 'remote.' + options.remote + '.vcs']);
    if (vcs.error || vcs.signal || vcs.status !== 1) fail('remote_helper_unsupported');
    const urls = checked(git(['remote', 'get-url', '--push', '--all', options.remote]), 'destination').trim().split(/\r?\n/);
    if (urls.length !== 1 || urls[0] !== options.url) fail('destination_mismatch');
    const readUrl = checked(git(['ls-remote', '--get-url', options.url]), 'destination').trim();
    if (readUrl !== options.url) fail('readback_url_rewritten');
  };
  destination();
  let mode = options.auth;
  let credential;
  if (mode !== 'existing') {
    credential = credentialContext(repo, options.credentialRepo, gitAt);
    const relative = path.relative(credential.repo, path.resolve(credential.repo, options.tokenFile));
    if (path.isAbsolute(options.tokenFile) || !relative || relative === '..' || relative.startsWith('..' + path.sep))
      fail('token_outside_repository');
    if (mode === 'auto') {
      try { fs.lstatSync(path.join(credential.repo, options.tokenFile)); mode = 'token'; }
      catch (error) { if (error.code === 'ENOENT') mode = 'existing'; else throw error; }
    }
    if (mode === 'token') readToken(credential.repo, options.tokenFile, credential.git);
  }
  const auth = ['-c', 'credential.interactive=false', '-c', 'core.askPass=',
    '-c', 'http.followRedirects=false', '-c', 'http.' + options.url + '.followRedirects=false'];
  if (mode === 'token') {
    const helperArgs = [repo, options.tokenFile, options.url];
    if (!sameDirectory(repo, credential.repo)) helperArgs.push('--credential-repo', credential.repo);
    const helper = helperCommand(process.execPath, SCRIPT, helperArgs);
    const contextUrl = target.origin + '/' + gitCredentialPath(target).split('/').map(encodeURIComponent).join('/');
    const context = 'credential.' + contextUrl;
    auth.unshift('-c', 'credential.helper=', '-c', context + '.helper=',
      '-c', context + '.helper=' + helper, '-c', 'credential.useHttpPath=true',
      '-c', context + '.useHttpPath=true', '-c', context + '.username=x-access-token',
      '-c', 'http.extraHeader=', '-c', 'http.' + options.url + '.extraHeader=');
  }
  destination();
  return { git, auth, mode };
}

/**
 * Shared synchronous operation core. Public CLI execution is supervised by
 * git-publish.mjs; direct imports retain the per-child API for controlled callers.
 * Private singleOperation workers perform only one network operation so the
 * controller can certify cleanup before launching readback.
 */
export function recover(options, execute = processResult, controls = {}) {
  const args = [options.operation, ...['repo', 'remote', 'url', 'ref', 'expect']
    .flatMap(key => ['--' + key, String(options[key] ?? '')]),
    '--token-file', options.tokenFile ?? 'gh.tkn', '--timeout-ms', String(options.timeoutMs ?? 30000),
    '--auth', options.auth ?? 'token'];
  if (options.credentialRepo) args.push('--credential-repo', options.credentialRepo);
  options = parseCli(args);
  const { git, auth, mode } = prepare(options, execute);
  let pushed;
  if (options.operation === 'push') {
    controls.onStage?.({ stage: 'push', auth_mode: mode });
    pushed = git(['push', '--porcelain', '--no-follow-tags', '--recurse-submodules=no',
      options.remote, options.expect + ':' + options.ref],
      [...auth, '-c', 'remote.' + options.remote + '.mirror=false']);
  }
  const push_result = processSummary(pushed, options.operation === 'push');
  if (options.operation === 'push' && controls.singleOperation) {
    return { schema_version: 1, ok: false, code: 'push_finished', stage: 'push',
      remote_state: 'unknown', push_attempted: true, push_result, auth_mode: mode };
  }
  let observed, readback;
  try {
    controls.onStage?.({ stage: 'readback', auth_mode: mode });
    readback = git(['ls-remote', '--refs', options.url, options.ref], auth);
    observed = remoteOid(checked(readback, 'readback'), options.ref);
  } catch (error) {
    const readback_result = processSummary(readback);
    if (error instanceof RecoveryError && ['ambiguous_readback', 'invalid_readback'].includes(error.code))
      readback_result.validation_error = error.code;
    return { schema_version: 1, ok: false, code: error instanceof RecoveryError ? error.code : 'readback_failed',
      stage: 'readback', remote_state: 'unknown', push_attempted: !!pushed, push_result,
      readback_result, auth_mode: mode };
  }
  const match = observed === options.expect;
  return { schema_version: 1, ok: match,
    code: match ? (pushed && (pushed.error || pushed.signal || pushed.status !== 0)
      ? 'verified_after_push_error' : 'remote_verified') : (observed ? 'remote_mismatch' : 'remote_absent'),
    stage: 'readback', remote_state: match ? 'matching' : observed ? 'different' : 'absent',
    push_attempted: !!pushed, expected: options.expect, observed, ref: options.ref,
    push_result, readback_result: processSummary(readback), auth_mode: mode };
}

/**
 * Build private-helper context without admitting relocation into public callers.
 * Git's transport supplies GIT_DIR and inherited command configuration. Resolve
 * the explicit worktree using a clean environment, then require GIT_DIR (when
 * present) to identify that worktree's actual administration directory. Other
 * relocation variables retain childEnv's rejection. No process.env mutation or
 * credential/configuration persistence occurs.
 * @param {string} selectedRepo Explicit repository passed by the parent utility.
 * @returns {{repo: string, env: object, git: Function}} Bound clean subprocesses.
 * @throws {RecoveryError|Error} Invalid worktree or mismatching helper context.
 */
function privateHelperContext(selectedRepo) {
  const base = Object.create(null);
  let directory;
  for (const [key, value] of Object.entries(process.env)) {
    if (/^GIT_DIR$/i.test(key)) {
      if (directory !== undefined) fail('helper_context_mismatch', 'helper');
      directory = value;
    } else if (!/^GIT_CONFIG_(?:PARAMETERS|COUNT|KEY_\d+|VALUE_\d+)$/i.test(key)) base[key] = value;
  }
  const env = childEnv(base), repo = fs.realpathSync(selectedRepo);
  const git = args => processResult('git', ['-C', repo, ...args], { cwd: repo, env });
  const root = checked(git(['rev-parse', '--show-toplevel']), 'helper').trim();
  if (!sameDirectory(root, repo)) fail('repo_must_be_root', 'helper');
  if (directory !== undefined) {
    const expected = checked(git(['rev-parse', '--absolute-git-dir']), 'helper').trim();
    let matches = false;
    try { matches = !!directory && sameDirectory(path.resolve(process.cwd(), directory), expected); } catch {}
    if (!matches) fail('helper_context_mismatch', 'helper');
  }
  return { repo, env, git };
}

/** Internal Git protocol entry. Credential stdout is consumed only by Git. */
function helperMain(args) {
  const [repo, tokenFile, url, ...tail] = args;
  const action = tail.at(-1);
  const selected = tail.length === 3 && tail[0] === '--credential-repo' ? tail[1] : undefined;
  if ((tail.length !== 1 && !selected) || !repo || !tokenFile || !url || !['get', 'store', 'erase'].includes(action)) fail('invalid_helper_arguments');
  if (action !== 'get') return;
  const buffer = Buffer.alloc(65537);
  let length = 0;
  while (length < buffer.length) {
    const read = fs.readSync(0, buffer, length, buffer.length - length, null);
    if (!read) break;
    length += read;
    if (buffer.subarray(0, length).includes(Buffer.from('\n\n')) || buffer.subarray(0, length).includes(Buffer.from('\r\n\r\n'))) break;
  }
  if (length > 65536) fail('invalid_credential_request');
  const request = credentialRequest(buffer.subarray(0, length).toString('utf8'));
  const target = validateTargetUrl(url);
  // Git URL-decodes the credential path once; validation excludes protocol controls.
  if (request.protocol !== 'https' || request.host !== target.host || request.path !== gitCredentialPath(target) ||
      (request.username && request.username !== 'x-access-token')) return;
  const context = privateHelperContext(repo);
  const gitAt = root => args => processResult('git', ['-C', root, ...args],
    { cwd: root, env: context.env });
  const credential = credentialContext(context.repo, selected, gitAt);
  const token = readToken(credential.repo, tokenFile, credential.git);
  process.stdout.write(`username=x-access-token\npassword=${token}\n\n`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT) {
  if (process.argv[2] === '--credential-helper') {
    try { helperMain(process.argv.slice(3)); }
    catch (error) { process.stderr.write(HELPER_MARKER + JSON.stringify(helperFailure(error)) + '\n'); process.exitCode = 1; }
  } else {
    try {
      if (Number(process.versions.node.split('.')[0]) < 22) fail('node_22_required');
      if (process.argv[2] === '--help') process.stdout.write(USAGE + '\n');
      else import('./git-publish.mjs')
        .then(module => module.runCli(process.argv.slice(2), { defaultAuth: 'token' }))
        .catch(() => { process.stdout.write(JSON.stringify({ schema_version: 1, ok: false,
          code: 'supervisor_unavailable', stage: 'preflight' }) + '\n'); process.exitCode = 1; });
    } catch (error) {
      process.stdout.write(JSON.stringify({ schema_version: 1, ok: false, code: error instanceof RecoveryError ? error.code : 'local_io_failed', stage: error instanceof RecoveryError ? error.stage : 'preflight' }) + '\n');
      process.exitCode = 1;
    }
  }
}
