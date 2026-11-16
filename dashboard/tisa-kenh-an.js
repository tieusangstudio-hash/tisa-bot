/* tisa-kenh-an.js - ẨN BỚT FANPAGE, NICK KHÔNG DÙNG ở Chatbot (V2.91).
   Kéo Facebook về có thể ra hàng chục Fanpage (chủ có 47) mà chatbot chỉ trả lời vài trang. Ở đây chọn trang nào HIỆN, trang nào ẨN.
   Ẩn chỉ là không hiển thị trong danh sách kênh, bộ chọn kênh và danh sách hội thoại "Tất cả kênh"; không xoá, không tắt bot, không đổi gì ở
   Facebook. Danh sách ẩn lưu trên máy chủ TISA BOT (server/tisa_kenh_an.py), có bản nhớ tạm trong trình duyệt. Không dùng ký tự em dash. */
(function () {
  "use strict";
  var KEY = "tisa.kenh.an", an = {}, tat = [], dangMo = null;
  function doc() { try { return JSON.parse(localStorage.getItem(KEY) || "[]") || []; } catch (e) { return []; } }
  function luuTam() { try { localStorage.setItem(KEY, JSON.stringify(Object.keys(an))); } catch (e) {} }
  doc().forEach(function (k) { an[k] = 1; });
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function soAn() { return Object.keys(an).length; }
  function bao() { try { window.dispatchEvent(new CustomEvent("tisa-kenh-an-doi")); } catch (e) {} }

  function dongBo() {
    fetch("/tisa-kenh/an", { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j.ok || !Array.isArray(j.an)) return;
      var moi = {}; j.an.forEach(function (k) { moi[k] = 1; });
      var khac = JSON.stringify(Object.keys(moi).sort()) !== JSON.stringify(Object.keys(an).sort());
      an = moi; luuTam();
      if (khac) bao();
    }).catch(function () {});
  }
  function ghiMayChu() {
    luuTam();
    return fetch("/tisa-kenh/an", { method: "POST", credentials: "same-origin", headers: { "content-type": "application/json" }, body: JSON.stringify({ an: Object.keys(an) }) }).catch(function () {});
  }

  function xemDS() { return tat.slice(); }
  var api = {
    /* gọi từ conversations.js khi nhận danh sách tài khoản kênh: nhớ cả danh sách đầy đủ, trả danh sách đang hiện */
    loc: function (ds) {
      tat = (ds || []).slice();
      return tat.filter(function (a) { return !an[a.account_key]; });
    },
    /* danh sách hội thoại "Tất cả kênh": khi có trang bị ẩn thì chỉ lấy hội thoại của các trang đang hiện */
    qs: function (st, tk) {
      if (!soAn() || (st.accs && st.accs.length)) return st;
      var keys = (tk || []).map(function (a) { return a.account_key; });
      if (!keys.length) return st;
      var o = {}; for (var k in st) o[k] = st[k];
      o.accs = keys; return o;
    },
    nut: function () {
      var n = soAn();
      return '<button type="button" class="s-btn-ghost kn-an-nut" data-kenh-an>Chọn page hiển thị' + (n ? " (" + n + " đang ẩn)" : "") + "</button>";
    },
    nutNho: function () {
      var n = soAn();
      return '<button type="button" class="ib-link kn-an-nut-nho" data-kenh-an>Ẩn bớt page' + (n ? " (" + n + ")" : "") + "</button>";
    },
    mo: function () { mo(); },
    soAn: soAn
  };
  window.TISAKenhAn = api;

  var TEN_KENH = { facebook: "Facebook / Messenger", messenger: "Messenger", zalo: "Zalo", zalo_personal: "Zalo cá nhân", telegram: "Telegram", instagram: "Instagram" };
  function css() {
    if (document.getElementById("kenhAnCss")) return;
    var s = document.createElement("style"); s.id = "kenhAnCss";
    s.textContent = ".kn-an-nut{width:100%;margin:6px 0 8px}.kn-an-nut-nho{margin-right:auto}" +
      ".kan-nen{position:fixed;inset:0;z-index:2000;background:rgba(15,18,35,.5);display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".kan-hop{background:var(--surface,#fff);color:var(--text,#172033);border:1px solid var(--border,#e3e8f3);border-radius:16px;width:min(560px,100%);max-height:86vh;display:flex;flex-direction:column;box-shadow:0 30px 80px -20px rgba(0,0,0,.5)}" +
      ".kan-dau{padding:16px 18px 8px}.kan-dau h3{margin:0 0 2px;font-size:17px}.kan-dau p{margin:0;font-size:13px;opacity:.7}" +
      ".kan-lenh{display:flex;flex-wrap:wrap;gap:6px;padding:6px 18px 10px}.kan-lenh button{padding:5px 11px;border-radius:999px;border:1px solid var(--border,#e3e8f3);background:transparent;color:inherit;font:inherit;font-size:12.5px;cursor:pointer}" +
      ".kan-lenh button:hover{border-color:#5b7cff}.kan-tim{margin:0 18px 8px;padding:8px 12px;border:1px solid var(--border,#e3e8f3);border-radius:10px;background:transparent;color:inherit;font:inherit}" +
      ".kan-ds{overflow:auto;padding:0 8px;flex:1;min-height:120px}.kan-nhom{padding:8px 10px 2px;font-size:12px;font-weight:700;opacity:.65;text-transform:uppercase;letter-spacing:.04em}" +
      ".kan-hang{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:10px;cursor:pointer}.kan-hang:hover{background:rgba(91,124,255,.08)}" +
      ".kan-hang b{display:block;font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.kan-hang small{display:block;opacity:.65;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" +
      ".kan-hang .kan-t{flex:1;min-width:0}.kan-hang.an-di b{opacity:.55;text-decoration:line-through}" +
      ".kan-cong{flex:none;width:38px;height:22px;border-radius:999px;background:#c7ccda;position:relative;transition:background .15s}.kan-cong::after{content:'';position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:left .15s}" +
      ".kan-hang input:checked+.kan-cong{background:#22c55e}.kan-hang input:checked+.kan-cong::after{left:19px}.kan-hang input{position:absolute;opacity:0;pointer-events:none}" +
      ".kan-chan{display:flex;align-items:center;gap:10px;padding:12px 18px;border-top:1px solid var(--border,#e3e8f3)}.kan-chan .kan-dem{flex:1;font-size:13px;opacity:.8}" +
      ".kan-chan button{padding:8px 16px;border-radius:10px;border:0;background:#172f72;color:#fff;font:inherit;font-weight:600;cursor:pointer}";
    document.head.appendChild(s);
  }

  function ve(hop) {
    var q = (hop.querySelector(".kan-tim") || {}).value || "", qq = q.toLowerCase();
    var ds = xemDS().filter(function (a) { return !qq || String(a.label || "").toLowerCase().indexOf(qq) >= 0 || String(a.bot_name || "").toLowerCase().indexOf(qq) >= 0; });
    var order = []; ds.forEach(function (a) { if (order.indexOf(a.channel) < 0) order.push(a.channel); });
    var h = "";
    order.forEach(function (ch) {
      h += '<div class="kan-nhom">' + esc(TEN_KENH[ch] || ch) + "</div>";
      ds.filter(function (a) { return a.channel === ch; }).forEach(function (a) {
        var hien = !an[a.account_key];
        h += '<label class="kan-hang' + (hien ? "" : " an-di") + '"><span class="kan-t"><b>' + esc(a.label || a.account_key) + "</b><small>" + esc(a.bot_name ? "A.I.: " + a.bot_name : "Chưa có A.I.") + "</small></span>" +
          '<input type="checkbox" data-k="' + esc(a.account_key) + '"' + (hien ? " checked" : "") + '><span class="kan-cong"></span></label>';
      });
    });
    hop.querySelector(".kan-ds").innerHTML = h || '<p style="padding:14px;opacity:.7">Không có trang nào khớp.</p>';
    var tong = xemDS().length, dang = xemDS().filter(function (a) { return !an[a.account_key]; }).length;
    hop.querySelector(".kan-dem").textContent = "Đang hiện " + dang + " trên " + tong + " trang";
  }
  function mo() {
    css(); if (dangMo) dangMo.remove();
    var nen = document.createElement("div"); nen.className = "kan-nen"; dangMo = nen;
    nen.innerHTML = '<div class="kan-hop" role="dialog" aria-modal="true" aria-label="Chọn page hiển thị"><div class="kan-dau"><h3>Chọn page hiển thị</h3><p>Bật công tắc cho trang anh dùng, tắt trang không dùng để danh sách gọn. Chỉ ẩn khỏi danh sách, không xoá và không tắt bot; hiện lại bất cứ lúc nào.</p></div>' +
      '<div class="kan-lenh"><button type="button" data-kan="co-bot">Chỉ hiện trang đang có A.I. trực</button><button type="button" data-kan="hien-het">Hiện tất cả</button><button type="button" data-kan="an-het">Ẩn tất cả</button></div>' +
      '<input type="search" class="kan-tim" placeholder="Tìm trang theo tên hoặc bot" aria-label="Tìm trang"><div class="kan-ds"></div>' +
      '<div class="kan-chan"><span class="kan-dem"></span><button type="button" data-kan="xong">Xong</button></div></div>';
    document.body.appendChild(nen);
    var hop = nen.firstChild; ve(hop);
    if (!xemDS().length) hop.querySelector(".kan-ds").innerHTML = '<p style="padding:14px;opacity:.7">Chưa có danh sách trang. Mở tab Hội thoại hoặc Kênh một lần rồi mở lại.</p>';
    function dong() { nen.remove(); dangMo = null; ghiMayChu().then(bao); }
    nen.addEventListener("click", function (e) {
      if (e.target === nen) { dong(); return; }
      var b = e.target.closest("[data-kan]"); if (!b) return;
      var v = b.getAttribute("data-kan");
      if (v === "xong") { dong(); return; }
      if (v === "hien-het") an = {};
      else if (v === "an-het") xemDS().forEach(function (a) { an[a.account_key] = 1; });
      else if (v === "co-bot") { an = {}; xemDS().forEach(function (a) { if (!a.bot_id && !a.bot_name) an[a.account_key] = 1; }); }
      ve(hop);
    });
    nen.addEventListener("change", function (e) {
      var c = e.target.closest("input[data-k]"); if (!c) return;
      if (c.checked) delete an[c.getAttribute("data-k")]; else an[c.getAttribute("data-k")] = 1;
      ve(hop);
    });
    nen.addEventListener("input", function (e) { if (e.target.classList.contains("kan-tim")) ve(hop); });
    document.addEventListener("keydown", function esc_(e) { if (e.key === "Escape" && dangMo) { dong(); document.removeEventListener("keydown", esc_); } });
  }
  document.addEventListener("click", function (e) { var b = e.target.closest && e.target.closest("[data-kenh-an]"); if (b) { e.preventDefault(); e.stopPropagation(); mo(); } }, true);
  dongBo();
})();
