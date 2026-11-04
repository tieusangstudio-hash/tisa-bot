// board-server.mjs - chạy Bảng giao việc Đội Quân AI ngay trên máy, không cần tài khoản Cloudflare.
// Giữ nguyên mã bảng (worker.mjs, chính là bản chạy trên Cloudflare), chỉ thay ba thứ nền tảng:
//   env.DB    = SQLite trong tệp (node:sqlite, Node 22.13 trở lên), dùng cùng cách gọi với D1
//   env.BLOBS = thư mục tệp trên máy, dùng cùng cách gọi với KV
//   public/   = tệp tĩnh (giọng đọc)
// Chỉ nghe trên 127.0.0.1. Mở từ chính máy này thì tự đăng nhập; đi qua đường hầm thì phải đăng nhập.
import http from 'node:http';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Readable } from 'node:stream';
import { fileURLToPath } from 'node:url';
import { DatabaseSync } from 'node:sqlite';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = process.env.DOI_QUAN_HOME || path.join(os.homedir(), '.doi-quan-ai');
const CFG = process.env.DOI_QUAN_ENV || path.join(os.homedir(), '.config', 'doi-quan-ai', '.env');
const PORT = Number(process.env.TISA_BOARD_PORT || 7788);
const BLOB_DIR = path.join(DATA, 'board-blobs');
fs.mkdirSync(BLOB_DIR, { recursive: true });
fs.mkdirSync(path.dirname(CFG), { recursive: true, mode: 0o700 });

/* ---- Mã ghi bảng: sinh một lần, cầu nối và MCP đọc cùng tệp ---- */
function envGet(k) {
  try {
    const m = fs.readFileSync(CFG, 'utf8').match(new RegExp('^' + k + '=(.*)$', 'm'));
    return m ? m[1].trim() : '';
  } catch { return ''; }
}
function envSet(k, v) {
  let s = '';
  try { s = fs.readFileSync(CFG, 'utf8'); } catch { /* chưa có tệp */ }
  s = s.split('\n').filter((l) => l && !l.startsWith(k + '=')).concat(k + '=' + v).join('\n') + '\n';
  fs.writeFileSync(CFG, s, { mode: 0o600 });
}
let TOKEN = envGet('BOARD_TOKEN');
if (!TOKEN) { TOKEN = crypto.randomBytes(32).toString('hex'); envSet('BOARD_TOKEN', TOKEN); }

/* ---- env.DB: cùng cách gọi với Cloudflare D1 ---- */
const sql = new DatabaseSync(path.join(DATA, 'board.sqlite'));
sql.exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;');
sql.exec(fs.readFileSync(path.join(HERE, 'schema.sql'), 'utf8'));
const clean = (a) => a.map((v) => (v === undefined ? null : typeof v === 'boolean' ? (v ? 1 : 0) : v));
class Stmt {
  constructor(text, args = []) { this.text = text; this.args = args; }
  bind(...a) { return new Stmt(this.text, clean(a)); }
  _all() { return sql.prepare(this.text).all(...this.args).map((r) => ({ ...r })); }
  async all() { return { results: this._all(), success: true, meta: {} }; }
  async run() {
    const results = this._all();
    const changes = sql.prepare('SELECT changes() AS c').get().c;
    return { results, success: true, meta: { changes } };
  }
  async first(col) { const r = this._all()[0]; return r ? (col ? r[col] : r) : null; }
}
const DB = {
  prepare: (text) => new Stmt(text),
  async batch(list) {
    sql.exec('BEGIN');
    try {
      const out = [];
      for (const s of list) out.push(await s.run());
      sql.exec('COMMIT');
      return out;
    } catch (e) { sql.exec('ROLLBACK'); throw e; }
  },
};

/* ---- env.BLOBS: cùng cách gọi với Cloudflare KV ---- */
const blobPath = (k) => path.join(BLOB_DIR, Buffer.from(k).toString('base64url'));
const metaPath = (k) => blobPath(k) + '.meta.json';
async function toBuffer(v) {
  if (typeof v === 'string') return Buffer.from(v);
  if (v instanceof ArrayBuffer) return Buffer.from(v);
  if (ArrayBuffer.isView(v)) return Buffer.from(v.buffer, v.byteOffset, v.byteLength);
  return Buffer.from(await new Response(v).arrayBuffer());
}
function readBlob(k, type) {
  const p = blobPath(k);
  if (!fs.existsSync(p)) return null;
  if (type === 'stream') return Readable.toWeb(fs.createReadStream(p));
  const b = fs.readFileSync(p);
  if (type === 'arrayBuffer') return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
  if (type === 'json') return JSON.parse(b.toString('utf8'));
  return b.toString('utf8');
}
const BLOBS = {
  async put(k, v, o = {}) {
    fs.writeFileSync(blobPath(k), await toBuffer(v));
    if (o.metadata) fs.writeFileSync(metaPath(k), JSON.stringify(o.metadata));
  },
  async get(k, o = {}) { return readBlob(k, typeof o === 'string' ? o : o.type); },
  async getWithMetadata(k, o = {}) {
    const value = readBlob(k, typeof o === 'string' ? o : o.type);
    let metadata = null;
    try { metadata = JSON.parse(fs.readFileSync(metaPath(k), 'utf8')); } catch { /* không có */ }
    return { value, metadata };
  },
  async delete(k) { fs.rmSync(blobPath(k), { force: true }); fs.rmSync(metaPath(k), { force: true }); },
};

/* ---- Đăng nhập ---- */
const worker = (await import('./worker.mjs')).default;
// Mật khẩu bảng khi mở từ xa (đường hầm): dùng chung tài khoản quản trị TISA BOT nếu có, đổi được trong Cài đặt của bảng.
const adminPass = process.env.JAVIS_ADMIN_PASSWORD || '';
const adminUser = String(process.env.JAVIS_ADMIN_USER || 'admin').trim().toLowerCase();
const BOARD_HASH = adminPass ? crypto.createHash('sha256').update('tisa-agent-hq|v1|' + adminUser + ':' + adminPass).digest('hex') : '';
const env = { DB, BLOBS, BOARD_API_TOKEN: TOKEN, BOARD_HASH };
const SESSION_DAYS = 30;
// Cùng công thức với worker.mjs (sessMsg, sessionCookie), kể cả "đời phiên" khi đổi mật khẩu.
function sessionSig(exp) {
  let epoch = '0';
  try { epoch = sql.prepare("SELECT v FROM secrets WHERE k = 'session_epoch'").get()?.v || '0'; } catch { /* chưa có bảng */ }
  const msg = epoch === '0' ? 'dq|' + exp : 'dq|' + exp + '|' + epoch;
  return crypto.createHmac('sha256', TOKEN).update(msg).digest('hex');
}
function sessionValue() {
  const exp = Date.now() + SESSION_DAYS * 864e5;
  return exp + '.' + sessionSig(exp);
}
// Phiên cũ có thể sai chữ ký sau khi cài lại hoặc đổi mật khẩu: coi như chưa có để không kẹt ở khung đăng nhập.
function sessionOk(cookieHeader) {
  const m = /(?:^|;\s*)dq_s=([^;]+)/.exec(cookieHeader || '');
  if (!m) return false;
  const [exp, sig] = decodeURIComponent(m[1]).split('.');
  return Boolean(sig) && Number(exp) > Date.now() && sig === sessionSig(exp);
}
// Máy chủ chỉ nghe trên 127.0.0.1, nên chỉ cần loại yêu cầu đi qua đường hầm/proxy và Host lạ (DNS rebinding).
function fromThisMachine(req) {
  const host = String(req.headers.host || '').replace(/:\d+$/, '');
  if (host !== '127.0.0.1' && host !== 'localhost') return false;
  return !['x-forwarded-for', 'cf-connecting-ip', 'x-real-ip', 'forwarded'].some((h) => req.headers[h]);
}

/* ---- Tệp tĩnh ---- */
const MIME = { '.mp3': 'audio/mpeg', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' };
const PUBLIC = path.join(HERE, 'public');
function staticFile(urlPath) {
  let rel;
  try { rel = decodeURIComponent(urlPath); } catch { return null; }
  const p = path.join(PUBLIC, path.normalize(rel));
  if (!p.startsWith(PUBLIC + path.sep)) return null;
  try { return fs.statSync(p).isFile() ? p : null; } catch { return null; }
}

/* ---- Máy chủ ---- */
const server = http.createServer(async (nreq, nres) => {
  try {
    const url = new URL(nreq.url, 'http://' + (nreq.headers.host || '127.0.0.1'));
    if (nreq.method === 'GET' || nreq.method === 'HEAD') {
      const f = staticFile(url.pathname);
      if (f) {
        nres.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'cache-control': 'public, max-age=86400', 'content-length': fs.statSync(f).size });
        if (nreq.method === 'HEAD') return nres.end();
        return fs.createReadStream(f).pipe(nres);
      }
    }
    const headers = new Headers();
    for (const [k, v] of Object.entries(nreq.headers)) headers.set(k, Array.isArray(v) ? v.join(', ') : String(v));
    let autoLogin = '';
    if (!sessionOk(headers.get('cookie')) && !headers.get('authorization') && url.pathname !== '/api/logout' && fromThisMachine(nreq)) {
      autoLogin = sessionValue();
      const c = (headers.get('cookie') || '').split(/;\s*/).filter((x) => x && !x.startsWith('dq_s=')).concat('dq_s=' + autoLogin);
      headers.set('cookie', c.join('; '));
    }
    const init = { method: nreq.method, headers };
    if (nreq.method !== 'GET' && nreq.method !== 'HEAD') { init.body = Readable.toWeb(nreq); init.duplex = 'half'; }
    const res = await worker.fetch(new Request(url, init), env);
    const out = {};
    res.headers.forEach((v, k) => { if (k !== 'set-cookie') out[k] = v; });
    // Trên máy đi bằng http: bỏ cờ Secure, nếu không Safari không giữ phiên đăng nhập.
    const cookies = res.headers.getSetCookie().map((c) => c.replace(/;\s*Secure/i, ''));
    if (autoLogin) cookies.push(`dq_s=${autoLogin}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`);
    if (cookies.length) out['set-cookie'] = cookies;
    // Trang chỉ hiện bảng khi đã nhớ "đã đăng nhập": trên chính máy này thì báo sẵn để vào thẳng, không hiện khung mật khẩu.
    if ((url.pathname === '/' || url.pathname === '/index.html') && res.status === 200 && fromThisMachine(nreq)) {
      const page = (await res.text()).replace('<head>', '<head><script>try{localStorage.setItem("vp-auth",JSON.stringify({exp:Date.now()+2592000000}))}catch(e){}</script>');
      delete out['content-length'];
      nres.writeHead(200, out);
      return nres.end(page);
    }
    nres.writeHead(res.status, out);
    if (!res.body || nreq.method === 'HEAD') return nres.end();
    Readable.fromWeb(res.body).pipe(nres);
  } catch (e) {
    console.error(e);
    if (!nres.headersSent) nres.writeHead(500, { 'content-type': 'application/json; charset=utf-8' });
    nres.end(JSON.stringify({ error: 'Lỗi máy chủ bảng: ' + String(e?.message || e).slice(0, 200) }));
  }
});
server.listen(PORT, '127.0.0.1', () => console.log('Bảng giao việc chạy ở http://127.0.0.1:' + PORT));
for (const s of ['SIGTERM', 'SIGINT']) process.on(s, () => { server.close(); sql.close(); process.exit(0); });
