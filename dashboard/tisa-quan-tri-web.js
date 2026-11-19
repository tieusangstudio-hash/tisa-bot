/* tisa-quan-tri-web.js - Cộng sự "Quản Trị WEB" nhận mọi việc hỗ trợ ở trang Quản lý web (V3.34, chủ yêu cầu 19/11/2026).
   moPhien(): mở cuộc chat kênh agent:tisa-quan-tri-web (TISA BOT nạp lời nhắc, kỹ năng, mô hình, mức nỗ lực của cộng sự này) mà không rời trang hiện tại.
   Cùng cách với tisa-dau-noi.js. Không dùng ký tự em dash. */
(function () {
  "use strict";
  var W = window;
  var SLUG = "tisa-quan-tri-web", KENH = "agent:" + SLUG;
  function brain() { try { return (typeof W.currentBrainPath === "function" && W.currentBrainPath()) || "brain"; } catch (e) { return "brain"; } }
  function lay(url, opt) { return fetch(url, opt).then(function (r) { return r.json().catch(function () { return {}; }); }); }
  function moPhien() {
    if (!W.TISASessions || typeof W.TISASessions.open !== "function") return Promise.resolve(false);
    return lay("/tisa-quan-tri-web/trang-thai").then(function (t) {
      if (!t || !t.co_ho_so) return false;          // chưa có hồ sơ cộng sự trong bộ não: quay về chat thường
      var fd = new FormData(); fd.append("brain", brain()); fd.append("channel", KENH);
      return fetch("/sessions/new", { method: "POST", body: fd }).then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (n) {
        if (!n || !n.id) return false;
        return Promise.resolve(W.TISASessions.open(n.id, function () { return true; }, { empty: true })).then(function () { return true; });
      });
    }).catch(function () { return false; });
  }
  W.TISAQuanTriWeb = { slug: SLUG, kenh: KENH, moPhien: moPhien };
})();
