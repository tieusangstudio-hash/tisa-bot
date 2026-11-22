/* tisa-trinh-duyet.js (V2.98): Trình duyệt TISA, cửa sổ riêng để AI Agent thao tác web thay người dùng.
 *
 * - Mục "Mở trình duyệt cho AI thao tác" trong nút + của khung chat (Hỏi nhanh, Hỏi chuyên gia).
 * - Bảng điều khiển: mở cửa sổ, đi nhanh tới các trang hay dùng để đăng nhập, trang đã đăng nhập (chỉ tên miền), AI đang làm gì,
 *   nút Dừng ngay, và danh sách xin duyệt (đăng, gửi, xóa...).
 * - Thẻ nổi ở mọi trang khi AI xin duyệt hoặc đang chờ anh đăng nhập, nhập mã, giải CAPTCHA.
 * Mật khẩu và mã xác thực người dùng gõ thẳng vào cửa sổ trình duyệt, TISA BOT không nhận. Phần máy chủ: server/tisa_browser.py.
 */
(function () {
  "use strict";
  if (typeof document === "undefined") return;
  var W = window, D = document;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(url, body) {
    var o = { credentials: "same-origin" };
    if (body !== undefined) { o.method = "POST"; o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(body || {}); }
    return fetch(url, o).then(function (r) { return r.json().catch(function () { return {}; }); }).catch(function () { return { loi: "Không kết nối được với TISA BOT." }; });
  }

  var TRANG = [
    ["Facebook", "https://www.facebook.com/"], ["Meta Business Suite", "https://business.facebook.com/"], ["Google", "https://accounts.google.com/"],
    ["YouTube", "https://studio.youtube.com/"], ["TikTok", "https://www.tiktok.com/login"], ["Zalo OA", "https://oa.zalo.me/"],
    ["Canva", "https://www.canva.com/"], ["Pancake", "https://pancake.vn/"]
  ];

  var CSS = [
    ".tbd-lop{position:fixed;inset:0;z-index:2147482000;display:flex;align-items:center;justify-content:center;padding:clamp(8px,2.2vw,28px);background:rgba(6,10,26,.8);animation:tbdVao .14s ease-out}",
    "@keyframes tbdVao{from{opacity:0}to{opacity:1}}",
    ".tbd-cua{display:flex;flex-direction:column;width:min(860px,100%);max-height:100%;background:var(--mm-base,#131a3a);color:var(--mm-ink,#dbe4ff);border:1px solid var(--mm-line2,rgba(255,255,255,.16));border-radius:18px;overflow:hidden;box-shadow:0 30px 80px -20px rgba(0,0,0,.6);font-family:inherit}",
    ".tbd-dau{display:flex;align-items:center;gap:12px;padding:14px 16px;border-bottom:1px solid var(--mm-line,rgba(255,255,255,.1));flex:none}",
    ".tbd-dau-i{flex:none;display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:var(--mm-or-wash,rgba(255,107,53,.14));color:var(--mm-or-ink,#ff8a5c)}.tbd-dau-i svg{width:20px;height:20px}",
    ".tbd-dau-t{flex:1 1 auto;min-width:0}.tbd-dau-t b{display:block;font-size:16px;font-weight:700}.tbd-dau-t span{display:block;margin-top:2px;font-size:12.5px;color:var(--mm-muted,#9aa6d6)}",
    ".tbd-nut{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-height:38px;padding:0 14px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));background:var(--mm-soft,rgba(255,255,255,.06));color:inherit;font:600 13.5px/1 inherit;cursor:pointer;white-space:nowrap}",
    ".tbd-nut:hover{background:var(--mm-soft2,rgba(255,255,255,.12))}.tbd-nut:disabled{opacity:.5;cursor:default}.tbd-nut:focus-visible{outline:2px solid var(--mm-or,#ff6b35);outline-offset:2px}",
    ".tbd-nut.chinh{background:var(--mm-or,#ff6b35);border-color:var(--mm-or,#ff6b35);color:#fff}.tbd-nut.chinh:hover{filter:brightness(1.08)}",
    ".tbd-nut.do{background:#d93025;border-color:#d93025;color:#fff}.tbd-nut.nho{min-height:32px;padding:0 11px;font-size:12.5px}",
    ".tbd-than{overflow:auto;padding:16px;display:grid;gap:14px}",
    ".tbd-the{padding:14px;border:1px solid var(--mm-line,rgba(255,255,255,.12));border-radius:14px;background:var(--mm-soft,rgba(255,255,255,.04))}.tbd-the h3{margin:0 0 8px;font-size:14px}.tbd-the p{margin:0 0 8px;color:var(--mm-muted,#9aa6d6);font-size:13px;line-height:1.55}",
    ".tbd-tt{display:flex;flex-wrap:wrap;align-items:center;gap:8px}.tbd-cham{display:inline-block;width:9px;height:9px;border-radius:50%;background:#9aa6d6;margin-right:6px}.tbd-cham.on{background:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.2)}.tbd-cham.dung{background:#d93025}",
    ".tbd-luoi{display:flex;flex-wrap:wrap;gap:8px}.tbd-mien{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border-radius:999px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));font-size:12.5px}.tbd-mien.phien{border-color:rgba(34,197,94,.55)}.tbd-mien i{font-style:normal;color:#22c55e;font-weight:700}",
    ".tbd-nk{display:grid;gap:4px;max-height:210px;overflow:auto;font-size:12.5px}.tbd-nk div{display:flex;gap:8px;padding:4px 0;border-bottom:1px dashed var(--mm-line,rgba(255,255,255,.1))}.tbd-nk time{flex:none;color:var(--mm-muted,#9aa6d6)}.tbd-nk b{font-weight:600}",
    ".tbd-nk .chan,.tbd-nk .cho{color:#f59e0b}.tbd-nk .loi{color:#ef4444}",
    ".tbd-buoc{margin:0;padding-left:18px;color:var(--mm-muted,#9aa6d6);font-size:13px;line-height:1.7}.tbd-buoc b{color:inherit;font-weight:700}",
    ".tbd-tabs{display:flex;gap:6px;padding:4px;border-radius:12px;background:var(--mm-soft,rgba(255,255,255,.06));width:max-content;max-width:100%}.tbd-tabs button{border:0;background:transparent;color:inherit;padding:8px 18px;border-radius:9px;font:700 13.5px/1 inherit;cursor:pointer}.tbd-tabs button.on{background:var(--mm-or,#ff6b35);color:#fff}",
    ".tbd-hs{display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:999px;border:1px solid var(--mm-line2,rgba(255,255,255,.2));background:transparent;color:inherit;font:600 13px/1 inherit;cursor:pointer}.tbd-hs .tbd-cham{margin:0}.tbd-hs small{color:var(--mm-or-ink,#ff8a5c);font-weight:700}",
    ".tbd-hs.on{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.14))}.tbd-hs.them{border-style:dashed;color:var(--mm-muted,#9aa6d6)}.tbd-ten input{flex:1 1 200px;min-width:0;height:38px;padding:0 12px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:var(--mm-base,#131a3a);color:inherit;font:inherit}",
    ".tbd-loc{width:100%;box-sizing:border-box;height:38px;padding:0 12px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:var(--mm-base,#131a3a);color:inherit;font:inherit}",
    ".tbd-ds-chrome{display:grid;gap:6px;max-height:280px;overflow:auto;margin-top:8px}.tbd-nguon{margin-top:6px;font:700 11.5px/1 inherit;letter-spacing:.06em;text-transform:uppercase;color:var(--mm-muted,#9aa6d6)}",
    ".tbd-hsc{display:flex;flex-direction:column;gap:2px;text-align:left;padding:9px 12px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.2));background:transparent;color:inherit;font:inherit;cursor:pointer}.tbd-hsc span{font-size:12.5px;color:var(--mm-muted,#9aa6d6)}",
    ".tbd-hsc:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}.tbd-hsc.on{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.14))}",
    ".tbd-muc{display:grid;gap:8px}.tbd-mc{display:grid;gap:3px;text-align:left;padding:11px 13px;border-radius:12px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));background:transparent;color:inherit;cursor:pointer;font:inherit}",
    ".tbd-mc b{font-size:13.5px}.tbd-mc span{font-size:12.5px;color:var(--mm-muted,#9aa6d6);line-height:1.45}.tbd-mc:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}",
    ".tbd-mc.on{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.12))}.tbd-mc.on.tq{border-color:#d93025;background:rgba(217,48,37,.12)}",
    ".tbd-the>.tbd-dt:first-child{margin-top:0;border-top:0;padding-top:0}",
    ".tbd-goi{margin:0 0 10px!important;line-height:1.5}.tbd-dong{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid var(--mm-line,rgba(255,255,255,.1))}.tbd-dong .tbd-nhan{flex:1 1 170px;font-size:13.5px}.tbd-dong .tbd-nhan b{margin-right:4px}",
    ".tbd-xn{margin-top:10px;padding:12px;border-radius:12px;border:1px solid rgba(217,48,37,.6);background:rgba(217,48,37,.08)}.tbd-xn p{margin:0 0 10px;color:inherit}",
    ".tbd-xn select{height:38px;padding:0 10px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.2));background:var(--mm-base,#131a3a);color:inherit;font:inherit}",
    ".tbd-duyet{border-color:rgba(245,158,11,.7);background:rgba(245,158,11,.1)}.tbd-duyet h3{color:#f59e0b}.tbd-hang{display:flex;flex-wrap:wrap;gap:8px;align-items:center}",
    /* thẻ nổi */
    ".tbd-noi{position:fixed;right:18px;top:70px;z-index:2147481900;width:min(380px,calc(100vw - 24px));display:grid;gap:10px}",
    ".tbd-ntc{padding:14px;border-radius:14px;background:var(--mm-base,#131a3a);color:var(--mm-ink,#dbe4ff);border:1px solid rgba(245,158,11,.75);box-shadow:0 18px 50px -12px rgba(0,0,0,.6);font:13.5px/1.5 inherit}",
    ".tbd-ntc{position:relative}.tbd-ntc b{display:block;margin-bottom:4px;padding-right:26px;font-size:14px}.tbd-ntc small{display:block;color:var(--mm-muted,#9aa6d6);margin-bottom:10px}",
    ".tbd-dong{position:absolute;top:8px;right:8px;width:26px;height:26px;border:0;border-radius:50%;background:transparent;color:var(--mm-muted,#9aa6d6);font:400 20px/1 system-ui,sans-serif;cursor:pointer;display:grid;place-items:center;padding:0}.tbd-dong:hover{background:rgba(127,127,127,.2);color:var(--mm-ink,#dbe4ff)}",
    "@media (max-width:640px){.tbd-lop{padding:0}.tbd-cua{width:100%;height:100%;border-radius:0;border:0}.tbd-noi{right:8px;left:8px;top:58px;width:auto}}",
    "@media (prefers-reduced-motion:reduce){.tbd-lop{animation:none}}"
  ].join("");
  function css() { if (D.getElementById("tbd-css")) return; var s = D.createElement("style"); s.id = "tbd-css"; s.textContent = CSS; (D.head || D.documentElement).appendChild(s); }

  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>';
  var lop = null, tim = null, ST = null, noi = null, dangDuyetId = {};

  function gio(t) { return String(t || "").slice(11, 16); }
  function dongNk(x) {
    var c = /chặn|chờ duyệt|chờ người|đang chờ/.test(x.ket_qua || "") ? (/chặn/.test(x.ket_qua) ? "chan" : "cho") : (/lỗi/.test(x.ket_qua || "") ? "loi" : "");
    return "<div class='" + c + "'><time>" + esc(gio(x.t)) + "</time><span><b>" + esc(x.op || "") + "</b> " + esc(x.ten || x.mo_ta || "") + (x.host ? " <small>(" + esc(x.host) + ")</small>" : "") + " " + esc(x.ket_qua || "") + "</span></div>";
  }
  function theDuyet(d) {
    return "<div class='tbd-the tbd-duyet'><h3>AI xin duyệt: " + esc(d.mo_ta) + "</h3><p>Nút: <b>" + esc(d.ten || "(không tên)") + "</b> trên " + esc(d.host) + (d.trang ? " · " + esc(d.trang) : "") + "</p>" +
      "<div class='tbd-hang'><button type='button' class='tbd-nut chinh' data-tbd-duyet='" + esc(d.id) + "' data-ok='1'>Duyệt</button><button type='button' class='tbd-nut' data-tbd-duyet='" + esc(d.id) + "' data-ok='1' data-tat='30'>Duyệt và đừng hỏi nữa (30 phút)</button><button type='button' class='tbd-nut' data-tbd-duyet='" + esc(d.id) + "' data-ok='0'>Không</button></div></div>";
  }

  var MUC = [
    ["hoi_het", "Hỏi mọi bước", "AI xin duyệt trước từng thao tác (bấm, gõ, chọn). An toàn nhất, chậm nhất."],
    ["quan_trong", "Hỏi bước quan trọng", "Khuyên dùng. AI tự làm việc thường; chỉ hỏi khi đăng, gửi, xóa, đổi bảo mật, đăng ký."],
    ["toan_quyen", "Toàn quyền", "AI tự làm cả đăng, gửi, xóa, không hỏi nữa. Vẫn không nhập mật khẩu, mã xác thực, CAPTCHA, không thanh toán, không vào trang ngân hàng."]
  ];
  var hoiToan = false;
  function conLai(den) {
    if (!den) return "";
    var s = Math.max(0, Math.round(den - Date.now() / 1000)), m = Math.ceil(s / 60);
    return m >= 60 ? " (còn " + Math.floor(m / 60) + " giờ " + (m % 60) + " phút)" : " (còn " + m + " phút)";
  }
  var MOTA_TB = { hoi_het: "AI xin duyệt từng thao tác bấm, gõ. An toàn nhất, chậm nhất.", quan_trong: "Khuyên dùng. AI tự làm việc thường, chỉ hỏi khi đăng, gửi, xóa, đổi bảo mật, đăng ký.", toan_quyen: "AI tự làm cả đăng, gửi, xóa, không hỏi. Vẫn không nhập mật khẩu, mã xác thực, CAPTCHA, không thanh toán." };
  function dongSeg(attr, cur, ds, d) {
    return "<div class='tbd-seg' role='radiogroup'>" + ds.map(function (m) {
      return "<button type='button' role='radio' aria-checked='" + (cur === m[0]) + "' class='" + (cur === m[0] ? "on" : "") + (m[0] === "toan_quyen" ? " tq" : "") + "' " + attr + "='" + m[0] + "'>" + esc(m[1]) + (cur === m[0] && m[0] === "toan_quyen" ? esc(conLai(d.muc_den) || "") : "") + "</button>";
    }).join("") + "</div>";
  }
  function theMuc(d) {
    var cur = d.muc || "quan_trong";
    var h = "<div class='tbd-the'><h3>3. Quyền của AI trên web</h3>" + dongSeg("data-tbd-muc", cur, MUC, d) + "<p class='tbd-kn-mo'>" + esc(MOTA_TB[cur] || "") + "</p>";
    if (hoiToan) h += "<div class='tbd-xn'><p><b>Bật Toàn quyền?</b> AI tự đăng bài, gửi tin, xóa, nộp biểu mẫu mà không hỏi. Nút Dừng AI ngay luôn dùng được.</p>" +
      "<div class='tbd-hang'><select id='tbdPhut'><option value='30'>30 phút</option><option value='120' selected>2 giờ</option><option value='480'>8 giờ</option><option value='0'>Đến khi anh tắt</option></select>" +
      "<button type='button' class='tbd-nut do' data-tbd-muc-ok='1'>Bật Toàn quyền</button><button type='button' class='tbd-nut' data-tbd-muc-ok='0'>Hủy</button></div></div>";
    return h + "</div>";
  }
  var DT = {}, DNL = null;
  function dt(ten, tieuDe, noi, mo) { return "<details class='tbd-dt' data-dt='" + ten + "'" + ((DT[ten] || mo) ? " open" : "") + "><summary>" + esc(tieuDe) + "</summary><div>" + noi + "</div></details>"; }

  var XEM = "", hsForm = "", nhapUI = null;
  function theNhap() {
    if (!nhapUI) return "";
    var u = nhapUI, h = "<div class='tbd-the tbd-duyet'><h3>Dùng hồ sơ Chrome anh đã có</h3>";
    if (u.kq) {
      var k = u.kq;
      if (k.ok === false) return h + "<p style='color:#ef4444'>" + esc(k.loi || "Không nhập được.") + "</p><div class='tbd-hang'><button type='button' class='tbd-nut' data-nhap='huy'>Đóng</button></div></div>";
      return h + "<p><b>Đã nhập xong \"" + esc(k.ten) + "\".</b> Lấy được " + (k.so_cookie || 0) + " cookie." + ((k.dang_nhap || []).length ? " Đang đăng nhập: " + (k.dang_nhap || []).slice(0, 12).map(esc).join(", ") + "." : "") + "</p>" +
        (k.canh_bao || []).map(function (c) { return "<p style='color:#f59e0b'>" + esc(c) + "</p>"; }).join("") +
        "<div class='tbd-hang'><button type='button' class='tbd-nut chinh' data-nhap='mo_xong' data-id='" + esc(k.id) + "'>Mở trình duyệt này</button><button type='button' class='tbd-nut' data-nhap='huy'>Xong</button></div></div>";
    }
    if (!u.ds) return h + "<p>Đang đọc danh sách hồ sơ Chrome trên máy...</p></div>";
    if (!u.ds.length) return h + "<p>Không thấy Chrome, Edge hay Brave nào có hồ sơ trên máy này.</p><div class='tbd-hang'><button type='button' class='tbd-nut' data-nhap='huy'>Đóng</button></div></div>";
    h += "<p>Chọn hồ sơ Chrome anh dùng lâu nay. TISA BOT <b>chép phần đăng nhập</b> (cookie) sang một trình duyệt riêng, nên Facebook, TikTok, Zalo... thường <b>không phải đăng nhập lại</b>. <b>Riêng Google (Gmail, YouTube, NotebookLM...) thường vẫn phải đăng nhập lại một lần</b> trong trình duyệt này, vì Google tự hủy phiên bị chép sang nơi khác. AI dùng được các tài khoản đang đăng nhập trong hồ sơ đó. Không chép mật khẩu đã lưu, thẻ, lịch sử. Chrome gốc của anh không bị sửa.</p>";
    if (u.ds.some(function (n) { return n.dang_mo; })) h += "<p style='color:#f59e0b'>Chrome đang mở. Nên <b>đóng Chrome trước</b> rồi nhập, để lấy đủ những đăng nhập mới nhất (vẫn nhập được nếu để mở).</p>";
    h += "<input id='nhapLoc' type='text' placeholder='Gõ tên hoặc email để lọc hồ sơ' class='tbd-loc'><div class='tbd-ds-chrome' id='nhapDs'>";
    u.ds.forEach(function (n) {
      h += "<div class='tbd-nguon'>" + esc(n.ten) + "</div>";
      n.ho_so.forEach(function (x) {
        var on = u.chon && u.chon.nguon === n.ma && u.chon.thu_muc === x.thu_muc;
        h += "<button type='button' class='tbd-hsc" + (on ? " on" : "") + "' data-nhap='chon' data-nguon='" + esc(n.ma) + "' data-tm='" + esc(x.thu_muc) + "' data-ten='" + esc(x.ten) + "' data-loc='" + esc((x.ten + " " + x.email).toLowerCase()) + "'><b>" + esc(x.ten) + "</b><span>" + esc(x.email || x.thu_muc) + (x.co_cookie ? "" : " · chưa có đăng nhập") + "</span></button>";
      });
    });
    h += "</div><div class='tbd-hang' style='margin-top:10px'><input id='nhapTen' type='text' maxlength='40' class='tbd-loc' style='max-width:260px' placeholder='Tên trình duyệt trong TISA' value='" + esc((u.chon && u.chon.ten) || "") + "'>" +
      "<button type='button' class='tbd-nut chinh' data-nhap='ok'" + ((u.chon && !u.dang) ? "" : " disabled") + ">" + (u.dang ? "Đang chép..." : "Nhập hồ sơ này") + "</button><button type='button' class='tbd-nut' data-nhap='huy'>Hủy</button></div></div>";
    return h;
  }
  function xemId() { return XEM || (ST && ST.hoso_xem) || (ST && ST.hoso_dang_dung) || ""; }
  function theHoSo(d) {
    var ds = d.ho_so_ds || [], xem = xemId(), mac = d.hoso_dang_dung, chay = !!d.dang_chay;
    var cur = ds.filter(function (x) { return x.id === xem; })[0] || ds[0] || { ten: "", id: "" };
    var ngoai = cur.loai === "ngoai", soTab = (d.trang || []).length, tr = trinhNay();
    var coChipNay = tr && !ds.some(function (x) { return x.loai === "ngoai" && x.trinh === tr; });
    // Bước 1: chọn trình duyệt
    var h = "<div class='tbd-the'><h3>1. AI làm việc trên trình duyệt nào?</h3>" +
      "<p class='tbd-goi'>Bấm chọn một cái, AI chỉ dùng cái có viền cam. Chấm xanh là đang mở, sẵn sàng.</p><div class='tbd-luoi'>" +
      ds.map(function (x) {
        return "<button type='button' class='tbd-hs" + (x.id === xem ? " on" : "") + "' data-tbd-hs='" + esc(x.id) + "' aria-pressed='" + (x.id === xem) + "'><i class='tbd-cham " + (x.dang_chay ? "on" : "") + "'></i>" + esc(x.ten) + (x.id === mac ? " <small>✓ AI đang dùng</small>" : "") + "</button>";
      }).join("") +
      (coChipNay ? "<button type='button' class='tbd-hs them' style='border-color:var(--mm-or,#ff6b35);color:var(--mm-or-ink,#e8572a);font-weight:700' data-tbd-ngoai='them' title='Dùng luôn " + esc(TEN_TR[tr]) + " anh đang mở TISA BOT, có sẵn mọi tài khoản anh đã đăng nhập'>+ Dùng " + esc(TEN_TR[tr]) + " này (đang mở TISA BOT)</button>" : "") +
      "</div>";
    if (ngoai) {
      var tt = cur.tinh_trang, ten = TEN_TR[cur.trinh] || "Chrome";
      if (tt === "da_noi") h += "<div class='tbd-dong'><span class='tbd-nhan'><i class='tbd-cham on'></i><b>Đã nối</b> với " + esc(ten) + " của anh" + (soTab ? ", thấy " + soTab + " tab" : "") + "</span>" +
        "<button type='button' class='tbd-nut nho' data-tbd-ngoai='ngat'>Ngắt kết nối</button></div>" +
        "<p class='tbd-kn-mo' style='margin-top:8px'>AI mở tab mới để làm, không đụng vào tab anh đang dùng. Chrome sẽ hiện dòng báo đang được điều khiển, đó là bình thường.</p>";
      else if (tt === "cho_cho_phep") h += "<div class='tbd-xn' style='border-color:rgba(245,158,11,.75);background:rgba(245,158,11,.08)'><p><b>" + esc(ten) + " đang hỏi anh.</b> Anh nhìn lên cửa sổ " + esc(ten) + ", bấm <b>Allow</b> (Cho phép) để AI làm việc được.</p></div>";
      else if (tt === "da_bat") h += "<div class='tbd-dong'><span class='tbd-nhan'><i class='tbd-cham'></i><b>Đã bật, chưa nối.</b> Bấm Nối, rồi bấm Allow khi " + esc(ten) + " hỏi.</span>" +
        "<button type='button' class='tbd-nut chinh nho' data-tbd-ngoai='noi'>Nối ngay</button></div>" + (cur.loi_noi ? "<p style='color:#f59e0b;margin-top:8px'>Lần trước anh chưa bấm Allow hoặc đã bấm Không. Bấm Nối ngay để thử lại.</p>" : "");
      else h += "<div class='tbd-xn' style='border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.08))'><p><b>Bật một lần cho " + esc(ten) + " (khoảng 20 giây):</b></p>" +
        "<ol class='tbd-buoc'><li>Mở tab mới, dán địa chỉ <code>chrome://inspect/#remote-debugging</code> rồi Enter. <button type='button' class='tbd-nut nho' data-tbd-ngoai='chep'>Chép địa chỉ</button></li>" +
        "<li>Tích ô <b>Allow remote debugging for this browser instance</b>.</li><li>Quay lại đây bấm <b>Nối ngay</b>, " + esc(ten) + " hỏi thì bấm <b>Allow</b>.</li></ol>" +
        "<div class='tbd-hang' style='margin-top:10px'><button type='button' class='tbd-nut chinh' data-tbd-ngoai='noi'>Nối ngay</button></div>" +
        (LOI_NG ? "<p style='color:#d93025;margin:10px 0 0'><b>" + esc(LOI_NG) + "</b></p>" : "") +
        "<p style='margin:10px 0 0'>Chỉ chạy khi TISA BOT và " + esc(ten) + " ở cùng một máy. Muốn tắt thì bỏ tích ô đó.</p></div>";
    } else {
      h += "<div class='tbd-dong'><span class='tbd-nhan'><i class='tbd-cham " + (chay ? "on" : "") + "'></i><b>Cửa sổ:</b> " + (chay ? "đang mở" + (soTab ? ", " + soTab + " tab" : "") : "chưa mở") + "</span>" +
        "<button type='button' class='tbd-nut chinh nho' data-tbd='mo'>" + (chay ? "Hiện cửa sổ lên" : "Mở cửa sổ") + "</button>" +
        (chay ? "<button type='button' class='tbd-nut nho' data-tbd='dong'>Đóng cửa sổ</button>" : "") + "</div>";
    }
    h += "<div class='tbd-dong'><span class='tbd-nhan'><i class='tbd-cham " + (d.dung ? "dung" : "on") + "'></i><b>AI:</b> " + (d.dung ? "đang bị dừng, chưa làm gì" : "được phép làm việc") + "</span>" +
      (d.dung ? "<button type='button' class='tbd-nut chinh nho' data-tbd='tiep'>Cho AI làm tiếp</button>" : "<button type='button' class='tbd-nut do nho' data-tbd='dung'>Dừng AI ngay</button>") + "</div>" +
      (d.loi ? "<p style='color:#ef4444;margin-top:8px'>" + esc(d.loi) + "</p>" : "") + "</div>";
    // Bước 2: tài khoản
    var dn = "<div class='tbd-the'><h3>2. Tài khoản trong \"" + esc(cur.ten) + "\"</h3>";
    if (ngoai) dn += "<p class='tbd-goi'>Không cần làm gì thêm: AI dùng luôn các tài khoản anh đang đăng nhập trong " + esc(TEN_TR[cur.trinh] || "Chrome") + " này (Facebook, Google, TikTok...). Mật khẩu, mã xác thực, thanh toán AI vẫn không làm thay anh.</p>";
    else if (nhapUI) dn += theNhap();
    else dn += "<p class='tbd-goi'>Cách nhanh: chép đăng nhập từ Chrome anh đang dùng, khỏi đăng nhập lại Facebook, TikTok, Zalo... Riêng Google vẫn phải đăng nhập lại một lần. Hoặc bấm Mở cửa sổ ở trên rồi tự đăng nhập như bình thường.</p>" +
      "<div class='tbd-hang'><button type='button' class='tbd-nut chinh' data-nhap='mo'>Chép đăng nhập từ Chrome của anh</button>" +
      (cur.nhap_tu ? "<button type='button' class='tbd-nut' data-nhap='lam_moi' title='Chép lại đăng nhập mới nhất từ " + esc(cur.nhap_tu) + "'>Chép lại đăng nhập mới nhất</button>" : "") + "</div>";
    dn += "</div>";
    // Thêm, đổi tên, xóa: ít dùng nên gập lại
    var ql = "<div class='tbd-hang'><button type='button' class='tbd-nut nho' data-tbd-hs-act='them'>+ Thêm trình duyệt riêng</button><button type='button' class='tbd-nut nho' data-tbd-hs-act='doi'>Đổi tên</button>" +
      (ds.length > 1 ? "<button type='button' class='tbd-nut nho' data-tbd-hs-act='xoa'>" + (ngoai ? "Bỏ khỏi danh sách" : "Xóa trình duyệt này") + "</button>" : "") + "</div>" +
      "<p class='tbd-kn-mo' style='margin-top:8px'>Trình duyệt riêng là một cửa sổ Chrome tách biệt do TISA BOT mở, mỗi cái đăng nhập một bộ tài khoản (ví dụ Facebook A, Facebook B).</p>";
    if (hsForm === "them" || hsForm === "doi") ql += "<div class='tbd-xn tbd-ten'><p><b>" + (hsForm === "them" ? "Tên trình duyệt mới" : "Tên mới cho \"" + esc(cur.ten) + "\"") + "</b></p><div class='tbd-hang'><input id='tbdTen' type='text' maxlength='40' value='" + (hsForm === "doi" ? esc(cur.ten) : "") + "' placeholder='Ví dụ Facebook Sang'>" +
      "<button type='button' class='tbd-nut chinh' data-tbd-hs-act='ok'>" + (hsForm === "them" ? "Tạo" : "Lưu") + "</button><button type='button' class='tbd-nut' data-tbd-hs-act='huy'>Hủy</button></div></div>";
    if (hsForm === "xoa") ql += "<div class='tbd-xn'><p><b>" + (ngoai ? "Bỏ \"" + esc(cur.ten) + "\" khỏi danh sách?</b> Chrome và tài khoản của anh không bị ảnh hưởng, AI chỉ thôi dùng nó." : "Xóa \"" + esc(cur.ten) + "\"?</b> Mọi đăng nhập trong trình duyệt này sẽ mất.") + "</p><div class='tbd-hang'><button type='button' class='tbd-nut do' data-tbd-hs-act='xoa_ok'>" + (ngoai ? "Bỏ" : "Xóa") + "</button><button type='button' class='tbd-nut' data-tbd-hs-act='huy'>Hủy</button></div></div>";
    return h + dn + "<div class='tbd-the'>" + dt("ql", "Thêm, đổi tên hoặc xóa trình duyệt", ql, !!hsForm) + "</div>";
  }
  // (V3.02) Trình duyệt đang mở TISA BOT là loại nào (chỉ Chrome, Edge, Brave trên máy tính mới nối được).
  var LOI_NG = "";
  var TEN_TR = { chrome: "Chrome", edge: "Edge", brave: "Brave", chromium: "Chromium" };
  function trinhNay() {
    var n = W.navigator || {}, ua = n.userAgent || "", b = ((n.userAgentData && n.userAgentData.brands) || []).map(function (x) { return x.brand; }).join(" ");
    if ((n.userAgentData && n.userAgentData.mobile) || /Android|iPhone|iPad|Mobile/.test(ua)) return "";
    if (/Edg\//.test(ua) || /Edge/.test(b)) return "edge";
    if (n.brave || /Brave/.test(b)) return "brave";
    if (/Google Chrome/.test(b) || (/Chrome\//.test(ua) && !/OPR\/|Electron|Tauri|wv\)/.test(ua))) return "chrome";
    return "";
  }
  function veTb() {
    var d = ST, h = "";
    (d.cho_duyet || []).forEach(function (x) { h += theDuyet(x); });
    if (d.cho_nguoi) h += "<div class='tbd-the tbd-duyet'><h3>AI đang chờ anh</h3><p>" + esc(d.cho_nguoi.ly_do) + ". Anh làm ngay trong cửa sổ trình duyệt rồi AI tự làm tiếp.</p></div>";
    h += theHoSo(d) + theMuc(d);
    var dn = DNL === null ? "<p class='tbd-kn-mo'>Đang tải...</p>" : (DNL.length ? "<div class='tbd-luoi'>" + DNL.slice(0, 24).map(function (x) { return "<span class='tbd-mien" + (x.phien ? " phien" : "") + "'>" + esc(x.mien) + (x.phien ? " <i>✓</i>" : "") + "</span>"; }).join("") + "</div>" : "<p class='tbd-kn-mo'>Chưa thấy trang nào đã đăng nhập (hoặc trình duyệt chưa mở).</p>");
    h += "<div class='tbd-the'>" + dt("dn", "Trang đã đăng nhập, mở nhanh", dn + "<div class='tbd-luoi' style='margin-top:10px'><button type='button' class='tbd-nut nho chinh' data-tbd-mo='" + esc(location.origin + "/") + "'>Mở TISA BOT</button>" + TRANG.map(function (t) { return "<button type='button' class='tbd-nut nho' data-tbd-mo='" + esc(t[1]) + "'>" + esc(t[0]) + "</button>"; }).join("") + "</div>") +
      dt("nk", "AI vừa làm gì", (d.nhat_ky || []).length ? "<div class='tbd-nk'>" + (d.nhat_ky || []).slice().reverse().slice(0, 8).map(dongNk).join("") + "</div>" : "<p class='tbd-kn-mo'>Chưa có thao tác nào.</p>") + "</div>";
    return h;
  }

  /* ---------- Điều khiển máy tính (tab thứ hai) ---------- */
  var TAB = "tb", STM = null, hoiToanM = false, hoiXoa = false;
  var MOTA_MAY = { tat: "AI không được dùng máy tính của anh (vẫn làm được bằng trình duyệt).", hoi_het: "AI xin duyệt từng cú bấm, gõ, mở ứng dụng.", quan_trong: "Khuyên dùng. AI tự xem, mở ứng dụng, bấm thường; hỏi khi gõ lệnh, gửi tin, đổi cài đặt.", toan_quyen: "AI tự làm mọi thao tác, không hỏi. Vẫn không xóa tệp, không mở ví, ngân hàng, mật khẩu." };
  var MUC_MAY = [["tat", "Không cho"], ["hoi_het", "Hỏi mọi bước"], ["quan_trong", "Hỏi bước quan trọng"], ["toan_quyen", "Toàn quyền"]];
  /* ---------- Mở khóa máy (Mac): ô nhập mật khẩu, bật/tắt, Zalo của anh ---------- */
  var MK = null, mkLoi = "", mkOk = "", mkDoi = false, mkXoa = false;
  function layMk() { return api("/mo-khoa/trang-thai").then(function (r) { MK = r || {}; return MK; }); }
  function veMoKhoa() {
    var m = MK;
    if (!m || m.ho_tro === undefined) return "";
    var h = "<div class='tbd-the' id='tbdMkThe'><h3>Mở khóa máy</h3>";
    if (!m.ho_tro) return h + "<p class='tbd-kn-mo'>Máy này không phải Mac. Trên Windows, màn hình khóa nằm ngoài tầm của chương trình chạy trong phiên đăng nhập nên TISA BOT chưa mở khóa từ xa được. Cách phòng: nhờ AI giữ máy thức khi có việc dài (\"giữ máy thức\"), và anh cân nhắc tắt yêu cầu đăng nhập khi máy thức dậy trong Cài đặt Windows nếu anh chấp nhận rủi ro.</p></div>";
    var tt = !m.da_cai ? "Chưa nhập mật khẩu" : (m.bat ? "Đang BẬT" : "Đã nhập mật khẩu, đang TẮT");
    h += "<p class='tbd-kn-mo'>Máy Mac khóa màn hình mà anh ở xa? Anh nhắn <b>\"mở khóa máy\"</b> ở bất kỳ ô chat nào trong TISA BOT, AI tự mở. Mật khẩu cất trong Keychain của máy, không nằm trong chat và AI không đọc được.</p>" +
      "<div class='tbd-tt' style='margin:8px 0'><span><i class='tbd-cham " + (m.da_cai && m.bat ? "on" : "") + "'></i>" + esc(tt) + "</span>" +
      (m.da_cai ? (m.bat ? "<button type='button' class='tbd-nut nho' data-mk='tat'>Tắt</button>" : "<button type='button' class='tbd-nut chinh nho' data-mk='bat'>Bật</button>") : "") + "</div>";
    if (!m.da_cai || mkDoi) {
      h += "<div class='tbd-xn tbd-ten'><p><b>" + (m.da_cai ? "Đổi mật khẩu máy" : "Nhập mật khẩu đăng nhập của máy") + "</b></p><div class='tbd-hang'><input id='tbdMkPw' type='password' autocomplete='new-password' autocapitalize='off' spellcheck='false' maxlength='200' placeholder='Mật khẩu anh dùng để mở máy'>" +
        "<button type='button' class='tbd-nut chinh' data-mk='luu'>Kiểm tra và lưu</button>" + (m.da_cai ? "<button type='button' class='tbd-nut' data-mk='huy'>Hủy</button>" : "") + "</div>" +
        "<p class='tbd-kn-mo'>TISA BOT kiểm mật khẩu đúng với máy rồi mới lưu vào Keychain. Sai thì không lưu.</p></div>";
    } else if (mkXoa) {
      h += "<div class='tbd-xn'><p><b>Xóa mật khẩu khỏi Keychain?</b> AI sẽ không mở khóa máy được nữa cho tới khi anh nhập lại.</p><div class='tbd-hang'><button type='button' class='tbd-nut do' data-mk='xoa-ok'>Xóa</button><button type='button' class='tbd-nut' data-mk='huy'>Hủy</button></div></div>";
    } else {
      h += "<div class='tbd-hang'><button type='button' class='tbd-nut nho' data-mk='doi'>Đổi mật khẩu</button><button type='button' class='tbd-nut nho' data-mk='xoa'>Xóa mật khẩu</button></div>";
    }
    if (mkLoi) h += "<p class='tbd-kn-mo' style='color:#f87171'><b>" + esc(mkLoi) + "</b></p>";
    if (mkOk) h += "<p class='tbd-kn-mo' style='color:#34d399'><b>" + esc(mkOk) + "</b></p>";
    if (m.con_lai !== undefined && m.con_lai < m.toi_da) {
      h += "<p class='tbd-kn-mo'>" + (m.con_lai <= 0 ? "AI đã thử " + m.toi_da + " lần không mở được nên đang dừng khoảng " + Math.max(1, Math.ceil((m.giay_dung || 0) / 60)) + " phút. " : "Còn " + m.con_lai + "/" + m.toi_da + " lần thử. ") +
        "<button type='button' class='tbd-nut nho' data-mk='lai'>Cho thử lại</button></p>";
    }
    var zc = m.zalo_cho || [], zd = m.zalo || [];
    zc.forEach(function (z) {
      h += "<div class='tbd-xn'><p><b>Có tin Zalo (…" + esc(String(z.id).slice(-4)) + ") vừa nhắn xin mở khóa máy.</b> Đó có phải Zalo của anh không? Chỉ Zalo anh xác nhận mới được mở khóa.</p><div class='tbd-hang'>" +
        "<button type='button' class='tbd-nut chinh nho' data-mk='zalo-them' data-id='" + esc(z.id) + "'>Đây là Zalo của anh</button><button type='button' class='tbd-nut nho' data-mk='zalo-bo-cho' data-id='" + esc(z.id) + "'>Không phải</button></div></div>";
    });
    if (zd.length) h += "<p class='tbd-kn-mo'>Zalo của anh được mở khóa: " + zd.map(function (z) { return "…" + esc(String(z.id).slice(-4)) + " <button type='button' class='tbd-nut nho' data-mk='zalo-bo' data-id='" + esc(z.id) + "'>Bỏ</button>"; }).join(" ") + "</p>";
    var nk = (m.nhat_ky || []).slice().reverse().slice(0, 3);
    if (nk.length) h += "<div class='tbd-nk' style='margin-top:6px'>" + nk.map(function (x) { return "<div class='tbd-kn-mo'>" + esc(String(x.luc || "").slice(5, 16)) + " · " + esc(x.kenh || "") + " · " + esc(x.ket_qua || "") + "</div>"; }).join("") + "</div>";
    return h + "</div>";
  }
  function veMay() {
    var d = STM || {}, q = d.quyen || {}, h = "";
    if (d.ho_tro === false) return "<div class='tbd-the'><h3>Chưa hỗ trợ</h3><p>Máy này chưa hỗ trợ điều khiển máy tính (cần macOS hoặc Windows).</p></div>";
    (ST && ST.cho_duyet || []).forEach(function (x) { h += theDuyet(x); });
    var macOS = d.he === "macOS", thieu = macOS && (!q.tro_nang || q.ghi_man_hinh === false), cur = d.muc || "quan_trong";
    h += "<div class='tbd-the'><h3>Điều khiển máy tính</h3>" + dongSeg("data-may-muc", cur, MUC_MAY, d) + "<p class='tbd-kn-mo'>" + esc(MOTA_MAY[cur] || "") + "</p>";
    if (hoiToanM) h += "<div class='tbd-xn'><p><b>Bật Toàn quyền điều khiển máy?</b> AI tự bấm, gõ, mở ứng dụng mà không hỏi. Đưa chuột về góc trên trái màn hình hoặc bấm Dừng AI ngay để dừng.</p>" +
      "<div class='tbd-hang'><select id='tbdPhutM'><option value='30'>30 phút</option><option value='120' selected>2 giờ</option><option value='480'>8 giờ</option><option value='0'>Đến khi anh tắt</option></select>" +
      "<button type='button' class='tbd-nut do' data-may-muc-ok='1'>Bật Toàn quyền</button><button type='button' class='tbd-nut' data-may-muc-ok='0'>Hủy</button></div></div>";
    h += "<div class='tbd-tt' style='margin-top:10px'><span><i class='tbd-cham " + (d.dung ? "dung" : thieu ? "" : "on") + "'></i>" + (d.dung ? "Đã dừng AI" : thieu ? "Còn thiếu quyền macOS" : "Sẵn sàng") + "</span>" +
      (d.dung ? "<button type='button' class='tbd-nut chinh nho' data-may-act='tiep'>Cho AI làm tiếp</button>" : "<button type='button' class='tbd-nut do nho' data-may-act='dung'>Dừng AI ngay</button>") +
      "<button type='button' class='tbd-nut nho' data-may-act='thu'>Thử chụp màn hình</button></div><div id='tbdAnhThu' style='margin-top:10px'></div></div>";
    h += veMoKhoa();
    if (thieu) h += "<div class='tbd-the tbd-duyet'><h3>macOS cần anh bật 2 quyền</h3><p>Trợ năng: <b>" + (q.tro_nang ? "đã cấp" : "chưa") + "</b> · Ghi màn hình: <b>" + (q.ghi_man_hinh === false ? "chưa" : "đã cấp") + "</b>. Bấm nút dưới, TISA BOT mở sẵn Cài đặt; anh chỉ cần bật công tắc (bấm + nếu chưa thấy <code style='word-break:break-all'>" + esc(q.chuong_trinh || "") + "</code>). Có thể hỏi mật khẩu máy.</p>" +
      "<div class='tbd-hang'><button type='button' class='tbd-nut chinh' data-may-act='cai-quyen'>Mở cài đặt giúp anh</button></div></div>";
    var xoa = d.cho_xoa_giay || 0, nx;
    if (hoiXoa) nx = "<div class='tbd-xn'><p><b>Cho AI xóa tệp?</b> Tệp bị xóa có thể không khôi phục được. Tự tắt khi hết giờ.</p><div class='tbd-hang'><select id='tbdPhutX'><option value='10'>10 phút</option><option value='30'>30 phút</option><option value='60'>1 giờ</option></select><button type='button' class='tbd-nut do' data-may-xoa-ok='1'>Cho phép xóa</button><button type='button' class='tbd-nut' data-may-xoa-ok='0'>Hủy</button></div></div>";
    else nx = "<p class='tbd-kn-mo'>" + (xoa ? "<b>Đang BẬT</b>, còn khoảng " + Math.ceil(xoa / 60) + " phút." : "Đang tắt: AI không xóa tệp ở mọi mức.") + "</p><div class='tbd-hang'>" + (xoa ? "<button type='button' class='tbd-nut chinh nho' data-may-xoa='tat'>Tắt quyền xóa</button>" : "<button type='button' class='tbd-nut do nho' data-may-xoa='bat'>Bật quyền xóa...</button>") + "</div>";
    h += "<div class='tbd-the'>" + dt("xoa", "Quyền xóa tệp", nx, !!(hoiXoa || xoa)) +
      dt("nkm", "AI vừa làm gì trên máy", (d.nhat_ky || []).length ? "<div class='tbd-nk'>" + (d.nhat_ky || []).slice().reverse().slice(0, 8).map(function (x) { return dongNk({ t: x.t, op: String(x.op || "").replace(/^may_/, ""), ten: x.ten, mo_ta: x.mo_ta, ket_qua: x.ket_qua }); }).join("") + "</div>" : "<p class='tbd-kn-mo'>Chưa có thao tác nào.</p>") + "</div>";
    return h;
  }
  function ve() {
    if (!lop || !ST) return;
    var tabs = "<div class='tbd-tabs'><button type='button' class='" + (TAB === "tb" ? "on" : "") + "' data-tbd-tab='tb'>Trình duyệt</button><button type='button' class='" + (TAB === "may" ? "on" : "") + "' data-tbd-tab='may'>Máy tính</button></div>";
    var nd = TAB === "may" ? veMay() : veTb();
    var kh = tabs + nd, than = lop.querySelector(".tbd-than");
    if (than.__tbdKh === kh) return;      // nội dung y hệt thì KHÔNG vẽ lại (vẽ lại mỗi 4 giây làm bảng chớp và mất ảnh chụp đang xem)
    than.__tbdKh = kh; than.innerHTML = kh;
  }

  // Đang gõ tên, chọn thời hạn hay mở hộp xác nhận thì KHÔNG vẽ lại bảng (vẽ lại mỗi 3 giây làm mất chữ đang gõ).
  function dangNhap() {
    var a = D.activeElement;
    return !!(hsForm || nhapUI || hoiToan || hoiToanM || hoiXoa || mkDoi || mkXoa || (a && lop && lop.contains(a) && /^(INPUT|SELECT|TEXTAREA)$/.test(a.tagName)));
  }
  function lam(nhe) {
    var p2 = (TAB === "may" && lop) ? Promise.all([api("/may-ai/trang-thai").then(function (m) { STM = m || {}; }), layMk()]) : Promise.resolve();
    var q = "?nhe=1&" + (XEM ? "hoso=" + encodeURIComponent(XEM) : "");      // luôn nhẹ: danh sách trang đã đăng nhập chỉ tải khi anh mở mục đó
    return Promise.all([api("/trinh-duyet/trang-thai" + q), p2]).then(function (r) { ST = r[0] || {}; if (lop && !dangNhap()) ve(); thongBao(); return ST; });
  }

  // Thông báo nổi: anh bấm × thì tắt, nhớ lại (kể cả khi tải lại trang) để không hiện lại cùng một thông báo.
  function daTat(k) { try { return (localStorage.getItem("tbd-tat:" + k) || "") === "1"; } catch (e) { return !!(window.__tbdTat && window.__tbdTat[k]); } }
  function tatNoi(k) {
    try { localStorage.setItem("tbd-tat:" + k, "1"); } catch (e) { window.__tbdTat = window.__tbdTat || {}; window.__tbdTat[k] = 1; }
  }
  function thongBao() {
    if (!ST) return;
    veChon();
    var ds = (ST.cho_duyet || []).filter(function (x) { return !daTat("d:" + x.id); }), cn = ST.cho_nguoi;
    if (cn && daTat("cn:" + (cn.luc || cn.ly_do))) cn = null;       // anh đã bấm × thông báo này: không hiện lại cho tới khi có thông báo mới
    if (!ds.length && !cn) { if (noi) { noi.remove(); noi = null; } return; }
    if (lop) { if (noi) { noi.remove(); noi = null; } return; }       // trong bảng đã hiện
    css();
    if (!noi) { noi = D.createElement("div"); noi.className = "tbd-noi"; D.body.appendChild(noi); }
    noi.innerHTML = ds.map(function (x) {
      return "<div class='tbd-ntc'><button type='button' class='tbd-dong' data-tbd-dong='d:" + esc(x.id) + "' aria-label='Tắt thông báo' title='Tắt thông báo (việc vẫn chờ trong chuông Thông báo)'>×</button><b>AI xin duyệt: " + esc(x.mo_ta) + "</b><small>Nút \"" + esc(x.ten || "") + "\" trên " + esc(x.host) + "</small><div class='tbd-hang'>" +
        "<button type='button' class='tbd-nut chinh nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='1'>Duyệt</button><button type='button' class='tbd-nut nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='1' data-tat='30'>Duyệt, đừng hỏi nữa</button><button type='button' class='tbd-nut nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='0'>Không</button>" +
        "<button type='button' class='tbd-nut nho' data-tbd='bang'>Xem</button></div></div>";
    }).join("") + (cn ? "<div class='tbd-ntc'><button type='button' class='tbd-dong' data-tbd-dong='cn:" + esc(String(cn.luc || cn.ly_do)) + "' aria-label='Tắt thông báo' title='Tắt thông báo'>×</button><b>AI đang chờ anh</b><small>" + esc(cn.ly_do) + ". Làm trong cửa sổ trình duyệt, xong AI tự làm tiếp.</small><button type='button' class='tbd-nut nho' data-tbd='bang'>Xem</button></div>" : "");
  }

  // Anh bấm Duyệt xong thì AI phải TỰ làm tiếp, không đứng yên chờ anh nhắn: gửi luôn "Anh đã duyệt" khi AI đã trả lời xong (không đè chữ anh đang gõ dở).
  function baoChat() {
    var n = 0;
    (function thu() {
      var i = D.getElementById("chatInput"), b = D.getElementById("sendBtn");
      if (!i || !b || String(i.value || "").trim()) return;
      if (b.disabled && n++ < 60) { setTimeout(thu, 500); return; }      // AI còn đang trả lời: chờ xong rồi gửi
      if (b.disabled) return;
      i.value = "Anh đã duyệt rồi, em làm tiếp nhé."; i.dispatchEvent(new Event("input", { bubbles: true }));
      setTimeout(function () { b.click(); }, 250);
    })();
  }

  function xuLyMk(t) {
    var a = t.getAttribute("data-mk"), id = t.getAttribute("data-id") || "";
    function xong(r) { return layMk().then(function () { ve(); return r; }); }
    mkLoi = ""; mkOk = "";
    if (a === "luu") {
      var ob = D.getElementById("tbdMkPw"), pw = ob ? ob.value : "";
      if (ob) ob.value = "";                                   // xóa khỏi ô ngay, không để mật khẩu nằm lại trên trang
      if (!pw) { mkLoi = "Anh chưa nhập mật khẩu."; ve(); return; }
      t.disabled = true; t.textContent = "Đang kiểm tra...";
      api("/mo-khoa/mat-khau", { mat_khau: pw }).then(function (r) {
        pw = "";
        if (r && r.ok) { mkDoi = false; mkOk = r.da_kiem ? "Đã kiểm đúng với máy và lưu vào Keychain. Tính năng đang BẬT." : "Đã lưu vào Keychain (chưa kiểm được khớp với máy). Tính năng đang BẬT."; }
        else mkLoi = (r && r.loi) || "Không lưu được. Thử lại giúp anh.";
        return xong(r);
      });
      return;
    }
    if (a === "doi") { mkDoi = true; mkXoa = false; ve(); var o2 = D.getElementById("tbdMkPw"); if (o2) o2.focus(); return; }
    if (a === "huy") { mkDoi = false; mkXoa = false; ve(); return; }
    if (a === "xoa") { mkXoa = true; ve(); return; }
    if (a === "xoa-ok") { mkXoa = false; api("/mo-khoa/xoa-mat-khau", {}).then(function () { mkOk = "Đã xóa mật khẩu khỏi Keychain."; return xong(); }); return; }
    if (a === "bat" || a === "tat") { api("/mo-khoa/bat", { bat: a === "bat" }).then(function (r) { if (r && r.ok === false) mkLoi = r.loi || ""; return xong(); }); return; }
    if (a === "lai") { api("/mo-khoa/cho-thu-lai", {}).then(function () { mkOk = "Đã cho AI thử lại."; return xong(); }); return; }
    if (a === "zalo-them" || a === "zalo-bo" || a === "zalo-bo-cho") {
      api("/mo-khoa/zalo", { hanh: a === "zalo-them" ? "them" : (a === "zalo-bo" ? "bo" : "bo_cho"), id: id }).then(function (r) { if (r && r.ok === false) mkLoi = r.loi || ""; else if (a === "zalo-them") mkOk = "Đã xác nhận Zalo của anh. Giờ anh nhắn \"mở khóa máy\" từ Zalo đó là được."; return xong(); });
      return;
    }
  }

  function bam(e) {
    var t = e.target.closest && e.target.closest("[data-tbd-ngoai],[data-nhap],[data-tbd-hs],[data-tbd-hs-act],[data-tbd],[data-tbd-mo],[data-tbd-duyet],[data-tbd-dong],[data-tbd-muc],[data-tbd-muc-ok],[data-tbd-tab],[data-may-muc],[data-may-muc-ok],[data-may-xoa],[data-may-xoa-ok],[data-may-act],[data-mk]");
    if (!t) return;
    if (t.hasAttribute("data-mk")) { xuLyMk(t); return; }
    if (t.hasAttribute("data-tbd-dong")) { tatNoi(t.getAttribute("data-tbd-dong")); thongBao(); return; }
    if (t.hasAttribute("data-tbd-duyet")) {
      var id = t.getAttribute("data-tbd-duyet"), ok = t.getAttribute("data-ok") === "1", tat = Number(t.getAttribute("data-tat") || 0);
      t.disabled = true;
      // (V3.43, chủ báo 22/11: bấm "đừng hỏi nữa" rồi mà vẫn hỏi hoài) Thẻ xin duyệt có thể là của trình duyệt HOẶC của điều khiển máy tính
      // (op may_*, vd gõ phím vào Chrome). Hai bên có mức riêng: trước đây chỉ bật Toàn quyền trình duyệt nên việc trên máy tính vẫn hỏi. Bật cả hai,
      // quyền xóa tệp giữ tắt.
      var truoc = tat ? Promise.all([api("/trinh-duyet/muc", { muc: "toan_quyen", phut: tat }),
        api("/may-ai/trang-thai").then(function (sm) { return (sm && sm.ho_tro === false) ? 0 : Promise.all([api("/may-ai/muc", { muc: "toan_quyen", phut: tat }), api("/may-ai/cho-xoa", { phut: 0 })]); }).catch(function () {})]) : Promise.resolve();
      truoc.then(function () { return api("/trinh-duyet/duyet", { id: id, ok: ok }); }).then(function () { lam(); if (ok) baoChat(); });
      return;
    }
    if (t.hasAttribute("data-nhap")) {
      var na = t.getAttribute("data-nhap");
      if (na === "mo") { nhapUI = { ds: null, chon: null }; ve(); api("/trinh-duyet/nguon-chrome").then(function (r) { if (nhapUI) { nhapUI.ds = (r && r.nguon) || []; ve(); } }); return; }
      if (na === "huy") { nhapUI = null; ve(); lam(); return; }
      if (na === "chon") { var ten0 = (D.getElementById("nhapTen") || {}).value || ""; nhapUI.chon = { nguon: t.getAttribute("data-nguon"), thu_muc: t.getAttribute("data-tm"), ten: t.getAttribute("data-ten") };
        Array.prototype.forEach.call(D.querySelectorAll(".tbd-hsc"), function (b) { b.classList.toggle("on", b === t); });
        var ti2 = D.getElementById("nhapTen"); if (ti2) ti2.value = nhapUI.chon.ten; var okb = lop.querySelector("[data-nhap='ok']"); if (okb) okb.disabled = false; return; }
      if (na === "ok") {
        if (!nhapUI.chon || nhapUI.dang) return;
        var tn = (D.getElementById("nhapTen") || {}).value || nhapUI.chon.ten; nhapUI.dang = true; t.disabled = true; t.textContent = "Đang chép...";
        api("/trinh-duyet/nhap-chrome", { nguon: nhapUI.chon.nguon, thu_muc: nhapUI.chon.thu_muc, ten: tn }).then(function (r) { nhapUI = { kq: r || { ok: false, loi: "Không nhập được." } }; if (r && r.id) { XEM = r.id; api("/trinh-duyet/ho-so", { hanh: "chon", id: r.id }); } ve(); lam(); });
        return;
      }
      if (na === "mo_xong") { var idm = t.getAttribute("data-id"); nhapUI = null; XEM = idm; api("/trinh-duyet/mo", { hoso: idm }).then(function () { setTimeout(function () { lam(); }, 800); }); return; }
      if (na === "lam_moi") { t.disabled = true; t.textContent = "Đang làm mới..."; api("/trinh-duyet/lam-moi-chrome", { id: xemId() }).then(function (r) { ST = ST || {}; ST.loi = r && r.ok === false ? (r.loi || "") : ""; nhapUI = { kq: Object.assign({ ten: "Đăng nhập đã làm mới" }, r || {}) }; ve(); lam(); }); return; }
      return;
    }
    if (t.hasAttribute("data-tbd-ngoai")) {
      var ng = t.getAttribute("data-tbd-ngoai"), trn = (ST && (ST.ho_so_ds || []).filter(function (x) { return x.id === xemId(); })[0] || {}).trinh || trinhNay() || "chrome";
      if (ng === "chep") { var dc = "chrome://inspect/#remote-debugging"; if (trn === "edge") dc = "edge://inspect/#remote-debugging"; if (trn === "brave") dc = "brave://inspect/#remote-debugging";
        (navigator.clipboard ? navigator.clipboard.writeText(dc) : Promise.reject()).then(function () { t.textContent = "Đã chép"; }, function () { t.textContent = dc; }); return; }
      if (ng === "them") { t.disabled = true; api("/trinh-duyet/ngoai", { hanh: "them", trinh: trinhNay() || "chrome" }).then(function (r) { if (r && r.id) XEM = r.id; hsForm = ""; nhapUI = null; DNL = null; lam(); }); return; }
      t.disabled = true; LOI_NG = ""; api("/trinh-duyet/ngoai", { hanh: ng, trinh: trn }).then(function (r) { if (r && r.ok === false && ng === "noi") LOI_NG = "Chưa thấy " + (TEN_TR[trn] || "Chrome") + " bật cho phép. Anh làm bước 1 và 2 ở trên rồi bấm Nối ngay lại."; lam(); });
      return;
    }
    if (t.hasAttribute("data-tbd-hs")) {
      // Bấm vào trình duyệt nào thì AI dùng đúng trình duyệt đó (trước đây chỉ là xem, AI vẫn dùng cái mặc định cũ nên vào nhầm trình duyệt khác).
      XEM = t.getAttribute("data-tbd-hs"); hsForm = ""; nhapUI = null; DNL = null;
      api("/trinh-duyet/ho-so", { hanh: "chon", id: XEM }).then(function () { lam(); });
      return;
    }
    if (t.hasAttribute("data-tbd-hs-act")) {
      var ha = t.getAttribute("data-tbd-hs-act"), idx = xemId();
      if (ha === "them" || ha === "doi" || ha === "xoa") { hsForm = ha === "xoa" ? "xoa" : ha; ve(); var ti = D.getElementById("tbdTen"); if (ti) { ti.focus(); ti.select(); } return; }
      if (ha === "huy") { hsForm = ""; ve(); return; }
      if (ha === "mac_dinh") { api("/trinh-duyet/ho-so", { hanh: "chon", id: idx }).then(function () { lam(); }); return; }
      if (ha === "ok") {
        var ten = (D.getElementById("tbdTen") || {}).value || "", f = hsForm; hsForm = "";
        (f === "them" ? api("/trinh-duyet/ho-so", { hanh: "tao", ten: ten }).then(function (r) { if (r && r.id) { XEM = r.id; api("/trinh-duyet/ho-so", { hanh: "chon", id: r.id }); } return r; }) : api("/trinh-duyet/ho-so", { hanh: "doi_ten", id: idx, ten: ten }))
          .then(function (r) { if (r && r.ok === false) { ST = ST || {}; ST.loi = r.loi || ""; } lam(); });
        return;
      }
      if (ha === "xoa_ok") { hsForm = ""; api("/trinh-duyet/ho-so", { hanh: "xoa", id: idx }).then(function (r) { XEM = ""; if (r && r.ok === false) { ST = ST || {}; ST.loi = r.loi || ""; } lam(); }); return; }
      return;
    }
    if (t.hasAttribute("data-tbd-tab")) { TAB = t.getAttribute("data-tbd-tab"); ve(); lam(); return; }
    if (t.hasAttribute("data-may-muc")) {
      var mm2 = t.getAttribute("data-may-muc");
      if (mm2 === "toan_quyen") { hoiToanM = true; ve(); return; }
      hoiToanM = false; api("/may-ai/muc", { muc: mm2 }).then(function () { lam(); }); return;
    }
    if (t.hasAttribute("data-may-muc-ok")) {
      if (t.getAttribute("data-may-muc-ok") === "1") { var sl = D.getElementById("tbdPhutM"); hoiToanM = false; api("/may-ai/muc", { muc: "toan_quyen", phut: Number(sl ? sl.value : 30) }).then(function () { lam(); }); }
      else { hoiToanM = false; ve(); }
      return;
    }
    if (t.hasAttribute("data-may-xoa")) { if (t.getAttribute("data-may-xoa") === "tat") api("/may-ai/cho-xoa", { phut: 0 }).then(function () { lam(); }); else { hoiXoa = true; ve(); } return; }
    if (t.hasAttribute("data-may-xoa-ok")) {
      if (t.getAttribute("data-may-xoa-ok") === "1") { var sx = D.getElementById("tbdPhutX"); hoiXoa = false; api("/may-ai/cho-xoa", { phut: Number(sx ? sx.value : 10) }).then(function () { lam(); }); }
      else { hoiXoa = false; ve(); }
      return;
    }
    if (t.hasAttribute("data-may-act")) {
      var ma = t.getAttribute("data-may-act");
      if (ma === "dung") api("/may-ai/dung", {}).then(function () { lam(); });
      else if (ma === "tiep") api("/may-ai/tiep-tuc", {}).then(function () { lam(); });
      else if (ma === "cai-quyen") { t.disabled = true; t.textContent = "Đang mở cài đặt..."; api("/may-ai/cai-dat-quyen", {}).then(function () { setTimeout(function () { lam(); }, 1500); }); }
      else if (ma === "q-tro-nang") api("/may-ai/mo-quyen", { loai: "tro_nang" });
      else if (ma === "q-man-hinh") api("/may-ai/mo-quyen", { loai: "man_hinh" });
      else if (ma === "thu") {
        t.disabled = true;
        api("/may-ai/thu", {}).then(function (r) {
          t.disabled = false; var el = D.getElementById("tbdAnhThu"); if (!el) return;
          el.innerHTML = /^Ảnh chụp/.test(String(r.kq || "")) ? "<img alt='Ảnh chụp thử' src='/may-ai/anh-moi?t=" + Date.now() + "' style='max-width:100%;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.2))'><p>Chụp được. AI nhìn thấy màn hình như thế này.</p>" : "<p style='color:#ef4444'>" + esc(r.kq || "Không chụp được") + "</p>";
          lam();
        });
      }
      return;
    }
    if (t.hasAttribute("data-tbd-muc")) {
      var mm = t.getAttribute("data-tbd-muc");
      if (mm === "toan_quyen") { hoiToan = true; ve(); return; }
      hoiToan = false; api("/trinh-duyet/muc", { muc: mm }).then(function () { lam(); });
      return;
    }
    if (t.hasAttribute("data-tbd-muc-ok")) {
      if (t.getAttribute("data-tbd-muc-ok") === "1") { var sel = D.getElementById("tbdPhut"); hoiToan = false; api("/trinh-duyet/muc", { muc: "toan_quyen", phut: Number(sel ? sel.value : 30) }).then(function () { lam(); }); }
      else { hoiToan = false; ve(); }
      return;
    }
    if (t.hasAttribute("data-tbd-mo")) { t.disabled = true; api("/trinh-duyet/mo", { url: t.getAttribute("data-tbd-mo"), hoso: xemId() }).then(function (r) { if (r && r.loi) { ST = ST || {}; ST.loi = r.loi; } setTimeout(function () { lam(); }, 800); }); return; }
    var a = t.getAttribute("data-tbd");
    if (a === "bang") { mo(); return; }
    if (a === "mo") { t.disabled = true; api("/trinh-duyet/mo", { hoso: xemId() }).then(function (r) { ST = ST || {}; ST.loi = (r && r.loi) || ""; setTimeout(function () { lam(); }, 800); }); }
    if (a === "dong") { t.disabled = true; api("/trinh-duyet/dong", { hoso: xemId() }).then(function () { setTimeout(function () { lam(); }, 600); }); }
    if (a === "dung") api("/trinh-duyet/dung", {}).then(function () { lam(); });
    if (a === "tiep") api("/trinh-duyet/tiep-tuc", {}).then(function () { lam(); });
    if (a === "x") dong();
  }

  function taiDn() {
    api("/trinh-duyet/trang-thai?hoso=" + encodeURIComponent(xemId())).then(function (d) { DNL = (d && d.da_dang_nhap) || []; if (lop && !dangNhap()) ve(); });
  }
  D.addEventListener("toggle", function (e) {
    var t = e.target; if (!t || !t.getAttribute || !t.hasAttribute("data-dt")) return;
    var k = t.getAttribute("data-dt"); DT[k] = t.open;
    if (k === "dn" && t.open && DNL === null) taiDn();
  }, true);
  function mo(tab) {
    css3();
    if (tab === "may" || tab === "tb") TAB = tab;
    if (lop) { ve(); lam(); return; }
    lop = D.createElement("div"); lop.className = "tbd-lop"; lop.setAttribute("role", "dialog"); lop.setAttribute("aria-modal", "true"); lop.setAttribute("aria-label", "Trình duyệt TISA");
    lop.innerHTML = "<div class='tbd-cua'><div class='tbd-dau'><span class='tbd-dau-i'>" + ICON + "</span><div class='tbd-dau-t'><b>Điều khiển của AI</b><span>Cho AI làm việc trên web và máy tính của anh</span></div>" +
      "<button type='button' class='tbd-nut' data-tbd='x' aria-label='Đóng'>Đóng</button></div><div class='tbd-than'><p>Đang tải…</p></div></div>";    // có số liệu đã nhớ thì hiện ngay bên dưới, tải mới chạy nền
    lop.addEventListener("mousedown", function (e) { if (e.target === lop) dong(); });
    D.body.appendChild(lop);
    if (noi) { noi.remove(); noi = null; }
    if (ST) ve();
    lam();
    tim = setInterval(function () { lam(); }, 4000);
  }
  function dong() { if (lop) { lop.remove(); lop = null; } if (tim) { clearInterval(tim); tim = null; } thongBao(); }

  var dangNgam = 0;
  function ngam() {
    if (D.hidden && dangNgam >= 3) return;      // đang rảnh và cửa sổ khuất: nghỉ. Đang có việc thì vẫn hỏi (AI có thể cần dán mã vào cửa sổ này).
    api("/trinh-duyet/trang-thai?nhe=1").then(function (d) {
      ST = d || {}; thongBao();
      if (ST.cho_dan) danThu();
      if (ST.cho_ui) uiThu();
      dangNgam = (ST.dang_chay || (ST.cho_duyet || []).length || (ST.cho_chon || []).length || ST.cho_nguoi || ST.cho_dan || ST.cho_ui) ? 0 : Math.min(dangNgam + 1, 6);
    });
  }
  function nhip() { ngam(); setTimeout(nhip, dangNgam >= 3 ? 15000 : (ST && (ST.dang_chay || ST.cho_dan || ST.cho_ui) ? 1500 : 4000)); }

  /* (V2.99) Dán mã thẳng vào ô đang được chọn của cửa sổ TISA BOT. AI dùng điều khiển máy tính click vào ô, rồi gọi op=dan_vao_tisa:
   * giá trị đi từ trang nền tảng qua máy chủ tới ô này, KHÔNG qua mô hình và không vào chat. Ô được che bằng chấm tròn để ảnh chụp màn hình không lộ mã. */
  var danBan = false;
  function oDangChon() {
    var e = D.activeElement;
    if (!e || (e.tagName !== "INPUT" && e.tagName !== "TEXTAREA") || e.readOnly || e.disabled) return null;
    if (e.tagName === "INPUT" && !/^(text|password|search|url|email|tel|)$/i.test(e.type || "")) return null;
    var ac = String(e.getAttribute("autocomplete") || "").toLowerCase();
    if (/current-password|new-password|one-time-code|username/.test(ac)) return null;
    if (e.id === "chatInput" || (e.closest && e.closest(".tbd-lop,#loginForm,[data-login],.login,.auth-card,.composer,.chat-composer,#composer"))) return null;
    return e;
  }
  function nhanO(e) {
    var l = e.labels && e.labels[0] ? e.labels[0].textContent : "";
    return String(e.getAttribute("aria-label") || l || e.placeholder || e.name || e.id || "ô nhập").replace(/\s+/g, " ").trim().slice(0, 60);
  }
  function danThu() {
    if (danBan || !oDangChon()) return;     // chỉ cửa sổ đang có ô được chọn mới nhận mã
    danBan = true;
    api("/trinh-duyet/dan-cho").then(function (r) {
      if (!r || !r.id) { danBan = false; return; }
      return api("/trinh-duyet/dan-lay", { id: r.id }).then(function (g) {
        if (!g || !g.co) { danBan = false; return; }
        var el = oDangChon();
        if (!el) { g.gia_tri = ""; api("/trinh-duyet/dan-xong", { id: r.id, ok: false, loi: "Ô đang chọn không dùng được (khung chat, ô đăng nhập hoặc ô chỉ đọc)." }).then(function () { danBan = false; }); return; }
        var v = String(g.gia_tri || ""), so = v.length;
        var set = Object.getOwnPropertyDescriptor(el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, "value").set;
        set.call(el, v); g.gia_tri = ""; v = "";
        el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true }));
        try { el.style.webkitTextSecurity = "disc"; } catch (e) {}
        api("/trinh-duyet/dan-xong", { id: r.id, ok: true, nhan: nhanO(el), so: so }).then(function () { danBan = false; });
      });
    });
  }

  var ICON_MENU = '<svg class="cp-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>';
  function dangKy(n) {
    var M = W.TISAComposerMenu;
    if (!M || !M.register) { if (n < 60) setTimeout(function () { dangKy(n + 1); }, 250); return; }
    M.register({ id: "trinh_duyet", order: 16, icon: ICON_MENU, label: "Mở trình duyệt cho AI thao tác", hint: function () { return "Đăng nhập một lần"; }, run: function () { mo("tb"); } });
    M.register({ id: "dieu_khien_may", order: 17, icon: ICON_MENU, label: "Cho AI điều khiển máy tính", hint: function () { return "Chuột, bàn phím, ứng dụng"; }, run: function () { mo("may"); } });
  }
  /* Nút luôn thấy bên cạnh dấu + của khung chat (Hỏi nhanh, Hỏi chuyên gia), không cần mở menu. */
  var CSS2 = ".tbd-pill{width:auto!important;max-width:240px;padding:0 11px!important;gap:6px;display:inline-flex;align-items:center;white-space:nowrap;font:600 12.5px/1 inherit;border-radius:999px!important}.tbd-pill svg{width:16px;height:16px;flex:none}" +
    ".tbd-pill{flex:0 1 auto!important;min-width:0}.tbd-pill span{overflow:hidden;text-overflow:ellipsis;min-width:0}.tbd-pill.gon span{display:none}.tbd-pill.gon{padding:0 9px!important}.tbd-pill i{display:none;width:8px;height:8px;border-radius:50%;background:#22c55e}.tbd-pill.on i{display:inline-block}@media (max-width:640px){.tbd-pill span{display:none}.tbd-pill{padding:0 9px!important}}";
  // Mọi khung chat (Hỏi nhanh, từng cộng sự ở Hỏi chuyên gia, cuộc trò chuyện mới...) đều có nút: tìm mọi nút + của khung chat.
  function chenNut() {
    var ds = D.querySelectorAll("button.cp-plus:not(.tbd-pill), #plusBtn");
    if (!ds.length) return;
    if (!D.getElementById("tbd-css2")) { var st = D.createElement("style"); st.id = "tbd-css2"; st.textContent = CSS2; (D.head || D.documentElement).appendChild(st); }
    Array.prototype.forEach.call(ds, function (p) {
      if (!p.parentNode || (p.nextSibling && p.nextSibling.classList && p.nextSibling.classList.contains("tbd-pill"))) return;
      var b = D.createElement("button"); b.type = "button"; b.className = (p.className || "cp-plus").replace(/\bcp-plus\b/, "cp-plus") + " tbd-pill";
      b.title = "Mở trình duyệt cho AI thao tác (anh đăng nhập một lần, AI làm thay)"; b.setAttribute("aria-label", "Mở trình duyệt cho AI thao tác");
      b.innerHTML = ICON + "<span>Trình duyệt AI</span><i></i>";
      b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); mo(); });
      p.parentNode.insertBefore(b, p.nextSibling);
    });
  }
  function chamXanh() {
    var m = ST && ST.muc, ten = m === "hoi_het" ? "Hỏi mọi bước" : m === "toan_quyen" ? "Toàn quyền" : "Hỏi bước quan trọng";
    Array.prototype.forEach.call(D.querySelectorAll(".tbd-pill"), function (b) {
      b.classList.toggle("on", !!(ST && ST.dang_chay));
      try { var hang = b.parentNode, rong = hang ? hang.clientWidth : 999; b.classList.toggle("gon", rong > 0 && rong < 560); } catch (e) {}   // hàng nút hẹp (khung chat nhiều cột): chỉ giữ biểu tượng, nhường chỗ cho model và mức Effort
      var dd = ST && ST.ho_so_ds && ST.hoso_dang_dung ? ST.ho_so_ds.filter(function (x) { return x.id === ST.hoso_dang_dung; })[0] : null;
      var lb = b.querySelector("span"); if (lb) lb.textContent = dd ? ("Trình duyệt: " + dd.ten) : "Trình duyệt AI";
      b.title = "AI đang dùng " + (dd ? dd.ten : "trình duyệt") + ". Bấm để mở, đổi trình duyệt. Mức tự động: " + ten;
    });
  }
  W.addEventListener("message", function (e) { if (e.data && e.data.tisaTrinhDuyet === "mo") mo(); });

  /* ---------- (V3.20) Thẻ "MCP của Claude Code đã nối vào TISA BOT" ở trang Kết nối ----------
   * Chủ yêu cầu 18/11/2026: MCP đã kết nối bên Claude Code (Meta Ads...) thì TISA BOT tự dùng, mặc định, và hiện ra để biết đã nối thành công.
   * Dữ liệu từ /tisa-claude-mcp/trang-thai (máy chủ chạy `claude mcp list` ở nền, cất kết quả). */
  var CMCP = { d: null, luc: 0, dang: false };
  function mauTT(t) { return t === "ok" ? "#16a34a" : t === "can_dang_nhap" ? "#d97706" : "#dc2626"; }
  function chuTT(t) { return t === "ok" ? "đã kết nối" : t === "can_dang_nhap" ? "cần đăng nhập lại" : "lỗi"; }
  function veClaudeMcp() {
    var o = D.getElementById("tbdClaudeMcp");
    if (!trangKetNoi()) { if (o) o.remove(); return; }
    var host = D.getElementById("cviewBody") || D.querySelector(".cview-body");
    if (!host) return;
    if (!o) {
      o = D.createElement("div"); o.id = "tbdClaudeMcp";
      o.style.cssText = "margin:0 0 14px;padding:14px 16px;border-radius:16px;border:1px solid rgba(23,47,114,.18);background:linear-gradient(135deg,rgba(255,107,53,.07),rgba(23,47,114,.05));font-size:14px;line-height:1.5;max-width:980px";
      host.insertBefore(o, host.firstChild);
    }
    var d = CMCP.d, h;
    if (!d) h = "<b>MCP của Claude Code</b> · đang kiểm tra...";
    else if (d.co_claude === false) h = "<b>MCP của Claude Code</b><div style='color:var(--mm-muted,#5b6478)'>Máy chưa có Claude Code nên chưa có MCP nào để nối. Cài Claude Code (và đăng nhập) là TISA BOT tự dùng được MCP đó, không cần cấu hình thêm.</div>";
    else {
      var ts = d.tom_tat || {}, ma = ts.meta_ads || {}, ds = d.may_chu || [];
      var dau = ts.ket_noi_tot > 0 ? "<span style='display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#16a34a;color:#fff;font-weight:800;font-size:13px;margin-right:8px'>✓</span>" : "<span style='display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#d97706;color:#fff;font-weight:800;margin-right:8px'>!</span>";
      h = dau + "<b>" + (ts.ket_noi_tot > 0 ? "Đã nối MCP của Claude Code vào TISA BOT" : "Chưa có MCP nào của Claude Code đang kết nối") + "</b>" +
        "<span style='color:var(--mm-muted,#5b6478)'> · " + (ts.ket_noi_tot || 0) + "/" + (ts.tong || 0) + " kết nối đang chạy" + (d.dang_quet ? " · đang kiểm tra lại..." : "") + "</span>";
      if (ma.co) h += "<div style='margin-top:6px'>" + (ma.ok ? "<b style='color:#16a34a'>✓ Meta Ads (Facebook Ads) đã nối</b>: nhắn TISA BOT để xem tài khoản, báo cáo số liệu, lên chiến dịch, tắt bật chiến dịch." : "<b style='color:#d97706'>Meta Ads có trong Claude Code nhưng " + chuTT(ma.trang_thai) + "</b>: mở Claude Code, vào Connectors, đăng nhập lại Meta Ads.") + "</div>";
      else h += "<div style='margin-top:6px;color:#b45309'>Chưa thấy Meta Ads (Facebook Ads) trong Claude Code. Mở Claude Code, vào Connectors, thêm Meta Ads; xong bấm Kiểm tra lại.</div>";
      if (d.engine_la_claude === false) h += "<div style='margin-top:6px;color:#b45309'>Lưu ý: MCP của Claude Code chỉ dùng khi TISA BOT chạy bằng Claude. Hiện đang chọn " + escH(d.engine) + ", ChatGPT/Codex có kho MCP riêng.</div>";
      h += "<div style='display:flex;flex-wrap:wrap;gap:6px;margin-top:10px'>" + ds.map(function (x) {
        return "<span title='" + escH(x.dia_chi + (x.chi_tiet ? " · " + x.chi_tiet : "")) + "' style='display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;background:var(--mm-card,#fff);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,rgba(23,47,114,.15));font-size:12.5px'><i style='width:8px;height:8px;border-radius:50%;background:" + mauTT(x.trang_thai) + "'></i>" + escH(x.ten) + "</span>";
      }).join("") + "</div>";
    }
    h += "<div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:10px'><button type='button' data-cmcp='quet' style='padding:6px 12px;border-radius:10px;border:1px solid var(--mm-line2,rgba(23,47,114,.25));background:var(--mm-soft2,#f4f6fc);color:var(--mm-ink,#172033);font:600 12.5px inherit;cursor:pointer'>Kiểm tra lại</button>" +
      (d && d.tom_tat && d.tom_tat.meta_ads && d.tom_tat.meta_ads.ok ? "<button type='button' data-cmcp='thu' style='padding:6px 12px;border-radius:10px;border:0;background:#ff6b35;color:#fff;font:700 12.5px inherit;cursor:pointer'>Thử: liệt kê tài khoản quảng cáo</button>" : "") + "</div>";
    if (o.getAttribute("data-k") !== h) { o.innerHTML = h; o.setAttribute("data-k", h); }
  }
  function taiClaudeMcp(ep) {
    if (CMCP.dang) return;
    CMCP.dang = true;
    (ep ? api("/tisa-claude-mcp/quet", {}) : api("/tisa-claude-mcp/trang-thai")).then(function (d) {
      CMCP.d = d && d.ok ? d : CMCP.d; CMCP.luc = Date.now(); CMCP.dang = false; veClaudeMcp();
      if (CMCP.d && CMCP.d.dang_quet) setTimeout(function () { taiClaudeMcp(false); }, 6000);       // đang quét nền: lát nữa lấy kết quả
    });
  }
  /* Thẻ "Trợ lý đấu nối" ở trang Kết nối: cho biết ai đang làm việc nối và mô hình, mức nỗ lực đang dùng; nút Cài đặt mở hộp chọn. */
  var DN = { d: null, luc: 0, dang: false };
  function taiDauNoi() {
    if (DN.dang) return; DN.dang = true;
    fetch("/tisa-dau-noi/cai-dat").then(function (r) { return r.json(); }).then(function (d) { DN.d = d; DN.luc = Date.now(); veDauNoi(); }).catch(function () {}).then(function () { DN.dang = false; });
  }
  var NHAN_R = { off: "Tắt", low: "Thấp", medium: "Vừa", high: "Cao", xhigh: "Rất cao", ultra: "Tối đa" };
  function veDauNoi() {
    var o = D.getElementById("tbdDauNoi");
    if (!trangKetNoi()) { if (o) o.remove(); return; }
    var host = D.getElementById("cviewBody") || D.querySelector(".cview-body");
    if (!host) return;
    if (!o) {
      o = D.createElement("div"); o.id = "tbdDauNoi";
      o.style.cssText = "margin:0 0 14px;padding:12px 16px;border-radius:16px;border:1px solid rgba(23,47,114,.18);background:rgba(23,47,114,.04);font-size:14px;line-height:1.5;max-width:960px;display:flex;align-items:center;gap:12px;flex-wrap:wrap";
      var m = D.getElementById("tbdClaudeMcp");
      if (m && m.nextSibling) host.insertBefore(o, m.nextSibling); else if (m) host.appendChild(o); else host.insertBefore(o, host.firstChild);
    }
    var d = DN.d, c = (d && d.cai_dat) || {}, md = (d && d.mac_dinh) || {};
    var mo = c.model ? c.model : "mặc định của TISA BOT", r = NHAN_R[c.reasoning || md.reasoning || "high"] || "Cao";
    o.innerHTML = "<span style='font-size:20px'>🛠️</span><div style='flex:1;min-width:220px'><b>Trợ lý đấu nối: Đạt Đấu Nối</b><div style='color:var(--mm-muted,#5b6478);font-size:13px'>" + (d ? "Mô hình " + escH(mo) + " · nỗ lực " + escH(r) + ". Mọi nút Nhờ TISA BOT kết nối giúp đều giao việc cho cộng sự này." : "Đang kiểm tra...") + "</div></div>" +
      "<button type='button' data-tdn-cd='1' style='padding:7px 14px;border-radius:10px;border:1px solid var(--mm-line2,rgba(23,47,114,.25));background:var(--mm-soft2,#f4f6fc);font:600 13px inherit;cursor:pointer;color:var(--mm-ink,#172033)'>⚙ Cài đặt mô hình</button>";
  }
  function chenDauNoi() {
    if (!trangKetNoi()) { var o = D.getElementById("tbdDauNoi"); if (o) o.remove(); return; }
    if (!DN.d || Date.now() - DN.luc > 60000) taiDauNoi();
    if (!D.getElementById("tbdDauNoi") && DN.d) veDauNoi();
  }
  W.addEventListener("tisa-dau-noi-doi", function () { DN.luc = 0; taiDauNoi(); });
  D.addEventListener("click", function (e) { var b = e.target.closest && e.target.closest("[data-tdn-cd]"); if (b && W.TISADauNoi) W.TISADauNoi.moCaiDat(); });
  function chenClaudeMcp() {
    if (!trangKetNoi()) { var o = D.getElementById("tbdClaudeMcp"); if (o) o.remove(); return; }
    if (!CMCP.d || Date.now() - CMCP.luc > 60000) taiClaudeMcp(false);
    veClaudeMcp();
  }
  D.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-cmcp]");
    if (!b) return;
    var k = b.getAttribute("data-cmcp");
    if (k === "quet") { if (CMCP.d) CMCP.d.dang_quet = true; veClaudeMcp(); taiClaudeMcp(true); }
    if (k === "thu") guiNgam("Dùng công cụ MCP Meta Ads của Claude Code (ads_get_ad_accounts, ads_insights_*) liệt kê các tài khoản quảng cáo của anh, rồi cho anh xem chi tiêu 7 ngày gần nhất của vài chiến dịch đang chạy. Chỉ ĐỌC, không đổi hay bật gì.", "Meta Ads qua Claude Code");
  });
  setInterval(function () { chenNut(); chamXanh(); chenKn(); chenAutoKn(); chenClaudeMcp(); chenDauNoi(); }, 1500);
  D.addEventListener("input", function (e) {
    if (!e.target || e.target.id !== "nhapLoc") return;
    var q = e.target.value.toLowerCase().trim();
    Array.prototype.forEach.call(D.querySelectorAll(".tbd-hsc"), function (b) { b.style.display = (!q || (b.getAttribute("data-loc") || "").indexOf(q) >= 0) ? "" : "none"; });
  });
  D.addEventListener("click", bam);
  D.addEventListener("keydown", function (e) {
    if (lop && e.key === "Escape") { e.stopPropagation(); if (hsForm || hoiToan || hoiToanM || hoiXoa) { hsForm = ""; hoiToan = hoiToanM = hoiXoa = false; ve(); } else dong(); return; }
    if (lop && e.key === "Enter" && e.target && e.target.id === "tbdTen") { e.preventDefault(); var ok = lop.querySelector("[data-tbd-hs-act='ok']"); if (ok) ok.click(); }
  }, true);

  /* ---------- (V2.99) AI hỗ trợ kết nối + hộp chọn web ----------
   * Nút "AI hỗ trợ kết nối" ở thanh trên của trang Kết nối: anh gõ hoặc nói muốn nối ứng dụng nào, chọn trình duyệt cho AI, rồi AI
   * đọc hướng dẫn, hỏi anh chọn web để mở (hộp chọn bên dưới), thao tác lấy mã và dán thẳng vào TISA BOT (mã không hiện trong chat). */
  var CSS3 = [
    ".tbd-kn-btn{display:inline-flex;align-items:center;gap:7px;height:38px;padding:0 14px;margin-right:8px;border-radius:999px;border:1px solid var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.12));color:var(--mm-or-ink,#e8541a);font:700 13px/1 inherit;cursor:pointer;white-space:nowrap;flex:none}",
    ".tbd-kn-btn svg{width:17px;height:17px;flex:none}.tbd-kn-btn:hover{filter:brightness(1.08)}.tbd-kn-btn:focus-visible{outline:2px solid var(--mm-or,#ff6b35);outline-offset:2px}",
    "@media (max-width:900px){.tbd-kn-btn span{display:none}.tbd-kn-btn{padding:0 11px}}",
    ".tbd-kn-nd{width:100%;box-sizing:border-box;min-height:88px;padding:11px 12px;border-radius:12px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:var(--mm-base,#131a3a);color:inherit;font:14px/1.5 inherit;resize:vertical}",
    ".tbd-kn-nd:focus{outline:2px solid var(--mm-or,#ff6b35);outline-offset:1px}",
    ".tbd-mic{display:inline-flex;align-items:center;gap:7px}.tbd-mic svg{width:16px;height:16px}.tbd-mic.nghe{background:#d93025;border-color:#d93025;color:#fff}",
    ".tbd-kn-tt{font-size:12.5px;color:var(--mm-muted,#9aa6d6)}",
    ".tbd-kn-sel{height:40px;max-width:100%;padding:0 10px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:var(--mm-base,#131a3a);color:inherit;font:inherit}",
    ".tbd-rd{cursor:pointer}.tbd-rd input{margin-right:8px;accent-color:var(--mm-or,#ff6b35)}.tbd-rd.on{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.12))}",
    ".tbd-rdh{display:flex;align-items:center}.tbd-rdh b{font-size:13.5px}",
    ".tbd-kn-so{display:inline-grid;place-items:center;width:22px;height:22px;margin-right:8px;border-radius:50%;background:var(--mm-or,#ff6b35);color:#fff;font:700 12px/1 inherit}",
    ".tbd-kn-qs{display:grid;gap:14px}.tbd-kn-q{padding:12px;border:1px solid var(--mm-line2,rgba(255,255,255,.18));border-radius:12px}",
    ".tbd-kn-qh{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin-bottom:8px}.tbd-kn-qh b{font-size:14px}.tbd-kn-qh span{font-size:12.5px;color:var(--mm-muted,#9aa6d6)}",
    ".tbd-seg{display:flex;flex-wrap:wrap;gap:6px}.tbd-seg button{flex:1 1 130px;min-height:40px;padding:0 12px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:transparent;color:inherit;font:600 13px/1.2 inherit;cursor:pointer}",
    ".tbd-seg button:hover{background:var(--mm-soft2,rgba(255,255,255,.08))}.tbd-seg button.on{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.14));color:var(--mm-or-ink,#e8541a)}",
    ".tbd-seg button.on.tq{border-color:#d93025;background:rgba(217,48,37,.12);color:#d93025}.tbd-seg button:focus-visible{outline:2px solid var(--mm-or,#ff6b35);outline-offset:2px}",
    ".tbd-kn-mo{margin:8px 0 0;font-size:12.5px;line-height:1.5;color:var(--mm-muted,#9aa6d6)}.tbd-kn-th{margin-top:8px;font-size:13px}",
    ".tbd-kn-hsl{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}.tbd-kn-hs{width:100%}",
    ".tbd-lk{border:0;background:none;padding:0;color:var(--mm-or-ink,#e8541a);font:inherit;text-decoration:underline;cursor:pointer}",
    ".tbd-the h3{margin-bottom:10px}.tbd-dt{margin-top:10px;border-top:1px dashed var(--mm-line2,rgba(255,255,255,.18));padding-top:8px}.tbd-dt summary{cursor:pointer;font:600 13px/1.4 inherit;color:var(--mm-muted,#9aa6d6);list-style:none}.tbd-dt summary::-webkit-details-marker{display:none}.tbd-dt summary::before{content:'▸ ';}.tbd-dt[open] summary::before{content:'▾ ';}.tbd-dt>div{margin-top:8px}",
    ".conn-chip.tbd-auto{border-color:var(--mm-or,#ff6b35);background:var(--mm-or-wash,rgba(255,107,53,.12));color:var(--mm-or-ink,#e8541a);font-weight:700;cursor:pointer}.conn-chip.tbd-auto:hover{filter:brightness(1.06)}",
    ".gcard-btn.tbd-auto{background:var(--mm-or-wash,rgba(255,107,53,.12));border:1px solid var(--mm-or,#ff6b35);color:var(--mm-or-ink,#e8541a);margin-top:6px;font-weight:700}",
    ".tbd-kn-chon input[type=text]{width:100%;box-sizing:border-box;height:38px;margin-top:6px;padding:0 10px;border-radius:9px;border:1px solid var(--mm-line2,rgba(255,255,255,.25));background:var(--mm-base,#131a3a);color:inherit;font:inherit}"
  ].join("");
  function css3() { css(); if (D.getElementById("tbd-css3")) return; var st = D.createElement("style"); st.id = "tbd-css3"; st.textContent = CSS3; (D.head || D.documentElement).appendChild(st); }

  var ICON_KN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0V7zM12 17v5"/></svg>';
  var ICON_MIC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';
  var kn = null, knNghe = null, knTen = [];

  function trangKetNoi() { var N = W.Alpine && W.Alpine.store && W.Alpine.store("nav"); return !!(N && N.active === "mcp"); }
  function chenKn() {
    var c = D.getElementById("tbdKnBtn");
    if (!trangKetNoi()) { if (c) c.remove(); return; }
    var hud = D.querySelector(".hud-top-right");
    if (c || !hud) return;
    css3();
    var b = D.createElement("button"); b.type = "button"; b.id = "tbdKnBtn"; b.className = "tbd-kn-btn";
    b.title = "Nhờ AI kết nối giúp: AI đọc hướng dẫn, mở web, lấy mã và dán vào TISA BOT"; b.setAttribute("aria-label", "AI hỗ trợ kết nối");
    b.innerHTML = ICON_KN + "<span>AI hỗ trợ kết nối</span>";
    b.addEventListener("click", function (e) { e.preventDefault(); moKn(); });
    hud.insertBefore(b, hud.firstChild);
  }

  function tenTheKetNoi() {
    var ds = [], thay = {};
    Array.prototype.forEach.call(D.querySelectorAll("#catGrid .cat-card"), function (c) {
      var nm = c.querySelector(".cat-name"), t = nm && nm.firstChild ? String(nm.firstChild.textContent || "").trim() : "";
      if (!t || /^tự thêm/i.test(t) || thay[t.toLowerCase()] || t.length > 48) return;
      thay[t.toLowerCase()] = 1; ds.push(t);
    });
    return ds.length >= 4 ? ds.slice(0, 14) : ["Meta Ads (quảng cáo Facebook)", "Facebook Fanpage", "Zalo OA", "TikTok Ads", "Google Ads", "Pancake", "Telegram", "Google Sheets"];
  }
  function tenDaNoi() {
    var ds = [];
    Array.prototype.forEach.call(D.querySelectorAll("#connList .prov-name"), function (e) { var t = String(e.textContent || "").trim(); if (t) ds.push(t); });
    return ds.slice(0, 20);
  }

  var QTB = { hoi_het: ["Hỏi mọi bước", "AI xin anh duyệt từng cú bấm, gõ trên web. An toàn nhất, chậm nhất."],
              quan_trong: ["Hỏi bước quan trọng", "Khuyên dùng. AI tự làm các thao tác thường; chỉ hỏi khi đăng, gửi, xóa, đổi bảo mật, cấp quyền, đăng ký."],
              toan_quyen: ["Toàn quyền", "AI tự làm cả những việc trên mà không hỏi, trong thời gian anh chọn, rồi tự về mức Hỏi bước quan trọng."] };
  var QMAY = { tat: ["Không cho", "AI không được dùng máy tính của anh. Việc kết nối chỉ làm trong trình duyệt."],
               hoi_het: ["Hỏi mọi bước", "AI xin duyệt từng cú bấm, gõ, mở ứng dụng trên máy anh."],
               quan_trong: ["Hỏi bước quan trọng", "Khuyên dùng. AI tự xem màn hình, mở ứng dụng, bấm thường; hỏi khi gõ lệnh, gửi tin, đổi cài đặt hệ thống."],
               toan_quyen: ["Toàn quyền", "AI tự làm mọi thao tác trên máy, không hỏi, trong thời gian anh chọn. Vẫn không xóa tệp, không mở ví, ngân hàng, mật khẩu."] };
  var knQ = { tb: "quan_trong", may: "quan_trong", pTb: 30, pMay: 30, hs: "" };
  function khoiQuyen(tb, may) {
    return "<div class='tbd-kn-q'><div class='tbd-kn-qh'><b>" + (tb ? "Điều khiển trình duyệt web" : "Điều khiển máy tính") + "</b><span>" + (tb ? "AI bấm, gõ, mở trang trong trình duyệt" : "AI nhìn màn hình, di chuột, mở ứng dụng, tệp") + "</span></div>" +
      "<div class='tbd-seg' role='radiogroup'>" + Object.keys(tb ? QTB : QMAY).map(function (k) {
        var cur = tb ? knQ.tb : knQ.may;
        return "<button type='button' role='radio' aria-checked='" + (cur === k) + "' class='" + (cur === k ? "on" : "") + (k === "toan_quyen" ? " tq" : "") + "' data-kn-q='" + (tb ? "tb" : "may") + "' data-v='" + k + "'>" + esc((tb ? QTB : QMAY)[k][0]) + "</button>";
      }).join("") + "</div>" +
      "<p class='tbd-kn-mo'>" + esc((tb ? QTB : QMAY)[tb ? knQ.tb : knQ.may][1]) + "</p>" +
      ((tb ? knQ.tb : knQ.may) === "toan_quyen" ? "<div class='tbd-hang tbd-kn-th'><span>Thời gian:</span><select class='tbd-kn-sel' data-kn-p='" + (tb ? "tb" : "may") + "'>" +
        [30, 120, 480].map(function (m) { return "<option value='" + m + "'" + ((tb ? knQ.pTb : knQ.pMay) === m ? " selected" : "") + ">" + (m >= 60 ? (m / 60) + " giờ" : m + " phút") + "</option>"; }).join("") + "</select></div>" : "") + "</div>";
  }
  function veQuyenKn() {
    var q = D.getElementById("knQuyen"); if (q) q.innerHTML = khoiQuyen(true) + khoiQuyen(false) +
      "<p class='tbd-kn-tt'>Luôn do anh tự làm: mật khẩu, mã xác thực, CAPTCHA, thanh toán. AI không xóa tệp trên máy anh.</p>";
    var b = D.getElementById("knTrinhDuyet"); if (b) b.innerHTML = ((ST && ST.ho_so_ds) || []).map(function (x) {
      return "<button type='button' role='radio' aria-checked='" + (knQ.hs === x.id) + "' class='tbd-hsc tbd-kn-hs" + (knQ.hs === x.id ? " on" : "") + "' data-kn-hs='" + esc(x.id) + "'><b>" + esc(x.ten) + "</b><span>" + (x.dang_chay ? "Đang mở" : "Chưa mở, AI sẽ mở khi cần") + (x.nhap_tu ? " · lấy đăng nhập từ " + esc(x.nhap_tu) : "") + "</span></button>";
    }).join("");
  }
  var knUI = null;
  function veQlKn() {
    var e = D.getElementById("knQl"); if (!e) return;
    var u = knUI;
    if (!u) { e.innerHTML = ""; return; }
    var h = "<div class='tbd-the' style='margin:10px 0 0'>";
    if (u.mode === "them") {
      h += "<p><b>Tên trình duyệt mới</b> (ví dụ Facebook Sang, Fanpage Shop A). Mỗi trình duyệt đăng nhập tài khoản riêng.</p><div class='tbd-hang'><input id='knhTen' type='text' class='tbd-loc' style='flex:1 1 200px' maxlength='40' placeholder='Tên trình duyệt' autocomplete='off'>" +
        "<button type='button' class='tbd-nut chinh nho' data-knh='tao'>Tạo</button><button type='button' class='tbd-nut nho' data-knh='huy'>Hủy</button></div>" + (u.loi ? "<p style='color:#ef4444;margin:8px 0 0'>" + esc(u.loi) + "</p>" : "");
    } else if (u.kq) {
      var k = u.kq;
      h += k.ok === false ? "<p style='color:#ef4444'>" + esc(k.loi || "Không nhập được.") + "</p>" :
        "<p><b>Đã nhập xong \"" + esc(k.ten) + "\".</b> Lấy được " + (k.so_cookie || 0) + " cookie." + ((k.dang_nhap || []).length ? " Đang đăng nhập: " + (k.dang_nhap || []).slice(0, 10).map(esc).join(", ") + "." : "") + " Trình duyệt này đã được chọn cho AI.</p>";
      h += "<div class='tbd-hang'><button type='button' class='tbd-nut nho' data-knh='huy'>Xong</button></div>";
    } else if (!u.ds) {
      h += "<p>Đang đọc danh sách hồ sơ Chrome trên máy...</p>";
    } else if (!u.ds.length) {
      h += "<p>Không thấy Chrome, Edge hay Brave nào có hồ sơ trên máy này.</p><div class='tbd-hang'><button type='button' class='tbd-nut nho' data-knh='huy'>Đóng</button></div>";
    } else {
      h += "<p><b>Chọn hồ sơ Chrome anh dùng lâu nay.</b> TISA BOT chép phần đăng nhập sang một trình duyệt riêng nên Facebook, TikTok, Zalo... thường không phải đăng nhập lại (riêng Google thì thường phải đăng nhập lại một lần trong trình duyệt này). Không chép mật khẩu đã lưu, thẻ, lịch sử; Chrome gốc không bị sửa.</p>" +
        (u.ds.some(function (n) { return n.dang_mo; }) ? "<p style='color:#f59e0b'>Chrome đang mở. Nên đóng Chrome trước để lấy đủ đăng nhập mới nhất.</p>" : "") +
        "<input id='knhLoc' type='text' placeholder='Gõ tên hoặc email để lọc' class='tbd-loc'><div class='tbd-ds-chrome' id='knhDs'>";
      u.ds.forEach(function (n) {
        h += "<div class='tbd-nguon'>" + esc(n.ten) + "</div>";
        n.ho_so.forEach(function (x) {
          h += "<button type='button' class='tbd-hsc' data-knh='chon' data-nguon='" + esc(n.ma) + "' data-tm='" + esc(x.thu_muc) + "' data-ten='" + esc(x.ten) + "' data-loc='" + esc((x.ten + " " + x.email).toLowerCase()) + "'><b>" + esc(x.ten) + "</b><span>" + esc(x.email || x.thu_muc) + (x.co_cookie ? "" : " · chưa có đăng nhập") + "</span></button>";
        });
      });
      h += "</div><div class='tbd-hang' style='margin-top:8px'><input id='knhTen' type='text' class='tbd-loc' style='flex:1 1 200px' maxlength='40' placeholder='Tên trình duyệt (tự điền khi chọn hồ sơ)'>" +
        "<button type='button' class='tbd-nut chinh nho' data-knh='ok' disabled>Nhập đăng nhập</button><button type='button' class='tbd-nut nho' data-knh='huy'>Hủy</button></div>";
    }
    e.innerHTML = h + "</div>";
    var f = D.getElementById("knhTen"); if (f && u.mode === "them") f.focus();
  }
  function lamMoiHs(chonId) {
    return api("/trinh-duyet/trang-thai?nhe=1").then(function (d) { ST = d || ST; if (chonId) knQ.hs = chonId; veQuyenKn(); });
  }
  function xuLyKnh(t) {
    var a = t.getAttribute("data-knh");
    if (a === "them") { knUI = { mode: "them" }; veQlKn(); return true; }
    if (a === "nhap") { knUI = { mode: "nhap", ds: null, chon: null }; veQlKn(); api("/trinh-duyet/nguon-chrome").then(function (r) { if (knUI && knUI.mode === "nhap") { knUI.ds = (r && r.nguon) || []; veQlKn(); } }); return true; }
    if (a === "huy") { knUI = null; veQlKn(); return true; }
    if (a === "tao") {
      var ten = String((D.getElementById("knhTen") || {}).value || "").trim();
      if (!ten) { knUI.loi = "Anh đặt tên cho trình duyệt đã nhé."; veQlKn(); return true; }
      t.disabled = true;
      api("/trinh-duyet/ho-so", { hanh: "tao", ten: ten }).then(function (r) {
        if (r && r.id) { knUI = null; veQlKn(); lamMoiHs(r.id); }
        else { knUI = { mode: "them", loi: (r && (r.loi || r.error)) || "Không tạo được trình duyệt." }; veQlKn(); }
      });
      return true;
    }
    if (a === "chon") {
      if (!knUI) return true;
      knUI.chon = { nguon: t.getAttribute("data-nguon"), thu_muc: t.getAttribute("data-tm"), ten: t.getAttribute("data-ten") };
      Array.prototype.forEach.call(D.querySelectorAll("#knhDs .tbd-hsc"), function (b) { b.classList.toggle("on", b === t); });
      var f = D.getElementById("knhTen"); if (f) f.value = knUI.chon.ten;
      var ok = D.querySelector("[data-knh='ok']"); if (ok) ok.disabled = false;
      return true;
    }
    if (a === "ok") {
      if (!knUI || !knUI.chon || knUI.dang) return true;
      var tn = String((D.getElementById("knhTen") || {}).value || "").trim() || knUI.chon.ten;
      knUI.dang = true; t.disabled = true; t.textContent = "Đang chép...";
      api("/trinh-duyet/nhap-chrome", { nguon: knUI.chon.nguon, thu_muc: knUI.chon.thu_muc, ten: tn }).then(function (r) {
        knUI = { mode: "nhap", kq: r || { ok: false, loi: "Không nhập được." } };
        veQlKn();
        if (r && r.id) { api("/trinh-duyet/ho-so", { hanh: "chon", id: r.id }); lamMoiHs(r.id); }
      });
      return true;
    }
    return true;
  }
  function moKn() {
    css3();
    if (kn) return;
    knTen = tenTheKetNoi();
    Promise.all([api("/trinh-duyet/trang-thai?nhe=1"), api("/may-ai/trang-thai")]).then(function (r) {
      ST = r[0] || ST || {}; var sm = r[1] || {};
      knQ.tb = QTB.toan_quyen ? "toan_quyen" : "quan_trong"; knQ.may = QMAY.toan_quyen ? "toan_quyen" : "quan_trong";   // V3.26: mặc định Toàn quyền khi nhờ nối công cụ (anh vẫn hạ được ở hộp này)
      knQ.pTb = knQ.pMay = 120; knQ.hs = ST.hoso_dang_dung || ((ST.ho_so_ds || [])[0] || {}).id || "";
      kn = D.createElement("div"); kn.className = "tbd-lop"; kn.setAttribute("role", "dialog"); kn.setAttribute("aria-modal", "true"); kn.setAttribute("aria-label", "AI hỗ trợ kết nối");
      kn.innerHTML = "<div class='tbd-cua' style='width:min(720px,100%)'><div class='tbd-dau'><span class='tbd-dau-i'>" + ICON_KN + "</span><div class='tbd-dau-t'><b>AI hỗ trợ kết nối</b><span>Anh nói muốn nối gì, AI tự đọc hướng dẫn, mở web, lấy mã và dán vào TISA BOT</span></div>" +
        "<button type='button' class='tbd-nut' data-kn='x' aria-label='Đóng'>Đóng</button></div><div class='tbd-than'>" +
        "<div class='tbd-the'><h3>Anh muốn kết nối gì?</h3><textarea id='knNd' class='tbd-kn-nd' placeholder='Ví dụ: Kết nối Meta Ads để AI xem số liệu quảng cáo giúp anh.&#10;Hoặc: Lấy API key của Zalo OA rồi dán vào TISA BOT.'></textarea>" +
        "<div class='tbd-hang' style='margin-top:8px'><button type='button' class='tbd-nut tbd-mic' id='knMic' data-kn='mic'>" + ICON_MIC + "Nói thay vì gõ</button><span class='tbd-kn-tt' id='knTt'></span></div>" +
        "<div class='tbd-luoi' style='margin-top:10px'>" + knTen.map(function (t) { return "<button type='button' class='tbd-hs' data-kn-chip='" + esc(t) + "'>" + esc(t) + "</button>"; }).join("") + "</div></div>" +
        "<div class='tbd-the'><h3><span class='tbd-kn-so'>1</span> Chọn quyền cho AI</h3><div id='knQuyen' class='tbd-kn-qs'></div></div>" +
        "<div class='tbd-the'><h3><span class='tbd-kn-so'>2</span> Chọn trình duyệt cho AI</h3><p class='tbd-kn-tt' style='margin:0 0 8px'>AI chỉ dùng đúng trình duyệt này. Trình duyệt nào đã đăng nhập sẵn tài khoản nào thì AI làm trên tài khoản đó.</p>" +
        "<div id='knTrinhDuyet' class='tbd-kn-hsl' role='radiogroup'></div>" +
        "<div class='tbd-hang' style='margin-top:10px'><button type='button' class='tbd-nut nho' data-knh='them'>+ Thêm trình duyệt riêng</button><button type='button' class='tbd-nut nho' data-knh='nhap'>Chép đăng nhập từ Chrome của anh</button></div><div id='knQl'></div></div>" +
        "</div><div class='tbd-hang' style='padding:12px 16px;border-top:1px solid var(--mm-line,rgba(255,255,255,.1));justify-content:flex-end'><button type='button' class='tbd-nut' data-kn='x'>Hủy</button><button type='button' class='tbd-nut chinh' data-kn='ok'>Bắt đầu nhờ AI</button></div></div>";
      kn.addEventListener("mousedown", function (e) { if (e.target === kn) dongKn(); });
      D.body.appendChild(kn);
      veQuyenKn();
      var nd = D.getElementById("knNd"); if (nd) nd.focus();
    });
  }
  function dongKn() { knUI = null; nghe(false); if (kn) { kn.remove(); kn = null; } }
  function ttKn(t) { var e = D.getElementById("knTt"); if (e) e.textContent = t || ""; }

  function nghe(bat) {
    var SR = W.SpeechRecognition || W.webkitSpeechRecognition, nut = D.getElementById("knMic"), nd = D.getElementById("knNd");
    if (!bat) { if (knNghe) { try { knNghe.stop(); } catch (e) {} knNghe = null; } if (nut) { nut.classList.remove("nghe"); nut.lastChild.nodeType === 3 && (nut.lastChild.textContent = "Nói thay vì gõ"); } return; }
    if (!SR) { ttKn("Ở đây chưa có tính năng nghe giọng. Anh gõ chữ, hoặc bấm mic ở khung chat Hỏi nhanh rồi nói."); return; }
    var goc = nd ? String(nd.value || "").trim() : "", r = new SR();
    r.lang = "vi-VN"; r.interimResults = true; r.continuous = true;
    r.onresult = function (e) {
      var t = ""; for (var i = 0; i < e.results.length; i++) t += e.results[i][0].transcript;
      if (nd) nd.value = (goc ? goc + " " : "") + t.trim();
    };
    r.onerror = function (e) { ttKn(e.error === "not-allowed" || e.error === "service-not-allowed" ? "Chưa cho phép dùng micro. Anh bật quyền micro rồi bấm lại, hoặc gõ chữ." : "Chưa nghe được (" + e.error + "). Anh thử lại hoặc gõ chữ."); nghe(false); };
    r.onend = function () { if (knNghe === r) { nghe(false); ttKn(""); } };
    try { r.start(); knNghe = r; if (nut) nut.classList.add("nghe"); ttKn("Đang nghe, anh nói xong bấm lại để dừng..."); } catch (e) { ttKn("Không bật được micro."); }
  }

  function loiNhacKn(nd, hsTen) {
    var pt = function (m, p) { return m === "toan_quyen" ? " (" + p + " phút)" : ""; };
    return "Dùng skill dq-ho-tro-ket-noi: " + nd + "\n" +
      "Quyền: trình duyệt web = " + QTB[knQ.tb][0].toLowerCase() + pt(knQ.tb, knQ.pTb) + "; điều khiển máy tính = " + QMAY[knQ.may][0].toLowerCase() + pt(knQ.may, knQ.pMay) + ". Trình duyệt cho AI: " + hsTen + ".\n" +
      "Chỉ dùng đúng trình duyệt đã chọn, không chạy lệnh mở trình duyệt khác (như `... login`, playwright).\n" +
      (knQ.may === "tat" ? "Không cho dùng điều khiển máy tính: không gọi tisa_desktop_*, làm trong trình duyệt." : "Em làm luôn: điều khiển giao diện TISA BOT bằng lệnh tisa_browser_do op=ui_tisa (không cần chuột, không dừng vì cửa sổ khác), không mở TISA BOT trong trình duyệt, không bắt anh đăng nhập lại.");
  }
  function guiChat(text) {
    var N = W.Alpine && W.Alpine.store && W.Alpine.store("nav");
    if (N && N.go) N.go("chat");
    var n = 0;
    (function cho() {
      var i = D.getElementById("chatInput"), b = D.getElementById("sendBtn");
      if ((!i || !b) && n++ < 40) { setTimeout(cho, 250); return; }
      if (!i || !b) { try { navigator.clipboard.writeText(text); } catch (e) {} return; }
      if (String(i.value || "").trim()) { try { navigator.clipboard.writeText(text); } catch (e) {} return; }   // ô chat đang có chữ chưa gửi: không đè
      i.value = text; i.dispatchEvent(new Event("input", { bubbles: true }));
      setTimeout(function () { b.click(); }, 300);
    })();
  }
  /* ---------- (V3.02) Nhờ TISA BOT làm giúp: dùng chung cho mọi nút "Nhờ ... làm giúp" (Quảng cáo, Cách 2, Meta, Web, Giao dự án) ----------
   * Chủ yêu cầu 17/11/2026: không dán lệnh sang Claude nữa, TISA BOT tự thao tác bằng trình duyệt và máy tính của anh.
   * Bấm là tự cấp Toàn quyền 2 giờ cho trình duyệt và máy tính, riêng quyền XÓA TỆP luôn tắt. Nút Dừng AI ngay vẫn dùng được. */
  var CAM_XOA = "\n\n[Quyền đã cấp: Toàn quyền trình duyệt và điều khiển máy trong 2 giờ. TUYỆT ĐỐI KHÔNG xóa tệp hay thư mục nào. Không nhập hộ mật khẩu, mã OTP, số thẻ; gặp đăng nhập, CAPTCHA, thanh toán thì dừng và nhờ anh làm rồi làm tiếp. Anh đang xem cửa sổ trợ lý nổi (không thấy khung chat): sau mỗi bước báo MỘT câu ngắn bắt đầu bằng \"Em đang\"; khi cần anh làm gì thì nói rõ NÚT nào, Ở ĐÂU trên màn hình, rồi dùng wait_user. Viết ngắn, dễ nghe; anh có thể bấm nút Gọi trong cửa sổ trợ lý để nói chuyện qua lại với em.]";
  var nhoDang = false;
  function thongBaoNho(t, loi) {
    var e = D.getElementById("tbdNhoTb"); if (e) e.remove();
    e = D.createElement("div"); e.id = "tbdNhoTb"; e.setAttribute("role", "status");
    e.style.cssText = "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2147483000;max-width:min(560px,calc(100vw - 24px));padding:12px 16px;border-radius:14px;background:#172f72;color:#fff;font:600 13.5px/1.5 inherit;box-shadow:0 18px 50px -12px rgba(0,0,0,.5);border:1px solid " + (loi ? "#f59e0b" : "rgba(255,255,255,.25)");
    e.textContent = t; D.body.appendChild(e);
    setTimeout(function () { if (e.parentNode) e.remove(); }, loi ? 14000 : 8000);
  }
  /* Gửi lời nhờ vào cuộc trò chuyện MỚI mà không chuyển sang trang chat (anh vẫn ở trang Kết nối, AI thao tác trên đó) và mở cửa sổ trợ lý nổi. */
  /* V3.25 (chủ 19/11/2026): việc nối công cụ giao cho cộng sự riêng "Đạt Đấu Nối" (kênh agent:tisa-dau-noi: có kỹ năng, sổ tay, mô hình và mức nỗ lực
     riêng, chọn ở nút ⚙), không dùng đại một ô chat thường. Việc không phải nối công cụ vẫn đi ô chat thường như cũ. */
  function laViecKetNoi(text, tieuDe) { return /dq-ho-tro-ket-noi|dq-dau-noi-cong-cu|cloudflare|wrangler|\bmcp\b|đấu nối|đưa web lên|oauth|api key|access token/i.test(String(text || "")) || /kết nối|cài đặt|cloudflare|đưa web|đấu nối/i.test(String(tieuDe || "")); }
  /* Chủ 19/11/2026: giao việc nối công cụ là tự cấp Toàn quyền trình duyệt và điều khiển máy 2 giờ, để Đạt dùng mọi cách thao tác cho làm được.
     Riêng quyền XÓA TỆP luôn tắt (cho-xoa phút 0). Mật khẩu, OTP, CAPTCHA, thanh toán vẫn là việc của chủ. */
  function canToanQuyen(text, tieuDe) { if (/Quyền: trình duyệt web = /.test(String(text || ""))) return false; return /dq-ho-tro-ket-noi|dq-dau-noi-cong-cu/.test(String(text || "")) || /kết nối|cài đặt|cloudflare|đưa web|đấu nối/i.test(String(tieuDe || "")); }
  function capToanQuyen() {
    return Promise.all([
      api("/trinh-duyet/muc", { muc: "toan_quyen", phut: 120 }),
      api("/may-ai/trang-thai").then(function (sm) { return (sm && sm.ho_tro === false) ? 0 : Promise.all([api("/may-ai/muc", { muc: "toan_quyen", phut: 120 }), api("/may-ai/cho-xoa", { phut: 0 })]); })
    ]).catch(function () {});
  }
  /* V3.34 (chủ 19/11/2026): việc làm web (trang Quản lý web: dựng, sửa, đưa lên Cloudflare, gắn tên miền...) giao cho cộng sự "Quản Trị WEB".
     Nhận ra bằng cờ agent từ trang Quản lý web, hoặc lời nhờ nhắc kỹ năng dq-quan-tri-web. Đi trước nhánh Đạt (lời nhờ web có chữ Cloudflare). */
  function laViecWeb(text, agent) { return agent === "tisa-quan-tri-web" || /dq-quan-tri-web/.test(String(text || "")); }
  function guiNgam(text, tieuDe, agent) {
    var web = laViecWeb(text, agent) && W.TISAQuanTriWeb && typeof W.TISAQuanTriWeb.moPhien === "function";
    var dauNoi = !web && laViecKetNoi(text, tieuDe) && W.TISADauNoi && typeof W.TISADauNoi.moPhien === "function";
    (canToanQuyen(text, tieuDe) ? capToanQuyen() : Promise.resolve()).then(function () { return web ? W.TISAQuanTriWeb.moPhien() : dauNoi ? W.TISADauNoi.moPhien() : false; }).catch(function () { return false; }).then(function (ok) {
      if (!ok) { try { if (typeof W.newChat === "function") W.newChat(); } catch (e) {} }
      setTimeout(function () {
        if (W.TISATroLyNoi) { W.TISATroLyNoi.bat(tieuDe || "Hỗ trợ cài đặt"); if (W.TISATroLyNoi.gui(text)) return; }
        guiChat(text);
      }, 300);
    });
  }
  function nhoAI(text, tieuDe, agent) {
    text = String(text || "").trim();
    if (!text || nhoDang) return Promise.resolve(false);
    nhoDang = true; css3();
    return chonChromeNeuCan().then(function (ch) {
      if (ch === false) { nhoDang = false; thongBaoNho("Chưa bắt đầu: anh chưa chọn Chrome. Bấm lại nút khi sẵn sàng.", false); return Promise.reject("huy-chon-chrome"); }
      if (ch) text += "\n\n[Chrome anh đã chọn: " + tenHoSo(ch) + ". Chỉ mở và làm việc trong ĐÚNG hồ sơ Chrome này (op=mo_chrome không cần ho_so). Không mở Chrome mới, không mở hồ sơ khác; trang chưa đăng nhập thì nhờ anh đăng nhập ngay trong hồ sơ này.]";
      return Promise.all([api("/trinh-duyet/trang-thai?nhe=1"), api("/may-ai/trang-thai")]);
    }).then(function (r) {
      var sm = r[1] || {}, q = sm.quyen || {}, coMay = sm.ho_tro !== false, canh = "";
      if (coMay && sm.he === "macOS" && (!q.tro_nang || q.ghi_man_hinh === false)) {
        api("/may-ai/cai-dat-quyen", {});
        canh = " macOS cần anh bật quyền Trợ năng và Ghi màn hình cho TISA BOT (em đã mở sẵn Cài đặt, anh chỉ cần bật công tắc). Trong lúc đó em làm bằng trình duyệt trước.";
      }
      return Promise.all([
        api("/trinh-duyet/muc", { muc: "toan_quyen", phut: 120 }),
        coMay ? api("/may-ai/muc", { muc: "toan_quyen", phut: 120 }) : 0,
        coMay ? api("/may-ai/cho-xoa", { phut: 0 }) : 0
      ]).then(function () {
        guiNgam(text + CAM_XOA, tieuDe || "Hỗ trợ cài đặt", agent); lam(true);
        // (V3.43, chủ 22/11) Đấu nối tự động: mở khung Trình duyệt cạnh màn hình để anh thấy bot đang làm gì, ở trang Chrome nào.
        if (W.TISAKhungTD && innerWidth > 820) setTimeout(function () { try { sessionStorage.removeItem("tkd-tat:" + ((W.TISASessions && W.TISASessions.current && W.TISASessions.current()) || "")); } catch (x) {} W.TISAKhungTD.mo({ cho: true }); }, 2500);
        thongBaoNho("TISA BOT đang làm giúp anh. Cửa sổ trợ lý ở góc phải màn hình báo tiến độ, anh nói hoặc gõ với em được ở đó. Đã bật Toàn quyền 2 giờ (không xóa tệp)." + canh, !!canh);
        nhoDang = false; return true;
      });
    }).catch(function (e) { nhoDang = false; if (e !== "huy-chon-chrome") thongBaoNho("Chưa bắt đầu được. Anh thử bấm lại.", true); return false; });
  }
  /* ---------- (V3.20) Chọn đúng Chrome (hồ sơ) có tài khoản cần kết nối ----------
   * Chủ báo 18/11/2026: nhờ TISA BOT kết nối giúp thì nó hay mở Chrome mới chưa đăng nhập, hoặc mở Chrome của anh nhưng sai hồ sơ.
   * Anh chọn MỘT hồ sơ Chrome ở đây (đọc từ Local State của Chrome: tên, email), TISA BOT chỉ mở và làm việc trong đúng hồ sơ đó. */
  function escH(t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function layHoSoChrome() { return api("/may-ai/chrome-ho-so").then(function (r) { return { chon: (r && r.da_chon) || null, ds: (r && r.ho_so) || [] }; }); }
  function tenHoSo(h) { return h ? (h.ten || h.thu_muc) + (h.email ? " (" + h.email + ")" : "") : ""; }
  /* Trả Promise: hồ sơ đã chọn | null (anh chọn "dùng trình duyệt riêng của TISA BOT") | false (anh đóng hộp, không làm gì). batBuoc: hiện lời nhắc "cần chọn trước". */
  function hopChonChrome(batBuoc) {
    return layHoSoChrome().then(function (d) {
      return new Promise(function (xong) {
        var cu = D.getElementById("tbdChromeHop"); if (cu) cu.remove();
        var o = D.createElement("div"); o.id = "tbdChromeHop"; o.setAttribute("role", "dialog"); o.setAttribute("aria-modal", "true");
        o.style.cssText = "position:fixed;inset:0;z-index:2147483400;background:rgba(10,16,38,.55);display:flex;align-items:center;justify-content:center;padding:16px";
        var h = d.ds.map(function (x) {
          var on = d.chon && d.chon.thu_muc === x.thu_muc, ch = String(x.ten || x.thu_muc || "?").trim().charAt(0).toUpperCase();
          return "<button type='button' data-hs='" + escH(x.thu_muc) + "' style='display:flex;gap:12px;align-items:center;width:100%;text-align:left;padding:11px 13px;margin:0 0 8px;border-radius:14px;border:2px solid " + (on ? "#ff6b35" : "rgba(23,47,114,.18)") + ";background:" + (on ? "rgba(255,107,53,.10)" : "#fff") + ";color:#172033;cursor:pointer;font:inherit'>" +
            "<span style='flex:none;width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#ff6b35,#172f72);color:#fff;display:grid;place-items:center;font-weight:800'>" + escH(ch) + "</span>" +
            "<span style='flex:1;min-width:0'><b style='display:block;font-size:15px'>" + escH(x.ten || x.thu_muc) + (on ? " <span style='color:#ff6b35;font-size:12px'>đang dùng</span>" : "") + "</b><small style='color:var(--mm-muted,#5b6478)'>" + escH(x.email || "chưa đăng nhập tài khoản Google") + " · " + escH(x.thu_muc) + "</small></span></button>";
        }).join("");
        o.innerHTML = "<div style='width:min(520px,100%);max-height:calc(100vh - 40px);overflow:auto;background:#fff;color:#172033;border-radius:20px;padding:20px 20px 16px;box-shadow:0 20px 60px rgba(0,0,0,.4);font:14px/1.5 system-ui,-apple-system,Segoe UI,sans-serif'>" +
          "<h3 style='margin:0 0 4px;font-size:18px'>Chọn Chrome có tài khoản cần kết nối</h3>" +
          "<p style='margin:0 0 12px;color:var(--mm-muted,#5b6478)'>" + (batBuoc ? "Anh chọn trước để TISA BOT mở đúng Chrome đã đăng nhập, không mở Chrome mới chưa có tài khoản. " : "") +
          "TISA BOT chỉ dùng đúng hồ sơ này, không nhảy sang hồ sơ khác.</p>" +
          (h || "<div style='padding:14px;border-radius:12px;background:#fff6f1;border:1px solid #ffd6c2'>Không đọc được danh sách hồ sơ Chrome (máy chưa cài Google Chrome, hoặc Chrome chưa được mở lần nào). TISA BOT sẽ dùng trình duyệt riêng của nó, anh đăng nhập một lần trong đó.</div>") +
          "<div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:12px'>" +
          "<button type='button' data-hs-rieng style='flex:1;min-width:150px;padding:10px 12px;border-radius:12px;border:1px solid rgba(23,47,114,.25);background:#f4f6fc;font:600 13px inherit;cursor:pointer'>Dùng trình duyệt riêng của TISA BOT</button>" +
          "<button type='button' data-hs-dong style='padding:10px 14px;border-radius:12px;border:0;background:#172f72;color:#fff;font:700 13px inherit;cursor:pointer'>Đóng</button></div></div>";
        function dong(v) { o.remove(); xong(v); }
        o.addEventListener("click", function (e) {
          var b = e.target.closest ? e.target.closest("button") : null;
          if (e.target === o) return dong(false);
          if (!b) return;
          if (b.hasAttribute("data-hs-dong")) return dong(false);
          if (b.hasAttribute("data-hs-rieng")) { api("/may-ai/chrome-ho-so", { ho_so: "" }).then(function () { try { W.dispatchEvent(new Event("tisa:chrome-chon")); } catch (x) {} dong(null); }); return; }
          var thuMuc = b.getAttribute("data-hs");
          if (thuMuc) api("/may-ai/chrome-ho-so", { ho_so: thuMuc }).then(function (r) {
            if (r && r.ok) {
              try { W.dispatchEvent(new Event("tisa:chrome-chon")); } catch (x) {}
              var ad = r.ap_dung || {};      // máy chủ đã MỞ đúng hồ sơ Chrome và chuyển TISA BOT sang Chrome của anh (không chỉ ghi nhớ)
              thongBaoNho(ad.tin || ("Đã chọn Chrome " + tenHoSo(r.ho_so) + "."), ad.ok === false);
              dong(r.ho_so);
            }
            else thongBaoNho((r && (r.loi || r.error)) || "Chưa chọn được hồ sơ này.", true);
          });
        });
        D.body.appendChild(o);
      });
    });
  }
  W.TISAChonChrome = hopChonChrome;
  W.TISALayChrome = layHoSoChrome;
  /* Đang có hồ sơ đã chọn thì dùng luôn; chưa chọn mà máy có hồ sơ Chrome thì bắt chọn trước khi nhờ AI làm. */
  function chonChromeNeuCan() {
    return layHoSoChrome().then(function (d) {
      if (d.chon || !d.ds.length) return d.chon;
      return hopChonChrome(true);
    }).catch(function () { return null; });
  }
  W.TISANhoAI = nhoAI;
  W.addEventListener("message", function (e) {
    var d = e.data;
    if (e.origin !== location.origin || !d || typeof d !== "object") return;
    if (d.tisa === "nho-tisabot" && typeof d.text === "string") nhoAI(d.text.slice(0, 8000), typeof d.tieu_de === "string" ? d.tieu_de.slice(0, 60) : "", d.agent === "tisa-quan-tri-web" ? d.agent : "");
  });
  /* ---------- (V3.02) Nút "Kết nối tự động" cạnh từng thẻ ở trang Kết nối ----------
   * Bấm là TISA BOT tự làm TỪ ĐẦU ĐẾN CUỐI (mở web, tạo app/khóa, dán kín vào ô, bấm Kết nối) với Toàn quyền trình duyệt và máy tính
   * (không xóa tệp); chỗ nào không làm thay được (đăng nhập, mã xác thực, QR, đồng ý quyền) thì báo anh đúng một việc cần bấm.
   * Hướng dẫn chi tiết từng công cụ nằm ở tisa-ket-noi-huong-dan.json (tools/sinh_huong_dan_ket_noi.py sinh ra). */
  var HDKN = null;
  function taiHdKn() {
    if (HDKN) return Promise.resolve(HDKN);
    return fetch("/static/tisa-ket-noi-huong-dan.json?v=1", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (j) { HDKN = j || {}; return HDKN; })
      .catch(function () { return { chung: [], dich_vu: [], phu: {} }; });
  }
  function nfc(t) { return String(t || "").normalize("NFC").toLowerCase(); }
  function timHdKn(j, ten) {
    var t = nfc(ten), best = null, dai = 0;
    (j.dich_vu || []).forEach(function (d) {
      (d.khop || []).forEach(function (k) { k = nfc(k); if (k && t.indexOf(k) >= 0 && k.length > dai) { best = d; dai = k.length; } });
    });
    return best;
  }
  function loiKetNoiTuDong(j, ten) {
    var d = timHdKn(j, ten), L = [];
    L.push("Dùng skill dq-ho-tro-ket-noi: KẾT NỐI TỰ ĐỘNG \"" + ten + "\" vào TISA BOT, làm TỪ ĐẦU ĐẾN CUỐI, không hỏi lại những gì tự làm được.");
    L.push("Anh đã cấp toàn quyền điều khiển trình duyệt và máy tính (không xóa tệp). Em tự mở trang, bấm, gõ, lấy mã và dán kín vào TISA BOT. Việc nào em không làm thay được thì dừng và nói anh ĐÚNG MỘT việc cần bấm gì, ở đâu; anh xong thì em làm tiếp ngay.");
    L.push("");
    if (d) {
      L.push("MỤC TIÊU: " + d.muc_tieu + ".");
      if ((d.can_lay || []).length) L.push("CẦN LẤY VÀ ĐIỀN: " + d.can_lay.join("; ") + ".");
      if ((d.trang || []).length) L.push("TRANG WEB: " + d.trang.join(" ; "));
      L.push("CÁC BƯỚC (làm lần lượt; giao diện các nền tảng đổi nhanh, thấy khác mô tả thì tìm mục tương đương hoặc tra tài liệu chính thức rồi làm tiếp):");
      d.buoc.forEach(function (b, i) { L.push((i + 1) + ". " + b); });
      if ((d.luu_y || []).length) { L.push("LƯU Ý:"); d.luu_y.forEach(function (x) { L.push("- " + x); }); }
    } else {
      L.push("Chưa có hướng dẫn riêng cho dịch vụ này. Làm theo quy trình của skill: ui_tisa lenh=mo_the ten=\"" + ten + "\" để xem ô cần điền và các nút; tra tài liệu chính thức bằng tisa_web_search và tisa_web_fetch (ưu tiên MCP chính chủ, rồi API chính thức, quyền tối thiểu); mở web của nền tảng bằng trình duyệt đã chọn, lấy mã, dán kín vào ô, bấm Kết nối và Kiểm tra.");
      var ph = (j.phu || {}); Object.keys(ph).forEach(function (k) { if (nfc(ten).indexOf(k) >= 0) L.push(ph[k]); });
    }
    L.push("");
    L.push("QUY TẮC CHUNG:");
    (j.chung || []).forEach(function (x) { L.push("- " + x); });
    return L.join("\n");
  }
  W.TISAKetNoiTuDong = { loi: function (ten) { return taiHdKn().then(function (j) { return loiKetNoiTuDong(j, ten); }); } };
  function tenTheKn(e) { var n = e && e.firstChild ? String(e.firstChild.textContent || "").trim() : String((e && e.textContent) || "").trim(); return n; }
  function chenAutoKn() {
    if (!trangKetNoi()) return;
    css3();
    Array.prototype.forEach.call(D.querySelectorAll(".conn-card:not([data-tbd-auto])"), function (c) {
      var acc = c.querySelector(".conn-accounts"), nm = c.querySelector(".prov-name"), ten = tenTheKn(nm);
      if (!acc || !ten) return;
      c.setAttribute("data-tbd-auto", "1");
      var b = D.createElement("button"); b.type = "button"; b.className = "conn-chip tbd-auto"; b.setAttribute("data-tbd-auto-ten", ten);
      b.title = "TISA BOT tự kết nối " + ten + " từ đầu đến cuối (Toàn quyền, không xóa tệp)"; b.textContent = "⚡ Kết nối tự động";
      acc.appendChild(b);
    });
    Array.prototype.forEach.call(D.querySelectorAll(".cat-card:not([data-tbd-auto])"), function (c) {
      var nm = c.querySelector(".cat-name"), ten = tenTheKn(nm), bt = c.querySelector(".gcard-btn");
      c.setAttribute("data-tbd-auto", "1");
      if (!ten || /^tự thêm/i.test(ten) || !bt) return;
      var b = D.createElement("button"); b.type = "button"; b.className = "gcard-btn tbd-auto"; b.setAttribute("data-tbd-auto-ten", ten);
      b.title = "TISA BOT tự kết nối " + ten + " từ đầu đến cuối (Toàn quyền, không xóa tệp)"; b.textContent = "⚡ Kết nối tự động";
      bt.insertAdjacentElement("afterend", b);
    });
  }
  D.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-tbd-auto-ten]");
    if (!b) return;
    e.preventDefault(); e.stopPropagation();
    var ten = b.getAttribute("data-tbd-auto-ten");
    b.disabled = true;
    taiHdKn().then(function (j) { return nhoAI(loiKetNoiTuDong(j, ten), "Kết nối " + ten); }).then(function () { b.disabled = false; });
  }, true);

  function batDauKn() {
    var nd = D.getElementById("knNd"), v = nd ? String(nd.value || "").trim() : "";
    if (!v) { ttKn("Anh gõ hoặc nói muốn kết nối gì đã nhé."); if (nd) nd.focus(); return; }
    var x = ((ST && ST.ho_so_ds) || []).filter(function (h) { return h.id === knQ.hs; })[0], ten = x ? x.ten : "trình duyệt đã chọn";
    var nut = kn && kn.querySelector("[data-kn='ok']"); if (nut) { nut.disabled = true; nut.textContent = "Đang kiểm tra..."; }
    var truoc = knQ.may === "tat" ? Promise.resolve(null) : api("/may-ai/trang-thai");
    truoc.then(function (m) {
      var q = (m && m.quyen) || {};
      if (m && m.he === "macOS" && (!q.tro_nang || q.ghi_man_hinh === false)) {          // macOS chưa cấp quyền: mở sẵn Cài đặt, nhờ anh bật công tắc rồi bấm lại
        api("/may-ai/cai-dat-quyen", {});
        if (nut) { nut.disabled = false; nut.textContent = "Bắt đầu nhờ AI"; }
        ttKn("macOS cần anh bật quyền Trợ năng và Ghi màn hình cho TISA BOT (em đã mở sẵn Cài đặt, anh chỉ cần bật công tắc). Bật xong bấm Bắt đầu lại.");
        return null;
      }
      if (nut) nut.textContent = "Đang bắt đầu...";
      return Promise.all([
      knQ.hs ? api("/trinh-duyet/ho-so", { hanh: "chon", id: knQ.hs }) : 0,
      api("/trinh-duyet/muc", knQ.tb === "toan_quyen" ? { muc: "toan_quyen", phut: knQ.pTb } : { muc: knQ.tb }),
      api("/may-ai/muc", knQ.may === "toan_quyen" ? { muc: "toan_quyen", phut: knQ.pMay } : { muc: knQ.may })
    ]).then(function () {
        var t = loiNhacKn(v, ten); dongKn(); guiNgam(t, "Kết nối ứng dụng"); lam(true);
      });
    });
  }

  /* Hộp chọn web: AI gọi tisa_browser_do op=hoi_mo, TISA BOT hiện hộp này, anh chọn web và trình duyệt. */
  var chonEl = null, chonKey = "";
  function veChon() {
    var ds = (ST && ST.cho_chon) || [];
    if (!ds.length) { if (chonEl) { chonEl.remove(); chonEl = null; chonKey = ""; } return; }
    var x = ds[0];
    if (chonEl && chonKey === x.id) return;
    css3();
    if (chonEl) chonEl.remove();
    chonKey = x.id;
    var hs = (ST && ST.ho_so_ds) || [];
    var trg = x.trang || [], pre = 0, ti;
    for (ti = 0; ti < trg.length; ti++) if (trg[ti].tab_san) { pre = ti; break; }
    if (!trg[pre] || !trg[pre].tab_san) for (ti = 0; ti < trg.length; ti++) if (trg[ti].da_dang_nhap) { pre = ti; break; }
    var hsChon = ST.hoso_dang_dung, hsCh = hs.filter(function (h) { return h.id === ST.hoso_dang_dung; })[0];
    if (!hsCh || !hsCh.dang_chay) { var hsRun = hs.filter(function (h) { return h.dang_chay; })[0]; if (hsRun) hsChon = hsRun.id; }   // ưu tiên trình duyệt TISA đang chạy: vào thẳng tab đã đăng nhập
    chonEl = D.createElement("div"); chonEl.className = "tbd-lop tbd-kn-chon"; chonEl.setAttribute("role", "dialog"); chonEl.setAttribute("aria-modal", "true"); chonEl.setAttribute("aria-label", "Chọn web để AI mở");
    chonEl.innerHTML = "<div class='tbd-cua' style='width:min(560px,100%)'><div class='tbd-dau'><span class='tbd-dau-i'>" + ICON + "</span><div class='tbd-dau-t'><b>AI muốn mở một trang web</b><span>" + esc(x.ly_do || "Anh chọn trang cần mở") + "</span></div></div>" +
      "<div class='tbd-than'><div class='tbd-muc'>" + trg.map(function (t, i) {
        var nhan = (t.tab_san ? " <small style='color:#16a34a;font-weight:700'>● Đã mở sẵn một tab</small>" : "") + (t.da_dang_nhap ? " <small style='color:#16a34a;font-weight:700'>✓ Đã đăng nhập" + (t.ten_hs ? " trong " + esc(t.ten_hs) : "") + "</small>" : "");
        return "<label class='tbd-mc tbd-rd" + (i === pre ? " on" : "") + "'><span class='tbd-rdh'><input type='radio' name='tbdChonUrl' value='" + esc(t.url) + "'" + (i === pre ? " checked" : "") + "><b>" + esc(t.ten) + "</b>" + nhan + "</span><span>" + esc(t.host) + (t.mo_ta ? " · " + esc(t.mo_ta) : "") + "</span></label>";
      }).join("") +
      "<label class='tbd-mc tbd-rd'><span class='tbd-rdh'><input type='radio' name='tbdChonUrl' value='__khac'><b>Trang khác</b></span><span>Dán địa chỉ web anh muốn mở</span><input type='text' id='tbdChonKhac' placeholder='https://...' autocomplete='off'></label></div>" +
      "<div class='tbd-the'><h3>Mở bằng trình duyệt nào?</h3><p class='tbd-kn-tt' style='margin:0 0 8px'>Chọn trình duyệt TISA BOT đang mở: AI vào thẳng các tab đã đăng nhập sẵn, khỏi mở Chrome mới và đăng nhập lại.</p><select id='tbdChonHs' class='tbd-kn-sel'>" + hs.map(function (h) { return "<option value='" + esc(h.id) + "'" + (h.id === hsChon ? " selected" : "") + ">" + esc(h.ten) + (h.dang_chay ? " (đang mở, dùng tab đã đăng nhập)" : "") + "</option>"; }).join("") + "</select></div></div>" +
      "<div class='tbd-hang' style='padding:12px 16px;border-top:1px solid var(--mm-line,rgba(255,255,255,.1));justify-content:flex-end'><button type='button' class='tbd-nut' data-chon-no='" + esc(x.id) + "'>Không mở</button><button type='button' class='tbd-nut chinh' data-chon-ok='" + esc(x.id) + "'>Mở trang này</button></div></div>";
    D.body.appendChild(chonEl);
  }
  function xuLyKn(e) {
    var t = e.target.closest && e.target.closest("[data-kn],[data-kn-chip],[data-kn-q],[data-kn-hs],[data-knh],[data-chon-ok],[data-chon-no],.tbd-rd input");
    if (!t) return false;
    if (t.hasAttribute("data-knh")) return xuLyKnh(t);
    if (t.hasAttribute("data-kn-q")) { var w = t.getAttribute("data-kn-q"), v2 = t.getAttribute("data-v"); if (w === "tb") knQ.tb = v2; else knQ.may = v2; veQuyenKn(); return true; }
    if (t.hasAttribute("data-kn-hs")) { knQ.hs = t.getAttribute("data-kn-hs"); veQuyenKn(); return true; }
    if (t.matches && t.matches(".tbd-rd input")) { Array.prototype.forEach.call(D.querySelectorAll(".tbd-rd"), function (l) { l.classList.toggle("on", !!l.querySelector("input:checked")); }); return false; }
    if (t.hasAttribute("data-kn-chip")) { var nd = D.getElementById("knNd"); if (nd) { var c = t.getAttribute("data-kn-chip"); nd.value = "Kết nối " + c + " giúp anh."; nd.focus(); } return true; }
    if (t.hasAttribute("data-chon-ok") || t.hasAttribute("data-chon-no")) {
      var id = t.getAttribute("data-chon-ok") || t.getAttribute("data-chon-no"), huy = t.hasAttribute("data-chon-no"), url = "";
      if (!huy) {
        var r = D.querySelector("input[name='tbdChonUrl']:checked"); url = r ? r.value : "";
        if (url === "__khac") { var k = D.getElementById("tbdChonKhac"); url = k ? String(k.value || "").trim() : ""; if (url && !/^https?:\/\//i.test(url)) url = "https://" + url; }
        if (!url) { var k2 = D.getElementById("tbdChonKhac"); if (k2) k2.focus(); return true; }
      }
      var sel = D.getElementById("tbdChonHs"); t.disabled = true;
      api("/trinh-duyet/chon", { id: id, url: url, hoso: sel ? sel.value : "", huy: huy }).then(function (r2) {
        if (r2 && r2.ok === false && !huy) { t.disabled = false; var k3 = D.getElementById("tbdChonKhac"); if (k3) { k3.value = url; k3.placeholder = r2.loi || ""; } return; }
        if (chonEl) { chonEl.remove(); chonEl = null; } chonKey = ""; lam(true);
      });
      return true;
    }
    var a = t.getAttribute("data-kn");
    if (a === "x") dongKn();
    else if (a === "ok") batDauKn();
    else if (a === "mic") nghe(!knNghe);
    else if (a === "tb") { dongKn(); mo("tb"); }
    else if (a === "may") { dongKn(); mo("may"); }
    return true;
  }
  D.addEventListener("click", xuLyKn);
  D.addEventListener("change", function (e) {
    var el = e.target; if (!el || !el.getAttribute || !el.hasAttribute("data-kn-p")) return;
    if (el.getAttribute("data-kn-p") === "tb") knQ.pTb = Number(el.value) || 120; else knQ.pMay = Number(el.value) || 120;
  });
  D.addEventListener("input", function (e) {
    if (e.target && e.target.id === "knhLoc") {
      var q = e.target.value.toLowerCase().trim();
      Array.prototype.forEach.call(D.querySelectorAll("#knhDs .tbd-hsc"), function (b) { b.style.display = (!q || (b.getAttribute("data-loc") || "").indexOf(q) >= 0) ? "" : "none"; });
    }
    if (e.target && e.target.id === "tbdChonKhac") { var r = D.querySelector("input[name='tbdChonUrl'][value='__khac']"); if (r) { r.checked = true; Array.prototype.forEach.call(D.querySelectorAll(".tbd-rd"), function (l) { l.classList.toggle("on", !!l.querySelector("input:checked")); }); } }
  });
  D.addEventListener("keydown", function (e) {
    if (kn && e.key === "Escape") { e.stopPropagation(); if (knUI) { knUI = null; veQlKn(); } else dongKn(); return; }
    if (kn && e.key === "Enter" && e.target && e.target.id === "knhTen") { e.preventDefault(); var b = kn.querySelector("[data-knh='tao'],[data-knh='ok']"); if (b && !b.disabled) b.click(); }
  }, true);


  /* (V2.99) AI điều khiển thẳng giao diện TISA BOT bằng lệnh (mở thẻ kết nối, chọn ô, bấm nút), không cần chuột nên không bị cửa sổ khác đè
   * hay vướng anh đang gõ. Kết quả báo lại CHỈ là chữ nhãn; không bao giờ gồm giá trị trong ô nhập. */
  function bo(s) { return String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/gi, "d").toLowerCase().replace(/\s+/g, " ").trim(); }
  function hien(e) { if (!e || !e.getBoundingClientRect) return false; var r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.visibility !== "hidden" && c.display !== "none"; }
  function ngu(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function choDen(fn, ms) { var t0 = Date.now(); return new Promise(function (res) { (function v() { var x = null; try { x = fn(); } catch (e) {} if (x || Date.now() - t0 > ms) res(x || null); else setTimeout(v, 150); })(); }); }
  // hộp thoại thật = lớp phủ che gần hết màn hình (không lẫn thanh bên, thanh trên)
  function hopTren() {
    var ds = [].slice.call(D.querySelectorAll("dialog[open],[role=dialog],[aria-modal=true],body *")).filter(function (e) {
      var c = getComputedStyle(e), r = e.getBoundingClientRect(), nhan = String(e.className || "") + " " + String(e.id || "");
      if (!hien(e) || /tbd-|notification|sound-toggle|theme-toggle|hud-/.test(nhan)) return false;
      var laHop = e.tagName === "DIALOG" || e.getAttribute("role") === "dialog" || e.getAttribute("aria-modal") === "true" || /modal|overlay|dialog|popup|dlg/i.test(nhan);
      var phu = c.position === "fixed" && r.width >= W.innerWidth * 0.8 && r.height >= W.innerHeight * 0.8;
      return laHop && (phu || c.position === "fixed" || e.tagName === "DIALOG") && e.querySelector("input:not([type=hidden]),textarea,select,button");
    });
    ds.sort(function (a, b) { return (+getComputedStyle(b).zIndex || 0) - (+getComputedStyle(a).zIndex || 0); });
    return ds[0] || null;
  }
  function nhanOUi(i) { return String((i.labels && i.labels[0] ? i.labels[0].textContent : "") || i.getAttribute("aria-label") || (i.previousElementSibling ? i.previousElementSibling.textContent : "") || i.placeholder || "").replace(/\s+/g, " ").trim().slice(0, 80); }
  function dsO(goc) { return [].slice.call((goc || D).querySelectorAll("input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=file]),textarea")).filter(function (i) { return hien(i) && !i.readOnly && !i.disabled && i.id !== "chatInput" && !(i.closest && i.closest(".tbd-lop")); }); }
  function xemUi() {
    var h = hopTren(), N = W.Alpine && W.Alpine.store && W.Alpine.store("nav"), out = [];
    if (h) {
      var tt = h.querySelector("h1,h2,h3,h4,.modal-title,.mp-title,[class*=title]"); out.push("Hộp đang mở: " + (tt ? tt.textContent.replace(/\s+/g, " ").trim().slice(0, 100) : "(không tên)"));
      var os = dsO(h).map(nhanOUi); if (os.length) out.push("Ô nhập: " + os.join(" | "));
      var ns = [].slice.call(h.querySelectorAll("button,[role=button]")).filter(hien).map(function (b) { return b.textContent.replace(/\s+/g, " ").trim(); }).filter(function (t) { return t && t.length < 40; });
      if (ns.length) out.push("Nút: " + ns.slice(0, 14).join(" | "));
    } else {
      out.push("Không có hộp nào đang mở. Trang hiện tại: " + (N && N.active || "?") + ".");
      var cs = [].slice.call(D.querySelectorAll("#catGrid .cat-card .cat-name")).filter(hien).map(function (n) { return (n.firstChild ? n.firstChild.textContent : n.textContent).trim(); }).filter(Boolean);
      if (cs.length) out.push("Thẻ kết nối đang hiện: " + cs.slice(0, 30).join(" | "));
    }
    var tb = [].slice.call(D.querySelectorAll("[role=alert],.mp-note,.toast,.toast-msg,.conn-err,.gcard-meta.err,[class*=error]")).filter(hien).map(function (e) { return e.textContent.replace(/\s+/g, " ").trim(); }).filter(function (t) { return t && t.length < 220; });
    if (tb.length) out.push("Thông báo: " + tb.slice(0, 4).join(" || "));
    return out.join("\n");
  }
  async function uiMoThe(a) {
    var N = W.Alpine && W.Alpine.store && W.Alpine.store("nav"); if (!N || !N.go) return { ok: false, kq: "Không điều khiển được trang trong TISA BOT." };
    N.go("mcp");
    await choDen(function () { return D.getElementById("mcpTabSanCo") || D.getElementById("catGrid"); }, 8000);
    var tab = [].slice.call(D.querySelectorAll("button.tab-kho")).filter(function (b) { return bo(b.textContent) === "ket noi san co"; })[0];
    var g = D.getElementById("catGrid"); if (tab && (!g || !hien(g))) { tab.click(); await ngu(400); }
    await choDen(function () { var g2 = D.getElementById("catGrid"); return g2 && hien(g2) && g2.querySelector(".cat-card"); }, 5000);
    var ten = bo(a.ten);
    var timThe = function () { return [].slice.call(D.querySelectorAll("#catGrid .cat-card")).filter(function (c) { var n = c.querySelector(".cat-name"); return n && bo(n.firstChild ? n.firstChild.textContent : n.textContent).indexOf(ten) >= 0; })[0]; };
    var the = timThe();
    if (!the) { var q = D.getElementById("catQ"); if (q) { q.value = a.ten; q.dispatchEvent(new Event("input", { bubbles: true })); await ngu(600); the = timThe(); } }
    if (!the) return { ok: false, kq: "Không thấy thẻ \"" + a.ten + "\". " + xemUi() };
    the.scrollIntoView({ block: "center" });
    var nut = [].slice.call(the.querySelectorAll(".gcard-btn")).filter(function (b) { return hien(b) && !/ghost/.test(b.className); })[0] || [].slice.call(the.querySelectorAll(".gcard-btn")).filter(hien)[0];
    if (!nut) return { ok: false, kq: "Thẻ \"" + a.ten + "\" không có nút kết nối (có thể đã kết nối). " + xemUi() };
    var chuNut = nut.textContent.replace(/\s+/g, " ").trim();
    nut.click(); await ngu(900);
    var h = await choDen(hopTren, 4000);
    if (a.dich_vu && !h) {                                  // thẻ nhiều dịch vụ (Google): chọn dịch vụ trong danh sách vừa mở ra
        var dv = [].slice.call(D.querySelectorAll("button,[role=button],label,li,div")).filter(function (e) { return hien(e) && e.children.length < 6 && bo(e.textContent).indexOf(bo(a.dich_vu)) >= 0 && bo(e.textContent).length < 120; })[0];
        if (dv) { dv.click(); await ngu(900); h = await choDen(hopTren, 4000); }
    }
    var rs = "Đã bấm \"" + chuNut + "\" ở thẻ " + a.ten + ". ";
    if (h && a.truong) { var o = dsO(h).filter(function (i) { return bo(nhanOUi(i)).indexOf(bo(a.truong)) >= 0; })[0]; if (o) { o.focus(); rs += "Đã chọn ô \"" + nhanOUi(o) + "\" (đang có con trỏ). "; } }
    else if (h) { var o2 = dsO(h).filter(function (i) { return !i.value; })[0]; if (o2) { o2.focus(); rs += "Ô đầu tiên còn trống \"" + nhanOUi(o2) + "\" đang có con trỏ. "; } }
    return { ok: true, kq: rs + "\n" + xemUi() };
  }
  async function uiChonO(a) {
    var h = hopTren(), o = dsO(h || D.body).filter(function (i) { return !a.truong || bo(nhanOUi(i)).indexOf(bo(a.truong)) >= 0; })[0];
    if (!o) return { ok: false, kq: "Không thấy ô \"" + (a.truong || "") + "\". " + xemUi() };
    o.scrollIntoView({ block: "center" }); o.focus();
    return { ok: true, kq: "Đã chọn ô \"" + nhanOUi(o) + "\": ô đang có con trỏ, sẵn sàng nhận dan_vao_tisa." };
  }
  var CAM_BAM = /xoa|go bo|go khoi|delete|dang xuat|logout|reset|huy ket noi|thu hoi/;
  async function uiBam(a) {
    var h = hopTren(), goc = h || D.body, n = bo(a.nhan);
    if (CAM_BAM.test(n)) return { ok: false, kq: "Lệnh này không được bấm nút xóa, gỡ, đăng xuất, đặt lại. Nhờ anh tự bấm." };
    var cs = [].slice.call(goc.querySelectorAll("button,[role=button],a.gcard-btn,.mp-btn")).filter(function (b) { return hien(b) && !b.disabled; });
    var b = cs.filter(function (x) { return bo(x.textContent) === n; })[0] || cs.filter(function (x) { return bo(x.textContent).indexOf(n) === 0; })[0] || cs.filter(function (x) { return bo(x.textContent).indexOf(n) >= 0 && bo(x.textContent).length < 40; })[0];
    if (!b) return { ok: false, kq: "Không thấy nút \"" + a.nhan + "\". " + xemUi() };
    if (CAM_BAM.test(bo(b.textContent))) return { ok: false, kq: "Nút này là nút xóa hoặc gỡ, không bấm." };
    var chu = b.textContent.replace(/\s+/g, " ").trim(); b.click(); await ngu(2500);
    return { ok: true, kq: "Đã bấm \"" + chu + "\".\n" + xemUi() };
  }
  async function chayUi(lenh, a) {
    a = a || {};
    try {
      if (lenh === "mo_the") return await uiMoThe(a);
      if (lenh === "chon_o") return await uiChonO(a);
      if (lenh === "bam") return await uiBam(a);
      if (lenh === "xem") return { ok: true, kq: xemUi() };
      return { ok: false, kq: "Lệnh không biết: " + lenh };
    } catch (e) { return { ok: false, kq: "Lỗi giao diện: " + (e && e.message || e) }; }
  }
  var uiBan = false;
  function uiThu() {
    if (uiBan) return;
    uiBan = true;
    api("/trinh-duyet/ui-cho").then(function (r) {
      if (!r || !r.id) { uiBan = false; return; }
      return (D.hidden ? ngu(900) : Promise.resolve()).then(function () {      // cửa sổ đang hiện được ưu tiên nhận lệnh
        return api("/trinh-duyet/ui-lay", { id: r.id });
      }).then(function (g) {
        if (!g || !g.co) { uiBan = false; return; }
        return chayUi(g.lenh, g.args).then(function (kq) {
          return api("/trinh-duyet/ui-xong", { id: r.id, ok: kq.ok, kq: kq.kq }).then(function () { uiBan = false; });
        });
      });
    }).catch(function () { uiBan = false; });
  }

  function khoi() { dangKy(0); setTimeout(nhip, 2500); }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", khoi); else khoi();
  /* Lối vào dễ thấy cho ô nhập mật khẩu mở khóa máy: một thẻ ở trang Cài đặt (Cài đặt nhanh) và hộp Cài đặt. Bấm là mở thẳng mục Mở khóa máy. */
  function moMoKhoa() {
    var dong = D.getElementById("settingsClose"), ov = D.getElementById("settingsOverlay");
    try { if (ov && ov.classList.contains("open") && dong) dong.click(); } catch (e) {}
    mo("may");
    var n = 0, t = setInterval(function () { var c = D.getElementById("tbdMkThe"); if (c || ++n > 20) { clearInterval(t); if (c) { try { c.scrollIntoView({ block: "center", behavior: "smooth" }); } catch (e) {} var ob = D.getElementById("tbdMkPw"); if (ob) ob.focus(); } } }, 250);
  }
  function chenLoiVaoMoKhoa() {
    [["quickSet", ".quick-set-body"], ["settingsOverlay", ".settings-body"]].forEach(function (x) {
      var goc = D.getElementById(x[0]), body = goc && goc.querySelector(x[1]);
      if (!body || body.querySelector(".tbd-mk-vao")) return;
      var d = D.createElement("div"); d.className = "tbd-mk-vao";
      d.style.cssText = "margin:0 0 12px;padding:12px 14px;border:1px solid rgba(255,107,53,.45);border-radius:12px;background:rgba(255,107,53,.08)";
      d.innerHTML = "<div style='font-weight:700;margin-bottom:4px'>Mở khóa máy tính cho AI</div><div style='font-size:12.5px;opacity:.8;margin-bottom:8px'>Nhập mật khẩu máy một lần để khi máy khóa, anh nhắn \"mở khóa máy\" là AI tự mở. Mật khẩu cất trong Keychain, AI không đọc được.</div>" +
        "<button type='button' class='s-btn tbd-mk-nut'>Nhập mật khẩu máy tính</button>";
      d.querySelector(".tbd-mk-nut").addEventListener("click", moMoKhoa);
      body.insertBefore(d, body.firstChild);
    });
  }
  var _tkMk = 0;
  function khoiMoKhoa() { chenLoiVaoMoKhoa(); if (++_tkMk < 40) setTimeout(khoiMoKhoa, 1500); }
  khoiMoKhoa();
  W.TISABrowser = { mo: mo, dong: dong, moMay: function () { mo("may"); }, ketNoi: moKn, chayUi: chayUi };
})();
