/* tisa-doi-quan.js - các trang của Đội Quân AI (/doiquanagent) mở ngay trong khung TISA BOT.
   Thanh menu TISA BOT là menu duy nhất: "Giao dự án" ở khối trên cùng, nhóm "Đội Quân AI" (Văn phòng, Tiến độ, Kết quả,
   Đội ngũ, Cài đặt đội), "Nạp kiến thức" và "Kho tư liệu" trong nhóm Bộ não. Mỗi mục là một `launch` (tisa-icons.js)
   gọi TISADoiQuan.mo(trang, mục). Bảng giữ nguyên trạng thái khi qua lại các trang khác; menu riêng của bảng bị ẩn
   (tisa-doi-quan-nhung.js). Bảng báo lại khi tự chuyển trang để menu tô đúng mục, và nhờ mở chat Cộng Sự khi cần. */
(function () {
  "use strict";
  var HASH = "#doiquan";
  var khung = null, iframe = null, khac = null, dangMo = false;

  function nav() { try { return window.Alpine && Alpine.store("nav"); } catch (e) { return null; } }
  // Trang của bảng -> mục trên thanh menu (để tô sáng).
  function mucCua(trang) {
    var goc = String(trang || "").split("/")[0], M = window.TISA_DQ_TRANG || {};
    for (var k in M) if (M[k].split("/")[0] === goc) return k;
    return "";
  }

  function dung() {
    if (khung) return;
    khung = document.createElement("div");
    khung.id = "tisaDoiQuanKhung";
    khung.className = "tisa-dq-khung";
    khung.hidden = true;
    iframe = document.createElement("iframe");
    iframe.title = "Đội Quân AI";
    iframe.setAttribute("allow", "microphone; clipboard-write; autoplay; fullscreen");
    khung.appendChild(iframe);
    // Khung thứ hai cho trang riêng của TISA (Tài khoản nhân viên): bảng vẫn giữ trạng thái khi qua lại.
    khac = document.createElement("iframe");
    khac.title = "TISA BOT";
    khac.hidden = true;
    khung.appendChild(khac);
    document.body.appendChild(khung);
  }

  // Đặt trang đang mở của TISA BOT là mục dq-... : thanh menu tự tô đúng mục, và bất kỳ lần chuyển trang nào khác của
  // TISA BOT (thanh menu, thông báo, linh vật, liên kết trong chat) đều đổi giá trị này nên khung tự đóng (xem theoDoi).
  function datMuc(muc) {
    var s = nav();
    if (!s || !muc) return;
    s.active = muc;
    // Mở thẳng bằng đường dẫn thì nhóm chứa mục chưa bung: bung đúng nhóm đó.
    try {
      var g = (s.groups || []).filter(function (x) { return !x.ghim && x.items.some(function (it) { return it.id === muc; }); })[0];
      if (g) s.openGroup = g.label;
    } catch (e) {}
  }

  function mo(trang, muc) {
    dung();
    trang = trang || "ban-lam-viec";
    var dich = "#" + trang;
    if (!iframe.src) iframe.src = "/doiquanagent/?nhung=1" + dich;
    else {
      try { if (iframe.contentWindow.location.hash !== dich) iframe.contentWindow.location.hash = dich; }
      catch (e) { iframe.src = "/doiquanagent/?nhung=1" + dich; }
    }
    dangMo = true;
    khung.hidden = false;
    iframe.hidden = false;
    if (khac) khac.hidden = true;
    document.body.classList.add("tisa-dq-mo");
    // Điện thoại: đóng ngăn kéo menu vừa bấm.
    document.body.classList.remove("nav-open");
    var nen = document.getElementById("navBackdrop"); if (nen) nen.hidden = true;
    datMuc(muc || mucCua(trang));
    var h = HASH + "/" + trang;
    if (location.hash !== h) history.replaceState(null, "", location.pathname + location.search + h);
  }

  // Mở một trang riêng của TISA (không phải bảng) trong cùng khung, ví dụ /tisa-nv/.
  function moTrang(url, muc) {
    dung();
    if (khac.getAttribute("src") !== url) khac.src = url;
    dangMo = true;
    khung.hidden = false;
    iframe.hidden = true;
    khac.hidden = false;
    document.body.classList.add("tisa-dq-mo");
    document.body.classList.remove("nav-open");
    var nen = document.getElementById("navBackdrop"); if (nen) nen.hidden = true;
    datMuc(muc);
    if (location.hash.indexOf(HASH) === 0) history.replaceState(null, "", location.pathname + location.search);
  }

  function dong() {
    if (!dangMo) return;
    dangMo = false;
    khung.hidden = true;
    document.body.classList.remove("tisa-dq-mo");
    if (location.hash.indexOf(HASH) === 0) history.replaceState(null, "", location.pathname + location.search);
  }

  window.addEventListener("message", function (e) {
    if (e.origin !== location.origin || !e.data || !e.data.tisaDoiQuan) return;
    var d = e.data, s = nav();
    if (d.tisaDoiQuan === "trang") {            // bảng tự chuyển trang (nút "Làm ngay", liên kết trong bảng)
      if (dangMo) { datMuc(mucCua(d.trang)); history.replaceState(null, "", location.pathname + location.search + HASH + "/" + d.trang); }
      return;
    }
    if (d.tisaDoiQuan === "mo-chat") {
      dong();
      var slug = String(d.slug || "");
      if (slug && window.TISAOpenCongSu && window.TISAOpenCongSu("agent:" + slug)) return;
      if (s) s.go("workspace");
      return;
    }
    if (d.tisaDoiQuan === "mo-trang" && s) {   // trang bảng đã chuyển sang TISA BOT (Bộ não)
      dong();
      s.go(String(d.trang || "home"));
    }
  });

  function theoHash() {
    var h = location.hash || "";
    if (h === HASH || h.indexOf(HASH + "/") === 0) mo(h.slice(HASH.length + 1) || "ban-lam-viec");
  }
  window.addEventListener("hashchange", theoHash);
  // Chờ Alpine dựng thanh menu rồi mới mở theo địa chỉ (để tô đúng mục).
  var lan = 0;
  (function cho() {
    if ((nav() && document.querySelector(".rail .rail-item")) || lan++ > 60) { theoHash(); return; }
    setTimeout(cho, 100);
  })();
  // TISA BOT chuyển sang trang của nó (giá trị active không còn là dq-...): đóng khung bảng.
  (function theoDoi() {
    if (!(window.Alpine && Alpine.effect && nav())) { setTimeout(theoDoi, 200); return; }
    Alpine.effect(function () {
      var a = String(nav().active || "");
      if (dangMo && a.indexOf("dq-") !== 0) dong();
    });
  })();

  window.TISADoiQuan = { mo: mo, moTrang: moTrang, dong: dong, khung: function () { return iframe; } };
})();
