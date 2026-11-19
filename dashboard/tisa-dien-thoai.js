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

  function quet() {
    var ds = document.querySelectorAll(".md-tablewrap > table.md-table:not(.dv-table)");
    for (var i = 0; i < ds.length; i++) { try { ganBang(ds[i]); } catch (e) {} }
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
