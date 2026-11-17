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
    ".tbd-lop{position:fixed;inset:0;z-index:2147482000;display:flex;align-items:center;justify-content:center;padding:clamp(8px,2.2vw,28px);background:rgba(6,10,26,.66);backdrop-filter:blur(6px);animation:tbdVao .14s ease-out}",
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
    ".tbd-xn{margin-top:10px;padding:12px;border-radius:12px;border:1px solid rgba(217,48,37,.6);background:rgba(217,48,37,.08)}.tbd-xn p{margin:0 0 10px;color:inherit}",
    ".tbd-xn select{height:38px;padding:0 10px;border-radius:10px;border:1px solid var(--mm-line2,rgba(255,255,255,.2));background:var(--mm-base,#131a3a);color:inherit;font:inherit}",
    ".tbd-duyet{border-color:rgba(245,158,11,.7);background:rgba(245,158,11,.1)}.tbd-duyet h3{color:#f59e0b}.tbd-hang{display:flex;flex-wrap:wrap;gap:8px;align-items:center}",
    /* thẻ nổi */
    ".tbd-noi{position:fixed;right:18px;top:70px;z-index:2147481900;width:min(380px,calc(100vw - 24px));display:grid;gap:10px}",
    ".tbd-ntc{padding:14px;border-radius:14px;background:var(--mm-base,#131a3a);color:var(--mm-ink,#dbe4ff);border:1px solid rgba(245,158,11,.75);box-shadow:0 18px 50px -12px rgba(0,0,0,.6);font:13.5px/1.5 inherit}",
    ".tbd-ntc b{display:block;margin-bottom:4px;font-size:14px}.tbd-ntc small{display:block;color:var(--mm-muted,#9aa6d6);margin-bottom:10px}",
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
  function theMuc(d) {
    var cur = d.muc || "quan_trong";
    var h = "<div class='tbd-the'><h3>Mức tự động của AI</h3><p>Chọn AI được tự làm tới đâu. Đổi lúc nào cũng được, có hiệu lực ngay.</p><div class='tbd-muc'>" +
      MUC.map(function (m) {
        return "<button type='button' class='tbd-mc" + (cur === m[0] ? " on" : "") + (m[0] === "toan_quyen" ? " tq" : "") + "' data-tbd-muc='" + m[0] + "' aria-pressed='" + (cur === m[0]) + "'><b>" + esc(m[1]) +
          (cur === m[0] && m[0] === "toan_quyen" ? esc(conLai(d.muc_den) || " (đến khi tắt)") : "") + "</b><span>" + esc(m[2]) + "</span></button>";
      }).join("") + "</div>";
    if (hoiToan) h += "<div class='tbd-xn'><p><b>Bật Toàn quyền?</b> AI sẽ tự đăng bài, gửi tin, xóa, nộp biểu mẫu trên các trang anh đã đăng nhập mà không hỏi. Anh chịu trách nhiệm với việc AI làm trong thời gian này. Nút Dừng AI ngay luôn dùng được.</p>" +
      "<div class='tbd-hang'><select id='tbdPhut'><option value='30'>Trong 30 phút</option><option value='120'>Trong 2 giờ</option><option value='0'>Đến khi anh tắt</option></select>" +
      "<button type='button' class='tbd-nut do' data-tbd-muc-ok='1'>Bật Toàn quyền</button><button type='button' class='tbd-nut' data-tbd-muc-ok='0'>Hủy</button></div></div>";
    return h + "</div>";
  }

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
    h += "<p>Chọn hồ sơ Chrome anh dùng lâu nay. TISA BOT <b>chép phần đăng nhập</b> (cookie) sang một trình duyệt riêng, nên anh <b>không phải đăng nhập lại</b> Google, Facebook, TikTok... AI dùng được mọi tài khoản đang đăng nhập trong hồ sơ đó. Không chép mật khẩu đã lưu, thẻ, lịch sử. Chrome gốc của anh không bị sửa.</p>";
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
    var ds = d.ho_so_ds || [], xem = xemId(), mac = d.hoso_dang_dung;
    var cur = ds.filter(function (x) { return x.id === xem; })[0] || ds[0] || { ten: "", id: "" };
    var h = "<div class='tbd-the'><h3>Trình duyệt của anh</h3><p>Mỗi trình duyệt có <b>đăng nhập riêng</b>. Cần 3 tài khoản Facebook cùng lúc thì tạo 3 trình duyệt, đặt tên cho dễ nhớ. AI dùng trình duyệt anh đặt làm <b>mặc định</b>; hoặc anh nói trong chat \"dùng Facebook 2\".</p><div class='tbd-luoi'>" +
      ds.map(function (x) {
        return "<button type='button' class='tbd-hs" + (x.id === xem ? " on" : "") + "' data-tbd-hs='" + esc(x.id) + "' aria-pressed='" + (x.id === xem) + "'><i class='tbd-cham " + (x.dang_chay ? "on" : "") + "'></i>" + esc(x.ten) + (x.id === mac ? " <small>mặc định</small>" : "") + "</button>";
      }).join("") + "<button type='button' class='tbd-hs them' data-tbd-hs-act='them'>+ Thêm trình duyệt</button></div>" +
      "<div class='tbd-hang' style='margin-top:10px'>" +
      (cur.id && cur.id !== mac ? "<button type='button' class='tbd-nut nho chinh' data-tbd-hs-act='mac_dinh'>Dùng \"" + esc(cur.ten) + "\" làm mặc định cho AI</button>" : "") +
      "<button type='button' class='tbd-nut nho' data-tbd-hs-act='doi'>Đổi tên</button><button type='button' class='tbd-nut nho chinh' data-nhap='mo'>Dùng hồ sơ Chrome có sẵn...</button>" +
      (cur.nhap_tu ? "<button type='button' class='tbd-nut nho' data-nhap='lam_moi'>Cập nhật đăng nhập từ " + esc(cur.nhap_tu) + "</button>" : "") + (ds.length > 1 ? "<button type='button' class='tbd-nut nho' data-tbd-hs-act='xoa'>Xóa trình duyệt này</button>" : "") + "</div>";
    if (hsForm === "them" || hsForm === "doi") h += "<div class='tbd-xn tbd-ten'><p><b>" + (hsForm === "them" ? "Tên trình duyệt mới" : "Tên mới cho \"" + esc(cur.ten) + "\"") + "</b> (ví dụ Facebook Sang, Fanpage Shop A)</p><div class='tbd-hang'><input id='tbdTen' type='text' maxlength='40' value='" + (hsForm === "doi" ? esc(cur.ten) : "") + "' placeholder='Tên trình duyệt'>" +
      "<button type='button' class='tbd-nut chinh' data-tbd-hs-act='ok'>" + (hsForm === "them" ? "Tạo" : "Lưu tên") + "</button><button type='button' class='tbd-nut' data-tbd-hs-act='huy'>Hủy</button></div></div>";
    if (hsForm === "xoa") h += "<div class='tbd-xn'><p><b>Xóa \"" + esc(cur.ten) + "\"?</b> Mọi tài khoản đã đăng nhập trong trình duyệt này sẽ mất, phải đăng nhập lại nếu cần. Không ảnh hưởng trình duyệt khác và Chrome cá nhân của anh.</p><div class='tbd-hang'><button type='button' class='tbd-nut do' data-tbd-hs-act='xoa_ok'>Xóa</button><button type='button' class='tbd-nut' data-tbd-hs-act='huy'>Hủy</button></div></div>";
    return h + "</div>" + theNhap();
  }
  function veTb() {
    var d = ST, chay = !!d.dang_chay;
    var h = "";
    (d.cho_duyet || []).forEach(function (x) { h += theDuyet(x); });
    if (d.cho_nguoi) h += "<div class='tbd-the tbd-duyet'><h3>AI đang chờ anh</h3><p>" + esc(d.cho_nguoi.ly_do) + ". Anh làm ngay trong cửa sổ trình duyệt (gõ mật khẩu, mã xác thực, giải CAPTCHA). Xong là AI tự làm tiếp.</p></div>";
    h += theHoSo(d);
    h += theMuc(d);
    h += "<div class='tbd-the'><h3>Cửa sổ: " + esc(d.ten_xem || "trình duyệt") + "</h3><div class='tbd-tt'><span><i class='tbd-cham " + (d.dung ? "dung" : chay ? "on" : "") + "'></i>" +
      (d.dung ? "Đã dừng AI" : chay ? "Đang mở" + (d.chrome ? " (" + esc(d.chrome.replace(/\.exe$/i, "")) + ")" : "") : "Chưa mở") + "</span>" +
      "<button type='button' class='tbd-nut chinh' data-tbd='mo'>" + (chay ? "Đưa trình duyệt lên trước" : "Mở trình duyệt") + "</button>" +
      (chay ? "<button type='button' class='tbd-nut' data-tbd='dong'>Đóng trình duyệt</button>" : "") +
      (d.dung ? "<button type='button' class='tbd-nut chinh' data-tbd='tiep'>Cho AI làm tiếp</button>" : "<button type='button' class='tbd-nut do' data-tbd='dung'>Dừng AI ngay</button>") + "</div>" +
      (d.loi ? "<p style='color:#ef4444'>" + esc(d.loi) + "</p>" : "") +
      ((d.trang || []).length ? "<p style='margin-top:10px'>Tab đang mở: " + (d.trang || []).map(function (t) { return esc(t.tieu_de || t.host); }).join(" · ") + "</p>" : "") + "</div>";
    h += "<div class='tbd-the'><h3>Đăng nhập một lần, AI dùng lại</h3><ol class='tbd-buoc'><li>Bấm trang cần dùng bên dưới, cửa sổ trình duyệt mở ra.</li><li><b>Anh tự đăng nhập</b> (mật khẩu, mã xác thực anh gõ, TISA BOT không nhận và không thấy).</li><li>Quay lại chat, giao việc. AI tự nhìn trang, bấm, gõ, làm thay anh.</li></ol><p style='margin-top:8px'><b>Chỉ có MỘT trình duyệt dùng chung.</b> Anh đăng nhập mọi tài khoản (Google, Facebook, TikTok, Facebook Ads, Zalo...) vào đúng cửa sổ này một lần, lần sau AI dùng lại, không phải đăng nhập lại. Đóng rồi mở lại vẫn còn.</p>" +
      "<div class='tbd-luoi' style='margin-top:10px'><button type='button' class='tbd-nut nho chinh' data-tbd-mo='" + esc(location.origin + "/") + "'>Mở TISA BOT (để AI tự cài đặt, kết nối)</button></div><div class='tbd-luoi' style='margin-top:8px'>" + TRANG.map(function (t) { return "<button type='button' class='tbd-nut nho' data-tbd-mo='" + esc(t[1]) + "'>" + esc(t[0]) + "</button>"; }).join("") + "</div></div>";
    var dn = d.da_dang_nhap || [];
    h += "<div class='tbd-the'><h3>Trang đã đăng nhập</h3>" + (dn.length ? "<div class='tbd-luoi'>" + dn.slice(0, 24).map(function (x) { return "<span class='tbd-mien" + (x.phien ? " phien" : "") + "'>" + esc(x.mien) + (x.phien ? " <i>✓</i>" : "") + "</span>"; }).join("") + "</div><p style='margin-top:8px'>Chỉ hiện tên trang. ✓ là có phiên đăng nhập. Cookie và mật khẩu không bao giờ hiện ở đây và không đưa vào mô hình.</p>" :
      "<p>" + (chay ? "Chưa thấy phiên đăng nhập nào." : "Mở trình duyệt để xem.") + "</p>") + "</div>";
    h += "<div class='tbd-the'><h3>AI vừa làm gì</h3>" + ((d.nhat_ky || []).length ? "<div class='tbd-nk'>" + (d.nhat_ky || []).slice().reverse().map(dongNk).join("") + "</div>" : "<p>Chưa có thao tác nào.</p>") +
      "<p style='margin-top:8px'>An toàn: AI không nhập mật khẩu, mã xác thực, CAPTCHA, không thanh toán, không vào trang ngân hàng. Đăng, gửi, xóa, đổi bảo mật luôn xin anh duyệt.</p></div>";
    return h;
  }

  /* ---------- Điều khiển máy tính (tab thứ hai) ---------- */
  var TAB = "tb", STM = null, hoiToanM = false, hoiXoa = false;
  function theMucMay(d) {
    var cur = d.muc || "quan_trong";
    var h = "<div class='tbd-the'><h3>Mức tự động khi AI dùng máy của anh</h3><p>Riêng cho việc điều khiển máy tính (chuột, bàn phím, mở ứng dụng). Đổi lúc nào cũng được.</p><div class='tbd-muc'>" +
      MUC.map(function (m) {
        var mo = m[2];
        if (m[0] === "toan_quyen") mo = "AI tự làm mọi thao tác trên máy, không hỏi. Vẫn KHÔNG xóa tệp (trừ khi anh bật công tắc xóa), vẫn không bấm vào cửa sổ mật khẩu, ví, ngân hàng.";
        if (m[0] === "hoi_het") mo = "AI xin duyệt trước từng cú bấm, gõ, mở ứng dụng. An toàn nhất, chậm nhất.";
        if (m[0] === "quan_trong") mo = "Khuyên dùng. AI tự mở ứng dụng, xem, bấm thường; chỉ hỏi khi gõ lệnh Terminal, gửi tin nhắn, đổi cài đặt hệ thống, thoát ứng dụng, mở tệp cài đặt.";
        return "<button type='button' class='tbd-mc" + (cur === m[0] ? " on" : "") + (m[0] === "toan_quyen" ? " tq" : "") + "' data-may-muc='" + m[0] + "' aria-pressed='" + (cur === m[0]) + "'><b>" + esc(m[1]) +
          (cur === m[0] && m[0] === "toan_quyen" ? esc(conLai(d.muc_den) || " (đến khi tắt)") : "") + "</b><span>" + esc(mo) + "</span></button>";
      }).join("") + "</div>";
    if (hoiToanM) h += "<div class='tbd-xn'><p><b>Bật Toàn quyền điều khiển máy?</b> AI sẽ tự bấm, gõ, mở ứng dụng trên máy này mà không hỏi. Anh chịu trách nhiệm với việc AI làm. Đưa chuột về góc trên trái màn hình hoặc bấm Dừng AI ngay để dừng.</p>" +
      "<div class='tbd-hang'><select id='tbdPhutM'><option value='30'>Trong 30 phút</option><option value='120'>Trong 2 giờ</option><option value='0'>Đến khi anh tắt</option></select>" +
      "<button type='button' class='tbd-nut do' data-may-muc-ok='1'>Bật Toàn quyền</button><button type='button' class='tbd-nut' data-may-muc-ok='0'>Hủy</button></div></div>";
    return h + "</div>";
  }
  function veMay() {
    var d = STM || {}, q = d.quyen || {}, h = "";
    if (d.ho_tro === false) return "<div class='tbd-the'><h3>Chưa hỗ trợ</h3><p>Máy này chưa hỗ trợ điều khiển máy tính (cần macOS hoặc Windows).</p></div>";
    (ST && ST.cho_duyet || []).forEach(function (x) { h += theDuyet(x); });
    var macOS = d.he === "macOS", thieu = macOS && (!q.tro_nang || q.ghi_man_hinh === false);
    h += "<div class='tbd-the'><h3>Điều khiển máy tính</h3><p>AI dùng chính máy anh như người thật: nhìn màn hình, di chuột, bấm, gõ, mở thư mục, tệp, ứng dụng. Chạy ngay trên máy này, không tải gì lên mạng.</p>" +
      "<div class='tbd-tt'><span><i class='tbd-cham " + (d.dung ? "dung" : "on") + "'></i>" + (d.dung ? "Đã dừng AI" : "Sẵn sàng") + (d.truoc ? " · đang ở trước: " + esc(d.truoc) : "") + "</span>" +
      (d.dung ? "<button type='button' class='tbd-nut chinh' data-may-act='tiep'>Cho AI làm tiếp</button>" : "<button type='button' class='tbd-nut do' data-may-act='dung'>Dừng AI ngay</button>") +
      "<button type='button' class='tbd-nut' data-may-act='thu'>Thử chụp màn hình</button></div>" +
      "<div id='tbdAnhThu' style='margin-top:10px'></div><p style='margin-top:8px'>Dừng khẩn cấp: đưa chuột về <b>góc trên trái</b> màn hình. AI cũng tự dừng khi anh bấm Dừng AI ngay.</p></div>";
    if (macOS) {
      h += "<div class='tbd-the" + (thieu ? " tbd-duyet" : "") + "'><h3>Quyền của macOS " + (thieu ? "(còn thiếu)" : "(đã đủ)") + "</h3><p>Trợ năng (điều khiển chuột, bàn phím): <b>" + (q.tro_nang ? "đã cấp" : "CHƯA cấp") +
        "</b>. Ghi màn hình (nhìn màn hình): <b>" + (q.ghi_man_hinh === false ? "CHƯA cấp" : q.ghi_man_hinh ? "đã cấp" : "không rõ") + "</b>.</p>" +
        (thieu ? "<p>Cấp quyền cho chương trình này (bấm dấu + nếu chưa có trong danh sách, bật công tắc): <code style='word-break:break-all'>" + esc(q.chuong_trinh || "") + "</code></p>" : "") +
        "<div class='tbd-hang'><button type='button' class='tbd-nut nho' data-may-act='q-tro-nang'>Mở cài đặt Trợ năng</button><button type='button' class='tbd-nut nho' data-may-act='q-man-hinh'>Mở cài đặt Ghi màn hình</button></div></div>";
    }
    h += theMucMay(d);
    var xoa = d.cho_xoa_giay || 0;
    h += "<div class='tbd-the" + (xoa ? " tbd-duyet" : "") + "'><h3>Cho phép AI xóa tệp</h3><p>" + (xoa ? "<b>Đang BẬT</b>, còn khoảng " + Math.ceil(xoa / 60) + " phút rồi tự tắt. AI được xóa tệp, thư mục trên máy anh trong thời gian này." :
      "<b>Đang TẮT</b> ở mọi mức, kể cả Toàn quyền. AI không được xóa tệp, thư mục, không dọn Thùng rác. Chỉ bật khi anh thật sự muốn AI xóa giúp.") + "</p>";
    if (hoiXoa) h += "<div class='tbd-xn'><p><b>Cho AI xóa tệp?</b> Tệp bị xóa có thể không khôi phục được. Chỉ bật khi anh đã nói rõ AI xóa cái gì. Công tắc tự tắt khi hết giờ.</p><div class='tbd-hang'><select id='tbdPhutX'><option value='10'>Trong 10 phút</option><option value='30'>Trong 30 phút</option><option value='60'>Trong 1 giờ</option></select>" +
      "<button type='button' class='tbd-nut do' data-may-xoa-ok='1'>Cho phép xóa</button><button type='button' class='tbd-nut' data-may-xoa-ok='0'>Hủy</button></div></div>";
    else h += "<div class='tbd-hang'>" + (xoa ? "<button type='button' class='tbd-nut chinh' data-may-xoa='tat'>Tắt quyền xóa ngay</button>" : "<button type='button' class='tbd-nut do' data-may-xoa='bat'>Bật quyền xóa...</button>") + "</div>";
    h += "</div>";
    h += "<div class='tbd-the'><h3>AI vừa làm gì trên máy</h3>" + ((d.nhat_ky || []).length ? "<div class='tbd-nk'>" + (d.nhat_ky || []).slice().reverse().map(function (x) { return dongNk({ t: x.t, op: String(x.op || "").replace(/^may_/, ""), ten: x.ten, mo_ta: x.mo_ta, ket_qua: x.ket_qua }); }).join("") + "</div>" : "<p>Chưa có thao tác nào.</p>") +
      "<p style='margin-top:8px'>Luôn có: không xóa tệp, không bấm vào cửa sổ mật khẩu, ví, ngân hàng. Gõ lệnh Terminal, gửi tin nhắn, đổi cài đặt hệ thống, thoát ứng dụng cần anh duyệt (trừ mức Toàn quyền).</p></div>";
    return h;
  }
  function ve() {
    if (!lop || !ST) return;
    var tabs = "<div class='tbd-tabs'><button type='button' class='" + (TAB === "tb" ? "on" : "") + "' data-tbd-tab='tb'>Trình duyệt</button><button type='button' class='" + (TAB === "may" ? "on" : "") + "' data-tbd-tab='may'>Máy tính</button></div>";
    var nd = TAB === "may" ? veMay() : veTb();
    lop.querySelector(".tbd-than").innerHTML = tabs + nd;
  }

  // Đang gõ tên, chọn thời hạn hay mở hộp xác nhận thì KHÔNG vẽ lại bảng (vẽ lại mỗi 3 giây làm mất chữ đang gõ).
  function dangNhap() {
    var a = D.activeElement;
    return !!(hsForm || nhapUI || hoiToan || hoiToanM || hoiXoa || (a && lop && lop.contains(a) && /^(INPUT|SELECT|TEXTAREA)$/.test(a.tagName)));
  }
  function lam(nhe) {
    var p2 = (TAB === "may" && lop) ? api("/may-ai/trang-thai").then(function (m) { STM = m || {}; }) : Promise.resolve();
    var q = "?" + (nhe ? "nhe=1&" : "") + (XEM ? "hoso=" + encodeURIComponent(XEM) : "");
    return Promise.all([api("/trinh-duyet/trang-thai" + q), p2]).then(function (r) { ST = r[0] || {}; if (lop && !dangNhap()) ve(); thongBao(); return ST; });
  }

  function thongBao() {
    if (!ST) return;
    var ds = ST.cho_duyet || [], cn = ST.cho_nguoi;
    if (!ds.length && !cn) { if (noi) { noi.remove(); noi = null; } return; }
    if (lop) { if (noi) { noi.remove(); noi = null; } return; }       // trong bảng đã hiện
    css();
    if (!noi) { noi = D.createElement("div"); noi.className = "tbd-noi"; D.body.appendChild(noi); }
    noi.innerHTML = ds.map(function (x) {
      return "<div class='tbd-ntc'><b>AI xin duyệt: " + esc(x.mo_ta) + "</b><small>Nút \"" + esc(x.ten || "") + "\" trên " + esc(x.host) + "</small><div class='tbd-hang'>" +
        "<button type='button' class='tbd-nut chinh nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='1'>Duyệt</button><button type='button' class='tbd-nut nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='1' data-tat='30'>Duyệt, đừng hỏi nữa</button><button type='button' class='tbd-nut nho' data-tbd-duyet='" + esc(x.id) + "' data-ok='0'>Không</button>" +
        "<button type='button' class='tbd-nut nho' data-tbd='bang'>Xem</button></div></div>";
    }).join("") + (cn ? "<div class='tbd-ntc'><b>AI đang chờ anh</b><small>" + esc(cn.ly_do) + ". Làm trong cửa sổ trình duyệt, xong AI tự làm tiếp.</small><button type='button' class='tbd-nut nho' data-tbd='bang'>Xem</button></div>" : "");
  }

  function baoChat() {
    var i = D.getElementById("chatInput");
    if (i && !String(i.value || "").trim()) { i.value = "Anh đã duyệt rồi, em làm tiếp nhé."; i.dispatchEvent(new Event("input", { bubbles: true })); }
  }

  function bam(e) {
    var t = e.target.closest && e.target.closest("[data-nhap],[data-tbd-hs],[data-tbd-hs-act],[data-tbd],[data-tbd-mo],[data-tbd-duyet],[data-tbd-muc],[data-tbd-muc-ok],[data-tbd-tab],[data-may-muc],[data-may-muc-ok],[data-may-xoa],[data-may-xoa-ok],[data-may-act]");
    if (!t) return;
    if (t.hasAttribute("data-tbd-duyet")) {
      var id = t.getAttribute("data-tbd-duyet"), ok = t.getAttribute("data-ok") === "1", tat = Number(t.getAttribute("data-tat") || 0);
      t.disabled = true;
      var truoc = tat ? api("/trinh-duyet/muc", { muc: "toan_quyen", phut: tat }) : Promise.resolve();
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
        api("/trinh-duyet/nhap-chrome", { nguon: nhapUI.chon.nguon, thu_muc: nhapUI.chon.thu_muc, ten: tn }).then(function (r) { nhapUI = { kq: r || { ok: false, loi: "Không nhập được." } }; if (r && r.id) XEM = r.id; ve(); lam(); });
        return;
      }
      if (na === "mo_xong") { var idm = t.getAttribute("data-id"); nhapUI = null; XEM = idm; api("/trinh-duyet/mo", { hoso: idm }).then(function () { setTimeout(function () { lam(); }, 800); }); return; }
      if (na === "lam_moi") { t.disabled = true; t.textContent = "Đang làm mới..."; api("/trinh-duyet/lam-moi-chrome", { id: xemId() }).then(function (r) { ST = ST || {}; ST.loi = r && r.ok === false ? (r.loi || "") : ""; nhapUI = { kq: Object.assign({ ten: "Đăng nhập đã làm mới" }, r || {}) }; ve(); lam(); }); return; }
      return;
    }
    if (t.hasAttribute("data-tbd-hs")) { XEM = t.getAttribute("data-tbd-hs"); hsForm = ""; lam(); return; }
    if (t.hasAttribute("data-tbd-hs-act")) {
      var ha = t.getAttribute("data-tbd-hs-act"), idx = xemId();
      if (ha === "them" || ha === "doi" || ha === "xoa") { hsForm = ha === "xoa" ? "xoa" : ha; ve(); var ti = D.getElementById("tbdTen"); if (ti) { ti.focus(); ti.select(); } return; }
      if (ha === "huy") { hsForm = ""; ve(); return; }
      if (ha === "mac_dinh") { api("/trinh-duyet/ho-so", { hanh: "chon", id: idx }).then(function () { lam(); }); return; }
      if (ha === "ok") {
        var ten = (D.getElementById("tbdTen") || {}).value || "", f = hsForm; hsForm = "";
        (f === "them" ? api("/trinh-duyet/ho-so", { hanh: "tao", ten: ten }).then(function (r) { if (r && r.id) XEM = r.id; return r; }) : api("/trinh-duyet/ho-so", { hanh: "doi_ten", id: idx, ten: ten }))
          .then(function (r) { if (r && r.ok === false) { ST = ST || {}; ST.loi = r.loi || ""; } lam(); });
        return;
      }
      if (ha === "xoa_ok") { hsForm = ""; api("/trinh-duyet/ho-so", { hanh: "xoa", id: idx }).then(function (r) { XEM = ""; if (r && r.ok === false) { ST = ST || {}; ST.loi = r.loi || ""; } lam(); }); return; }
      return;
    }
    if (t.hasAttribute("data-tbd-tab")) { TAB = t.getAttribute("data-tbd-tab"); lam(); return; }
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

  function mo(tab) {
    css();
    if (tab === "may" || tab === "tb") TAB = tab;
    if (lop) { lam(); return; }
    lop = D.createElement("div"); lop.className = "tbd-lop"; lop.setAttribute("role", "dialog"); lop.setAttribute("aria-modal", "true"); lop.setAttribute("aria-label", "Trình duyệt TISA");
    lop.innerHTML = "<div class='tbd-cua'><div class='tbd-dau'><span class='tbd-dau-i'>" + ICON + "</span><div class='tbd-dau-t'><b>Điều khiển của AI</b><span>Trình duyệt dùng chung và máy tính của anh</span></div>" +
      "<button type='button' class='tbd-nut' data-tbd='x' aria-label='Đóng'>Đóng</button></div><div class='tbd-than'><p>Đang tải…</p></div></div>";
    lop.addEventListener("mousedown", function (e) { if (e.target === lop) dong(); });
    D.body.appendChild(lop);
    if (noi) { noi.remove(); noi = null; }
    lam();
    tim = setInterval(function () { lam(); }, 3000);
  }
  function dong() { if (lop) { lop.remove(); lop = null; } if (tim) { clearInterval(tim); tim = null; } thongBao(); }

  var dangNgam = 0;
  function ngam() {
    if (D.hidden) return;
    api("/trinh-duyet/trang-thai?nhe=1").then(function (d) {
      ST = d || {}; thongBao();
      dangNgam = (ST.dang_chay || (ST.cho_duyet || []).length || ST.cho_nguoi) ? 0 : Math.min(dangNgam + 1, 6);
    });
  }
  function nhip() { ngam(); setTimeout(nhip, dangNgam >= 3 ? 15000 : 4000); }

  var ICON_MENU = '<svg class="cp-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>';
  function dangKy(n) {
    var M = W.TISAComposerMenu;
    if (!M || !M.register) { if (n < 60) setTimeout(function () { dangKy(n + 1); }, 250); return; }
    M.register({ id: "trinh_duyet", order: 16, icon: ICON_MENU, label: "Mở trình duyệt cho AI thao tác", hint: function () { return "Đăng nhập một lần"; }, run: function () { mo("tb"); } });
    M.register({ id: "dieu_khien_may", order: 17, icon: ICON_MENU, label: "Cho AI điều khiển máy tính", hint: function () { return "Chuột, bàn phím, ứng dụng"; }, run: function () { mo("may"); } });
  }
  /* Nút luôn thấy bên cạnh dấu + của khung chat (Hỏi nhanh, Hỏi chuyên gia), không cần mở menu. */
  var CSS2 = ".tbd-pill{width:auto!important;padding:0 11px!important;gap:6px;display:inline-flex;align-items:center;white-space:nowrap;font:600 12.5px/1 inherit;border-radius:999px!important}.tbd-pill svg{width:16px;height:16px;flex:none}" +
    ".tbd-pill i{display:none;width:8px;height:8px;border-radius:50%;background:#22c55e}.tbd-pill.on i{display:inline-block}@media (max-width:640px){.tbd-pill span{display:none}.tbd-pill{padding:0 9px!important}}";
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
      b.title = "Mở trình duyệt cho AI thao tác. Mức tự động: " + ten;
    });
  }
  W.addEventListener("message", function (e) { if (e.data && e.data.tisaTrinhDuyet === "mo") mo(); });
  setInterval(function () { chenNut(); chamXanh(); }, 1500);
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
  function khoi() { dangKy(0); setTimeout(nhip, 2500); }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", khoi); else khoi();
  W.TISABrowser = { mo: mo, dong: dong, moMay: function () { mo("may"); } };
})();
