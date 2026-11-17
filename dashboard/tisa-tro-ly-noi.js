/* tisa-tro-ly-noi.js - Cửa sổ trợ lý NỔI khi TISA BOT hỗ trợ cài đặt, kết nối (V3.04, chủ yêu cầu 17/11/2026).

   Vấn đề: bấm "Kết nối tự động" thì TISA BOT tự mở trang Kết nối và hộp nhập mã, che mất khung chat nên anh không thấy AI nói gì,
   không ra lệnh được, không bật mic được. Cửa sổ này nổi trên MỌI trang và hộp thoại:
     - báo AI đang làm tới đâu (câu mới nhất của AI, các việc vừa làm trong trình duyệt);
     - hiện thẻ "Anh cần làm" khi AI chờ anh (đăng nhập, bấm Cho phép...) kèm nút "Em làm xong rồi";
     - ô chat để gõ với AI, và nút GỌI: dùng đúng tính năng gọi điện nói chuyện qua lại của khung chat (#voiceBtn), không có mic hay đọc to riêng;
     - nút Dừng AI ngay, thu nhỏ, kéo đi chỗ khác.
   Không có khung chat riêng: dùng chính khung chat của TISA BOT (#chatInput, #sendBtn, #chatArea) nên lời nói nằm trong cùng một cuộc trò chuyện. */
(function () {
  "use strict";
  var W = window, D = document;
  var el = null, pill = null, tim = null, mo = false, thu = false, tieuDe = "Hỗ trợ cài đặt";
  var lanCuoi = { text: "", luc: 0, nk: "", steps: "" }, goiTuDay = false;
  var vt = null;      // vị trí đã kéo

  var CSS = [
    ".tln{position:fixed;right:16px;bottom:16px;z-index:2147483200;width:min(380px,calc(100vw - 24px));max-height:min(620px,calc(100vh - 24px));display:flex;flex-direction:column;border-radius:18px;background:var(--mm-base,#fff);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,rgba(23,47,114,.18));box-shadow:0 24px 70px -18px rgba(8,16,48,.55);font:14px/1.5 inherit;overflow:hidden}",
    ".tln[hidden]{display:none}",
    ".tln-dau{display:flex;align-items:center;gap:10px;padding:10px 12px;background:linear-gradient(135deg,var(--tisa-nhan,#ff6b35),var(--tisa-chinh,#172f72));color:#fff;cursor:grab;user-select:none;touch-action:none}",
    ".tln-dau b{flex:1;min-width:0;font-size:14px;line-height:1.25}.tln-dau small{display:block;font-weight:500;opacity:.85;font-size:12px}",
    ".tln-cham{flex:none;width:10px;height:10px;border-radius:50%;background:#9aa6d6}.tln-cham.lam{background:#4ade80;box-shadow:0 0 0 0 rgba(74,222,128,.7);animation:tlnNhip 1.4s infinite}.tln-cham.cho{background:#fbbf24}",
    "@keyframes tlnNhip{0%{box-shadow:0 0 0 0 rgba(74,222,128,.6)}100%{box-shadow:0 0 0 9px rgba(74,222,128,0)}}",
    ".tln-nut-dau{flex:none;border:0;background:rgba(255,255,255,.18);color:#fff;width:28px;height:28px;border-radius:8px;cursor:pointer;font-size:15px;line-height:1}.tln-nut-dau:hover{background:rgba(255,255,255,.32)}",
    ".tln-than{flex:1 1 auto;overflow:auto;padding:12px;display:grid;gap:10px;min-height:120px;align-content:start}",
    ".tln-nguoi{padding:11px 12px;border-radius:12px;border:1.5px solid #f59e0b;background:rgba(245,158,11,.12)}.tln-nguoi b{display:block;margin-bottom:4px;color:#b45309}",
    ".tln-nguoi .tln-hang{margin-top:8px}",
    ".tln-ai{padding:10px 12px;border-radius:12px;background:var(--mm-soft,#f1f4fb);max-height:210px;overflow:auto;white-space:pre-wrap;word-break:break-word;font-size:13.5px}",
    ".tln-ai small{display:block;color:var(--mm-muted,#5b6478);margin-bottom:4px;font-weight:600}",
    ".tln-nk{display:grid;gap:3px;font-size:12.5px;color:var(--mm-muted,#5b6478);max-height:104px;overflow:auto}.tln-nk div{display:flex;gap:6px}.tln-nk time{flex:none;opacity:.8}",
    ".tln-hang{display:flex;gap:8px;flex-wrap:wrap;align-items:center}",
    ".tln-nut{border:1px solid var(--mm-line2,rgba(23,47,114,.2));background:var(--mm-soft,#f1f4fb);color:inherit;border-radius:10px;padding:0 12px;min-height:34px;font:600 13px/1 inherit;cursor:pointer}.tln-nut:hover{filter:brightness(.96)}",
    ".tln-nut.chinh{background:var(--tisa-nhan,#ff6b35);border-color:var(--tisa-nhan,#ff6b35);color:#fff}.tln-nut.do{background:#d93025;border-color:#d93025;color:#fff}.tln-nut:disabled{opacity:.5;cursor:default}",
    ".tln-chat{display:flex;gap:6px;align-items:center;padding:8px 10px;border-top:1px solid var(--mm-line,rgba(23,47,114,.12))}",
    ".tln-chat input[type=text]{flex:1 1 auto;min-width:0;height:38px;border-radius:10px;border:1px solid var(--mm-line2,rgba(23,47,114,.22));background:var(--mm-base,#fff);color:inherit;padding:0 10px;font:inherit}",
    ".tln-chan{display:flex;gap:8px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:8px 10px 10px;border-top:1px solid var(--mm-line,rgba(23,47,114,.12));font-size:12.5px}",
    ".tln-nut.goi{background:#16a34a;border-color:#16a34a;color:#fff}.tln-nut.goi.dang{background:#d93025;border-color:#d93025}",
    ".tln-tt{padding:0 12px 8px;font-size:12.5px;color:var(--mm-muted,#5b6478)}.tln-tt.loi{color:#d93025}",
    ".tln-pill{position:fixed;right:16px;bottom:16px;z-index:2147483200;display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;border:0;background:linear-gradient(135deg,var(--tisa-nhan,#ff6b35),var(--tisa-chinh,#172f72));color:#fff;font:700 13.5px/1 inherit;cursor:pointer;box-shadow:0 14px 40px -12px rgba(8,16,48,.6)}",
    ".tln-pill[hidden]{display:none}",
    ".tln-pill.cho{animation:tlnPill 1s infinite alternate}@keyframes tlnPill{to{transform:scale(1.06)}}",
    "@media (prefers-reduced-motion:reduce){.tln-cham.lam,.tln-pill.cho{animation:none}}",
    "@media (max-width:640px){.tln{right:8px;left:8px;bottom:8px;width:auto}}"
  ].join("");

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(url, body) {
    var o = { method: body === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store" };
    if (body !== undefined) { o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(body); }
    return fetch(url, o).then(function (r) { return r.json(); }).catch(function () { return null; });
  }
  function luu(k, v) { try { W.localStorage.setItem("tln_" + k, v); } catch (e) {} }
  function doc(k) { try { return W.localStorage.getItem("tln_" + k); } catch (e) { return null; } }

  function dungKhung() {
    if (el) return;
    var st = D.createElement("style"); st.id = "tln-css"; st.textContent = CSS; (D.head || D.documentElement).appendChild(st);
    el = D.createElement("div"); el.className = "tln"; el.id = "tisaTroLyNoi"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Trợ lý hỗ trợ cài đặt"); el.hidden = true;
    el.innerHTML = "<div class='tln-dau' id='tlnDau'><i class='tln-cham' id='tlnCham'></i><b><span id='tlnTieu'></span><small id='tlnTrang'>Đang chờ</small></b>" +
      "<button type='button' class='tln-nut-dau' data-tln='thu' title='Thu nhỏ' aria-label='Thu nhỏ'>–</button><button type='button' class='tln-nut-dau' data-tln='dong' title='Đóng' aria-label='Đóng'>✕</button></div>" +
      "<div class='tln-than'><div id='tlnNguoi'></div><div class='tln-ai' id='tlnAi'><small>TISA BOT nói</small><span id='tlnAiText'>Em đang bắt đầu, anh chờ em một chút nhé.</span></div><div class='tln-nk' id='tlnNk'></div></div>" +
      "<div class='tln-tt' id='tlnTt'></div>" +
      "<div class='tln-chat'>" +
      "<input type='text' id='tlnIn' placeholder='Gõ với TISA BOT...' autocomplete='off'><button type='button' class='tln-nut chinh' data-tln='gui'>Gửi</button></div>" +
      "<div class='tln-chan'><button type='button' class='tln-nut goi' id='tlnGoi' data-tln='goi' title='Gọi điện nói chuyện qua lại với TISA BOT'>📞 Gọi TISA BOT</button><span class='tln-hang'><button type='button' class='tln-nut' data-tln='chat'>Mở khung chat</button><button type='button' class='tln-nut do' data-tln='dung'>Dừng AI ngay</button></span></div>";
    D.body.appendChild(el);
    pill = D.createElement("button"); pill.type = "button"; pill.className = "tln-pill"; pill.hidden = true; pill.innerHTML = "<span>🤖</span><span id='tlnPillT'>Trợ lý đang hỗ trợ</span>";
    pill.addEventListener("click", function () { thu = false; hien(); });
    D.body.appendChild(pill);
    var dau = D.getElementById("tlnDau");
    dau.addEventListener("pointerdown", batDauKeo);
    el.addEventListener("click", bam);
    D.getElementById("tlnIn").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); gui(); } });
    var v = doc("vt"); if (v) { try { vt = JSON.parse(v); } catch (e) { vt = null; } }
  }

  /* ---------- kéo thả ---------- */
  function datViTri() {
    if (!el || !vt) return;
    var w = el.offsetWidth || 380;
    var x = Math.max(4, Math.min(W.innerWidth - w - 4, vt.x)), y = Math.max(4, Math.min(W.innerHeight - 60, vt.y));
    el.style.left = x + "px"; el.style.top = y + "px"; el.style.right = "auto"; el.style.bottom = "auto";
  }
  function batDauKeo(e) {
    if (e.target.closest && e.target.closest("button")) return;
    var r = el.getBoundingClientRect(), dx = e.clientX - r.left, dy = e.clientY - r.top;
    function di(ev) { vt = { x: ev.clientX - dx, y: ev.clientY - dy }; datViTri(); }
    function xong() { D.removeEventListener("pointermove", di); D.removeEventListener("pointerup", xong); if (vt) luu("vt", JSON.stringify(vt)); }
    D.addEventListener("pointermove", di); D.addEventListener("pointerup", xong);
  }

  /* ---------- đọc khung chat ---------- */
  function bongAi() {
    var ds = D.querySelectorAll("#chatArea .msg-tisa .bubble");
    return ds.length ? ds[ds.length - 1] : null;
  }
  function buocAi() {
    var ds = D.querySelectorAll("#chatArea .msg-steps");
    return ds.length ? String(ds[ds.length - 1].innerText || "").replace(/\s+/g, " ").trim().slice(0, 160) : "";
  }
  function chuanVb(t) { return String(t || "").replace(/\n{3,}/g, "\n\n").trim(); }

  /* ---------- gửi tin và mic ---------- */
  function guiVaoChat(text) {
    var i = D.getElementById("chatInput"), b = D.getElementById("sendBtn");
    if (!i || !b) { tt("Chưa gửi được: khung chat chưa sẵn sàng. Anh bấm Mở khung chat.", true); return false; }
    var nhap = String(i.value || "");
    i.value = text; i.dispatchEvent(new Event("input", { bubbles: true }));
    setTimeout(function () { b.click(); setTimeout(function () { if (!String(i.value || "").trim() && nhap) { i.value = nhap; i.dispatchEvent(new Event("input", { bubbles: true })); } }, 700); }, 150);
    return true;
  }
  function gui() {
    var o = D.getElementById("tlnIn"), t = String(o.value || "").trim();
    if (!t) return;
    if (guiVaoChat(t)) { o.value = ""; tt("Đã gửi cho TISA BOT.", false); lanCuoi.luc = Date.now(); }
  }
  function tt(t, loi) { var e = D.getElementById("tlnTt"); if (e) { e.textContent = t || ""; e.className = "tln-tt" + (loi ? " loi" : ""); } }
  /* ---------- gọi điện: dùng đúng nút Đàm thoại của khung chat ---------- */
  function dangGoi() {
    var b = D.getElementById("voiceBtn");
    return !!(b && (b.classList.contains("handsfree") || b.classList.contains("in-call")));
  }
  function goi() {
    var b = D.getElementById("voiceBtn");
    if (!b) { tt("Chưa gọi được: khung chat chưa sẵn sàng. Anh bấm Mở khung chat.", true); return; }
    if (!dangGoi()) goiTuDay = true;
    b.click();
    tt("", false);
    setTimeout(goiVe, 600); setTimeout(goiVe, 2000);
  }
  function goiVe() {
    var n = D.getElementById("tlnGoi"); if (!n) return;
    var g = dangGoi();
    n.textContent = g ? "📵 Cúp máy" : "📞 Gọi TISA BOT";
    n.classList.toggle("dang", g);
    if (!g) goiTuDay = false;
    var cb = D.getElementById("callBar"), tx = g && cb ? String(cb.innerText || "").replace(/\s+/g, " ").trim().slice(0, 80) : "";
    var e = D.getElementById("tlnTt");
    if (e && !/loi/.test(e.className)) e.textContent = g ? ("Đang gọi" + (tx ? " · " + tx : "") + ". Anh cứ nói, bấm Cúp máy khi xong.") : (e.textContent && /^Đang gọi/.test(e.textContent) ? "" : e.textContent);
  }

  /* ---------- vòng cập nhật ---------- */
  function veNk(ds) {
    var h = (ds || []).slice(-5).reverse().map(function (x) {
      var g = String(x.t || "").slice(11, 16);
      return "<div><time>" + esc(g) + "</time><span>" + esc((x.mo_ta || x.ten || x.op || "") + (x.host ? " (" + x.host + ")" : "")) + (x.ket_qua ? " · " + esc(x.ket_qua) : "") + "</span></div>";
    }).join("");
    D.getElementById("tlnNk").innerHTML = h ? "<b style='font-size:12px;color:inherit'>Việc vừa làm</b>" + h : "";
  }
  function veNguoi(s) {
    var o = D.getElementById("tlnNguoi"), h = "";
    var cn = s && s.cho_nguoi, cd = (s && s.cho_duyet) || [];
    if (cn) h += "<div class='tln-nguoi'><b>👉 Anh cần làm</b>" + esc(cn.ly_do || "") + "<div class='tln-hang'><button type='button' class='tln-nut chinh' data-tln='xong'>Em làm xong rồi</button></div></div>";
    cd.forEach(function (x) {
      h += "<div class='tln-nguoi'><b>AI xin duyệt</b>" + esc(x.mo_ta || "") + (x.ten ? " · nút " + esc(x.ten) : "") + "<div class='tln-hang'><button type='button' class='tln-nut chinh' data-tln='duyet' data-id='" + esc(x.id) + "'>Duyệt</button><button type='button' class='tln-nut' data-tln='tuchoi' data-id='" + esc(x.id) + "'>Không</button></div></div>";
    });
    if (o.getAttribute("data-k") !== h) { o.innerHTML = h; o.setAttribute("data-k", h); }
    return !!(cn || cd.length);
  }
  function lam() {
    if (!mo || !el) return;
    api("/trinh-duyet/trang-thai?nhe=1").then(function (s) {
      var can = veNguoi(s || {});
      veNk((s && s.nhat_ky) || []);
      var b = bongAi(), text = b ? chuanVb(b.innerText) : "", steps = buocAi(), now = Date.now();
      if (text && text !== lanCuoi.text) { lanCuoi.text = text; lanCuoi.luc = now; }
      if (steps !== lanCuoi.steps) { lanCuoi.steps = steps; lanCuoi.luc = now; }
      var nkMoi = JSON.stringify(((s && s.nhat_ky) || []).slice(-1)); if (nkMoi !== lanCuoi.nk) { lanCuoi.nk = nkMoi; lanCuoi.luc = now; }
      if (text && text !== lanCuoi.goc) { D.getElementById("tlnAiText").textContent = text.length > 900 ? "…" + text.slice(-900) : text; var a = D.getElementById("tlnAi"); a.scrollTop = a.scrollHeight; }
      var lamDang = now - lanCuoi.luc < 12000;
      var tr = D.getElementById("tlnTrang"), ch = D.getElementById("tlnCham");
      tr.textContent = can ? "Đang chờ anh làm" : lamDang ? (steps ? "Đang làm · " + steps : "Đang làm") : "Đang chờ anh nhắn";
      ch.className = "tln-cham" + (can ? " cho" : lamDang ? " lam" : "");
      pill.classList.toggle("cho", can); D.getElementById("tlnPillT").textContent = can ? "Trợ lý đang chờ anh" : "Trợ lý đang hỗ trợ";
      goiVe();
      hienTheoTrang();
    });
  }
  // Ở trang chat thì ẩn (khung chat đã hiện đủ), sang trang khác thì hiện lại.
  function hienTheoTrang() {
    var tren = false;
    try { tren = W.Alpine && Alpine.store("nav").active === "chat"; } catch (e) {}
    if (!mo || tren) { el.hidden = true; pill.hidden = true; return; }
    el.hidden = thu; pill.hidden = !thu;
    if (!thu) datViTri();
  }
  function hien() { hienTheoTrang(); lam(); }

  function bam(e) {
    var t = e.target.closest && e.target.closest("[data-tln]");
    if (!t) return;
    var k = t.getAttribute("data-tln");
    if (k === "dong") { mo = false; if (goiTuDay && dangGoi()) { try { D.getElementById("voiceBtn").click(); } catch (x) {} } goiTuDay = false; hienTheoTrang(); clearInterval(tim); tim = null; }
    else if (k === "thu") { thu = true; hienTheoTrang(); }
    else if (k === "gui") gui();
    else if (k === "goi") goi();
    else if (k === "chat") { try { Alpine.store("nav").go("chat"); } catch (x) {} }
    else if (k === "dung") { t.disabled = true; Promise.all([api("/trinh-duyet/dung", {}), api("/may-ai/dung", {})]).then(function () { t.disabled = false; tt("Đã dừng AI. Muốn làm tiếp thì nhắn cho em.", false); lam(); }); }
    else if (k === "xong") { t.disabled = true; api("/trinh-duyet/nguoi-xong", {}).then(function () { tt("Em báo AI là anh làm xong rồi.", false); lam(); }); }
    else if (k === "duyet" || k === "tuchoi") { api("/trinh-duyet/duyet", { id: t.getAttribute("data-id"), ok: k === "duyet" }).then(function () { lam(); }); }
  }

  /* ---------- gọi từ ngoài ---------- */
  function bat(ten) {
    dungKhung();
    tieuDe = String(ten || "Hỗ trợ cài đặt").slice(0, 60);
    D.getElementById("tlnTieu").textContent = "TISA BOT hỗ trợ: " + tieuDe;
    mo = true; thu = false; lanCuoi = { text: "", luc: Date.now(), nk: "", steps: "", goc: "" };
    var a = bongAi(); lanCuoi.goc = a ? chuanVb(a.innerText) : "";   // câu cũ của cuộc trò chuyện trước không tính là "AI vừa nói"
    D.getElementById("tlnAiText").textContent = "Em đang bắt đầu, anh chờ em một chút nhé.";
    tt("", false); hien();
    if (!tim) tim = setInterval(lam, 1500);
    if (!bat.theoDoi) { bat.theoDoi = true; setInterval(function () { if (mo && el) hienTheoTrang(); }, 800); }
  }
  W.TISATroLyNoi = { bat: bat, dong: function () { mo = false; if (el) hienTheoTrang(); }, gui: guiVaoChat };
})();
