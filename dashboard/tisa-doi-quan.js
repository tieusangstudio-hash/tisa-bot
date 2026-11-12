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

  function moTrangDq(trang) { var ok = { "tien-do": "dq-tien-do", "ket-qua": "dq-ket-qua", "ban-lam-viec": "dq-du-an" }; mo(trang, ok[trang] || "dq-tien-do"); }
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
    if (d.tisaDoiQuan === "soan" && s) {       // trang con (Quản lý web) soạn sẵn yêu cầu vào ô Hỏi nhanh, chủ xem rồi bấm gửi
      dong();
      s.go("chat");
      var chu = String(d.text || "").slice(0, 4000);
      setTimeout(function () {
        var o = document.getElementById("chatInput");
        if (!o) return;
        o.value = chu;
        o.dispatchEvent(new Event("input", { bubbles: true }));
        o.focus();
      }, 250);
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

  // Trang Quảng Cáo (và các trang riêng khác) nhờ trợ lý hoặc mở trang Kết nối: nhận tin nhắn từ khung con cùng nguồn.
  window.addEventListener("message", function (e) {
    var d = e.data;
    if (e.origin !== location.origin || !d || typeof d !== "object") return;
    if (d.tisa === "hoi-tro-ly" && typeof d.text === "string") {
      dong();
      try { nav().go("chat"); } catch (x) {}
      var lan = 0;
      (function dien() {
        var o = document.getElementById("chatInput");
        if (o && o.offsetParent !== null) {
          o.value = d.text.slice(0, 6000);
          o.dispatchEvent(new Event("input", { bubbles: true }));
          o.focus();
        } else if (lan++ < 400) setTimeout(dien, 250);
      })();
    } else if (d.tisa === "mo-doi-quan") {
      try { moTrangDq(String(d.trang || "tien-do")); } catch (x) {}
    } else if (d.tisa === "mo-ket-noi") {
      dong();
      try { nav().go("mcp"); } catch (x) {}
    }
  });

  window.TISADoiQuan = { mo: mo, moTrang: moTrang, dong: dong, khung: function () { return iframe; } };
})();

/* Khung Giao dự án + Đội Quân AI trên thanh menu (V2.75, chủ chọn Mẫu 4A ngày 10/11/2026).
   Nút "+ Giao" mở Bàn làm việc và đặt con trỏ vào ô giao việc. 3 ô số đếm việc trên Bảng giao việc theo đúng cách trang
   Tiến độ chia cột: Đang làm (chưa xong, chưa chờ duyệt), Chờ duyệt, Đã xong; bấm vào mở trang Tiến độ.
   Bảng không bật hoặc không đọc được thì ẩn hàng số, phần còn lại vẫn dùng bình thường. */
(function () {
  "use strict";
  var dangDoc = false;

  function moBang(trang, muc) {
    if (window.TISADoiQuan) window.TISADoiQuan.mo(trang, muc);
  }

  function datConTro() {
    var lan = 0;
    (function thu() {
      var f = window.TISADoiQuan && window.TISADoiQuan.khung && window.TISADoiQuan.khung();
      var o = null;
      try { o = f && f.contentDocument && f.contentDocument.getElementById("demo-input"); } catch (e) {}
      if (o && o.offsetParent !== null) { try { o.focus(); o.scrollIntoView({ block: "center" }); } catch (e) {} return; }
      if (lan++ < 40) setTimeout(thu, 150);
    })();
  }

  function giao() { moBang("ban-lam-viec", "dq-du-an"); datConTro(); }
  function xem() { moBang("tien-do", "dq-tien-do"); }

  function dem(docs) {
    var c = { dang: 0, duyet: 0, xong: 0 };
    (docs || []).forEach(function (d) {
      var s = String((d && (d.status || (d.data && d.data.status))) || "");
      if (s === "xong") c.xong++;
      else if (s === "duyet") c.duyet++;
      else c.dang++;
    });
    return c;
  }

  function ve(c) {
    var hang = document.getElementById("tkgSo");
    if (!hang) return;
    if (!c) { hang.hidden = true; return; }
    [["dang", c.dang], ["duyet", c.duyet], ["xong", c.xong]].forEach(function (x) {
      var b = hang.querySelector(".tkg-" + x[0] + " b");
      if (b) b.textContent = String(x[1]);
    });
    hang.hidden = false;
  }

  function doc() {
    if (dangDoc || document.hidden || !document.getElementById("tkgSo")) return;
    dangDoc = true;
    fetch("/doiquanagent/api/db/tasks", { credentials: "same-origin", cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (j) { ve(dem(j && j.docs)); })
      .catch(function () { ve(null); })
      .then(function () { dangDoc = false; });
  }

  // Thu gọn 5 mục Đội Quân AI (mẫu 1): nhớ trong trình duyệt này, mở lại vẫn giữ.
  var KHOA_GON = "tisa_khung_giao_gon";
  function apGon(gon) {
    var k = document.getElementById("tisaKhungGiao"), t = document.getElementById("tkgThanh");
    if (!k) return;
    k.classList.toggle("thu-gon", !!gon);
    if (t) t.setAttribute("aria-expanded", gon ? "false" : "true");
  }
  function thuGon() {
    var k = document.getElementById("tisaKhungGiao");
    var gon = !(k && k.classList.contains("thu-gon"));
    apGon(gon);
    try { localStorage.setItem(KHOA_GON, gon ? "1" : "0"); } catch (e) {}
  }
  (function choKhung() {
    if (!document.getElementById("tisaKhungGiao")) { setTimeout(choKhung, 150); return; }
    var gon = false;
    try { gon = localStorage.getItem(KHOA_GON) === "1"; } catch (e) {}
    apGon(gon);
  })();

  window.TISAKhungGiao = { giao: giao, xem: xem, doc: doc, dem: dem, thuGon: thuGon };
  var lan = 0;
  (function cho() {
    if (document.getElementById("tkgSo")) { doc(); return; }
    if (lan++ < 80) setTimeout(cho, 150);
  })();
  setInterval(doc, 45000);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) doc(); });
  // Bảng vừa đổi trang hoặc vừa giao xong việc: đếm lại sau một nhịp.
  window.addEventListener("message", function (e) {
    if (e.origin === location.origin && e.data && e.data.tisaDoiQuan) setTimeout(doc, 1500);
  });
})();

/* Thanh nhắc khi máy này vừa nhận dữ liệu từ máy cũ và đang CHẠY THỬ: hướng người dùng thử cho kỹ rồi mới chuyển tên miền. */
(function () {
  "use strict";
  function ve(d) {
    var cu = document.getElementById("tisaThuBanner");
    if (!d || d.giai_doan === "xong") { if (cu) cu.remove(); return; }
    try { if (sessionStorage.getItem("tisa-thu-an") === d.giai_doan) return; } catch (e) {}
    if (cu) return;
    var b = document.createElement("div"); b.id = "tisaThuBanner"; b.setAttribute("role", "status");
    b.style.cssText = "position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:9000;max-width:min(720px,94vw);display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 14px;border-radius:14px;background:#4c1d95;color:#fff;font:600 14px/1.4 system-ui,sans-serif;box-shadow:0 14px 40px -12px rgba(0,0,0,.5)";
    b.innerHTML = '<span>🧪 Máy này đang <b>chạy thử</b> sau khi chuyển. Máy cũ vẫn chạy bình thường, chưa chuyển tên miền.</span>' +
      '<button type="button" id="tisaThuMo" style="border:0;border-radius:10px;padding:7px 12px;font-weight:800;cursor:pointer;background:#fbbf24;color:#1f1300">Xem hướng dẫn thử</button>' +
      '<button type="button" id="tisaThuDong" aria-label="Ẩn" style="border:0;background:transparent;color:#fff;font-size:16px;cursor:pointer">✕</button>';
    document.body.appendChild(b);
    document.getElementById("tisaThuMo").onclick = function () { b.remove(); if (window.TISADoiQuan) window.TISADoiQuan.moTrang("/tisa-chuyen-may/", "dq-chuyen-may"); };
    document.getElementById("tisaThuDong").onclick = function () { try { sessionStorage.setItem("tisa-thu-an", d.giai_doan); } catch (e) {} b.remove(); };
  }
  function doc() {
    fetch("/tisa-chuyen-may/api/che-do-thu", { credentials: "same-origin" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) { if (j && j.ok) ve(j.che_do_thu); }).catch(function () {});
  }
  setTimeout(doc, 3500);
})();
