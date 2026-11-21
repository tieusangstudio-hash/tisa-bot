/* TISA BOT: TRÌNH XEM TỆP dạng cửa sổ popup + MENU CHUỘT PHẢI cho tệp (V2.95, chủ yêu cầu 17/11/2026).
   Dùng chung cho khung chat (thẻ tệp "Lưu tại: anh.png"), trang Kết quả của Đội Quân AI và bất kỳ chỗ nào gắn thuộc tính data-xt.

   Xem tệp: bấm vào thẻ tệp mở CỬA SỔ popup ngay trên trang (không mở tab mới): ảnh, video, âm thanh, PDF, văn bản. Nhiều tệp cùng nhóm
   (cùng một tin nhắn / cùng một kết quả) thì có mũi tên trái phải, phím mũi tên, dải ảnh thu nhỏ phía dưới và nút "Tải tất cả" (một file .zip).
   Chuột phải vào tệp: Xem, Tải về, Hiện trong thư mục trên máy, Mở bằng app, Đến nơi chứa tệp (trang Tệp tin), Sao chép đường dẫn, Mở tab mới.
   Mấy mục "trên máy" chỉ hiện khi đang dùng ngay trên máy chạy TISA BOT (GET /tisa-mo-tep/may-chu); dùng từ xa thì có "Đến nơi chứa tệp".

   Gắn vào chỗ khác: phần tử có data-xt-path="<đường dẫn trong bộ não>" (tuỳ chọn data-xt-brain, data-xt-name, data-xt-grp). Bấm phần tử có thêm
   data-xt-open thì mở trình xem; mọi phần tử data-xt-path đều có menu chuột phải. API: window.TISAXemTep.mo(ds, chiSo), .menu(x, y, tep, nhom). */
(function () {
  "use strict";
  if (window.TISAXemTep) return;

  var DUOI = {
    anh: /^(png|jpe?g|gif|webp|bmp|ico|svg|avif)$/, video: /^(mp4|webm|mov|m4v|mkv)$/, am: /^(mp3|wav|m4a|ogg|oga|opus|flac)$/,
    pdf: /^pdf$/, chu: /^(txt|md|csv|tsv|json|jsonl|log|ya?ml|xml|ini|toml|html?|css|js|ts|py|sh)$/
  };
  var TAI_ZIP_TOI_DA = 300;
  var mayChu = null;   // true: đang dùng ngay trên máy chạy TISA BOT

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function duoi(ten) { var m = /\.([A-Za-z0-9]{1,8})$/.exec(String(ten || "").split(/[?#]/)[0]); return m ? m[1].toLowerCase() : ""; }
  function loai(e) { for (var k in DUOI) if (DUOI[k].test(e)) return k; return "khac"; }
  function kb(b) { b = Number(b) || 0; return b >= 1048576 ? (b / 1048576).toFixed(1) + " MB" : b >= 1024 ? Math.round(b / 1024) + " KB" : b ? b + " B" : ""; }
  function urlRaw(brain, path, dl) { return "/files/raw?brain=" + encodeURIComponent(brain || "brain") + "&path=" + encodeURIComponent(path) + (dl ? "&dl=1" : ""); }

  /* Chuẩn hoá một mô tả tệp: {path, brain, name, size, url, dl} -> thêm ext, kind. */
  function chuan(t) {
    if (t.ngoai) {   // ảnh/tệp KHÔNG nằm trong bộ não (link /_blob, ảnh khách gửi, ảnh tạo ra...): xem và lưu theo chính đường link
      var nm = t.name || "", e0;
      if (!nm) { try { nm = decodeURIComponent(new URL(t.url, location.href).pathname.split("/").pop() || ""); } catch (x) { nm = ""; } }
      e0 = duoi(nm) || t.ext || "";
      if (!nm || !duoi(nm)) nm = (nm || "tep") + (e0 ? "" : "." + (t.kindGoi === "video" ? "mp4" : "jpg"));
      e0 = duoi(nm);
      return { path: t.url, brain: "", ngoai: true, name: nm, ext: e0, kind: t.kindGoi || loai(e0), size: t.size || 0, url: t.url, dl: t.dl || t.url };
    }
    var path = String(t.path || "").replace(/^\.?\//, ""), name = t.name || path.split("/").pop() || "tệp", e = duoi(name);
    return { path: path, brain: t.brain || "brain", name: name, ext: e, kind: loai(e), size: t.size || 0, url: t.url || urlRaw(t.brain, path, 0), dl: t.dl || urlRaw(t.brain, path, 1) };
  }
  function trongNao(ds) { return (ds || []).filter(function (t) { return !t.ngoai; }); }
  function docMayChu() {
    if (mayChu !== null) return Promise.resolve(mayChu);
    return fetch("/tisa-mo-tep/may-chu", { credentials: "same-origin" }).then(function (r) { return r.json(); })
      .then(function (j) { mayChu = !!(j && j.may_chu); return mayChu; }).catch(function () { mayChu = false; return false; });
  }
  docMayChu();

  /* ---------------------------------------------------------------- hành động trên một tệp */
  function taiVe(t) { var a = document.createElement("a"); a.href = t.dl; a.download = t.name; a.style.display = "none"; document.body.appendChild(a); a.click(); setTimeout(function () { a.remove(); }, 400); }
  function taiTatCa(ds, ten) {
    ds = trongNao(ds); if (!ds.length) { bao("Các tệp này không gói .zip được, anh lưu từng tệp nhé"); return; }
    var u ="/tisa-mo-tep/zip?brain=" + encodeURIComponent(ds[0].brain) + "&name=" + encodeURIComponent(ten || "tep-ket-qua") + ds.slice(0, TAI_ZIP_TOI_DA).map(function (t) { return "&p=" + encodeURIComponent(t.path); }).join("");
    var a = document.createElement("a"); a.href = u; a.download = (ten || "tep-ket-qua") + ".zip"; a.style.display = "none"; document.body.appendChild(a); a.click(); setTimeout(function () { a.remove(); }, 400);
  }
  function moMay(t, cach) {
    return fetch("/tisa-mo-tep", { method: "POST", credentials: "same-origin", headers: { "content-type": "application/json" }, body: JSON.stringify({ brain: t.brain, path: t.path, cach: cach }) })
      .then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (j) { if (!j || !j.ok) bao((j && j.error) || "Không mở được tệp"); else bao(cach === "thu-muc" ? "Đã hiện tệp trong thư mục trên máy" : "Đã mở bằng ứng dụng trên máy"); })
      .catch(function () { bao("Không mở được tệp"); });
  }
  function denNoiChua(t) {   // trang Tệp tin của TISA BOT, tới đúng thư mục chứa tệp (dùng được cả khi truy cập từ xa)
    var top = window.top || window;
    dong();
    try { if (typeof top.TISAOpenFiles === "function") { top.TISAOpenFiles(t.path); bao("Đã chuyển tới thư mục chứa tệp ở trang Tệp tin"); return; } } catch (e) {}
    try { top.location.hash = "#open=" + encodeURIComponent(t.path); } catch (e2) { location.hash = "#open=" + encodeURIComponent(t.path); }
  }
  function chepDuongDan(t) {
    var s = t.ngoai ? new URL(t.url, location.href).href : t.path; try { navigator.clipboard.writeText(s).then(function () { bao("Đã sao chép đường dẫn"); }, function () { bao(s); }); } catch (e) { bao(s); }
  }
  function tabMoi(t) { window.open(t.url, "_blank", "noopener"); }

  /* ---------------------------------------------------------------- ĐIỆN THOẠI: bấm Tải về hiện bảng chọn cách lưu (chủ 17/11/2026)
     iPhone: "Lưu vào Ảnh" mở bảng chia sẻ của máy (có Lưu hình ảnh / Lưu video, gửi Zalo, Messenger). Android: tải thẳng về máy, ảnh tự vào Thư viện.
     Tệp được tải sẵn khi bảng vừa mở để lúc bấm nút chia sẻ vẫn còn "cú chạm của người dùng" (Safari bắt buộc). */
  var MIME = { jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", gif: "image/gif", webp: "image/webp", heic: "image/heic", avif: "image/avif", svg: "image/svg+xml", bmp: "image/bmp",
    mp4: "video/mp4", mov: "video/quicktime", m4v: "video/x-m4v", webm: "video/webm", mp3: "audio/mpeg", m4a: "audio/mp4", wav: "audio/wav", pdf: "application/pdf" };
  function laDienThoai() { try { return matchMedia("(pointer:coarse)").matches || innerWidth <= 720; } catch (e) { return innerWidth <= 720; } }
  function laIOS() { return /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1); }
  function coChiaSeTep() { try { return !!(navigator.share && navigator.canShare && navigator.canShare({ files: [new File(["x"], "x.png", { type: "image/png" })] })); } catch (e) { return false; } }
  var GIOI_HAN_CHIA_SE = 20, GIOI_HAN_MB = 180;
  function layFile(t) {
    return fetch(t.url, { credentials: "same-origin" }).then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.blob(); })
      .then(function (b) { return new File([b], t.name, { type: MIME[t.ext] || b.type || "application/octet-stream" }); });
  }
  var sheet = null;
  function dongSheet() { if (sheet) { sheet.el.remove(); sheet = null; } }
  function luuSheet(t, nhom) {
    chenCss(); dongSheet(); t = chuan(t); nhom = (nhom || []).map(chuan);
    var media = function (x) { return x.kind === "anh" || x.kind === "video"; };
    var share = coChiaSeTep(), ios = laIOS(), loaiTu = t.kind === "anh" ? "ảnh" : t.kind === "video" ? "video" : "tệp";
    var nhomMedia = nhom.length > 1 ? nhom.filter(media).slice(0, GIOI_HAN_CHIA_SE) : [];
    var zipDuoc = trongNao(nhom).length > 1;
    var hang = [];
    if (share) hang.push(["chia", media(t) ? (ios ? "Lưu " + loaiTu + " vào thư viện Ảnh" : "Lưu hoặc gửi " + loaiTu) : "Lưu vào Tệp hoặc gửi đi", ios && media(t) ? "Chọn \"Lưu hình ảnh\" / \"Lưu video\", hoặc gửi Zalo, Messenger" : "Mở bảng chia sẻ của điện thoại", true]);
    hang.push(["tai", ios ? "Tải về thư mục Tệp" : "Tải " + loaiTu + " về điện thoại", ios ? "Vào app Tệp, mục Tải về để xem" : (media(t) ? "Tự hiện trong Thư viện ảnh / mục Tải xuống" : "Nằm trong mục Tải xuống"), !share]);
    if (t.kind === "anh") hang.push(["mo", "Mở ảnh gốc", "Nhấn giữ vào ảnh để lưu theo cách của trình duyệt", false]);
    if (share && nhomMedia.length > 1) hang.push(["chia_het", "Lưu cả " + nhomMedia.length + " ảnh/video vào máy", ios ? "Một lần chọn \"Lưu " + nhomMedia.length + " mục\"" : "Mở bảng chia sẻ cho cả bộ", false]);
    if (zipDuoc) hang.push(["zip", "Tải tất cả (" + trongNao(nhom).length + ") thành 1 file .zip", "Hợp với máy tính hoặc gửi cho người khác", false]);
    var lop = document.createElement("div"); lop.className = "xt-sh-lop" + tongSang();
    lop.innerHTML = '<div class="xt-sh" role="dialog" aria-modal="true" aria-label="Lưu tệp"><div class="xt-sh-keo"></div><div class="xt-sh-dau">' +
      (t.kind === "anh" ? '<img src="' + esc(t.url) + '" alt="">' : '<span class="xt-ext">' + esc(t.ext || "tệp") + "</span>") + '<b>' + esc(t.name) + "</b></div>" +
      hang.map(function (h) { return '<button type="button" class="xt-sh-n' + (h[3] ? " xt-chinh" : "") + '" data-sh="' + h[0] + '"' + (h[0] === "chia" || h[0] === "chia_het" ? " disabled" : "") + ">" + IC.tai + '<span><b>' + esc(h[1]) + "</b><small>" + esc(h[2]) + "</small></span></button>"; }).join("") +
      '<button type="button" class="xt-sh-n xt-sh-huy" data-sh="huy">Hủy</button></div>';
    document.body.appendChild(lop);
    sheet = { el: lop, file: null, files: null };
    var s = sheet;
    function sanSang(ma, ok) { var b = lop.querySelector('[data-sh="' + ma + '"]'); if (!b) return; b.disabled = !ok; if (!ok) { var sm = b.querySelector("small"); if (sm) sm.textContent = "Không chuẩn bị được, anh dùng cách khác"; } }
    if (share) {
      layFile(t).then(function (f) { s.file = f; sanSang("chia", true); }, function () { sanSang("chia", false); });
      if (nhomMedia.length > 1) Promise.all(nhomMedia.map(layFile)).then(function (fs) {
        var mb = fs.reduce(function (a, f) { return a + f.size; }, 0) / 1048576;
        if (mb > GIOI_HAN_MB || !navigator.canShare({ files: fs })) { sanSang("chia_het", false); return; }
        s.files = fs; sanSang("chia_het", true);
      }, function () { sanSang("chia_het", false); });
    }
    lop.addEventListener("click", function (e) {
      if (e.target === lop) { dongSheet(); return; }
      var b = e.target.closest && e.target.closest("[data-sh]"); if (!b || b.disabled) return;
      var a = b.getAttribute("data-sh");
      if (a === "huy") { dongSheet(); return; }
      if (a === "chia" || a === "chia_het") {
        var fs = a === "chia" ? [s.file] : s.files;
        navigator.share({ files: fs }).then(function () { dongSheet(); bao(a === "chia" ? "Xong" : "Đã gửi " + fs.length + " mục"); }, function (err) { if (err && err.name !== "AbortError") bao("Điện thoại chưa cho lưu cách này, anh thử Tải về"); });
        return;
      }
      dongSheet();
      if (a === "tai") { taiVe(t); bao(ios ? "Đang tải, xem trong app Tệp > Tải về" : "Đang tải về điện thoại"); }
      else if (a === "mo") tabMoi(t);
      else if (a === "zip") taiTatCa(nhom, (st && st.ten) || "tep-ket-qua");
    });
  }
  // Nút Tải về dùng chung: máy tính tải luôn, điện thoại hiện bảng chọn cách lưu.
  function taiThongMinh(t, nhom) { if (laDienThoai()) luuSheet(t, nhom); else taiVe(chuan(t)); }

  /* ---------------------------------------------------------------- thông báo nhỏ */
  var toastEl = null, toastT = 0;
  function bao(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "xt-toast" + tongSang(); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.className = "xt-toast" + tongSang() + " on"; clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("on"); }, 2600);
  }

  /* ---------------------------------------------------------------- giao diện */
  var CSS = "code.xt-code{cursor:pointer;text-decoration:underline;text-decoration-color:rgba(255,107,53,.7);text-underline-offset:3px;border-radius:6px}code.xt-code:hover{background:rgba(255,107,53,.14)}code.xt-code::after{content:\" \\25B6\";font-size:.8em;color:#ff6b35}"
    + ".xt-lop,.xt-menu,.xt-toast{--xt-vei:rgba(7,11,28,.9);--xt-nen-cua:#0f1530;--xt-chu:#eef1ff;--xt-mo:#9aa6d6;--xt-vien:rgba(255,255,255,.1);--xt-vien2:rgba(255,255,255,.18);--xt-nut:rgba(255,255,255,.06);--xt-nut-h:rgba(255,255,255,.14);--xt-san:#070a1c;--xt-dai:#0b1026;--xt-tn:#1b2350;--xt-tn-c:#b9c7ff;--xt-ext:rgba(124,150,255,.2);--xt-ext-c:#b9c7ff;--xt-mt:rgba(15,21,48,.72);--xt-mt-h:rgba(15,21,48,.95);--xt-mt-c:#fff;--xt-menu:#12183a;--xt-van:#e5e9ff;--xt-bong:rgba(0,0,0,.7)}"
    + ".xt-sang{--xt-vei:rgba(60,70,110,.7);--xt-nen-cua:#ffffff;--xt-chu:#1b2350;--xt-mo:#6b7599;--xt-vien:rgba(30,40,90,.12);--xt-vien2:rgba(30,40,90,.22);--xt-nut:rgba(30,40,90,.05);--xt-nut-h:rgba(30,40,90,.11);--xt-san:#eef1fa;--xt-dai:#f4f6fc;--xt-tn:#e3e8f6;--xt-tn-c:#4a5a99;--xt-ext:rgba(60,90,200,.12);--xt-ext-c:#3a4fa8;--xt-mt:rgba(255,255,255,.85);--xt-mt-h:#ffffff;--xt-mt-c:#1b2350;--xt-menu:#ffffff;--xt-van:#1f2a55;--xt-bong:rgba(30,40,90,.25)}"
    + ".xt-lop{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:clamp(8px,2.5vw,32px);background:var(--xt-vei);animation:xtVao .14s ease-out}"
    + "@keyframes xtVao{from{opacity:0}to{opacity:1}}"
    + "body:has(.xt-lop) #tisaPet,body:has(.xt-lop) .pet{visibility:hidden!important;animation:none!important}"
    + ".xt-cua{display:flex;flex-direction:column;width:min(1180px,100%);height:min(860px,100%);background:var(--xt-nen-cua);color:var(--xt-chu);border:1px solid var(--xt-vien2);border-radius:18px;overflow:hidden;box-shadow:0 30px 80px -20px var(--xt-bong);font-family:inherit}"
    + ".xt-dau{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid var(--xt-vien);flex:none}"
    + ".xt-ext{flex:none;padding:3px 9px;border-radius:7px;background:var(--xt-ext);color:var(--xt-ext-c);font:800 11.5px/1.4 inherit;letter-spacing:.06em;text-transform:uppercase}"
    + ".xt-ten{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:15px;font-weight:700}"
    + ".xt-dem{flex:none;color:var(--xt-mo);font-size:13px;font-weight:600}"
    + ".xt-nut{flex:none;display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 13px;border-radius:11px;border:1px solid var(--xt-vien2);background:var(--xt-nut);color:var(--xt-chu);font:600 13.5px/1 inherit;cursor:pointer;white-space:nowrap}"
    + ".xt-nut:hover{background:var(--xt-nut-h)}.xt-nut:focus-visible{outline:2px solid #ff8a5c;outline-offset:2px}"
    + ".xt-nut.xt-chinh{background:#ff6b35;border-color:#ff6b35;color:#fff}.xt-nut.xt-chinh:hover{background:#ff7d4d}"
    + ".xt-nut svg{width:16px;height:16px;flex:none}"
    + ".xt-dong{padding:0;width:36px;justify-content:center;font-size:20px}"
    + ".xt-san{position:relative;flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center;background:var(--xt-san)}"
    + ".xt-san img,.xt-san video{max-width:100%;max-height:100%;object-fit:contain;display:block}.xt-san img{cursor:zoom-in}.xt-san img.xt-to{max-width:none;max-height:none;cursor:zoom-out}"
    + ".xt-san.xt-cuon{overflow:auto;align-items:flex-start;justify-content:flex-start}.xt-san audio{width:min(560px,92%)}.xt-san iframe{width:100%;height:100%;border:0;background:#fff}"
    + ".xt-van{margin:0;padding:18px 22px;width:100%;height:100%;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;font:13.5px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--xt-van);box-sizing:border-box}"
    + ".xt-khac{display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center;padding:24px;max-width:520px}.xt-khac b{font-size:17px}.xt-khac span{color:var(--xt-mo);font-size:14px;line-height:1.5}.xt-khac .xt-hang{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}"
    + ".xt-mt{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:64px;border-radius:14px;border:1px solid var(--xt-vien2);background:var(--xt-mt);color:var(--xt-mt-c);font-size:26px;cursor:pointer;z-index:3;display:flex;align-items:center;justify-content:center}"
    + ".xt-mt:hover{background:var(--xt-mt-h)}.xt-mt.xt-t{left:12px}.xt-mt.xt-p{right:12px}"
    + ".xt-dai{display:flex;gap:8px;padding:10px 12px;overflow-x:auto;border-top:1px solid var(--xt-vien);background:var(--xt-dai);flex:none;scrollbar-width:thin}"
    + ".xt-tn{position:relative;flex:none;width:78px;height:58px;border-radius:9px;overflow:hidden;border:2px solid transparent;background:var(--xt-tn);cursor:pointer;padding:0;display:flex;align-items:center;justify-content:center;color:var(--xt-tn-c);font:800 11px/1 inherit;text-transform:uppercase}"
    + ".xt-tn img,.xt-tn video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}.xt-tn.on{border-color:#ff6b35}.xt-tn:hover{border-color:rgba(255,138,92,.6)}"
    + ".xt-tn i{position:absolute;right:3px;bottom:3px;padding:1px 5px;border-radius:5px;background:rgba(0,0,0,.65);font:700 9.5px/1.4 inherit;font-style:normal;color:#fff}"
    + ".xt-menu{position:fixed;z-index:2147483200;min-width:250px;max-width:340px;padding:6px;border-radius:13px;background:var(--xt-menu);color:var(--xt-chu);border:1px solid var(--xt-vien2);box-shadow:0 22px 50px -12px var(--xt-bong);font-family:inherit}"
    + ".xt-menu .xt-m{display:flex;align-items:center;gap:10px;width:100%;padding:9px 11px;border:0;border-radius:8px;background:none;color:inherit;font:500 14px/1.2 inherit;text-align:left;cursor:pointer}"
    + ".xt-menu .xt-m:hover,.xt-menu .xt-m:focus-visible{background:var(--xt-nut-h);outline:none}.xt-menu .xt-m small{margin-left:auto;color:var(--xt-mo);font-size:11.5px}"
    + ".xt-menu .xt-m svg{width:16px;height:16px;flex:none;opacity:.9}.xt-menu hr{border:0;border-top:1px solid var(--xt-vien);margin:5px 4px}.xt-menu .xt-t{padding:7px 11px 5px;color:var(--xt-mo);font-size:12px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    + ".xt-the{margin:14px 0 2px;padding:10px 12px 12px;border:1px solid var(--mm-line2,rgba(120,130,180,.3));border-radius:14px;background:var(--mm-soft,rgba(120,130,180,.08))}"
    + ".xt-the-h{display:flex;align-items:center;gap:8px;margin-bottom:9px;font-size:13px}.xt-the-h b{font-weight:700}.xt-the-h .xt-sl{flex:none;white-space:nowrap;padding:1px 8px;border-radius:999px;background:var(--mm-soft2,rgba(120,130,180,.2));font-weight:700;font-size:12px}"
    + ".xt-the-h .xt-tatca{margin-left:auto;display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 11px;border-radius:9px;border:1px solid var(--mm-line2,rgba(120,130,180,.4));background:var(--mm-card,transparent);color:inherit;font:600 12.5px/1 inherit;cursor:pointer}"
    + ".xt-the-h .xt-tatca:hover{border-color:#ff6b35}.xt-the-h .xt-tatca svg{width:15px;height:15px}"
    + ".xt-the-l{display:flex;gap:10px;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}"
    + ".xt-thu .xt-the-l{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior:contain}.xt-thu.xt-luoi .xt-the-l{flex-wrap:wrap;max-height:400px;overflow-y:auto;overflow-x:hidden}"
    + ".xt-thu .xt-grp-h{display:none}.xt-thu.xt-luoi .xt-grp-h{display:block}"
    + ".xt-the-h .xt-doi{margin-left:auto;height:30px;padding:0 11px;border-radius:9px;border:1px solid var(--mm-line2,rgba(120,130,180,.4));background:none;color:inherit;font-weight:600;font-size:12.5px;cursor:pointer;white-space:nowrap}.xt-the-h .xt-doi+.xt-tatca{margin-left:0}"
    + ".xt-grp-h{flex:0 0 100%;margin:8px 0 0;padding-top:6px;font-weight:700;font-size:12.5px;line-height:1.3;letter-spacing:.02em;color:var(--mm-muted,#8a93b8);border-top:1px solid var(--mm-line,rgba(120,130,180,.25))}.xt-grp-h:first-child{margin-top:0;padding-top:0;border-top:0}"
    + ".xt-the-h b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}.xt-the-h .xt-tatca{white-space:nowrap;flex:none}"
    + "@media (max-width:720px){.xt-the{padding:9px 10px 10px}.xt-the-h{font-size:12.5px;flex-wrap:wrap;row-gap:7px}.xt-the-h b{flex:1 1 100%}.xt-the-h .xt-doi,.xt-the-h .xt-tatca{height:32px}.xt-card{width:112px!important}.xt-card .xt-th{height:74px!important}.xt-card .xt-nm{font-size:11.5px}.xt-the-h .xt-tatca{height:32px}}"
    + ".xt-card{flex:none;width:132px;padding:0;border:1px solid var(--mm-line2,rgba(120,130,180,.35));border-radius:11px;overflow:hidden;background:var(--mm-card,#fff);color:inherit;text-align:left;cursor:pointer;font:inherit}"
    + ".xt-card:hover{border-color:#ff6b35}.xt-card:focus-visible{outline:2px solid #ff8a5c;outline-offset:2px}"
    + ".xt-card .xt-th{position:relative;display:flex;align-items:center;justify-content:center;height:84px;background:rgba(120,130,180,.14);font:800 13px/1 inherit;text-transform:uppercase;color:#7c8cc8}"
    + ".xt-card .xt-th img,.xt-card .xt-th video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}"
    + ".xt-card .xt-th i{position:absolute;right:5px;bottom:5px;padding:1px 6px;border-radius:6px;background:rgba(0,0,0,.65);color:#fff;font:700 10px/1.5 inherit;font-style:normal}"
    + ".xt-card .xt-nm{display:block;padding:7px 9px 8px;font-size:12px;font-weight:600;line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    + ".xt-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);z-index:2147483300;padding:10px 16px;border-radius:12px;background:var(--xt-menu);color:var(--xt-chu);border:1px solid var(--xt-vien2);font:600 13.5px/1.3 inherit;opacity:0;pointer-events:none;transition:opacity .18s,transform .18s}"
    + ".xt-toast.on{opacity:1;transform:translateX(-50%) translateY(0)}"
    + ".xt-chan{display:none}"
    /* Điện thoại: MỘT kiểu xem toàn màn hình — đầu chỉ tên + số thứ tự + nút đóng, ảnh chiếm giữa, dải ảnh nhỏ, thanh nút to ở đáy (Lưu ảnh / Tải tất cả / ⋯). */
    + "@media (max-width:720px),(pointer:coarse) and (max-width:1024px){.xt-lop{padding:0}.xt-cua{width:100%;height:100%;height:100dvh;border-radius:0;border:0}"
    + ".xt-dau{padding:calc(8px + env(safe-area-inset-top)) 10px 8px 12px;gap:8px}.xt-ten{font-size:14px}.xt-pc{display:none}.xt-dong{width:40px;height:40px;font-size:24px;border-radius:12px}"
    + ".xt-mt{width:36px;height:48px;border-radius:12px;font-size:22px;opacity:.85}.xt-mt.xt-t{left:6px}.xt-mt.xt-p{right:6px}"
    + ".xt-dai{padding:8px 10px;gap:6px}.xt-tn{width:58px;height:44px;border-radius:8px}"
    + ".xt-chan{display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));border-top:1px solid var(--xt-vien);background:var(--xt-nen-cua);flex:none}"
    + ".xt-chan .xt-nut{height:48px;border-radius:14px;font-size:15px;justify-content:center;padding:0 14px}.xt-chan .xt-chinh{flex:1 1 auto}.xt-chan .xt-it{width:48px;padding:0;font-size:20px}.xt-chan svg{width:19px;height:19px}"
    + ".xt-menu{min-width:min(300px,calc(100vw - 16px))}.xt-menu .xt-m{padding:13px 12px;font-size:15px}}"
    /* Bảng chọn cách lưu (điện thoại) */
    + ".xt-sh-lop{--xt-vei:rgba(7,11,28,.6);--xt-nen-cua:#12183a;--xt-chu:#eef1ff;--xt-mo:#9aa6d6;--xt-vien:rgba(255,255,255,.1);--xt-nut:rgba(255,255,255,.06);--xt-nut-h:rgba(255,255,255,.12);--xt-ext:rgba(124,150,255,.2);--xt-ext-c:#b9c7ff;"
    + "position:fixed;inset:0;z-index:2147483400;display:flex;align-items:flex-end;justify-content:center;background:var(--xt-vei);animation:xtVao .14s ease-out}"
    + ".xt-sh-lop.xt-sang{--xt-vei:rgba(40,50,90,.4);--xt-nen-cua:#ffffff;--xt-chu:#1b2350;--xt-mo:#6b7599;--xt-vien:rgba(30,40,90,.12);--xt-nut:rgba(30,40,90,.04);--xt-nut-h:rgba(30,40,90,.09);--xt-ext:rgba(60,90,200,.12);--xt-ext-c:#3a4fa8}"
    + ".xt-sh{width:min(520px,100%);max-height:88vh;overflow:auto;padding:8px 12px calc(12px + env(safe-area-inset-bottom));border-radius:20px 20px 0 0;background:var(--xt-nen-cua);color:var(--xt-chu);display:flex;flex-direction:column;gap:8px;animation:xtLen .2s ease-out;font-family:inherit}"
    + "@keyframes xtLen{from{transform:translateY(30px);opacity:.4}to{transform:none;opacity:1}}"
    + ".xt-sh-keo{width:40px;height:5px;border-radius:9px;background:var(--xt-vien);margin:2px auto 4px;background:rgba(127,135,170,.45)}"
    + ".xt-sh-dau{display:flex;align-items:center;gap:10px;padding:2px 2px 6px}.xt-sh-dau img{width:46px;height:46px;border-radius:10px;object-fit:cover;flex:none}.xt-sh-dau b{font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}"
    + ".xt-sh-n{display:flex;align-items:center;gap:12px;width:100%;min-height:58px;padding:10px 14px;border:1px solid var(--xt-vien);border-radius:14px;background:var(--xt-nut);color:var(--xt-chu);text-align:left;font:inherit;cursor:pointer}"
    + ".xt-sh-n:active{background:var(--xt-nut-h)}.xt-sh-n svg{width:20px;height:20px;flex:none}.xt-sh-n span{display:flex;flex-direction:column;gap:3px;min-width:0}.xt-sh-n b{font-size:15.5px;font-weight:700}.xt-sh-n small{font-size:12.5px;color:var(--xt-mo);line-height:1.35}"
    + ".xt-sh-n.xt-chinh{background:#ff6b35;border-color:#ff6b35;color:#fff}.xt-sh-n.xt-chinh small{color:rgba(255,255,255,.85)}.xt-sh-n:disabled{opacity:.55;cursor:progress}"
    + ".xt-sh-huy{justify-content:center;font-weight:700;font-size:15.5px;margin-top:2px}"
    + "@media (prefers-reduced-motion:reduce){.xt-lop,.xt-sh-lop,.xt-sh{animation:none}.xt-toast{transition:none}}";
  // Tông sáng/tối theo giao diện đang dùng của TISA BOT (html[data-theme]); không có thì theo hệ thống.
  function tongSang() {
    var t = ""; try { t = document.documentElement.getAttribute("data-theme") || (window.parent !== window ? window.parent.document.documentElement.getAttribute("data-theme") : "") || ""; } catch (e) {}
    if (!t) t = (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) ? "light" : "dark";
    return t === "light" ? " xt-sang" : "";
  }
  function chenCss() { if (document.getElementById("xt-css")) return; var s = document.createElement("style"); s.id = "xt-css"; s.textContent = CSS; (document.head || document.documentElement).appendChild(s); }

  var IC = {
    tai: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M5 21h14"/></svg>',
    thumuc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"/></svg>',
    mo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5"/></svg>',
    xem: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    chep: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 012-2h10"/></svg>',
    zip: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8l-9-5-9 5v8l9 5 9-5zM3 8l9 5 9-5M12 13v8"/></svg>'
  };

  /* ---------------------------------------------------------------- cửa sổ xem */
  var st = null;   // {ds, i, el, ten}
  function dong() { dongSheet(); if (st && st.el) { st.el.remove(); document.removeEventListener("keydown", phim, true); document.documentElement.style.overflow = st.cu; } st = null; }
  function phim(e) {
    if (!st) return;
    if (e.key === "Escape") { if (sheet) dongSheet(); else if (document.querySelector(".xt-menu")) { xoaMenu(); } else dong(); e.preventDefault(); e.stopPropagation(); }
    else if (e.key === "ArrowLeft") { chuyen(-1); e.preventDefault(); } else if (e.key === "ArrowRight") { chuyen(1); e.preventDefault(); }
  }
  function chuyen(b) { if (!st || st.ds.length < 2) return; st.i = (st.i + b + st.ds.length) % st.ds.length; ve(); }
  function noiDung(t) {
    var h = "";
    if (t.kind === "anh") h = '<img src="' + esc(t.url) + '" alt="' + esc(t.name) + '">';
    else if (t.kind === "video") h = '<video src="' + esc(t.url) + '" controls autoplay playsinline></video>';
    else if (t.kind === "am") h = '<audio src="' + esc(t.url) + '" controls autoplay></audio>';
    else if (t.kind === "pdf") h = '<iframe src="' + esc(t.url) + '" title="' + esc(t.name) + '"></iframe>';
    else if (t.kind === "chu") h = '<pre class="xt-van">Đang tải…</pre>';
    else h = '<div class="xt-khac"><b>' + esc(t.name) + '</b><span>Loại tệp này chưa xem trước được ở đây. Anh tải về hoặc mở bằng ứng dụng trên máy.</span><div class="xt-hang"><button class="xt-nut xt-chinh" data-xt-a="tai">' + IC.tai + 'Tải về</button></div></div>';
    return h;
  }
  function ve() {
    var t = st.ds[st.i], n = st.ds.length, el = st.el;
    var nhieu = n > 1, nZip = trongNao(st.ds).length, loaiTu = t.kind === "anh" ? "ảnh" : t.kind === "video" ? "video" : "tệp";
    el.querySelector(".xt-cua").innerHTML =
      '<div class="xt-dau"><span class="xt-ext">' + esc(t.ext || "tệp") + '</span><span class="xt-ten" title="' + esc(t.ngoai ? t.name : t.path) + '">' + esc(t.name) + '</span>' +
      (nhieu ? '<span class="xt-dem">' + (st.i + 1) + ' / ' + n + '</span>' : (t.size ? '<span class="xt-dem">' + kb(t.size) + '</span>' : '')) +
      '<button class="xt-nut xt-chinh xt-pc" data-xt-a="tai" title="Tải tệp này về máy">' + IC.tai + '<span>Tải về</span></button>' +
      (nZip > 1 ? '<button class="xt-nut xt-pc" data-xt-a="zip" title="Tải tất cả ' + nZip + ' tệp thành một file .zip">' + IC.zip + '<span>Tải tất cả (' + nZip + ')</span></button>' : '') +
      '<button class="xt-nut xt-pc" data-xt-a="them" title="Thêm tuỳ chọn">⋯</button>' +
      '<button class="xt-nut xt-dong" data-xt-a="dong" aria-label="Đóng" title="Đóng (Esc)">×</button></div>' +
      '<div class="xt-san' + (t.kind === "chu" ? " xt-cuon" : "") + '">' + noiDung(t) +
      (nhieu ? '<button class="xt-mt xt-t" data-xt-a="truoc" aria-label="Tệp trước">‹</button><button class="xt-mt xt-p" data-xt-a="sau" aria-label="Tệp sau">›</button>' : '') + '</div>' +
      (nhieu ? '<div class="xt-dai" role="tablist">' + st.ds.map(function (g, k) {
        var th = g.kind === "anh" ? '<img loading="lazy" src="' + esc(g.url) + '" alt="">' : g.kind === "video" ? '<video preload="metadata" muted src="' + esc(g.url) + '#t=0.4"></video><i>MP4</i>' : esc(g.ext || "tệp");
        return '<button class="xt-tn' + (k === st.i ? " on" : "") + '" data-xt-k="' + k + '" title="' + esc(g.name) + '">' + th + '</button>'; }).join("") + '</div>' : '') +
      // Điện thoại: thanh nút to ở đáy, ngón cái bấm tới
      '<div class="xt-chan"><button class="xt-nut xt-chinh" data-xt-a="tai">' + IC.tai + '<span>Lưu ' + loaiTu + '</span></button>' +
      (nZip > 1 ? '<button class="xt-nut" data-xt-a="zip">' + IC.zip + '<span>Tải tất cả (' + nZip + ')</span></button>' : '') +
      '<button class="xt-nut xt-it" data-xt-a="them" aria-label="Thêm tuỳ chọn">⋯</button></div>';
    var on = el.querySelector(".xt-tn.on"); if (on && on.scrollIntoView) { try { on.scrollIntoView({ block: "nearest", inline: "center" }); } catch (e) {} }
    if (t.kind === "chu") {
      fetch(t.url, { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (tx) { var p = el.querySelector(".xt-van"); if (p && st && st.ds[st.i] === t) p.textContent = tx.length > 400000 ? tx.slice(0, 400000) + "\n\n… (còn nữa, tải về để xem đủ)" : tx; })
        .catch(function () { var p = el.querySelector(".xt-van"); if (p) p.textContent = "Không đọc được nội dung tệp."; });
    }
  }
  function mo(ds, chiSo) {
    chenCss(); ds = (ds || []).map(chuan); if (!ds.length) return;
    dong();
    var lop = document.createElement("div"); lop.className = "xt-lop" + tongSang(); lop.setAttribute("role", "dialog"); lop.setAttribute("aria-modal", "true");
    lop.innerHTML = '<div class="xt-cua"></div>';
    document.body.appendChild(lop);
    st = { ds: ds, i: Math.max(0, Math.min(ds.length - 1, chiSo | 0)), el: lop, cu: document.documentElement.style.overflow, ten: "tep-" + ds.length };
    document.documentElement.style.overflow = "hidden";
    document.addEventListener("keydown", phim, true);
    lop.addEventListener("mousedown", function (e) { if (e.target === lop) dong(); });
    lop.addEventListener("click", function (e) {
      var img = e.target.closest && e.target.closest(".xt-san img"); if (img) { img.classList.toggle("xt-to"); var sb = img.closest(".xt-san"); sb.classList.toggle("xt-cuon", img.classList.contains("xt-to")); return; }
      var tn = e.target.closest && e.target.closest("[data-xt-k]"); if (tn) { st.i = Number(tn.getAttribute("data-xt-k")); ve(); return; }
      var b = e.target.closest && e.target.closest("[data-xt-a]"); if (!b) return; var a = b.getAttribute("data-xt-a"), t = st.ds[st.i];
      if (a === "dong") dong(); else if (a === "tai") taiThongMinh(t, st.ds); else if (a === "zip") taiTatCa(st.ds, st.ten);
      else if (a === "truoc") chuyen(-1); else if (a === "sau") chuyen(1);
      else if (a === "thumuc") { docMayChu().then(function (m) { if (m) moMay(t, "thu-muc"); else denNoiChua(t); }); }
      else if (a === "them") { var r = b.getBoundingClientRect(); menu(r.left, r.bottom + 6, t, st.ds, true); }
    });
    ve();
    var d = lop.querySelector(".xt-dong"); if (d && d.focus) d.focus();
  }

  /* ---------------------------------------------------------------- menu chuột phải */
  function xoaMenu() { var m = document.querySelector(".xt-menu"); if (m) m.remove(); document.removeEventListener("mousedown", ngoai, true); }
  function ngoai(e) { if (!(e.target.closest && e.target.closest(".xt-menu"))) xoaMenu(); }
  function menu(x, y, tep, nhom, trongXem) {
    chenCss(); xoaMenu(); var t = chuan(tep), ds = (nhom || []).map(chuan);
    docMayChu().then(function (may) {
      var d = [];
      if (!trongXem) d.push(["xem", IC.xem, "Xem trong cửa sổ", ""]);
      d.push(["tai", IC.tai, laDienThoai() ? "Lưu về điện thoại" : "Tải về", ""]);
      if (may && !t.ngoai) { d.push(["app", IC.mo, "Mở bằng ứng dụng trên máy", ""]); }
      d.push(["chep", IC.chep, "Sao chép đường dẫn", ""]);
      d.push(["tab", IC.mo, "Mở trong tab mới", ""]);
      if (trongNao(ds).length > 1) d.push(["hr"], ["zip", IC.zip, "Tải tất cả " + trongNao(ds).length + " tệp (.zip)", ""]);
      var m = document.createElement("div"); m.className = "xt-menu" + tongSang(); m.setAttribute("role", "menu");
      m.innerHTML = '<div class="xt-t" title="' + esc(t.ngoai ? t.name : t.path) + '">' + esc(t.name) + '</div>' + d.map(function (i) { return i[0] === "hr" ? "<hr>" : '<button class="xt-m" role="menuitem" data-xt-m="' + i[0] + '">' + i[1] + esc(i[2]) + (i[3] ? "<small>" + esc(i[3]) + "</small>" : "") + "</button>"; }).join("");
      document.body.appendChild(m);
      var w = m.offsetWidth, h = m.offsetHeight; m.style.left = Math.max(8, Math.min(x, innerWidth - w - 8)) + "px"; m.style.top = Math.max(8, Math.min(y, innerHeight - h - 8)) + "px";
      m.addEventListener("click", function (e) {
        var b = e.target.closest("[data-xt-m]"); if (!b) return; var a = b.getAttribute("data-xt-m"); xoaMenu();
        if (a === "xem") mo(ds.length ? ds : [t], Math.max(0, ds.map(function (g) { return g.path; }).indexOf(t.path)));
        else if (a === "tai") taiThongMinh(t, ds); else if (a === "thumuc") moMay(t, "thu-muc"); else if (a === "app") moMay(t, "mo");
        else if (a === "noichua") denNoiChua(t); else if (a === "chep") chepDuongDan(t); else if (a === "tab") tabMoi(t); else if (a === "zip") taiTatCa(ds, "tep-ket-qua");
      });
      document.addEventListener("mousedown", ngoai, true);
      var f = m.querySelector(".xt-m"); if (f && f.focus) f.focus();
    });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") xoaMenu(); }, true);
  window.addEventListener("scroll", xoaMenu, true); window.addEventListener("resize", xoaMenu);

  /* ---------------------------------------------------------------- tự gắn vào chat và vào mọi chỗ có data-xt */
  function tepTuPhanTu(el) {
    if (!el) return null;
    var p = el.getAttribute("data-xt-path");
    if (p) return { path: p, brain: el.getAttribute("data-xt-brain") || "brain", name: el.getAttribute("data-xt-name") || "", size: Number(el.getAttribute("data-xt-size")) || 0 };
    // Thẻ tệp trong khung chat: <a class="jv-fdownload" data-vault-path="..." href="/files/raw?brain=..&path=..">
    var vp = el.getAttribute("data-vault-path");
    if (vp && el.tagName === "A" && /\/files\/raw\?/.test(el.getAttribute("href") || "")) {
      var m = /[?&]brain=([^&]+)/.exec(el.getAttribute("href")); return { path: vp, brain: m ? decodeURIComponent(m[1]) : "brain" };
    }
    // Ảnh trong tin nhắn: <a class="jv-img-link" data-vault-path> hoặc <img src="/files/raw?...">
    if (el.tagName === "IMG" && /\/files\/raw\?/.test(el.getAttribute("src") || "")) {
      var u = new URL(el.getAttribute("src"), location.href); var pp = u.searchParams.get("path"); if (pp) return { path: pp, brain: u.searchParams.get("brain") || "brain" };
    }
    // Ảnh KHÔNG nằm trong bộ não (link /_blob, ảnh khách gửi trong hộp thư, ảnh tạo ra): trước đây rơi vào khung xem ảnh cũ nên điện thoại thấy 2 kiểu khác nhau.
    var link = el.tagName === "A" && el.matches(LINK_ANH) ? el.getAttribute("href") : el.tagName === "IMG" && laAnhTinNhan(el) ? (el.currentSrc || el.getAttribute("src")) : "";
    if (link && !/^(javascript|blob):/i.test(link)) {
      var abs = link; try { abs = new URL(link, location.href).href; } catch (x) {}
      var ten = el.getAttribute("download") || el.getAttribute("data-ten") || el.getAttribute("title") || "";
      if (!duoi(ten)) ten = "";
      return { ngoai: true, url: abs, path: abs, name: ten, kindGoi: "anh" };
    }
    return null;
  }
  var LINK_ANH = "a.jv-img-link, a.ht-anh";
  // Ảnh thật trong tin nhắn (không phải biểu tượng nhỏ, không nằm trong link tới trang khác, không phải ảnh thu nhỏ của chính trình xem).
  function laAnhTinNhan(img) {
    if (!img.closest(".bubble") || img.closest(".xt-the") || img.closest(".xt-lop") || img.closest("[data-xt-open]")) return false;
    var a = img.closest("a[href]"); if (a && !a.matches(LINK_ANH)) return false;
    if (/^data:image\/svg/i.test(img.getAttribute("src") || "")) return false;
    var w = img.naturalWidth || img.width || 0; return !(w && w < 48);
  }
  function goc(e) { return e.target.closest ? e.target.closest("[data-xt-path], a[data-vault-path], a.jv-img-link, a.ht-anh, .bubble img") : null; }
  function nhomCua(el) {
    var ct = el.closest("[data-xt-grp-root]") || el.closest(".bubble") || el.closest(".msg");
    var g = el.getAttribute("data-xt-grp");
    var all = [].slice.call((ct || document).querySelectorAll(g ? '[data-xt-grp="' + g + '"]' : "[data-xt-path], a.jv-fxem[data-vault-path], a.jv-fdownload[data-vault-path], a.jv-img-link, a.ht-anh, .bubble img"));
    var seen = {}, out = [];
    all.forEach(function (n) { if (n.tagName === "IMG" && n.closest(LINK_ANH + ", a[data-vault-path]")) return; var t = tepTuPhanTu(n); if (t && !seen[t.path]) { seen[t.path] = 1; var c = chuan(t); if (c.kind !== "khac" || n === el) out.push(t); } });
    return out;
  }
  window.addEventListener("click", function (e) {   // window + pha bắt: chạy trước khung xem ảnh cũ (chat-render.js) dù nạp sau
    if (e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    // Cả ảnh nằm sẵn trong câu trả lời (a.jv-img-link, <img> từ /files/raw) cũng mở cửa sổ này, thay khung xem ảnh cũ; chuyển qua lại mọi ảnh/tệp của tin nhắn.
    if (e.target.closest && e.target.closest(".xt-lop")) return;
    var a = e.target.closest && (e.target.closest("[data-xt-open]") || e.target.closest("a.jv-fxem[data-vault-path], a.jv-img-link, a.ht-anh, .bubble img")); if (!a) return;
    if (a.tagName === "IMG" && !/\/files\/raw\?/.test(a.getAttribute("src") || "") && !laAnhTinNhan(a)) return;
    var t = tepTuPhanTu(a); if (!t) return;
    var ds = nhomCua(a), i = ds.map(function (g) { return g.path; }).indexOf(t.path); if (i < 0) { ds.push(t); i = ds.length - 1; }
    e.preventDefault(); e.stopImmediatePropagation(); mo(ds, i);
  }, true);
  document.addEventListener("contextmenu", function (e) {
    var el = goc(e); if (!el) return; var t = tepTuPhanTu(el); if (!t) return;
    e.preventDefault(); menu(e.clientX, e.clientY, t, nhomCua(el), false);
  }, true);



  /* Điện thoại / máy tính bảng: không có chuột phải, nên NHẤN GIỮ một tệp ~0,55 giây mở cùng menu; trong cửa sổ xem thì vuốt trái phải để chuyển tệp. */
  var giu = { t: 0, x: 0, y: 0, el: null }, chan = 0, giuXong = false;
  function huyGiu() { clearTimeout(giu.t); giu.el = null; }
  document.addEventListener("touchstart", function (e) {
    if (e.touches.length !== 1) { huyGiu(); return; }
    var el = goc(e); if (!el || el.closest(".xt-lop")) return; var tep = tepTuPhanTu(el); if (!tep) return;
    var tc = e.touches[0]; giu.x = tc.clientX; giu.y = tc.clientY; giu.el = el;
    clearTimeout(giu.t); giu.t = setTimeout(function () { if (!giu.el) return; giuXong = true; try { navigator.vibrate && navigator.vibrate(12); } catch (x) {} menu(giu.x, giu.y, tep, nhomCua(el), false); giu.el = null; }, 550);
  }, { passive: true });
  document.addEventListener("touchmove", function (e) { if (!giu.el) return; var tc = e.touches[0]; if (Math.abs(tc.clientX - giu.x) > 10 || Math.abs(tc.clientY - giu.y) > 10) huyGiu(); }, { passive: true });
  document.addEventListener("touchend", function () { huyGiu(); if (giuXong) { giuXong = false; chan = Date.now() + 600; } }, { passive: true }); document.addEventListener("touchcancel", function () { huyGiu(); giuXong = false; }, { passive: true });
  document.addEventListener("click", function (e) { if (chan && Date.now() < chan) { e.preventDefault(); e.stopImmediatePropagation(); } }, true);
  var vx = 0, vy = 0;
  document.addEventListener("touchstart", function (e) { if (st && e.target.closest && e.target.closest(".xt-san") && e.touches.length === 1) { vx = e.touches[0].clientX; vy = e.touches[0].clientY; } else vx = 0; }, { passive: true });
  document.addEventListener("touchend", function (e) { if (!st || !vx) return; var tc = e.changedTouches[0], dx = tc.clientX - vx, dy = tc.clientY - vy; vx = 0; if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.6) chuyen(dx < 0 ? 1 : -1); }, { passive: true });

  /* ---------------------------------------------------------------- dải "Tệp trong tin nhắn" ở cuối câu trả lời của AI (thẻ có ảnh nhỏ, bấm là xem, có Tải tất cả) */
  // Thanh ngang "Hình, video và tệp trong tin nhắn": gom MỌI ảnh/video/tệp của câu trả lời (cả ảnh nằm sẵn trong chữ) để xem tổng quan và bấm xem từng cái.
  // Có từ 2 mục trở lên, hoặc có tệp đính kèm dạng thẻ, mới hiện. Cái nào đã nằm trong thẻ thư mục (.xt-thu) thì không lặp lại.
  function dungDaiTep(bubble) {
    var phu = {}; [].slice.call(bubble.querySelectorAll(".xt-thu .xt-card[data-xt-path]")).forEach(function (c) { phu[c.getAttribute("data-xt-path")] = 1; });
    var daCo = {}, ds = [], coThe = false;
    [].slice.call(bubble.querySelectorAll("a.jv-img-link[data-vault-path], img[src*='/files/raw?']")).filter(function (n) { return !n.closest(".xt-the") && !n.closest(".xt-lop"); })
      .forEach(function (n) { var t = tepTuPhanTu(n); if (!t || daCo[t.path] || phu[t.path]) return; daCo[t.path] = 1; ds.push(t); });
    [].slice.call(bubble.querySelectorAll("a.jv-fxem[data-vault-path], a.jv-fdownload[data-vault-path]")).filter(function (a) { return !a.closest(".xt-the") && /\/files\/raw\?/.test(a.getAttribute("href") || ""); })
      .forEach(function (a) { var t = tepTuPhanTu(a); if (!t || daCo[t.path] || phu[t.path]) return; daCo[t.path] = 1; ds.push(t); coThe = true; });
    var cu = bubble.querySelector(".xt-the:not(.xt-thu)"), hien = ds.length >= 2 || (ds.length === 1 && coThe);
    var khoa = hien ? ds.map(function (t) { return t.path; }).join("|") : "";
    if (cu && cu.getAttribute("data-xt-k") === khoa) return;
    if (cu) cu.remove();
    if (!hien) return;
    chenCss();
    var the = document.createElement("div"); the.className = "xt-the"; the.setAttribute("data-xt-k", khoa); the.setAttribute("data-xt-grp-root", "1");
    var nA = 0, nV = 0, nK = 0; ds.forEach(function (t) { var k = chuan(t).kind; if (k === "anh") nA++; else if (k === "video") nV++; else nK++; });
    var mota = [nA ? nA + " ảnh" : "", nV ? nV + " video" : "", nK ? nK + " tệp" : ""].filter(Boolean).join(", ");
    the.innerHTML = '<div class="xt-the-h"><b>Hình, video và tệp trong tin nhắn</b><span class="xt-sl">' + mota + '</span>' + (ds.length > 1 ? '<button type="button" class="xt-tatca" title="Tải tất cả thành một file .zip">' + IC.zip + 'Tải tất cả</button>' : '') + '</div><div class="xt-the-l">' +
      ds.map(function (t) { var c = chuan(t), th = c.kind === "anh" ? '<img loading="lazy" src="' + esc(c.url) + '" alt="">' : c.kind === "video" ? '<video preload="metadata" muted src="' + esc(c.url) + '#t=0.4"></video><i>VIDEO</i>' : esc(c.ext || "tệp");
        return '<button type="button" class="xt-card" data-xt-path="' + esc(c.path) + '" data-xt-brain="' + esc(c.brain) + '" data-xt-name="' + esc(c.name) + '" data-xt-open title="' + esc(c.name) + '"><span class="xt-th">' + th + '</span><span class="xt-nm">' + esc(c.name) + '</span></button>'; }).join("") + '</div>';
    the.querySelector(".xt-tatca") && the.querySelector(".xt-tatca").addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); taiTatCa(ds.map(chuan), "tep-trong-tin-nhan"); });
    bubble.appendChild(the);
  }

  /* ---------------------------------------------------------------- AI ghi ĐƯỜNG DẪN thay vì gửi ảnh (chủ 17/11/2026: "phải gửi toàn bộ ảnh, không gửi link")
     Đường dẫn thư mục hoặc tệp nằm trong chữ code (`04-ket-qua/.../`) -> hỏi máy chủ có gì bên trong -> hiện thẻ ảnh thật, bấm xem cả bộ, tải tất cả. */
  var cacheDuong = {}, choDuong = {};
  // (V3.08) Đường dẫn AI ghi nằm trong bộ não ĐANG MỞ (vd MKT AGENT), không phải lúc nào cũng là bộ não mặc định: hỏi và mở đúng bộ não đó.
  function nao() { try { return (typeof window.currentBrainPath === "function" && window.currentBrainPath()) || "brain"; } catch (e) { return "brain"; } }
  var MEDIA_TRAN = /^[^\s\/\\`]{3,200}\.(mp4|mov|m4v|webm|mkv|mp3|m4a|wav|png|jpe?g|webp|gif|pdf|docx?|xlsx?|pptx?|csv)$/i;
  function ungVien(bubble) {
    var out = [], tran = [];
    [].slice.call(bubble.querySelectorAll("code")).forEach(function (c) {
      if (c.closest("pre") || c.closest(".xt-the") || c.closest(".xt-lop")) return;
      var t = (c.textContent || "").trim();
      if (MEDIA_TRAN.test(t)) { if (tran.indexOf(t) < 0) tran.push(t); return; }   // tên tệp trần (thiếu thư mục): dò theo tên ở máy chủ
      if (t.length < 6 || t.length > 300 || t.indexOf("/") < 0 || /^(https?:|file:|~|\.\/\.\.)/.test(t) || /[<>"|*?:\\]/.test(t)) return;
      if (/^\/(usr|bin|etc|var|opt|System|Library|private|dev)\//.test(t)) return;
      if (out.indexOf(t) < 0) out.push(t);
    });
    // Có thư mục trong tin thì thẻ thư mục đã chứa các tệp đó; chỉ khi không có thư mục nào mới hỏi từng tên trần.
    return out.length ? out.slice(0, 5) : tran.slice(0, 12);
  }
  function hoiDuong(t) {
    var b = nao(), k = b + "|" + t;
    if (Object.prototype.hasOwnProperty.call(cacheDuong, k)) return Promise.resolve(cacheDuong[k]);
    if (choDuong[k]) return choDuong[k];
    choDuong[k] = fetch("/tisa-mo-tep/xem-duong?brain=" + encodeURIComponent(b) + "&p=" + encodeURIComponent(t), { credentials: "same-origin" })
      .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
      .then(function (j) { cacheDuong[k] = (j && j.files && j.files.length) ? j : null; delete choDuong[k]; return cacheDuong[k]; });
    return choDuong[k];
  }
  function dungTheDuong(bubble) {
    var uv = ungVien(bubble);
    if (!uv.length) { var x = bubble.querySelector(".xt-thu"); if (x) x.remove(); return; }
    Promise.all(uv.map(hoiDuong)).then(function (kq) {
      if (!bubble.isConnected) return;
      var files = [], seen = {}, ten = "";
      kq.forEach(function (j) { if (!j) return; if (!ten) ten = j.ten; j.files.forEach(function (f) { if (!seen[f.path]) { seen[f.path] = 1; files.push(f); } }); });
      var cu = bubble.querySelector(".xt-thu"), khoa = files.map(function (f) { return f.path; }).join("|");
      if (!files.length) { if (cu) cu.remove(); return; }
      if (cu && cu.getAttribute("data-xt-k") === khoa) return;
      if (cu) cu.remove();
      chenCss();
      var bn = nao(), ds = files.map(function (f) { return { path: f.path, brain: bn, name: f.name, size: f.size || 0 }; });
      var nAnh = 0, nVid = 0;
      var the = document.createElement("div"); the.className = "xt-the xt-thu"; the.setAttribute("data-xt-k", khoa); the.setAttribute("data-xt-grp-root", "1");
      var subs = {}; files.forEach(function (f) { subs[f.sub || ""] = 1; });
      var nhieuSub = Object.keys(subs).length > 1, subTruoc = null;
      var cards = files.map(function (f, i) {
        var c = chuan(ds[i]), th, dau = "";
        if (c.kind === "anh") { nAnh++; th = '<img loading="lazy" src="' + esc(c.url) + '" alt="">'; }
        else if (c.kind === "video") { nVid++; th = (nVid <= 6 ? '<video preload="metadata" muted src="' + esc(c.url) + '#t=0.4"></video>' : "") + "<i>VIDEO</i>"; }
        else th = esc(c.ext || "tệp");
        if (nhieuSub && (f.sub || "") !== subTruoc) { subTruoc = f.sub || ""; dau = '<div class="xt-grp-h">' + esc(subTruoc || "Thư mục gốc") + "</div>"; }
        return dau + '<button type="button" class="xt-card" data-xt-path="' + esc(c.path) + '" data-xt-brain="' + esc(c.brain) + '" data-xt-name="' + esc(c.name) + '" data-xt-open title="' + esc((f.sub ? f.sub + "/" : "") + c.name) + '"><span class="xt-th">' + th + '</span><span class="xt-nm">' + esc(c.name) + "</span></button>";
      }).join("");
      var mota = [nAnh ? nAnh + " ảnh" : "", nVid ? nVid + " video" : "", (files.length - nAnh - nVid) ? (files.length - nAnh - nVid) + " tệp" : ""].filter(Boolean).join(", ");
      the.innerHTML = '<div class="xt-the-h"><b>' + esc(ten ? "Trong thư mục: " + ten : "Tệp AI nhắc tới") + '</b><span class="xt-sl">' + mota + '</span><button type="button" class="xt-doi" title="Đổi giữa thanh ngang và lưới">Xem dạng lưới</button><button type="button" class="xt-tatca" title="Tải tất cả thành một file .zip">' + IC.zip + "Tải tất cả</button></div>" +
        '<div class="xt-the-l">' + cards + "</div>";
      the.querySelector(".xt-tatca").addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); taiTatCa(ds.map(chuan), ten || "tep-ket-qua"); });
      var doi = the.querySelector(".xt-doi");
      if (files.length < 5) doi.remove();
      else doi.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); var l = the.classList.toggle("xt-luoi"); doi.textContent = l ? "Thu thành thanh ngang" : "Xem dạng lưới"; });
      bubble.appendChild(the);
      // Tên tệp / đường dẫn viết trong chữ code mà khớp một tệp thật: bấm vào chính chữ đó mở trình xem (cả nhóm, có mũi tên chuyển tệp).
      [].slice.call(bubble.querySelectorAll("code")).forEach(function (c) {
        if (c.closest("pre") || c.closest(".xt-the") || c.closest(".xt-lop") || c.hasAttribute("data-xt-path")) return;
        var tx = (c.textContent || "").trim(); if (!tx) return;
        var f = null; for (var q = 0; q < files.length; q++) { var fp = files[q]; if (fp.path === tx || fp.name === tx || fp.path.slice(-(tx.length + 1)) === "/" + tx) { f = fp; break; } }
        if (!f) return;
        c.setAttribute("data-xt-path", f.path); c.setAttribute("data-xt-brain", bn); c.setAttribute("data-xt-name", f.name); c.setAttribute("data-xt-open", "1"); c.setAttribute("data-xt-grp", "code");
        c.classList.add("xt-code"); c.title = "Bấm để xem " + f.name;
      });
      try { dungDaiTep(bubble); } catch (x) {}   // ảnh đã nằm trong thẻ thư mục thì thanh chung không lặp lại
    });
  }
  var hen = 0;
  function quet() { [].slice.call(document.querySelectorAll(".msg-tisa .bubble")).forEach(function (b) { try { dungDaiTep(b); } catch (e) {} try { dungTheDuong(b); } catch (e) {} }); }
  function lichQuet() { clearTimeout(hen); hen = setTimeout(quet, 700); }
  try { new MutationObserver(lichQuet).observe(document.documentElement, { childList: true, subtree: true }); } catch (e) {}
  lichQuet();

  window.TISAXemTep = { mo: mo, menu: menu, taiTatCa: function (ds, ten) { taiTatCa((ds || []).map(chuan), ten); } };
})();
