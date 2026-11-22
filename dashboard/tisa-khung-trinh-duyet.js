/* Khung trình duyệt cạnh ô chat (V3.43, chủ yêu cầu 22/11/2026).
   Nút "Trình duyệt" trên thanh khung chat mở một khung bên phải: thấy trực tiếp trình duyệt AI đang dùng, tự bấm, gõ, đăng nhập
   ngay trong khung (kể cả khi mở TISA BOT qua tên miền, trên máy khác). Giao việc ở ô chat bên trái, AI làm trong đúng tab đang xem.
   Máy chủ: server/tisa_khung_trinh_duyet.py (WebSocket /trinh-duyet/khung/ws). Không ghi lại phím hay chữ anh gõ. */
(function () {
  "use strict";
  if (window.TISAKhungTD) return;
  var D = document, LS = "tkd-", MOBI = 820;
  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg>';
  function luu(k, v) { try { localStorage.setItem(LS + k, v); } catch (e) {} }
  function doc(k) { try { return localStorage.getItem(LS + k); } catch (e) { return null; } }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(u, body) {
    return fetch(u, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), credentials: "same-origin" } : { credentials: "same-origin" })
      .then(function (r) { return r.json(); }).catch(function () { return {}; });
  }

  function css() {
    if (D.getElementById("tkdCss")) return;
    var s = D.createElement("style"); s.id = "tkdCss";
    s.textContent =
      ".tkd{--n:#0d1330;--n2:#141b40;--vien:rgba(255,255,255,.1);--chu:#eef1ff;--mo:#9aa6d6;--nut:rgba(255,255,255,.07);--nut-h:rgba(255,255,255,.14);--cam:#ff8a3d;--xanh:#5b8cff}" +
      "html[data-theme='light'] .tkd{--n:#ffffff;--n2:#f3f5fb;--vien:rgba(30,40,90,.13);--chu:#1b2350;--mo:#66709a;--nut:rgba(30,40,90,.05);--nut-h:rgba(30,40,90,.11)}" +
      "body.tkd-mo #cview{right:var(--tkd-w)!important;width:auto!important}" +
      ".tkd{position:fixed;top:0;right:0;bottom:0;width:var(--tkd-w);z-index:400;display:flex;flex-direction:column;background:var(--n);color:var(--chu);border-left:1px solid var(--vien);font:13px/1.4 inherit;font-family:inherit}" +
      ".tkd-keo{position:absolute;left:-4px;top:0;bottom:0;width:8px;cursor:col-resize;z-index:2}.tkd-keo:hover{background:rgba(91,140,255,.25)}" +
      ".tkd-tabs{display:flex;align-items:center;gap:4px;padding:6px 8px 0;overflow-x:auto;scrollbar-width:none;flex:none}.tkd-tabs::-webkit-scrollbar{display:none}" +
      ".tkd-tab{display:flex;align-items:center;gap:6px;max-width:190px;min-width:90px;padding:6px 8px 6px 10px;border-radius:9px 9px 0 0;background:var(--nut);color:var(--mo);border:1px solid transparent;cursor:pointer;flex:none}" +
      ".tkd-tab.on{background:var(--n2);color:var(--chu);border-color:var(--vien);border-bottom-color:var(--n2)}" +
      ".tkd-tab span{flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.tkd-tab b{font-weight:400;opacity:.6;padding:0 3px;border-radius:5px}.tkd-tab b:hover{opacity:1;background:var(--nut-h)}" +
      ".tkd-ic{flex:none;display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:30px;padding:0 8px;border:0;border-radius:8px;background:transparent;color:var(--chu);cursor:pointer;font:inherit;gap:5px}" +
      ".tkd-ic:hover{background:var(--nut-h)}.tkd-ic:disabled{opacity:.35;cursor:default;background:transparent}.tkd-ic svg{width:16px;height:16px}" +
      ".tkd-thanh{display:flex;align-items:center;gap:4px;padding:6px 8px;background:var(--n2);border-bottom:1px solid var(--vien);flex:none}" +
      ".tkd-dc{flex:1;min-width:60px;height:32px;padding:0 12px;border-radius:16px;border:1px solid var(--vien);background:var(--n);color:var(--chu);font:inherit;outline:none}.tkd-dc:focus{border-color:var(--xanh)}" +
      ".tkd-quyen{display:flex;align-items:center;gap:6px;padding:6px 10px;border-bottom:1px solid var(--vien);flex:none;flex-wrap:wrap}" +
      ".tkd-quyen select{height:28px;border-radius:8px;border:1px solid var(--vien);background:var(--n2);color:var(--chu);font:inherit;padding:0 6px}" +
      ".tkd-hs{max-width:230px}" +
      ".tkd-quyen .tq{color:var(--cam);font-weight:700}.tkd-nho{color:var(--mo);font-size:12px;flex:1;min-width:120px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}" +
      ".tkd-nut{height:28px;padding:0 10px;border-radius:8px;border:1px solid var(--vien);background:var(--nut);color:var(--chu);font:inherit;cursor:pointer}.tkd-nut:hover{background:var(--nut-h)}" +
      ".tkd-nut.do{border-color:rgba(255,90,90,.5);color:#ff7b7b}.tkd-nut.cam{background:var(--cam);border-color:var(--cam);color:#1a1000;font-weight:700}" +
      ".tkd-man{position:relative;flex:1;min-height:0;overflow:hidden;background:#000;display:flex;align-items:flex-start;justify-content:center;outline:none}" +
      ".tkd-man canvas{display:block;user-select:none;-webkit-user-drag:none;cursor:default;touch-action:none}" +
      ".tkd-man.ai{box-shadow:inset 0 0 0 2px var(--cam)}" +
      ".tkd-go{position:absolute;left:-9999px;top:0;width:20px;height:20px;opacity:0}" +
      ".tkd-bao{position:absolute;left:50%;top:14px;transform:translateX(-50%);max-width:90%;padding:8px 14px;border-radius:10px;background:rgba(13,19,48,.92);color:#eef1ff;font-size:13px;pointer-events:none;text-align:center}" +
      ".tkd-bao[hidden]{display:none}" +
      ".tkd-hop{position:absolute;left:12px;right:12px;bottom:12px;padding:10px 12px;border-radius:10px;background:var(--n2);border:1px solid var(--vien);display:flex;gap:8px;align-items:center;flex-wrap:wrap}" +
      ".tkd-hop p{flex:1;margin:0;min-width:160px}" +
      ".tkd-xn{display:flex;align-items:center;gap:6px;flex-wrap:wrap;width:100%;padding:8px;border-radius:8px;background:rgba(255,138,61,.12);border:1px solid rgba(255,138,61,.4)}" +
      ".tkd-xn p{margin:0;flex:1;min-width:180px}" +
      ".tkd-mo-nut svg{width:15px;height:15px}" +
      ".tkd-td{margin:0 0 14px;padding:12px 14px;border-radius:12px;border:1px dashed rgba(91,140,255,.55);background:rgba(91,140,255,.07)}" +
      ".tkd-td label{display:flex;align-items:center;gap:6px;font-weight:700;margin:0 0 8px}.tkd-td label svg{width:16px;height:16px}" +
      ".tkd-td-hang{display:flex;gap:8px}.tkd-td-hang input{flex:1;min-width:0}" +
      ".tkd-td-nut{flex:none;padding:0 16px;min-height:40px;border:0;border-radius:10px;background:#172f72;color:#fff;font:700 14px/1 inherit;font-family:inherit;cursor:pointer}.tkd-td-nut:disabled{opacity:.6}" +
      ".tkd-td small{display:block;margin-top:6px;opacity:.75;line-height:1.45}" +
      ".tkd-mo-nut-cp{margin-left:auto;flex:none;display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:9px;border:1px solid var(--line,rgba(120,130,170,.3));background:transparent;color:inherit;font:600 13px/1 inherit;font-family:inherit;cursor:pointer}" +
      ".tkd-mo-nut-cp:hover,.tkd-mo-nut-cp.on{background:rgba(91,140,255,.14)}" +
      "@media (max-width:" + MOBI + "px){.tkd{width:100%!important;left:0;border-left:0;z-index:2147481000}.tkd-keo{display:none}body.tkd-mo #cview{right:0!important}}";
    D.head.appendChild(s);
  }

  /* ------------------------------------------------------------ trạng thái */
  var el = null, man = null, img = null, go = null, ws = null, mo = false, meta = { w: 0, h: 0 }, thu = 0, henNoi = null, henKt = null, henTt = null, vua = doc("vua") !== "0";
  var TT = {}, ST = {}, hoiTQ = false, hop = null, NGOAI = false, CHAT = "", henChat = null, CHO = false;
  // Mỗi ô chat một trình duyệt riêng (tab riêng): đổi ô chat thì khung nối lại, chỉ thấy tab của ô chat đó.
  function chatHienTai() { try { return (window.TISASessions && window.TISASessions.current && window.TISASessions.current()) || ""; } catch (e) { return ""; } }
  function theoChat() {
    if (!mo) return;
    var c = chatHienTai();
    if (c && c !== CHAT) { thu = 0; clearTimeout(henNoi); noi(); taiHs(); }
  }

  function beRong() {
    var w = parseInt(doc("w"), 10), vw = innerWidth;
    if (!(w > 0)) w = Math.round(vw * 0.46);
    return Math.max(380, Math.min(w, Math.round(vw * 0.75)));
  }
  function datBeRong(w) { D.documentElement.style.setProperty("--tkd-w", w + "px"); }

  function gui(o) { if (ws && ws.readyState === 1) ws.send(JSON.stringify(o)); }
  function bao(chu, giu) {
    if (!el) return; var b = el.querySelector(".tkd-bao"); if (!b) return;
    b.textContent = chu || ""; b.hidden = !chu; clearTimeout(bao.t);
    if (chu && !giu) bao.t = setTimeout(function () { b.hidden = true; }, 3500);
  }

  /* ------------------------------------------------------------ dựng khung */
  function dung() {
    css();
    el = D.createElement("div"); el.className = "tkd"; el.setAttribute("role", "region"); el.setAttribute("aria-label", "Trình duyệt của AI");
    el.innerHTML =
      "<div class='tkd-keo' title='Kéo để đổi bề rộng'></div>" +
      "<div class='tkd-tabs'></div>" +
      "<div class='tkd-thanh'>" +
        "<button type='button' class='tkd-ic' data-k='lui' title='Lùi' disabled>‹</button>" +
        "<button type='button' class='tkd-ic' data-k='toi' title='Tới' disabled>›</button>" +
        "<button type='button' class='tkd-ic' data-k='tai' title='Tải lại'>⟳</button>" +
        "<input class='tkd-dc' type='text' spellcheck='false' autocomplete='off' placeholder='Nhập địa chỉ hoặc từ khóa' aria-label='Địa chỉ trang'>" +
        "<button type='button' class='tkd-ic' data-k='vua' title='Vừa khung: trang dàn theo bề rộng khung. Tắt: xem như màn hình máy tính rồi thu nhỏ'>⤢</button>" +
        "<button type='button' class='tkd-ic' data-k='dong' title='Đóng khung trình duyệt' aria-label='Đóng'>×</button>" +
      "</div>" +
      "<div class='tkd-quyen'></div>" +
      "<div class='tkd-man' tabindex='-1'><canvas class='tkd-hinh' role='img' aria-label='Màn hình trình duyệt của AI'></canvas><textarea class='tkd-go' aria-label='Gõ vào trang' autocapitalize='off' autocomplete='off' spellcheck='false'></textarea><div class='tkd-bao' hidden></div></div>";
    D.body.appendChild(el);
    man = el.querySelector(".tkd-man"); img = man.querySelector("canvas"); go = man.querySelector(".tkd-go");
    noiSuKien();
  }

  function veTabs() {
    if (!el) return;
    var ds = TT.tabs || [], h = ds.map(function (t) {
      return "<div class='tkd-tab" + (t.id === TT.tab ? " on" : "") + "' data-tab='" + esc(t.id) + "' title='" + esc(t.url) + "'><span>" + esc(t.tieu_de || "Tab mới") + "</span><b data-dong='" + esc(t.id) + "' title='Đóng tab'>×</b></div>";
    }).join("") + "<button type='button' class='tkd-ic' data-k='tab_moi' title='Mở tab mới'>+</button>";
    el.querySelector(".tkd-tabs").innerHTML = h;
    var dc = el.querySelector(".tkd-dc");
    if (D.activeElement !== dc) dc.value = TT.url && TT.url !== "about:blank" && !/^data:/.test(TT.url) ? TT.url : "";      // trang chủ TISA (data:) không hiện chuỗi dài
    el.querySelector("[data-k=lui]").disabled = !TT.lui;
    el.querySelector("[data-k=toi]").disabled = !TT.toi;
    var nv = el.querySelector("[data-k=vua]"); nv.hidden = NGOAI; nv.style.color = vua ? "var(--xanh)" : "";
  }

  var MUC = [["hoi_het", "Hỏi mọi bước"], ["quan_trong", "Hỏi bước quan trọng"], ["toan_quyen", "Toàn quyền"]];
  function veQuyen() {
    if (!el) return;
    var q = el.querySelector(".tkd-quyen"), cur = ST.muc || "quan_trong", nk = (ST.nhat_ky || [])[(ST.nhat_ky || []).length - 1];
    if (q.contains(D.activeElement) && D.activeElement.tagName === "SELECT") return;
    var h = "<select data-k='hs' class='tkd-hs' aria-label='Trình duyệt của ô chat này' title='Chọn Chrome đã đăng nhập tài khoản cần dùng'>" + moHs() + "</select>" +
      "<span class='" + (cur === "toan_quyen" ? "tq" : "") + "'>AI:</span><select data-k='muc' aria-label='Mức tự làm của AI'>" +
      MUC.map(function (m) { return "<option value='" + m[0] + "'" + (m[0] === cur ? " selected" : "") + ">" + m[1] + "</option>"; }).join("") + "</select>" +
      (ST.dung ? "<button type='button' class='tkd-nut cam' data-k='tiep'>Cho AI làm tiếp</button>" : "<button type='button' class='tkd-nut do' data-k='dungai'>Dừng AI</button>") +
      "<span class='tkd-nho' title='" + esc(nk ? nk.mo_ta : "") + "'>" + (cur === "toan_quyen" && ST.muc_den ? "Toàn quyền tới " + new Date(ST.muc_den * 1000).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }) + " · " : "") +
      esc(nk && (nk.mo_ta || nk.op) ? "Vừa làm: " + (nk.mo_ta || nk.op) : "Giao việc ở ô chat, AI làm ngay trong khung này") + "</span>";
    if (hoiTQ) h += "<div class='tkd-xn'><p><b>Bật Toàn quyền?</b> AI tự bấm, gõ, đăng, gửi trong trình duyệt và trên máy tính mà không hỏi (vẫn không xóa tệp). Mật khẩu, mã OTP anh tự nhập trong khung này.</p>" +
      "<select data-k='phut'><option value='30'>30 phút</option><option value='120' selected>2 giờ</option><option value='480'>8 giờ</option><option value='0'>Đến khi anh tắt</option></select>" +
      "<button type='button' class='tkd-nut cam' data-k='tq_ok'>Bật</button><button type='button' class='tkd-nut' data-k='tq_huy'>Hủy</button></div>";
    q.innerHTML = h;
    man.classList.toggle("ai", cur === "toan_quyen" && !ST.dung);
  }
  // Một mức cho cả trình duyệt và điều khiển máy tính (gõ phím, bấm chuột thật): chọn Toàn quyền ở khung là bot không hỏi nữa ở cả hai.
  // Quyền xóa tệp luôn giữ tắt.
  function datMuc(v, phut) {
    Promise.all([api("/trinh-duyet/muc", { muc: v, phut: phut }),
      api("/may-ai/trang-thai").then(function (sm) { return (sm && sm.ho_tro === false) ? 0 : Promise.all([api("/may-ai/muc", { muc: v, phut: phut }), api("/may-ai/cho-xoa", { phut: 0 })]); }).catch(function () {})
    ]).then(taiTT);
  }
  // Trình duyệt của ô chat: trình duyệt riêng chạy ngầm, hoặc một hồ sơ Chrome đã đăng nhập sẵn của anh (đọc từ Chrome trên máy).
  var HS = { ds: null, loai: "", ho_so: "" };
  function moHs() {
    var on = HS.loai === "chrome" ? "c:" + HS.ho_so : HS.loai === "rieng" ? "r" : "";
    var h = (on ? "" : "<option value='' selected>Trình duyệt: chọn...</option>") + "<option value='r'" + (on === "r" ? " selected" : "") + ">Trình duyệt riêng (chạy ngầm)</option>";
    (HS.ds || []).forEach(function (x) {
      var v = "c:" + x.thu_muc;
      h += "<option value='" + esc(v) + "'" + (on === v ? " selected" : "") + ">Chrome: " + esc(x.ten || x.thu_muc) + (x.email ? " (" + esc(x.email) + ")" : "") + "</option>";
    });
    return h;
  }
  function taiHs() {
    var c = CHAT || chatHienTai();
    return Promise.all([HS.ds ? Promise.resolve(null) : api("/may-ai/chrome-ho-so"), c ? api("/trinh-duyet/khung/chat?chat=" + encodeURIComponent(c)) : Promise.resolve({})]).then(function (r) {
      if (r[0]) HS.ds = r[0].ho_so || [];
      HS.loai = (r[1] || {}).loai || ""; HS.ho_so = (r[1] || {}).ho_so || "";
      if (!(el && el.querySelector(".tkd-quyen select:focus"))) veQuyen();
    });
  }
  function chonHs(v) {
    var c = CHAT || chatHienTai(); if (!c || !v) return;
    var body = v === "r" ? { chat: c, loai: "rieng" } : { chat: c, loai: "chrome", ho_so: v.slice(2) };
    bao("Đang đổi trình duyệt...", true);
    api("/trinh-duyet/khung/chon", body).then(function (r) {
      bao(r && r.ok ? r.tin : ((r && (r.loi || r.error)) || "Chưa đổi được trình duyệt."), !(r && r.ok));
      if (r && r.ok) { CHO = false; thu = 0; noi(); }
      taiHs();
    });
  }
  function taiTT() {
    return api("/trinh-duyet/trang-thai?nhe=1").then(function (d) { ST = d || {}; veQuyen(); });
  }

  function veHop() {
    var c = man && man.querySelector(".tkd-hop"); if (c) c.remove();
    if (!hop || !man) return;
    var d = D.createElement("div"); d.className = "tkd-hop";
    d.innerHTML = "<p>Trang hỏi: <b>" + esc(hop.chu) + "</b></p>" + (hop.kieu === "prompt" ? "<input class='tkd-dc' style='flex:1' data-hop-chu>" : "") +
      "<button type='button' class='tkd-nut cam' data-hop='1'>Đồng ý</button>" + (hop.kieu !== "alert" ? "<button type='button' class='tkd-nut' data-hop='0'>Hủy</button>" : "");
    man.appendChild(d);
  }

  /* ------------------------------------------------------------ kết nối */
  function kichThuoc() {
    var r = man.getBoundingClientRect();
    return { t: "kt", w: Math.round(r.width), h: Math.round(r.height), dpr: window.devicePixelRatio || 1, vua: vua };
  }
  function noi() {
    if (!mo) return;
    clearTimeout(henNoi);
    CHAT = chatHienTai();
    var u = (location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/trinh-duyet/khung/ws?chat=" + encodeURIComponent(CHAT) + (CHO ? "&cho=1" : "");
    TT = {}; if (el) veTabs();
    bao("Đang nối trình duyệt...", true);
    if (ws) { var cu = ws; ws = null; try { cu.close(); } catch (e) {} }      // chỉ giữ MỘT kết nối: kết nối cũ còn sống sẽ vẽ tab của ô chat khác
    try { ws = new WebSocket(u); } catch (e) { henNoi = setTimeout(noi, 3000); return; }
    var w = ws;
    w.onopen = function () { thu = 0; w.send(JSON.stringify(kichThuoc())); };
    w.onmessage = function (e) {
      if (w !== ws) return;          // tin của kết nối đã bỏ (ô chat trước): không vẽ
      var d; try { d = JSON.parse(e.data); } catch (x) { return; }
      if (d.t === "hinh") {
        if (d.m) meta = { w: d.m.w || meta.w, h: d.m.h || meta.h };
        veHinh(d.d);
      } else if (d.t === "trang") { TT = d; veTabs(); }
      else if (d.t === "san_sang") { bao(NGOAI || d.ngoai ? "Đang xem tab TISA BOT mở trong Chrome của anh (chỉ tab của việc này)" : ""); NGOAI = !!d.ngoai; veTabs(); }
      else if (d.t === "cho") { TT = {}; veTabs(); bao(d.chu, true); }
      else if (d.t === "bao") bao(d.chu);
      else if (d.t === "loi") bao(d.chu, true);
      else if (d.t === "hop") { hop = d; veHop(); }
      else if (d.t === "chep") { if (d.s && navigator.clipboard) navigator.clipboard.writeText(d.s).then(function () { bao("Đã chép"); }, function () {}); }
    };
    w.onclose = function () {
      if (ws !== w) return;          // mình tự đóng (đổi ô chat, nối lại): không hẹn nối thêm
      ws = null;
      if (!mo) return;
      thu++; bao("Mất kết nối trình duyệt, đang nối lại...", true);
      henNoi = setTimeout(noi, Math.min(10000, 1000 * thu));
    };
  }

  // Vẽ khung hình lên canvas: giải mã xong mới thay, không có lúc trống giữa hai khung (đổi img.src liên tục làm khung nháy).
  var soGui = 0, soVe = 0;
  function veHinh(b64) {
    var so = ++soGui, bin = atob(b64), u8 = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    var blob = new Blob([u8], { type: "image/jpeg" });
    function ve(nguon, w, h, xong) {
      if (!img || so < soVe) { if (xong) xong(); return; }
      soVe = so;
      if (img.width !== w || img.height !== h) { img.width = w; img.height = h; }
      var cx = img.getContext("2d"); cx.clearRect(0, 0, w, h); cx.drawImage(nguon, 0, 0, w, h);
      if (xong) xong();
      vuaAnh();
    }
    if (window.createImageBitmap) createImageBitmap(blob).then(function (bm) { ve(bm, bm.width, bm.height, function () { if (bm.close) bm.close(); }); }, function () {});
    else { var im = new Image(), u = URL.createObjectURL(blob); im.onload = function () { ve(im, im.naturalWidth, im.naturalHeight); URL.revokeObjectURL(u); }; im.src = u; }
  }
  // Hình nhỏ hơn khung (Chrome của anh, hoặc tắt Vừa khung): phóng cho vừa khung, giữ đúng tỉ lệ.
  function vuaAnh() {
    if (!man || !img || !img.width || !img.height) return;
    var W = man.clientWidth, H = man.clientHeight, k = Math.min(W / img.width, H / img.height);
    img.style.width = Math.floor(img.width * k) + "px"; img.style.height = Math.floor(img.height * k) + "px";
  }

  /* ------------------------------------------------------------ chuột, phím */
  function toaDo(e) {
    var r = img.getBoundingClientRect();
    if (!r.width || !meta.w) return null;
    return { x: (e.clientX - r.left) / r.width * meta.w, y: (e.clientY - r.top) / r.height * meta.h };
  }
  function mods(e) { return (e.altKey ? 1 : 0) | (e.ctrlKey ? 2 : 0) | (e.metaKey ? 4 : 0) | (e.shiftKey ? 8 : 0); }
  var NUT = ["left", "middle", "right"], dangGiu = 0, henDi = 0, diCho = null;
  function lamChuot(kieu, e) {
    var p = toaDo(e); if (!p) return;
    gui({ t: "chuot", kieu: kieu, x: p.x, y: p.y, nut: kieu === "mouseMoved" ? (dangGiu ? "left" : "none") : (NUT[e.button] || "left"), nuts: e.buttons || 0, lan: kieu === "mouseMoved" ? 0 : (e.detail || 1), mods: mods(e) });
  }
  var DAC_BIET = /^(Enter|Backspace|Tab|Escape|Delete|ArrowLeft|ArrowRight|ArrowUp|ArrowDown|Home|End|PageUp|PageDown|F5)$/;

  function noiSuKien() {
    el.addEventListener("click", function (e) {
      var t = e.target.closest("[data-k],[data-tab],[data-dong],[data-hop]"); if (!t) return;
      if (t.hasAttribute("data-dong")) { e.stopPropagation(); gui({ t: "dong_tab", id: t.getAttribute("data-dong") }); return; }
      if (t.hasAttribute("data-tab")) { gui({ t: "tab", id: t.getAttribute("data-tab") }); return; }
      if (t.hasAttribute("data-hop")) { var c = man.querySelector("[data-hop-chu]"); gui({ t: "hop", ok: t.getAttribute("data-hop") === "1", chu: c ? c.value : null }); hop = null; veHop(); return; }
      var k = t.getAttribute("data-k");
      if (k === "dong") dong();
      else if (k === "lui" || k === "toi" || k === "tai") gui({ t: k });
      else if (k === "tab_moi") gui({ t: "tab_moi" });
      else if (k === "vua") { vua = !vua; luu("vua", vua ? "1" : "0"); gui({ t: "vua", on: vua }); veTabs(); }
      else if (k === "dungai") api("/trinh-duyet/dung", {}).then(taiTT);
      else if (k === "tiep") api("/trinh-duyet/tiep-tuc", {}).then(taiTT);
      else if (k === "tq_huy") { hoiTQ = false; veQuyen(); }
      else if (k === "tq_ok") { var ph = el.querySelector("[data-k=phut]"); hoiTQ = false; datMuc("toan_quyen", +(ph ? ph.value : 120)); }
    });
    el.addEventListener("change", function (e) {
      if (e.target.getAttribute("data-k") === "hs") { chonHs(e.target.value); return; }
      if (e.target.getAttribute("data-k") !== "muc") return;
      var v = e.target.value;
      if (v === "toan_quyen") { hoiTQ = true; ST.muc = ST.muc || "quan_trong"; e.target.blur(); veQuyen(); return; }
      datMuc(v, 0);
    });
    var dc = el.querySelector(".tkd-dc");
    dc.addEventListener("keydown", function (e) { if (e.key === "Enter") { gui({ t: "di", url: dc.value }); dc.blur(); } });
    dc.addEventListener("focus", function () { dc.select(); });

    // kéo đổi bề rộng
    el.querySelector(".tkd-keo").addEventListener("mousedown", function (e) {
      e.preventDefault();
      function di(ev) { datBeRong(Math.max(380, Math.min(innerWidth - ev.clientX, innerWidth * 0.75))); }
      function tha() { D.removeEventListener("mousemove", di); D.removeEventListener("mouseup", tha); luu("w", parseInt(getComputedStyle(D.documentElement).getPropertyValue("--tkd-w"), 10) || ""); }
      D.addEventListener("mousemove", di); D.addEventListener("mouseup", tha);
    });

    // chuột
    img.addEventListener("mousedown", function (e) { e.preventDefault(); go.focus({ preventScroll: true }); dangGiu = 1; lamChuot("mousePressed", e); });
    D.addEventListener("mouseup", function (e) { if (!dangGiu) return; dangGiu = 0; lamChuot("mouseReleased", e); });
    img.addEventListener("mousemove", function (e) {
      diCho = e; var now = Date.now();
      if (now - henDi < (dangGiu ? 30 : 90)) return;
      henDi = now; lamChuot("mouseMoved", diCho);
    });
    img.addEventListener("contextmenu", function (e) { e.preventDefault(); });
    man.addEventListener("wheel", function (e) {
      e.preventDefault(); var p = toaDo(e); if (!p) return;
      var k = e.deltaMode === 1 ? 33 : e.deltaMode === 2 ? man.clientHeight : 1;
      gui({ t: "cuon", x: p.x, y: p.y, dx: e.deltaX * k, dy: e.deltaY * k, mods: mods(e) });
    }, { passive: false });

    // chạm (điện thoại): chạm = bấm, vuốt = cuộn
    var cham = null;
    img.addEventListener("touchstart", function (e) { if (e.touches.length !== 1) return; var t = e.touches[0]; cham = { x: t.clientX, y: t.clientY, x0: t.clientX, y0: t.clientY, keo: false }; }, { passive: true });
    img.addEventListener("touchmove", function (e) {
      if (!cham || e.touches.length !== 1) return; e.preventDefault();
      var t = e.touches[0], dx = cham.x - t.clientX, dy = cham.y - t.clientY;
      if (Math.abs(t.clientX - cham.x0) + Math.abs(t.clientY - cham.y0) > 8) cham.keo = true;
      var p = toaDo(t); if (p && cham.keo) gui({ t: "cuon", x: p.x, y: p.y, dx: dx * 1.5, dy: dy * 1.5, mods: 0 });
      cham.x = t.clientX; cham.y = t.clientY;
    }, { passive: false });
    img.addEventListener("touchend", function (e) {
      if (!cham) return; var c = cham; cham = null; if (c.keo) return;
      e.preventDefault(); var ev = { clientX: c.x0, clientY: c.y0, button: 0, buttons: 1, detail: 1 };
      go.focus({ preventScroll: true }); lamChuot("mousePressed", ev); ev.buttons = 0; lamChuot("mouseReleased", ev);
    }, { passive: false });

    // phím: chữ (kể cả gõ dấu tiếng Việt) đi qua ô ẩn rồi insertText; phím đặc biệt và phím tắt đi thẳng
    var dangGo = false;
    go.addEventListener("compositionstart", function () { dangGo = true; });
    go.addEventListener("compositionend", function (e) { dangGo = false; if (e.data) gui({ t: "chu", s: e.data }); go.value = ""; });
    go.addEventListener("input", function (e) { if (dangGo || e.isComposing) return; if (go.value) gui({ t: "chu", s: go.value }); go.value = ""; });
    go.addEventListener("paste", function (e) { e.preventDefault(); var s = (e.clipboardData || window.clipboardData).getData("text"); if (s) gui({ t: "chu", s: s }); });
    go.addEventListener("copy", function (e) { e.preventDefault(); gui({ t: "chep" }); });
    go.addEventListener("cut", function (e) { e.preventDefault(); gui({ t: "chep" }); gui({ t: "phim", kieu: "down", key: "x", code: "KeyX", ma: 88, mods: 4 }); });
    function phim(kieu, e) {
      if (e.isComposing || e.keyCode === 229 || dangGo) return;
      var tat = (e.metaKey || e.ctrlKey) && e.key.length === 1;
      if (tat && /^[vc]$/i.test(e.key)) return;        // dán, chép: để trình duyệt của anh lo (sự kiện paste / copy ở trên)
      if (!DAC_BIET.test(e.key) && !tat) return;
      e.preventDefault();
      if (e.key === "F5") { if (kieu === "down") gui({ t: "tai" }); return; }
      gui({ t: "phim", kieu: kieu, key: e.key, code: e.code, ma: e.keyCode, mods: mods(e) });
    }
    go.addEventListener("keydown", function (e) { phim("down", e); });
    go.addEventListener("keyup", function (e) { phim("up", e); });
    man.addEventListener("mousedown", function (e) { if (e.target === man) go.focus({ preventScroll: true }); });

    // đổi cỡ khung thì báo máy chủ (trang dàn lại theo khung)
    if (window.ResizeObserver) new ResizeObserver(function () { vuaAnh(); clearTimeout(henKt); henKt = setTimeout(function () { gui(kichThuoc()); }, 250); }).observe(man);
  }

  /* ------------------------------------------------------------ mở / đóng */
  // opts.cho: tự mở để XEM bot làm (đấu nối MCP/API, bot dùng trình duyệt): đi theo đúng trình duyệt và tab bot đang dùng,
  // chưa có tab thì chờ, không tự mở trình duyệt riêng. Anh bấm nút Trình duyệt thì như cũ (trình duyệt chạy ngầm riêng của khung).
  function moKhung(opts) {
    var cho = !!(opts && opts.cho);
    if (mo) { if (cho !== CHO) { CHO = cho; thu = 0; noi(); } else if (el && !cho) el.querySelector(".tkd-dc").focus(); return; }
    CHO = cho;
    mo = true; luu("mo", "1");
    datBeRong(beRong());
    if (!el) dung(); else el.hidden = false;
    D.body.classList.add("tkd-mo");
    noi(); taiTT(); taiHs(); henTt = setInterval(function () { if (!D.hidden) taiTT(); }, 4000);
    henChat = setInterval(theoChat, 1000);
    capNhatNut();
  }
  function dong() {
    if (CHAT) { try { sessionStorage.setItem(LS + "tat:" + CHAT, "1"); } catch (e) {} }      // anh tự đóng: không tự mở lại cho ô chat này
    mo = false; CHO = false; luu("mo", "0");
    clearTimeout(henNoi); clearInterval(henTt); clearInterval(henChat);
    if (ws) { var w = ws; ws = null; try { w.close(); } catch (e) {} }
    if (el) { el.remove(); el = null; man = img = go = null; }
    D.body.classList.remove("tkd-mo");
    capNhatNut();
  }

  /* ------------------------------------------------------------ nút trên thanh khung chat */
  function capNhatNut() {
    // Chỉ ghi khi khác: ghi thuộc tính mỗi lần quét làm MutationObserver tự kích lại chính nó (vòng lặp nhỏ vô ích).
    D.querySelectorAll(".tkd-mo-nut").forEach(function (b) { var v = mo ? "true" : "false"; if (b.getAttribute("aria-pressed") !== v) b.setAttribute("aria-pressed", v); if (b.classList.contains("on") !== mo) b.classList.toggle("on", mo); });
  }
  function camNut() {
    css();          // nút và ô Kết nối tự động cần kiểu ngay cả khi khung chưa mở lần nào (thiếu là biểu tượng phình to)
    // Trang Cộng sự: thanh .ws-bar; trang Hỏi nhanh / Trò chuyện: thanh .chatpage-bar (Thu nhỏ + tên hội thoại).
    var them = false;
    D.querySelectorAll(".ws-bar, .chatpage-bar").forEach(function (bar) {
      if (bar.querySelector(".tkd-mo-nut")) return;
      them = true;
      var b = D.createElement("button"); b.type = "button"; b.className = "ws-btn tkd-mo-nut"; b.title = "Mở trình duyệt bên cạnh để xem và điều khiển cùng AI";
      b.innerHTML = ICON + " Trình duyệt";
      b.onclick = function () { mo ? dong() : moKhung(); };      // bấm tay: khung dùng trình duyệt chạy ngầm riêng
      if (bar.classList.contains("chatpage-bar")) { b.className = "tkd-mo-nut tkd-mo-nut-cp"; bar.appendChild(b); return; }
      var phai = bar.querySelector("#wsRightBtn"); bar.insertBefore(b, phai || null);
    });
    if (them) capNhatNut();
  }
  /* (V3.43, chủ 22/11) Hộp "Tự thêm MCP server": thêm ô Kết nối tự động. Anh gõ tên app/công cụ, bấm Tự động: Đạt Đấu Nối tìm MCP hoặc API chính thức,
     mở trang nhà cung cấp trong Chrome đã đăng nhập của anh, lấy link/khóa, thêm vào TISA BOT và kiểm tra; khung Trình duyệt bên cạnh cho anh xem bot làm. */
  function camTuDong() {
    D.querySelectorAll(".mcpf-dan").forEach(function (dan) {
      var than = dan.parentNode; if (!than || than.querySelector(".tkd-td")) return;
      var o = D.createElement("div"); o.className = "tkd-td";
      o.innerHTML = "<label for='tkdTdTen'>" + ICON + " Kết nối tự động</label>" +
        "<div class='tkd-td-hang'><input class='js-input' id='tkdTdTen' autocomplete='off' spellcheck='false' placeholder='Tên app cần kết nối, ví dụ: Notion, Google Sheets, Canva, TikTok Ads'>" +
        "<button type='button' class='tkd-td-nut'>Tự động</button></div>" +
        "<small>TISA BOT tự tìm cách kết nối chính thức, mở trình duyệt bên cạnh và làm giúp anh. Gặp đăng nhập, mã OTP hay bấm Cho phép thì anh làm trong khung.</small>";
      than.insertBefore(o, dan);
      var inp = o.querySelector("input"), nut = o.querySelector("button");
      function chay() {
        var ten = String(inp.value || "").trim();
        if (!ten) { inp.focus(); return; }
        if (!window.TISANhoAI) { nut.textContent = "Chưa sẵn sàng, thử lại"; return; }
        var text = "Đấu nối tự động (skill dq-dau-noi-cong-cu): kết nối \"" + ten + "\" vào TISA BOT để em dùng được trong chat.\n" +
          "1. Tìm cách kết nối CHÍNH THỨC của " + ten + ": ưu tiên MCP server chính thức (link https hoặc lệnh npx/uvx), không có thì API key/OAuth của nhà cung cấp. Nói rõ cách đã chọn.\n" +
          "2. Mở trang của nhà cung cấp trong trình duyệt (Chrome có sẵn đăng nhập của anh), tự bấm, tạo khóa hoặc link. Trang bắt đăng nhập, mã OTP, CAPTCHA, thanh toán thì dừng và nhờ anh làm trong khung Trình duyệt.\n" +
          "3. Thêm vào TISA BOT (Kết nối > MCP: Tự thêm MCP server, hoặc ô API tương ứng), lưu và kiểm tra kết nối chạy thật.\n" +
          "4. Báo lại ngắn: đã nối gì, kiểm tra ra sao, còn thiếu gì. Không ghi khóa vào chat hay bộ não.";
        var hop = o.closest(".pkm, .conn-modal, [role=dialog]");
        var dong = hop && hop.querySelector("[data-close], .pkm-x, .modal-close, button[aria-label='Đóng'], button[aria-label='Close']");
        nut.disabled = true; nut.textContent = "Đang giao...";
        window.TISANhoAI(text, "Kết nối " + ten, "tisa-dau-noi").then(function (ok) {
          if (ok && dong) dong.click();
          nut.disabled = false; nut.textContent = "Tự động";
        });
      }
      nut.addEventListener("click", chay);
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); chay(); } });
    });
  }
  var henCam = 0;
  new MutationObserver(function () { if (henCam) return; henCam = setTimeout(function () { henCam = 0; camNut(); camTuDong(); }, 300); }).observe(D.documentElement, { childList: true, subtree: true });
  camNut();
  window.addEventListener("resize", function () { if (mo) datBeRong(beRong()); });
  if (doc("mo") === "1" && innerWidth > MOBI) setTimeout(moKhung, 800);      // lần trước để mở thì mở lại (máy tính), điện thoại thì không tự mở

  // Bot của ô chat đang mở vừa dùng trình duyệt (đấu nối, cài MCP/API, làm web...): tự mở khung để anh thấy bot đang làm gì, ở trang nào.
  // Chỉ trên máy tính (điện thoại: khung che hết ô chat). Anh đóng khung thì không tự mở lại cho ô chat đó.
  var henTu = 0;
  setInterval(function () {
    if (mo || D.hidden || innerWidth <= MOBI || henTu) return;
    var c = chatHienTai(); if (!c) return;
    try { if (sessionStorage.getItem(LS + "tat:" + c) === "1") return; } catch (e) {}
    henTu = 1;
    api("/trinh-duyet/khung/chat?chat=" + encodeURIComponent(c)).then(function (d) { henTu = 0; if (d && d.moi && !mo && chatHienTai() === c) moKhung({ cho: true }); }, function () { henTu = 0; });
  }, 4000);

  window.TISAKhungTD = { mo: moKhung, dong: dong, dangMo: function () { return mo; } };
})();
