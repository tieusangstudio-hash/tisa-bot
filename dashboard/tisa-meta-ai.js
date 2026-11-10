/* tisa-meta-ai.js - nút "Tạo prompt cho Claude làm giúp" trong hộp Kết nối Meta (V2.75, chủ chốt 10/11/2026).

   Phần mất thời gian nhất khi nối Fanpage là bấm trên developers.facebook.com: tạo app, thêm Messenger và 4 quyền,
   dán Địa chỉ quay về và link chính sách. Nút này soạn sẵn một prompt có đúng hai địa chỉ của máy này để học viên dán
   vào Claude trên Chrome (Chrome đã đăng nhập Facebook): Claude bấm giúp các bước đó.

   Prompt dặn Claude dừng ở 4 chỗ chỉ chủ tài khoản được làm: mã OTP, mật khẩu Facebook, App secret (chìa khoá Fanpage,
   AI không đọc, không chép) và bấm đồng ý cấp quyền. Bật Live phải hỏi trước. Prompt không chứa bí mật nào của máy này:
   chỉ hai địa chỉ công khai mà hộp Kết nối Meta vốn đã hiện. */
(function () {
  "use strict";

  function esc(t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Hai địa chỉ công khai của máy này, đọc từ chính các ô "Chép" của hộp (Địa chỉ quay về, Link chính sách).
  function diaChi(form) {
    var o = form.querySelectorAll(".msc-copy input");
    var quayVe = o[0] ? o[0].value : "", chinhSach = o[1] ? o[1].value : "";
    if (!quayVe) quayVe = location.origin + "/messenger/oauth/callback";
    if (!chinhSach) chinhSach = location.origin + "/messenger/privacy";
    return { quayVe: quayVe, chinhSach: chinhSach };
  }

  function soanPrompt(d) {
    return [
      "Bạn đang giúp tôi nối Fanpage Facebook vào TISA BOT để bot tự trả lời tin nhắn và bình luận.",
      "Tôi đã đăng nhập Facebook trên Chrome bằng tài khoản quản trị viên Fanpage.",
      "Làm trên https://developers.facebook.com, bấm từng bước, chụp màn hình kiểm tra sau mỗi bước, giao diện tiếng Việt hay tiếng Anh đều được.",
      "",
      "THÔNG TIN CỦA TÔI (dán đúng từng ký tự):",
      "- Địa chỉ quay về: " + d.quayVe,
      "- Link chính sách quyền riêng tư: " + d.chinhSach,
      "- Tên app: lấy tên Fanpage của tôi, thêm chữ Bot (hỏi tôi nếu tôi có nhiều Fanpage).",
      "",
      "LUẬT AN TOÀN, BẮT BUỘC:",
      "- KHÔNG gõ mật khẩu, mã OTP, mã xác minh. Gặp thì dừng, nhờ tôi tự gõ rồi làm tiếp.",
      "- KHÔNG bấm \"Hiển thị\" App secret, KHÔNG đọc, KHÔNG chép App secret.",
      "- KHÔNG bấm đồng ý cấp quyền thay tôi.",
      "- KHÔNG gạt app sang Live khi chưa hỏi tôi.",
      "- Ngoài các bước dưới đây thì không đổi gì khác trong tài khoản Facebook của tôi.",
      "",
      "CÁC BƯỚC:",
      "1. Vào \"Ứng dụng của tôi\" (My Apps). Nếu đã có app dùng cho Fanpage này thì dùng lại, báo tôi tên app.",
      "   Chưa có thì bấm \"Tạo ứng dụng\", đặt tên như trên, điền email của tài khoản, chọn trường hợp sử dụng",
      "   \"Tương tác với khách hàng trên Messenger from Meta\" (Engage with customers on Messenger from Meta),",
      "   chọn Business portfolio đang quản lý Fanpage (không có thì chọn chưa kết nối), bấm Tạo. Meta hỏi mật khẩu thì dừng chờ tôi.",
      "2. Mục \"Trường hợp sử dụng\" (Use cases): đảm bảo có Messenger. Ở dòng \"Quản lý mọi thứ trên Trang\" bấm Tùy chỉnh,",
      "   thêm 4 quyền: pages_read_engagement, pages_read_user_content, pages_manage_engagement, pages_manage_posts.",
      "   Hộp hỏi ảnh hưởng trường hợp khác thì bấm Add. Kiểm tra các quyền đều hiện \"Sẵn sàng thử nghiệm\" (Ready for testing).",
      "3. Mục \"Facebook Login\" (Facebook Login for Business) → Cài đặt: bật \"Đăng nhập OAuth ứng dụng khách\" và \"Đăng nhập OAuth trên web\",",
      "   dán Địa chỉ quay về vào ô \"URI chuyển hướng OAuth hợp lệ\" (Valid OAuth Redirect URIs), bấm Lưu thay đổi.",
      "   Chưa có mục này thì thêm sản phẩm / trường hợp sử dụng Facebook Login trước.",
      "4. \"Cài đặt ứng dụng\" → \"Thông tin cơ bản\" (App settings → Basic): dán Link chính sách vào \"URL chính sách quyền riêng tư\"",
      "   và \"Hướng dẫn xoá dữ liệu người dùng\" (User data deletion), chọn Hạng mục phù hợp với shop, bấm Lưu thay đổi.",
      "5. Đọc cho tôi ID ứng dụng (App ID, một dãy số). Nhắc tôi tự bấm \"Hiển thị\" App secret và tự chép vào TISA BOT.",
      "6. Dừng lại và báo tôi đúng câu: \"Xong phần Meta. Anh dán App ID và App secret vào hộp Kết nối Meta của TISA BOT,",
      "   bấm Đăng nhập Facebook, chọn Fanpage và đồng ý tất cả quyền.\"",
      "7. Hỏi tôi có muốn bật chế độ Live để khách thật nhắn được không. Tôi đồng ý thì mới gạt Live.",
      "Cuối cùng tóm tắt ngắn: bước nào đã xong, bước nào tôi cần tự làm, có lỗi gì Meta báo."
    ].join("\n");
  }

  function chep(text, done) {
    function cachCu() {
      var t = document.createElement("textarea");
      t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(t); done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(true); }, cachCu);
    else cachCu();
  }

  function gan(form) {
    if (!form || form.querySelector(".tisa-meta-ai")) return;
    var dau = form.querySelector(".msc-form-head");
    if (!dau) return;
    var o = document.createElement("div");
    o.className = "tisa-meta-ai";
    o.innerHTML =
      '<div class="tma-dau"><span class="tma-ico" aria-hidden="true">' + (window.ic ? window.ic("sparkles") : "") + '</span>'
      + '<div><b>Để Claude làm giúp phần trên trang Meta</b><small>Tạo app, thêm quyền, dán địa chỉ. Còn khoảng 5 phút thay vì 20.</small></div></div>'
      + '<ol class="tma-buoc">'
      + '<li>Bấm <b>Tạo prompt</b>, prompt được chép sẵn, có đúng địa chỉ của máy này.</li>'
      + '<li>Mở <b>Chrome đã đăng nhập Facebook</b>, mở tiện ích <b>Claude</b>, dán prompt vào.</li>'
      + '<li>Claude tự bấm. Anh chỉ tự làm 4 chỗ: mã OTP, mật khẩu Facebook, chép App secret, bấm đồng ý quyền.</li>'
      + '<li>Quay lại đây dán <b>App ID</b> và <b>App secret</b>, bấm <b>Đăng nhập Facebook</b>.</li>'
      + '</ol>'
      + '<div class="tma-hang"><button type="button" class="s-btn tma-tao">Tạo prompt cho Claude làm giúp</button>'
      + '<button type="button" class="s-btn-ghost tma-xem" aria-expanded="false">Xem prompt</button>'
      + '<span class="lv-msg tma-msg" role="status"></span></div>'
      + '<textarea class="js-input tma-noi" rows="10" readonly hidden aria-label="Prompt cho Claude"></textarea>';
    dau.insertAdjacentElement("afterend", o);
    var noi = o.querySelector(".tma-noi"), msg = o.querySelector(".tma-msg"), xem = o.querySelector(".tma-xem");
    function lamMoi() { noi.value = soanPrompt(diaChi(form)); }
    o.querySelector(".tma-tao").onclick = function () {
      lamMoi();
      chep(noi.value, function (ok) {
        msg.textContent = ok ? "Đã chép prompt. Dán vào Claude trên Chrome." : "Chưa chép tự động được, bấm Xem prompt rồi chép tay.";
        if (!ok) { noi.hidden = false; xem.setAttribute("aria-expanded", "true"); xem.textContent = "Ẩn prompt"; noi.select(); }
      });
    };
    xem.onclick = function () {
      lamMoi();
      noi.hidden = !noi.hidden;
      xem.setAttribute("aria-expanded", noi.hidden ? "false" : "true");
      xem.textContent = noi.hidden ? "Xem prompt" : "Ẩn prompt";
    };
  }

  function quet() { document.querySelectorAll(".msc-form").forEach(gan); }
  new MutationObserver(quet).observe(document.documentElement, { childList: true, subtree: true });
  quet();
  window.TISAMetaAI = { soanPrompt: soanPrompt };
})();
