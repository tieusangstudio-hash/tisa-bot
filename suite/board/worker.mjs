// Khung quản lý Đội Quân AI: bảng giao việc cho một doanh nghiệp.
// Cloudflare Worker + D1 (dữ liệu) + KV (ảnh, tệp). TISA BOT nhận việc qua cầu nối trên máy chủ doanh nghiệp,
// hoặc đội chạy ngay trong trang bằng khóa Claude (đi qua /api/ai, khóa không bao giờ về trình duyệt).
import { readFileSync } from 'node:fs';
const BOARD = readFileSync(new URL('./board.html', import.meta.url), 'utf8');
const KIT_DEFAULT = JSON.parse(readFileSync(new URL('./kit-default.json', import.meta.url), 'utf8'));

const SALT = 'tisa-agent-hq|v1|';
const COLS = new Set(['tasks', 'schedules', 'reports', 'results', 'inputs', 'settings', 'messages', 'library']);
// Tin hệ thống: cầu nối trên máy tự xử lý, không phải tin trao đổi với nhân sự
const SYS_KINDS = new Set(['mo-thu-muc', 'kiem-tra-ket-noi', 'lien-ket-thu-muc', 'ghi-boc-tach', 'phan-loai-ngay']);
// Logo doanh nghiệp cho thẻ tab trình duyệt
const FAVICON_B64 = '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';
const SESSION_DAYS = 30;
const MAX_BLOB = 24 * 1024 * 1024;
const enc = new TextEncoder();

const hex = (buf) => [...new Uint8Array(buf)].map((x) => x.toString(16).padStart(2, '0')).join('');
const sha256 = async (s) => hex(await crypto.subtle.digest('SHA-256', enc.encode(s)));
async function hmac(key, msg) {
  const k = await crypto.subtle.importKey('raw', enc.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return hex(await crypto.subtle.sign('HMAC', k, enc.encode(msg)));
}
function same(a, b) {
  a = String(a || ''); b = String(b || '');
  if (!a || a.length !== b.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
const json = (o, status = 200, extra = {}) => new Response(JSON.stringify(o), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra },
});
const err = (status, msg) => json({ error: msg }, status);
const now = () => new Date().toISOString();
const rid = (p = '') => p + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);

function cookie(req, name) {
  const c = req.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : '';
}
// Phiên đăng nhập = hạn + chữ ký. Đổi mật khẩu thì tăng "đời phiên" để mọi phiên cũ hết hiệu lực.
let epochCache = { v: null, t: 0 };
async function sessionEpoch(env) {
  if (epochCache.v !== null && Date.now() - epochCache.t < 30000) return epochCache.v;
  const v = (await secretGet(env, 'session_epoch')) || '0';
  epochCache = { v, t: Date.now() };
  return v;
}
const sessMsg = (exp, epoch) => (epoch === '0' ? 'dq|' + exp : 'dq|' + exp + '|' + epoch);
async function sessionCookie(env) {
  const exp = Date.now() + SESSION_DAYS * 864e5;
  const v = exp + '.' + (await hmac(env.BOARD_API_TOKEN, sessMsg(exp, await sessionEpoch(env))));
  return `dq_s=${v}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`;
}
async function sessionOk(req, env) {
  const v = cookie(req, 'dq_s'); if (!v) return false;
  const [exp, sig] = v.split('.');
  if (!exp || !sig || Number(exp) < Date.now()) return false;
  return same(sig, await hmac(env.BOARD_API_TOKEN, sessMsg(exp, await sessionEpoch(env))));
}
function bearerOk(req, env) {
  const h = req.headers.get('authorization') || '';
  const t = h.startsWith('Bearer ') ? h.slice(7).trim() : '';
  return !!env.BOARD_API_TOKEN && same(t, env.BOARD_API_TOKEN);
}

/* ---------------- Kho dữ liệu ---------------- */
async function bump(env, col) {
  const r = await env.DB.batch([
    env.DB.prepare("UPDATE meta SET v = v + 1 WHERE k = 'ver' RETURNING v"),
    env.DB.prepare("INSERT INTO meta (k, v) VALUES (?1, 1) ON CONFLICT(k) DO UPDATE SET v = v + 1").bind('ver:' + col),
  ]);
  return r[0].results[0].v;
}
async function getDoc(env, col, id) {
  const r = await env.DB.prepare('SELECT data, ver FROM docs WHERE col = ?1 AND id = ?2').bind(col, id).first();
  return r ? { data: JSON.parse(r.data), ver: r.ver } : null;
}
async function putDoc(env, col, id, data) {
  const ver = await bump(env, col);
  const d = { ...data }; delete d.id;
  await env.DB.prepare('INSERT INTO docs (col, id, data, ver) VALUES (?1, ?2, ?3, ?4) ON CONFLICT(col, id) DO UPDATE SET data = excluded.data, ver = excluded.ver')
    .bind(col, id, JSON.stringify(d), ver).run();
  return ver;
}
// Đọc - sửa - ghi có kiểm tra phiên bản, để nhiều nhân sự TISA BOT báo cùng lúc không đè lên nhau.
async function mutate(env, col, id, fn) {
  for (let i = 0; i < 6; i++) {
    const cur = await getDoc(env, col, id);
    const next = await fn(cur ? cur.data : null);
    if (next === undefined) return cur ? cur.data : null;
    const d = { ...next }; delete d.id;
    const ver = await bump(env, col);
    const res = cur
      ? await env.DB.prepare('UPDATE docs SET data = ?1, ver = ?2 WHERE col = ?3 AND id = ?4 AND ver = ?5').bind(JSON.stringify(d), ver, col, id, cur.ver).run()
      : await env.DB.prepare('INSERT OR IGNORE INTO docs (col, id, data, ver) VALUES (?1, ?2, ?3, ?4)').bind(col, id, JSON.stringify(d), ver).run();
    if (res.meta.changes === 1) return d;
    await new Promise((r) => setTimeout(r, 40 + Math.random() * 120));
  }
  throw new Error('busy');
}
async function listCol(env, col) {
  const r = await env.DB.prepare('SELECT id, data FROM docs WHERE col = ?1').bind(col).all();
  return r.results.map((x) => ({ id: x.id, ...JSON.parse(x.data) }));
}
async function versions(env) {
  const r = await env.DB.prepare("SELECT k, v FROM meta WHERE k = 'ver' OR k LIKE 'ver:%'").all();
  const out = { ver: 0, cols: {} };
  r.results.forEach((x) => { if (x.k === 'ver') out.ver = x.v; else out.cols[x.k.slice(4)] = x.v; });
  return out;
}


/* ---------------- Khóa bí mật, cấu hình khung, nhịp TISA BOT ---------------- */
let secretsReady = false;
async function ensureSecrets(env) {
  if (secretsReady) return;
  await env.DB.prepare('CREATE TABLE IF NOT EXISTS secrets (k TEXT PRIMARY KEY, v TEXT NOT NULL, updated TEXT)').run();
  secretsReady = true;
}
async function secretGet(env, k) {
  await ensureSecrets(env);
  const r = await env.DB.prepare('SELECT v FROM secrets WHERE k = ?1').bind(k).first();
  return r ? r.v : '';
}
async function secretSet(env, k, v) {
  await ensureSecrets(env);
  if (!v) { await env.DB.prepare('DELETE FROM secrets WHERE k = ?1').bind(k).run(); return; }
  await env.DB.prepare('INSERT INTO secrets (k, v, updated) VALUES (?1, ?2, ?3) ON CONFLICT(k) DO UPDATE SET v = excluded.v, updated = excluded.updated').bind(k, v, now()).run();
}
async function boardHash(env) { return (await secretGet(env, 'board_hash')) || env.BOARD_HASH || ''; }
async function claudeKey(env) { return env.ANTHROPIC_API_KEY || (await secretGet(env, 'anthropic')); }
async function kitDoc(env) { const d = await getDoc(env, 'settings', 'kit'); return d ? d.data : {}; }
// Khung mặc định + phần chủ doanh nghiệp đã lưu (giống cách trang ghép trong build.py)
function mergeKit(saved) {
  const K = { ...KIT_DEFAULT };
  for (const [k, v] of Object.entries(saved || {})) {
    if (v == null) continue;
    const d = KIT_DEFAULT[k];
    K[k] = (v && typeof v === 'object' && !Array.isArray(v) && d && typeof d === 'object' && !Array.isArray(d)) ? { ...d, ...v } : v;
  }
  return K;
}
// Đội hình đang bật (đổi tên, tắt, thêm vai trò riêng) cho TISA BOT, cùng luật với core.js
function roster(K) {
  const T = K.team || {}, off = T.off || [], ed = T.edits || {}, rn = T.roomNames || {};
  const rooms = {}; (T.rooms || []).concat((T.roomsX || []).filter((r) => r && /^x-[\w-]{2,40}$/.test(r.id))).forEach((r) => { rooms[r.id] = rn[r.id] || r.name; });
  const base = (T.agents || []).map((a) => { const e = ed[a.id] || {}; const o = { ...a }; ['name', 'title', 'room'].forEach((k) => { if (e[k]) o[k] = String(e[k]); }); return o; });
  const custom = (T.custom || []).filter((a) => a && /^x-[\w-]{2,40}$/.test(a.id)).map((a) => ({ id: a.id, name: String(a.name || ''), title: String(a.title || ''), room: a.room, jobs: (a.jobs || []).map(String), custom: true, skill_path: String(a.skill || ''), to: String(a.to || '') }));
  return base.concat(custom).filter((a) => a.id && a.id !== 'chu' && (a.id === 'tam' || !off.includes(a.id)) && rooms[a.room])
    .map((a) => ({ ma: a.id, ten: a.name, chuc_danh: a.title || '', phong: rooms[a.room], viec: (a.jobs || []).slice(0, 8), skill_rieng: a.custom ? (a.skill_path || '') : (!a.skill ? '' : 'dq-' + a.skill), ban_giao_cho: a.to || '', tu_them: !!a.custom }));
}
function bizInfo(K) {
  const o = K.owner || {}, b = K.brand || {};
  return { ten: b.name || '', doi: b.team || '', khau_hieu: b.slogan || '', ho_so: K.business || '', luat: (K.rules || []).filter(Boolean),
    chu: { ten: o.name || '', goi_la: o.call || 'anh', nhan: o.label || ('Sếp ' + (o.name || '')).trim() },
    bo_nao: (K.brain || {}).abs || (K.brain || {}).path || '', thu_muc_van_phong: (K.brain || {}).office || '' };
}
const BRAND_KEYS = ['name', 'short', 'team', 'slogan', 'logo', 'color', 'color2'];
async function kitScript(env, auth) {
  const kit = await kitDoc(env);
  let out = kit;
  if (!auth) {
    const b = kit.brand || {}; const brand = {};
    BRAND_KEYS.forEach((k) => { if (b[k] != null) brand[k] = b[k]; });
    out = { brand, owner: { call: (kit.owner || {}).call || 'anh' } };
  }
  const js = 'window.__KIT_SAVED=' + JSON.stringify(out).replace(/</g, '\\u003c').replace(/[\u2028\u2029]/g, '') + ';' + (auth ? 'window.__KIT_AUTH=true;' : '');
  return new Response(js, { headers: { 'content-type': 'application/javascript; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' } });
}
async function heartbeat(env) {
  const t = Math.floor(Date.now() / 1000);
  const r = await env.DB.prepare("SELECT v FROM meta WHERE k = 'javis_seen'").first();
  if (!r || t - Number(r.v) >= 60) await env.DB.prepare("INSERT INTO meta (k, v) VALUES ('javis_seen', ?1) ON CONFLICT(k) DO UPDATE SET v = excluded.v").bind(t).run();
}
async function status(env) {
  const r = await env.DB.prepare("SELECT v FROM meta WHERE k = 'javis_seen'").first();
  const seen = r ? Number(r.v) : 0;
  const kit = await kitDoc(env);
  return { javis: { online: !!seen && Date.now() / 1000 - seen < 180, seen: seen * 1000 },
    claude: { key: !!(await claudeKey(env)), env: !!env.ANTHROPIC_API_KEY }, engine: kit.engine || 'auto' };
}

/* ---------------- Claude trong trang: chuyển tiếp tới Claude API ---------------- */
const MODELS = new Set(['claude-fable-5-1', 'claude-opus-5-5', 'claude-sonnet-5-5', 'claude-haiku-5-5']);
const AI_URL = 'https://api.anthropic.com/v1/messages';
function aiCode(status, msg) {
  msg = String(msg || '').toLowerCase();
  if (status === 401 || status === 403) return 'bad_key';
  if (msg.includes('credit balance')) return 'no_credit';
  if (status === 404 || (status === 400 && msg.includes('model'))) return 'bad_model';
  if (status === 429) return 'rate_limited';
  if (status === 529 || msg.includes('overloaded')) return 'overloaded';
  return 'unavailable';
}
async function aiProxy(req, env) {
  const key = await claudeKey(env);
  if (!key) return json({ error: 'Chưa có khóa Claude', code: 'no_key' }, 400);
  const b = await req.json().catch(() => null);
  if (!b || !Array.isArray(b.messages) || !b.messages.length) return json({ error: 'Thiếu nội dung', code: 'bad_request' }, 400);
  const body = {
    model: MODELS.has(b.model) ? b.model : 'claude-sonnet-5-5',
    max_tokens: Math.min(Math.max(Number(b.max_tokens) || 8000, 256), 32000),
    messages: b.messages.slice(-40),
    stream: b.stream !== false,
  };
  if (typeof b.system === 'string' && b.system) body.system = b.system.slice(0, 60000);
  const r = await fetch(AI_URL, { method: 'POST', body: JSON.stringify(body),
    headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' } });
  if (!r.ok) {
    const j = await r.json().catch(() => ({}));
    const m = (j.error && j.error.message) || ('Lỗi ' + r.status);
    return json({ error: m.slice(0, 300), code: aiCode(r.status, m) }, r.status === 401 ? 400 : r.status >= 500 ? 502 : r.status);
  }
  return new Response(r.body, { headers: { 'content-type': r.headers.get('content-type') || 'text/event-stream', 'cache-control': 'no-store' } });
}
async function setClaudeKey(req, env) {
  if (req.method === 'DELETE') { await secretSet(env, 'anthropic', ''); return json({ ok: true }); }
  const b = await req.json().catch(() => ({}));
  const k = String(b.key || '').trim();
  if (!/^sk-ant-[\w-]{20,}$/.test(k)) return json({ error: 'Khóa không đúng dạng (bắt đầu bằng sk-ant-).', code: 'bad_key' }, 400);
  const t = await fetch('https://api.anthropic.com/v1/models?limit=1', { headers: { 'x-api-key': k, 'anthropic-version': '2023-06-01' } });
  if (t.status === 401 || t.status === 403) return json({ error: 'Claude từ chối khóa này. Kiểm tra lại khóa.', code: 'bad_key' }, 400);
  await secretSet(env, 'anthropic', k);
  return json({ ok: true });
}
async function changePassword(req, env) {
  const b = await req.json().catch(() => ({}));
  const u0 = String(b.u0 || '').trim().toLowerCase(), u = String(b.u || u0).trim().toLowerCase();
  const old = String(b.old || ''), p = String(b.p || '');
  if (!same(await sha256(SALT + u0 + ':' + old), await boardHash(env))) { await new Promise((r) => setTimeout(r, 700)); return json({ error: 'Tên đăng nhập hoặc mật khẩu hiện tại chưa đúng.' }, 400); }
  if (!/^[a-z0-9._@-]{3,40}$/.test(u)) return json({ error: 'Tên đăng nhập 3 đến 40 ký tự, chỉ gồm chữ không dấu, số, dấu chấm, gạch.' }, 400);
  if (p.length < 8) return json({ error: 'Mật khẩu mới cần ít nhất 8 ký tự.' }, 400);
  await secretSet(env, 'board_hash', await sha256(SALT + u + ':' + p));
  const next = String(Number(await sessionEpoch(env)) + 1);
  await secretSet(env, 'session_epoch', next);
  epochCache = { v: next, t: Date.now() };
  // mọi phiên cũ (máy khác, trình duyệt khác) hết hiệu lực; phiên đang đổi mật khẩu được cấp lại
  return json({ ok: true }, 200, { 'set-cookie': await sessionCookie(env) });
}
async function exportAll(env) {
  const r = await env.DB.prepare('SELECT col, id, data FROM docs ORDER BY col, id').all();
  const out = { exported: now(), collections: {} };
  r.results.forEach((x) => { (out.collections[x.col] = out.collections[x.col] || []).push({ id: x.id, ...JSON.parse(x.data) }); });
  const name = 'doi-quan-ai-' + now().slice(0, 10) + '.json';
  return new Response(JSON.stringify(out, null, 1), { headers: { 'content-type': 'application/json; charset=utf-8', 'content-disposition': 'attachment; filename="' + name + '"', 'cache-control': 'no-store' } });
}

/* ---------------- Việc của TISA BOT ---------------- */
const TASK_STATE = { sua: 'dang', run: 'dang', recv: 'dang', that: 'dang', wait: 'cho', owner: 'cho', given: 'xong', duyet: 'duyet', done: 'xong', skip: 'xong', err: 'cho' };
async function syncTasks(env, jobId, job) {
  const plan = Array.isArray(job.plan) ? job.plan : [];
  for (const p of plan) {
    if (!p || !p.n) continue;
    const id = jobId + '-p' + p.n;
    const status = TASK_STATE[p.state] || 'cho';
    await mutate(env, 'tasks', id, (t) => {
      const base = t || { created: now(), priority: 'tb', createdBy: 'tam', due: job.date || now().slice(0, 10) };
      const n = { ...base, title: p.viec || base.title || 'Phần ' + p.n, assignee: p.agent || base.assignee || 'tam', status, jobId,
        input: 'Việc giao Tâm: ' + String(job.task || '').slice(0, 200), output: String(p.out || '').slice(0, 1200) };
      if (t && t.status === n.status && t.title === n.title && t.output === n.output) return undefined;
      n.updated = now();
      return n;
    });
  }
}
const sendKey = (r) => r.status + '|' + (r.updated || r.created || '');
function needsSend(r) {
  if (!r || r.demo) return false;
  if (r.status !== 'hang-doi' && r.status !== 'can-sua' && r.status !== 'da-duyet') return false;
  return (r.javis || {}).sentKey !== sendKey(r);
}

async function apiV1(req, env, path, url) {
  // /api/v1/queue, /api/v1/ack/:id, /api/v1/job/:id[/plan|/part|/link|/patch|/done]
  // Tin nhắn chủ doanh nghiệp gửi cho từng nhân sự trong khung trao đổi của việc
  if (path === '/api/v1/tin/hang-doi' && req.method === 'GET') {
    if (url.searchParams.get('javis') !== '0') await heartbeat(env);
    const since = url.searchParams.get('since');
    const vm = await env.DB.prepare("SELECT v FROM meta WHERE k = 'ver:messages'").first();
    const ver = vm ? Number(vm.v) : 0;
    if (since !== null && Number(since) === ver) return json({ tin: [], ver });
    const all = await listCol(env, 'messages');
    const q = all.filter((m) => m.from === 'chu' && m.status === 'moi').sort((a, b) => String(a.created).localeCompare(String(b.created)));
    const out = [];
    const K = q.length ? mergeKit(await kitDoc(env)) : null, team = K ? roster(K) : [];
    for (const m of q) {
      const r = m.jobId ? await getDoc(env, 'results', m.jobId) : null;
      const job = r ? r.data : {};
      const part = (job.plan || []).find((p) => Number(p.n) === Number(m.part)) || null;
      const thread = all.filter((x) => !SYS_KINDS.has(x.kind) && (m.dm ? x.dm === m.dm : (!x.dm && x.jobId === m.jobId && Number(x.part || 0) === Number(m.part || 0)))).sort((a, b) => String(a.created).localeCompare(String(b.created))).slice(-12)
        .map((x) => ({ from: x.from, text: String(x.text || '').slice(0, 1500), created: x.created, anh: (x.images || []).length, tep: (x.files || []).length }));
      if (SYS_KINDS.has(m.kind)) { out.push({ id: m.id, kind: m.kind, path: String(m.path || ''), file: String(m.file || ''), data: m.data || null, created: m.created }); continue; }
      out.push({ id: m.id, jobId: m.jobId, part: m.part || 0, dm: m.dm || '', model: m.model || '', effort: m.effort || '' /* CHAT-NOI-BO-2 */, to: m.to, kind: m.kind || 'hoi', text: m.text, created: m.created,
        images: (m.images || []).map((i) => ({ id: i.id, name: i.name, type: i.type })),
        files: (m.files || []).map((f) => ({ id: f.id, name: f.name, type: f.type, size: f.size, kind: f.kind })),
        job: { title: job.title || '', task: job.task || '', folder: job.folder || '', status: job.status || '' },
        phan: part ? { n: part.n, agent: part.agent, viec: part.viec, state: part.state, out: String(part.out || '').slice(0, 3000) } : null, thread,
        nguoi: team.find((a) => a.ma === m.to) || null, chu: K ? bizInfo(K).chu : null });
    }
    return json({ tin: out, ver });
  }
  let tm = path.match(/^\/api\/v1\/tin\/([\w-]+)\/ack$/);
  if (tm && req.method === 'POST') {
    const d = await mutate(env, 'messages', tm[1], (m) => (m ? { ...m, status: 'dang-xu-ly', sentAt: now() } : undefined));
    return d ? json({ ok: true }) : err(404, 'không có tin này');
  }
  if (path === '/api/v1/tin/tra-loi' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const orig = b.replyTo ? await getDoc(env, 'messages', String(b.replyTo)) : null;
    if (!orig) return err(404, 'không có tin gốc');
    const o = orig.data, id = rid('t');
    await putDoc(env, 'messages', id, { jobId: o.jobId, part: o.part || 0, dm: o.dm || '' /* CHAT-NOI-BO */, from: String(b.from || o.to || 'tam').slice(0, 20), to: 'chu',
      text: String(b.text || '').slice(0, 8000), kind: 'tra-loi', replyTo: b.replyTo, status: 'tra-loi', created: now(),
      claudePrompt: b.claudePrompt ? String(b.claudePrompt).slice(0, 12000) : '' });
    if (b.done !== false) await mutate(env, 'messages', String(b.replyTo), (m) => (m ? { ...m, status: 'da-tra-loi', answeredAt: now() } : undefined));
    return json({ ok: true, id });
  }
  if (path === '/api/v1/queue' && req.method === 'GET') {
    if (url.searchParams.get('javis') !== '0') await heartbeat(env);
    const since = url.searchParams.get('since');
    const vr = await env.DB.prepare("SELECT v FROM meta WHERE k = 'ver:results'").first();
    const ver = vr ? Number(vr.v) : 0;
    if (since !== null && Number(since) === ver) return json({ jobs: [], ver });
    const all = await listCol(env, 'results');
    const q = all.filter(needsSend).sort((a, b) => String(a.created).localeCompare(String(b.created)));
    return json({ jobs: q.map((r) => ({ id: r.id, title: r.title, task: r.task, status: r.status, date: r.date, time: r.time, folder: r.folder,
      note: r.note || '', plan: r.plan || [], settings: r.settings || null, updated: r.updated, approvedNow: r.approvedNow || [],
      files: (r.files || []).map((f) => ({ id: f.id, name: f.name, type: f.type, size: f.size, kind: f.kind })),
      kind: r.kind || '', skillFor: r.skillFor || '', skillWish: r.skillWish || '', github: !!r.github,
      roomWish: r.roomWish || '', roomN: r.roomN || '', ktLinks: r.ktLinks || [], ktFocus: r.ktFocus || '', tuLuc: r.tuLuc || '' })), ver });
  }
  let m = path.match(/^\/api\/v1\/ack\/([\w-]+)$/);
  if (m && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const d = await mutate(env, 'results', m[1], (r) => {
      if (!r) return undefined;
      const j = { ...(r.javis || {}), sentKey: sendKey(r), sentStatus: r.status, sentAt: Date.now(), state: b.state || 'da-gui', note: String(b.note || '').slice(0, 300) };
      // Báo ngay trên bảng là TISA BOT đã nhận, để chủ không phải chờ trong im lặng.
      const vn = new Date(Date.now() + 7 * 3600e3).toISOString().slice(11, 16);
      const sua = r.status === 'can-sua', duyet = r.status === 'da-duyet';
      return { ...r, javis: j, status: 'dang-chay',
        summary: sua ? 'TISA BOT đã nhận góp ý lúc ' + vn + ', đang sửa.'
          : duyet ? 'TISA BOT đã nhận phần anh duyệt lúc ' + vn + ', đang làm bước tiếp theo.'
          : (r.summary || 'TISA BOT đã nhận lúc ' + vn + '. Tâm đang đọc bộ não và chia việc.') };
    });
    return d ? json({ ok: true }) : err(404, 'không có việc này');
  }
  if (path === '/api/v1/kit' && req.method === 'GET') { const K = mergeKit(await kitDoc(env)); return json({ doanh_nghiep: bizInfo(K), doi: roster(K) }); }
  m = path.match(/^\/api\/v1\/job\/([\w-]+)(?:\/(plan|part|link|patch|done))?$/);
  if (!m) return err(404, 'không có đường này');
  const id = m[1], op = m[2] || '';
  if (!op && req.method === 'GET') {
    const d = await getDoc(env, 'results', id); if (!d) return err(404, 'không có việc này');
    const inputs = (await listCol(env, 'inputs')).filter((x) => x.jobId === id);
    const K = mergeKit(await kitDoc(env));
    return json({ id, ...d.data, inputs, doanh_nghiep: bizInfo(K), doi: roster(K) });
  }
  if (req.method !== 'POST') return err(405, 'sai phương thức');
  const b = await req.json().catch(() => null);
  if (!b || typeof b !== 'object') return err(400, 'thân yêu cầu phải là JSON');
  const t = now();
  const doc = await mutate(env, 'results', id, (r) => {
    if (!r) return undefined;
    const n = { ...r, updated: t };
    if (op === 'plan') {
      n.plan = (Array.isArray(b.plan) ? b.plan : []).slice(0, 12).map((p, i) => ({ agent: 'tam', state: 'wait', pct: 0, out: '', duyet: false, deps: [], ...p, n: Number(p.n) || i + 1 }));
      if (b.summary !== undefined) n.summary = String(b.summary).slice(0, 600);
      n.status = b.status || 'dang-chay';
    } else if (op === 'part') {
      const k = Number(b.n); if (!k) return undefined;
      const plan = Array.isArray(n.plan) ? n.plan.map((x) => ({ ...x })) : [];
      let p = plan.find((x) => Number(x.n) === k);
      if (!p) { p = { n: k, agent: b.agent || 'tam', viec: b.viec || '', state: 'wait', pct: 0, out: '', deps: [], duyet: false }; plan.push(p); plan.sort((a, c) => a.n - c.n); }
      ['agent', 'viec', 'mo_ta', 'dau_ra', 'state', 'duyet', 'deps', 'note'].forEach((f) => { if (b[f] !== undefined) p[f] = b[f]; });
      if (b.pct !== undefined) p.pct = Math.max(0, Math.min(100, Number(b.pct) || 0));
      if (b.out !== undefined) p.out = String(b.out).slice(0, 12000);
      if (b.claudePrompt !== undefined) p.claudePrompt = String(b.claudePrompt).slice(0, 8000);
      if (b.append) p.out = (String(p.out || '') + '\n' + String(b.append)).trim().slice(-12000);
      if (p.state === 'done' || p.state === 'duyet') p.pct = 100;
      n.plan = plan;
      if (n.status === 'hang-doi' || n.status === 'can-sua') n.status = 'dang-chay';
    } else if (op === 'link') {
      const L = { title: String(b.title || 'Kết quả').slice(0, 160), url: String(b.url || ''), kind: String(b.kind || 'file') };
      if (b.file) L.file = String(b.file).slice(0, 300);
      if (!/^(https:\/\/|\/_blob\/)/.test(L.url)) return undefined;
      n.links = (Array.isArray(n.links) ? n.links : []).filter((x) => x.url !== L.url).concat([L]).slice(-40);
    } else if (op === 'patch') {
      const allow = ['title', 'summary', 'insights', 'status', 'folder', 'note', 'synced', 'syncedAt', 'brain', 'realPass', 'links'];
      allow.forEach((f) => { if (b[f] !== undefined) n[f] = b[f]; });
    } else if (op === 'done') {
      n.status = b.status || 'cho-duyet';
      if (b.summary !== undefined) n.summary = String(b.summary).slice(0, 800);
      if (Array.isArray(b.insights)) n.insights = b.insights.slice(0, 6);
      n.realPass = 'xong'; n.finished = t;
    }
    return n;
  });
  if (!doc) return err(404, 'không có việc này hoặc dữ liệu không hợp lệ');
  if (op === 'plan' || op === 'part' || op === 'done') await syncTasks(env, id, doc);
  return json({ ok: true, id, status: doc.status, plan: (doc.plan || []).map((p) => ({ n: p.n, agent: p.agent, state: p.state, pct: p.pct })) });
}

/* ---------------- Ảnh, tệp ----------------
   Tệp nhỏ: một lần gửi. Tệp lớn (video): trình duyệt chia từng khúc tối đa 20MB, gửi lần lượt
   ?id=..&part=i&parts=n; khúc cuối ghi phiếu tổng (b:id) để tải về nối lại đúng thứ tự. */
const MAX_FILE = 200 * 1024 * 1024;
async function putBlob(req, env, url) {
  const len = Number(req.headers.get('content-length') || 0);
  if (len > MAX_BLOB) return err(413, 'tệp quá lớn (mỗi lần gửi tối đa 24MB)');
  const buf = await req.arrayBuffer();
  if (!buf.byteLength) return err(400, 'tệp rỗng');
  if (buf.byteLength > MAX_BLOB) return err(413, 'tệp quá lớn (mỗi lần gửi tối đa 24MB)');
  const type = (url.searchParams.get('type') || req.headers.get('content-type') || 'application/octet-stream').split(';')[0].slice(0, 100);
  const name = (url.searchParams.get('name') || 'tep').slice(0, 300);
  const id = (url.searchParams.get('id') || '').replace(/[^\w-]/g, '').slice(0, 64) || hex(crypto.getRandomValues(new Uint8Array(16)));
  const parts = Math.max(1, Math.min(20, Number(url.searchParams.get('parts') || 1) | 0));
  if (parts > 1) {
    const part = Number(url.searchParams.get('part') || 0) | 0;
    if (part < 0 || part >= parts) return err(400, 'khúc tệp không hợp lệ');
    const total = Number(url.searchParams.get('size') || 0);
    if (!total || total > MAX_FILE) return err(413, 'tệp quá lớn (tối đa 200MB)');
    await env.BLOBS.put('b:' + id + ':' + part, buf);
    if (part < parts - 1) return json({ ok: true, id, part, parts });
    await env.BLOBS.put('b:' + id, '1', { metadata: { type, name, size: total, parts } });
    await env.DB.prepare('INSERT OR REPLACE INTO blobs (id, type, name, size, created) VALUES (?1, ?2, ?3, ?4, ?5)').bind(id, type, name, total, now()).run();
    return json({ id, url: '/_blob/' + id, type, contentType: type, size: total, name });
  }
  await env.BLOBS.put('b:' + id, buf, { metadata: { type, name, size: buf.byteLength } });
  await env.DB.prepare('INSERT OR REPLACE INTO blobs (id, type, name, size, created) VALUES (?1, ?2, ?3, ?4, ?5)').bind(id, type, name, buf.byteLength, now()).run();
  return json({ id, url: '/_blob/' + id, type, contentType: type, size: buf.byteLength, name });
}
async function getBlob(env, id) {
  const r = await env.BLOBS.getWithMetadata('b:' + id, { type: 'stream' });
  if (!r || !r.value) return new Response('Không tìm thấy', { status: 404 });
  const m = r.metadata || {};
  let body = r.value;
  if (m.parts > 1) {
    try { await r.value.cancel(); } catch (e) {}
    const n = m.parts;
    const { readable, writable } = typeof FixedLengthStream === 'function' && m.size ? new FixedLengthStream(m.size) : new TransformStream();
    (async () => {
      try {
        for (let i = 0; i < n; i++) {
          const c = await env.BLOBS.get('b:' + id + ':' + i, { type: 'stream' });
          if (!c) throw new Error('thiếu khúc');
          await c.pipeTo(writable, { preventClose: true });
        }
        await writable.close();
      } catch (e) { try { await writable.abort(e); } catch (x) {} }
    })();
    body = readable;
  }
  const safeInline = /^(image\/(png|jpeg|webp|gif|avif)|video\/|audio\/|application\/pdf|text\/plain)/.test(m.type || '');
  const h = {
    'content-type': safeInline ? m.type : 'application/octet-stream',
    'content-disposition': (safeInline ? 'inline' : 'attachment') + "; filename*=UTF-8''" + encodeURIComponent(String(m.name || id).split('/').pop()),
    'cache-control': 'private, max-age=31536000, immutable', 'x-content-type-options': 'nosniff',
  };
  return new Response(body, { headers: h });
}

/* ---------------- Cổng chính ---------------- */
const PAGE_HEADERS = {
  'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-cache', 'x-content-type-options': 'nosniff',
  'referrer-policy': 'same-origin', 'x-frame-options': 'DENY', 'permissions-policy': 'camera=(), geolocation=(), microphone=(self)',
};

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;
    try {
      if (path === '/' || path === '/index.html') return new Response(BOARD, { headers: PAGE_HEADERS });
      if (path === '/health') return json({ ok: true });
      if (path === '/favicon.ico' || path === '/favicon.png') return new Response(Uint8Array.from(atob(FAVICON_B64), (c) => c.charCodeAt(0)), { headers: { 'content-type': 'image/png', 'cache-control': 'public, max-age=86400' } });
      if (path === '/kit.js') return kitScript(env, bearerOk(req, env) || (await sessionOk(req, env)));

      if (path === '/api/login' && req.method === 'POST') {
        const ip = req.headers.get('cf-connecting-ip') || 'x';
        const fk = 'fail:' + ip + ':' + Math.floor(Date.now() / 600000);
        const fr = await env.DB.prepare('SELECT v FROM meta WHERE k = ?1').bind(fk).first();
        if (fr && fr.v >= 15) return err(429, 'Sai quá nhiều lần. Thử lại sau 10 phút.');
        const b = await req.json().catch(() => ({}));
        const h = await sha256(SALT + String(b.u || '').trim().toLowerCase() + ':' + String(b.p || ''));
        if (!same(h, await boardHash(env))) {
          await env.DB.prepare('INSERT INTO meta (k, v) VALUES (?1, 1) ON CONFLICT(k) DO UPDATE SET v = v + 1').bind(fk).run();
          await new Promise((r) => setTimeout(r, 700)); return err(401, 'Sai tên đăng nhập hoặc mật khẩu.'); }
        return json({ ok: true }, 200, { 'set-cookie': await sessionCookie(env) });
      }
      if (path === '/api/logout') return json({ ok: true }, 200, { 'set-cookie': 'dq_s=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0' });

      const isBearer = bearerOk(req, env);
      const isUser = isBearer || (await sessionOk(req, env));
      if (!isUser) return path.startsWith('/_blob/') ? new Response('Cần đăng nhập', { status: 401 }) : err(401, 'Cần đăng nhập');
      // chặn gửi chéo trang: trình duyệt chỉ được ghi từ chính trang này
      if (!isBearer && req.method !== 'GET') {
        const o = req.headers.get('origin');
        if (o && o !== url.origin) return err(403, 'Nguồn không hợp lệ');
      }

      if (path === '/api/me') return json({ ok: true, via: isBearer ? 'token' : 'phien' });
      if (path === '/api/status') return json(await status(env));
      if (path === '/api/ai' && req.method === 'POST') return aiProxy(req, env);
      if (path === '/api/ai-key' && (req.method === 'POST' || req.method === 'DELETE')) return setClaudeKey(req, env);
      if (path === '/api/password' && req.method === 'POST') { if (isBearer) return err(403, 'Đổi mật khẩu trên trang'); return changePassword(req, env); }
      if (path === '/api/export') return exportAll(env);
      if (path === '/api/ver') return json(await versions(env));
      if (path.startsWith('/_blob/')) return getBlob(env, path.slice(7).replace(/[^\w-]/g, ''));
      if (path === '/api/assets' && req.method === 'POST') return putBlob(req, env, url);
      if (path.startsWith('/api/v1/')) { if (!isBearer) return err(403, 'Chỉ TISA BOT dùng đường này'); return apiV1(req, env, path, url); }

      const m = path.match(/^\/api\/db\/(\w+)(?:\/([\w.-]+))?$/);
      if (m) {
        const col = m[1], id = m[2];
        if (!COLS.has(col)) return err(404, 'không có bảng này');
        if (!id && req.method === 'GET') return json({ docs: await listCol(env, col), ver: (await versions(env)).cols[col] || 0 });
        if (!id && req.method === 'POST') {
          const b = await req.json(); const nid = rid('m');
          await putDoc(env, col, nid, b); return json({ id: nid });
        }
        if (id && req.method === 'GET') { const d = await getDoc(env, col, id); return d ? json({ id, ...d.data }) : err(404, 'không có'); }
        if (id && req.method === 'PUT') { const b = await req.json(); await putDoc(env, col, id, b); return json({ ok: true }); }
        if (id && req.method === 'PATCH') {
          const b = await req.json();
          const d = await mutate(env, col, id, (cur) => (cur ? { ...cur, ...b } : undefined));
          return d ? json({ ok: true }) : err(404, 'không có');
        }
        if (id && req.method === 'DELETE') {
          await bump(env, col);
          await env.DB.prepare('DELETE FROM docs WHERE col = ?1 AND id = ?2').bind(col, id).run();
          return json({ ok: true });
        }
      }
      return err(404, 'Không có trang này');
    } catch (e) {
      return err(500, 'Lỗi máy chủ: ' + String(e && e.message || e).slice(0, 200));
    }
  },
};
