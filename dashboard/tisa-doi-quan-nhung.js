/* tisa-doi-quan-nhung.js - chạy TRONG trang Đội Quân AI khi mở qua /doiquanagent (tisa_giao_dien.py chèn vào).
   1. Mã bảng gọi máy chủ bằng đường dẫn tuyệt đối: thêm tiền tố cho những chỗ máy chủ chưa kịp đổi trong mã.
   2. Nằm trong khung TISA BOT: theo tông sáng/tối của TISA BOT, bỏ nút đăng xuất và nút đổi tông riêng của bảng.
   3. "Chat nội bộ" mở khung chat Cộng Sự của TISA BOT: hai bên vốn là một cuộc trò chuyện, giờ dùng chung một giao diện. */
(function () {
  "use strict";
  var BASE = window.__DQ_BASE || "/doiquanagent";
  var DUONG = ["/api/", "/_blob/", "/kit.js", "/tisa-model.js"];
  function doi(u) {
    if (typeof u !== "string" || u.indexOf(BASE + "/") === 0) return u;
    for (var i = 0; i < DUONG.length; i++) if (u.indexOf(DUONG[i]) === 0) return BASE + u;
    return u;
  }
  var _fetch = window.fetch;
  window.fetch = function (input, init) {
    if (typeof input === "string") input = doi(input);
    else if (input && input.url && input.url.indexOf(location.origin + "/") === 0) {
      var p = input.url.slice(location.origin.length);
      if (doi(p) !== p) input = new Request(location.origin + doi(p), input);
    }
    return _fetch.call(this, input, init);
  };
  var _open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) {
    arguments[1] = doi(u);
    return _open.apply(this, arguments);
  };

  // Logo của bảng theo logo TISA BOT (ô Ảnh đại diện trong Cài đặt). Logo riêng đặt trong bảng vẫn đè lên trên.
  var stLogo = document.createElement("style");
  stLogo.textContent = ".ns-logo[data-kit-logo]{display:grid!important;background:#fff url(/brand-logo) center/cover no-repeat!important}" +
    ".ns-logo[data-kit-logo]+.ns-mark{display:none!important}";
  (document.head || document.documentElement).appendChild(stLogo);

  var trongKhung = window.parent && window.parent !== window;
  var cha = null;
  try { cha = trongKhung ? window.parent.document : null; } catch (e) { cha = null; }

  function theoTong() {
    if (!cha) return;
    // TISA BOT: tông sáng là data-theme="light", tông tối là KHÔNG có thuộc tính (theme.js).
    var t = cha.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
    if (document.documentElement.getAttribute("data-theme") !== t) {
      document.documentElement.setAttribute("data-theme", t);
      try { localStorage.setItem("vp-theme", t); } catch (e) {}
    }
  }
  if (cha) {
    // Nằm trong TISA BOT: menu TISA BOT là menu duy nhất. Ẩn menu, thanh trên điện thoại của bảng, và những phần
    // TISA BOT đã có (logo, màu, bộ máy AI, tài khoản, thư mục bộ não).
    document.documentElement.classList.add("tisa-nhung");
    var an = document.createElement("style");
    an.textContent =
      "html.tisa-nhung,html.tisa-nhung.side-mini{--side-w:0px!important}" +
      "html.tisa-nhung .nav-side,html.tisa-nhung .nav-mtop,html.tisa-nhung .nav-backdrop{display:none!important}" +
      "html.tisa-nhung body:not(.locked){padding-left:0!important}html.tisa-nhung .toast{left:50%!important}" +
      "html.tisa-nhung [data-sub-link='cai-dat/bo-may'],html.tisa-nhung [data-sub-link='cai-dat/tai-khoan']{display:none!important}" +
      "html.tisa-nhung #set-engine,html.tisa-nhung #set-brain,html.tisa-nhung #set-login,html.tisa-nhung #set-data{display:none!important}" +
      "html.tisa-nhung .f:has(.logo-row),html.tisa-nhung .f:has(.color-row){display:none!important}" +
      // Khung "Bắt đầu với Đội Quân AI": hồ sơ, đội ngũ và bộ máy AI đã có từ TISA BOT (chủ bỏ 09/11/2026).
      "html.tisa-nhung #kit-start{display:none!important}" +
      ".tisa-gop{margin-top:22px}.tisa-gop>h3.sec{margin:0 0 10px}.tisa-gop-hd{margin-top:18px}.tisa-gop-hd>summary{cursor:pointer;font-weight:700;padding:12px 0}";
    (document.head || document.documentElement).appendChild(an);
    theoTong();
    new MutationObserver(theoTong).observe(cha.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    var st = document.createElement("style");
    st.textContent = "#logout-btn,#theme-btn{display:none!important}";
    (document.head || document.documentElement).appendChild(st);
  }

  /* ---------- Gộp trang khi nằm trong TISA BOT ---------- */
  // "Nộp dữ liệu" vào Tiến độ > Cần anh xử lý; "Hướng dẫn" xuống cuối Cài đặt. Chỉ chuyển phần tử, mã bảng vẫn tìm
  // được theo id (#need-list, #inputs-list) nên không phải sửa mã bảng.
  function gop() {
    if (!cha) return;
    var sub = document.querySelector('section.view[data-view="cai-dat"] .page-head .sub');
    if (sub) sub.textContent = "Hồ sơ doanh nghiệp, nhân sự và phòng ban. Lưu ở đây là cả đội dùng ngay.";
    var td = document.querySelector('section.view[data-view="tien-do"]');
    var dl = document.querySelector('section.view[data-view="du-lieu"]');
    if (td && dl && !td.querySelector(".tisa-gop")) {
      var w = document.createElement("div");
      w.className = "tisa-gop"; w.setAttribute("data-sub", "can-anh");
      var head = dl.querySelector(".page-head");
      var h = document.createElement("h3"); h.className = "sec"; h.textContent = "Dữ liệu đội đang cần";
      w.appendChild(h);
      var nut = head && head.querySelector("#upload-free");
      if (nut) w.appendChild(nut);
      Array.prototype.slice.call(dl.children).forEach(function (c) { if (c !== head) w.appendChild(c); });
      td.appendChild(w);
    }
    var cd = document.querySelector('section.view[data-view="cai-dat"]');
    var hd = document.querySelector('section.view[data-view="huong-dan"]');
    if (cd && hd && !cd.querySelector(".tisa-gop-hd")) {
      var d = document.createElement("details");
      d.className = "card tisa-gop-hd"; d.setAttribute("data-sub", "doanh-nghiep nhan-su"); d.id = "tisa-huong-dan";
      d.innerHTML = "<summary>Hướng dẫn sử dụng Đội Quân AI</summary>";
      Array.prototype.slice.call(hd.children).forEach(function (c) { if (!c.classList.contains("page-head")) d.appendChild(c); });
      cd.appendChild(d);
    }
  }
  // Trang đã bỏ khỏi bảng thì chuyển sang chỗ mới; trang còn lại thì báo TISA BOT để tô đúng mục trên menu.
  function theoTrang() {
    if (!cha) return;
    var h = (location.hash || "").replace("#", ""), v = h.split("/")[0];
    if (v === "chat") { history.replaceState(null, "", "#ban-lam-viec"); moChatTisa(""); return; }
    if (v === "bo-nao") { history.replaceState(null, "", "#ban-lam-viec"); window.parent.postMessage({ tisaDoiQuan: "mo-trang", trang: "home" }, location.origin); return; }
    if (v === "du-lieu") { location.replace("#tien-do/can-anh"); return; }
    if (v === "huong-dan") { location.replace("#cai-dat/doanh-nghiep"); setTimeout(function () { var d = document.getElementById("tisa-huong-dan"); if (d) { d.open = true; d.scrollIntoView(); } }, 150); return; }
    window.parent.postMessage({ tisaDoiQuan: "trang", trang: h || "ban-lam-viec" }, location.origin);
  }
  if (cha) {
    // Chạy trước bộ chuyển trang của bảng (gắn sau), để trang đã bỏ không kịp hiện ra.
    window.addEventListener("hashchange", theoTrang);
    document.addEventListener("DOMContentLoaded", function () { gop(); theoTrang(); });
  }

  // Mã nhân sự trên bảng -> tên cộng sự bên TISA BOT, cùng quy tắc với tisa_team_sync.board_roster.
  function khongDau(s) {
    return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D")
      .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  }
  function slugCua(id) {
    var K = window.__KIT || {}, T = K.team || {};
    var a = (T.agents || []).filter(function (x) { return x && x.id === id; })[0];
    if (a) return "dq-" + (a.skill || a.id);
    var c = (T.custom || []).filter(function (x) { return x && x.id === id; })[0];
    if (!c) return "";
    var sk = String(c.skill || "");
    return /^[\w-]+$/.test(sk) && sk !== "tu-chon" ? sk : "dq-" + (khongDau(c.name) || khongDau(String(c.id).slice(2)));
  }
  function moChatTisa(id) {
    var slug = id ? slugCua(id) : "";
    var msg = { tisaDoiQuan: "mo-chat", slug: slug };
    if (trongKhung) window.parent.postMessage(msg, location.origin);
    else location.href = "/#" + (slug ? "cs=" + encodeURIComponent("agent:" + slug) : "workspace");
  }
  document.addEventListener("click", function (e) {
    var t = e.target && e.target.closest ? e.target : null;
    if (!t) return;
    var dm = t.closest("[data-dm-open]");
    var nav = t.closest('[data-view-link="chat"]');
    if (!dm && !nav) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    moChatTisa(dm ? dm.getAttribute("data-dm-open") : "");
  }, true);
})();
