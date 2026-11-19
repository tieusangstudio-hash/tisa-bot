/* tisa-meta-ai.js - nút "Nhờ TISA BOT làm giúp" trong hộp Kết nối Meta (V2.75; từ V3.02 TISA BOT tự thao tác, không dùng Claude).

   Phần mất thời gian nhất khi nối Fanpage là bấm trên developers.facebook.com: tạo app, thêm Messenger và 4 quyền,
   dán Địa chỉ quay về và link chính sách. Nút này soạn sẵn lời nhờ có đúng hai địa chỉ của máy này rồi giao thẳng cho TISA BOT
   (trình duyệt đã chọn, tự cấp Toàn quyền, không xóa tệp): AI bấm giúp các bước đó.

   Lời nhờ dặn AI dừng ở 4 chỗ chỉ chủ tài khoản được làm: mã OTP, mật khẩu Facebook, App secret (chìa khoá Fanpage,
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
      "Dùng skill dq-ho-tro-ket-noi: nối Fanpage Facebook vào TISA BOT để bot tự trả lời tin nhắn và bình luận. Làm luôn từng bước.",
      "Dùng trình duyệt đã chọn cho AI. Chưa đăng nhập Facebook bằng tài khoản quản trị viên Fanpage thì dừng (wait_user) để tôi tự đăng nhập.",
      "Làm trên https://developers.facebook.com, bấm từng bước, chụp màn hình kiểm tra sau mỗi bước, giao diện tiếng Việt hay tiếng Anh đều được.",
      "",
      "THÔNG TIN CỦA TÔI (dán đúng từng ký tự):",
      "- Địa chỉ quay về: " + d.quayVe,
      "- Link chính sách quyền riêng tư: " + d.chinhSach,
      "- Tên app: lấy tên Fanpage của tôi, thêm chữ Bot (hỏi tôi nếu tôi có nhiều Fanpage).",
      "",
      "LUẬT AN TOÀN, BẮT BUỘC:",
      "- KHÔNG gõ mật khẩu, mã OTP, mã xác minh. Gặp thì dừng, nhờ tôi tự gõ rồi làm tiếp.",
      "- KHÔNG bấm \"Hiển thị\" App secret, KHÔNG đọc, KHÔNG chép App secret ra chat. Nếu cần chuyển thì chỉ dùng tisa_browser_do op=dan_vao_tisa.",
      "- KHÔNG bấm đồng ý cấp quyền thay tôi.",
      "- KHÔNG gạt app sang Live khi chưa hỏi tôi.",
      "- Ngoài các bước dưới đây thì không đổi gì khác trong tài khoản Facebook của tôi.",
      "- Hộp Kết nối Meta của TISA BOT có hai ô quyền thêm: \"Nối cả Instagram của Trang\" và \"Đọc số liệu bài viết\". ĐỂ TRỐNG, không tick,",
      "  trừ khi tôi nói muốn dùng VÀ app đã thêm đúng quyền (instagram_basic, instagram_manage_messages, instagram_manage_comments; read_insights).",
      "  Tick mà app chưa có quyền thì Facebook báo \"Invalid Scopes\" và hỏng cả lần đăng nhập. Gặp lỗi đó: bỏ tick hai ô rồi bấm Đăng nhập Facebook lại.",
      "- Facebook chỉ nhận địa chỉ quay về https. Hộp báo cần HTTPS hoặc nút Đăng nhập Facebook xám: Cài đặt > Truy cập từ xa, bật rồi mở lại hộp, đừng làm tiếp trên Meta bằng địa chỉ http.",
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
      "   bấm Đăng nhập Facebook (để trống hai ô quyền thêm), chọn Fanpage và đồng ý tất cả quyền.\"",
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
      + '<div><b>Để TISA BOT làm giúp phần trên trang Meta</b><small>Tạo app, thêm quyền, dán địa chỉ. Còn khoảng 5 phút thay vì 20.</small></div></div>'
      + '<ol class="tma-buoc">'
      + '<li>Bấm <b>Nhờ TISA BOT làm giúp</b>: TISA BOT sang khung chat và tự bắt đầu, đã có sẵn địa chỉ của máy này.</li>'
      + '<li>TISA BOT mở trình duyệt đã chọn và tự bấm trên trang Meta.</li>'
      + '<li>Anh chỉ tự làm 4 chỗ: mã OTP, mật khẩu Facebook, chép App secret, bấm đồng ý quyền.</li>'
      + '<li>Quay lại đây dán <b>App ID</b> và <b>App secret</b>, bấm <b>Đăng nhập Facebook</b>.</li>'
      + '</ol>'
      + '<div class="tma-hang"><button type="button" class="s-btn tma-tao">🤖 Nhờ TISA BOT làm giúp</button>'
      + '<button type="button" class="s-btn-ghost tma-xem" aria-expanded="false">Xem lời nhờ</button>'
      + '<span class="lv-msg tma-msg" role="status"></span></div>'
      + '<textarea class="js-input tma-noi" rows="10" readonly hidden aria-label="Lời nhờ TISA BOT"></textarea>';
    dau.insertAdjacentElement("afterend", o);
    var noi = o.querySelector(".tma-noi"), msg = o.querySelector(".tma-msg"), xem = o.querySelector(".tma-xem");
    function lamMoi() { noi.value = soanPrompt(diaChi(form)); }
    o.querySelector(".tma-tao").onclick = function () {
      lamMoi();
      if (window.TISANhoAI) { msg.textContent = "Đang giao việc cho TISA BOT..."; window.TISANhoAI(noi.value, "Kết nối Meta").then(function (ok) { msg.textContent = ok ? "TISA BOT đang làm, xem ở khung chat." : ""; }); return; }
      chep(noi.value, function (ok) {
        msg.textContent = ok ? "Đã chép lời nhờ. Dán vào khung chat TISA BOT." : "Chưa chép tự động được, bấm Xem lời nhờ rồi chép tay.";
        if (!ok) { noi.hidden = false; xem.setAttribute("aria-expanded", "true"); xem.textContent = "Ẩn lời nhờ"; noi.select(); }
      });
    };
    xem.onclick = function () {
      lamMoi();
      noi.hidden = !noi.hidden;
      xem.setAttribute("aria-expanded", noi.hidden ? "false" : "true");
      xem.textContent = noi.hidden ? "Xem lời nhờ" : "Ẩn lời nhờ";
    };
  }

  /* Sửa hai lỗi học viên hay gặp ở nút "Đăng nhập Facebook":
     1. Tick "Nối cả Instagram" hoặc "Đọc số liệu bài viết" thì TISA BOT xin thêm quyền instagram_* / read_insights. App Meta làm theo hướng dẫn
        chỉ có Messenger và 4 quyền Trang, chưa có các quyền đó, nên Facebook từ chối cả lần đăng nhập ("Invalid Scopes: read_insights").
        Ở đây: gỡ tick sẵn, ghi chú rõ, và hỏi lại một lần trước khi đăng nhập với quyền thêm.
     2. Bấm đăng nhập mà Facebook báo lỗi thì trang không bao giờ quay về TISA BOT, nút kẹt xám tới 15 phút. Sau 45 giây mở nút lại kèm gợi ý. */
  function chinhHop(form) {
    if (!form || form.dataset.tmaChinh === "1") return;
    var nut = form.querySelector('[data-f="login"]');
    var ig = form.querySelector("[data-f-ig]"), ins = form.querySelector("[data-f-insights]");
    if (!nut || !ig || !ins) return;
    form.dataset.tmaChinh = "1";
    ig.checked = false; ins.checked = false;
    var ghi = document.createElement("div");
    ghi.className = "lv-note tma-quyen";
    ghi.textContent = "Hai ô trên là quyền thêm. Chỉ tick khi app Meta đã thêm quyền đó (Instagram, read_insights). Chưa thêm mà tick thì Facebook báo \"Invalid Scopes\" và không đăng nhập được. Chưa chắc thì để trống: nhắn tin và bình luận Fanpage vẫn chạy đủ.";
    var hang = nut.closest(".lv-form-act");
    if (hang) hang.parentNode.insertBefore(ghi, hang);
    var goiY = document.createElement("div");
    goiY.className = "lv-note tma-goi-y"; goiY.hidden = true;
    if (hang) hang.parentNode.insertBefore(goiY, hang.nextSibling);
    var timer = 0;
    nut.addEventListener("click", function (e) {
      if (nut.disabled) return;
      if ((ig.checked || ins.checked) && form.dataset.tmaDaHoi !== "1") {
        e.stopImmediatePropagation(); e.preventDefault();
        form.dataset.tmaDaHoi = "1";
        var m = form.querySelector('[data-f="login-msg"]');
        if (m) m.textContent = "Đang xin quyền thêm. Chắc app Meta đã có quyền đó thì bấm Đăng nhập Facebook lần nữa, chưa chắc thì bỏ tick rồi bấm.";
        return;
      }
      form.dataset.tmaDaHoi = "";
      goiY.hidden = true;
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (!form.isConnected || !nut.disabled) return;
        nut.disabled = false;
        goiY.hidden = false;
        goiY.textContent = "Vẫn đang chờ Facebook. Nếu trang Facebook báo lỗi (ví dụ Invalid Scopes), bỏ tick hai ô quyền thêm ở trên rồi bấm Đăng nhập Facebook lần nữa. Đang đăng nhập dở thì cứ làm tiếp trên trang Facebook.";
      }, 45000);
    }, true);
  }

  function quet() { document.querySelectorAll(".msc-form").forEach(function (f) { gan(f); chinhHop(f); }); }
  new MutationObserver(quet).observe(document.documentElement, { childList: true, subtree: true });
  quet();
  window.TISAMetaAI = { soanPrompt: soanPrompt };
})();
