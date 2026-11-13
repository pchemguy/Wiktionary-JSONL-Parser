/**
 * Contained root-relative token input shared by SDD Manager utilities.
 *
 * Node >=22 and native Git. Files use the caller's ordinary OS read access.
 * This module never stores credentials, inspects or repairs file permissions,
 * changes configuration, performs network requests or runs on import.
 * Callers establish the trusted repository and bound their Git runner; this
 * validates containment, exclusion, file identity and token bytes.
 */
import fs from 'node:fs';
import path from 'node:path';

const MAX_TOKEN = 16384;
/** A public error code/stage, deliberately excluding raw subprocess output. */
export class ProtectedInputError extends Error {
  constructor(code, stage = 'preflight') { super(code); this.code = code; this.stage = stage; }
}
const fail = (code, stage) => { throw new ProtectedInputError(code, stage); };

/**
 * Compare actual directory identity across native case/short-path spellings.
 * @param {string} a Existing directory path.
 * @param {string} b Existing directory path.
 * @returns {boolean} Whether both identify the same directory.
 * @throws {Error} Native metadata cannot be read.
 */
export function sameDirectory(a, b) {
  const left = fs.statSync(a), right = fs.statSync(b);
  return left.isDirectory() && right.isDirectory() && left.dev === right.dev && left.ino === right.ino;
}

/**
 * Accept one normal line ending; never trim malformed credential values.
 * @param {string} raw Bounded file contents; never pass via argv/logging.
 * @returns {string} Secret, for private authenticated-client use only.
 * @throws {ProtectedInputError} Empty, oversized or non-single-line ASCII token.
 */
export function validateToken(raw) {
  const token = raw.replace(/\r?\n$/, '');
  if (!token || Buffer.byteLength(raw) > MAX_TOKEN || /[^\x21-\x7e]/.test(token)) fail('invalid_token');
  return token;
}

/**
 * Preserve the process context while excluding credential/trace channels.
 * @param {object} [base] Process environment; values are never logged.
 * @returns {object} Noninteractive environment without injected trace/auth flags.
 * @throws {ProtectedInputError} Git relocation/config environment is present.
 */
export function childEnv(base = process.env) {
  const env = {};
  for (const [key, value] of Object.entries(base)) {
    if (/^(GIT_DIR|GIT_WORK_TREE|GIT_COMMON_DIR|GIT_INDEX_FILE|GIT_CONFIG|GIT_CONFIG_PARAMETERS|GIT_CONFIG_COUNT|GIT_CONFIG_KEY_\d+|GIT_CONFIG_VALUE_\d+)$/i.test(key)) fail('relocated_git_environment');
    if (/^(GIT_ASKPASS|SSH_ASKPASS|GIT_TRACE.*|GIT_CURL_VERBOSE|GIT_TRACE_CURL.*|GIT_TERMINAL_PROMPT|GCM_INTERACTIVE)$/i.test(key)) continue;
    env[key] = value;
  }
  return { ...env, GIT_TERMINAL_PROMPT: '0', GCM_INTERACTIVE: 'never' };
}

function checked(result, stage) {
  if (result.error) fail(result.error.code === 'ETIMEDOUT' ? 'process_timeout' : 'process_unavailable', stage);
  if (result.signal) fail('process_signal', stage);
  if (result.status !== 0) fail('git_failed', stage);
  return result.stdout || '';
}

/**
 * Validate a selected root-relative token before bounded reading. The caller
 * establishes trusted path context; this is not a hostile same-user race sandbox.
 * Ordinary OS read access is sufficient on Windows and POSIX.
 * @param {string} repo Resolved eligible worktree root.
 * @param {string} tokenFile Root-relative selected token-file path.
 * @param {Function} git Bounded Git runner returning spawnSync-style results.
 * @returns {string} Secret for private credential use, never diagnostic output.
 * @throws {ProtectedInputError|Error} Invalid path/context, format or local I/O.
 */
export function readToken(repo, tokenFile, git) {
  if (path.isAbsolute(tokenFile)) fail('token_outside_repository');
  const filename = path.resolve(repo, tokenFile), relative = path.relative(repo, filename);
  if (!relative || relative.startsWith('..' + path.sep) || relative === '..') fail('token_outside_repository');
  let current = repo;
  for (const part of relative.split(path.sep)) {
    current = path.join(current, part);
    if (fs.lstatSync(current).isSymbolicLink()) fail('token_symlink');
  }
  const info = fs.lstatSync(filename);
  if (!info.isFile() || info.nlink !== 1 || info.size > MAX_TOKEN) fail('invalid_token_file');
  const parentRoot = checked(git(['-C', path.dirname(filename), 'rev-parse', '--show-toplevel']), 'token');
  if (!sameDirectory(parentRoot.trim(), repo)) fail('token_outside_repository');
  if (git(['check-ignore', '--no-index', '--', relative]).status !== 0) fail('token_not_ignored');
  const tracked = git(['ls-files', '--error-unmatch', '--', `:(literal)${relative}`]);
  if (tracked.status !== 1 || tracked.error || tracked.signal) fail('token_tracked_or_unknown');
  const descriptor = fs.openSync(filename, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  try {
    const actual = fs.fstatSync(descriptor);
    if (actual.dev !== info.dev || actual.ino !== info.ino) fail('token_changed');
    const data = Buffer.alloc(MAX_TOKEN + 1);
    const length = fs.readSync(descriptor, data, 0, data.length, 0);
    if (length > MAX_TOKEN) fail('invalid_token');
    return validateToken(data.subarray(0, length).toString('utf8'));
  } finally { fs.closeSync(descriptor); }
}
