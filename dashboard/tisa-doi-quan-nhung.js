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
      "section.view[data-view=tien-do] .subtabs,section.view[data-view=tien-do][data-dq=can-anh] [data-sub=bang],section.view[data-view=tien-do][data-dq=can-anh] [data-sub=lich]{display:none!important}" +
      "section.view[data-view=ket-qua]:not([data-dq-kq=bc]) .dq-kq-bc{display:none!important}section.view[data-view=ket-qua][data-dq-kq=bc] .dq-kq-bc{display:grid!important}" +
      "section.view[data-view=ket-qua][data-dq-kq=bc]>:not(.dq-kq-nav):not(.page-head):not(.dq-kq-bc){display:none!important}" +
      "section.view[data-view=ket-qua]:not([data-dq-kq=bang]) .dq-kq-bang{display:none!important}section.view[data-view=ket-qua][data-dq-kq=bang] .dq-kq-bang{display:block!important}" +
      "section.view[data-view=ket-qua][data-dq-kq=bang]>:not(.dq-kq-nav):not(.page-head):not(.dq-kq-bang){display:none!important}.dq-kq-bang .row-actions{margin:0 0 10px}" +
      ".dq-ngu-nav{display:inline-flex;flex-wrap:wrap;gap:4px;padding:4px;margin:2px 0 14px;border:1px solid var(--line);border-radius:12px;background:var(--surface)}" +
      ".dq-ngu-nav a{padding:8px 15px;border-radius:9px;color:var(--muted);font:700 13.5px var(--font-body);text-decoration:none}" +
      ".dq-ngu-nav a:hover{color:var(--ink);background:var(--surface-2)}.dq-ngu-nav a[aria-current=page]{background:var(--b2,#172f72);color:#fff}" +
      ".tisa-gop{margin-top:22px}.tisa-gop>h3.sec{margin:0 0 10px}.tisa-gop-hd{margin-top:18px}.tisa-gop-hd>summary{cursor:pointer;font-weight:700;padding:12px 0}" +
      // Điện thoại (V2.96, chủ 17/11/2026: "kiểm tra giao diện điện thoại, fix bố cục"): cột việc không kéo dài cả màn hình khi trống,
      // bộ lọc ngày gọn một hàng, thanh tab Đội ngũ/Kết quả một hàng cuộn ngang thay vì rớt dòng.
      "@media (max-width:640px){" +
        "html.tisa-nhung .kanban{grid-template-columns:repeat(4,minmax(80vw,80vw));align-items:start;gap:10px;scroll-snap-type:x proximity;scroll-padding-left:2px}" +
        "html.tisa-nhung .kcol{scroll-snap-align:start;min-height:0}html.tisa-nhung .kcol-list{max-height:58vh!important}" +
        "html.tisa-nhung .df{gap:8px;padding:8px 10px}" +
        "html.tisa-nhung .df>.seg{display:flex;flex:1 1 0;min-width:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}" +
        "html.tisa-nhung .df>.seg::-webkit-scrollbar{display:none}html.tisa-nhung .df>.seg>*{flex:0 0 auto;white-space:nowrap}" +
        "html.tisa-nhung .df-custom{flex:1 1 100%;flex-wrap:nowrap;gap:8px}" +
        "html.tisa-nhung .df-custom label{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:flex-start;gap:3px;font-size:11.5px}" +
        "html.tisa-nhung .df-custom input{width:100%;box-sizing:border-box}html.tisa-nhung .df-sum{flex:1 1 100%;margin:0}" +
        ".dq-ngu-nav{display:flex;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;max-width:100%;box-sizing:border-box}" +
        ".dq-ngu-nav::-webkit-scrollbar{display:none}.dq-ngu-nav a{flex:0 0 auto;padding:8px 12px;font-size:13px;white-space:nowrap}" +
        // V3.28 (chủ 19/11/2026 "chồng chữ, lệch nút trên điện thoại"): ô tìm ở Kết quả và Kho tư liệu đủ rộng một hàng.
        "html.tisa-nhung .res-tools>.mic-wrap,html.tisa-nhung .kho-bar>.mic-wrap{flex:1 1 100%;min-width:0}" +
        "html.tisa-nhung .res-tools>.mic-wrap>input,html.tisa-nhung .kho-bar>.mic-wrap>input{width:100%;box-sizing:border-box}" +
        // Bốn nút Ảnh, video, tệp / Cả thư mục / Nói thay gõ / Trình duyệt AI: 2 cột, biểu tượng nằm cạnh chữ, không còn ô hẹp chữ xếp 3 dòng.
        "html.tisa-nhung .att-acts{grid-auto-flow:row;grid-template-columns:repeat(2,minmax(0,1fr))}" +
        "html.tisa-nhung .att-acts .att-b{flex-direction:row;min-height:44px;padding:8px 10px;font-size:13px}" +
        // Thông báo nổi nhiều dòng: bo góc vừa phải thay vì viên thuốc méo.
        "html.tisa-nhung .toast{border-radius:14px;width:max-content;line-height:1.4}" +
      "}" +
      // V3.28: Cài đặt đội > Nhân sự: dưới 900px nút bật/tắt và nút "Chi tiết" cùng ô lưới nên đè lên nhau. "Chi tiết" xuống hàng Phòng.
      "@media (max-width:899px){" +
        "html body .pb-luoi .pb-the .tm-custom{grid-template-areas:'av ten on' 'av cd cd' 'av phong act'!important}" +
        "html body .pb-luoi .pb-the .tm-custom>.tm-act{grid-area:act!important;justify-self:end;align-self:center}" +
      "}";
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
  // Đội ngũ gồm 3 trang: Văn phòng (3D/2D), Sơ đồ & hồ sơ, Cài đặt đội. Thanh 3 nút ở đầu mỗi trang để đi qua lại, thay cho 3 mục rời trên menu.
  var NAV_NGU = [["van-phong", "Văn phòng", "#van-phong"], ["doi-ngu", "Sơ đồ và hồ sơ", "#doi-ngu"], ["cai-dat", "Cài đặt đội", "#cai-dat/nhan-su"]];
  function thanhDoiNgu() {
    ["van-phong", "doi-ngu", "cai-dat"].forEach(function (v) {
      var sec = document.querySelector('section.view[data-view="' + v + '"]');
      if (!sec || sec.querySelector(".dq-ngu-nav")) return;
      var nav = document.createElement("nav");
      nav.className = "dq-ngu-nav"; nav.setAttribute("aria-label", "Đội ngũ");
      nav.innerHTML = NAV_NGU.map(function (x) {
        return '<a href="' + x[2] + '"' + (x[0] === v ? ' aria-current="page"' : "") + ">" + x[1] + "</a>";
      }).join("");
      sec.insertBefore(nav, sec.firstChild);
    });
    var h2 = document.querySelector('section.view[data-view="cai-dat"] .page-head h2');
    if (h2 && h2.textContent.trim() === "Cài đặt") h2.textContent = "Cài đặt đội";
  }
  // Cần anh và Đang làm là HAI trang riêng (chủ 17/11/2026), dù cùng nằm trong khung Tiến độ của bảng: mỗi trang một tiêu đề, một bộ tab.
  //   Cần anh: chỉ danh sách việc chờ anh, không tab. Đang làm: Bảng công việc + Lịch báo cáo.
  function theoTienDo() {
    var td = document.querySelector('section.view[data-view="tien-do"]');
    if (!td) return;
    var h = (location.hash || "").replace("#", "").split("/");
    if (h[0] !== "tien-do") return;
    var cheDo = h[1] === "bang" ? "dang-lam" : "can-anh";
    td.setAttribute("data-dq", cheDo);
    var h2 = td.querySelector(".page-head h2"), sub = td.querySelector(".page-head .sub");
    if (h2) h2.textContent = cheDo === "can-anh" ? "Cần anh" : "Đang làm";
    if (sub) sub.textContent = cheDo === "can-anh"
      ? "Việc đang chờ anh quyết: duyệt, anh làm, bị kẹt hoặc cần nộp dữ liệu. Xử lý ngay tại đây."
      : "Đội làm tới đâu rồi: mọi việc theo trạng thái. Việc xong xem ở mục Kết quả.";
  }
  // Báo cáo tự động (lịch + báo cáo gần đây) là thành phẩm nên nằm ở Kết quả, tab thứ hai.
  function theoKetQua() {
    var kq = document.querySelector('section.view[data-view="ket-qua"]');
    if (!kq) return;
    var h = (location.hash || "").replace("#", "").split("/");
    if (h[0] !== "ket-qua") return;
    var bc = h[1] === "bao-cao", bang = h[1] === "bang", che = bc ? "bc" : bang ? "bang" : "vl";
    kq.setAttribute("data-dq-kq", che);
    Array.prototype.forEach.call(kq.querySelectorAll(".dq-kq-nav a"), function (a) {
      if (a.getAttribute("data-k") === che) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    if (bang) { try { window.dispatchEvent(new Event("resize")); } catch (e) {} }
    var sub = kq.querySelector(".page-head .sub");
    if (sub) {
      if (!kq.__subGoc) kq.__subGoc = sub.textContent;
      sub.textContent = bc ? "Báo cáo tự động của đội: lịch chạy và các báo cáo gần đây (tổng kết ngày, việc cần quyết sáng nay, báo cáo tuần)."
        : bang ? "Tiến độ của đội: mọi việc theo 4 cột, từ chờ làm, đang làm, chờ anh duyệt tới xong. Lọc theo nhân sự và theo ngày." : kq.__subGoc;
    }
  }
  function ganBaoCao() {
    var kq = document.querySelector('section.view[data-view="ket-qua"]');
    var td = document.querySelector('section.view[data-view="tien-do"]');
    var lich = td && td.querySelector('.two-col[data-sub="lich"]');
    var bangEl = td && td.querySelector("#kanban");
    if (kq && bangEl && !kq.querySelector(".dq-kq-bang")) {
      var wb = document.createElement("div"); wb.className = "dq-kq-bang";
      [td.querySelector('.row-actions[data-sub="bang"]'), td.querySelector('.date-filter[data-df="tasks"]'), bangEl].forEach(function (x) {
        if (x) { x.removeAttribute("data-sub"); wb.appendChild(x); }
      });
      kq.appendChild(wb);
    }
    if (!kq || !lich || kq.querySelector(".dq-kq-nav")) return;
    lich.removeAttribute("data-sub");
    lich.classList.add("dq-kq-bc");
    kq.appendChild(lich);
    var nav = document.createElement("nav");
    nav.className = "dq-kq-nav dq-ngu-nav"; nav.setAttribute("aria-label", "Kết quả");
    nav.innerHTML = '<a href="#ket-qua/bang" data-k="bang">Tiến độ</a><a href="#ket-qua" data-k="vl">Kết quả công việc</a><a href="#ket-qua/bao-cao" data-k="bc">Báo cáo tự động</a>';
    kq.insertBefore(nav, kq.firstChild);
  }
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
    // Một nơi duy nhất cho "Cần anh": trang Cần anh (gộp theo từng việc, duyệt và sửa tại chỗ) chuyển vào Tiến độ > Cần anh xử lý, thay danh sách cũ.
    var ca = document.getElementById("ca-page"), mine = document.getElementById("mine");
    if (td && ca && mine && !td.querySelector("#ca-page") && !document.getElementById("gop-card")) {
      ca.setAttribute("data-sub", "can-anh");
      mine.parentNode.insertBefore(ca, mine);
      mine.style.display = "none";
    }
    thanhDoiNgu();
    ganBaoCao();
    theoKetQua();
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
    if (v === "cho-anh" || h === "tien-do" || h === "tien-do/can-anh" || v === "du-lieu") { location.replace("#ban-lam-viec"); return; }   // 23/11: Cần anh gộp vào Giao dự án
    if (h === "tien-do/lich") { location.replace("#ket-qua/bao-cao"); return; }
    if (h === "tien-do/bang") { location.replace("#ket-qua/bang"); return; }                                                           // 23/11: bảng 4 cột chuyển sang Kết quả > Tiến độ
    if (v === "huong-dan") { location.replace("#cai-dat/doanh-nghiep"); setTimeout(function () { var d = document.getElementById("tisa-huong-dan"); if (d) { d.open = true; d.scrollIntoView(); } }, 150); return; }
    window.parent.postMessage({ tisaDoiQuan: "trang", trang: h || "ban-lam-viec" }, location.origin);
  }
  if (cha) {
    // Chạy trước bộ chuyển trang của bảng (gắn sau), để trang đã bỏ không kịp hiện ra.
    window.addEventListener("hashchange", theoTrang);
    window.addEventListener("hashchange", theoTienDo);
    window.addEventListener("hashchange", theoKetQua);
    document.addEventListener("DOMContentLoaded", function () { gop(); theoTienDo(); theoKetQua(); setTimeout(function () { theoTienDo(); theoKetQua(); }, 400); theoTrang(); });
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

  /* 4. TRANG KẾT QUẢ: tiêu đề ngắn dễ hiểu (V2.91). Việc giao bằng giọng có tiêu đề là nguyên văn lời nói; ở đây thay bằng tiêu đề AI tóm tắt
        (máy chủ lưu lại, mỗi việc tóm tắt một lần), tạm dùng bản rút gọn bằng luật trong lúc chờ. Lời gốc vẫn xem được khi rê chuột và trong chi tiết việc. */
  (function () {
    var KEY = "tisa.dq.tieude", mem = {}, cho = {}, dangGoi = false, hen = 0;
    try { mem = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { mem = {}; }
    var THUA = ["alo", "a lô", "ê", "này", "nè", "dạ", "vâng", "ừ", "ok", "okay", "rồi", "bây giờ", "giờ", "vậy", "thế", "thì", "mà", "em ơi", "ơi", "anh muốn em", "anh muốn", "anh cần em", "anh cần", "anh nhờ em", "anh nhờ", "anh bảo em", "anh bảo", "anh dặn em", "mình muốn em", "mình muốn", "tôi muốn", "bạn hãy", "em hãy", "các em hãy", "hãy", "làm ơn", "giúp cho anh", "giúp anh", "giúp em", "giúp", "giùm", "cho anh", "đó là", "những cái", "cái", "em", "anh", "mình", "nha", "nhé"].sort(function (a, b) { return b.length - a.length; });
    function rutGon(t) {
      var s = String(t || "").replace(/https?:\/\/\S+|\(\d+ link\)/g, "").replace(/\s+/g, " ").trim().replace(/[.…:;,]+$/, "").replace(/^[\W_]+/, "");
      for (var n = 0; n < 12; n++) {
        var low = s.toLowerCase(), hit = "";
        for (var i = 0; i < THUA.length; i++) { var w = THUA[i]; if (low.indexOf(w) === 0 && (low.length === w.length || !/[0-9a-zà-ỹ]/i.test(low.charAt(w.length)))) { hit = w; break; } }
        if (!hit) break;
        s = s.slice(hit.length).replace(/^[\s,.!?:;]+/, "");
      }
      [" giúp cho anh", " giúp anh", " giùm anh", " cho anh", " đó là những cái", " đó là", " những cái", " nha", " nhé"].forEach(function (g) { var k; while ((k = s.toLowerCase().indexOf(g)) >= 0 && (k + g.length === s.length || /[\s,.!?]/.test(s.charAt(k + g.length)))) s = s.slice(0, k) + s.slice(k + g.length); });
      s = s.replace(/\s+/g, " ").trim();
      if (!s) s = String(t || "").trim();
      s = s.charAt(0).toUpperCase() + s.slice(1);
      if (s.length > 56) s = s.slice(0, 56).replace(/\s+\S*$/, "").replace(/[ ,;:-]+$/, "") + "…";
      return s;
    }
    /* V2.95 Việc nối tiếp: tiêu đề = "<tên chuỗi> · Bước N: <phần mới>", kèm chip "Tiếp từ <việc trước>". */
    var CM = {};   // tên chuỗi theo id việc gốc, để các bước cùng một mạch dùng chung một tên
    try { CM = JSON.parse(localStorage.getItem(KEY + ".c") || "{}") || {}; } catch (e) { CM = {}; }
    function ghep(e) { return (e && e.t) || ""; }   // tiêu đề = việc làm là gì; "bước mấy, tiếp từ kết quả nào" nằm ở chip phía trên (board)
    function tenViec(id, goc) { var e = mem[id]; return (e && e.t) ? ghep(e, e.b) : rutGon(goc); }
    var quan = null;
    function ap() {
      if (quan) quan.disconnect();
      try { ap2(); } finally { var el = document.getElementById("results"); if (quan && el) { quan.takeRecords(); quan.observe(el, { childList: true, subtree: true }); } }
    }
    function ap2() {
      var ds = document.querySelectorAll("#results .rr-open[data-result-open]"), thieu = [];
      for (var i = 0; i < ds.length; i++) {
        var b = ds[i], id = b.getAttribute("data-result-open"), goc = b.getAttribute("data-goc");
        if (!goc) { goc = b.textContent; b.setAttribute("data-goc", goc); }
        var sub = b.parentNode.querySelector(".rr-sub"), gocSub = sub ? (sub.getAttribute("data-goc") || sub.textContent) : "";
        if (sub && !sub.getAttribute("data-goc")) sub.setAttribute("data-goc", gocSub);
        var e = mem[id], hop = e && e.g === goc;
        var tid = b.getAttribute("data-tiep-id") || (b.parentNode.querySelector(".rr-tiep") || { getAttribute: function () { return ""; } }).getAttribute("data-tiep-id"),
            buoc = Number(b.getAttribute("data-buoc")) || 0, tTen = b.getAttribute("data-tiep-ten") || "";
        var moi = hop && e.t ? ghep(e, buoc) : rutGon(goc), tit = "Việc anh giao: " + goc;
        var chip = b.parentNode.querySelector(".rr-tiep");
        if (chip && tid) { var tn = chip.querySelector(".rr-tiep-ten"); if (tn) { var ct = tenViec(tid, tTen); if (tn.textContent !== ct) tn.textContent = ct; } }
        if (b.textContent !== moi) b.textContent = moi;        // chỉ ghi khi khác: ghi lại cùng chữ làm trang vẽ lại không ngừng
        if (b.title !== tit) b.title = tit;
        if (sub && hop && e.m && sub.textContent !== e.m) sub.textContent = e.m;
        var item = { id: id, title: goc, summary: gocSub, _b: buoc };
        if (tid && tTen) item.tiep = { ten: tenViec(tid, tTen), chuoi: (mem[tid] && mem[tid].c) || CM[tid] || b.getAttribute("data-chuoi") || "", buoc: buoc || 2 }, item._t = tid;
        if (!(hop && e.ai) && !cho[id]) thieu.push(item);
      }
      if (thieu.length && !dangGoi) { clearTimeout(hen); hen = setTimeout(function () { goi(thieu.slice(0, 20)); }, 600); }
    }
    function goi(ds) {
      if (dangGoi) return; dangGoi = true;
      ds.forEach(function (x) { cho[x.id] = 1; });
      var gui = ds.map(function (x) { return { id: x.id, title: x.title, summary: x.summary, tiep: x.tiep }; });
      fetch("/tisa-doi-quan/tieu-de", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ items: gui }) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j || !j.ok) return;
          ds.forEach(function (x) { var v = j.tieu_de && j.tieu_de[x.id]; if (v && v.t) { mem[x.id] = { g: x.title, t: v.t, m: v.m || "", c: v.c || "", b: x._b || 0, ai: !!v.ai }; if (x._t && v.c && v.ai && !CM[x._t]) CM[x._t] = v.c; } });
          try { localStorage.setItem(KEY + ".c", JSON.stringify(CM)); } catch (e) {}
          try { var k = Object.keys(mem); if (k.length > 400) k.slice(0, k.length - 400).forEach(function (z) { delete mem[z]; }); localStorage.setItem(KEY, JSON.stringify(mem)); } catch (e) {}
        })
        .catch(function () {})
        .then(function () { dangGoi = false; ds.forEach(function (x) { if (!(mem[x.id] && mem[x.id].ai)) setTimeout(function () { delete cho[x.id]; }, 120000); else delete cho[x.id]; }); ap(); });
    }
    /* Tiêu đề ở đầu cửa sổ chi tiết việc cũng dùng tiêu đề ngắn (lời gốc xem khi rê chuột). */
    function apTieuDe() {
      var t = document.getElementById("drawer-title"); if (!t) return;
      var goc = t.getAttribute("data-goc"); if (!goc) { goc = t.textContent; t.setAttribute("data-goc", goc); }
      var moi = "", k;
      for (k in mem) { if (mem[k] && mem[k].g === goc && mem[k].t) { moi = ghep(mem[k], mem[k].b); break; } }
      if (!moi) moi = rutGon(goc);
      if (t.textContent !== moi) t.textContent = moi;
      if (t.title !== "Việc anh giao: " + goc) t.title = "Việc anh giao: " + goc;
    }
    var pend = 0, pend2 = 0;
    function lich() { clearTimeout(pend); pend = setTimeout(ap, 80); }
    function ganTieuDe() { new MutationObserver(function () { clearTimeout(pend2); pend2 = setTimeout(apTieuDe, 60); }).observe(document.body, { childList: true, subtree: true }); }
    if (document.body) ganTieuDe(); else document.addEventListener("DOMContentLoaded", ganTieuDe);
    function gan() {
      var el = document.getElementById("results");
      if (!el) { setTimeout(gan, 600); return; }
      quan = new MutationObserver(lich); quan.observe(el, { childList: true, subtree: true });
      lich();
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", gan); else gan();
  })();

  /* 5. MỞ FILE, HIỆN TRONG FINDER NGAY (V2.91). Trước đây bấm nút là gửi một tin lên máy chủ đám mây, chờ máy anh tới hỏi lại rồi mới mở
        (chậm cả chục giây). Khi trang đang chạy ngay trên máy TISA BOT thì gọi thẳng máy chủ TISA BOT, mở tức thì. Không gọi được thì quay về
        đường cũ (qua đám mây) như trước. */
  (function () {
    var may = null, stl = document.createElement("style");
    stl.textContent = ".da-mo-nhanh{box-shadow:0 0 0 3px rgba(34,197,94,.45)!important;transition:box-shadow .2s}";
    document.head.appendChild(stl);
    fetch("/tisa-mo-tep/may-chu", { credentials: "same-origin" }).then(function (r) { return r.json(); })
      .then(function (j) { may = !!(j && j.may_chu); }).catch(function () { may = false; });
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-open-path]");
      if (!b || b.__tisaCu || may !== true) return;
      var dir = String(b.getAttribute("data-open-path") || "");
      if (/^kho:/.test(dir)) return;
      var file = b.getAttribute("data-open-file") || "", mo = b.hasAttribute("data-open-mo");
      e.preventDefault(); e.stopImmediatePropagation();
      var rel = dir.replace(/^\/+|\/+$/g, "") + (file ? "/" + file.replace(/^\/+/, "") : "");
      b.disabled = true;
      b.setAttribute("aria-busy", "true");
      function xong() { b.disabled = false; b.removeAttribute("aria-busy"); }
      fetch("/tisa-mo-tep", { method: "POST", credentials: "same-origin", headers: { "content-type": "application/json" },
        body: JSON.stringify({ brain: "brain", path: rel, cach: (mo && file) ? "mo" : "thu-muc" }) })
        .then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function (j) {
          xong();
          if (j && j.ok) { b.classList.add("da-mo-nhanh"); setTimeout(function () { b.classList.remove("da-mo-nhanh"); }, 900); return; }
          b.__tisaCu = true; b.click(); b.__tisaCu = false;   // không mở thẳng được: dùng đường cũ
        })
        .catch(function () { xong(); b.__tisaCu = true; b.click(); b.__tisaCu = false; });
    }, true);
  })();

  /* V2.98: nút "Trình duyệt AI" ngay trong ô Giao việc, mở bảng Trình duyệt TISA ở cửa sổ cha. */
  (function () {
    function chen() {
      var ds = document.querySelectorAll("#task-att .att-acts");
      Array.prototype.forEach.call(ds, function (d) {
        if (d.querySelector(".tbd-b")) return;
        var b = document.createElement("button"); b.type = "button"; b.className = "btn btn-sm att-b tbd-b";
        b.title = "Mở trình duyệt cho AI thao tác: anh đăng nhập một lần, AI làm thay"; b.innerHTML = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px;vertical-align:-2px"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>Trình duyệt AI';
        b.addEventListener("click", function (e) { e.preventDefault(); try { window.parent.postMessage({ tisaTrinhDuyet: "mo" }, location.origin); } catch (x) {} });
        d.appendChild(b);
      });
    }
    setInterval(chen, 1500); chen();
  })();
})();
