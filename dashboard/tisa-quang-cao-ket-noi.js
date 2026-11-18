/* tisa-quang-cao-ket-noi.js - phần "Tài khoản và kết nối" mở rộng (V2.78): tính năng nào cần gì để dùng, báo cáo tự động,
   hướng dẫn từng bước kết nối từng nền tảng, nút nhờ TISA BOT làm giúp (V3.02: tự thao tác, không dùng Claude), nhật ký thao tác.
   Mã truy cập và mật khẩu KHÔNG bao giờ đi qua khung chat: AI dừng cho anh tự đăng nhập và dán mã thẳng vào ô bằng lệnh dán kín. */
(function () {
  "use strict";
  var Q = window.TisaQC, esc = Q.esc, api = Q.api;
  var NEN = { facebook: "Facebook / Meta", tiktok: "TikTok", google: "Google Ads" };
  var goc = null, KN = {}, TK = [], NK = [], BC = "", BCky = "7-ngay";

  /* ---------- hướng dẫn từng bước ---------- */
  var HD = {
    facebook_api: { ten: "Facebook: lấy mã truy cập bằng API (khuyên dùng)", nen: "facebook", thoi_gian: "khoảng 15 phút", buoc: [
      "Mở <b>business.facebook.com</b> và đăng nhập bằng tài khoản quản trị doanh nghiệp. Chưa có Business Manager thì bấm <b>Tạo tài khoản</b> và làm theo hướng dẫn.",
      "Bấm biểu tượng bánh răng <b>Cài đặt doanh nghiệp</b> (Business Settings).",
      "Vào <b>Tài khoản &gt; Tài khoản quảng cáo</b>, chọn tài khoản cần dùng. Ghi lại <b>mã tài khoản quảng cáo</b> (dãy số ở đầu trang, ví dụ 1234567890). Chưa có thì bấm <b>Thêm</b> để tạo hoặc thêm tài khoản có sẵn.",
      "Vào <b>Người dùng &gt; Người dùng hệ thống &gt; Thêm</b>. Đặt tên <b>TISA BOT</b>. Vai trò: <b>Quản trị viên</b> nếu muốn cho phép bật tắt, đổi ngân sách; <b>Nhân viên</b> nếu chỉ xem số liệu.",
      "Chọn người dùng vừa tạo, bấm <b>Thêm tài sản &gt; Tài khoản quảng cáo</b>, chọn đúng tài khoản. Bật quyền <b>Quản lý chiến dịch</b> (để bật tắt, đổi ngân sách) hoặc chỉ <b>Xem hiệu quả</b> (chỉ xem). Bấm Lưu.",
      "Cần một ứng dụng Meta. Vào <b>developers.facebook.com &gt; Ứng dụng của tôi &gt; Tạo ứng dụng</b>, chọn loại <b>Doanh nghiệp</b>. Sau đó trong Cài đặt doanh nghiệp vào <b>Tài khoản &gt; Ứng dụng &gt; Thêm</b> để gắn ứng dụng vào doanh nghiệp. Đã có ứng dụng thì chỉ cần kiểm tra nó đã được gắn.",
      "Quay lại <b>Người dùng hệ thống</b>, chọn TISA BOT, bấm <b>Tạo mã</b>. Chọn ứng dụng, đặt <b>Hết hạn: Không bao giờ</b>, tick quyền <b>ads_read</b> (xem số liệu) và <b>ads_management</b> (bật tắt, đổi ngân sách). Bấm Tạo mã.",
      "Bấm <b>Sao chép</b> mã. Mã chỉ hiện một lần. Đừng gửi cho ai và đừng dán vào khung chat.",
      "Quay lại TISA BOT, tab <b>Kết nối</b>, ở thẻ <b>Facebook / Meta</b> bấm <b>Tôi đã có mã</b>, dán mã tài khoản và mã truy cập, bấm <b>Lưu và kiểm tra</b>. Thấy <b>● Nối được</b> là xong.",
      "Muốn bật tắt, đổi ngân sách: chỉ cần ra lệnh trong chat hoặc bấm nút trong bảng, làm ngay, không cần công tắc hay mã."],
      luu_y: "Báo thiếu quyền thì kiểm tra lại bước 5 và bước 7. Mã hết hạn thì tạo mã mới ở bước 7 rồi nhập lại." },
    facebook_mcp: { ten: "Facebook: nối Meta Ads MCP chính chủ (không cần tự tạo mã)", nen: "facebook", thoi_gian: "khoảng 5 phút", buoc: [
      "Bấm <b>Mở trang Kết nối</b> ở cuối khung Nền tảng quảng cáo (hoặc vào menu <b>Kết nối</b> bên trái).",
      "Tìm thẻ <b>Meta Ads</b> (MCP chính chủ của Meta), bấm <b>Kết nối</b> hoặc <b>Cài</b>.",
      "Cửa sổ đăng nhập Facebook mở ra. Đăng nhập, chọn doanh nghiệp và tài khoản quảng cáo cho phép TISA BOT truy cập, bấm <b>Cho phép</b>.",
      "Quay lại, thẻ hiện đèn xanh. Trang này tự nhận trong khoảng 15 giây (hiện ở thẻ Facebook / Meta).",
      "Dùng: hỏi trợ lý bằng tiếng Việt ở ô <b>Hỏi trợ lý</b> trên tab Tổng quan. Kết nối này mặc định chỉ đọc số liệu; việc tạo, bật quảng cáo luôn chờ anh duyệt."],
      luu_y: "TISA BOT chưa kiểm chứng trọn đường nối này với mọi tài khoản. Nếu bấm Kết nối vẫn báo lỗi thì dùng cách API ở trên, hoặc bấm Nhờ TISA BOT làm giúp." },
    mcp_khac: { ten: "Nối một kết nối MCP quảng cáo khác (TikTok, Google Ads, công cụ riêng)", nen: "facebook", thoi_gian: "khoảng 5 đến 10 phút", buoc: [
      "Bấm <b>Mở trang Kết nối</b> ở cuối khung Nền tảng quảng cáo (hoặc vào menu <b>Kết nối</b> bên trái TISA BOT).",
      "Tìm trong danh mục kết nối nền tảng quảng cáo anh dùng (ví dụ TikTok Ads, Google Ads). Thấy thẻ phù hợp thì bấm <b>Kết nối</b> và đăng nhập khi được hỏi.",
      "Không thấy thẻ phù hợp: bấm <b>Thêm kết nối riêng</b>, dán địa chỉ MCP (dạng https://...) mà nhà cung cấp đưa cho anh, đặt tên dễ nhớ rồi lưu.",
      "Bật kết nối, chờ đèn xanh <b>Nối được</b>. Trang này tự nhận trong khoảng 15 giây, hiện ở thẻ nền tảng tương ứng.",
      "Nên chọn quyền <b>chỉ đọc</b> trước. Khi cần tạo hoặc sửa quảng cáo thì nâng quyền sau, và luôn kiểm tra kỹ rồi mới duyệt."],
      luu_y: "Chỉ nối kết nối do chính nhà cung cấp quảng cáo hoặc người anh tin tưởng đưa. Không dán mã truy cập vào khung chat." },
    tiktok: { ten: "TikTok: lấy Advertiser ID và Access Token", nen: "tiktok", thoi_gian: "30 phút đến vài ngày (chờ TikTok duyệt ứng dụng)", buoc: [
      "Mở <b>business-api.tiktok.com</b> (TikTok API for Business), đăng nhập bằng tài khoản quản trị tài khoản quảng cáo.",
      "Vào <b>My Apps &gt; Create an App</b>. Tên <b>TISA BOT</b>, ghi mô tả ngắn, chọn quyền (Scope) <b>Ads Management</b> và <b>Reporting</b>. Ô Redirect URL điền <b>https://localhost</b>. Gửi duyệt, chờ TikTok duyệt (có thể mất vài ngày).",
      "Khi được duyệt, mở <b>Advertiser authorization URL</b> của ứng dụng, đăng nhập, chọn các tài khoản nhà quảng cáo cho phép, bấm <b>Confirm</b>. TikTok chuyển về địa chỉ Redirect kèm <b>auth_code</b> trên thanh địa chỉ.",
      "Đổi <b>auth_code</b> lấy <b>Access Token</b> (mã dài hạn): dùng mục <b>Get access token</b> trong trang ứng dụng, hoặc bấm nút Nhờ TISA BOT bên dưới để AI hướng dẫn từng bước.",
      "Lấy <b>Advertiser ID</b> (mã nhà quảng cáo): ở góc trên TikTok Ads Manager, hoặc trong màn hình kết quả ở bước 3.",
      "Quay lại TISA BOT, tab <b>Kết nối</b>, ở thẻ <b>TikTok</b> bấm <b>Tôi đã có mã</b>, dán Advertiser ID và Access Token, bấm <b>Lưu và kiểm tra</b>.",
      "Muốn bật tắt: chỉ cần ra lệnh trong chat hoặc bấm nút trong bảng, làm ngay."],
      luu_y: "Chưa được duyệt ứng dụng thì chưa lấy được mã. Trong lúc chờ có thể dùng Meta hoặc Google trước." },
    google: { ten: "Google Ads: Developer token, OAuth và Refresh token", nen: "google", thoi_gian: "khoảng 30 phút", buoc: [
      "<b>Developer token</b>: đăng nhập Google Ads bằng tài khoản quản lý (MCC). Vào <b>Công cụ và cài đặt &gt; Thiết lập &gt; Trung tâm API</b>, xin Developer token. Mức Basic là đủ để xem số liệu và thao tác.",
      "Mở <b>console.cloud.google.com</b>, tạo một dự án mới, vào <b>APIs &amp; Services &gt; Library</b>, tìm <b>Google Ads API</b>, bấm <b>Enable</b>.",
      "Vào <b>APIs &amp; Services &gt; Credentials &gt; Create credentials &gt; OAuth client ID</b>, loại <b>Desktop app</b>. Ghi lại <b>Client ID</b> và <b>Client secret</b>. Nếu được hỏi màn hình đồng ý OAuth thì điền tên ứng dụng, thêm email của anh vào Test users.",
      "Lấy <b>Refresh token</b>: mở <b>developers.google.com/oauthplayground</b>, bấm bánh răng, tick <b>Use your own OAuth credentials</b> và dán Client ID, Client secret. Ở Bước 1 nhập scope <b>https://www.googleapis.com/auth/adwords</b>, bấm <b>Authorize APIs</b> và đăng nhập. Ở Bước 2 bấm <b>Exchange authorization code for tokens</b>, sao chép <b>Refresh token</b>.",
      "<b>Customer ID</b>: 10 số ở góc trên bên phải Google Ads của tài khoản cần dùng. Truy cập qua tài khoản quản lý thì ghi thêm mã MCC ở ô tương ứng.",
      "Quay lại TISA BOT, tab <b>Kết nối</b>, ở thẻ <b>Google Ads</b> bấm <b>Tôi đã có mã</b>, dán đủ các mã, bấm <b>Lưu và kiểm tra</b>.",
      "Muốn bật tắt: chỉ cần ra lệnh trong chat hoặc bấm nút trong bảng, làm ngay."],
      luu_y: "Báo phiên bản API hết hạn thì đổi ô Phiên bản (ví dụ v24). Developer token mức Test chỉ chạy với tài khoản thử." }
  };

  /* ---------- lệnh nhờ TISA BOT làm giúp ---------- */
  function lenh(loai) { return loai === "bao_cao" ? "" : lenhTisa(loai); }
  function lenhBaoCao(tanSuat, kenh) {
    return "/ts-lap-lich-tu-dong Cài báo cáo quảng cáo tự động cho anh.\n- Khi chạy: " + tanSuat + ".\n- Việc làm: đọc số liệu quảng cáo của các tài khoản đã nối trong TISA BOT (Facebook, TikTok, Google Ads; dùng kết nối MCP hoặc API đã nối), viết báo cáo ngắn gồm: chi phí, kết quả, giá mỗi kết quả, doanh thu nếu có, so với kỳ trước; chiến dịch tốt nhất và tệ nhất; tối đa 3 việc nên làm.\n- Lưu báo cáo vào bộ não (thư mục output, mỗi báo cáo một thư mục theo ngày) và " + kenh + ".\n- CHỈ ĐỌC số liệu. Không bật, tắt, đổi ngân sách hay tiêu tiền. Việc đó chỉ là gợi ý trong báo cáo để anh quyết.\n- Cài xong cho anh xem lịch đã cài và cách tắt.\n\n" + LUAT;
  }

  /* ---------- vẽ ---------- */
  function trangThai() {
    var rows = [["Xem số liệu và báo cáo", "Một tài khoản nối bằng API hoặc một kết nối MCP quảng cáo", function (n) { var v = KN[n] || {}; return v.ok ? "ok" : v.co ? ((v.api || []).some(function (x) { return !x.da_kiem_tra; }) ? "phan" : "loi") : ""; }],
      ["Bật, tắt, đổi ngân sách (ra lệnh là làm)", "Tài khoản nối bằng API, mã có quyền ghi (Quản lý chiến dịch / ads_management). Không cần công tắc hay mã xác nhận", function (n) { return TK.some(function (t) { return t.nen === n; }) ? "ok" : ""; }],
      ["Tạo quảng cáo (luôn tạm dừng)", "Trợ lý và công cụ quảng cáo của nền tảng (MCP hoặc skill). Anh duyệt rồi mới bật", function (n) { var v = KN[n] || {}; return v.mcp && v.mcp.some(function (x) { return x.ok; }) ? "ok" : (v.ok ? "phan" : ""); }]];
    var h = '<div class="the"><h2>Muốn dùng tính năng nào thì cần gì?</h2><p class="sub">Bảng này tự cập nhật khi anh nối xong. ● là đã đủ, ◐ là dùng được một phần, ○ là chưa.</p><div class="bang-cuon"><table><thead><tr><th class="trai">Tính năng</th><th class="trai">Cần</th>' + Object.keys(NEN).map(function (n) { return "<th>" + NEN[n] + "</th>"; }).join("") + "</tr></thead><tbody>";
    rows.forEach(function (r) { h += '<tr><td class="trai"><b>' + r[0] + '</b></td><td class="trai mo" style="white-space:normal;min-width:240px">' + r[1] + "</td>" + Object.keys(NEN).map(function (n) { var s = r[2](n); return '<td style="text-align:center">' + (s === "ok" ? '<span class="tang">●</span>' : s === "phan" ? '<span class="mo">◐</span>' : s === "loi" ? '<span class="giam">⚠</span>' : '<span class="mo">○</span>') + "</td>"; }).join("") + "</tr>"; });
    // Giải thích vì sao dòng "Bật, tắt, đổi ngân sách" còn trống dù đã nối MCP: dòng này chỉ sáng khi có TÀI KHOẢN API có quyền ghi và công tắc đã bật.
    var gc = Object.keys(NEN).filter(function (n) { var v = KN[n] || {}; return v.mcp && v.mcp.some(function (x) { return x.ok; }) && !TK.some(function (t) { return t.nen === n; }); }).map(function (n) {
      var coApi = TK.some(function (t) { return t.nen === n; });
      return '<div class="canh" style="margin-top:12px;font-size:13.5px"><b>' + NEN[n] + ': muốn ra lệnh bật, tắt, đổi ngân sách?</b> Kết nối MCP hiện chỉ để xem số liệu và tạo quảng cáo (luôn tạm dừng). Để anh ra lệnh trong chat là AI bật, tắt ngay (không cần công tắc, không nhập mã), nối thêm <b>tài khoản bằng API</b> có mã quyền Quản lý chiến dịch (ads_management). Chưa nối thì AI vẫn làm được bằng cách thao tác trên trang quản lý quảng cáo trong Trình duyệt TISA.' +
        ' <button type="button" class="nut cam nho" data-kn-mo="' + (n === "facebook" ? "facebook_api" : n) + '" style="margin-left:6px">Mở hướng dẫn nối API</button></div>';
    }).join("");
    return h + "</tbody></table></div>" + gc + "</div>";
  }
  function huongDan() {
    var h = '<div class="the"><h2>Tự kết nối theo hướng dẫn</h2><p class="sub">Muốn tự làm thì mở từng hướng dẫn. Mỗi hướng dẫn có nút để AI làm giúp anh: AI mở trang, thao tác từng bước, dừng cho anh tự đăng nhập, không bao giờ nhận mật khẩu hay mã bí mật.</p>';
    Object.keys(HD).forEach(function (k) {
      var g = HD[k];
      h += '<details class="tk-hd" data-hd="' + k + '"><summary><i class="cham nen-' + g.nen + '"></i><b>' + g.ten + '</b> <span class="mo">· ' + g.thoi_gian + '</span></summary><ol class="tk-buoc">' + g.buoc.map(function (b) { return "<li>" + b + "</li>"; }).join("") + "</ol>" +
        '<div class="canh" style="font-size:13px">' + esc(g.luu_y) + '</div><div class="hang"><button type="button" class="nut cam nho" data-kn-hoi="' + k + '">🤖 Nhờ AI làm</button><span class="mo" style="font-size:12.5px">TISA BOT tự thao tác trong khung chat, anh chỉ cần đăng nhập và bấm Cho phép khi được nhờ.</span></div></details>';
    });
    return h + "</div>";
  }
  function baoCao() {
    var h = '<div class="the"><h2>Báo cáo quảng cáo</h2><p class="sub">Soạn báo cáo bằng chữ từ số liệu thật ngay bây giờ, hoặc cài để báo cáo tự chạy mỗi ngày, mỗi tuần.</p>' +
      '<h3>Soạn báo cáo ngay</h3><div class="hang"><select id="bcKy"><option value="hom-qua">Hôm qua</option><option value="7-ngay" selected>7 ngày qua</option><option value="30-ngay">30 ngày qua</option><option value="thang-nay">Tháng này</option><option value="thang-truoc">Tháng trước</option></select>' +
      '<button type="button" class="nut nho" data-kn-bc>📝 Soạn báo cáo</button><span class="mo" id="bcTt"></span></div>';
    if (BC) h += '<div class="bc-hop"><pre class="bc-chu" id="bcChu">' + esc(BC) + '</pre><div class="hang"><button type="button" class="nut phu nho" data-kn-bc-chep>Chép</button><button type="button" class="nut phu nho" data-kn-bc-chat>Hỏi AI về báo cáo này</button></div></div>';
    h += '<h3 style="margin-top:16px">Cài báo cáo tự động</h3><div class="cot2"><label class="truong">Chạy khi nào<select id="bcLich"><option value="mỗi ngày lúc 21:00">Mỗi ngày 21:00 (tổng kết ngày)</option><option value="mỗi sáng thứ Hai lúc 08:00 (tổng kết tuần trước)">Thứ Hai hàng tuần 08:00</option><option value="ngày 1 hàng tháng lúc 08:00 (tổng kết tháng trước)">Ngày 1 hàng tháng 08:00</option><option value="mỗi ngày lúc 09:00 (tổng kết hôm qua)">Mỗi ngày 09:00 (tổng kết hôm qua)</option></select></label>' +
      '<label class="truong">Báo cho anh ở đâu<select id="bcKenh"><option value="báo tóm tắt trong TISA BOT">Trong TISA BOT</option><option value="gửi tóm tắt qua Zalo của anh (nếu đã nối Zalo)">Zalo</option><option value="gửi tóm tắt qua Telegram của anh (nếu đã nối Telegram)">Telegram</option></select></label></div>' +
      '<div class="hang" style="margin-top:8px"><button type="button" class="nut cam nho" data-kn-lich>🗓 Dán lệnh nhờ trợ lý cài báo cáo tự động</button><span class="mo" style="font-size:12.5px">Báo cáo chỉ đọc số liệu, không tự bật, tắt hay đổi ngân sách.</span></div></div>';
    return h;
  }
  function nhatKy() {
    var h = '<details class="the pa-gap"><summary><b>Nhật ký thao tác</b><span class="mo">· ' + (NK.length ? NK.length + " việc gần đây" : "chưa có") + '</span></summary><p class="sub">Mọi lần bật, tắt, đổi ngân sách từ trang này đều ghi lại tại đây.</p>';
    if (!NK.length) return h + '<div class="trong">Chưa có thao tác nào.</div></details>';
    h += '<div class="bang-cuon"><table><thead><tr><th class="trai">Lúc</th><th class="trai">Tài khoản</th><th class="trai">Việc</th><th class="trai">Kết quả</th></tr></thead><tbody>' + NK.slice(0, 15).map(function (x) {
      return '<tr><td class="trai">' + esc(x.luc) + '</td><td class="trai">' + esc(x.tk || "") + '</td><td class="trai" style="white-space:normal;min-width:260px">' + esc(x.viec || "") + '</td><td class="trai" style="white-space:normal">' + esc(x.ket_qua || "") + "</td></tr>"; }).join("") + "</tbody></table></div>";
    return h + "</details>";
  }
  function ve() {
    if (!goc) return;
    goc.innerHTML = baoCao() + huongDan() + nhatKy();   // bảng "tính năng nào cần gì" đã thay bằng 3 thẻ nền tảng
  }
  async function nap() {
    var a = await api("/tisa-quang-cao/api/ket-noi"), b = await api("/tisa-quang-cao/api/tai-khoan"), c = await api("/tisa-quang-cao/api/thao-tac/nhat-ky");
    KN = (a && a.ket_noi) || {}; TK = (b && b.tai_khoan) || []; NK = (c && c.nhat_ky) || [];
    ve();
  }

  function gan(el) {
    if (goc === el) return;
    goc = el;
    el.addEventListener("click", async function (e) {
      var t = e.target, x;
      if ((x = t.closest("[data-kn-mo]"))) { var dt = goc.querySelector('details[data-hd="' + x.dataset.knMo + '"]'); if (dt) { dt.open = true; dt.scrollIntoView({ behavior: "smooth", block: "center" }); } return; }
      if ((x = t.closest("[data-kn-hoi]"))) { Q.nho(lenh(x.dataset.knHoi), (HD[x.dataset.knHoi] || {}).ten); return; }
      if (t.closest("[data-kn-lich]")) { Q.hoi(lenhBaoCao(goc.querySelector("#bcLich").value, goc.querySelector("#bcKenh").value)); return; }
      if (t.closest("[data-kn-bc]")) {
        var tt = goc.querySelector("#bcTt"); BCky = goc.querySelector("#bcKy").value; tt.textContent = "AI đang soạn báo cáo (khoảng 20 giây)...";
        var j = await api("/tisa-quang-cao/api/ai/bao-cao", { kieu: BCky });
        if (!j.ok) { tt.textContent = j.error || "Chưa soạn được."; return; }
        BC = j.bao_cao; ve(); goc.querySelector("#bcKy").value = BCky; return; }
      if (t.closest("[data-kn-bc-chep]")) { try { await navigator.clipboard.writeText(BC); Q.toast("Đã chép báo cáo."); } catch (er) { Q.toast("Trình duyệt chưa cho chép."); } return; }
      if (t.closest("[data-kn-bc-chat]")) { (Q.tuVan || Q.hoi)("Đây là báo cáo quảng cáo vừa soạn. Giải thích kỹ hơn và đề xuất cụ thể từng việc nên làm (chỉ gợi ý):\n\n" + BC); return; }
    });
    nap();
  }

  /* ---------- NHỜ TISA BOT làm giúp ----------
     TISA BOT tự thao tác phần làm được bằng trình duyệt và máy tính của anh, dừng đúng chỗ anh phải tự làm
     (đăng nhập, mã xác thực, đồng ý điều khoản). Mã truy cập KHÔNG đi qua khung chat. */
  var NHO = {
    facebook_api: {
      muc_tieu: "lấy MÃ TÀI KHOẢN QUẢNG CÁO và MÃ TRUY CẬP của Facebook / Meta (tạo Người dùng hệ thống TISA BOT trong Business Manager) để dán vào TISA BOT",
      claude: ["Mở business.facebook.com, đi tới Cài đặt doanh nghiệp, tìm và đọc ra mã tài khoản quảng cáo (dãy số, không phải bí mật)", "Tạo Người dùng hệ thống tên TISA BOT, gán đúng tài khoản quảng cáo và quyền (chỉ xem hoặc quản lý chiến dịch theo anh chọn)", "Mở màn hình Tạo mã, chọn ứng dụng, đặt hết hạn Không bao giờ, tích quyền ads_read (và ads_management nếu anh muốn bật tắt)", "Mở sẵn trang TISA BOT chỗ dán mã và chỉ cho anh ô cần dán"],
      anh: ["ĐĂNG NHẬP Facebook (mật khẩu, mã xác thực 2 lớp). AI sẽ dừng lại chờ anh", "Trả lời AI: muốn CHỈ XEM số liệu hay cho cả BẬT TẮT, ĐỔI NGÂN SÁCH", "Nếu Facebook hỏi xác minh danh tính hoặc nhập lại mật khẩu khi tạo mã thì tự nhập", "Khi mã hiện ra: TỰ bấm nút Sao chép (mã chỉ hiện một lần, đừng đọc cho AI, đừng dán vào khung chat)", "TỰ dán mã vào ô Mã truy cập trong TISA BOT, rồi bấm Lưu và kiểm tra"],
      quyen: "ads_read; chỉ thêm ads_management khi anh nói muốn bật, tắt, đổi ngân sách"
    },
    facebook_mcp: {
      muc_tieu: "nối kết nối Meta Ads MCP chính chủ vào TISA BOT (không cần tự tạo mã)",
      claude: ["Mở trang Kết nối trong TISA BOT (menu Kết nối bên trái)", "Tìm thẻ Meta Ads, bấm Kết nối hoặc Cài", "Theo dõi cửa sổ đăng nhập Facebook mở ra và báo cho anh"],
      anh: ["ĐĂNG NHẬP Facebook trong cửa sổ hiện ra (mật khẩu, mã xác thực 2 lớp)", "CHỌN doanh nghiệp và tài khoản quảng cáo cho phép TISA BOT truy cập", "TỰ bấm nút Cho phép (Allow) ở màn hình xin quyền. AI không bấm đồng ý quyền thay anh"],
      quyen: "chỉ đọc số liệu"
    },
    mcp_khac: {
      muc_tieu: "nối một kết nối MCP quảng cáo khác (TikTok Ads, Google Ads hoặc công cụ riêng) vào TISA BOT",
      claude: ["Mở trang Kết nối trong TISA BOT và tìm thẻ nền tảng anh cần", "Nếu có thẻ: bấm Kết nối. Nếu không có: bấm Thêm kết nối riêng, điền tên dễ nhớ và địa chỉ MCP anh đưa", "Bật kết nối và chờ đèn xanh Nối được"],
      anh: ["ĐƯA cho AI địa chỉ MCP (dạng https://...) của nhà cung cấp nếu phải thêm kết nối riêng", "ĐĂNG NHẬP nền tảng khi được hỏi và bấm Cho phép", "Nếu nền tảng đưa mã hoặc khoá bí mật thì TỰ dán vào ô, không đưa cho AI"],
      quyen: "chỉ đọc số liệu trước, nâng quyền sau"
    },
    tiktok: {
      muc_tieu: "lấy ADVERTISER ID và ACCESS TOKEN của TikTok (TikTok API for Business) để dán vào TISA BOT",
      claude: ["Mở business-api.tiktok.com, vào My Apps > Create an App", "Điền tên TISA BOT, mô tả ngắn, chọn quyền Ads Management và Reporting, điền Redirect URL https://localhost", "Khi ứng dụng được duyệt: mở đường dẫn xác thực nhà quảng cáo, hướng dẫn anh chọn tài khoản", "Chỉ cho anh chỗ lấy Advertiser ID và cách đổi auth_code lấy Access Token"],
      anh: ["ĐĂNG NHẬP TikTok bằng tài khoản quản trị nhà quảng cáo", "BẤM GỬI DUYỆT ứng dụng và CHỜ TikTok duyệt (vài giờ đến vài ngày, không ai rút ngắn được). Duyệt xong anh quay lại nói với AI để làm tiếp", "TỰ bấm Confirm cho phép các tài khoản nhà quảng cáo", "TỰ sao chép Access Token (đừng đọc cho AI), TỰ dán Advertiser ID và Access Token vào TISA BOT rồi bấm Lưu và kiểm tra"],
      quyen: "Ads Management và Reporting"
    },
    google: {
      muc_tieu: "lấy DEVELOPER TOKEN, CLIENT ID, CLIENT SECRET, REFRESH TOKEN và CUSTOMER ID của Google Ads để dán vào TISA BOT",
      claude: ["Mở console.cloud.google.com, tạo dự án mới, bật Google Ads API", "Tạo OAuth client ID loại Desktop app, ghi tên TISA BOT", "Mở developers.google.com/oauthplayground, cấu hình dùng thông tin OAuth riêng, nhập scope https://www.googleapis.com/auth/adwords", "Chỉ cho anh chỗ xem Customer ID (10 số) ở góc trên bên phải Google Ads"],
      anh: ["ĐĂNG NHẬP Google (tài khoản quản lý MCC) kèm xác thực 2 lớp", "TỰ xin Developer token trong Google Ads (Công cụ và cài đặt > Trung tâm API) và chờ Google duyệt nếu cần", "TỰ điền màn hình đồng ý OAuth và thêm email của anh vào Test users", "TỰ bấm Authorize APIs rồi đăng nhập ở Playground", "TỰ sao chép Client secret và Refresh token (đừng đọc cho AI), TỰ dán vào TISA BOT rồi bấm Lưu và kiểm tra"],
      quyen: "scope adwords"
    }
  };
  function lenhTisa(k) {
    var n = NHO[k], h = HD[k]; if (!n || !h) return "";
    var mcp = k === "facebook_mcp" || k === "mcp_khac";
    return "Dùng skill dq-ho-tro-ket-noi: giúp anh làm việc này trên máy anh, làm luôn từng bước.\n\n" +
      "MỤC TIÊU: " + n.muc_tieu + ".\n" +
      "NƠI DÁN MÃ: TISA BOT > Quảng Cáo > tab Kết nối" + (mcp ? " (hoặc trang Kết nối)" : " > thẻ của nền tảng > bấm \"Tôi đã có mã\" để hiện các ô dán") + ". Việc trong TISA BOT làm bằng tisa_browser_do op=ui_tisa (không mở TISA BOT trong trình duyệt, không bắt anh đăng nhập lại TISA BOT).\n\n" +
      "CÁCH LÀM:\n- Dùng đúng trình duyệt đã chọn cho AI. Mở mỗi trang mới trong một tab mới, làm tuần tự, xong mỗi bước báo thật ngắn: đã làm gì, bước kế là gì.\n" +
      "- PHẦN CỦA EM (tự thao tác):\n" + n.claude.map(function (x) { return "  + " + x; }).join("\n") + "\n" +
      "- ĐIỂM DỪNG, PHẦN ANH TỰ LÀM. Tới đúng chỗ này em DỪNG, nói rõ bằng một câu ngắn anh cần làm gì ở đâu (wait_user), rồi làm tiếp khi anh báo xong:\n" + n.anh.map(function (x) { return "  * " + x; }).join("\n") + "\n\n" +
      "CÁC BƯỚC CHI TIẾT (tham khảo):\n" + h.buoc.map(function (b, i) { return (i + 1) + ". " + b.replace(/<[^>]+>/g, "").replace(/&gt;/g, ">").replace(/&amp;/g, "&"); }).join("\n") + "\n\n" +
      "QUY TẮC AN TOÀN, KHÔNG ĐƯỢC PHÁ:\n- Không nhập hộ mật khẩu, mã xác thực, OTP, số thẻ. Gặp CAPTCHA hoặc hộp thoại bảo mật thì dừng và nhờ anh.\n" +
      "- Mã truy cập, khoá bí mật: KHÔNG đọc ra, KHÔNG ghi vào chat, ghi chú hay bộ nhớ. Chỉ chuyển thẳng từ trang nền tảng vào ô của TISA BOT bằng tisa_browser_do op=dan_vao_tisa.\n" +
      "- Không bấm thanh toán, đăng bài, bật quảng cáo, xoá. Chỉ xin quyền tối thiểu cần thiết: " + n.quyen + ".\n" +
      "- LƯU Ý: " + h.luu_y + "\n\n" +
      "KẾT THÚC: dán xong thì bấm Lưu và kiểm tra, đọc kết quả rồi báo anh một câu. Nếu báo lỗi, đọc lỗi trên màn hình và sửa đúng bước đó.";
  }
  /* ---------- nút "Nhờ TISA BOT làm giúp" và "Hướng dẫn" dùng ở mọi nơi trong trang ---------- */
  function hdNut(k) {
    return '<button type="button" class="nut cam nho" data-hd-nho="' + k + '">🤖 Nhờ AI làm</button><button type="button" class="nut phu nho" data-hd-xem="' + k + '">📖 Hướng dẫn</button>';
  }
  function hdModal(k) {
    var g = HD[k]; if (!g) return;
    var cu = document.getElementById("hdNen"); if (cu) cu.remove();
    var el = document.createElement("div"); el.id = "hdNen"; el.className = "hd-nen"; el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); el.setAttribute("aria-labelledby", "hdTd");
    el.innerHTML = '<div class="hd-hop"><div class="hang" style="justify-content:space-between;align-items:flex-start"><div><h3 id="hdTd" style="margin:0">' + esc(g.ten) + '</h3><div class="mo" style="font-size:13px">Thời gian làm: ' + esc(g.thoi_gian) + '. Làm lần lượt từ bước 1.</div></div><button type="button" class="nut phu nho" data-hd-dong aria-label="Đóng">✕</button></div>' +
      '<ol class="tk-buoc hd-ds">' + g.buoc.map(function (b) { return "<li>" + b + "</li>"; }).join("") + "</ol>" +
      '<div class="canh" style="font-size:13px;margin-top:8px"><b>Lưu ý:</b> ' + esc(g.luu_y) + '</div>' +
      '<div class="hd-chan"><button type="button" class="nut cam nho" data-hd-nho="' + k + '">🤖 Nhờ AI làm</button><button type="button" class="nut phu nho" data-hd-dong>Đóng</button></div></div>';
    document.body.appendChild(el);
    var nut = el.querySelector("[data-hd-dong]"); if (nut) nut.focus();
  }
  document.addEventListener("click", async function (e) {
    var t = e.target, x;
    if ((x = t.closest("[data-hd-xem]"))) { hdModal(x.dataset.hdXem); return; }
    if ((x = t.closest("[data-hd-nho]"))) { var m0 = document.getElementById("hdNen"); if (m0) m0.remove(); Q.nho(lenhTisa(x.dataset.hdNho), (HD[x.dataset.hdNho] || {}).ten); return; }
    if (t.closest("[data-hd-dong]") || t.classList.contains("hd-nen")) { var m = document.getElementById("hdNen"); if (m) m.remove(); }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { var m = document.getElementById("hdNen"); if (m) m.remove(); } });
  window.TisaKetNoi = { gan: gan, nap: nap, nut: hdNut };
})();
