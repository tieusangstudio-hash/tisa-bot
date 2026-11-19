/* tisa-kho-drive.js - Kho tư liệu nối Google Drive (V3.34, chủ yêu cầu 19/11/2026). Chạy TRONG trang Đội Quân AI mở qua /doiquanagent
   (tisa_giao_dien.py chèn vào), thêm thẻ "Google Drive" lên đầu trang Kho tư liệu và sắp lại trang thành ba nguồn rõ ràng:
   1. Google Drive: nối một lần, chọn THƯ MỤC LÀM VIỆC (chép tư liệu về kho) và THƯ MỤC NHẬN KẾT QUẢ (đội tải kết quả lên).
   2. Tải từ máy tính (khung kéo thả có sẵn).  3. Thư mục có sẵn trên máy (liên kết có sẵn).
   Máy chủ: server/tisa_kho_drive.py (/tisa-kho-drive/api/*). Khóa Google không bao giờ đi qua bảng hay AI: ô dán khóa gửi thẳng về máy này. */
(function () {
  "use strict";
  var W = window, D = document;
  var API = "/tisa-kho-drive/api/";
  var st = null, view = null, root = null, timer = 0, dnTimer = 0, dangDangNhap = false, moForm = false, moHd = false, msg = {}, modal = null;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(path, body) {
    var o = { credentials: "same-origin" };
    if (body !== undefined) { o.method = "POST"; o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(body); }
    return fetch(API + path, o).then(function (r) { return r.json().catch(function () { return {}; }); }).catch(function () { return { ok: false, error: "Không nối được máy chủ TISA BOT." }; });
  }
  function gio(t) {
    if (!t) return "chưa lần nào";
    var d = new Date(t * 1000), h = new Date();
    var hm = ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
    return d.toDateString() === h.toDateString() ? "hôm nay " + hm : ("0" + d.getDate()).slice(-2) + "/" + ("0" + (d.getMonth() + 1)).slice(-2) + " " + hm;
  }
  function dungLuong(b) {
    b = Number(b || 0);
    if (b >= 1073741824) return (b / 1073741824).toFixed(1).replace(".", ",") + " GB";
    if (b >= 1048576) return Math.round(b / 1048576) + " MB";
    return Math.max(1, Math.round(b / 1024)) + " KB";
  }

  var ICO_DRIVE = '<svg viewBox="0 0 87.3 78" width="26" height="26" aria-hidden="true"><path fill="#0066da" d="m6.6 66.85 3.85 6.65c.8 1.4 1.95 2.5 3.3 3.3l13.75-23.8h-27.5c0 1.55.4 3.1 1.2 4.5z"/><path fill="#00ac47" d="M43.65 25 29.9 1.2c-1.35.8-2.5 1.9-3.3 3.3l-25.4 44a9.06 9.06 0 0 0-1.2 4.5h27.5z"/><path fill="#ea4335" d="M73.55 76.8c1.35-.8 2.5-1.9 3.3-3.3l1.6-2.75 7.65-13.25c.8-1.4 1.2-2.95 1.2-4.5h-27.502l5.852 11.5z"/><path fill="#00832d" d="M43.65 25 57.4 1.2C56.05.4 54.5 0 52.9 0H34.4c-1.6 0-3.15.45-4.5 1.2z"/><path fill="#2684fc" d="M59.8 53h-32.3L13.75 76.8c1.35.8 2.9 1.2 4.5 1.2h50.8c1.6 0 3.15-.45 4.5-1.2z"/><path fill="#ffba00" d="m73.4 26.5-12.7-22c-.8-1.4-1.95-2.5-3.3-3.3L43.65 25 59.8 53h27.45c0-1.55-.4-3.1-1.2-4.5z"/></svg>';
  var ICO_DIR = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>';

  var CSS = "#kdDrive{display:grid;gap:14px;padding:18px;margin-bottom:14px}" +
    "#kdDrive .kd-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}#kdDrive .kd-top>.kd-ico{display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:var(--surface-2,#f1f5f9)}" +
    "#kdDrive .kd-top .kd-tt{flex:1 1 220px;min-width:0}#kdDrive .kd-top b{font-size:16px;display:block}#kdDrive .kd-top small{color:var(--muted,#64748b);display:block;margin-top:2px;line-height:1.4}" +
    "#kdDrive .kd-dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#16a34a;margin-right:6px;vertical-align:1px}" +
    "#kdDrive .kd-hero{display:grid;gap:12px;padding:16px;border:1px dashed var(--line,#d6dbe4);border-radius:14px;background:var(--surface-2,#f8fafc)}" +
    "#kdDrive .kd-hero p{margin:0;line-height:1.5}#kdDrive .kd-hang{display:flex;gap:10px;flex-wrap:wrap;align-items:center}" +
    "#kdDrive .kd-form{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}#kdDrive .kd-form label{display:grid;gap:4px;font-size:12.5px;color:var(--muted,#64748b)}" +
    "#kdDrive input[type=text],#kdDrive input[type=password],#kdDrive select,.kd-modal input[type=text]{height:40px;box-sizing:border-box;padding:0 12px;border:1px solid var(--line,#d6dbe4);border-radius:10px;background:var(--surface,#fff);color:inherit;font:inherit;min-width:0}" +
    "#kdDrive .kd-cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}" +
    "#kdDrive .kd-box{display:grid;gap:10px;align-content:start;padding:14px;border:1px solid var(--line,#e2e8f0);border-radius:14px;background:var(--surface,#fff)}" +
    "#kdDrive .kd-box h4{margin:0;font-size:13px;letter-spacing:.02em;text-transform:uppercase;color:var(--navy,#172F72);display:flex;gap:8px;align-items:center}" +
    "#kdDrive .kd-box h4 i{font-style:normal;display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--b1,#FF6B35);color:#fff;font-size:12px}" +
    "#kdDrive .kd-box>p{margin:0;font-size:13px;color:var(--muted,#64748b);line-height:1.45}" +
    "#kdDrive .kd-chon{display:flex;gap:10px;align-items:center;padding:10px 12px;border:1px solid var(--line,#e2e8f0);border-radius:12px;min-width:0}" +
    "#kdDrive .kd-chon .kd-ten{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}#kdDrive .kd-chon .kd-ten small{display:block;color:var(--muted,#64748b);overflow:hidden;text-overflow:ellipsis}" +
    "#kdDrive .kd-chon.kd-trong{border-style:dashed;color:var(--muted,#64748b)}" +
    "#kdDrive .kd-tt2{font-size:12.5px;color:var(--muted,#64748b);line-height:1.5}#kdDrive .kd-tt2 b{color:inherit}" +
    "#kdDrive .kd-tick{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:13.5px}#kdDrive .kd-tick input{width:17px;height:17px;flex:0 0 auto}#kdDrive .kd-tick select{width:auto;flex:0 0 auto}#kdDrive .kd-tt2 select{width:auto;height:34px}" +
    "#kdDrive .kd-loi{color:#dc2626;font-size:13px}#kdDrive .kd-ok{color:#16a34a;font-size:13px}#kdDrive .kd-canh{font-size:12.5px;padding:8px 10px;border-radius:10px;background:#fffbeb;color:#92400e}" +
    "#kdDrive details.kd-hd{border:1px solid var(--line,#e2e8f0);border-radius:12px;padding:8px 12px;background:var(--surface,#fff)}#kdDrive details.kd-hd summary{cursor:pointer;font-weight:600;font-size:13.5px}" +
    "#kdDrive details.kd-hd ol{margin:8px 0 2px;padding-left:20px;line-height:1.6;font-size:13px}" +
    "#kdDrive .btn[disabled]{opacity:.55;cursor:default}#kdDrive .kd-an{display:none}" +
    ".kd-sec{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:2px 0 10px}.kd-sec b{font-size:15px}.kd-sec small{color:var(--muted,#64748b)}" +
    ".kd-modal{position:fixed;inset:0;z-index:2000;display:grid;place-items:center;background:rgba(15,23,42,.55);padding:16px}" +
    ".kd-modal .kd-card{width:min(560px,100%);max-height:min(640px,92vh);display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;gap:10px;padding:18px;border-radius:16px;background:var(--surface,#fff);color:var(--text,inherit);box-shadow:0 20px 60px rgba(0,0,0,.35)}" +
    ".kd-modal h3{margin:0;font-size:16px}.kd-modal .kd-duong{display:flex;gap:4px;flex-wrap:wrap;font-size:13px;align-items:center}.kd-modal .kd-duong button{border:0;background:none;color:var(--navy,#172F72);cursor:pointer;padding:2px 4px;font:inherit;text-decoration:underline}" +
    ".kd-modal .kd-ds{overflow:auto;border:1px solid var(--line,#e2e8f0);border-radius:12px;min-height:140px}.kd-modal .kd-ds button.kd-dong{display:flex;gap:10px;align-items:center;width:100%;text-align:left;padding:10px 12px;border:0;border-bottom:1px solid var(--line,#eef1f5);background:none;color:inherit;font:inherit;cursor:pointer}" +
    ".kd-modal .kd-ds button.kd-dong:hover{background:var(--surface-2,#f1f5f9)}.kd-modal .kd-ds .kd-rong{padding:18px;color:var(--muted,#64748b);font-size:13px;text-align:center}" +
    ".kd-modal .kd-chan{display:grid;gap:8px}.kd-modal .kd-hang{display:flex;gap:8px;flex-wrap:wrap}.kd-modal .kd-hang input{flex:1 1 180px}" +
    "@media (max-width:760px){#kdDrive .kd-cols,#kdDrive .kd-form{grid-template-columns:minmax(0,1fr)}}";

  function css() {
    if (D.getElementById("kdCss")) return;
    var s = D.createElement("style"); s.id = "kdCss"; s.textContent = CSS; (D.head || D.documentElement).appendChild(s);
  }

  // ---------------------------------------------------------------- lời nhờ TISA BOT tự kết nối (giao cho Đạt Đấu Nối)
  function loiNho() {
    return [
      "Dùng kỹ năng dq-dau-noi-cong-cu và dq-ho-tro-ket-noi (phần Google Drive): nối Google Drive vào Kho tư liệu của TISA BOT bằng API. Làm luôn từng bước.",
      "Mục tiêu: Kho tư liệu chép tư liệu từ một thư mục Drive về máy, và tải kết quả đội AI làm xong lên một thư mục Drive.",
      "Dùng đúng trình duyệt anh đã chọn. Chưa đăng nhập Google thì dừng (wait_user) để anh tự đăng nhập.",
      "",
      "CÁC BƯỚC:",
      "1. tisa_drive_do op=trang_thai: xem đã có khóa Google (co_oauth_client) và đã đăng nhập chưa. Đã đăng nhập rồi thì báo anh, không làm lại.",
      "2. Chưa có khóa: vào https://console.cloud.google.com. Dùng project TISA BOT sẵn có hoặc tạo mới. Bật Google Drive API. Màn hình đồng ý OAuth (Google Auth Platform): loại External, thêm CHÍNH email Google của anh vào người dùng thử, rồi bấm Publish app để quyền không hết hạn sau 7 ngày.",
      "   Tạo OAuth client ID loại \"Desktop app\" (ứng dụng máy tính). Cất Client ID và Client secret vào kho khóa bằng tisa_browser_do op=luu_keychain ten=drive-client truong=client_id, rồi truong=client_secret (giá trị đi thẳng từ trang vào kho khóa, KHÔNG đọc ra, KHÔNG chép vào chat).",
      "3. tisa_drive_do op=dang_nhap: mở địa chỉ trả về trong trình duyệt anh đã chọn để anh bấm Cho phép (bước chỉ người thật làm; Google báo \"chưa được xác minh\" thì bấm Nâng cao rồi Tiếp tục). Xong gọi op=dang_nhap_xem.",
      "4. Báo anh: \"Xong phần kết nối. Anh quay lại trang Kho tư liệu bấm Chọn thư mục làm việc và Chọn thư mục nhận kết quả.\"",
      "",
      "LUẬT: KHÔNG đọc hay chép Client secret, mật khẩu, mã xác thực ra chat. Dừng nhờ anh ở: đăng nhập, mật khẩu, mã xác thực, CAPTCHA, bấm Cho phép của Google. Không xóa gì trên Drive. Cuối cùng tóm tắt ngắn bước nào xong, bước nào anh cần làm."
    ].join("\n");
  }
  function nhoTuDong() {
    var f = null;
    try { f = (W.parent && W.parent !== W && W.parent.TISANhoAI) || W.TISANhoAI || null; } catch (e) { f = null; }
    if (typeof f === "function") {
      datMsg("nho", "Đang giao việc cho TISA BOT, xem ở khung chat.", "ok"); ve();
      try {
        var p = f(loiNho(), "Kết nối Google Drive");
        if (p && p.then) p.then(function (ok) { if (!ok) { datMsg("nho", "Chưa giao được việc, thử lại hoặc tự kết nối bên dưới.", "loi"); ve(); } });
      } catch (e) { datMsg("nho", "Chưa giao được việc, thử lại hoặc tự kết nối bên dưới.", "loi"); ve(); }
      return;
    }
    var t = loiNho();
    (navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
      datMsg("nho", "Đã chép lời nhờ. Dán vào khung chat TISA BOT.", "ok"); ve();
    }, function () { datMsg("nho", "Chưa tự giao được. Mở khung chat TISA BOT và nhắn: \"Nối Google Drive cho Kho tư liệu\".", "loi"); ve(); });
  }
  function datMsg(k, t, loai) { msg[k] = t ? { t: t, loai: loai || "", luc: Date.now() } : null; }
  // Thông báo thành công tự hết sau 8 giây (lỗi giữ tới khi thao tác lại).
  function dong(k) {
    var m = msg[k];
    if (m && m.loai !== "loi" && Date.now() - m.luc > 8000) { msg[k] = m = null; }
    return m ? '<div class="' + (m.loai === "loi" ? "kd-loi" : "kd-ok") + '" role="status">' + esc(m.t) + "</div>" : "";
  }

  // ---------------------------------------------------------------- vẽ
  function khungTu() {
    return '<details class="kd-hd"' + (moHd ? " open" : "") + '><summary>Cách lấy khóa Google (khoảng 5 phút, làm một lần)</summary><ol>' +
      "<li>Vào <b>console.cloud.google.com</b>, chọn hoặc tạo một project (tên gì cũng được).</li>" +
      "<li>Mục <b>APIs &amp; Services &gt; Library</b>: tìm <b>Google Drive API</b>, bấm <b>Enable</b>.</li>" +
      "<li><b>Google Auth Platform</b>: loại <b>External</b>, thêm email Google của anh vào <b>Test users</b>, rồi bấm <b>Publish app</b> (để quyền không hết hạn sau 7 ngày).</li>" +
      "<li><b>Credentials &gt; Create credentials &gt; OAuth client ID</b>, loại <b>Desktop app</b>. Chép <b>Client ID</b> và <b>Client secret</b> dán vào hai ô bên trên.</li>" +
      "<li>Bấm <b>Lưu khóa và đăng nhập</b>, chọn tài khoản Google, bấm <b>Cho phép</b>. Google báo \"chưa được xác minh\" thì bấm <b>Nâng cao</b> rồi <b>Tiếp tục</b>.</li></ol></details>";
  }
  function veChuaNoi() {
    var chuaKhoa = st.buoc === "chua_client";
    var h = '<div class="kd-hero">';
    if (chuaKhoa) {
      h += "<p><b>Bước 1 trên 2: lấy khóa Google.</b> Cách dễ nhất: để TISA BOT làm giúp: TISA BOT tự bấm trên trang Google, anh chỉ đăng nhập và bấm Cho phép.</p>" +
        '<div class="kd-hang"><button type="button" class="btn btn-primary" data-kd="nho">⚡ Nhờ TISA BOT kết nối tự động</button>' +
        '<button type="button" class="btn" data-kd="mo-form">' + (moForm ? "Ẩn ô dán khóa" : "Tự kết nối: dán khóa Google") + "</button></div>" + dong("nho");
      if (moForm) {
        h += '<div class="kd-form"><label>Client ID<input type="text" id="kdCid" autocomplete="off" spellcheck="false" placeholder="123456-abc.apps.googleusercontent.com"></label>' +
          '<label>Client secret<input type="password" id="kdCs" autocomplete="off" spellcheck="false" placeholder="GOCSPX-..."></label></div>' +
          '<div class="kd-hang"><button type="button" class="btn btn-primary" data-kd="luu-khoa">Lưu khóa và đăng nhập</button><span id="kdKhoaMsg" class="kd-loi"></span></div>' + khungTu();
      }
    } else {
      h += "<p><b>Bước 2 trên 2: đăng nhập Google.</b> Đã có khóa Google trên máy này. Bấm đăng nhập, chọn tài khoản có Drive anh muốn dùng và bấm <b>Cho phép</b>.</p>" +
        '<div class="kd-hang"><button type="button" class="btn btn-primary" data-kd="dang-nhap"' + (dangDangNhap ? " disabled" : "") + ">" + (dangDangNhap ? "Đang chờ anh bấm Cho phép..." : "Đăng nhập Google Drive") + "</button>" +
        '<button type="button" class="btn" data-kd="nho">⚡ Nhờ TISA BOT làm giúp</button></div>' + dong("dn") + dong("nho");
    }
    return h + "</div>";
  }
  function thanhChon(vt, tm, nhan) {
    if (!tm) return '<div class="kd-chon kd-trong">' + ICO_DIR + '<span class="kd-ten">Chưa chọn thư mục</span><button type="button" class="btn btn-primary btn-sm" data-kd="chon" data-vt="' + vt + '">Chọn thư mục</button></div>';
    return '<div class="kd-chon">' + ICO_DIR + '<span class="kd-ten"><b>' + esc(tm.ten) + "</b><small>" + esc(tm.duong || "") + '</small></span><button type="button" class="btn btn-sm" data-kd="chon" data-vt="' + vt + '">Đổi</button></div>';
  }
  function veVe() {
    var t = st.ve || {}, lv = st.lam_viec;
    var h = '<div class="kd-box"><h4><i>1</i>Lấy tư liệu từ Drive về kho</h4><p>Đội AI đọc tư liệu thật trên máy. TISA BOT chép tệp mới trong thư mục Drive này về Kho tư liệu (không xóa gì trên Drive hay trên máy).</p>' +
      thanhChon("lam_viec", lv) +
      '<label class="kd-tick"><input type="checkbox" data-kd="tu-ve"' + (st.tu_ve ? " checked" : "") + (lv ? "" : " disabled") + "> Tự động chép về mỗi <select data-kd=\"chu-ky\"" + (lv ? "" : " disabled") + ">" +
      [5, 15, 30, 60, 180, 1440].map(function (p) { return '<option value="' + p + '"' + (p === st.ve_moi_phut ? " selected" : "") + ">" + (p >= 1440 ? "ngày" : p >= 60 ? (p / 60) + " giờ" : p + " phút") + "</option>"; }).join("") + "</select></label>" +
      '<div class="kd-hang"><button type="button" class="btn btn-primary" data-kd="chay" data-v="ve"' + (lv && !st.dang_chay && !st.cho_ve ? "" : " disabled") + ">↻ " + (st.dang_chay === "ve" ? "Đang chép về..." : st.cho_ve ? "Đang chờ..." : "Đồng bộ ngay") + "</button>" +
      '<label class="kd-tt2">Bỏ qua tệp lớn hơn <select data-kd="gioi-han">' + [100, 200, 500, 1024, 2048, 5120].map(function (m) { return '<option value="' + m + '"' + (m === st.gioi_han_mb ? " selected" : "") + ">" + (m >= 1024 ? (m / 1024) + " GB" : m + " MB") + "</option>"; }).join("") + "</select></label></div>";
    if (t.luc) {
      h += '<div class="kd-tt2">Lần cuối ' + gio(t.luc) + ": <b>" + (t.so_moi || 0) + " tệp mới</b>, kho Drive có " + (t.so_tong || 0) + " tệp" + (t.dung_luong ? ", chép " + dungLuong(t.dung_luong) : "") + ".";
      if (t.bo_qua_lon && t.bo_qua_lon.length) h += "<br>" + t.bo_qua_lon.length + " tệp lớn hơn " + st.gioi_han_mb + " MB chưa chép (tăng giới hạn nếu cần).";
      if (t.loi && t.loi.length) h += '<br><span class="kd-loi">' + t.loi.length + " tệp lỗi: " + esc(String(t.loi[0]).slice(0, 90)) + "</span>";
      h += "</div>";
    }
    if (t.loi_chung) h += '<div class="kd-loi">' + esc(t.loi_chung) + "</div>";
    return h + dong("ve") + "</div>";
  }
  function veLen() {
    var t = st.len || {}, kq = st.ket_qua;
    var h = '<div class="kd-box"><h4><i>2</i>Tải kết quả của đội lên Drive</h4><p>Đội làm xong việc thì kết quả (bài viết, ảnh, video...) được tải lên thư mục Drive này, xếp theo ngày và tên việc.</p>' +
      thanhChon("ket_qua", kq) +
      '<label class="kd-tick"><input type="checkbox" data-kd="tu-len"' + (st.tu_len ? " checked" : "") + (kq ? "" : " disabled") + "> Tự động tải lên khi đội có kết quả mới</label>" +
      '<div class="kd-hang"><button type="button" class="btn btn-primary" data-kd="chay" data-v="len"' + (kq && !st.dang_chay && !st.cho_len ? "" : " disabled") + ">⇪ " + (st.dang_chay === "len" ? "Đang tải lên..." : st.cho_len ? "Đang chờ..." : "Tải kết quả lên ngay") + "</button></div>";
    if (t.luc) {
      h += '<div class="kd-tt2">Lần cuối ' + gio(t.luc) + ": <b>" + (t.so_moi || 0) + " tệp đã lên Drive</b>" + (t.cho_on_dinh ? ", " + t.cho_on_dinh + " tệp đang ghi dở, chờ lượt sau" : "") + ".";
      if (t.gan_nhat && t.gan_nhat.length) h += "<br>Mới nhất: " + t.gan_nhat.slice(-3).map(function (x) { return x.link ? '<a href="' + esc(x.link) + '" target="_blank" rel="noopener">' + esc(x.ten) + "</a>" : esc(x.ten); }).join(", ");
      if (t.loi && t.loi.length) h += '<br><span class="kd-loi">' + t.loi.length + " tệp lỗi: " + esc(String(t.loi[0]).slice(0, 90)) + "</span>";
      h += "</div>";
    }
    if (t.loi_chung) h += '<div class="kd-loi">' + esc(t.loi_chung) + "</div>";
    return h + dong("len") + "</div>";
  }
  function ve() {
    if (!root) return;
    var a = D.activeElement, giu = a && root.contains(a) && a.id ? a.id : "";
    var gtri = {}; ["kdCid", "kdCs"].forEach(function (i) { var e = D.getElementById(i); if (e) gtri[i] = e.value; });
    var h = '<div class="kd-top"><span class="kd-ico">' + ICO_DRIVE + '</span><div class="kd-tt"><b>Google Drive</b>';
    if (!st) { root.innerHTML = h + "<small>Đang kiểm tra...</small></div></div>"; return; }
    if (st.buoc === "da_ket_noi") {
      h += '<small><span class="kd-dot"></span>Đã kết nối' + (st.email ? " · " + esc(st.email) : "") + "</small></div>" +
        '<button type="button" class="btn btn-sm" data-kd="ngat">Ngắt kết nối</button></div>';
      if (!st.cau_noi_song) h += '<div class="kd-canh">Cầu nối của Đội Quân AI chưa chạy trên máy này nên chưa chép hay tải được. Mở lại TISA BOT (hoặc chờ vài chục giây nếu vừa mở).</div>';
      h += '<div class="kd-cols">' + veVe() + veLen() + "</div>" + dong("chung");
    } else {
      h += "<small>Nối Drive để đội lấy tư liệu thật từ Drive về kho và gửi kết quả lại lên Drive. Khóa nằm trên máy anh, không đi qua mạng khác.</small></div></div>" + veChuaNoi();
    }
    root.innerHTML = h;
    Object.keys(gtri).forEach(function (i) { var e = D.getElementById(i); if (e) e.value = gtri[i]; });
    if (giu) { var e2 = D.getElementById(giu); if (e2) try { e2.focus(); } catch (x) {} }
  }

  // ---------------------------------------------------------------- tải trạng thái
  var dauVan = "";
  function lam() {
    return api("trang-thai").then(function (r) {
      var doi = false;
      if (r && r.ok) {
        var v = JSON.stringify(r);
        if (v !== dauVan) { dauVan = v; doi = true; }
        st = r;
        if (st.buoc === "da_ket_noi") dangDangNhap = false;
      } else if (!st) { st = { buoc: "chua_client", ve: {}, len: {} }; doi = true; }
      var ban = !!(st && (st.dang_chay || st.cho_ve || st.cho_len || dangDangNhap));
      if (doi || Object.keys(msg).some(function (k) { return msg[k] && msg[k].loai !== "loi" && Date.now() - msg[k].luc > 8000; })) ve();
      clearTimeout(timer);
      if (view && !view.hidden) timer = setTimeout(function () { lam(); }, ban ? 3000 : 20000);
    });
  }

  // ---------------------------------------------------------------- hộp chọn thư mục
  function moChon(vt) {
    var tieuDe = vt === "lam_viec" ? "Chọn thư mục Drive làm việc (lấy tư liệu về kho)" : "Chọn thư mục Drive nhận kết quả";
    var nganXep = [{ id: "", ten: "Google Drive" }], hienTai = { id: "", ten: "Google Drive", muc: [] }, loi = "", dangTai = true;
    modal = D.createElement("div"); modal.className = "kd-modal"; modal.setAttribute("role", "dialog"); modal.setAttribute("aria-modal", "true");
    D.body.appendChild(modal);
    function dong() { if (modal) { modal.remove(); modal = null; } }
    function vemo() {
      var duong = nganXep.map(function (x, i) { return (i ? " › " : "") + '<button type="button" data-i="' + i + '">' + esc(x.ten) + "</button>"; }).join("");
      var chonDuoc = hienTai.id && hienTai.id !== "sharedWithMe";
      modal.innerHTML = '<div class="kd-card"><h3>' + esc(tieuDe) + '</h3><div class="kd-duong">' + duong + "</div>" +
        '<div class="kd-ds">' + (dangTai ? '<div class="kd-rong">Đang tải...</div>' : loi ? '<div class="kd-rong kd-loi">' + esc(loi) + "</div>" :
          (hienTai.muc.length ? hienTai.muc.map(function (m, i) { return '<button type="button" class="kd-dong" data-m="' + i + '">' + ICO_DIR + "<span>" + esc(m.ten) + "</span></button>"; }).join("") : '<div class="kd-rong">Thư mục này chưa có thư mục con.</div>')) + "</div>" +
        '<div class="kd-chan"><div class="kd-hang"><input type="text" id="kdLink" placeholder="Hoặc dán link thư mục Drive vào đây" autocomplete="off"><button type="button" class="btn" data-a="link">Dùng link này</button></div>' +
        '<div class="kd-hang">' + (chonDuoc ? '<input type="text" id="kdMoi" placeholder="Tên thư mục mới (không bắt buộc)" maxlength="100"><button type="button" class="btn" data-a="tao">Tạo thư mục mới ở đây</button>' : "") + "</div>" +
        '<div class="kd-hang" style="justify-content:flex-end"><button type="button" class="btn" data-a="huy">Hủy</button><button type="button" class="btn btn-primary" data-a="chon"' + (chonDuoc ? "" : " disabled") + ">Chọn thư mục này</button></div></div></div>";
    }
    function vao(id, ten) {
      dangTai = true; loi = ""; vemo();
      api("thu-muc?cha=" + encodeURIComponent(id)).then(function (r) {
        dangTai = false;
        if (!r || !r.ok) { loi = (r && r.error) || "Không mở được thư mục."; } else { hienTai = { id: id, ten: ten || r.ten, muc: r.muc || [] }; }
        vemo();
      });
    }
    function xong(r) {
      if (r && r.ok) { dong(); datMsg(vt === "lam_viec" ? "ve" : "len", "Đã chọn thư mục " + (r.thu_muc ? r.thu_muc.ten : "") + ".", "ok"); lam(); }
      else { loi = (r && r.error) || "Chưa chọn được."; vemo(); }
    }
    modal.addEventListener("click", function (e) {
      var t = e.target;
      if (t === modal) { dong(); return; }
      var m = t.closest && t.closest("[data-m]"), i = t.closest && t.closest("[data-i]"), a = t.closest && t.closest("[data-a]");
      if (m) { var x = hienTai.muc[+m.getAttribute("data-m")]; nganXep.push({ id: x.id, ten: x.ten }); vao(x.id, x.ten); return; }
      if (i) { var k = +i.getAttribute("data-i"); nganXep = nganXep.slice(0, k + 1); vao(nganXep[k].id, nganXep[k].ten); return; }
      if (!a) return;
      var ac = a.getAttribute("data-a");
      if (ac === "huy") dong();
      else if (ac === "chon") api("chon", { vai_tro: vt, id: hienTai.id, ten: hienTai.ten }).then(xong);
      else if (ac === "tao") {
        var ten = (D.getElementById("kdMoi") || {}).value || "";
        if (!ten.trim()) { loi = "Gõ tên thư mục mới trước."; vemo(); return; }
        api("tao-thu-muc", { cha: hienTai.id, ten: ten }).then(function (r) { if (r && r.ok) api("chon", { vai_tro: vt, id: r.id, ten: r.ten }).then(xong); else xong(r); });
      } else if (ac === "link") {
        var lk = (D.getElementById("kdLink") || {}).value || "";
        if (!lk.trim()) { loi = "Dán link thư mục Drive vào ô trước."; vemo(); return; }
        api("phan-giai", { lien_ket: lk }).then(function (r) { if (r && r.ok) api("chon", { vai_tro: vt, id: r.id, ten: r.ten }).then(xong); else xong(r); });
      }
    });
    modal.addEventListener("keydown", function (e) { if (e.key === "Escape") dong(); });
    vao("", "Google Drive");
  }

  // ---------------------------------------------------------------- đăng nhập
  function dangNhap() {
    dangDangNhap = true; datMsg("dn", "", ""); ve();
    api("dang-nhap", {}).then(function (r) {
      if (!r || !r.ok) { dangDangNhap = false; datMsg("dn", (r && r.error) || "Chưa mở được đăng nhập.", "loi"); ve(); return; }
      var w = null; try { w = W.open(r.url, "_blank"); } catch (e) { w = null; }
      datMsg("dn", w ? "Đã mở trang Google. Chọn tài khoản và bấm Cho phép, xong quay lại đây." : "", "ok");
      if (!w) msg.dn = { t: "", loai: "ok", link: r.url };
      ve();
      if (!w) { var m = root.querySelector('[data-kd="dang-nhap"]'); if (m) m.insertAdjacentHTML("afterend", ' <a href="' + esc(r.url) + '" target="_blank" rel="noopener">Bấm vào đây để mở trang Google</a>'); }
      var t0 = Date.now();
      clearInterval(dnTimer);
      dnTimer = setInterval(function () {
        if (Date.now() - t0 > 5 * 60 * 1000) { clearInterval(dnTimer); dangDangNhap = false; datMsg("dn", "Hết giờ chờ. Bấm Đăng nhập Google Drive để làm lại.", "loi"); ve(); return; }
        api("dang-nhap-xem").then(function (x) {
          if (!x || !x.ok) return;
          if (x.ket_qua === "ok" || x.buoc === "da_ket_noi") { clearInterval(dnTimer); dangDangNhap = false; datMsg("dn", "", ""); lam(); }
          else if (x.ket_qua === "that_bai" || x.ket_qua === "het_gio") { clearInterval(dnTimer); dangDangNhap = false; datMsg("dn", "Google chưa trả mã về (có thể anh bấm Hủy hoặc khóa chưa đúng loại Desktop app). Thử lại.", "loi"); ve(); }
        });
      }, 2000);
    });
  }

  // ---------------------------------------------------------------- sự kiện
  function click(e) {
    var b = e.target.closest && e.target.closest("[data-kd]");
    if (!b || b.disabled || b.tagName === "SELECT" || b.type === "checkbox") return;
    var a = b.getAttribute("data-kd");
    if (a === "nho") nhoTuDong();
    else if (a === "mo-form") { moForm = !moForm; if (moForm) moHd = true; ve(); }
    else if (a === "luu-khoa") {
      var cid = (D.getElementById("kdCid") || {}).value || "", cs = (D.getElementById("kdCs") || {}).value || "", m = D.getElementById("kdKhoaMsg");
      if (m) m.textContent = "";
      b.disabled = true;
      api("client", { client_id: cid, client_secret: cs }).then(function (r) {
        b.disabled = false;
        if (r && r.ok) { var s = D.getElementById("kdCs"); if (s) s.value = ""; moForm = false; lam().then(function () { if (st.buoc === "chua_dang_nhap") dangNhap(); }); }
        else if (m) m.textContent = (r && r.error) || "Chưa cất được khóa.";
      });
    } else if (a === "dang-nhap") dangNhap();
    else if (a === "ngat") { if (W.confirm("Ngắt kết nối Google Drive? Tệp đã chép về kho và tệp đã tải lên Drive vẫn giữ nguyên.")) api("ngat", {}).then(function () { st = null; dauVan = ""; lam(); }); }
    else if (a === "chon") moChon(b.getAttribute("data-vt"));
    else if (a === "chay") {
      var v = b.getAttribute("data-v");
      api("chay", { viec: v }).then(function (r) { if (r && r.ok) { st = r; datMsg(v, "Đã gửi lệnh, cầu nối sẽ chạy trong vài giây.", "ok"); ve(); lam(); } else { datMsg(v, (r && r.error) || "Chưa gửi được lệnh.", "loi"); ve(); } });
    }
  }
  function doi(e) {
    var t = e.target, a = t.getAttribute && t.getAttribute("data-kd");
    if (!a) return;
    var body = null;
    if (a === "tu-ve") body = { tu_ve: t.checked };
    else if (a === "tu-len") body = { tu_len: t.checked };
    else if (a === "chu-ky") body = { ve_moi_phut: Number(t.value) };
    else if (a === "gioi-han") body = { gioi_han_mb: Number(t.value) };
    if (body) api("cai-dat", body).then(function (r) { if (r && r.ok) { st = r; ve(); } });
  }

  // ---------------------------------------------------------------- gắn vào trang Kho tư liệu và sắp lại bố cục
  function mount() {
    view = D.querySelector('[data-view="kho"]');
    if (!view || D.getElementById("kdDrive")) return !!root;
    css();
    var dau = view.querySelector(".page-head");
    var sub = view.querySelector(".page-head .sub");
    if (sub) sub.textContent = "Ảnh, video B-roll, nhạc, hiệu ứng, nền và logo của doanh nghiệp. Đội AI vào đây lấy tư liệu thật để đăng bài, dựng clip, thiết kế. Có ba cách đưa tư liệu vào: nối Google Drive, tải từ máy tính, hoặc liên kết thư mục có sẵn trên máy.";
    root = D.createElement("section"); root.id = "kdDrive"; root.className = "card";
    (dau ? dau.insertAdjacentElement("afterend", root) : view.insertBefore(root, view.firstChild));
    var tai = view.querySelector(".kho-drop");
    if (tai && !view.querySelector(".kd-sec")) {
      var h = D.createElement("div"); h.className = "kd-sec";
      h.innerHTML = "<b>Tải từ máy tính và thư mục trên máy</b><small>Kéo thả tệp vào đây, hoặc cho đội đọc thẳng một thư mục có sẵn trên máy</small>";
      tai.parentNode.insertBefore(h, tai);
    }
    root.addEventListener("click", click);
    root.addEventListener("change", doi);
    ve();
    new MutationObserver(function () { if (!view.hidden) lam(); }).observe(view, { attributes: true, attributeFilter: ["hidden"] });
    if (!view.hidden) lam();
    return true;
  }

  function khoiDong() {
    if (mount()) return;
    var n = 0, iv = setInterval(function () { if (mount() || ++n > 40) clearInterval(iv); }, 500);
  }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", khoiDong); else khoiDong();
  W.TISAKhoDrive = { lam: lam };
})();
