/**
 * Shared GitHub-bound transport for optional forge executables.
 * Node >=22; import-safe and dependency-free. Bounded reads, pagination,
 * cancellation and sanitized failures; capability validation owns writes.
 * Caller authorization and cross-machine exclusivity remain external.
 */
const API = 'https://api.github.com';
const MAX_RESPONSE = 8 * 1024 * 1024;
const MAX_PAGES = 100;
/** Safe public failure metadata; raw transport/credential values are excluded. */
export class ForgeError extends Error {
  constructor(code, stage = 'preflight', details = {}) {
    super(code); this.code = code; this.stage = stage; Object.assign(this, details);
  }
}
export const fail = (code, stage, details) => { throw new ForgeError(code, stage, details); };
export const positive = value => Number.isSafeInteger(value) && value > 0;
/**
 * Check one exact phase association while preserving unrelated labels.
 * @param {object[]} labels Provider label records, each with a nonblank name.
 * @param {string|null} expected Exact caller label, or null for docs-main.
 * @returns {boolean} False for malformed, duplicate or foreign phase labels.
 * Managed namespace detection is case-insensitive; ownership spelling is exact.
 * Explicit custom completion labels remain supported without another managed phase.
 */
export function phaseLabelsMatch(labels, expected) {
  if (!Array.isArray(labels) || labels.some(label => typeof label?.name !== 'string' || !label.name.trim())) return false;
  const managed = labels.filter(label => /^sdd-phase-[1-9]\d*-/i.test(label.name));
  return expected === null ? managed.length === 0
    : labels.filter(label => label.name === expected).length === 1
      && managed.length <= 1 && managed.every(label => label.name === expected);
}
/** Validate bounded UTF-8 authored text, excluding reserved ownership markers. */
export function text(value, max = 16000, multiline = false) {
  return typeof value === 'string' && value.trim().length > 0 && Buffer.byteLength(value) <= max
    && Buffer.from(value).toString('utf8') === value
    && !(multiline ? /[\x00-\x08\x0b-\x1f\x7f]/ : /[\x00-\x1f\x7f]/).test(value)
    && !value.includes('<!-- sdd-forge:');
}
/** Reject absent/extra fields before interpreting a versioned object. */
export function keys(value, required, optional = []) {
  if (!value || typeof value !== 'object' || Array.isArray(value)
      || required.some(key => !Object.hasOwn(value, key))
      || Object.keys(value).some(key => !required.includes(key) && !optional.includes(key))) fail('invalid_schema');
}
/** Normalize one GitHub owner/name identity, never an arbitrary URL. */
export function repositoryName(value) {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9][a-zA-Z0-9-]{0,38}\/[a-zA-Z0-9_.-]{1,100}$/.test(value)
      || ['.', '..'].includes(value.split('/')[1])) fail('invalid_repository');
  return value.toLowerCase();
}
// Bound our wait even if an injected stream does not propagate fetch abort.
async function abortable(promise, signal) {
  if (signal.aborted) throw new Error('aborted');
  let abort;
  const stopped = new Promise((_, reject) => { abort = () => reject(new Error('aborted')); });
  signal.addEventListener('abort', abort, { once: true });
  try { return await Promise.race([promise, stopped]); }
  finally { signal.removeEventListener('abort', abort); }
}

/**
 * GitHub-only bounded transport. Credentials stay in request headers only.
 * fetchImpl/clock/sleep are injectable dependency boundaries for controlled
 * execution. Production defaults use native fetch and monotonic elapsed time.
 * No mutation is retried here; safe reads have at most three retries.
 */
export class GitHubTransport {
  /**
   * @param {object} options Explicit scope and protected in-memory credential.
   * @param {string} options.repository GitHub owner/repository, never a URL.
   * @param {string} options.token Eligible credential; never print this client.
   * @param {'completion'|'projection'} [options.capability='completion'] Immutable route/mutation boundary.
   * @param {number} [options.timeoutMs=60000] Overall monotonic elapsed budget.
   * @param {number} [options.requestTimeoutMs=15000] Per-request/body budget.
   * @param {Function} [options.fetchImpl] Native-compatible HTTP dependency.
   * @param {Function} [options.clock] Monotonic millisecond clock.
   * @param {Function} [options.sleep] Awaitable millisecond delay.
   */
  constructor({ repository, token, capability = 'completion', timeoutMs = 60000, requestTimeoutMs = 15000, fetchImpl = globalThis.fetch,
    clock = () => performance.now(), sleep = ms => new Promise(resolve => setTimeout(resolve, ms)) }) {
    if (!['completion', 'projection'].includes(capability) || typeof token !== 'string' || !/^[\x21-\x7e]{1,16384}$/.test(token)
        || !Number.isFinite(timeoutMs) || timeoutMs <= 0 || !Number.isFinite(requestTimeoutMs) || requestTimeoutMs <= 0
        || typeof fetchImpl !== 'function' || typeof clock !== 'function' || typeof sleep !== 'function') fail('invalid_client_options');
    this.repository = repositoryName(repository); this.base = API + '/repos/' + this.repository;
    this.token = token; this.fetchImpl = fetchImpl; this.clock = clock; this.sleep = sleep;
    this.deadline = clock() + timeoutMs; this.requestTimeoutMs = requestTimeoutMs; this.lastMutation = null; this.repositoryId = null;
    this.readRetries = 0; this.retryFailures = [];
    Object.defineProperty(this, 'capability', { value: capability });
  }
  /** @private Remaining elapsed budget, in milliseconds. */
  remaining() { return Math.max(0, this.deadline - this.clock()); }
  /** @private Wait only within the current budget; never reset it. */
  async wait(ms, code = 'deadline_exceeded', retryAt) {
    if (ms >= this.remaining()) fail(code, 'transport', retryAt ? { retry_at: retryAt } : {});
    await this.sleep(ms);
  }
  /** @private Resolve only this repository's canonical/identity-based routes. */
  target(raw) {
    let url;
    try { url = new URL(raw.startsWith('https://') ? raw : this.base + raw); }
    catch { fail('invalid_api_target', 'transport'); }
    const prefixes = ['/repos/' + this.repository, ...(this.repositoryId ? ['/repositories/' + this.repositoryId] : [])];
    const prefix = prefixes.find(item => url.pathname === item || url.pathname.startsWith(item + '/'));
    if (url.origin !== API || url.username || url.password || url.hash || !prefix) fail('api_target_mismatch', 'transport');
    const suffix = url.pathname.slice(prefix.length);
    const route = this.capability === 'projection'
      ? /^(?:|\/labels|\/issues(?:\/\d+)?|\/milestones(?:\/\d+)?)$/
      : /^(?:|\/issues(?:\/\d+(?:\/comments)?)?|\/milestones(?:\/\d+)?)$/;
    if (!route.test(suffix)) fail('api_target_mismatch', 'transport');
    return url;
  }
  /** @private One bounded request; cleanup cannot renew its budget. */
  async once(method, raw, body) {
    const url = this.target(raw);
    if (!['GET', 'POST', 'PATCH'].includes(method)) fail('invalid_method', 'transport');
    const suffix = url.pathname.replace(/^\/(?:repos\/[^/]+\/[^/]+|repositories\/\d+)/, '');
    if (this.capability === 'projection' && method !== 'GET') {
      if (method !== 'POST') fail('unsupported_mutation', 'transport');
      if (suffix === '/labels') {
        keys(body, ['name', 'color', 'description']);
        if (!text(body.name, 100) || !/^sdd-phase-[1-9]\d*-.+/.test(body.name)
            || !/^[a-f0-9]{6}$/.test(body.color) || !text(body.description, 100)) fail('unsupported_mutation', 'transport');
      } else if (suffix === '/milestones') {
        keys(body, ['title', 'state', 'description']);
        if (body.state !== 'open' || !text(body.title, 255)
            || !/^(?:sdd-[1-9]\d*(?:\.[1-9]\d*)+-.+|sdd-docs-main)$/.test(body.title)
            || !text(body.description, 16000, true)) fail('unsupported_mutation', 'transport');
      } else if (suffix === '/issues') {
        keys(body, ['title', 'body', 'labels', 'milestone']);
        const opening = typeof body.body === 'string' && body.body.match(/^(?:<!-- sdd-forge:docs-scope=main -->\n)?## Task brief <!-- sdd-forge:task-id=(T-\d{3,}|DOCS-\d{3}) -->\n/);
        if (!opening || !text(body.title, 255) || !body.title.startsWith('[' + opening[1] + '] ')
            || Buffer.byteLength(body.body) > 32768 || Buffer.from(body.body).toString('utf8') !== body.body
            || /[\x00-\x08\x0b-\x1f\x7f]/.test(body.body)
            || !Array.isArray(body.labels) || body.labels.length > 1
            || body.labels.some(value => !text(value, 100) || !/^sdd-phase-[1-9]\d*-.+/.test(value))
            || !positive(body.milestone)) fail('unsupported_mutation', 'transport');
      } else fail('unsupported_mutation', 'transport');
    } else if (method === 'POST') {
      keys(body, ['body']);
      const comment = body.body;
      if (!/^\/issues\/\d+\/comments$/.test(suffix) || typeof comment !== 'string' || Buffer.byteLength(comment) > 32768
          || Buffer.from(comment).toString('utf8') !== comment || /[\x00-\x08\x0b-\x1f\x7f]/.test(comment)
          || !/^<!-- sdd-forge:completion task=T-\d{3,} commit=(?:[a-f0-9]{40}|[a-f0-9]{64}) -->\n/.test(comment)) fail('unsupported_mutation', 'transport');
    } else if (method === 'PATCH') {
      if (/^\/issues\/\d+$/.test(suffix)) {
        keys(body, ['state', 'state_reason']);
        if (body.state !== 'closed' || body.state_reason !== 'completed') fail('unsupported_mutation', 'transport');
      } else if (/^\/milestones\/\d+$/.test(suffix)) {
        keys(body, ['state']);
        if (body.state !== 'closed') fail('unsupported_mutation', 'transport');
      } else fail('unsupported_mutation', 'transport');
    } else if (body !== undefined) fail('unsupported_request_body', 'transport');
    if (body !== undefined && JSON.stringify(body).includes(this.token)) fail('credential_in_request', 'preflight');
    if (this.remaining() <= 0) fail('deadline_exceeded', 'transport');
    if (method !== 'GET' && this.lastMutation !== null) await this.wait(Math.max(0, 1000 - (this.clock() - this.lastMutation)));
    if (this.remaining() <= 0) fail('deadline_exceeded', 'transport');
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), Math.min(this.requestTimeoutMs, this.remaining()));
    let sent = false;
    try {
      sent = true;
      if (method !== 'GET') this.lastMutation = this.clock();
      const response = await abortable(this.fetchImpl(url.href, { method, redirect: 'manual', signal: controller.signal,
        headers: { Accept: 'application/vnd.github+json', Authorization: 'Bearer ' + this.token,
          'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json', 'User-Agent': 'sdd-manager-forge-close' },
        ...(body === undefined ? {} : { body: JSON.stringify(body) }) }), controller.signal);
      const chunks = []; let size = 0;
      if (response.body) {
        const reader = response.body.getReader(); let finished = false;
        try {
          for (;;) {
            const item = await abortable(reader.read(), controller.signal);
            if (item.done) { finished = true; break; }
            size += item.value.byteLength;
            if (size > MAX_RESPONSE) fail('response_too_large', 'transport');
            chunks.push(item.value);
          }
        } finally {
          // A tee/foreign stream can leave cancel pending on its other reader.
          // Do not let cleanup renew the operation budget or conceal uncertainty.
          if (!finished) void reader.cancel().catch(() => {});
          reader.releaseLock();
        }
      }
      let rawBody;
      try { rawBody = new TextDecoder('utf-8', { fatal: true }).decode(Buffer.concat(chunks)); }
      catch { fail('invalid_response', 'transport'); }
      if (!response.ok) {
        const rate = response.status === 429 || (response.status === 403 && (response.headers.get('retry-after')
          || response.headers.get('x-ratelimit-remaining') === '0' || /secondary rate limit/i.test(rawBody)));
        let delay = 0;
        if (rate) {
          const after = response.headers.get('retry-after'), reset = response.headers.get('x-ratelimit-reset');
          if (after) delay = /^\d+$/.test(after) ? Number(after) * 1000 : Math.max(0, Date.parse(after) - Date.now());
          if (response.headers.get('x-ratelimit-remaining') === '0' && /^\d+$/.test(reset || '')) delay = Math.max(delay, Number(reset) * 1000 - Date.now());
          if (!Number.isFinite(delay) || delay <= 0) delay = 60000;
        }
        const identifier = response.headers.get('x-github-request-id');
        fail(rate ? 'rate_limited' : response.status === 401 ? 'authentication_failed'
          : response.status === 403 ? 'access_or_policy_denied' : response.status === 404 ? 'access_or_missing'
            : response.status >= 300 && response.status < 400 ? 'redirect_rejected'
              : response.status >= 500 ? 'service_unavailable' : 'request_rejected', 'transport', {
          http_status: response.status, uncertain: method !== 'GET' && response.status >= 500,
          retryable: rate || response.status >= 500, delay,
          ...(rate && delay < 8e15 - Date.now() ? { retry_at: new Date(Date.now() + delay).toISOString() } : {}),
          ...(identifier && /^[a-zA-Z0-9:-]{1,128}$/.test(identifier) ? { request_id: identifier } : {}),
        });
      }
      if (response.status !== (method === 'POST' ? 201 : 200)) fail('unexpected_status', 'transport');
      let data;
      try { data = JSON.parse(rawBody); } catch { fail('invalid_response', 'transport'); }
      return { data, link: response.headers.get('link') };
    } catch (error) {
      if (error instanceof ForgeError) {
        if (method !== 'GET' && sent && error.uncertain === undefined) error.uncertain = true;
        throw error;
      }
      throw new ForgeError(controller.signal.aborted ? 'request_timeout' : 'transport_failed', 'transport',
        { uncertain: method !== 'GET' && sent, retryable: true });
    } finally { clearTimeout(timer); }
  }
  /**
   * Issue an allowed exact request; only safe reads have bounded retries.
   * @param {'GET'|'POST'|'PATCH'} method Read or capability-permitted mutation.
   * @param {string} raw Repository-relative route or validated pagination URL.
   * @param {object} [body] Exact permitted mutation shape; omitted for GET.
   * @returns {Promise<{data: object|Array, link: string|null}>} Decoded response.
   * @throws {ForgeError} Safe classified failure, including uncertain effects.
   */
  async request(method, raw, body) {
    for (let attempt = 0; ; attempt++) {
      try { return await this.once(method, raw, body); }
      catch (error) {
        if (error instanceof ForgeError) error.attempts = attempt + 1;
        if (!(error instanceof ForgeError) || method !== 'GET' || !error.retryable || attempt === 3) throw error;
        const delay = error.delay || 100 * 2 ** attempt;
        if (delay >= this.remaining()) throw error;
        await this.wait(delay, error.code, error.retry_at);
        this.readRetries++;
        if (this.retryFailures.length < 8) this.retryFailures.push({ code: error.code, ...(error.http_status ? { http_status: error.http_status } : {}) });
      }
    }
  }
  /**
   * Exhaust a bounded collection; incomplete pages never imply absence.
   * @param {string} suffix Repository-relative collection route.
   * @param {object} [params] Fixed collection filters, preserved across pages.
   * @returns {Promise<object[]>} Complete observed unique object collection.
   * @throws {ForgeError} Incomplete, contradictory or failed enumeration.
   */
  async list(suffix, params = {}) {
    const first = this.target(suffix); first.search = new URLSearchParams({ ...params, per_page: '100' }).toString();
    let url = first, page = 1; const seen = new Set(), ids = new Set(), result = [];
    for (;;) {
      if (page > MAX_PAGES || seen.has(url.href)) fail('pagination_incomplete', 'lookup');
      seen.add(url.href);
      const response = await this.request('GET', url.href);
      if (!Array.isArray(response.data)) fail('invalid_response', 'lookup');
      for (const item of response.data) {
        if (!item || !positive(item.id) || ids.has(item.id)) fail('pagination_conflict', 'lookup');
        ids.add(item.id); result.push(item);
      }
      if (!response.link) return result;
      const entries = response.link.split(',').map(item => item.trim());
      const next = [];
      for (const entry of entries) {
        const match = entry.match(/^<([^>]+)>;\s*rel="([^"]+)"$/);
        if (!match) fail('invalid_pagination', 'lookup');
        if (match[2].split(' ').includes('next')) next.push(match[1]);
      }
      if (!next.length) return result;
      if (next.length !== 1) fail('invalid_pagination', 'lookup');
      const candidate = this.target(next[0]); page++;
      const strip = value => {
        const copy = new URL(value); copy.searchParams.delete('page');
        return JSON.stringify([...copy.searchParams].sort());
      };
      const suffixOf = value => value.pathname.replace(/^\/(?:repos\/[^/]+\/[^/]+|repositories\/\d+)/, '');
      if (candidate.searchParams.getAll('page').length !== 1 || candidate.searchParams.get('page') !== String(page)
          || suffixOf(candidate) !== suffixOf(first) || strip(candidate) !== strip(first)) fail('invalid_pagination', 'lookup');
      url = candidate;
    }
  }
  /**
   * Bind full name/numeric identity before allowing ID-based pagination.
   * @returns {Promise<object>} Verified repository metadata; stores numeric identity.
   * @throws {ForgeError} Access failure, redirect or mismatched repository.
   */
  async identify() {
    const { data } = await this.request('GET', '');
    if (!data || !positive(data.id) || typeof data.full_name !== 'string' || data.full_name.toLowerCase() !== this.repository) fail('repository_mismatch', 'lookup');
    this.repositoryId = data.id;
    return data;
  }
}

