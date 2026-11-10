/* tisa-giao-dien.js - người dùng tự đặt tên và màu cho TISA BOT (Cài đặt > Chung > Giao diện thương hiệu).
   Lưu ở máy chủ (/tisa-giao-dien), máy chủ sinh /tisa-giao-dien.css: TISA BOT đọc --tisa-*, Đội Quân AI đọc --b1, --b2.
   Logo dùng lại chức năng tải ảnh có sẵn (ô Ảnh đại diện ngay phía trên).
   Đang kéo chọn màu thì xem trước trên cả trang; chưa bấm Lưu thì tải lại trang là về màu cũ. */
(function () {
  "use strict";
  var GOC = { ten: "TISA BOT", mau_nhan: "#ff6b35", mau_chinh: "#172f72" };
  var MAU_SAN = [
    { ten: "TISA", nhan: "#ff6b35", chinh: "#172f72" },
    { ten: "Đại dương", nhan: "#2563eb", chinh: "#0f1e3d" },
    { ten: "Ngọc bích", nhan: "#0d9488", chinh: "#123b3a" },
    { ten: "Lá non", nhan: "#16a34a", chinh: "#163a24" },
    { ten: "Hoa cà", nhan: "#8b5cf6", chinh: "#2a1857" },
    { ten: "Hồng sen", nhan: "#e11d74", chinh: "#3d1028" },
    { ten: "Đỏ son", nhan: "#dc2626", chinh: "#3a1414" },
    { ten: "Hổ phách", nhan: "#d97706", chinh: "#3a2a12" },
    { ten: "Than chì", nhan: "#f97316", chinh: "#1f2430" },
    { ten: "Bạc hà", nhan: "#10b981", chinh: "#1e293b" },
  ];
  var hien = Object.assign({}, GOC), luu = Object.assign({}, GOC);

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function hop(h) { return /^#[0-9a-f]{6}$/i.test(String(h || "")); }

  /* ---------- Tên ---------- */
  var tenGocRail = null, tieuGoc = null;
  function apTen(ten) {
    ten = String(ten || "").trim() || GOC.ten;
    var el = document.querySelector(".rail-brand-text");
    if (el) {
      if (tenGocRail === null) tenGocRail = el.innerHTML;
      if (ten === GOC.ten) el.innerHTML = tenGocRail;
      else el.textContent = ten;           // xuống hàng giữ nguyên nhờ white-space: pre-line
      var dong = ten.split("\n"), dai = Math.max.apply(null, dong.map(function (x) { return x.length; }));
      el.classList.toggle("dai", ten !== GOC.ten && (dong.length > 1 || ten.length > 11));
      el.classList.toggle("rat-dai", ten !== GOC.ten && (dai > 15 || ten.length > 24));
      var kt = el.closest(".rail-brand"); if (kt) kt.classList.toggle("ten-rat-dai", el.classList.contains("rat-dai"));
    }
    // Giữ tiêu đề gốc của trang ("… TISA BOT") để gõ tới đâu đổi tới đó, không bị kẹt ở chữ đầu tiên.
    var t = document.title, motDong = ten.replace(/\s*\n\s*/g, " ");
    if (t && t.indexOf("TISA BOT") >= 0) tieuGoc = t;
    if (tieuGoc) document.title = ten === GOC.ten ? tieuGoc : tieuGoc.split("TISA BOT").join(motDong);
    window.__TISA_TEN = ten;
  }
  var titleEl = document.querySelector("title");
  if (titleEl) new MutationObserver(function () { if (window.__TISA_TEN && window.__TISA_TEN !== GOC.ten && document.title.indexOf("TISA BOT") >= 0) apTen(window.__TISA_TEN); }).observe(titleEl, { childList: true });

  /* ---------- Phiên bản hiện cho người dùng: TiSaBot - V2.69 (số nội bộ VERSION giữ cho bộ cập nhật) ---------- */
  // Chấm xanh: đang chạy bản mới nhất. Có bản mới: chấm cam và nút "Cập nhật lên V2.70" mở Cài đặt → Cập nhật.
  function layJson(u) { return fetch(u, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }
  function moCapNhat() {
    try {
      var nav = Alpine.store("nav"); nav.settingsTab = "updates"; nav.go("settings");
      setTimeout(function () { var b = document.getElementById("settings-tab-updates"); if (b && b.getAttribute("aria-selected") !== "true") b.click(); }, 350);
    } catch (e) {}
  }
  /* Trang Cập nhật và hộp Thông báo ghi số nội bộ "v0.517.2": đổi sang tên V ("V2.68") cho khớp cách đặt tên mới.
     Chỉ đổi trong các khung đó, chỉ số có trong bảng (các lần phát + bản mới nhất trên mạng). */
  var BANG_V = {}, HOI_V = {}, RE_V = /\bv(\d+\.\d+\.\d+)\b/g;
  var VUNG_V = "#notificationPanel, #settings-panel, .cl-wrap, .upd-card";
  function tenV(m, v) {
    var b = BANG_V[v] || HOI_V[v];
    return b ? "V" + b : m;          // số lõi nhắc trong nội dung (không phải một lần phát) giữ nguyên
  }
  function quetV(goc) {
    if (!goc || !Object.keys(BANG_V).length) return;
    var vung = goc.nodeType === 1 && goc.matches && goc.matches(VUNG_V) ? [goc] : [];
    if (goc.querySelectorAll) vung = vung.concat(Array.prototype.slice.call(goc.querySelectorAll(VUNG_V)));
    if (goc.nodeType === 3 || (goc.closest && goc.closest(VUNG_V))) vung.push(goc.nodeType === 3 ? goc.parentNode : goc);
    vung.forEach(function (v) {
      if (!v) return;
      var w = document.createTreeWalker(v, NodeFilter.SHOW_TEXT), n, doi = [];
      while ((n = w.nextNode())) { RE_V.lastIndex = 0; if (RE_V.test(n.nodeValue)) doi.push(n); }
      doi.forEach(function (t) { var moi = t.nodeValue.replace(RE_V, tenV); if (moi !== t.nodeValue) t.nodeValue = moi; });
    });
  }
  var choQuet = null, gocQuet = [];
  new MutationObserver(function (ds) {
    ds.forEach(function (d) { gocQuet.push(d.target); });
    if (choQuet) return;
    choQuet = requestAnimationFrame(function () { var g = gocQuet; gocQuet = []; choQuet = null; g.forEach(quetV); });
  }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });

  /* Tên V của một số nội bộ ("0.526.5" -> "V2.76") cho dải báo bản mới (freshness.js). Hỏi máy chủ mỗi lần: trang đang mở
     có thể cũ hơn bản vừa cài nên bảng tên trong trang chưa có bản đó. Không tra được thì trả "" (dải giữ số nội bộ). */
  window.TISATenBan = function (ver) {
    ver = String(ver || "").replace(/^v/i, "");
    return layJson("/tisa-ban?moi=" + encodeURIComponent(ver)).then(function (j) {
      if (!j) return "";
      if (j.noi_bo === ver && j.ban) return "V" + j.ban;
      if (j.bang && j.bang[ver]) return "V" + j.bang[ver];
      return j.ban_moi ? "V" + j.ban_moi : "";
    }, function () { return ""; });
  };

  function napBan(o) {
    layJson("/version").then(function (v) {
      var moi = v && v.update_available && v.latest ? v.latest : "";
      return layJson("/tisa-ban" + (moi ? "?moi=" + encodeURIComponent(moi) : "")).then(function (j) {
        if (!j || !j.ban) return;
        BANG_V = j.bang || {}; if (j.noi_bo) BANG_V[j.noi_bo] = j.ban; if (moi && j.ban_moi) HOI_V[moi] = j.ban_moi;
        quetV(document.body);
        o.querySelector(".tb-v").textContent = "V" + j.ban;
        o.classList.toggle("co-moi", !!moi);
        var cap = o.querySelector(".tb-cap");
        cap.hidden = !moi;
        cap.querySelector(".tb-cap-chu").textContent = j.ban_moi ? "Cập nhật lên V" + j.ban_moi : "Có bản mới · Cập nhật";
        cap.title = "Mở Cài đặt → Cập nhật";
        o.querySelector(".tb-dong").title = moi ? "Đang dùng TiSaBot - V" + j.ban + ". Đã có bản mới." : "Đang dùng bản mới nhất: TiSaBot - V" + j.ban;
        o.hidden = false;
      });
    });
  }
  (function cho(lan) {
    var o = document.getElementById("tisaBan");
    if (!o) { if (lan < 50) setTimeout(function () { cho(lan + 1); }, 150); return; }
    o.querySelector(".tb-cap").onclick = moCapNhat;
    napBan(o);
    setInterval(function () { napBan(o); }, 30 * 60 * 1000);
  })(0);

  /* ---------- Màu ---------- */
  // Xem trước đặt biến màu thẳng lên <html> của TISA BOT và của khung Đội Quân AI (nếu đang mở).
  var BIEN = ["--tisa-nhan", "--tisa-nhan-sang", "--tisa-nhan-dam", "--tisa-chinh", "--tisa-chinh-dam",
    "--b1", "--b1l", "--b2", "--b2l", "--gold-ink", "--gold-wash", "--gold-line"];
  function docBang() {
    try { var f = window.TISADoiQuan && window.TISADoiQuan.khung(); return f && f.contentDocument; } catch (e) { return null; }
  }
  function xemTruoc(nhan, chinh) {
    var sang = "color-mix(in srgb, " + nhan + " 78%, #ffffff)";
    var v = {
      "--tisa-nhan": nhan, "--tisa-nhan-sang": sang, "--tisa-nhan-dam": "color-mix(in srgb, " + nhan + " 86%, #000000)",
      "--tisa-chinh": chinh, "--tisa-chinh-dam": "color-mix(in srgb, " + chinh + " 80%, #000000)",
      "--b1": nhan, "--b1l": sang, "--b2": chinh, "--b2l": "color-mix(in srgb, " + chinh + " 82%, #ffffff)",
      "--gold-ink": "color-mix(in srgb, " + nhan + " 72%, #000)", "--gold-wash": "color-mix(in srgb, " + nhan + " 9%, #fff)",
      "--gold-line": "color-mix(in srgb, " + nhan + " 32%, #fff)",
    };
    [document, docBang()].forEach(function (d) {
      if (!d || !d.documentElement) return;
      BIEN.forEach(function (k) { d.documentElement.style.setProperty(k, v[k]); });
    });
  }
  function boXemTruoc() {
    [document, docBang()].forEach(function (d) {
      if (!d || !d.documentElement) return;
      BIEN.forEach(function (k) { d.documentElement.style.removeProperty(k); });
    });
  }
  function napLaiCss(doc) {
    var links = (doc || document).querySelectorAll('link[href^="/tisa-giao-dien.css"]');
    Array.prototype.forEach.call(links, function (l) { l.href = "/tisa-giao-dien.css?t=" + Date.now(); });
  }
  function napLaiBang() {
    try {
      var f = window.TISADoiQuan && window.TISADoiQuan.khung();
      if (f && f.contentDocument) napLaiCss(f.contentDocument);
    } catch (e) { /* bảng chưa mở */ }
  }

  /* HSV <-> hex cho khung kéo chọn màu */
  function hex2rgb(h) { h = h.replace("#", ""); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function rgb2hex(r, g, b) { return "#" + [r, g, b].map(function (x) { var s = Math.round(Math.max(0, Math.min(255, x))).toString(16); return s.length < 2 ? "0" + s : s; }).join(""); }
  function rgb2hsv(r, g, b) {
    r /= 255; g /= 255; b /= 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn, h = 0;
    if (d) { if (mx === r) h = ((g - b) / d) % 6; else if (mx === g) h = (b - r) / d + 2; else h = (r - g) / d + 4; h *= 60; if (h < 0) h += 360; }
    return [h, mx ? d / mx : 0, mx];
  }
  function hsv2hex(h, s, v) {
    var c = v * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = v - c, rr = 0, gg = 0, bb = 0;
    if (h < 60) { rr = c; gg = x; } else if (h < 120) { rr = x; gg = c; } else if (h < 180) { gg = c; bb = x; }
    else if (h < 240) { gg = x; bb = c; } else if (h < 300) { rr = x; bb = c; } else { rr = c; bb = x; }
    return rgb2hex((rr + m) * 255, (gg + m) * 255, (bb + m) * 255);
  }

  /* Một ô chọn màu: mẫu màu, mã hex, khung kéo (độ đậm, độ sáng) và thanh sắc độ. */
  function oChonMau(goc, khoa, nhan, goiY, doi) {
    var hsv = rgb2hsv.apply(null, hex2rgb(hien[khoa]));
    var wrap = document.createElement("div");
    wrap.className = "tgd-o";
    wrap.innerHTML =
      '<div class="tgd-o-dau"><span class="tgd-mau" data-mau></span><div><b>' + esc(nhan) + '</b><small>' + esc(goiY) + '</small></div>' +
      '<input class="tgd-hex" maxlength="7" spellcheck="false" aria-label="Mã màu ' + esc(nhan) + '"></div>' +
      '<div class="tgd-sv" tabindex="0" aria-label="Kéo để chọn độ đậm và độ sáng"><span class="tgd-tro"></span></div>' +
      '<input type="range" class="tgd-hue" min="0" max="359" step="1" aria-label="Sắc độ ' + esc(nhan) + '">';
    goc.appendChild(wrap);
    var sv = wrap.querySelector(".tgd-sv"), tro = wrap.querySelector(".tgd-tro"), hue = wrap.querySelector(".tgd-hue");
    var o = wrap.querySelector(".tgd-hex"), mau = wrap.querySelector("[data-mau]");
    function ve(tuHex) {
      var h = tuHex ? hien[khoa] : hsv2hex(hsv[0], hsv[1], hsv[2]);
      if (!tuHex) hien[khoa] = h;
      sv.style.background = "linear-gradient(to top, #000, transparent), linear-gradient(to right, #fff, hsl(" + hsv[0] + ",100%,50%))";
      tro.style.left = (hsv[1] * 100) + "%"; tro.style.top = ((1 - hsv[2]) * 100) + "%";
      hue.value = Math.round(hsv[0]);
      if (document.activeElement !== o) o.value = h;
      mau.style.background = h;
      doi();
    }
    function keo(e) {
      var r = sv.getBoundingClientRect();
      hsv[1] = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width));
      hsv[2] = Math.max(0, Math.min(1, 1 - (e.clientY - r.top) / r.height));
      ve(false);
    }
    sv.addEventListener("pointerdown", function (e) { e.preventDefault(); sv.setPointerCapture(e.pointerId); keo(e); });
    sv.addEventListener("pointermove", function (e) { if (sv.hasPointerCapture(e.pointerId)) keo(e); });
    sv.addEventListener("keydown", function (e) {
      var d = { ArrowLeft: [-0.03, 0], ArrowRight: [0.03, 0], ArrowUp: [0, 0.03], ArrowDown: [0, -0.03] }[e.key];
      if (!d) return; e.preventDefault();
      hsv[1] = Math.max(0, Math.min(1, hsv[1] + d[0])); hsv[2] = Math.max(0, Math.min(1, hsv[2] + d[1])); ve(false);
    });
    hue.addEventListener("input", function () { hsv[0] = Number(hue.value); ve(false); });
    o.addEventListener("input", function () {
      var v = o.value.trim(); if (v && v[0] !== "#") v = "#" + v;
      if (!hop(v)) return;
      hien[khoa] = v.toLowerCase(); hsv = rgb2hsv.apply(null, hex2rgb(hien[khoa])); ve(true);
    });
    o.addEventListener("blur", function () { o.value = hien[khoa]; });
    ve(true);
    return { datMau: function (h) { hien[khoa] = h; hsv = rgb2hsv.apply(null, hex2rgb(h)); ve(true); } };
  }

  function veThe(goc) {
    goc.innerHTML =
      '<div class="popover-label">GIAO DIỆN THƯƠNG HIỆU</div>' +
      '<div class="opt-sub">Đổi tên và màu của TISA BOT theo thương hiệu của bạn. Đội Quân AI đổi theo. Logo đổi ở ô Ảnh đại diện phía trên.</div>' +
      '<label class="tgd-ten"><span>Tên hiển thị</span><textarea id="tgdTen" rows="1" maxlength="60" placeholder="TISA BOT" spellcheck="false"></textarea>' +
      '<small>Tên dài tự xuống hàng. Muốn tự ngắt dòng thì bấm <kbd>Shift</kbd> + <kbd>Enter</kbd>.</small></label>' +
      '<div class="tgd-nhan">Bộ màu có sẵn</div><div class="tgd-san" id="tgdSan"></div>' +
      '<div class="tgd-nhan">Tự chọn màu</div><div class="tgd-hai" id="tgdHai"></div>' +
      '<div class="js-actions qs-foot tgd-nut"><button class="gcard-btn" id="tgdLuu" disabled>Lưu</button>' +
      '<button class="gcard-btn ghost" id="tgdHuy" disabled>Bỏ thay đổi</button><button class="gcard-btn ghost" id="tgdGoc">Về mặc định</button></div>' +
      '<div class="opt-sub" id="tgdTrangThai"></div>';
    var ten = goc.querySelector("#tgdTen"), san = goc.querySelector("#tgdSan"), hai = goc.querySelector("#tgdHai");
    var btLuu = goc.querySelector("#tgdLuu"), btHuy = goc.querySelector("#tgdHuy"), tt = goc.querySelector("#tgdTrangThai");
    ten.value = hien.ten === GOC.ten ? "" : hien.ten;
    function coGian() { ten.style.height = "auto"; ten.style.height = Math.min(ten.scrollHeight + 2, 110) + "px"; }
    // Enter không xuống hàng (dễ lỡ tay); Shift + Enter mới xuống hàng, tối đa 3 dòng.
    ten.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" || e.isComposing) return;
      if (!e.shiftKey || ten.value.split("\n").length >= 3) e.preventDefault();
    });
    setTimeout(coGian, 0);
    function doi() {
      var khac = hien.mau_nhan !== luu.mau_nhan || hien.mau_chinh !== luu.mau_chinh || (ten.value.trim() || GOC.ten) !== luu.ten;
      btLuu.disabled = btHuy.disabled = !khac;
      // Chỉ đè biến khi màu khác bản đã lưu; giống nhau thì để tệp màu của máy chủ lo (đúng cả tông tối).
      if (hien.mau_nhan !== luu.mau_nhan || hien.mau_chinh !== luu.mau_chinh) xemTruoc(hien.mau_nhan, hien.mau_chinh); else boXemTruoc();
      Array.prototype.forEach.call(san.children, function (b) { b.classList.toggle("on", b.dataset.nhan === hien.mau_nhan && b.dataset.chinh === hien.mau_chinh); });
      tt.textContent = khac ? "Đang xem trước, bấm Lưu để giữ." : "";
    }
    var oNhan = oChonMau(hai, "mau_nhan", "Màu nhấn", "Nút bấm, điểm nhấn, nút Đội Quân AI", doi);
    var oChinh = oChonMau(hai, "mau_chinh", "Màu chính", "Thanh menu, tiêu đề", doi);
    MAU_SAN.forEach(function (m) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "tgd-bo"; b.title = m.ten; b.dataset.nhan = m.nhan; b.dataset.chinh = m.chinh;
      b.innerHTML = '<span style="background:' + m.chinh + '"><i style="background:' + m.nhan + '"></i></span><em>' + esc(m.ten) + '</em>';
      b.onclick = function () { oNhan.datMau(m.nhan); oChinh.datMau(m.chinh); };
      san.appendChild(b);
    });
    ten.addEventListener("input", function () { coGian(); apTen(ten.value); doi(); });
    btHuy.onclick = function () {
      hien = Object.assign({}, luu); ten.value = luu.ten === GOC.ten ? "" : luu.ten; coGian();
      oNhan.datMau(luu.mau_nhan); oChinh.datMau(luu.mau_chinh); apTen(luu.ten); boXemTruoc(); doi(); tt.textContent = "";
    };
    goc.querySelector("#tgdGoc").onclick = function () { ten.value = ""; coGian(); apTen(GOC.ten); oNhan.datMau(GOC.mau_nhan); oChinh.datMau(GOC.mau_chinh); };
    btLuu.onclick = async function () {
      btLuu.disabled = true; tt.textContent = "Đang lưu…";
      try {
        var r = await fetch("/tisa-giao-dien", { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ten: ten.value.trim(), mau_nhan: hien.mau_nhan, mau_chinh: hien.mau_chinh }) });
        var j = await r.json();
        if (!r.ok || !j.ok) throw new Error(j.error || ("HTTP " + r.status));
        luu = { ten: j.ten, mau_nhan: j.mau_nhan, mau_chinh: j.mau_chinh }; hien = Object.assign({}, luu);
        napLaiCss(); napLaiBang(); setTimeout(boXemTruoc, 400); apTen(luu.ten); doi();
        tt.textContent = "Đã lưu. Mọi máy mở TISA BOT này đều thấy giao diện mới.";
      } catch (e) {
        tt.textContent = "Chưa lưu được: " + (e && e.message ? e.message : e); btLuu.disabled = false;
      }
    };
    doi(); tt.textContent = "";
  }

  function thuVe() {
    var goc = document.getElementById("tisaGiaoDien");
    if (goc && !goc.dataset.xong) { goc.dataset.xong = "1"; veThe(goc); }
  }

  // Cuối menu điện thoại chỉ còn biểu tượng: nút Thư mục cần tên khi giữ ngón tay / đọc màn hình.
  (function () { var n = 0; (function dat() { var b = document.getElementById("pickFolderBtn");
    if (b) { if (!b.title) b.title = "Chọn thư mục bộ não"; if (!b.getAttribute("aria-label")) b.setAttribute("aria-label", "Chọn thư mục bộ não"); return; }
    if (n++ < 60) setTimeout(dat, 200); })(); })();

  // Điện thoại: nút thu gọn cạnh "Hệ thống" đóng ngăn kéo menu, không thu rail về dải icon như trên máy tính.
  document.addEventListener("click", function (e) {
    var nut = e.target && e.target.closest ? e.target.closest(".rail .rail-collapse-btn") : null;
    if (!nut || !window.matchMedia("(max-width: 860px)").matches) return;
    e.preventDefault(); e.stopPropagation();
    document.body.classList.remove("nav-open");
    var nen = document.querySelector(".nav-backdrop"); if (nen) nen.hidden = true;
  }, true);

  fetch("/tisa-giao-dien.json", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (j) {
    luu = { ten: j.ten || GOC.ten, mau_nhan: j.mau_nhan || GOC.mau_nhan, mau_chinh: j.mau_chinh || GOC.mau_chinh };
    hien = Object.assign({}, luu);
    apTen(luu.ten);
    var lan = 0;
    (function cho() { if (document.querySelector(".rail-brand-text") || lan++ > 50) { apTen(luu.ten); return; } setTimeout(cho, 120); })();
    thuVe();
    new MutationObserver(thuVe).observe(document.body, { childList: true, subtree: true });
  }).catch(function () {});
})();
