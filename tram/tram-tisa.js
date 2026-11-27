// Trạm TISA: một Cloudflare Worker của chính chủ, dựng một lần, để nhiều máy chạy TISA BOT dùng chung một bộ não (bản thử 21/11/2026).
//
// Trạm KHÔNG chạy AI, không dựng video. Nó chỉ:
//   1. Làm CỔNG: tên miền chính trỏ vào Worker này; Worker chuyển người dùng, điện thoại, webhook sang máy đang giữ vai "cong" (máy chủ).
//      Đổi máy chủ chỉ là đổi một dòng trong D1, không đụng DNS.
//   2. Giữ SỔ MÁY: máy nào đã ghép, đang bật hay tắt, giữ vai nào (cong, khach, lich, bang, viec_nang), số nhiệm kỳ của từng vai.
//   3. Giữ KHO: tệp bộ não và gói cấu hình đã MÃ HÓA trên máy chủ nhân (Trạm không có mật khẩu, không đọc được), trong R2.
//
// Bindings: DB (D1), KHO (R2), QUAN_TRI (secret: khóa dựng Trạm, chỉ dùng để ghép máy đầu tiên).
// Mọi API nằm dưới /_tram/api/. Còn lại là cổng.

const PHIEN_BAN = "1";
const VAI = ["cong", "khach", "lich", "bang", "viec_nang"];
const MAY_TAT_SAU = 180;          // giây không có nhịp thì coi máy là tắt
const MA_GHEP_HAN = 15 * 60;      // mã ghép sống 15 phút
const TEP_TOI_DA = 95 * 1024 * 1024;
const BANG = [
  "CREATE TABLE IF NOT EXISTS may (id TEXT PRIMARY KEY, ten TEXT, he TEXT, ban TEXT, dia_chi TEXT, khoa_bam TEXT, tao INTEGER, lan_cuoi INTEGER, trang_thai TEXT)",
  "CREATE TABLE IF NOT EXISTS vai (ten TEXT PRIMARY KEY, may_id TEXT, nhiem_ky INTEGER, luc INTEGER)",
  "CREATE TABLE IF NOT EXISTS ghep (ma TEXT PRIMARY KEY, het INTEGER, tao_boi TEXT, da_dung INTEGER DEFAULT 0, goi TEXT)",
  "CREATE TABLE IF NOT EXISTS tep (duong_dan TEXT PRIMARY KEY, bam TEXT, kich_thuoc INTEGER, luc INTEGER, xoa INTEGER DEFAULT 0, seq INTEGER, boi TEXT)",
  "CREATE INDEX IF NOT EXISTS tep_seq ON tep(seq)",
  "CREATE TABLE IF NOT EXISTS chung (khoa TEXT PRIMARY KEY, gia_tri TEXT)",
  "CREATE TABLE IF NOT EXISTS nhat_ky (id INTEGER PRIMARY KEY AUTOINCREMENT, luc INTEGER, may_id TEXT, viec TEXT, chi_tiet TEXT)",
];

const now = () => Math.floor(Date.now() / 1000);
const json = (d, status = 200) => new Response(JSON.stringify(d), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const loi = (status, chu) => json({ ok: false, loi: chu }, status);

async function bam(chu) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(chu));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}

function ngauNhien(n, bang = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789") {
  const r = crypto.getRandomValues(new Uint8Array(n));
  return [...r].map((x) => bang[x % bang.length]).join("");
}

function bangNhau(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let k = 0;
  for (let i = 0; i < a.length; i++) k |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return k === 0;
}

// D1 thỉnh thoảng báo "D1_ERROR: internal error" khi nhiều máy/luồng cùng ghi (thấy khi đẩy 20.000 tệp đêm 21/11): thử lại vài lần.
async function d1(fn) {
  for (let i = 0; ; i++) {
    try {
      return await fn();
    } catch (e) {
      const m = String((e && e.message) || e);
      if (i >= 3 || !/D1_ERROR|internal error|overloaded|busy|reset|timed out/i.test(m)) throw e;
      await new Promise((r) => setTimeout(r, 150 * (i + 1) + Math.floor(Math.random() * 100)));
    }
  }
}

let daTaoBang = false;
async function chuanBi(env) {
  if (daTaoBang) return;
  await env.DB.batch(BANG.map((s) => env.DB.prepare(s)));
  daTaoBang = true;
}

async function ghiNhatKy(env, may_id, viec, chi_tiet) {
  await env.DB.prepare("INSERT INTO nhat_ky (luc, may_id, viec, chi_tiet) VALUES (?, ?, ?, ?)").bind(now(), may_id || "", viec, JSON.stringify(chi_tiet || {}).slice(0, 2000)).run();
  await env.DB.prepare("DELETE FROM nhat_ky WHERE id < (SELECT MAX(id) - 500 FROM nhat_ky)").run();
}

// Xác thực máy: Authorization: Bearer <may_id>.<khoa>
async function mayGoi(req, env) {
  const h = req.headers.get("authorization") || "";
  const m = /^Bearer ([A-Za-z0-9]{6,40})\.([A-Za-z0-9_-]{20,100})$/.exec(h);
  if (!m) return null;
  const r = await d1(() => env.DB.prepare("SELECT * FROM may WHERE id = ?").bind(m[1]).first());
  if (!r || r.trang_thai === "da_go") return null;
  return bangNhau(r.khoa_bam, await bam(m[2])) ? r : null;
}

async function bangVai(env) {
  const { results } = await env.DB.prepare("SELECT * FROM vai").all();
  const out = {};
  for (const v of results || []) out[v.ten] = { may_id: v.may_id, nhiem_ky: v.nhiem_ky, luc: v.luc };
  return out;
}

async function danhSachMay(env) {
  const { results } = await env.DB.prepare("SELECT id, ten, he, ban, dia_chi, tao, lan_cuoi, trang_thai FROM may WHERE trang_thai != 'da_go' ORDER BY tao").all();
  const t = now();
  return (results || []).map((m) => ({ ...m, dang_bat: t - (m.lan_cuoi || 0) < MAY_TAT_SAU }));
}

async function datVai(env, gan, boi) {
  // gan: {ten_vai: may_id|null}. Vai đổi chủ thì tăng nhiệm kỳ: máy giữ vai cũ thấy nhiệm kỳ mới hơn là tự buông.
  const cu = await bangVai(env);
  const lenh = [];
  for (const [ten, may_id] of Object.entries(gan)) {
    if (!VAI.includes(ten)) continue;
    if ((cu[ten] || {}).may_id === may_id) continue;
    const nk = ((cu[ten] || {}).nhiem_ky || 0) + 1;
    lenh.push(env.DB.prepare("INSERT INTO vai (ten, may_id, nhiem_ky, luc) VALUES (?, ?, ?, ?) ON CONFLICT(ten) DO UPDATE SET may_id = excluded.may_id, nhiem_ky = excluded.nhiem_ky, luc = excluded.luc").bind(ten, may_id, nk, now()));
  }
  if (lenh.length) {
    await env.DB.batch(lenh);
    await ghiNhatKy(env, boi, "dat_vai", gan);
  }
  return bangVai(env);
}

async function dangKyMay(env, body) {
  const id = ngauNhien(10, "abcdefghijkmnpqrstuvwxyz23456789");
  const khoa = ngauNhien(40, "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789");
  await env.DB.prepare("INSERT INTO may (id, ten, he, ban, dia_chi, khoa_bam, tao, lan_cuoi, trang_thai) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'hoat_dong')")
    .bind(id, String(body.ten || "Máy").slice(0, 60), String(body.he || "").slice(0, 20), String(body.ban || "").slice(0, 30), "", await bam(khoa), now(), now()).run();
  return { may_id: id, khoa };
}

function diaChiHopLe(u, env) {
  try {
    const x = new URL(u);
    if (env && env.THU_NOI_BO === "1" && /^http:\/\/127\.0\.0\.1:\d+$/.test(x.origin)) return x.origin;   // chỉ khi chạy thử cục bộ
    return x.protocol === "https:" && !/^(localhost|127\.|10\.|192\.168\.|169\.254\.)/.test(x.hostname) ? x.origin : "";
  } catch (_) { return ""; }
}

// ------------------------------------------------------------------ API
async function api(req, env, url) {
  await chuanBi(env);
  const p = url.pathname.slice("/_tram/api".length) || "/";
  const M = req.method;
  const doc = async () => { try { return await req.json(); } catch (_) { return {}; } };

  if (p === "/chao" && M === "GET") {
    const ds = await danhSachMay(env);
    const salt = await env.DB.prepare("SELECT gia_tri FROM chung WHERE khoa = 'muoi'").first();
    return json({ ok: true, tram: "tisa", phien_ban: PHIEN_BAN, da_co_may: ds.length > 0, co_kho: !!env.KHO, co_mat_khau: !!salt });
  }

  // Máy đầu tiên: dùng khóa dựng Trạm (QUAN_TRI). Sau đó máy mới chỉ vào được bằng mã ghép do một máy đã ghép tạo ra.
  if (p === "/khoi-tao" && M === "POST") {
    if (!env.QUAN_TRI || !bangNhau(req.headers.get("x-tram-quan-tri") || "", env.QUAN_TRI)) return loi(401, "Sai khóa dựng Trạm.");
    const body = await doc();
    const r = await dangKyMay(env, body);
    const v = await bangVai(env);
    if (!v.cong) await datVai(env, Object.fromEntries(VAI.map((k) => [k, r.may_id])), r.may_id);
    // muối và mẫu kiểm của mật khẩu bộ não (máy tự tạo, Trạm chỉ cất)
    if (body.muoi && body.mau_kiem) {
      await env.DB.batch([
        env.DB.prepare("INSERT OR IGNORE INTO chung (khoa, gia_tri) VALUES ('muoi', ?)").bind(String(body.muoi).slice(0, 200)),
        env.DB.prepare("INSERT OR IGNORE INTO chung (khoa, gia_tri) VALUES ('mau_kiem', ?)").bind(String(body.mau_kiem).slice(0, 400)),
      ]);
    }
    await ghiNhatKy(env, r.may_id, "khoi_tao", { ten: body.ten });
    return json({ ok: true, ...r, vai: await bangVai(env) });
  }

  // Máy mới dùng mã ghép (không cần khóa). Mã dùng một lần, hết hạn sau 15 phút.
  if (p === "/ghep" && M === "POST") {
    const body = await doc();
    const ma = String(body.ma || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
    const g = await env.DB.prepare("SELECT * FROM ghep WHERE ma = ?").bind(ma).first();
    if (!g || g.da_dung || g.het < now()) return loi(400, "Mã ghép sai, đã dùng hoặc đã hết hạn. Tạo mã mới ở máy chính.");
    const chung = {};
    const { results } = await env.DB.prepare("SELECT khoa, gia_tri FROM chung").all();
    for (const x of results || []) chung[x.khoa] = x.gia_tri;
    // Bước kiểm: máy mới lấy muối + mẫu kiểm để thử mật khẩu bộ não TRƯỚC khi dùng mã (gõ sai mật khẩu không làm cháy mã).
    if (body.chi_kiem) return json({ ok: true, muoi: chung.muoi || "", mau_kiem: chung.mau_kiem || "", con_giay: g.het - now() });
    const dung = await env.DB.prepare("UPDATE ghep SET da_dung = 1 WHERE ma = ? AND da_dung = 0").bind(ma).run();
    if (!dung.meta || dung.meta.changes !== 1) return loi(400, "Mã ghép vừa được dùng ở máy khác.");
    const r = await dangKyMay(env, body);
    await ghiNhatKy(env, r.may_id, "ghep", { ten: body.ten, boi: g.tao_boi });
    return json({ ok: true, ...r, muoi: chung.muoi || "", mau_kiem: chung.mau_kiem || "", goi: g.goi || "" });
  }

  const may = await mayGoi(req, env);
  if (!may) return loi(401, "Máy chưa ghép với Trạm hoặc khóa máy sai.");

  if (p === "/nhip" && M === "POST") {
    const body = await doc();
    const dc = diaChiHopLe(String(body.dia_chi || ""), env);
    await d1(() => env.DB.prepare("UPDATE may SET lan_cuoi = ?, dia_chi = COALESCE(NULLIF(?, ''), dia_chi), ban = ?, he = ?, ten = COALESCE(NULLIF(?, ''), ten) WHERE id = ?")
      .bind(now(), dc, String(body.ban || "").slice(0, 30), String(body.he || "").slice(0, 20), String(body.ten || "").slice(0, 60), may.id).run());
    const seq = await env.DB.prepare("SELECT COALESCE(MAX(seq), 0) AS s FROM tep").first();
    return json({ ok: true, may_id: may.id, vai: await bangVai(env), may: await danhSachMay(env), seq_tep: seq.s, gio: now() });
  }

  if (p === "/tinh-trang" && M === "GET") {
    const { results } = await env.DB.prepare("SELECT luc, may_id, viec, chi_tiet FROM nhat_ky ORDER BY id DESC LIMIT 30").all();
    const t = await env.DB.prepare("SELECT COUNT(*) AS n, COALESCE(SUM(kich_thuoc), 0) AS kt FROM tep WHERE xoa = 0").first();
    return json({ ok: true, may_id: may.id, vai: await bangVai(env), may: await danhSachMay(env), nhat_ky: results || [], tep: t, co_kho: !!env.KHO });
  }

  if (p === "/dat-vai" && M === "POST") {
    const body = await doc();
    const ds = await danhSachMay(env);
    const co = new Set(ds.map((m) => m.id));
    const gan = {};
    for (const [k, v] of Object.entries(body.gan || {})) if (VAI.includes(k) && (v === null || co.has(v))) gan[k] = v;
    if ("cong" in gan && !gan.cong) return loi(400, "Phải có một máy chủ (vai cổng).");
    return json({ ok: true, vai: await datVai(env, gan, may.id) });
  }

  if (p === "/ma-ghep" && M === "POST") {
    const body = await doc();
    const ma = ngauNhien(8);
    await env.DB.prepare("DELETE FROM ghep WHERE het < ?").bind(now() - 86400).run();
    await env.DB.prepare("INSERT INTO ghep (ma, het, tao_boi, da_dung, goi) VALUES (?, ?, ?, 0, ?)").bind(ma, now() + MA_GHEP_HAN, may.id, String(body.goi || "").slice(0, 80)).run();
    await ghiNhatKy(env, may.id, "tao_ma_ghep", {});
    return json({ ok: true, ma, het: now() + MA_GHEP_HAN });
  }

  if (p === "/go-may" && M === "POST") {
    const body = await doc();
    const v = await bangVai(env);
    if (Object.values(v).some((x) => x.may_id === body.may_id && x === v.cong)) return loi(400, "Không gỡ được máy đang là máy chủ. Chuyển máy chủ sang máy khác trước.");
    await env.DB.prepare("UPDATE may SET trang_thai = 'da_go', khoa_bam = '' WHERE id = ?").bind(String(body.may_id || "")).run();
    const gan = {};
    for (const [k, x] of Object.entries(v)) if (x.may_id === body.may_id) gan[k] = null;
    if (Object.keys(gan).length) await datVai(env, gan, may.id);
    await ghiNhatKy(env, may.id, "go_may", { may_id: body.may_id });
    return json({ ok: true });
  }

  // ---- tệp bộ não (đã mã hóa ở máy). Khóa trong R2 theo dấu nội dung, nên tệp giống nhau chỉ lưu một lần.
  if (!env.KHO) return loi(501, "Trạm chưa gắn kho R2.");

  if (p === "/tep" && M === "GET") {
    const sau = parseInt(url.searchParams.get("sau") || "0", 10) || 0;
    const { results } = await env.DB.prepare("SELECT duong_dan, bam, kich_thuoc, luc, xoa, seq, boi FROM tep WHERE seq > ? ORDER BY seq LIMIT 1000").bind(sau).all();
    return json({ ok: true, tep: results || [] });
  }

  if (p === "/tep" && M === "PUT") {
    const dd = url.searchParams.get("duong_dan") || "";
    const b = url.searchParams.get("bam") || "";
    const goc = url.searchParams.get("goc") || "";
    if (!dd || dd.length > 900 || !/^[0-9a-f]{32,64}$/.test(b)) return loi(400, "Thiếu đường dẫn hoặc dấu tệp.");
    const cu = await d1(() => env.DB.prepare("SELECT bam, xoa FROM tep WHERE duong_dan = ?").bind(dd).first());
    const bamCu = cu && !cu.xoa ? cu.bam : "";
    if (bamCu === b) return json({ ok: true, giong: true });
    if (bamCu !== goc) return json({ ok: false, xung_dot: true, bam_tram: bamCu }, 409);
    const len = parseInt(req.headers.get("content-length") || "0", 10);
    if (len > TEP_TOI_DA) return loi(413, "Tệp quá lớn để đồng bộ.");
    const khoa = "noi-dung/" + b;
    if (!(await env.KHO.head(khoa))) await env.KHO.put(khoa, req.body);
    await d1(() => env.DB.prepare("INSERT INTO tep (duong_dan, bam, kich_thuoc, luc, xoa, seq, boi) VALUES (?1, ?2, ?3, ?4, 0, (SELECT COALESCE(MAX(seq), 0) + 1 FROM tep), ?5) ON CONFLICT(duong_dan) DO UPDATE SET bam = ?2, kich_thuoc = ?3, luc = ?4, xoa = 0, seq = (SELECT COALESCE(MAX(seq), 0) + 1 FROM tep), boi = ?5")
      .bind(dd, b, len, now(), may.id).run());
    return json({ ok: true });
  }

  if (p === "/tep/xoa" && M === "POST") {
    const body = await doc();
    const cu = await env.DB.prepare("SELECT bam, xoa FROM tep WHERE duong_dan = ?").bind(String(body.duong_dan || "")).first();
    if (!cu || cu.xoa) return json({ ok: true });
    if (cu.bam !== body.goc) return json({ ok: false, xung_dot: true, bam_tram: cu.bam }, 409);
    await env.DB.prepare("UPDATE tep SET xoa = 1, luc = ?, seq = (SELECT COALESCE(MAX(seq), 0) + 1 FROM tep), boi = ? WHERE duong_dan = ?").bind(now(), may.id, body.duong_dan).run();
    return json({ ok: true });
  }

  if (p.startsWith("/noi-dung/") && M === "GET") {
    const b = p.slice("/noi-dung/".length);
    if (!/^[0-9a-f]{32,64}$/.test(b)) return loi(400, "Dấu tệp sai.");
    const o = await env.KHO.get("noi-dung/" + b);
    if (!o) return loi(404, "Không còn nội dung này.");
    return new Response(o.body, { headers: { "content-type": "application/octet-stream" } });
  }

  // ---- gói nhân bản máy phụ (gói Chuyển máy đã mã hóa), tải lên từng phần vì Worker nhận tối đa 100 MB mỗi lần
  if (p === "/goi/bat-dau" && M === "POST") {
    const ten = "goi/" + ngauNhien(12, "abcdefghijkmnpqrstuvwxyz23456789") + ".tisapack";
    const up = await env.KHO.createMultipartUpload(ten);
    return json({ ok: true, ten, upload_id: up.uploadId });
  }
  if (p === "/goi/phan" && M === "PUT") {
    const ten = url.searchParams.get("ten") || "";
    const so = parseInt(url.searchParams.get("so") || "0", 10);
    if (!/^goi\/[a-z0-9]{12}\.tisapack$/.test(ten) || !(so >= 1 && so <= 10000)) return loi(400, "Phần gói sai.");
    const up = env.KHO.resumeMultipartUpload(ten, url.searchParams.get("upload_id") || "");
    const part = await up.uploadPart(so, req.body);
    return json({ ok: true, part });
  }
  if (p === "/goi/xong" && M === "POST") {
    const body = await doc();
    if (!/^goi\/[a-z0-9]{12}\.tisapack$/.test(body.ten || "")) return loi(400, "Tên gói sai.");
    const up = env.KHO.resumeMultipartUpload(body.ten, body.upload_id || "");
    await up.complete(body.parts || []);
    await ghiNhatKy(env, may.id, "tai_goi", { ten: body.ten });
    return json({ ok: true, ten: body.ten });
  }
  if (p === "/goi" && M === "GET") {
    const ten = url.searchParams.get("ten") || "";
    if (!/^goi\/[a-z0-9]{12}\.tisapack$/.test(ten)) return loi(400, "Tên gói sai.");
    const range = req.headers.get("range");
    let o;
    if (range) {
      const m = /^bytes=(\d+)-$/.exec(range);
      o = await env.KHO.get(ten, m ? { range: { offset: parseInt(m[1], 10) } } : undefined);
    } else o = await env.KHO.get(ten);
    if (!o) return loi(404, "Gói đã bị xóa hoặc chưa tải xong.");
    const h = { "content-type": "application/octet-stream", "x-tong": String(o.size) };
    return new Response(o.body, { status: range ? 206 : 200, headers: h });
  }
  if (p === "/goi/xoa" && M === "POST") {
    const body = await doc();
    if (/^goi\/[a-z0-9]{12}\.tisapack$/.test(body.ten || "")) await env.KHO.delete(body.ten);
    return json({ ok: true });
  }

  return loi(404, "Không có đường này.");
}

// ------------------------------------------------------------------ cổng
const MAY_COOKIE = "tram_may";

function layCookie(req, ten) {
  const m = new RegExp("(?:^|;\\s*)" + ten + "=([^;]+)").exec(req.headers.get("cookie") || "");
  return m ? decodeURIComponent(m[1]) : "";
}

function trangBaoTri(ds, chu) {
  const dong = ds.map((m) => `<li><b>${esc(m.ten)}</b> (${esc(m.he || "?")}) ${m.dang_bat ? "đang bật" : "đang tắt"}${m.dang_bat && m.id !== chu ? ` <a href="/_tram/chon/${m.id}">mở máy này</a>` : ""}</li>`).join("");
  return new Response(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TISA BOT</title>
<body style="font-family:system-ui;max-width:560px;margin:40px auto;padding:0 16px;color:#1B2A4A">
<h2>Máy chủ TISA BOT đang tắt</h2><p>Trạm vẫn chạy nhưng máy đang làm chủ không trả lời. Bật lại máy chủ, hoặc mở một máy phụ rồi vào Cài đặt, Nhiều máy, bấm <b>Tiếp quản</b>.</p>
<ul>${dong || "<li>Chưa có máy nào ghép với Trạm.</li>"}</ul></body>`, { status: 503, headers: { "content-type": "text/html; charset=utf-8", "retry-after": "60" } });
}

function esc(s) { return String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

async function cong(req, env, url) {
  await chuanBi(env);
  if (url.pathname.startsWith("/_tram/chon/")) {
    const id = url.pathname.slice("/_tram/chon/".length).replace(/[^a-z0-9]/g, "");
    const h = new Headers({ location: "/" });
    h.append("set-cookie", id && id !== "chu" ? `${MAY_COOKIE}=${id}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=43200` : `${MAY_COOKIE}=; Path=/; Max-Age=0`);
    return new Response(null, { status: 302, headers: h });
  }
  const ds = await danhSachMay(env);
  const v = await bangVai(env);
  const chuId = (v.cong || {}).may_id;
  const chon = layCookie(req, MAY_COOKIE);
  let dich = ds.find((m) => m.id === (chon || chuId));
  const xemMayKhac = !!(chon && chon !== chuId && dich);
  if (!dich || !dich.dang_bat || !dich.dia_chi) {
    if (chon) dich = ds.find((m) => m.id === chuId);
    if (!dich || !dich.dang_bat || !dich.dia_chi) return trangBaoTri(ds, chuId);
  }
  const goc = new URL(dich.dia_chi);
  const dichUrl = new URL(url.pathname + url.search, goc);
  const h = new Headers(req.headers);
  const mo = url.origin;
  if (h.get("origin") === mo) h.set("origin", goc.origin);           // cùng nguồn qua cổng = cùng nguồn ở máy
  const ref = h.get("referer");
  if (ref && ref.startsWith(mo)) h.set("referer", goc.origin + ref.slice(mo.length));
  h.set("x-forwarded-host", url.host);
  h.set("x-tram-tisa", "1");
  h.delete("cf-connecting-ip");
  const init = { method: req.method, headers: h, redirect: "manual" };
  if (!["GET", "HEAD"].includes(req.method)) init.body = req.body;
  let res;
  try {
    res = await fetch(dichUrl.toString(), init);
  } catch (e) {
    return trangBaoTri(ds, chuId);
  }
  if (res.status === 101) return res;                                    // WebSocket đi thẳng
  if (res.status >= 520 && res.status <= 530) return trangBaoTri(ds, chuId);
  const out = new Headers(res.headers);
  const loc = out.get("location");
  if (loc && loc.startsWith(goc.origin)) out.set("location", mo + loc.slice(goc.origin.length));
  let r = new Response(res.body, { status: res.status, statusText: res.statusText, headers: out });
  // Không chèn thanh "Đang xem máy ... · về máy chủ" nữa (22/11/2026): nhãn máy đã hiện ở thanh trên của giao diện.
  return r;
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    try {
      if (url.pathname.startsWith("/_tram/api/")) return await api(req, env, url);
      return await cong(req, env, url);
    } catch (e) {
      return loi(500, "Trạm gặp lỗi: " + String((e && e.message) || e).slice(0, 200));
    }
  },
};
