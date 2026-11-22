/* tisa-dien-thoai.js - V3.28: phần chạy của tisa-dien-thoai.css trên điện thoại.
   1. Bảng trong khung chat (từ 3 cột): gắn nhãn cột vào từng ô (data-nhan) để CSS xếp mỗi dòng thành một thẻ.
      Chỉ thêm thuộc tính, không đổi nội dung bảng; máy tính vẫn thấy bảng như cũ.
   2. Trang Đội Quân AI (khung bảng nhúng): đổi sang trang khác thì cuộn về đầu trang. Trước đây giữ vị trí cuộn
      của trang cũ, mở Kho tư liệu sau Nạp kiến thức là thấy ngay giữa trang. */
(function () {
  "use strict";

  function chuCua(o) { return String(o.textContent || "").replace(/\s+/g, " ").trim(); }

  function ganBang(t) {
    var dau = t.querySelectorAll(":scope > thead th");
    if (dau.length < 3) { if (t.getAttribute("data-tdt") !== "0") t.setAttribute("data-tdt", "0"); return; }
    var nhan = [];
    for (var i = 0; i < dau.length; i++) nhan.push(chuCua(dau[i]));
    if (t.getAttribute("data-tdt") !== "1") t.setAttribute("data-tdt", "1");
    var o = t.querySelectorAll(":scope > tbody > tr > td:not([data-nhan])");
    for (var j = 0; j < o.length; j++) {
      var k = Array.prototype.indexOf.call(o[j].parentNode.children, o[j]);
      o[j].setAttribute("data-nhan", nhan[k] || "");
    }
  }

  /* 3. Thanh "đang chạy ngầm" trên ô chat (background-strip.js) không có nút tắt, việc chạy lâu thì nằm đó mãi.
     Chủ 19/11/2026: "có nút tắt hay ẩn đi cho anh". Thêm nút × ẩn thanh: việc vẫn chạy, xem ở trang Việc.
     Nhớ theo nội dung thanh (mức + tên việc): có việc khác, hay việc chuyển sang kẹt, thì thanh hiện lại. */
  var KHOA_AN = "tisa.bgstrip.an";
  function docAn() { try { return localStorage.getItem(KHOA_AN) || ""; } catch (e) { return ""; } }
  function ghiAn(v) { try { localStorage.setItem(KHOA_AN, v); } catch (e) {} }
  function khoaDai(e) {
    var t = e.querySelector(".bg-pill-txt");
    var muc = String(e.className).split(/\s+/).filter(function (x) { return x.indexOf("bg-") === 0 && x !== "bg-strip"; }).join(",");
    return muc + "|" + (t ? t.textContent : "");
  }
  function xuLyDai() {
    var e = document.getElementById("bgStrip");
    if (!e || e.hidden || !e.querySelector(".bg-pill")) return;
    var k = khoaDai(e);
    e.classList.toggle("tisa-an", docAn() === k);
    if (e.querySelector(".bg-an")) return;
    var b = document.createElement("button");
    b.type = "button";
    b.className = "bg-an";
    b.textContent = "×";
    b.setAttribute("aria-label", "Ẩn dòng việc đang chạy");
    b.title = "Ẩn dòng này. Việc vẫn chạy, xem ở trang Việc. Có việc mới thì dòng tự hiện lại.";
    b.onclick = function (ev) { ev.stopPropagation(); ghiAn(khoaDai(e)); e.classList.add("tisa-an"); };
    e.appendChild(b);
  }

  function quet() {
    var ds = document.querySelectorAll(".md-tablewrap > table.md-table:not(.dv-table)");
    for (var i = 0; i < ds.length; i++) { try { ganBang(ds[i]); } catch (e) {} }
    try { xuLyDai(); } catch (e) {}
  }

  var hen = 0;
  function henQuet() {
    if (hen) return;
    hen = setTimeout(function () { hen = 0; quet(); }, 120);
  }

  function batDau() {
    quet();
    try { new MutationObserver(henQuet).observe(document.body, { childList: true, subtree: true }); } catch (e) {}
  }
  if (document.body) batDau(); else document.addEventListener("DOMContentLoaded", batDau);

  /* 2. Khung Đội Quân AI: cuộn về đầu khi đổi trang. Khóa trang = phần đầu địa chỉ (#kho, #ket-qua...);
     riêng Tiến độ tách Cần anh / Đang làm vì trên menu là hai trang khác nhau. */
  function khoaTrang(h) {
    var p = String(h || "").replace(/^#/, "").split("/");
    return p[0] === "tien-do" ? p[0] + "/" + (p[1] || "") : p[0];
  }
  function noiKhung(f) {
    if (!f || f.__tisaCuon) return;
    var w;
    try { w = f.contentWindow; if (!w || !w.document) return; } catch (e) { return; }
    f.__tisaCuon = 1;
    var truoc = khoaTrang(w.location.hash);
    w.addEventListener("hashchange", function () {
      var k = khoaTrang(w.location.hash);
      if (k === truoc) return;
      truoc = k;
      try { (w.document.scrollingElement || w.document.documentElement).scrollTop = 0; } catch (e) {}
    });
    // Tải lại khung (đăng nhập lại, đổi tông) thì gắn lại.
    if (!f.__tisaNap) {
      f.__tisaNap = 1;
      f.addEventListener("load", function () { f.__tisaCuon = 0; noiKhung(f); });
    }
  }
  (function choKhung() {
    var f = null;
    try { f = window.TISADoiQuan && window.TISADoiQuan.khung && window.TISADoiQuan.khung(); } catch (e) {}
    if (f && f.contentWindow && f.getAttribute("src")) noiKhung(f);
    setTimeout(choKhung, f && f.__tisaCuon ? 4000 : 800);
  })();
})();

/* (V3.44, chủ báo 22/11 kèm ảnh iPhone) Gõ trên điện thoại: ô nhập đứng cách bàn phím một khoảng trống.
   Bố cục bám bàn phím của lõi (mobile-chat.js mục 7) chỉ đo lại khi visualViewport báo "resize"/"scroll". Safari iOS mới
   báo chiều cao lúc bàn phím còn đang trượt lên rồi có khi không báo số cuối, nên khung chat dừng ở chiều cao cũ (thấp hơn):
   phía dưới ô nhập thừa một dải trống. Ở đây: chạm vào ô gõ thì nhắc đo lại thêm vài nhịp trong 1,5 giây.
   Đồng thời gửi số đo (một lần mỗi lần mở bàn phím) về máy chủ để dò nếu máy nào còn lệch: server/trinh-duyet/do-ban-phim.jsonl. */
(function () {
  "use strict";
  var vv = window.visualViewport;
  if (!vv || !window.matchMedia || !window.matchMedia("(max-width: 820px)").matches) return;
  function laOGo(a) {
    if (!a) return false;
    var t = (a.tagName || "").toLowerCase();
    return t === "textarea" || a.isContentEditable || (t === "input" && !/^(button|checkbox|radio|range|color|file|submit|reset|image|hidden)$/i.test(a.type || ""));
  }
  function nhac() { try { vv.dispatchEvent(new Event("resize")); } catch (e) {} }
  // ---- bù phần Safari iOS 26+ trừ thừa (chiều cao thanh công cụ đáy) khi bàn phím mở ----
  var nghi = { ih: 0 };
  function dinhTren() {
    try {
      var d = document.createElement("div");
      d.style.cssText = "position:fixed;top:0;left:-9px;width:1px;height:env(safe-area-inset-top,0px);visibility:hidden;pointer-events:none";
      document.body.appendChild(d); var h = d.offsetHeight; d.remove(); return h || 0;
    } catch (e) { return 0; }
  }
  function doNghi() {
    if (laOGo(document.activeElement) || document.body.classList.contains("kb-open")) return;
    if (Math.abs((vv.scale || 1) - 1) > 0.01) return;
    nghi.ih = Math.max(innerHeight, Math.round(vv.height)); nghi.tren = dinhTren();
  }
  function safari26() {
    var ua = navigator.userAgent, m = /Version\/(\d+)/.exec(ua);
    return /iPhone|iPad|iPod/.test(ua) && !/CriOS|FxiOS|EdgiOS/.test(ua) && navigator.standalone !== true && m && +m[1] >= 26;
  }
  var them = 0;
  function bu() {
    var kb = document.body.classList.contains("kb-open");
    them = 0;
    if (kb && safari26() && nghi.ih) {
      // Thanh công cụ đáy lúc chưa gõ = màn hình - thanh trạng thái - vùng trang. Trang bắt đầu DƯỚI thanh trạng thái (safe-area-top = 0,
      // số đo iPhone 22/11: màn 956, trang 796, đỉnh 0) nên phải trừ thanh trạng thái (~62 điểm trên máy có Dynamic Island, ~47 máy tai thỏ).
      var trangThai = nghi.tren || (screen.height >= 840 ? 62 : (screen.height >= 800 ? 47 : 20));
      var thanh = screen.height - trangThai - nghi.ih;
      // TẮT 22/11 16:00: số đo iPhone cho thấy khung nhìn Safari thật sự chỉ 376 điểm (trang cuộn tối đa đúng 420 = 796 - 376);
      // dải trống phía trên thanh địa chỉ nổi là vùng Safari tự giữ, không vẽ trang vào được. Bù thêm chỉ đẩy đáy ô nhập ra ngoài vùng thấy.
      // Giữ phép tính để ghi số đo (them_tinh) phục vụ dò lỗi, không áp dụng.
      nghi.them_tinh = (thanh > 30 && thanh < 150) ? thanh - 8 : 0;
    }
    document.documentElement.style.setProperty("--tdt-kb-them", them + "px");
    document.body.classList.toggle("tdt-kb-bu", them > 0);
  }
  // (22/11) Phép thử dải đỏ đã có kết quả: vùng trống trước đây LÀ trang web (Safari báo sai lúc bàn phím trượt); đo lại nhiều nhịp là đủ. Đã gỡ.
  doNghi();
  window.addEventListener("load", doNghi);
  window.addEventListener("orientationchange", function () { nghi.ih = 0; setTimeout(doNghi, 600); });
  vv.addEventListener("resize", function () { setTimeout(function () { doNghi(); bu(); }, 60); });
  document.addEventListener("focusout", function () { setTimeout(function () { bu(); doNghi(); }, 450); });
  var daGui = 0;
  function guiSoDo() {
    if (Date.now() - daGui < 20000) return;
    if (!document.body.classList.contains("kb-open") && vv.height > (nghi.ih || 0) - 120) return;     // chưa có bàn phím thật: không ghi
    daGui = Date.now();
    var o = [].slice.call(document.querySelectorAll(".hud-voice")).filter(function (e) { return e.getBoundingClientRect().height > 0; }).pop();
    var r = o ? o.getBoundingClientRect() : null;
    var d = { ih: innerHeight, iw: innerWidth, vh: Math.round(vv.height), vt: Math.round(vv.offsetTop), vpt: Math.round(vv.pageTop), sy: Math.round(scrollY),
              sh: screen.height, kb: document.body.classList.contains("kb-open"), cssvh: getComputedStyle(document.documentElement).getPropertyValue("--vv-h"),
              o_tren: r ? Math.round(r.top) : null, o_duoi: r ? Math.round(r.bottom) : null, sa: navigator.standalone === true, ua: navigator.userAgent.slice(0, 160),
              nghi_ih: nghi.ih, tren: nghi.tren, them: them, them_tinh: nghi.them_tinh || 0,
              ch: document.documentElement.clientHeight, sh2: document.documentElement.scrollHeight, dem: !!dem };
    try { fetch("/trinh-duyet/khung/do-ban-phim", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) }); } catch (e) {}
  }
  // Nhắc đo lại nhiều nhịp. (22/11 16:20) Trang chat khách tự đặt con trỏ vào ô nhập lúc mở (chưa có bàn phím): anh chạm vào ô thì bàn phím
  // bật mà KHÔNG có focusin, nên trước đây không nhắc, Safari giữ chiều cao sai và ô nhập bị che. Nay nhắc cả khi chạm ô gõ và khi màn hình
  // bị bàn phím thu nhỏ.
  var lanNhac = 0, dangNhac = false;
  function chuoiNhac() {
    if (Date.now() - lanNhac < 1600) return;
    lanNhac = Date.now();
    [120, 300, 550, 900, 1500].forEach(function (ms) { setTimeout(function () { dangNhac = true; nhac(); dangNhac = false; setTimeout(bu, 40); }, ms); });
    setTimeout(guiSoDo, 1700);
  }
  document.addEventListener("focusin", function (e) {
    if (!laOGo(e.target)) return;
    doNghi();
    chuoiNhac();
  });
  document.addEventListener("touchend", function (e) {
    var o = e.target && e.target.closest && e.target.closest("textarea,input,[contenteditable]");
    if (o && laOGo(o)) chuoiNhac();
  }, { passive: true });

  // (22/11 16:25, tìm ra từ số đo iPhone) Safari iOS không cho vùng nhìn thấy vượt quá ĐÁY TÀI LIỆU. Trang TISA cao đúng bằng màn hình (796),
  // bàn phím đẩy trang lên 420 nên Safari chỉ báo 376 điểm, phần dưới đáy trang hiện thành khoảng trống trên thanh địa chỉ. Lần có dải đỏ
  // thử nghiệm (trang dài 1.034) thì Safari báo đủ 474 và ô nhập sát thanh địa chỉ. Nên: anh CHẠM vào ô gõ thì kéo đáy tài liệu dài thêm
  // một đoạn vô hình (trước khi bàn phím bật), bàn phím tắt / rời ô thì bỏ.
  var dem = null;
  function noiDai(bat) {
    if (bat) {
      if (!dem) {
        dem = document.createElement("div");
        dem.setAttribute("aria-hidden", "true");
        dem.style.cssText = "position:absolute;left:0;width:1px;height:1px;pointer-events:none;visibility:hidden";
        document.body.appendChild(dem);
      }
      dem.style.top = (Math.max(document.documentElement.clientHeight, nghi.ih || 0) + 320) + "px";
    } else if (dem) {
      dem.remove(); dem = null;
    }
  }
  document.addEventListener("touchstart", function (e) {
    var o = e.target && e.target.closest && e.target.closest("textarea,input,[contenteditable]");
    if (o && laOGo(o)) noiDai(true);
  }, { passive: true, capture: true });
  document.addEventListener("focusout", function () {
    setTimeout(function () { if (!laOGo(document.activeElement)) noiDai(false); }, 500);
  });
  vv.addEventListener("resize", function () {
    if (dem && !dangNhac && nghi.ih && vv.height >= nghi.ih - 60 && !document.body.classList.contains("kb-open")) {
      setTimeout(function () { if (vv.height >= nghi.ih - 60) { noiDai(false); if (window.scrollY) window.scrollTo(0, 0); } }, 400);    // bàn phím đã tắt
    }
  });
  vv.addEventListener("resize", function () {
    if (dangNhac) return;            // chính mình vừa nhắc
    if (laOGo(document.activeElement) && nghi.ih && vv.height < nghi.ih - 120) chuoiNhac();
  });
})();
