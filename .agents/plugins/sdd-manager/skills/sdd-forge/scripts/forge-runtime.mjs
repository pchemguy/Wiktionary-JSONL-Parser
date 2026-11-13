/**
 * Native local execution boundary shared by forge utilities.
 * Explicit Git root/remote, bounded subprocesses, regular JSON input and
 * common-directory lock ownership; no credential or network import effects.
 * Token-file validation remains owned by sdd-manage/protected-token.mjs.
 */
import fs from 'node:fs';
import path from 'node:path';
import { randomUUID, createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { fail, ForgeError, repositoryName } from './github-client.mjs';
import { ProtectedInputError, readToken, sameDirectory, childEnv } from '../../sdd-manage/scripts/protected-token.mjs';
const MAX_JSON = 1024 * 1024;
/** Normalize established GitHub HTTPS/SSH push destinations without changes. */
export function remoteRepository(value) {
  let name;
  if (/^git@github\.com:/i.test(value)) name = value.slice(value.indexOf(':') + 1);
  else {
    let url; try { url = new URL(value); } catch { fail('unsupported_remote'); }
    if (url.hostname.toLowerCase() !== 'github.com' || url.password || url.search || url.hash
        || !['https:', 'ssh:'].includes(url.protocol) || (url.protocol === 'https:' && url.username)
        || (url.protocol === 'ssh:' && url.username !== 'git') || (url.port && !['443', '22'].includes(url.port))) fail('unsupported_remote');
    name = url.pathname.slice(1);
  }
  return repositoryName(name.replace(/\.git$/, ''));
}
/**
 * Reject known special/oversized paths before opening. POSIX nonblocking mode
 * also avoids waiting if a path becomes a FIFO after this check. Callers must
 * still validate the opened descriptor; this is not a trusted-filesystem waiver.
 */
function openRegular(filename, code) {
  const info = fs.statSync(filename);
  if (!info.isFile() || info.size > MAX_JSON) fail(code);
  const flags = fs.constants.O_RDONLY | (process.platform === 'win32' ? 0 : fs.constants.O_NONBLOCK);
  return fs.openSync(filename, flags);
}

/** Read one regular bounded UTF-8 JSON input; optional UTF-8 BOM is accepted. */
export function requestFile(filename) {
  const descriptor = openRegular(filename, 'invalid_request_file');
  try {
    const info = fs.fstatSync(descriptor);
    if (!info.isFile() || info.size > MAX_JSON) fail('invalid_request_file');
    const raw = Buffer.alloc(MAX_JSON + 1);
    const count = fs.readSync(descriptor, raw, 0, raw.length, 0);
    if (count > MAX_JSON) fail('invalid_request_file');
    try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(raw.subarray(0, count))); }
    catch { fail('invalid_request_json'); }
  } finally { fs.closeSync(descriptor); }
}
/** Acquire a common-directory lock; return cleanup bound to its nonce. */
export function acquireLock(common) {
  const directory = path.join(common, 'sdd-forge-close.lock'), nonce = randomUUID();
  try { fs.mkdirSync(directory, { mode: 0o700 }); }
  catch (error) { fail(error.code === 'EEXIST' ? 'operation_busy' : 'lock_unavailable', 'lock'); }
  const file = path.join(directory, 'owner.json');
  try { fs.writeFileSync(file, JSON.stringify({ nonce, pid: process.pid, created_at: new Date().toISOString() }), { flag: 'wx', mode: 0o600 }); }
  catch { try { fs.rmdirSync(directory); } catch {} fail('lock_unavailable', 'lock'); }
  return () => {
    if (JSON.parse(fs.readFileSync(file, 'utf8')).nonce !== nonce) fail('lock_ownership_changed', 'lock');
    fs.unlinkSync(file); fs.rmdirSync(directory);
  };
}

/** Produce safe known/unknown failure metadata without raw exception messages. */
export function failure(error, effects = {}) {
  const safe = error instanceof ForgeError || error instanceof ProtectedInputError;
  return { schema_version: 1, ok: false, code: safe ? error.code : 'operation_failed', stage: safe ? error.stage : 'preflight',
    remote_state: Object.values(effects).includes('unknown') ? 'unknown' : 'not_verified', effects: { ...effects },
    ...(safe && error.http_status ? { http_status: error.http_status } : {}), ...(safe && error.retry_at ? { retry_at: error.retry_at } : {}),
    ...(safe && error.request_id ? { request_id: error.request_id } : {}),
    ...(safe && Number.isSafeInteger(error.attempts) ? { attempts: error.attempts } : {}) };
}
/** Reject a protected credential's literal occurrence in structured content. */
export function containsCredential(value, token) {
  if (typeof value === 'string') return value.includes(token);
  return value && typeof value === 'object' && Object.values(value).some(item => containsCredential(item, token));
}


/** Establish the exact root/destination and bounded native Git context. */
export function createContext(options, repository, started = performance.now()) {
  const repo = fs.realpathSync(options.repo), env = childEnv();
  const remainingMs = () => options.timeoutMs - (performance.now() - started);
  const git = (args, { encoding = 'utf8' } = {}) => {
    if (remainingMs() <= 0) return { error: { code: 'ETIMEDOUT' }, status: null };
    return spawnSync('git', ['-C', repo, ...args], { encoding, env, windowsHide: true, shell: false,
      timeout: Math.max(1, Math.floor(Math.min(10000, remainingMs()))), maxBuffer: 1024 * 1024 });
  };
  const checked = args => {
    const result = git(args);
    if (result.error || result.signal || result.status !== 0) fail('git_preflight_failed');
    return result.stdout.trim();
  };
  if (!sameDirectory(checked(['rev-parse', '--show-toplevel']), repo)) fail('repo_must_be_root');
  const urls = checked(['remote', 'get-url', '--push', '--all', options.remote]).split(/\r?\n/);
  if (urls.length !== 1) fail('destination_mismatch');
  const destination = remoteRepository(urls[0]);
  if (repository !== undefined && destination !== repository) fail('destination_mismatch');
  const common = fs.realpathSync(path.resolve(repo, checked(['rev-parse', '--git-common-dir'])));
  return { repo, git, checked, remainingMs, common, repository: destination };
}

/**
 * Read a contained regular Markdown owner and bind its actual raw-byte hash.
 * For execution, repo sources must equal HEAD text, allowing only native CRLF
 * checkout conversion. No configured clean/textconv filter is executed.
 */
export function inspectSource(context, source, { committed = false } = {}) {
  if (!source || !['repo', 'plugin'].includes(source.root) || typeof source.path !== 'string'
      || source.path.includes('\\') || source.path.includes(':') || source.path.startsWith('/')
      || source.path.split('/').some(part => !part || part === '.' || part === '..') || !/\.md$/i.test(source.path)
      || (source.root === 'plugin' && source.path !== 'assets/DOCS_TASKS_TEMPLATE.md')) fail('invalid_source');
  const root = source.root === 'repo' ? context.repo : fileURLToPath(new URL('../../../', import.meta.url));
  const filename = fs.realpathSync(path.resolve(root, source.path)), relative = path.relative(fs.realpathSync(root), filename);
  if (relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative)) fail('source_outside_root');
  const fd = openRegular(filename, 'invalid_source'); let raw;
  try {
    const stat = fs.fstatSync(fd);
    if (!stat.isFile() || stat.size > MAX_JSON) fail('invalid_source');
    const bytes = Buffer.alloc(MAX_JSON + 1), size = fs.readSync(fd, bytes, 0, bytes.length, 0);
    if (size > MAX_JSON) fail('invalid_source');
    raw = bytes.subarray(0, size);
  } finally { fs.closeSync(fd); }
  let content;
  try { content = new TextDecoder('utf-8', { fatal: true }).decode(raw); } catch { fail('invalid_source_encoding'); }
  const sha256 = createHash('sha256').update(raw).digest('hex');
  if (source.sha256 !== undefined && source.sha256 !== sha256) fail('source_changed');
  if (committed && source.root === 'repo') {
    const head = context.git(['show', 'HEAD:' + source.path], { encoding: null });
    let committedText;
    try {
      if (head.error || head.status !== 0) fail('source_not_committed');
      committedText = new TextDecoder('utf-8', { fatal: true }).decode(head.stdout);
    } catch { fail('source_not_committed'); }
    if (content.replace(/\r\n/g, '\n') !== committedText.replace(/\r\n/g, '\n')) fail('source_not_committed');
  }
  return { source: { root: source.root, path: source.path, sha256 }, content };
}

/**
 * Select the existing docs owner, or the package template before it exists.
 * Only absence of the default path permits bootstrap fallback; an explicit,
 * malformed, unreadable or dangling source never falls back. No file is made.
 * @param {object} context Validated native repository context.
 * @param {string} [tasks] Explicit repository-relative Markdown owner.
 * @param {object} [options] inspectSource committed-source requirements.
 * @returns {object} Inspected content and raw-byte source identity.
 */
export function inspectDocsSource(context, tasks, options = {}) {
  const filename = tasks === undefined ? 'docs/dev/DOCS_TASKS.md' : tasks.replaceAll('\\', '/');
  if (tasks === undefined) {
    try { fs.lstatSync(path.join(context.repo, filename)); }
    catch (error) {
      if (error.code !== 'ENOENT') fail('invalid_source');
      return inspectSource(context, { root: 'plugin', path: 'assets/DOCS_TASKS_TEMPLATE.md' }, options);
    }
  }
  return inspectSource(context, { root: 'repo', path: filename }, options);
}

/** Read an eligible repository token through the bounded Git context. */
export function protectedToken(context, tokenFile) {
  return readToken(context.repo, tokenFile, context.git);
}

/** Native file identity handles Windows case/short-path entry spellings. */
export function isMain(metaUrl) {
  try {
    if (!process.argv[1]) return false;
    const a = fs.statSync(process.argv[1]), b = fs.statSync(fileURLToPath(metaUrl));
    return a.dev === b.dev && a.ino === b.ino;
  } catch { return false; }
}
