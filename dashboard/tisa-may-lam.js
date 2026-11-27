/* Nhiều máy (bản thử, chủ yêu cầu 21/11/2026):
 *  1. Nhãn MÁY NÀY ở thanh trên cùng: tên máy + Máy chủ/Máy phụ, nhìn là biết trang đang chạy trên máy nào.
 *  2. Nút "Máy làm" cạnh dấu + của ô chat: chọn máy nào làm việc vừa gõ (Hỏi nhanh hoặc một cộng sự như Dũng Edit).
 *     Chọn máy khác thì việc gửi sang máy đó (server/tisa_giao_may.py), kết quả hiện ngay trong khung chat này.
 *     Lựa chọn nhớ theo từng cuộc trò chuyện và từng cộng sự.
 * Chỉ hiện khi máy đã nối Nhiều máy. Tắt Nhiều máy là trang như cũ. */
(function () {
  "use strict";
  var W = window, D = document;
  if (W.__tisaMayLam) return;
  W.__tisaMayLam = 1;

  var ST = { d: null, luc: 0, dang: false };
  var THE = {};            // id việc -> bản ghi (đã giao từ máy này)
  var DA_TAI = {};         // phiên -> đã lấy danh sách việc của phiên đó chưa
  var TAM = "";            // phiên tạm khi giao việc lúc khung chat còn trống (chưa có mã phiên)
  var PH_GOC = null;       // chữ gợi ý gốc của ô chat
  var LS_CHON = "tisa.mayLam.chon", LS_BIDANH = "tisa.mayLam.biDanh";

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function docLS(k) { try { return JSON.parse(localStorage.getItem(k) || "{}") || {}; } catch (e) { return {}; } }
  function ghiLS(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function api(u, body) {
    var o = body ? { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body), credentials: "same-origin" }
      : { credentials: "same-origin", cache: "no-store" };
    return fetch(u, o).then(function (r) { return r.json().catch(function () { return { ok: false, loi: "Máy chủ trả lỗi " + r.status }; }); })
      .catch(function () { return { ok: false, loi: "Mất kết nối tới TISA BOT" }; });
  }
  function luc(t) {
    var s = Math.max(0, Date.now() / 1000 - (t || 0));
    return s < 60 ? "vừa xong" : s < 3600 ? Math.floor(s / 60) + " phút trước" : s < 86400 ? Math.floor(s / 3600) + " giờ trước" : Math.floor(s / 86400) + " ngày trước";
  }

  var IC_MAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>';
  var IC_GIAO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7h11l-3-3M17 17H6l3 3"/></svg>';

  var CSS = [
    // Nhãn máy (21/11 chủ nhờ làm gọn, đẹp hơn): cùng khuôn với nút chọn bộ não bên cạnh (cao 30, bo 8, nền --bg3), chấm màu vai + tên + chip vai nhỏ.
    ".tml-nhan{display:inline-flex;align-items:center;gap:7px;margin-left:8px;height:30px;padding:0 5px 0 10px;border-radius:8px;border:1px solid var(--border,rgba(23,47,114,.12));background:var(--bg3,#f4f6fb);color:var(--text,#172033);font:inherit;font-size:13px;text-decoration:none;white-space:nowrap;max-width:280px;min-width:0;flex:0 1 auto;cursor:pointer;transition:border-color .15s}",
    ".tml-nhan:hover{border-color:var(--accent,#F26A21)}.tml-nhan:focus-visible{outline:2px solid var(--accent,#F26A21);outline-offset:2px}",
    ".tml-nhan .tml-cham{width:7px;height:7px;border-radius:50%;flex:none;background:#94a3b8}",
    ".tml-nhan b{font-weight:600;overflow:hidden;text-overflow:ellipsis;min-width:0;max-width:170px}",
    ".tml-nhan .tml-vai{flex:none;font-size:11px;font-weight:650;line-height:1;padding:5px 7px;border-radius:6px;letter-spacing:.1px}",
    ".tml-nhan.chu .tml-cham{background:#F26A21;box-shadow:0 0 0 3px rgba(242,106,33,.18)}.tml-nhan.chu .tml-vai{background:rgba(242,106,33,.12);color:#c2410c}",
    ".tml-nhan.phu .tml-cham{background:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,.18)}.tml-nhan.phu .tml-vai{background:rgba(59,130,246,.11);color:#1d4ed8}",
    "@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .tml-nhan.chu .tml-vai{color:#fdba74}:root:not([data-theme=light]) .tml-nhan.phu .tml-vai{color:#93c5fd}}",
    ":root[data-theme=dark] .tml-nhan.chu .tml-vai{color:#fdba74}:root[data-theme=dark] .tml-nhan.phu .tml-vai{color:#93c5fd}",
    "@media (max-width:760px){.tml-nhan{margin-left:6px;padding:0 4px 0 8px;gap:6px}.tml-nhan b{max-width:96px}.tml-nhan .tml-vai{padding:4px 5px;font-size:10.5px}}",
    "@media (max-width:420px){.tml-nhan b{display:none}.tml-nhan{padding:0 4px 0 8px}}",
    // Không dùng lớp cp-plus: tisa-trinh-duyet.js chèn nút Trình duyệt sau MỌI nút cp-plus (thấy 21/11: hai nút Trình duyệt).
    // 22/11/2026 (chủ): cùng khuôn với hai nút kế bên (.mb-chip model, .cp-eff mức suy nghĩ): chữ 12px đậm 600, đệm 4px 11px, bo tròn, cùng cao; màu XANH ĐẬM nổi bật.
    // (Khai báo cũ `font:600 12.5px/1 inherit` không hợp lệ nên bị bỏ: nút rơi về chữ mặc định và cao 32px, lệch hai nút kia.)
    // Cam dành riêng cho trạng thái ĐANG GIAO máy khác (.xa), vàng cho máy đích đang tắt (.tat).
    ".tml-pill{display:inline-flex;align-items:center;gap:6px;flex:0 1 auto;min-width:0;max-width:220px;padding:4px 11px;border-radius:999px;white-space:nowrap;cursor:pointer;font-family:var(--font,inherit);font-size:12px;font-weight:600;line-height:normal;color:#fff;border:1px solid #1d4ed8;background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 2px 8px rgba(37,99,235,.35);transition:filter .15s,box-shadow .15s,transform .15s}",
    ".tml-pill:hover{filter:brightness(1.08);box-shadow:0 3px 12px rgba(37,99,235,.5)}.tml-pill:active{transform:translateY(1px)}.tml-pill:focus-visible{outline:2px solid #F26A21;outline-offset:2px}",
    ".tml-pill svg{width:14px;height:14px;flex:none}.tml-pill span{overflow:hidden;text-overflow:ellipsis;min-width:0}.tml-pill .tml-car{font-size:10px;opacity:.75;flex:none}",
    ".tml-pill.xa{background:linear-gradient(135deg,#ff8a50,#F26A21)!important;color:#fff!important;border-color:#e2530f!important;box-shadow:0 2px 8px rgba(242,106,33,.4)!important}",
    ".tml-pill.tat{background:#fef3c7!important;color:#92400e!important;border-color:#f59e0b!important;box-shadow:none!important}",
    ".tml-pill.gon span,.tml-pill.gon .tml-car{display:none}.tml-pill.gon{padding:0 9px}",
    "@media (max-width:640px){.tml-pill span{max-width:84px}.tml-pill{padding:0 9px}}",
    "#hudVoice.tml-xa{box-shadow:0 0 0 2px rgba(242,106,33,.55)!important}",
    ".tml-menu{position:fixed;z-index:2147483000;width:340px;max-width:calc(100vw - 24px);background:var(--surface,#fff);color:var(--text,#172033);border:1px solid var(--border,rgba(23,47,114,.15));border-radius:16px;box-shadow:0 18px 50px rgba(15,23,42,.22);padding:8px;font-size:14px}",
    ".tml-menu h4{margin:6px 8px 8px;font-size:13px;font-weight:700;color:var(--text2,#475569)}",
    ".tml-mo{display:flex;align-items:center;gap:10px;width:100%;text-align:left;border:0;background:none;color:inherit;padding:9px 10px;border-radius:11px;cursor:pointer;font:inherit}",
    ".tml-mo:hover:not([disabled]),.tml-mo:focus-visible{background:var(--surface-2,rgba(23,47,114,.06));outline:none}.tml-mo[disabled]{opacity:.5;cursor:not-allowed}",
    ".tml-mo i{width:9px;height:9px;border-radius:50%;background:#94a3b8;flex:none}.tml-mo i.on{background:#22c55e}",
    ".tml-mo .tml-t{flex:1;min-width:0}.tml-mo .tml-t b{display:block;font-weight:650;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
    ".tml-mo .tml-t small{display:block;color:var(--text3,#64748b);font-size:12px;margin-top:2px}.tml-mo .tml-ok{color:#F26A21;font-weight:800;flex:none}",
    ".tml-mo.chon{background:rgba(242,106,33,.08)}",
    ".tml-ghi{margin:6px 8px 4px;padding-top:8px;border-top:1px solid var(--border,rgba(23,47,114,.12));color:var(--text3,#64748b);font-size:12.5px;line-height:1.45}",
    ".tml-gan{margin:4px 0 0}.tml-gan .tml-mo small{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
    ".tml-via{display:inline-flex;align-items:center;gap:5px}.tml-via svg{width:13px;height:13px}",
    ".tml-kq .bubble{border-left:3px solid #F26A21}",
    ".tml-dau{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:13px;font-weight:650;margin-bottom:6px;color:var(--text2,#475569)}",
    ".tml-dau svg{width:15px;height:15px}.tml-dau .tml-tag{padding:3px 8px;border-radius:999px;font-size:11.5px;font-weight:700}",
    ".tml-dau .dang{background:rgba(242,106,33,.12);color:#c2410c}.tml-dau .xong{background:rgba(34,197,94,.14);color:#15803d}.tml-dau .loi{background:rgba(220,38,38,.12);color:#b91c1c}",
    ".tml-quay{display:inline-block;width:11px;height:11px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:tmlQuay .8s linear infinite;vertical-align:-1px}@keyframes tmlQuay{to{transform:rotate(360deg)}}",
    ".tml-tiendo{color:var(--text3,#64748b);font-size:13.5px}.tml-chan{margin-top:10px;padding-top:8px;border-top:1px dashed var(--border,rgba(23,47,114,.15));font-size:12.5px;color:var(--text3,#64748b)}",
    ".tml-chan a{color:#F26A21;font-weight:650}.tml-tep code{font-size:12px}",
    ".tml-toast{position:fixed;left:50%;bottom:110px;transform:translateX(-50%);z-index:2147483001;background:#1f2937;color:#fff;padding:10px 16px;border-radius:12px;font-size:13.5px;max-width:min(520px,calc(100vw - 32px));box-shadow:0 10px 30px rgba(0,0,0,.25)}"
  ].join("");
  function css() {
    if (D.getElementById("tml-css")) return;
    var st = D.createElement("style"); st.id = "tml-css"; st.textContent = CSS; (D.head || D.documentElement).appendChild(st);
  }
  var _toastT = 0;
  function toast(chu) {
    var t = D.getElementById("tmlToast");
    if (!t) { t = D.createElement("div"); t.id = "tmlToast"; t.className = "tml-toast"; t.setAttribute("role", "status"); D.body.appendChild(t); }
    t.textContent = chu; t.hidden = false; clearTimeout(_toastT); _toastT = setTimeout(function () { t.hidden = true; }, 5200);
  }

  // ---------------------------------------------------------------- dữ liệu máy
  function tai(ep) {
    if (ST.dang || (!ep && Date.now() - ST.luc < 25000)) return Promise.resolve(ST.d);
    ST.dang = true;
    return api("/tisa-nhieu-may/api/may-lam").then(function (d) {
      ST.dang = false; ST.luc = Date.now();
      if (d && d.ok) ST.d = d;
      ve();
      return ST.d;
    });
  }
  function bat() { return !!(ST.d && ST.d.bat && (ST.d.may || []).length); }
  function mayNay() { return (ST.d && ST.d.may_nay) || {}; }
  function timMay(id) { return ((ST.d && ST.d.may) || []).filter(function (m) { return m.id === id; })[0] || null; }

  // ---------------------------------------------------------------- 1. nhãn máy ở thanh trên cùng
  function veNhan() {
    var host = D.querySelector(".hud-top-left");
    var el = D.getElementById("tmlNhan");
    if (!bat() || !host) { if (el) el.remove(); return; }
    if (!el) {
      el = D.createElement("a"); el.id = "tmlNhan"; el.href = "/tisa-nhieu-may/";
      el.addEventListener("click", function (e) {
        if (W.TISADoiQuan && W.TISADoiQuan.moTrang) { e.preventDefault(); W.TISADoiQuan.moTrang("/tisa-nhieu-may/", "dq-nhieu-may"); }
      });
      host.appendChild(el);
    }
    var m = mayNay(), chu = !!m.la_chu;
    var h = "<span class='tml-cham' aria-hidden='true'></span><b>" + esc(m.ten || "Máy này") + "</b><span class='tml-vai'>" + (chu ? "Máy chủ" : "Máy phụ") + "</span>";
    if (el.getAttribute("data-k") !== h) { el.innerHTML = h; el.setAttribute("data-k", h); }
    el.className = "tml-nhan " + (chu ? "chu" : "phu");
    el.title = "Trang này đang chạy trên máy \"" + (m.ten || "") + "\"" + (m.may_that && m.may_that !== m.ten ? " (" + m.may_that + ")" : "") +
      ", là " + (chu ? "máy chủ: tên miền trỏ về đây" : "máy phụ") + ". AI làm việc trên máy này, trừ khi anh chọn máy khác ở nút Máy làm trong ô chat. Bấm để mở trang Nhiều máy.";
    el.setAttribute("aria-label", "Máy này: " + (m.ten || "") + ", " + (chu ? "máy chủ" : "máy phụ"));
  }

  // ---------------------------------------------------------------- ngữ cảnh ô chat
  function oChat() { return D.getElementById("chatInput"); }
  function boiCanh() {
    var ws = W.TISAWorkspace, S = null, inp = oChat();
    try { S = ws && ws.state && ws.state(); } catch (e) {}
    if (S && S.el && D.body.contains(S.el) && inp && S.el.contains(inp)) {
      if (S.loai === "agent") {
        var slug = S.chon && S.chon.agent, a = (S.agents || []).filter(function (x) { return x.slug === slug; })[0] || {};
        return slug ? { loai: "agent", slug: slug, ten: a.name || slug } : { loai: "chat" };
      }
      return { loai: "workflow" };
    }
    return { loai: "chat" };
  }
  function phienApp() { try { return (W.TISASessions && W.TISASessions.current()) || ""; } catch (e) { return ""; } }
  function phienGui() { var p = phienApp(); if (!p) return TAM || (TAM = "moi" + Date.now().toString(36)); return docLS(LS_BIDANH)[p] || p; }
  function cacPhienHien() {
    var p = phienApp(), ds = [];
    if (p) { ds.push(p); var b = docLS(LS_BIDANH)[p]; if (b) ds.push(b); } else if (TAM) ds.push(TAM);
    return ds;
  }
  function khoaChon() { var bc = boiCanh(); return bc.loai === "agent" ? "a:" + bc.slug : "chat"; }
  function mayChon() {
    var c = docLS(LS_CHON), p = phienApp();
    var id = (p && c["p:" + p]) || c[khoaChon()] || "";
    if (!id || id === mayNay().id || !timMay(id)) return null;
    return timMay(id);
  }
  function datChon(id) {
    var c = docLS(LS_CHON), p = phienApp(), v = id === mayNay().id ? "" : id;
    c[khoaChon()] = v;
    if (p) c["p:" + p] = v;
    var ks = Object.keys(c); if (ks.length > 300) ks.slice(0, ks.length - 300).forEach(function (k) { delete c[k]; });
    ghiLS(LS_CHON, c);
    ve();
  }

  // ---------------------------------------------------------------- 2. nút "Máy làm" ở ô chat
  function vePill() {
    var plus = D.getElementById("plusBtn"), b = D.getElementById("tmlPill"), inp = oChat(), hud = D.getElementById("hudVoice");
    var co = bat() && (ST.d.may || []).length > 1 && plus && plus.parentNode;
    if (!co) {
      if (b) b.remove();
      if (hud) hud.classList.remove("tml-xa");
      if (inp && PH_GOC !== null && inp.getAttribute("data-tml-ph") === "1") { inp.placeholder = PH_GOC; inp.removeAttribute("data-tml-ph"); }
      return;
    }
    if (!b) {
      b = D.createElement("button"); b.type = "button"; b.id = "tmlPill"; b.className = "tml-pill";
      b.setAttribute("aria-haspopup", "menu");
      b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); moMenu(b); });
    }
    var sau = plus.nextSibling && plus.nextSibling.classList && plus.nextSibling.classList.contains("tbd-pill") ? plus.nextSibling : plus;
    if (b.previousSibling !== sau || b.parentNode !== plus.parentNode) plus.parentNode.insertBefore(b, sau.nextSibling);
    var m = mayChon(), bc = boiCanh();
    var xa = !!m && bc.loai !== "workflow", tat = xa && !m.dang_bat;
    var h = (xa ? IC_GIAO : IC_MAY) + "<span>" + esc(xa ? "Máy làm: " + m.ten : "Máy này làm") + "</span><b class='tml-car'>▾</b>";
    if (b.getAttribute("data-k") !== h) { b.innerHTML = h; b.setAttribute("data-k", h); }
    b.classList.toggle("xa", xa && !tat); b.classList.toggle("tat", tat);
    try { var rong = b.parentNode.clientWidth; b.classList.toggle("gon", rong > 0 && rong < 520 && !xa); } catch (e) {}
    b.title = xa ? "Việc gõ ở đây sẽ gửi cho máy \"" + m.ten + "\" làm" + (tat ? " (máy đang tắt)" : "") + ". Bấm để đổi máy."
      : "Máy này (" + (mayNay().ten || "") + ") làm việc. Bấm để chọn máy khác làm.";
    b.setAttribute("aria-label", b.title);
    if (hud) hud.classList.toggle("tml-xa", xa);
    if (inp) {
      if (PH_GOC === null) PH_GOC = inp.placeholder;
      if (xa) { var ph = "Việc này sẽ gửi cho máy " + m.ten + " làm..."; if (inp.placeholder !== ph) { inp.placeholder = ph; inp.setAttribute("data-tml-ph", "1"); } }
      else if (inp.getAttribute("data-tml-ph") === "1") { inp.placeholder = PH_GOC; inp.removeAttribute("data-tml-ph"); }
    }
  }

  var MENU = null;
  function dongMenu() { if (MENU) { MENU.remove(); MENU = null; } }
  function moMenu(nut) {
    if (MENU) { dongMenu(); return; }
    tai(true);
    var bc = boiCanh(), chon = mayChon(), nay = mayNay();
    var m = D.createElement("div"); m.className = "tml-menu"; m.setAttribute("role", "menu");
    var h = "<h4>" + (bc.loai === "agent" ? "Máy nào làm việc của " + esc(bc.ten) + "?" : "Máy nào làm việc này?") + "</h4>";
    (ST.d.may || []).forEach(function (x) {
      var la = x.la_may_nay ? !chon : !!(chon && chon.id === x.id);
      var khoa = !x.la_may_nay && (!x.dang_bat || bc.loai === "workflow");
      var phu = [x.la_may_nay ? "máy này" : "", x.la_chu ? "Máy chủ" : "Máy phụ", x.viec_nang ? "giữ việc nặng" : "", x.dang_bat ? "đang bật" : "đang tắt"].filter(Boolean).join(" · ");
      h += "<button type='button' role='menuitemradio' aria-checked='" + la + "' class='tml-mo" + (la ? " chon" : "") + "' data-may='" + esc(x.id) + "'" + (khoa ? " disabled" : "") + ">" +
        "<i class='" + (x.dang_bat ? "on" : "") + "'></i><span class='tml-t'><b>" + esc(x.ten) + "</b><small>" + esc(phu) + "</small></span>" + (la ? "<span class='tml-ok'>✓</span>" : "") + "</button>";
    });
    h += "<div class='tml-ghi'>" + (bc.loai === "workflow" ? "Quy trình chỉ chạy trên máy này." :
      "Chọn máy khác: việc anh gõ sẽ gửi sang máy đó làm, dùng chuột, phần mềm và tệp của máy đó. Kết quả hiện ngay trong khung chat này. Máy " + esc(nay.ten || "") + " vẫn dùng bình thường.") + "</div>";
    var gan = Object.keys(THE).map(function (k) { return THE[k]; }).sort(function (a, b) { return (b.luc || 0) - (a.luc || 0); }).slice(0, 4);
    if (gan.length) {
      h += "<div class='tml-ghi'><b>Việc đã giao gần đây</b></div><div class='tml-gan'>" + gan.map(function (r) {
        var tt = r.trang_thai === "xong" ? "✓ xong" : r.trang_thai === "loi" ? "lỗi" : "đang làm";
        return "<button type='button' class='tml-mo' data-xem='" + esc(r.id) + "'><span class='tml-t'><b>" + esc(r.loi_nhan) + "</b><small>" +
          esc((r.ten_cong_su ? r.ten_cong_su + " · " : "") + r.ten_may + " · " + tt + " · " + luc(r.luc)) + "</small></span></button>";
      }).join("") + "</div>";
    }
    m.innerHTML = h;
    D.body.appendChild(m); MENU = m;
    var r = nut.getBoundingClientRect(), mw = m.offsetWidth, mh = m.offsetHeight;
    m.style.left = Math.max(12, Math.min(r.left, innerWidth - mw - 12)) + "px";
    m.style.top = (r.top - mh - 8 > 8 ? r.top - mh - 8 : Math.min(r.bottom + 8, innerHeight - mh - 8)) + "px";
    m.addEventListener("click", function (e) {
      var o = e.target.closest("[data-may]");
      if (o && !o.disabled) { datChon(o.getAttribute("data-may")); dongMenu(); var inp = oChat(); if (inp) inp.focus(); return; }
      var x = e.target.closest("[data-xem]");
      if (x) { dongMenu(); xemLai(x.getAttribute("data-xem")); }
    });
    var dau = m.querySelector(".tml-mo.chon") || m.querySelector(".tml-mo:not([disabled])");
    if (dau) dau.focus();
  }
  D.addEventListener("mousedown", function (e) { if (MENU && !MENU.contains(e.target) && !(e.target.closest && e.target.closest("#tmlPill"))) dongMenu(); }, true);
  D.addEventListener("keydown", function (e) { if (MENU && e.key === "Escape") { dongMenu(); var b = D.getElementById("tmlPill"); if (b) b.focus(); } });

  // ---------------------------------------------------------------- gửi việc sang máy khác
  function guiXa() {
    var m = mayChon(), bc = boiCanh(), inp = oChat();
    if (!m || !inp || bc.loai === "workflow") return false;
    var msg = (inp.value || "").trim();
    if (!msg || msg.charAt(0) === "/") return false;               // lệnh "/" là tính năng của trang này: chạy trên máy này
    if (!m.dang_bat) { toast("Máy " + m.ten + " đang tắt. Bật máy đó lên, hoặc bấm nút Máy làm để chọn máy khác."); return true; }
    var dinh = [];
    try { dinh = (W.TISAAttach && W.TISAAttach.list && W.TISAAttach.list()) || []; } catch (e) {}
    if (dinh.length) { toast("Tệp đính kèm chỉ có trên máy này nên chưa gửi sang máy " + m.ten + " được. Bỏ tệp, hoặc chọn Máy này làm."); return true; }
    var phien = phienGui();
    inp.value = ""; inp.style.height = "auto";
    try { inp.dispatchEvent(new Event("input", { bubbles: true })); } catch (e) {}
    var tam = { id: "tam" + Date.now(), may_id: m.id, ten_may: m.ten, agent: bc.slug || "", ten_cong_su: bc.ten || "", loi_nhan: msg, phien: phien,
      luc: Date.now() / 1000, trang_thai: "dang_lam", tien_do: "Đang gửi sang máy " + m.ten + "..." };
    THE[tam.id] = tam; veThe(tam, true);
    var brain = ""; try { brain = W.TISASessions.brain() || ""; } catch (e) {}
    api("/tisa-nhieu-may/api/giao", { may_id: m.id, loi_nhan: msg, agent: bc.slug || "", brain: brain, phien: phien, ten_cong_su: bc.ten || "" }).then(function (d) {
      boThe(tam.id); delete THE[tam.id];
      if (!d || !d.ok) {
        tam.trang_thai = "loi"; tam.loi = (d && d.loi) || "Không gửi được"; tam.id = "loi" + Date.now(); THE[tam.id] = tam; veThe(tam, true);
        if (!inp.value) { inp.value = msg; try { inp.dispatchEvent(new Event("input", { bubbles: true })); } catch (e) {} }
        return;
      }
      THE[d.viec.id] = d.viec; veThe(d.viec, true); hoiTienDo();
    });
    return true;
  }
  function boc() {
    var goc = W.sendMessage;
    if (typeof goc !== "function") return false;
    if (goc.__tml) return true;
    var moi = function (text, opts) {
      if (!text && !opts) { try { if (guiXa()) return; } catch (e) { try { console.warn("[may-lam]", e); } catch (e2) {} } }
      return goc.apply(this, arguments);
    };
    moi.__tml = 1;
    W.sendMessage = moi;
    return true;
  }

  // ---------------------------------------------------------------- thẻ việc trong khung chat
  function khung() { return D.getElementById("chatArea"); }
  function boThe(id) { Array.prototype.forEach.call(D.querySelectorAll("[data-tml='" + id + "']"), function (e) { e.remove(); }); }
  function htmlKq(r) {
    var tt = r.trang_thai, ten = esc(r.ten_may || "máy kia");
    var tag = tt === "xong" ? "<span class='tml-tag xong'>✓ Máy " + ten + " đã làm xong</span>"
      : tt === "loi" ? "<span class='tml-tag loi'>Máy " + ten + " báo lỗi</span>"
      : "<span class='tml-tag dang'><span class='tml-quay'></span> Máy " + ten + " đang làm</span>";
    var h = "<div class='tml-dau'>" + IC_GIAO + tag + (r.ten_cong_su ? "<span>" + esc(r.ten_cong_su) + "</span>" : "") + "</div>";
    if (tt === "xong") {
      var md = r.tra_loi || "(Máy kia làm xong nhưng không gửi lời nào về.)";
      try { h += W.mdToHtml ? W.mdToHtml(md) : "<div style='white-space:pre-wrap'>" + esc(md) + "</div>"; } catch (e) { h += "<div style='white-space:pre-wrap'>" + esc(md) + "</div>"; }
      if ((r.tep || []).length) h += "<div class='tml-chan tml-tep'>Tệp nằm trên máy " + ten + ":<br>" + r.tep.map(function (t) { return "<code>" + esc(t) + "</code>"; }).join("<br>") + "</div>";
    } else if (tt === "loi") {
      h += "<div style='white-space:pre-wrap'>" + esc(r.loi || "Lỗi không rõ") + "</div>";
    } else {
      h += "<div class='tml-tiendo'>" + esc(r.tien_do || "Đang làm...") + "</div>";
    }
    var quaTram = !/^(127\.|localhost|\[::1\])/.test(location.hostname);
    if (String(r.id).indexOf("tam") !== 0 && String(r.id).indexOf("loi") !== 0) {
      h += "<div class='tml-chan'>Cuộc trò chuyện này lưu trên máy " + ten + (r.ten_cong_su ? " (cộng sự " + esc(r.ten_cong_su) + ")" : "") + ". " +
        (quaTram && r.may_id ? "<a href='/_tram/chon/" + encodeURIComponent(r.may_id) + "'>Mở máy " + ten + " để xem chi tiết</a>" : "Mở TISA BOT trên máy đó để xem chi tiết.") + "</div>";
    }
    return h;
  }
  function veThe(r, cuon) {
    var k = khung();
    if (!k) return;
    var tin = k.querySelector(".tml-tin[data-tml='" + r.id + "']"), kq = k.querySelector(".tml-kq[data-tml='" + r.id + "']");
    var gan = k.scrollHeight - k.scrollTop - k.clientHeight < 160;
    if (!tin) {
      tin = D.createElement("div"); tin.className = "msg msg-user tml-tin"; tin.setAttribute("data-tml", r.id);
      tin.innerHTML = "<div class='msg-via tml-via'>" + IC_GIAO + "Giao cho máy " + esc(r.ten_may) + (r.ten_cong_su ? " · " + esc(r.ten_cong_su) : "") + "</div><div class='bubble' style='white-space:pre-wrap'>" + esc(r.loi_nhan) + "</div>";
      k.appendChild(tin);
    }
    if (!kq) { kq = D.createElement("div"); kq.className = "msg msg-tisa tml-kq"; kq.setAttribute("data-tml", r.id); kq.innerHTML = "<div class='bubble'></div>"; k.appendChild(kq); }
    var h = htmlKq(r), bub = kq.querySelector(".bubble");
    if (bub.getAttribute("data-k") !== h) { bub.innerHTML = h; bub.setAttribute("data-k", h); }
    if (cuon || gan) k.scrollTop = k.scrollHeight;
  }
  function xemLai(id) {
    var r = THE[id];
    if (!r) return;
    var e = D.querySelector(".tml-kq[data-tml='" + id + "']");
    if (!e) { veThe(r, false); e = D.querySelector(".tml-kq[data-tml='" + id + "']"); }
    if (e) e.scrollIntoView({ block: "center", behavior: "smooth" });
  }
  // Khung chat dựng lại khi đổi cuộc trò chuyện: vẽ lại thẻ của đúng cuộc đang mở, theo thứ tự thời gian.
  function giuThe() {
    var k = khung();
    if (!k) return;
    var ds = cacPhienHien();
    Object.keys(THE).forEach(function (id) {
      var r = THE[id], thuoc = ds.indexOf(r.phien) >= 0;
      var co = k.querySelector(".tml-kq[data-tml='" + id + "']");
      if (thuoc && !co) veThe(r, false);
      else if (!thuoc && co) boThe(id);
    });
    ds.forEach(function (p) {
      if (DA_TAI[p] || !bat()) return;
      DA_TAI[p] = 1;
      api("/tisa-nhieu-may/api/giao?phien=" + encodeURIComponent(p)).then(function (d) {
        ((d && d.viec) || []).forEach(function (r) { if (!THE[r.id]) THE[r.id] = r; });
        giuThe(); hoiTienDo();
      });
    });
  }
  // Khung chat còn trống mà anh gửi việc, rồi gõ tiếp như thường thì TISA BOT tạo mã phiên mới: nhớ phiên tạm đi kèm phiên đó.
  var _phienTruoc = null;
  function theoDoiPhien() {
    var p = phienApp();
    if (p && TAM && !_phienTruoc) { var b = docLS(LS_BIDANH); b[p] = TAM; ghiLS(LS_BIDANH, b); TAM = ""; }
    else if (p !== _phienTruoc && _phienTruoc !== null && !p) TAM = "";
    _phienTruoc = p;
  }

  var _hoi = false;
  function hoiTienDo() {
    if (_hoi) return;
    var dang = Object.keys(THE).filter(function (k) { return THE[k].trang_thai === "dang_lam" && /^[0-9a-f]{16}$/.test(k); });
    if (!dang.length) return;
    _hoi = true;
    var i = 0;
    (function tiep() {
      if (i >= dang.length) { _hoi = false; setTimeout(hoiTienDo, 4000); return; }
      var id = dang[i++];
      api("/tisa-nhieu-may/api/giao/" + id).then(function (d) {
        if (d && d.ok && d.viec) {
          var cu = THE[id] && THE[id].trang_thai;
          THE[id] = d.viec;
          if (D.querySelector(".tml-kq[data-tml='" + id + "']")) veThe(d.viec, false);
          if (cu === "dang_lam" && d.viec.trang_thai !== "dang_lam")
            toast(d.viec.trang_thai === "xong" ? "Máy " + d.viec.ten_may + " đã làm xong việc anh giao." : "Máy " + d.viec.ten_may + " báo lỗi khi làm việc anh giao.");
        }
        tiep();
      });
    })();
  }

  function ve() { css(); veNhan(); vePill(); }
  function vong() { theoDoiPhien(); ve(); giuThe(); }
  function khoiDong(n) {
    if (!D.body || !boc()) { if (n < 120) setTimeout(function () { khoiDong(n + 1); }, 250); return; }
    tai(true).then(function () { vong(); });
    setInterval(function () { tai(false); vong(); }, 3000);
    W.addEventListener("tisa:sessions-changed", function (e) {
      if (e && e.detail && e.detail.reason === "open") { TAM = ""; _phienTruoc = phienApp(); }   // mở cuộc khác: phiên tạm không đi theo
      setTimeout(vong, 60);
    });
    W.addEventListener("resize", function () { if (MENU) dongMenu(); vePill(); });
  }
  khoiDong(0);
  W.TISAMayLam = { tai: tai, chon: datChon, mayChon: mayChon, boiCanh: boiCanh, veThe: veThe };
})();
