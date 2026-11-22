/* tisa-tro-ly-noi.js - Cửa sổ trợ lý NỔI khi TISA BOT hỗ trợ cài đặt, kết nối (V3.04, chủ yêu cầu 17/11/2026).

   Vấn đề: bấm "Kết nối tự động" thì TISA BOT tự mở trang Kết nối và hộp nhập mã, che mất khung chat nên anh không thấy AI nói gì,
   không ra lệnh được, không bật mic được. Cửa sổ này nổi trên MỌI trang và hộp thoại:
     - báo AI đang làm tới đâu (câu mới nhất của AI, các việc vừa làm trong trình duyệt);
     - hiện thẻ "Anh cần làm" khi AI chờ anh (đăng nhập, bấm Cho phép...) kèm nút "Em làm xong rồi";
     - ô chat để gõ với AI, và nút GỌI: dùng đúng tính năng gọi điện nói chuyện qua lại của khung chat (#voiceBtn), không có mic hay đọc to riêng;
     - nút Dừng AI ngay, thu nhỏ, kéo đi chỗ khác.
   V3.05: khi đang gọi, cửa sổ này đưa lời báo của phần đang làm, việc anh cần làm và việc xin duyệt cho GIỌNG GỌI đọc (keDoc), nên chỉ có một giọng hướng dẫn.
   Không có khung chat riêng: dùng chính khung chat của TISA BOT (#chatInput, #sendBtn, #chatArea) nên lời nói nằm trong cùng một cuộc trò chuyện. */
(function () {
  "use strict";
  var W = window, D = document;
  var el = null, pill = null, tim = null, mo = false, thu = false, ep = false, tieuDe = "Hỗ trợ cài đặt";
  var lanCuoi = { text: "", luc: 0, nk: "", steps: "" }, goiTuDay = false;
  var daDoc = "", daDocNguoi = "", daDocDuyet = {}, daChao = false, canNguoi = false, dungNow = false;
  var vt = null;      // vị trí đã kéo

  var CSS = [
    ".tln{position:fixed;right:16px;bottom:16px;z-index:2147483200;width:min(560px,calc(100vw - 24px));height:min(860px,calc(100vh - 24px));max-height:calc(100vh - 24px);display:flex;flex-direction:column;border-radius:18px;background:var(--mm-base,#fff);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,rgba(23,47,114,.18));box-shadow:0 24px 70px -18px rgba(8,16,48,.55);font:14px/1.5 inherit;overflow:hidden}",
    ".tln[hidden]{display:none}",
    ".tln-dau{display:flex;align-items:center;gap:10px;padding:10px 12px;background:linear-gradient(135deg,var(--tisa-nhan,#ff6b35),var(--tisa-chinh,#172f72));color:#fff;cursor:grab;user-select:none;touch-action:none}",
    ".tln-dau b{flex:1;min-width:0;font-size:14px;line-height:1.25}.tln-dau small{display:block;font-weight:500;opacity:.85;font-size:12px}",
    ".tln-cham{flex:none;width:10px;height:10px;border-radius:50%;background:#9aa6d6}.tln-cham.lam{background:#4ade80;animation:tlnNhip 1.4s infinite}.tln-cham.cho{background:#fbbf24}",
    "@keyframes tlnNhip{0%,100%{opacity:1}50%{opacity:.35}}",      /* chỉ đổi độ trong suốt (card đồ họa lo): vòng box-shadow cũ bắt vẽ lại 60 lần/giây, chồng lên lớp làm mờ nền thì chớp (22/11/2026) */
    ".tln-nut-dau{flex:none;border:0;background:rgba(255,255,255,.18);color:#fff;width:28px;height:28px;border-radius:8px;cursor:pointer;font-size:15px;line-height:1}.tln-nut-dau:hover{background:rgba(255,255,255,.32)}",
    ".tln-than{flex:1 1 auto;overflow:auto;padding:12px;display:grid;gap:10px;min-height:200px;align-content:start;overscroll-behavior:contain}",
    ".tln.to{width:min(900px,calc(100vw - 24px));height:calc(100vh - 24px)}.tln-nut-dau.to{font-size:13px}",
    ".tln-nguoi{font-size:15px;padding:11px 12px;border-radius:12px;border:1.5px solid #f59e0b;background:rgba(245,158,11,.12)}.tln-nguoi b{display:block;margin-bottom:4px;color:#b45309}",
    ".tln-nguoi .tln-hang{margin-top:8px}",
    ".tln-ai{padding:10px 12px;border-radius:12px;background:var(--mm-soft,#f1f4fb);white-space:pre-wrap;word-break:break-word;font-size:15px}",
    ".tln-anh{padding:8px 12px;border-radius:12px;background:rgba(255,107,53,.10);border:1px solid rgba(255,107,53,.35);font-size:14.5px;word-break:break-word;white-space:pre-wrap}.tln-anh small{display:block;color:var(--mm-muted,#5b6478);margin-bottom:2px;font-weight:600}",
    ".tln-chrome{display:flex;align-items:center;gap:8px;padding:6px 12px;font-size:12.5px;border-bottom:1px solid var(--mm-line,rgba(23,47,114,.12))}.tln-chrome span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.tln-chrome.chua span{color:#b45309;font-weight:700}.tln-chrome button{flex:none;border:1px solid var(--mm-line2,rgba(23,47,114,.25));background:var(--mm-soft,#f1f4fb);color:inherit;border-radius:8px;padding:3px 10px;font:700 12px inherit;cursor:pointer}",
    ".tln-ai small{display:block;color:var(--mm-muted,#5b6478);margin-bottom:4px;font-weight:600}",
    ".tln-nk{display:grid;gap:3px;font-size:12.5px;color:var(--mm-muted,#5b6478)}.tln-nk div{display:flex;gap:6px}.tln-nk time{flex:none;opacity:.8}",
    ".tln-hang{display:flex;gap:8px;flex-wrap:wrap;align-items:center}",
    ".tln-nut{border:1px solid var(--mm-line2,rgba(23,47,114,.2));background:var(--mm-soft,#f1f4fb);color:inherit;border-radius:10px;padding:0 12px;min-height:34px;font:600 13px/1 inherit;cursor:pointer}.tln-nut:hover{filter:brightness(.96)}",
    ".tln-nut.chinh{background:var(--tisa-nhan,#ff6b35);border-color:var(--tisa-nhan,#ff6b35);color:#fff}.tln-nut.do{background:#d93025;border-color:#d93025;color:#fff}.tln-nut:disabled{opacity:.5;cursor:default}",
    ".tln-tep{display:flex;gap:10px;flex-wrap:wrap;padding:8px 12px 2px;border-top:1px solid var(--mm-line,rgba(23,47,114,.12))}.tln-tep[hidden]{display:none}",
    ".tln-t{position:relative;width:64px;height:64px;border-radius:10px;border:1px solid var(--mm-line2,rgba(23,47,114,.25));background:var(--mm-soft,#f1f4fb) center/cover no-repeat;overflow:hidden;font-size:10.5px;line-height:1.2;color:var(--mm-muted,#5b6478)}.tln-t span{display:block;padding:4px;word-break:break-all}",
    ".tln-t.tai{opacity:.5}.tln-t.loi{border-color:#d93025}.tln-t button{position:absolute;top:2px;right:2px;width:20px;height:20px;border-radius:50%;border:0;background:rgba(23,32,51,.82);color:#fff;font-size:11px;line-height:1;cursor:pointer;padding:0}",
    ".tln-chat .tln-clip{flex:none;min-width:38px;height:38px;padding:0;font-size:17px}",
    ".tln-chat{display:flex;gap:6px;align-items:center;padding:8px 10px 4px;border-top:1px solid var(--mm-line,rgba(23,47,114,.12))}",
    ".tln-chat input[type=text]{flex:1 1 auto;min-width:0;height:38px;border-radius:10px;border:1px solid var(--mm-line2,rgba(23,47,114,.22));background:var(--mm-base,#fff);color:inherit;padding:0 10px;font:inherit}",
    ".tln-chan{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px 10px 10px;border-top:1px solid var(--mm-line,rgba(23,47,114,.12))}",
    ".tln-chan .tln-nut{width:100%;padding:0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
    ".tln-nut.goi{background:#16a34a;border-color:#16a34a;color:#fff}.tln-nut.goi.dang{background:#d93025;border-color:#d93025}",
    ".tln-tt{padding:0 12px 8px;font-size:12.5px;color:var(--mm-muted,#5b6478)}.tln-tt.loi{color:#d93025}",
    ".tln-pill{position:fixed;right:16px;bottom:16px;z-index:2147483200;display:flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;border:0;background:linear-gradient(135deg,var(--tisa-nhan,#ff6b35),var(--tisa-chinh,#172f72));color:#fff;font:700 13.5px/1 inherit;cursor:pointer;box-shadow:0 14px 40px -12px rgba(8,16,48,.6)}",
    ".tln-pill[hidden]{display:none}",
    ".tln-pill.cho{animation:tlnPill 1s infinite alternate}@keyframes tlnPill{to{transform:scale(1.06)}}",
    "@media (prefers-reduced-motion:reduce){.tln-cham.lam,.tln-pill.cho{animation:none}}",
    "@media (max-width:640px){.tln{right:8px;left:8px;bottom:calc(8px + env(safe-area-inset-bottom));width:auto;max-height:min(80vh,calc(100dvh - 24px))}",
    ".tln-nut-dau{width:40px;height:40px;font-size:18px}.tln-nk{display:none}.tln-than{min-height:90px}",
    ".tln-nut{min-height:46px;font-size:14px}.tln-chat input[type=text]{height:46px;font-size:16px}.tln-chan{padding-bottom:calc(10px + env(safe-area-inset-bottom))}",
    ".tln-pill{bottom:calc(16px + env(safe-area-inset-bottom));min-height:46px}}"
  ].join("");

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(url, body) {
    var o = { method: body === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store" };
    if (body !== undefined) { o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(body); }
    return fetch(url, o).then(function (r) { return r.json(); }).catch(function () { return null; });
  }
  /* V3.20 (chủ báo 18/11/2026): cửa sổ nổi không được tự mất khi anh qua trang khác hay tải lại trang lúc đang trao đổi, vì anh còn cần nó để trao đổi, bấm gọi hoặc tắt.
     Trạng thái (đang mở, đang thu nhỏ, tên) được nhớ trong trình duyệt và khôi phục khi trang nạp lại; chỉ biến mất khi anh bấm ✕. */
  function nhoTrangThai() { luu("st", JSON.stringify({ mo: mo, thu: thu, ten: tieuDe, luc: Date.now() })); }
  function luu(k, v) { try { W.localStorage.setItem("tln_" + k, v); } catch (e) {} }
  function doc(k) { try { return W.localStorage.getItem("tln_" + k); } catch (e) { return null; } }

  function dungKhung() {
    if (el) return;
    var st = D.createElement("style"); st.id = "tln-css"; st.textContent = CSS; (D.head || D.documentElement).appendChild(st);
    el = D.createElement("div"); el.className = "tln"; el.id = "tisaTroLyNoi"; el.setAttribute("role", "dialog"); el.setAttribute("aria-label", "Trợ lý hỗ trợ cài đặt"); el.hidden = true;
    el.innerHTML = "<div class='tln-dau' id='tlnDau'><i class='tln-cham' id='tlnCham'></i><b><span id='tlnTieu'></span><small id='tlnTrang'>Đang chờ</small></b>" +
      "<button type='button' class='tln-nut-dau to' data-tln='cd' title='Cài đặt mô hình và mức nỗ lực của trợ lý đấu nối' aria-label='Cài đặt trợ lý'>⚙</button><button type='button' class='tln-nut-dau to' data-tln='to' id='tlnTo' title='Phóng to / thu về' aria-label='Phóng to'>⤢</button><button type='button' class='tln-nut-dau' data-tln='thu' title='Thu nhỏ' aria-label='Thu nhỏ'>–</button><button type='button' class='tln-nut-dau' data-tln='dong' title='Đóng' aria-label='Đóng'>✕</button></div>" +
      "<div class='tln-chrome' id='tlnChrome'><span id='tlnChromeT'>Chrome: đang kiểm tra...</span><button type='button' data-tln='chrome'>Đổi</button></div>" +
      "<div class='tln-than'><div id='tlnNguoi'></div><div class='tln-anh' id='tlnAnh' hidden></div><div class='tln-ai' id='tlnAi'><small>TISA BOT nói</small><span id='tlnAiText'>Em đang bắt đầu, anh chờ em một chút nhé.</span></div><div class='tln-nk' id='tlnNk'></div></div>" +
      "<div class='tln-tt' id='tlnTt'></div>" +
      "<div class='tln-tep' id='tlnTep' hidden></div><div class='tln-chat'><button type='button' class='tln-nut tln-clip' data-tln='anh' title='Đính kèm hình hoặc tệp (cũng dán được bằng Ctrl+V, hoặc kéo thả vào đây)' aria-label='Đính kèm hình'>📎</button>" +
      "<input type='text' id='tlnIn' placeholder='Gõ hoặc dán hình (Ctrl+V)...' autocomplete='off'><button type='button' class='tln-nut chinh' data-tln='gui'>Gửi</button></div>" +
      "<div class='tln-chan'><button type='button' class='tln-nut goi' id='tlnGoi' data-tln='goi' title='Gọi điện nói chuyện qua lại với TISA BOT'>📞 Gọi</button><button type='button' class='tln-nut' data-tln='chat' title='Mở khung chat'>💬 Khung chat</button><button type='button' class='tln-nut do' data-tln='dung' title='Dừng AI ngay'>⏹ Dừng AI</button></div>";
    D.body.appendChild(el);
    pill = D.createElement("button"); pill.type = "button"; pill.className = "tln-pill"; pill.hidden = true; pill.innerHTML = "<span>🤖</span><span id='tlnPillT'>Trợ lý đang hỗ trợ</span>";
    pill.addEventListener("click", function () { thu = false; ep = true; nhoTrangThai(); hien(); });
    D.body.appendChild(pill);
    var dau = D.getElementById("tlnDau");
    dau.addEventListener("pointerdown", batDauKeo);
    el.addEventListener("click", bam);
    D.getElementById("tlnIn").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); gui(); } });
    if (doc("to") === "1") el.classList.add("to");
    var v = doc("vt"); if (v) { try { vt = JSON.parse(v); } catch (e) { vt = null; } }
  }

  /* ---------- kéo thả ---------- */
  function datViTri() {
    if (!el || !vt) return;
    var w = el.offsetWidth || 380;
    var x = Math.max(4, Math.min(W.innerWidth - w - 4, vt.x)), y = Math.max(4, Math.min(W.innerHeight - Math.min(el.offsetHeight || 60, W.innerHeight - 8) - 4, vt.y));
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
    var ds = D.querySelectorAll("#chatArea .msg-tisa:not([data-live]) .bubble");   // bong bóng do cuộc gọi vẽ (data-live) không phải của phần đang làm: bỏ để khỏi đọc lại lời chính giọng gọi
    return ds.length ? ds[ds.length - 1] : null;
  }
  // Chỉ để HIỂN THỊ: gồm cả lời trả lời của cuộc gọi (data-live). Phiên gọi nói chuyện (voice-live) trả lời bằng bong bóng này, bỏ đi thì anh gõ gì cũng
  // thấy "không phản hồi" dù AI đã trả lời (chủ báo 18/11/2026). Việc ĐỌC TO vẫn dùng bongAi() ở trên để khỏi đọc lại lời của chính giọng gọi.
  function bongHienThi() {
    var ds = D.querySelectorAll("#chatArea .msg-tisa .bubble");
    return ds.length ? ds[ds.length - 1] : null;
  }
  function tinAnh() {
    var ds = D.querySelectorAll("#chatArea .msg-user");
    if (!ds.length) return { text: "", note: "" };
    var e = ds[ds.length - 1], n = e.querySelector(".steer-note"), c = e.cloneNode(true), cn = c.querySelector(".steer-note");
    if (cn) cn.remove();
    var b = c.querySelector(".bubble") || c;
    return { text: chuanVb(b.innerText || b.textContent || ""), note: n ? String(n.textContent || "").trim() : "" };
  }
  function buocAi() {
    var ds = D.querySelectorAll("#chatArea .msg-steps");
    return ds.length ? String(ds[ds.length - 1].innerText || "").replace(/\s+/g, " ").trim().slice(0, 160) : "";
  }
  function chuanVb(t) { return String(t || "").replace(/\n{3,}/g, "\n\n").trim(); }

  /* ---------- gửi tin và mic ---------- */
  function guiVaoChat(text) {
    // V3.18: gọi thẳng hàm gửi của khung chat. Đang gọi điện hay đang có lượt chạy thì nút Gửi bị khoá (bấm không ăn), tin gõ như vậy là mất.
    // Tin gõ luôn đi vào lượt đang chạy (steer), không bị xếp hàng chờ như lời nói từ mic.
    try {
      var ci = D.getElementById("chatInput");
      if (typeof W.sendMessage === "function" && ci) {
        var nhap0 = String(ci.value || "");
        W.sendMessage(text);
        if (nhap0 && !String(ci.value || "").trim()) { ci.value = nhap0; ci.dispatchEvent(new Event("input", { bubbles: true })); }   // trả lại chữ anh đang gõ dở ở khung chat
        return true;
      }
    } catch (e) {}
    var i = D.getElementById("chatInput"), b = D.getElementById("sendBtn");
    if (!i || !b) { tt("Chưa gửi được: khung chat chưa sẵn sàng. Anh bấm Mở khung chat.", true); return false; }
    var nhap = String(i.value || "");
    i.value = text; i.dispatchEvent(new Event("input", { bubbles: true }));
    setTimeout(function () { b.click(); setTimeout(function () { if (!String(i.value || "").trim() && nhap) { i.value = nhap; i.dispatchEvent(new Event("input", { bubbles: true })); } }, 700); }, 150);
    return true;
  }
  function tiepTuc() {
    return Promise.all([api("/trinh-duyet/tiep-tuc", {}), api("/may-ai/tiep-tuc", {})]).then(function () { dungNow = false; });
  }
  /* V3.24 (chủ 19/11/2026): gửi hình vào ô chat nổi để TISA BOT nhìn thấy màn hình anh đang thấy. Dán (Ctrl+V), kéo thả hoặc bấm 📎; tệp đi chung đường đính kèm của khung chat. */
  function veTep() {
    var e = D.getElementById("tlnTep"); if (!e) return;
    var A = W.TISAAttach, ds = (A && A.list && A.list()) || [];
    var sig = JSON.stringify(ds.map(function (a) { return [a.name, a.preview, !!a.uploading, !!a.loi, !!a.path]; }));
    if (sig === lanCuoi.tep) return; lanCuoi.tep = sig;
    e.hidden = !ds.length;
    e.innerHTML = ds.map(function (a, i) {
      var hong = a.loi || (!a.uploading && !a.path);
      return "<div class='tln-t" + (a.uploading ? " tai" : "") + (hong ? " loi" : "") + "' title='" + esc(a.name) + (a.uploading ? " · đang tải" : hong ? " · tải lỗi" : "") + "'" +
        (a.preview ? " style=\"background-image:url('" + esc(a.preview) + "')\"" : "") + ">" + (a.preview ? "" : "<span>" + esc(a.name) + "</span>") +
        "<button type='button' data-tln='bo' data-i='" + i + "' aria-label='Bỏ'>✕</button></div>";
    }).join("");
  }
  function gui() {
    var o = D.getElementById("tlnIn"), t = String(o.value || "").trim();
    var A = W.TISAAttach, co = !!(A && A.list && A.list().length);
    if (!t && !co) return;
    if (!t) t = "Anh gửi hình này, em xem giúp anh nhé.";
    if (dungNow) tiepTuc();   // anh nhắn việc mới thì AI được làm tiếp, không bắt anh tìm nút
    if (guiVaoChat(t)) {
      o.value = ""; tt("Đã gửi cho TISA BOT, đang chờ trả lời...", false); lanCuoi.luc = Date.now();
      setTimeout(lam, 700); setTimeout(lam, 2500); setTimeout(veTep, 300); setTimeout(veTep, 1500);
    }
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
    n.textContent = g ? "📵 Cúp máy" : "📞 Gọi";
    n.classList.toggle("dang", g);
    if (!g) goiTuDay = false;
    var cb = D.getElementById("callBar"), tx = g && cb ? String(cb.innerText || "").replace(/\s+/g, " ").trim().slice(0, 80) : "";
    var e = D.getElementById("tlnTt");
    if (e && !/loi/.test(e.className)) e.textContent = g ? ("Đang gọi" + (tx ? " · " + tx : "") + ". Anh cứ nói, bấm Cúp máy khi xong.") : (e.textContent && /^Đang gọi/.test(e.textContent) ? "" : e.textContent);
  }

  /* ---------- giọng dẫn: MỘT giọng duy nhất (V3.05, chủ báo 18/11/2026) ----------
     Đang gọi thì TISA BOT nói chuyện (ChatGPT Live) là người hướng dẫn DUY NHẤT. Phần đang làm việc (chạy ở khung chat) báo gì, cần anh làm gì,
     xin anh duyệt gì thì đưa cho giọng gọi ĐỌC (app.js docQuaLive: đọc cùng giọng, máy chủ chờ lúc im mới đọc), không để hai bên nói hai giọng,
     và bot gọi điện biết ngay việc đang làm tới đâu vì chính nó vừa nói ra. */
  function ngan(t) {
    t = String(t || "").replace(/[`*_#>|]/g, " ").replace(/\s+/g, " ").trim();
    if (t.length <= 420) return t;
    var c = t.slice(0, 420), k = Math.max(c.lastIndexOf(". "), c.lastIndexOf("! "), c.lastIndexOf("? "));
    return (k > 120 ? c.slice(0, k + 1) : c) ;
  }
  function cuoiDoan(t) { var p = String(t || "").split(/\n\s*\n/).filter(function (x) { return x.trim(); }); return p.length ? p[p.length - 1] : String(t || ""); }
  function keDoc(s, text, now) {
    var doc = W.docQuaLive;
    if (typeof doc !== "function") return;
    var cn = s && s.cho_nguoi, ly = cn ? String(cn.ly_do || "") : "";
    if (!daChao) {
      var live = W.TISAVoiceLive && W.TISAVoiceLive.isOn && W.TISAVoiceLive.isOn();
      if (!live) return;                       // chờ cuộc gọi nối xong rồi mới chào
      daChao = true; daDocNguoi = ly; daDoc = text || "";
      var v = "Em đang giúp anh việc: " + tieuDe + ".";
      if (ly) v += " Giờ anh cần làm: " + ngan(ly);
      else if (text) v += " Vừa rồi em báo: " + ngan(cuoiDoan(text));
      doc(v);
      return;
    }
    if (ly && ly !== daDocNguoi) { daDocNguoi = ly; doc("Anh làm giúp em bước này nhé: " + ngan(ly)); }
    if (!ly) daDocNguoi = "";
    ((s && s.cho_duyet) || []).forEach(function (x) {
      if (!x || daDocDuyet[x.id]) return;
      daDocDuyet[x.id] = 1;
      doc("Em đang xin anh duyệt: " + ngan(x.mo_ta || "một thao tác") + ". Anh bấm nút duyệt trên màn hình nhé.");
    });
    if (text && text !== lanCuoi.goc && text !== daDoc && now - lanCuoi.luc > 2500) {
      daDoc = text;
      var cd = cuoiDoan(text);
      if (!(ly && cd.indexOf(ly.slice(0, 30)) >= 0)) doc(ngan(cd));   // câu báo trùng với việc anh cần làm thì đã đọc ở trên
    }
  }
  // Anh NÓI "xong rồi" lúc phần đang làm chờ anh: báo cho nó làm tiếp, không bắt anh bấm nút trên cửa sổ.
  function nguoiNoi(text) {
    if (mo && dungNow && /(làm tiếp|tiếp tục|tiếp đi|làm đi|cứ làm)/.test(String(text || "").toLowerCase())) { tiepTuc().then(function () { tt("AI được làm tiếp.", false); lam(); }); return; }
    if (!mo || !canNguoi) return;
    var t = String(text || "").toLowerCase().trim();
    if (!t || t.length > 80 || /chưa|không|đâu|sao |\?|bao giờ|khi nào/.test(t)) return;   // câu hỏi ("làm tới đâu rồi", "xong chưa") không phải lời báo xong
    if (/(^|\s)(xong|được rồi|làm xong|đã làm|đã xong|ok|oke|okay|tiếp tục|làm tiếp|tiếp đi|done)(\s|$|[.,!])/.test(t)) {
      api("/trinh-duyet/nguoi-xong", {}).then(function () { tt("Em báo AI là anh làm xong rồi.", false); lam(); });
    }
  }

  /* ---------- vòng cập nhật ---------- */
  function veNk(ds) {
    var h = (ds || []).slice(-5).reverse().map(function (x) {
      var g = String(x.t || "").slice(11, 16);
      return "<div><time>" + esc(g) + "</time><span>" + esc((x.mo_ta || x.ten || x.op || "") + (x.host ? " (" + x.host + ")" : "")) + (x.ket_qua ? " · " + esc(x.ket_qua) : "") + "</span></div>";
    }).join("");
    var nk = D.getElementById("tlnNk"), moi = h ? "<b style='font-size:12px;color:inherit'>Việc vừa làm</b>" + h : "";
    if (nk.getAttribute("data-k") !== moi) { nk.innerHTML = moi; nk.setAttribute("data-k", moi); }      // chỉ dựng lại khi có việc mới: cứ 1,5 giây dựng lại một lần làm cửa sổ chớp (22/11/2026)
  }
  function veNguoi(s) {
    var o = D.getElementById("tlnNguoi"), h = "";
    var cn = s && s.cho_nguoi, cd = (s && s.cho_duyet) || [];
    dungNow = !!(s && s.dung);
    if (dungNow) h += "<div class='tln-nguoi'><b>⏸ Anh đã bấm Dừng</b>AI đang bị khóa nên chưa làm được gì. Bấm nút dưới đây để cho AI làm tiếp.<div class='tln-hang'><button type='button' class='tln-nut chinh' data-tln='tiep'>▶ Cho AI làm tiếp</button></div></div>";
    if (cn) h += "<div class='tln-nguoi'><b>👉 Anh cần làm</b>" + esc(cn.ly_do || "") + "<div class='tln-hang'><button type='button' class='tln-nut chinh' data-tln='xong'>Em làm xong rồi</button></div></div>";
    cd.forEach(function (x) {
      h += "<div class='tln-nguoi'><b>AI xin duyệt</b>" + esc(x.mo_ta || "") + (x.ten ? " · nút " + esc(x.ten) : "") + "<div class='tln-hang'><button type='button' class='tln-nut chinh' data-tln='duyet' data-id='" + esc(x.id) + "'>Duyệt</button><button type='button' class='tln-nut' data-tln='tuchoi' data-id='" + esc(x.id) + "'>Không</button></div></div>";
    });
    if (o.getAttribute("data-k") !== h) { o.innerHTML = h; o.setAttribute("data-k", h); }
    return !!(cn || cd.length || dungNow);
  }
  function lam() {
    if (!mo || !el) return;
    api("/trinh-duyet/trang-thai?nhe=1").then(function (s) {
      var can = veNguoi(s || {}); canNguoi = !!(s && s.cho_nguoi);
      veNk((s && s.nhat_ky) || []);
      var b = bongAi(), text = b ? chuanVb(b.innerText) : "", steps = buocAi(), now = Date.now();
      var bh = bongHienThi(), textHt = bh ? chuanVb(bh.innerText) : "", anh = tinAnh();
      if (textHt && textHt !== lanCuoi.ht) { lanCuoi.ht = textHt; lanCuoi.luc = now; }
      if (anh.text && anh.text !== lanCuoi.anh) { lanCuoi.anh = anh.text; lanCuoi.luc = now; }
      if (text && text !== lanCuoi.text) { lanCuoi.text = text; lanCuoi.luc = now; }
      if (steps !== lanCuoi.steps) { lanCuoi.steps = steps; lanCuoi.luc = now; }
      var nkMoi = JSON.stringify(((s && s.nhat_ky) || []).slice(-1)); if (nkMoi !== lanCuoi.nk) { lanCuoi.nk = nkMoi; lanCuoi.luc = now; }
      if (textHt && textHt !== lanCuoi.gocHt) { D.getElementById("tlnAiText").textContent = textHt.length > 900 ? "…" + textHt.slice(-900) : textHt; var a = D.getElementById("tlnAi"); a.scrollTop = a.scrollHeight; }
      var ea = D.getElementById("tlnAnh");     // tin anh vừa gửi, để thấy mình đã gửi tới nơi và AI đang đọc hay đã trả lời
      if (anh.text && anh.text !== lanCuoi.gocAnh) {
        ea.hidden = false;
        ea.innerHTML = "<small>Anh vừa nhắn" + (anh.note ? " · " + esc(anh.note) : "") + "</small>" + esc(anh.text.length > 300 ? anh.text.slice(0, 300) + "…" : anh.text);
      }
      var lamDang = now - lanCuoi.luc < 12000;
      var tr = D.getElementById("tlnTrang"), ch = D.getElementById("tlnCham");
      tr.textContent = can ? "Đang chờ anh làm" : lamDang ? (steps ? "Đang làm · " + steps : "Đang làm") : "Đang chờ anh nhắn";
      ch.className = "tln-cham" + (can ? " cho" : lamDang ? " lam" : "");
      pill.classList.toggle("cho", can); D.getElementById("tlnPillT").textContent = can ? "Trợ lý đang chờ anh" : "Trợ lý đang hỗ trợ";
      goiVe();
      if (dangGoi()) keDoc(s || {}, text, now); else daChao = false;
      hienTheoTrang();
    });
  }
  // Ở trang chat thì ẩn (khung chat đã hiện đủ), sang trang khác thì hiện lại.
  function hienTheoTrang() {
    var tren = false;
    try { tren = W.Alpine && Alpine.store("nav").active === "chat"; } catch (e) {}
    if (!mo) { el.hidden = true; pill.hidden = true; return; }
    // Trang Trò chuyện đã có khung chat đủ nên cửa sổ nổi thu thành nút nhỏ ở góc, KHÔNG biến mất: anh luôn tìm thấy nó để mở lại, bấm gọi hoặc tắt.
    var gon = thu || (tren && !ep);
    el.hidden = gon; pill.hidden = !gon;
    if (!gon) datViTri();
  }
  function veChrome() {
    if (!W.TISALayChrome || !el) return;
    W.TISALayChrome().then(function (d) {
      var e = D.getElementById("tlnChrome"), t = D.getElementById("tlnChromeT"); if (!e || !t) return;
      var c = d.chon;
      t.textContent = c ? "Chrome đang dùng: " + (c.ten || c.thu_muc) + (c.email ? " (" + c.email + ")" : "") : (d.ds.length ? "Chưa chọn Chrome: TISA BOT dùng trình duyệt riêng" : "Dùng trình duyệt riêng của TISA BOT");
      e.classList.toggle("chua", !c && d.ds.length > 0);
    });
  }
  W.addEventListener("tisa:chrome-chon", function () { veChrome(); });
  function hien() { hienTheoTrang(); lam(); veChrome(); }

  function bam(e) {
    var t = e.target.closest && e.target.closest("[data-tln]");
    if (!t) return;
    var k = t.getAttribute("data-tln");
    if (k === "dong") { mo = false; ep = false; nhoTrangThai(); if (goiTuDay && dangGoi()) { try { D.getElementById("voiceBtn").click(); } catch (x) {} } goiTuDay = false; hienTheoTrang(); clearInterval(tim); tim = null; }
    else if (k === "cd") { try { W.TISADauNoi.moCaiDat(); } catch (x) {} }
    else if (k === "to") { var b = el.classList.toggle("to"); luu("to", b ? "1" : "0"); try { datViTri(); } catch (x) {} }
    else if (k === "thu") { thu = true; ep = false; nhoTrangThai(); hienTheoTrang(); }
    else if (k === "chrome") { if (W.TISAChonChrome) W.TISAChonChrome(false).then(function () { veChrome(); }); }
    else if (k === "anh") { try { W.TISAAttach.pick(); } catch (x) { tt("Chưa chọn được tệp: khung chat chưa sẵn sàng.", true); } }
    else if (k === "bo") { try { W.TISAAttach.removeAt(Number(t.getAttribute("data-i"))); } catch (x) {} veTep(); }
    else if (k === "gui") gui();
    else if (k === "goi") goi();
    else if (k === "chat") { try { Alpine.store("nav").go("chat"); } catch (x) {} }
    else if (k === "dung") { t.disabled = true; Promise.all([api("/trinh-duyet/dung", {}), api("/may-ai/dung", {})]).then(function () { t.disabled = false; tt("Đã dừng AI. Muốn làm tiếp thì nhắn cho em.", false); lam(); }); }
    else if (k === "tiep") { t.disabled = true; tiepTuc().then(function () { tt("AI được làm tiếp. Anh nhắn em làm gì tiếp nhé.", false); lam(); }); }
    else if (k === "xong") { t.disabled = true; api("/trinh-duyet/nguoi-xong", {}).then(function () { tt("Em báo AI là anh làm xong rồi.", false); lam(); }); }
    else if (k === "duyet" || k === "tuchoi") { api("/trinh-duyet/duyet", { id: t.getAttribute("data-id"), ok: k === "duyet" }).then(function () { lam(); }); }
  }

  /* ---------- gọi từ ngoài ---------- */
  function bat(ten, khoiPhuc) {
    dungKhung();
    tieuDe = String(ten || "Hỗ trợ cài đặt").slice(0, 60);
    D.getElementById("tlnTieu").textContent = "TISA BOT hỗ trợ: " + tieuDe;
    mo = true; thu = false; lanCuoi = { text: "", luc: Date.now(), nk: "", steps: "", goc: "" }; daDoc = ""; daDocNguoi = ""; daDocDuyet = {}; daChao = false;
    var a = bongAi(); lanCuoi.goc = a ? chuanVb(a.innerText) : "";
    var h0 = bongHienThi(); lanCuoi.gocHt = h0 ? chuanVb(h0.innerText) : ""; lanCuoi.ht = lanCuoi.gocHt;
    lanCuoi.gocAnh = tinAnh().text; lanCuoi.anh = lanCuoi.gocAnh;   // câu cũ của cuộc trò chuyện trước không tính là "AI vừa nói"
    if (!khoiPhuc) D.getElementById("tlnAiText").textContent = "Em đang bắt đầu, anh chờ em một chút nhé.";
    else if (h0) D.getElementById("tlnAiText").textContent = chuanVb(h0.innerText).slice(-900);
    tt("", false); nhoTrangThai(); hien();
    if (!tim) tim = setInterval(lam, 1500);
    if (!bat.theoDoi) { bat.theoDoi = true; setInterval(function () { if (mo && el) { hienTheoTrang(); veTep(); } }, 800); }
  }
  function khoiPhuc() {
    var j = null;
    try { j = JSON.parse(doc("st") || "null"); } catch (e) {}
    if (!j || !j.mo || Date.now() - (j.luc || 0) > 12 * 3600 * 1000) return;
    bat(j.ten || "Hỗ trợ cài đặt", true);
    thu = !!j.thu; hienTheoTrang();
  }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", function () { setTimeout(khoiPhuc, 400); });
  else setTimeout(khoiPhuc, 400);
  setInterval(function () { if (mo) nhoTrangThai(); }, 60000);          // còn đang mở thì giữ trạng thái "mới", không hết hạn khi anh để lâu
  W.TISATroLyNoi = { nguoiNoi: nguoiNoi, bat: bat, dong: function () { mo = false; ep = false; nhoTrangThai(); if (el) hienTheoTrang(); }, gui: guiVaoChat };
})();
