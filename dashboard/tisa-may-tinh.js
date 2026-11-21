/* tisa-may-tinh.js (V2.96, chủ 17/11/2026): "Lấy dữ liệu từ máy tính" trong nút + của khung chat.
 *
 * Mở một cửa sổ chọn ổ đĩa, thư mục và tệp NGAY TRÊN máy đang chạy TISA BOT. Chọn xong thì ghim thư mục đó làm thư mục làm
 * việc của cuộc trò chuyện (đường ghim sẵn có: AI đọc, sửa, tạo tệp tại chỗ), kèm tên các tệp đã chọn chèn vào ô nhập.
 * Tệp giữ nguyên chỗ cũ: không sao chép, không tải lên. Chỉ LIỆT KÊ qua /may-tinh/diem và /may-tinh/duyet.
 */
(function () {
  "use strict";
  if (typeof document === "undefined") return;
  var W = window, D = document;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(url) {
    return fetch(url, { credentials: "same-origin" }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .catch(function () { return { loi: "Không kết nối được với TISA BOT." }; });
  }
  function kb(n) { return n >= 1073741824 ? (n / 1073741824).toFixed(1) + " GB" : n >= 1048576 ? (n / 1048576).toFixed(1) + " MB" : n >= 1024 ? Math.round(n / 1024) + " KB" : n + " B"; }
  function ngay(t) {
    if (!t) return "";
    var d = new Date(t * 1000), n = new Date(), p = function (x) { return (x < 10 ? "0" : "") + x; };
    if (d.toDateString() === n.toDateString()) return "Hôm nay " + p(d.getHours()) + ":" + p(d.getMinutes());
    return p(d.getDate()) + "/" + p(d.getMonth() + 1) + "/" + d.getFullYear();
  }
  function tenCuoi(p) { return String(p || "").replace(/[\\/]+$/, "").split(/[\\/]/).pop() || p; }
  function khongDau(s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d"); }

  /* ---------- biểu tượng ---------- */
  function svg(d) { return '<svg class="mt-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + "</svg>"; }
  var IC = {
    may: svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    thuMuc: svg('<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'),
    tep: svg('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/>'),
    anh: svg('<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="M21 16l-5-5-8 9"/>'),
    video: svg('<rect x="3" y="5" width="13" height="14" rx="2"/><path d="M16 10l5-3v10l-5-3"/>'),
    am: svg('<path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>'),
    bang: svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/>'),
    slide: svg('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'),
    ma: svg('<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>'),
    nen: svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v8M10 7h4M10 11h4"/>'),
    o: svg('<rect x="3" y="13" width="18" height="7" rx="2"/><path d="M3 13l2.5-7h13L21 13M7 16.5h.01"/>'),
    ngoai: svg('<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M9 17h6"/>'),
    nao: svg('<path d="M9.5 3a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3 2.5 2.5 0 0 0 2.5-2.5V5.5A2.5 2.5 0 0 0 9.5 3zM14.5 3a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3 2.5 2.5 0 0 1-2.5-2.5V5.5A2.5 2.5 0 0 1 14.5 3z"/>'),
    nha: svg('<path d="M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10"/>'),
    xuong: svg('<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>'),
    dong: svg('<path d="M6 6l12 12M18 6L6 18"/>'),
    len: svg('<path d="M15 18l-6-6 6-6"/>'),
    chevron: svg('<path d="M9 6l6 6-6 6"/>'),
    tick: svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    gan: svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    lamMoi: svg('<path d="M20 11a8 8 0 1 0-2.3 5.7M20 5v6h-6"/>'),
    tim: svg('<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4-4"/>'),
    canhBao: svg('<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17.5h.01"/>'),
  };
  var ICON_KIND = { "thu-muc": "thuMuc", anh: "anh", video: "video", am: "am", "van-ban": "tep", bang: "bang", slide: "slide", ma: "ma", nen: "nen", khac: "tep", o: "o", ngoai: "ngoai" };
  var ICON_TAT = { "man-hinh": "may", "tai-lieu": "tep", "tai-ve": "xuong", anh: "anh", video: "video", nhac: "am", "bo-nao": "nao", home: "nha" };
  var LOC = [["tat-ca", "Tất cả"], ["anh", "Ảnh"], ["video", "Video"], ["tai-lieu", "Tài liệu"]];
  var NHOM = { anh: ["anh"], video: ["video"], "tai-lieu": ["van-ban", "bang", "slide"] };

  /* ---------- kiểu dáng: token --mm-* của TISA BOT (tối mặc định, sáng khi data-theme=light) ---------- */
  var CSS = [
    ".mt-lop{position:fixed;inset:0;z-index:2147482000;display:flex;align-items:center;justify-content:center;padding:clamp(8px,2.2vw,28px);background:rgba(6,10,26,.8);animation:mtVao .16s ease}",
    "@keyframes mtVao{from{opacity:0}to{opacity:1}}@keyframes mtLen{from{transform:translateY(10px);opacity:0}to{transform:none;opacity:1}}",
    ".mt-cua{display:flex;flex-direction:column;width:min(1040px,100%);height:min(720px,100%);background:var(--mm-base,#131a3a);color:var(--mm-ink,#dbe4ff);border:1px solid var(--mm-line2,rgba(255,255,255,.18));border-radius:18px;box-shadow:0 30px 80px -20px rgba(0,0,0,.6);overflow:hidden;animation:mtLen .2s ease;font-family:inherit}",
    ".mt-dau{display:flex;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.1));flex:none}",
    ".mt-dau-i{flex:none;display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:var(--mm-or-wash,rgba(255,107,53,.14));color:var(--mm-or-ink,#ff8a5c)}.mt-dau-i .mt-i{width:20px;height:20px}",
    ".mt-dau-t{flex:1 1 auto;min-width:0}.mt-dau-t b{display:block;font-size:16px;font-weight:700;line-height:1.25}.mt-dau-t span{display:block;margin-top:2px;font-size:12.5px;color:var(--mm-muted,#9aa6d6);line-height:1.35}",
    ".mt-nut{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:38px;padding:0 14px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));background:var(--mm-card,rgba(255,255,255,.055));color:inherit;font-weight:600;font-size:13.5px;line-height:1;cursor:pointer;white-space:nowrap}",
    ".mt-nut:hover{background:var(--mm-soft2,rgba(255,255,255,.1))}.mt-nut[disabled]{opacity:.45;cursor:not-allowed}.mt-nut .mt-i{width:16px;height:16px}.mt-vuong{width:38px;padding:0}",
    ".mt-nut.mt-chinh{background:var(--mm-or,#ff6b35);border-color:var(--mm-or,#ff6b35);color:#fff}.mt-nut.mt-chinh:hover{filter:brightness(1.08)}",
    ".mt-cua,.mt-cua button,.mt-cua input,.mt-cua h4{font-family:inherit}",
    ".mt-chip .mt-i{width:14px;height:14px}",
    ".mt-lop button:focus-visible{outline:2px solid var(--mm-or,#ff6b35);outline-offset:2px}",
    ".mt-than{display:flex;flex:1 1 auto;min-height:0}",
    ".mt-ben{flex:none;width:224px;padding:12px 10px;border-right:1px solid var(--mm-line,rgba(255,255,255,.1));overflow-y:auto;background:var(--mm-soft,rgba(255,255,255,.035));scrollbar-width:thin}",
    ".mt-ben h4{margin:12px 8px 6px;font-weight:700;font-size:11px;line-height:1;letter-spacing:.08em;text-transform:uppercase;color:var(--mm-muted,#9aa6d6)}.mt-ben h4:first-child{margin-top:2px}",
    ".mt-cho{display:flex;align-items:center;gap:9px;width:100%;padding:8px 10px;border:0;border-radius:9px;background:none;color:inherit;font-weight:500;font-size:13.5px;line-height:1.25;text-align:left;cursor:pointer}",
    ".mt-cho .mt-i{width:17px;height:17px;flex:none;color:var(--mm-muted,#9aa6d6)}.mt-cho span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
    ".mt-cho:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}.mt-cho.on{background:var(--mm-or-wash,rgba(255,107,53,.14));color:var(--mm-or-ink,#ff8a5c);font-weight:700}.mt-cho.on .mt-i{color:inherit}",
    ".mt-cot-chinh{display:flex;flex-direction:column;flex:1 1 auto;min-width:0}",
    ".mt-thanh{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.1));flex:none}",
    ".mt-duong{display:flex;align-items:center;flex:1 1 auto;min-width:0;overflow-x:auto;scrollbar-width:none;white-space:nowrap}.mt-duong::-webkit-scrollbar{display:none}",
    ".mt-tang{flex:none;padding:6px 8px;border:0;border-radius:8px;background:none;color:inherit;font-weight:600;font-size:13.5px;line-height:1;cursor:pointer}.mt-tang:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}.mt-tang.cuoi{font-weight:800;cursor:default}.mt-tang.cuoi:hover{background:none}",
    ".mt-sep{flex:none;display:grid;place-items:center;color:var(--mm-muted,#9aa6d6);opacity:.7}.mt-sep .mt-i{width:14px;height:14px}",
    ".mt-loc{display:flex;align-items:center;gap:7px;flex:0 1 230px;min-width:130px;height:38px;padding:0 11px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));background:var(--mm-card,rgba(255,255,255,.055))}",
    ".mt-loc .mt-i{width:16px;height:16px;color:var(--mm-muted,#9aa6d6);flex:none}.mt-loc input{flex:1;min-width:0;border:0;outline:0;background:none;color:inherit;font-weight:500;font-size:13.5px;line-height:1}.mt-loc:focus-within{border-color:var(--mm-or,#ff6b35)}",
    ".mt-bo{display:flex;align-items:center;gap:7px;padding:8px 12px;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.1));flex:none;overflow-x:auto;scrollbar-width:none}.mt-bo::-webkit-scrollbar{display:none}",
    ".mt-chip{flex:none;display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:999px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));background:none;color:inherit;font-weight:600;font-size:12.5px;line-height:1;cursor:pointer}",
    ".mt-chip:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}.mt-chip.on{background:var(--mm-or-wash,rgba(255,107,53,.14));border-color:var(--mm-or-line,rgba(255,107,53,.5));color:var(--mm-or-ink,#ff8a5c)}",
    ".mt-chip small{font-weight:700;font-size:11px;line-height:1;opacity:.75}.mt-gap{flex:1 1 auto}.mt-bo label{flex:none;display:inline-flex;align-items:center;gap:6px;font-weight:500;font-size:12.5px;line-height:1;color:var(--mm-muted,#9aa6d6);cursor:pointer}",
    ".mt-ds{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin;padding:2px 8px 8px}",
    ".mt-hang{display:grid;grid-template-columns:34px minmax(0,1fr) 92px 132px 24px;align-items:center;gap:6px;width:100%;min-height:46px;padding:0 8px;border:0;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.08));background:none;color:inherit;font-weight:500;font-size:13.5px;line-height:1.25;text-align:left;cursor:pointer}",
    ".mt-hang:hover{background:var(--mm-soft2,rgba(255,255,255,.07))}.mt-hang.chon{background:var(--mm-or-wash,rgba(255,107,53,.14))}",
    ".mt-hop{display:grid;place-items:center;width:20px;height:20px;border-radius:6px;border:1.6px solid var(--mm-line2,rgba(255,255,255,.35));color:transparent}.mt-hop .mt-i{width:13px;height:13px}.mt-hang.chon .mt-hop{background:var(--mm-or,#ff6b35);border-color:var(--mm-or,#ff6b35);color:#fff}",
    ".mt-ten{display:flex;align-items:center;gap:10px;min-width:0}.mt-ten .mt-i{width:20px;height:20px;flex:none;color:var(--mm-muted,#9aa6d6)}.mt-ten span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
    ".mt-hang.thu .mt-ten .mt-i{color:#e0a020}.mt-hang.k-anh .mt-ten .mt-i{color:#2fa36b}.mt-hang.k-video .mt-ten .mt-i{color:#e0455f}.mt-hang.k-bang .mt-ten .mt-i{color:#2f9e5a}.mt-hang.k-slide .mt-ten .mt-i{color:#e07b2f}.mt-hang.k-van-ban .mt-ten .mt-i{color:#4c7cf0}.mt-hang.k-am .mt-ten .mt-i{color:#a064e8}",
    ".mt-cot{font-size:12.5px;color:var(--mm-muted,#9aa6d6);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.mt-vao{display:grid;place-items:center;color:var(--mm-muted,#9aa6d6)}.mt-vao .mt-i{width:16px;height:16px}",
    ".mt-rong{display:flex;flex-direction:column;align-items:center;gap:10px;padding:44px 20px;text-align:center;color:var(--mm-muted,#9aa6d6);font-size:14px;line-height:1.5}.mt-rong .mt-i{width:34px;height:34px;opacity:.7}.mt-rong b{color:var(--mm-ink,#fff);font-size:15px}.mt-rong p{margin:0;max-width:440px}",
    ".mt-chan{display:flex;gap:10px;margin:12px;padding:12px 14px;border-radius:12px;border:1px solid color-mix(in srgb,#e0a020 55%,transparent);background:color-mix(in srgb,#e0a020 12%,transparent);font-size:13.5px;line-height:1.5;overflow-wrap:anywhere}.mt-chan .mt-i{width:18px;height:18px;flex:none;margin-top:2px;color:#e0a020}",
    ".mt-chan b{display:block}",
    ".mt-chan2{flex:none;padding:7px 14px;font-size:12.5px;color:var(--mm-muted,#9aa6d6);text-align:center;border-top:1px solid var(--mm-line,rgba(255,255,255,.08))}",
    ".mt-chan2 b{color:var(--mm-ink,#fff)}",
  ].join("\n");
  CSS += "\n" + [
    ".mt-cuoi{display:flex;align-items:center;gap:12px;padding:12px 14px;border-top:1px solid var(--mm-line,rgba(255,255,255,.1));background:var(--mm-soft,rgba(255,255,255,.035));flex:none}",
    ".mt-cuoi-t{flex:1 1 auto;min-width:0}.mt-cuoi-t b{display:block;font-size:14px;line-height:1.3}.mt-cuoi-t span{display:block;margin-top:2px;font-size:12.5px;color:var(--mm-muted,#9aa6d6);line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
    ".mt-cuoi-t em{font-style:normal;color:var(--mm-or-ink,#ff8a5c);font-weight:700}",
    ".mt-hd{display:flex;gap:8px;flex:none}",
    ".mt-loi{padding:8px 14px;color:#ff8a8a;font-size:13px}",
    "@media (max-width:860px){",
    ".mt-lop{padding:0}.mt-cua{width:100%;height:100%;border-radius:0;border:0}",
    ".mt-than{flex-direction:column}",
    ".mt-ben{display:flex;gap:6px;width:auto;padding:8px 10px;border-right:0;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.1));overflow-x:auto;overflow-y:hidden;scrollbar-width:none}.mt-ben::-webkit-scrollbar{display:none}",
    ".mt-ben h4{display:none}.mt-cho{flex:none;width:auto;padding:7px 12px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));border-radius:999px}",
    ".mt-thanh{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px}.mt-loc{grid-column:1/-1;grid-row:2;flex:none;min-width:0}",
    ".mt-hang{grid-template-columns:34px minmax(0,1fr) 22px;min-height:54px}.mt-hang .mt-c1,.mt-hang .mt-c2{display:none}",
    ".mt-ten{flex-direction:row}.mt-ten>div{min-width:0}.mt-ten small{display:block;font-size:12px;color:var(--mm-muted,#9aa6d6)}",
    ".mt-cuoi{flex-direction:column;align-items:stretch;padding-bottom:max(12px,env(safe-area-inset-bottom))}.mt-hd{width:100%;flex-wrap:wrap}.mt-hd .mt-nut{flex:1 1 40%;padding:0 10px}.mt-hd .mt-chinh{order:-1;flex:1 1 100%}",
    "}",
    "@media (min-width:861px){.mt-ten small{display:none}}",
  ].join("\n");
  CSS += "\n" + [
    ".mt-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(14px);z-index:2147483300;max-width:min(520px,92vw);padding:11px 16px;border-radius:12px;background:#12183a;color:#eef1ff;border:1px solid rgba(255,255,255,.18);box-shadow:0 14px 34px -12px rgba(0,0,0,.7);font-weight:600;font-size:13.5px;line-height:1.4;opacity:0;pointer-events:none;transition:opacity .18s,transform .18s}",
    ".mt-toast.on{opacity:1;transform:translateX(-50%)}",
  ].join("\n");
  function chenCss() { if (D.getElementById("mt-css")) return; var s = D.createElement("style"); s.id = "mt-css"; s.textContent = CSS; (D.head || D.documentElement).appendChild(s); }

  /* ---------- nhớ nơi đã dùng ---------- */
  function docGan() { try { return JSON.parse(W.localStorage.getItem("tisa.mt.gan") || "[]") || []; } catch (e) { return []; } }
  function ghiGan(p) {
    try {
      var ds = docGan().filter(function (x) { return x.path !== p; });
      ds.unshift({ path: p, name: tenCuoi(p) });
      W.localStorage.setItem("tisa.mt.gan", JSON.stringify(ds.slice(0, 5)));
      W.localStorage.setItem("tisa.mt.cuoi", p);
    } catch (e) { /* không lưu được thì thôi */ }
  }
  function docCuoi() { try { return W.localStorage.getItem("tisa.mt.cuoi") || ""; } catch (e) { return ""; } }

  /* ---------- thông báo nhỏ ---------- */
  var toastEl = null, toastT = 0;
  function bao(msg) {
    if (!toastEl) { toastEl = D.createElement("div"); toastEl.className = "mt-toast"; toastEl.setAttribute("role", "status"); D.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("on"); }, 3200);
  }

  /* ---------- cửa sổ ---------- */
  var S = null, lop = null;
  function q(sel) { return lop ? lop.querySelector(sel) : null; }
  function dong() {
    if (lop) { lop.remove(); lop = null; }
    S = null;
  }
  function tuongTu(a, b) { return String(a || "").replace(/[\\/]+$/, "") === String(b || "").replace(/[\\/]+$/, ""); }
  function trongNhau(cha, con) {
    cha = String(cha || "").replace(/[\\/]+$/, ""); con = String(con || "");
    return !!cha && (con === cha || con.indexOf(cha + "/") === 0 || con.indexOf(cha + "\\") === 0);
  }

  function veBen() {
    var h = "", d = S.diem || {}, cur = S.path;
    function cho(it, ic) { return '<button type="button" class="mt-cho' + (it.__on ? " on" : "") + '" data-mt-di="' + esc(it.duong_dan) + '" title="' + esc(it.duong_dan) + '">' + IC[ic] + "<span>" + esc(it.ten) + "</span></button>"; }
    var tat = (d.loi_tat || []).slice(), o = (d.o_dia || []).slice();
    var tot = null, dai = -1;
    tat.concat(o).forEach(function (x) { if (trongNhau(x.duong_dan, cur) && x.duong_dan.length > dai) { dai = x.duong_dan.length; tot = x; } });
    tat.concat(o).forEach(function (x) { x.__on = x === tot; });
    h += "<h4>Vị trí</h4>" + tat.map(function (x) { return cho(x, ICON_TAT[x.ma] || "thuMuc"); }).join("");
    var gan = docGan().filter(function (x) { return x && x.path; });
    if (gan.length) h += "<h4>Vừa dùng</h4>" + gan.map(function (x) { return cho({ ten: x.name, duong_dan: x.path, __on: false }, "gan"); }).join("");
    if (o.length) h += "<h4>Ổ đĩa</h4>" + o.map(function (x) { return cho(x, ICON_KIND[x.loai] || "o"); }).join("");
    q('[data-mt="ben"]').innerHTML = h;
  }
  function veDuong() {
    var dt = S.data || {}, cs = dt.crumbs || [], h = "";
    if (!cs.length) h = '<span class="mt-tang cuoi">' + esc(dt.ten || "Máy này") + "</span>";
    if (typeof dt.path === "string" && /^[A-Za-z]:/.test(dt.path)) h = '<button type="button" class="mt-tang" data-mt-di="">Máy này</button><span class="mt-sep">' + IC.chevron + "</span>" + h;
    h += cs.map(function (c, i) {
      var cuoi = i === cs.length - 1;
      return (i ? '<span class="mt-sep">' + IC.chevron + "</span>" : "") + (cuoi ? '<span class="mt-tang cuoi" aria-current="page">' + esc(c.ten) + "</span>"
        : '<button type="button" class="mt-tang" data-mt-di="' + esc(c.duong_dan) + '">' + esc(c.ten) + "</button>");
    }).join("");
    var el = q('[data-mt="duong"]'); el.innerHTML = h; el.scrollLeft = el.scrollWidth;
    var len = q('[data-mt-a="len"]'); len.disabled = dt.parent == null;
  }
  function nhomCua(it) { for (var k in NHOM) if (NHOM[k].indexOf(it.kind) >= 0) return k; return ""; }
  function nhin() {
    var dt = S.data || {}, ds = dt.items || [], loc = S.loc, tk = khongDau(S.q);
    return ds.filter(function (it) {
      if (tk && khongDau(it.name).indexOf(tk) < 0) return false;
      if (loc === "tat-ca" || it.dir) return true;
      return nhomCua(it) === loc;
    });
  }
  function veBo() {
    var dt = S.data || {}, ds = dt.items || [], dem = { anh: 0, video: 0, "tai-lieu": 0 };
    ds.forEach(function (it) { var g = it.dir ? "" : nhomCua(it); if (g) dem[g]++; });
    var h = LOC.map(function (l) {
      var n = l[0] === "tat-ca" ? ds.length : dem[l[0]];
      return '<button type="button" class="mt-chip' + (S.loc === l[0] ? " on" : "") + '" data-mt-loc="' + l[0] + '">' + l[1] + " <small>" + n + "</small></button>";
    }).join("");
    var nTep = nhin().filter(function (x) { return !x.dir; }).length;
    h += '<span class="mt-gap"></span>' + (nTep ? '<button type="button" class="mt-chip" data-mt-a="het">' + IC.tick + " Chọn hết " + nTep + " tệp</button>" : "")
      + '<label><input type="checkbox" data-mt-an' + (S.an ? " checked" : "") + "> Hiện tệp ẩn</label>";
    q('[data-mt="bo"]').innerHTML = h;
  }
  function veDs() {
    var dt = S.data || {}, el = q('[data-mt="ds"]');
    if (dt.__dang) { el.innerHTML = '<div class="mt-rong"><span>Đang mở…</span></div>'; return; }
    var h = "";
    if (dt.loi) h += '<div class="mt-chan">' + IC.canhBao + "<div>" + esc(dt.loi) + "</div></div>";
    S.view = nhin();
    if (!S.view.length && !dt.loi) {
      var loc = S.q || S.loc !== "tat-ca";
      h += '<div class="mt-rong">' + IC.thuMuc + "<b>" + (loc ? "Không có mục nào khớp" : "Thư mục này đang trống") + "</b><p>" + (loc ? "Thử bỏ bộ lọc hoặc đổi từ khoá." : "Anh vẫn có thể bấm Làm việc trong thư mục này để AI tạo tệp vào đây.") + "</p></div>";
    }
    h += S.view.map(function (it, i) {
      var on = !!S.sel[it.path], k = it.kind;
      var meta = it.dir ? "" : kb(it.size);
      return '<div class="mt-hang' + (it.dir ? " thu" : "") + " k-" + esc(k) + (on ? " chon" : "") + '" role="listitem" tabindex="0" data-i="' + i + '">'
        + '<span class="mt-hop" role="checkbox" aria-checked="' + on + '" aria-label="Chọn ' + esc(it.name) + '" data-hop="1">' + IC.tick + "</span>"
        + '<div class="mt-ten">' + IC[ICON_KIND[k] || "tep"] + "<div style=\"min-width:0\"><span>" + esc(it.name) + "</span><small>" + esc((meta ? meta + " · " : "") + ngay(it.mtime)) + "</small></div></div>"
        + '<span class="mt-cot mt-c1">' + esc(meta) + '</span><span class="mt-cot mt-c2">' + esc(ngay(it.mtime)) + "</span>"
        + '<span class="mt-vao">' + (it.dir ? IC.chevron : "") + "</span></div>";
    }).join("");
    if (dt.cat) h += '<div class="mt-rong"><p>Thư mục có rất nhiều mục, mới hiện phần đầu. Dùng ô lọc hoặc vào thư mục con.</p></div>';
    el.innerHTML = h;
  }
  function chon() { return Object.keys(S.sel).map(function (k) { return S.sel[k]; }); }
  function veCuoi() {
    var dt = S.data || {}, ds = chon(), n = ds.length, goc = dt.path === "" || dt.path == null;
    var tong = ds.reduce(function (s, x) { return s + (x.dir ? 0 : x.size || 0); }, 0);
    var t, ph, hd;
    if (!n) {
      t = "Chưa chọn tệp nào";
      ph = "Hoặc để AI làm việc cả thư mục <em>" + esc(dt.ten || "") + "</em>";
      hd = '<button type="button" class="mt-nut" data-mt-a="dong">Huỷ</button><button type="button" class="mt-nut mt-chinh" data-mt-a="viec"' + (goc ? " disabled" : "") + ">" + IC.thuMuc + " Làm việc trong thư mục này</button>";
    } else {
      t = "Đã chọn " + n + " mục" + (tong ? " · " + kb(tong) : "");
      ph = esc(ds.slice(0, 3).map(function (x) { return x.name; }).join(", ") + (n > 3 ? " và " + (n - 3) + " mục nữa" : ""));
      hd = '<button type="button" class="mt-nut" data-mt-a="bo">Bỏ chọn</button><button type="button" class="mt-nut" data-mt-a="viec">Làm cả thư mục</button>'
        + '<button type="button" class="mt-nut mt-chinh" data-mt-a="chon">' + IC.tick + " Làm với " + n + " mục này</button>";
    }
    q('[data-mt="tomtat"]').innerHTML = "<b>" + t + "</b><span>" + ph + "</span>";
    q('[data-mt="hd"]').innerHTML = hd;
  }
  function veHet() { veBen(); veDuong(); veBo(); veDs(); veCuoi(); }
  function ve2() { veBo(); veDs(); veCuoi(); }

  function mo_thu_muc(p) {
    var n = ++S.seq;
    S.path = p; S.sel = {}; S.q = ""; var o = q('[data-mt="loc"]'); if (o) o.value = "";
    S.data = { __dang: true, items: [], crumbs: [], path: p };
    veHet();
    api("/may-tinh/duyet?path=" + encodeURIComponent(p) + "&hien_an=" + (S.an ? 1 : 0)).then(function (d) {
      if (!S || n !== S.seq) return;
      S.data = d || { loi: "Không đọc được thư mục.", items: [] };
      if (typeof d.path === "string") S.path = d.path;
      veHet();
      var ds = q('[data-mt="ds"]'); if (ds) ds.scrollTop = 0;
    });
  }

  /* ---------- hành động chốt ---------- */
  function chenVaoOChat(ds, thuMuc) {
    var el = D.getElementById("chatInput");
    if (!el) return;
    var ten = ds.map(function (x) { return '"' + x.name + (x.dir ? "/" : "") + '"'; }).join(", ");
    var dong1 = "Dữ liệu cần làm (có sẵn trong thư mục làm việc " + thuMuc + "): " + ten + ".";
    el.value = dong1 + "\n" + (el.value ? el.value : "");
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.focus();
    try { var e = el.value.length; el.setSelectionRange(e, e); } catch (x) { /* ô nhập khác kiểu */ }
  }
  function ghim(p) {
    if (!W.TISAPinnedFolder || !W.TISAPinnedFolder.pin) return Promise.resolve("Trang chưa sẵn sàng để ghim thư mục, anh tải lại trang rồi thử lại.");
    return W.TISAPinnedFolder.pin(p);
  }
  function chot(theoChon) {
    var dt = S.data || {}, ds = chon(), dir = dt.path, ten = dt.ten || tenCuoi(dir);
    var thuMucDich = dir, kem = [];
    if (theoChon && ds.length) {
      if (ds.length === 1 && ds[0].dir) { thuMucDich = ds[0].path; ten = ds[0].name; }
      else kem = ds;
    }
    if (!thuMucDich) return;
    var nut = q(".mt-chinh"); if (nut) nut.disabled = true;
    ghim(thuMucDich).then(function (loi) {
      if (!S) return;
      if (loi) {
        if (nut) nut.disabled = false;
        var el = q('[data-mt="tomtat"]'); if (el) el.insertAdjacentHTML("beforeend", '<div class="mt-loi" role="alert">' + esc(loi) + "</div>");
        return;
      }
      ghiGan(thuMucDich);
      if (kem.length) chenVaoOChat(kem, ten);
      dong();
      bao(kem.length ? "Đã chọn " + kem.length + " mục trong “" + ten + "”. AI làm ngay trên máy, không tải lên." : "AI sẽ làm việc trong thư mục “" + ten + "” ngay trên máy.");
      var o = D.getElementById("chatInput"); if (o) o.focus();
    });
  }

  /* ---------- mở cửa sổ ---------- */
  function mo() {
    dong(); chenCss();
    S = { path: "", data: null, sel: {}, loc: "tat-ca", q: "", an: false, diem: null, seq: 0, view: [] };
    lop = D.createElement("div"); lop.className = "mt-lop"; lop.id = "mtLop";
    lop.innerHTML = '<div class="mt-cua" role="dialog" aria-modal="true" aria-labelledby="mtTieuDe">'
      + '<div class="mt-dau"><span class="mt-dau-i">' + IC.may + '</span><div class="mt-dau-t"><b id="mtTieuDe">Chọn dữ liệu trên máy tính</b><span data-mt="may">Đang tìm máy…</span></div>'
      + '<button type="button" class="mt-nut mt-vuong" data-mt-a="dong" aria-label="Đóng">' + IC.dong + "</button></div>"
      + '<div class="mt-than"><nav class="mt-ben" data-mt="ben" aria-label="Vị trí trên máy"></nav><div class="mt-cot-chinh">'
      + '<div class="mt-thanh"><button type="button" class="mt-nut mt-vuong" data-mt-a="len" aria-label="Lên thư mục cha" title="Lên một cấp">' + IC.len + '</button><div class="mt-duong" data-mt="duong"></div>'
      + '<label class="mt-loc">' + IC.tim + '<input type="search" data-mt="loc" placeholder="Lọc trong thư mục này" aria-label="Lọc trong thư mục này" autocomplete="off"></label>'
      + '<button type="button" class="mt-nut mt-vuong" data-mt-a="moi" aria-label="Làm mới" title="Làm mới">' + IC.lamMoi + "</button></div>"
      + '<div class="mt-bo" data-mt="bo"></div><div class="mt-ds" data-mt="ds" role="list"></div></div></div>'
      + '<div class="mt-cuoi"><div class="mt-cuoi-t" data-mt="tomtat"></div><div class="mt-hd" data-mt="hd"></div></div></div>';
    D.body.appendChild(lop);
    lop.addEventListener("mousedown", function (e) { if (e.target === lop) S.__ngoai = true; });
    lop.addEventListener("click", function (e) { if (e.target === lop && S && S.__ngoai) dong(); if (S) S.__ngoai = false; });
    lop.addEventListener("click", bam);
    lop.addEventListener("keydown", phim);
    lop.addEventListener("change", function (e) { if (e.target.hasAttribute("data-mt-an")) { S.an = e.target.checked; mo_thu_muc(S.path); } });
    lop.addEventListener("input", function (e) { if (e.target.getAttribute("data-mt") === "loc") { S.q = e.target.value; ve2(); } });
    veHet();
    api("/may-tinh/diem").then(function (d) {
      if (!S) return;
      S.diem = d || {};
      q('[data-mt="may"]').textContent = (d.may ? "Máy: " + d.may + (d.he ? " (" + d.he + ")" : "") + " · " : "") + "Tệp giữ nguyên trên máy, không sao chép hay tải lên";
      var pin = W.TISAPinnedFolder && W.TISAPinnedFolder.current && W.TISAPinnedFolder.current();
      var bd = (pin && /^([A-Za-z]:[\\/]|\/)/.test(pin.path || "") ? pin.path : "") || docCuoi() || "";
      mo_thu_muc(bd);
    });
    var dongBtn = q('[data-mt-a="dong"]'); if (dongBtn) dongBtn.focus();
  }
  function bam(e) {
    if (!S) return;
    var t = e.target, el;
    if ((el = t.closest("[data-mt-di]"))) { mo_thu_muc(el.getAttribute("data-mt-di")); return; }
    if ((el = t.closest("[data-mt-loc]"))) { S.loc = el.getAttribute("data-mt-loc"); ve2(); return; }
    if ((el = t.closest("[data-mt-a]"))) {
      var a = el.getAttribute("data-mt-a");
      if (a === "dong") dong();
      else if (a === "len") { if (S.data && S.data.parent != null) mo_thu_muc(S.data.parent); }
      else if (a === "moi") mo_thu_muc(S.path);
      else if (a === "bo") { S.sel = {}; ve2(); }
      else if (a === "het") { S.view.forEach(function (x) { if (!x.dir) S.sel[x.path] = x; }); ve2(); }
      else if (a === "viec") chot(false);
      else if (a === "chon") chot(true);
      return;
    }
    if ((el = t.closest(".mt-hang"))) {
      var it = S.view[+el.getAttribute("data-i")]; if (!it) return;
      if (it.dir && !t.closest("[data-hop]")) { mo_thu_muc(it.path); return; }
      if (S.sel[it.path]) delete S.sel[it.path]; else S.sel[it.path] = it;
      ve2();
    }
  }
  function phim(e) {
    if (!S) return;
    if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); dong(); return; }
    var h = e.target.closest && e.target.closest(".mt-hang");
    if (h && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      var it = S.view[+h.getAttribute("data-i")]; if (!it) return;
      if (e.key === "Enter" && it.dir) { mo_thu_muc(it.path); return; }
      if (S.sel[it.path]) delete S.sel[it.path]; else S.sel[it.path] = it;
      ve2();
      var again = lop && lop.querySelector('.mt-hang[data-i="' + h.getAttribute("data-i") + '"]'); if (again) again.focus();
    }
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      var rows = lop.querySelectorAll(".mt-hang"); if (!rows.length) return;
      var cur = Array.prototype.indexOf.call(rows, D.activeElement);
      var nx = e.key === "ArrowDown" ? Math.min(rows.length - 1, cur + 1) : Math.max(0, cur < 0 ? 0 : cur - 1);
      if (cur >= 0 || e.key === "ArrowDown") { e.preventDefault(); rows[nx].focus(); }
    }
  }

  /* ---------- gắn vào nút + ---------- */
  var ICON_MENU = '<svg class="cp-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>';
  function dangKy(n) {
    var M = W.TISAComposerMenu;
    if (!M || !M.register) { if (n < 60) setTimeout(function () { dangKy(n + 1); }, 250); return; }
    M.register({ id: "may_tinh", order: 15, icon: ICON_MENU, label: "Lấy dữ liệu từ máy tính", hint: function () { return "Không tải lên"; }, run: mo });
  }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", function () { dangKy(0); }); else dangKy(0);
  W.TISAMayTinh = { mo: mo, dong: dong };
})();
