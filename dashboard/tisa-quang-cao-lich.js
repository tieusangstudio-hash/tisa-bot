/* tisa-quang-cao-lich.js - ô chọn ngày kiểu lịch cho trang Quảng Cáo (V2.78).
   Bấm vào ô ngày thì hiện lịch tháng trước và tháng này, chọn ngày đầu rồi ngày cuối, hoặc bấm một mốc nhanh bên trái.
   Dùng: TisaLich.gan(nutEl, { lay: () => ({kieu, tu, den}), khiChon: ({kieu, tu, den}) => ... }) */
(function () {
  "use strict";
  var MOC = [["hom-nay", "Hôm nay"], ["hom-qua", "Hôm qua"], ["7-ngay", "7 ngày qua"], ["30-ngay", "30 ngày qua"], ["thang-nay", "Tháng này"], ["thang-truoc", "Tháng trước"]];
  var THU = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function tu(s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function dmy(s) { var p = s.split("-"); return p[2] + "/" + p[1] + "/" + p[0]; }
  function cong(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function khoang(kieu) {
    var h = new Date(); h.setHours(0, 0, 0, 0);
    if (kieu === "hom-nay") return [h, h];
    if (kieu === "hom-qua") return [cong(h, -1), cong(h, -1)];
    if (kieu === "30-ngay") return [cong(h, -29), h];
    if (kieu === "thang-nay") return [new Date(h.getFullYear(), h.getMonth(), 1), h];
    if (kieu === "thang-truoc") return [new Date(h.getFullYear(), h.getMonth() - 1, 1), new Date(h.getFullYear(), h.getMonth(), 0)];
    return [cong(h, -6), h];
  }
  function nhan(v) {
    var m = MOC.filter(function (x) { return x[0] === v.kieu; })[0];
    if (m) return m[1];
    return v.tu && v.den ? (v.tu === v.den ? dmy(v.tu) : dmy(v.tu).slice(0, 5) + " đến " + dmy(v.den)) : "Chọn ngày";
  }

  function gan(nut, cb) {
    var pop = null, sel = null, thang = null;
    function dong() { if (pop) { pop.remove(); pop = null; document.removeEventListener("mousedown", ngoai, true); document.removeEventListener("keydown", phim, true); } nut.setAttribute("aria-expanded", "false"); }
    function ngoai(e) { if (pop && !pop.contains(e.target) && !nut.contains(e.target)) dong(); }
    function phim(e) { if (e.key === "Escape") dong(); }
    function chu() { var v = cb.lay(); nut.querySelector("[data-lich-nhan]").textContent = nhan(v); }
    function lich(nam, th) {
      var dau = new Date(nam, th, 1), so = new Date(nam, th + 1, 0).getDate(), lech = (dau.getDay() + 6) % 7, h = new Date(); h.setHours(0, 0, 0, 0);
      var s = '<div class="lich-thang"><div class="lich-ten">Tháng ' + (th + 1) + " / " + nam + '</div><div class="lich-luoi">' + THU.map(function (x) { return "<b>" + x + "</b>"; }).join("");
      for (var i = 0; i < lech; i++) s += "<span></span>";
      for (var d = 1; d <= so; d++) {
        var ng = new Date(nam, th, d), k = iso(ng), cls = "lich-ngay", dis = ng > h;
        if (sel.tu && sel.den && k >= sel.tu && k <= sel.den) cls += " trong";
        if (k === sel.tu) cls += " dau"; if (k === sel.den) cls += " cuoi";
        if (sel.tu && !sel.den && k === sel.tu) cls += " cuoi";
        if (k === iso(h)) cls += " nay";
        s += '<button type="button" class="' + cls + '" data-ng="' + k + '"' + (dis ? " disabled" : "") + ">" + d + "</button>";
      }
      return s + "</div></div>";
    }
    function ve() {
      var th2 = new Date(thang.getFullYear(), thang.getMonth() + 1, 1);
      var tomTat = sel.tu && sel.den ? dmy(sel.tu) + " đến " + dmy(sel.den) + " (" + (Math.round((tu(sel.den) - tu(sel.tu)) / 864e5) + 1) + " ngày)" : sel.tu ? "Từ " + dmy(sel.tu) + ", chọn ngày cuối" : "Chọn ngày đầu";
      var h = new Date(); h.setHours(0, 0, 0, 0);
      var troi = th2 >= new Date(h.getFullYear(), h.getMonth(), 1);
      pop.innerHTML = '<div class="lich-moc">' + MOC.map(function (m) { return '<button type="button" data-moc="' + m[0] + '" class="' + (cb.lay().kieu === m[0] ? "on" : "") + '">' + m[1] + "</button>"; }).join("") + "</div>" +
        '<div class="lich-chinh"><div class="lich-nav"><button type="button" data-di="-1" aria-label="Tháng trước">‹</button><span class="lich-tt">' + tomTat + '</span><button type="button" data-di="1" aria-label="Tháng sau"' + (troi ? " disabled" : "") + ">›</button></div>" +
        '<div class="lich-hai">' + lich(thang.getFullYear(), thang.getMonth()) + lich(th2.getFullYear(), th2.getMonth()) + "</div>" +
        '<div class="lich-chan"><button type="button" class="phu" data-huy>Đóng</button><button type="button" class="chinh" data-ap ' + (sel.tu && sel.den ? "" : "disabled") + ">Áp dụng</button></div></div>";
    }
    function mo() {
      if (pop) { dong(); return; }
      var v = cb.lay(), h = new Date(); h.setHours(0, 0, 0, 0);
      var kq = v.kieu === "tuy-chon" ? [tu(v.tu), tu(v.den)] : khoang(v.kieu);
      sel = { tu: iso(kq[0]), den: iso(kq[1]) };
      thang = new Date(h.getFullYear(), h.getMonth() - 1, 1);   // tháng trước và tháng này
      pop = document.createElement("div"); pop.className = "lich-pop"; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Chọn khoảng ngày");
      nut.parentNode.style.position = "relative"; nut.parentNode.appendChild(pop);
      nut.setAttribute("aria-expanded", "true"); ve();
      pop.addEventListener("click", function (e) {
        var m = e.target.closest("[data-moc]"), n = e.target.closest("[data-ng]"), d = e.target.closest("[data-di]");
        if (m) { var r = khoang(m.dataset.moc); dong(); cb.khiChon({ kieu: m.dataset.moc, tu: iso(r[0]), den: iso(r[1]) }); chu(); return; }
        if (d) { thang = new Date(thang.getFullYear(), thang.getMonth() + (+d.dataset.di), 1); ve(); return; }
        if (n) { var k = n.dataset.ng; if (!sel.tu || (sel.tu && sel.den)) sel = { tu: k, den: "" }; else if (k < sel.tu) sel = { tu: k, den: sel.tu }; else sel.den = k; ve(); return; }
        if (e.target.closest("[data-huy]")) { dong(); return; }
        if (e.target.closest("[data-ap]") && sel.tu && sel.den) { var a = sel; dong(); cb.khiChon({ kieu: "tuy-chon", tu: a.tu, den: a.den }); chu(); }
      });
      document.addEventListener("mousedown", ngoai, true); document.addEventListener("keydown", phim, true);
    }
    nut.addEventListener("click", mo);
    chu();
    return { capNhat: chu };
  }
  window.TisaLich = { gan: gan, nhan: nhan };
})();
