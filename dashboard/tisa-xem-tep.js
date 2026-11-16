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
    var path = String(t.path || "").replace(/^\.?\//, ""), name = t.name || path.split("/").pop() || "tệp", e = duoi(name);
    return { path: path, brain: t.brain || "brain", name: name, ext: e, kind: loai(e), size: t.size || 0, url: t.url || urlRaw(t.brain, path, 0), dl: t.dl || urlRaw(t.brain, path, 1) };
  }
  function docMayChu() {
    if (mayChu !== null) return Promise.resolve(mayChu);
    return fetch("/tisa-mo-tep/may-chu", { credentials: "same-origin" }).then(function (r) { return r.json(); })
      .then(function (j) { mayChu = !!(j && j.may_chu); return mayChu; }).catch(function () { mayChu = false; return false; });
  }
  docMayChu();

  /* ---------------------------------------------------------------- hành động trên một tệp */
  function taiVe(t) { var a = document.createElement("a"); a.href = t.dl; a.download = t.name; a.style.display = "none"; document.body.appendChild(a); a.click(); setTimeout(function () { a.remove(); }, 400); }
  function taiTatCa(ds, ten) {
    var u = "/tisa-mo-tep/zip?brain=" + encodeURIComponent(ds[0].brain) + "&name=" + encodeURIComponent(ten || "tep-ket-qua") + ds.slice(0, TAI_ZIP_TOI_DA).map(function (t) { return "&p=" + encodeURIComponent(t.path); }).join("");
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
    var s = t.path; try { navigator.clipboard.writeText(s).then(function () { bao("Đã sao chép đường dẫn"); }, function () { bao(s); }); } catch (e) { bao(s); }
  }
  function tabMoi(t) { window.open(t.url, "_blank", "noopener"); }

  /* ---------------------------------------------------------------- thông báo nhỏ */
  var toastEl = null, toastT = 0;
  function bao(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "xt-toast"; document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("on"); }, 2600);
  }

  /* ---------------------------------------------------------------- giao diện */
  var CSS = ".xt-lop{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:clamp(8px,2.5vw,32px);background:rgba(7,11,28,.78);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);animation:xtVao .14s ease-out}"
    + "@keyframes xtVao{from{opacity:0}to{opacity:1}}"
    + ".xt-cua{display:flex;flex-direction:column;width:min(1180px,100%);height:min(860px,100%);background:#0f1530;color:#eef1ff;border:1px solid rgba(255,255,255,.12);border-radius:18px;overflow:hidden;box-shadow:0 30px 80px -20px rgba(0,0,0,.7);font-family:inherit}"
    + ".xt-dau{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.1);flex:none}"
    + ".xt-ext{flex:none;padding:3px 9px;border-radius:7px;background:rgba(124,150,255,.2);color:#b9c7ff;font:800 11.5px/1.4 inherit;letter-spacing:.06em;text-transform:uppercase}"
    + ".xt-ten{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:15px;font-weight:700}"
    + ".xt-dem{flex:none;color:#9aa6d6;font-size:13px;font-weight:600}"
    + ".xt-nut{flex:none;display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 13px;border-radius:11px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.06);color:#eef1ff;font:600 13.5px/1 inherit;cursor:pointer;white-space:nowrap}"
    + ".xt-nut:hover{background:rgba(255,255,255,.14)}.xt-nut:focus-visible{outline:2px solid #ff8a5c;outline-offset:2px}"
    + ".xt-nut.xt-chinh{background:#ff6b35;border-color:#ff6b35;color:#fff}.xt-nut.xt-chinh:hover{background:#ff7d4d}"
    + ".xt-nut svg{width:16px;height:16px;flex:none}"
    + ".xt-dong{padding:0;width:36px;justify-content:center;font-size:20px}"
    + ".xt-san{position:relative;flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center;background:#070a1c}"
    + ".xt-san img,.xt-san video{max-width:100%;max-height:100%;object-fit:contain;display:block}.xt-san img{cursor:zoom-in}.xt-san img.xt-to{max-width:none;max-height:none;cursor:zoom-out}"
    + ".xt-san.xt-cuon{overflow:auto;align-items:flex-start;justify-content:flex-start}.xt-san audio{width:min(560px,92%)}.xt-san iframe{width:100%;height:100%;border:0;background:#fff}"
    + ".xt-van{margin:0;padding:18px 22px;width:100%;height:100%;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;font:13.5px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;color:#e5e9ff;box-sizing:border-box}"
    + ".xt-khac{display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center;padding:24px;max-width:520px}.xt-khac b{font-size:17px}.xt-khac span{color:#9aa6d6;font-size:14px;line-height:1.5}.xt-khac .xt-hang{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}"
    + ".xt-mt{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:64px;border-radius:14px;border:1px solid rgba(255,255,255,.2);background:rgba(15,21,48,.72);color:#fff;font-size:26px;cursor:pointer;z-index:3;display:flex;align-items:center;justify-content:center}"
    + ".xt-mt:hover{background:rgba(15,21,48,.95)}.xt-mt.xt-t{left:12px}.xt-mt.xt-p{right:12px}"
    + ".xt-dai{display:flex;gap:8px;padding:10px 12px;overflow-x:auto;border-top:1px solid rgba(255,255,255,.1);background:#0b1026;flex:none;scrollbar-width:thin}"
    + ".xt-tn{position:relative;flex:none;width:78px;height:58px;border-radius:9px;overflow:hidden;border:2px solid transparent;background:#1b2350;cursor:pointer;padding:0;display:flex;align-items:center;justify-content:center;color:#b9c7ff;font:800 11px/1 inherit;text-transform:uppercase}"
    + ".xt-tn img,.xt-tn video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}.xt-tn.on{border-color:#ff6b35}.xt-tn:hover{border-color:rgba(255,138,92,.6)}"
    + ".xt-tn i{position:absolute;right:3px;bottom:3px;padding:1px 5px;border-radius:5px;background:rgba(0,0,0,.65);font:700 9.5px/1.4 inherit;font-style:normal;color:#fff}"
    + ".xt-menu{position:fixed;z-index:2147483200;min-width:250px;max-width:340px;padding:6px;border-radius:13px;background:#12183a;color:#eef1ff;border:1px solid rgba(255,255,255,.16);box-shadow:0 22px 50px -12px rgba(0,0,0,.65);font-family:inherit}"
    + ".xt-menu .xt-m{display:flex;align-items:center;gap:10px;width:100%;padding:9px 11px;border:0;border-radius:8px;background:none;color:inherit;font:500 14px/1.2 inherit;text-align:left;cursor:pointer}"
    + ".xt-menu .xt-m:hover,.xt-menu .xt-m:focus-visible{background:rgba(255,255,255,.1);outline:none}.xt-menu .xt-m small{margin-left:auto;color:#9aa6d6;font-size:11.5px}"
    + ".xt-menu .xt-m svg{width:16px;height:16px;flex:none;opacity:.9}.xt-menu hr{border:0;border-top:1px solid rgba(255,255,255,.12);margin:5px 4px}.xt-menu .xt-t{padding:7px 11px 5px;color:#9aa6d6;font-size:12px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    + ".xt-the{margin:14px 0 2px;padding:10px 12px 12px;border:1px solid var(--mm-line2,rgba(120,130,180,.3));border-radius:14px;background:var(--mm-soft,rgba(120,130,180,.08))}"
    + ".xt-the-h{display:flex;align-items:center;gap:8px;margin-bottom:9px;font-size:13px}.xt-the-h b{font-weight:700}.xt-the-h .xt-sl{padding:1px 8px;border-radius:999px;background:var(--mm-soft2,rgba(120,130,180,.2));font-weight:700;font-size:12px}"
    + ".xt-the-h .xt-tatca{margin-left:auto;display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 11px;border-radius:9px;border:1px solid var(--mm-line2,rgba(120,130,180,.4));background:var(--mm-card,transparent);color:inherit;font:600 12.5px/1 inherit;cursor:pointer}"
    + ".xt-the-h .xt-tatca:hover{border-color:#ff6b35}.xt-the-h .xt-tatca svg{width:15px;height:15px}"
    + ".xt-the-l{display:flex;gap:10px;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin}"
    + ".xt-thu .xt-the-l{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior:contain}.xt-thu.xt-luoi .xt-the-l{flex-wrap:wrap;max-height:400px;overflow-y:auto;overflow-x:hidden}"
    + ".xt-thu .xt-grp-h{display:none}.xt-thu.xt-luoi .xt-grp-h{display:block}"
    + ".xt-the-h .xt-doi{margin-left:auto;height:30px;padding:0 11px;border-radius:9px;border:1px solid var(--mm-line2,rgba(120,130,180,.4));background:none;color:inherit;font-weight:600;font-size:12.5px;cursor:pointer;white-space:nowrap}.xt-the-h .xt-doi+.xt-tatca{margin-left:0}"
    + ".xt-grp-h{flex:0 0 100%;margin:8px 0 0;padding-top:6px;font-weight:700;font-size:12.5px;line-height:1.3;letter-spacing:.02em;color:var(--mm-muted,#8a93b8);border-top:1px solid var(--mm-line,rgba(120,130,180,.25))}.xt-grp-h:first-child{margin-top:0;padding-top:0;border-top:0}"
    + ".xt-the-h b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}.xt-the-h .xt-tatca{white-space:nowrap;flex:none}"
    + "@media (max-width:720px){.xt-the{padding:9px 10px 10px}.xt-the-h{font-size:12.5px}.xt-card{width:112px!important}.xt-card .xt-th{height:74px!important}.xt-card .xt-nm{font-size:11.5px}.xt-the-h .xt-tatca{height:32px}}"
    + ".xt-card{flex:none;width:132px;padding:0;border:1px solid var(--mm-line2,rgba(120,130,180,.35));border-radius:11px;overflow:hidden;background:var(--mm-card,#fff);color:inherit;text-align:left;cursor:pointer;font:inherit}"
    + ".xt-card:hover{border-color:#ff6b35}.xt-card:focus-visible{outline:2px solid #ff8a5c;outline-offset:2px}"
    + ".xt-card .xt-th{position:relative;display:flex;align-items:center;justify-content:center;height:84px;background:rgba(120,130,180,.14);font:800 13px/1 inherit;text-transform:uppercase;color:#7c8cc8}"
    + ".xt-card .xt-th img,.xt-card .xt-th video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}"
    + ".xt-card .xt-th i{position:absolute;right:5px;bottom:5px;padding:1px 6px;border-radius:6px;background:rgba(0,0,0,.65);color:#fff;font:700 10px/1.5 inherit;font-style:normal}"
    + ".xt-card .xt-nm{display:block;padding:7px 9px 8px;font-size:12px;font-weight:600;line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    + ".xt-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);z-index:2147483300;padding:10px 16px;border-radius:12px;background:#12183a;color:#eef1ff;border:1px solid rgba(255,255,255,.18);font:600 13.5px/1.3 inherit;opacity:0;pointer-events:none;transition:opacity .18s,transform .18s}"
    + ".xt-toast.on{opacity:1;transform:translateX(-50%) translateY(0)}"
    + "@media (max-width:720px){.xt-lop{padding:0}.xt-cua{height:100%;border-radius:0}.xt-dau{flex-wrap:wrap}.xt-ten{flex-basis:60%}.xt-mt{width:38px;height:52px}.xt-nut span{display:none}.xt-nut{padding:0 11px}}"
    + "@media (prefers-reduced-motion:reduce){.xt-lop{animation:none}.xt-toast{transition:none}}";
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
  function dong() { if (st && st.el) { st.el.remove(); document.removeEventListener("keydown", phim, true); document.documentElement.style.overflow = st.cu; } st = null; }
  function phim(e) {
    if (!st) return;
    if (e.key === "Escape") { if (document.querySelector(".xt-menu")) { xoaMenu(); } else dong(); e.preventDefault(); e.stopPropagation(); }
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
    else h = '<div class="xt-khac"><b>' + esc(t.name) + '</b><span>Loại tệp này chưa xem trước được ở đây. Anh tải về hoặc mở bằng ứng dụng trên máy.</span><div class="xt-hang"><button class="xt-nut xt-chinh" data-xt-a="tai">' + IC.tai + 'Tải về</button><button class="xt-nut" data-xt-a="thumuc">' + IC.thumuc + 'Hiện trong thư mục</button></div></div>';
    return h;
  }
  function ve() {
    var t = st.ds[st.i], n = st.ds.length, el = st.el;
    var nhieu = n > 1;
    el.querySelector(".xt-cua").innerHTML =
      '<div class="xt-dau"><span class="xt-ext">' + esc(t.ext || "tệp") + '</span><span class="xt-ten" title="' + esc(t.path) + '">' + esc(t.name) + '</span>' +
      (nhieu ? '<span class="xt-dem">' + (st.i + 1) + ' / ' + n + '</span>' : (t.size ? '<span class="xt-dem">' + kb(t.size) + '</span>' : '')) +
      '<button class="xt-nut xt-chinh" data-xt-a="tai" title="Tải tệp này về máy">' + IC.tai + '<span>Tải về</span></button>' +
      (nhieu ? '<button class="xt-nut" data-xt-a="zip" title="Tải tất cả ' + n + ' tệp thành một file .zip">' + IC.zip + '<span>Tải tất cả (' + n + ')</span></button>' : '') +
      '<button class="xt-nut" data-xt-a="thumuc" title="Hiện tệp trong thư mục">' + IC.thumuc + '<span>Thư mục</span></button>' +
      '<button class="xt-nut" data-xt-a="them" title="Thêm tuỳ chọn">⋯</button>' +
      '<button class="xt-nut xt-dong" data-xt-a="dong" aria-label="Đóng" title="Đóng (Esc)">×</button></div>' +
      '<div class="xt-san' + (t.kind === "chu" ? " xt-cuon" : "") + '">' + noiDung(t) +
      (nhieu ? '<button class="xt-mt xt-t" data-xt-a="truoc" aria-label="Tệp trước">‹</button><button class="xt-mt xt-p" data-xt-a="sau" aria-label="Tệp sau">›</button>' : '') + '</div>' +
      (nhieu ? '<div class="xt-dai" role="tablist">' + st.ds.map(function (g, k) {
        var th = g.kind === "anh" ? '<img loading="lazy" src="' + esc(g.url) + '" alt="">' : g.kind === "video" ? '<video preload="metadata" muted src="' + esc(g.url) + '#t=0.4"></video><i>MP4</i>' : esc(g.ext || "tệp");
        return '<button class="xt-tn' + (k === st.i ? " on" : "") + '" data-xt-k="' + k + '" title="' + esc(g.name) + '">' + th + '</button>'; }).join("") + '</div>' : '');
    var on = el.querySelector(".xt-tn.on"); if (on && on.scrollIntoView) { try { on.scrollIntoView({ block: "nearest", inline: "center" }); } catch (e) {} }
    if (t.kind === "chu") {
      fetch(t.url, { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (tx) { var p = el.querySelector(".xt-van"); if (p && st && st.ds[st.i] === t) p.textContent = tx.length > 400000 ? tx.slice(0, 400000) + "\n\n… (còn nữa, tải về để xem đủ)" : tx; })
        .catch(function () { var p = el.querySelector(".xt-van"); if (p) p.textContent = "Không đọc được nội dung tệp."; });
    }
  }
  function mo(ds, chiSo) {
    chenCss(); ds = (ds || []).map(chuan); if (!ds.length) return;
    dong();
    var lop = document.createElement("div"); lop.className = "xt-lop"; lop.setAttribute("role", "dialog"); lop.setAttribute("aria-modal", "true");
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
      if (a === "dong") dong(); else if (a === "tai") taiVe(t); else if (a === "zip") taiTatCa(st.ds, st.ten);
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
      d.push(["tai", IC.tai, "Tải về", ""]);
      if (may) { d.push(["thumuc", IC.thumuc, "Hiện trong thư mục trên máy", "Finder"]); d.push(["app", IC.mo, "Mở bằng ứng dụng trên máy", ""]); }
      d.push(["noichua", IC.thumuc, "Đến nơi chứa tệp (trang Tệp tin)", ""]);
      d.push(["chep", IC.chep, "Sao chép đường dẫn", ""]);
      d.push(["tab", IC.mo, "Mở trong tab mới", ""]);
      if (ds.length > 1) d.push(["hr"], ["zip", IC.zip, "Tải tất cả " + ds.length + " tệp (.zip)", ""]);
      var m = document.createElement("div"); m.className = "xt-menu"; m.setAttribute("role", "menu");
      m.innerHTML = '<div class="xt-t" title="' + esc(t.path) + '">' + esc(t.name) + '</div>' + d.map(function (i) { return i[0] === "hr" ? "<hr>" : '<button class="xt-m" role="menuitem" data-xt-m="' + i[0] + '">' + i[1] + esc(i[2]) + (i[3] ? "<small>" + esc(i[3]) + "</small>" : "") + "</button>"; }).join("");
      document.body.appendChild(m);
      var w = m.offsetWidth, h = m.offsetHeight; m.style.left = Math.max(8, Math.min(x, innerWidth - w - 8)) + "px"; m.style.top = Math.max(8, Math.min(y, innerHeight - h - 8)) + "px";
      m.addEventListener("click", function (e) {
        var b = e.target.closest("[data-xt-m]"); if (!b) return; var a = b.getAttribute("data-xt-m"); xoaMenu();
        if (a === "xem") mo(ds.length ? ds : [t], Math.max(0, ds.map(function (g) { return g.path; }).indexOf(t.path)));
        else if (a === "tai") taiVe(t); else if (a === "thumuc") moMay(t, "thu-muc"); else if (a === "app") moMay(t, "mo");
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
    return null;
  }
  function goc(e) { return e.target.closest ? e.target.closest("[data-xt-path], a[data-vault-path], a.jv-img-link, .bubble img") : null; }
  function nhomCua(el) {
    var ct = el.closest("[data-xt-grp-root]") || el.closest(".bubble") || el.closest(".msg");
    var g = el.getAttribute("data-xt-grp");
    var all = [].slice.call((ct || document).querySelectorAll(g ? '[data-xt-grp="' + g + '"]' : "[data-xt-path], a.jv-fxem[data-vault-path], a.jv-fdownload[data-vault-path], a.jv-img-link[data-vault-path], .bubble img[src*='/files/raw?']"));
    var seen = {}, out = [];
    all.forEach(function (n) { var t = tepTuPhanTu(n); if (t && !seen[t.path]) { seen[t.path] = 1; var c = chuan(t); if (c.kind !== "khac" || n === el) out.push(t); } });
    return out;
  }
  window.addEventListener("click", function (e) {   // window + pha bắt: chạy trước khung xem ảnh cũ (chat-render.js) dù nạp sau
    if (e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    // Cả ảnh nằm sẵn trong câu trả lời (a.jv-img-link, <img> từ /files/raw) cũng mở cửa sổ này, thay khung xem ảnh cũ; chuyển qua lại mọi ảnh/tệp của tin nhắn.
    if (e.target.closest && e.target.closest(".xt-lop")) return;
    var a = e.target.closest && e.target.closest("[data-xt-open], a.jv-fxem[data-vault-path], a.jv-img-link[data-vault-path], .bubble img[src*='/files/raw?']"); if (!a) return;
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
  function ungVien(bubble) {
    var out = [];
    [].slice.call(bubble.querySelectorAll("code")).forEach(function (c) {
      if (c.closest("pre") || c.closest(".xt-the") || c.closest(".xt-lop")) return;
      var t = (c.textContent || "").trim();
      if (t.length < 6 || t.length > 300 || t.indexOf("/") < 0 || /^(https?:|file:|~|\.\/\.\.)/.test(t) || /[<>"|*?:\\]/.test(t)) return;
      if (/^\/(usr|bin|etc|var|opt|System|Library|private|dev)\//.test(t)) return;
      if (out.indexOf(t) < 0) out.push(t);
    });
    return out.slice(0, 5);
  }
  function hoiDuong(t) {
    if (Object.prototype.hasOwnProperty.call(cacheDuong, t)) return Promise.resolve(cacheDuong[t]);
    if (choDuong[t]) return choDuong[t];
    choDuong[t] = fetch("/tisa-mo-tep/xem-duong?brain=brain&p=" + encodeURIComponent(t), { credentials: "same-origin" })
      .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
      .then(function (j) { cacheDuong[t] = (j && j.files && j.files.length) ? j : null; delete choDuong[t]; return cacheDuong[t]; });
    return choDuong[t];
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
      var ds = files.map(function (f) { return { path: f.path, name: f.name, size: f.size || 0 }; });
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
