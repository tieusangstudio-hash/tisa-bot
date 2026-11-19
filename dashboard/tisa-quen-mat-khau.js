/* Quên mật khẩu ở màn đăng nhập TISA BOT: gửi MÃ 6 số về Zalo admin đã nối, nhập mã + mật khẩu mới ngay tại đây.
   Server: server/tisa_quen_mat_khau.py (/auth/quen/*). Không bao giờ nhận hay hiện lại mật khẩu cũ (mật khẩu được băm một chiều). */
(function () {
  "use strict";
  var W = window, D = document, panel = null, buoc = "gui", dem = 0, timerDem = 0, daNoi = null;

  function $(id) { return D.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function api(url, body) {
    var o = { credentials: "same-origin" };
    if (body !== undefined) { o.method = "POST"; o.headers = { "Content-Type": "application/json" }; o.body = JSON.stringify(body); }
    return fetch(url, o).then(function (r) { return r.json().catch(function () { return {}; }); }).catch(function () { return { ok: false, loi: "Không kết nối được với TISA BOT." }; });
  }
  function css() {
    if ($("qmkCss")) return;
    var st = D.createElement("style"); st.id = "qmkCss";
    st.textContent = "#tisaQmk{margin:6px 0 0;padding:0;border:0;background:none;font-size:12.5px;line-height:1.45;color:#64748b;text-align:center}" +
      "#tisaQmk .qmk-h{display:flex;gap:6px;align-items:center;justify-content:center;flex-wrap:wrap}" +
      "#tisaQmk input{height:36px;padding:0 10px;border:1px solid #e2e8f0;border-radius:9px;background:#fff;font:inherit;font-size:13px;color:#0f172a;min-width:0;box-sizing:border-box}" +
      "#tisaQmk input:focus{outline:2px solid rgba(249,115,22,.35);border-color:#f97316}" +
      "#tisaQmk .qmk-b{height:36px;padding:0 14px;border-radius:9px;border:1px solid #f97316;background:#fff7ed;color:#c2410c;font:inherit;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap}" +
      "#tisaQmk .qmk-b:disabled{opacity:.55;cursor:default}#tisaQmk .qmk-l{background:none;border:0;padding:0;color:#64748b;font:inherit;font-size:12px;text-decoration:underline;cursor:pointer}" +
      "#tisaQmk .qmk-l:disabled{text-decoration:none;cursor:default;opacity:.7}#tisaQmk .qmk-e{color:#dc2626;min-height:0;margin-top:4px}#tisaQmk .qmk-o{color:#059669;font-weight:600;margin-top:4px}";
    D.head.appendChild(st);
  }
  function ve() {
    if (!panel) return;
    css();
    var kenh = daNoi, h = "";
    if (kenh && kenh.co_tai_khoan === false) {
      h = "<div>Máy này chưa đặt mật khẩu nên chưa có gì để lấy lại.</div>";
    } else if (kenh && kenh.co_kenh === false) {
      h = "<div>Chưa nối Zalo admin nên chưa gửi mã được. <button type='button' class='qmk-l' data-qmk='thucong'>Cách làm thủ công</button></div>";
    } else if (buoc === "gui") {
      h = "<div class='qmk-h'><span>Gửi mã đặt lại về Zalo admin của bạn</span><button type='button' class='qmk-b' data-qmk='gui'>Gửi mã</button></div>";
    } else {
      h = "<div class='qmk-h'><input id='qmkMa' inputmode='numeric' autocomplete='one-time-code' maxlength='8' placeholder='Mã 6 số' style='width:92px;text-align:center'>" +
        "<input id='qmkMk' type='password' autocomplete='new-password' placeholder='Mật khẩu mới (từ 8 ký tự)' style='flex:1 1 150px'>" +
        "<button type='button' class='qmk-b' data-qmk='doi'>Đặt lại</button></div>" +
        "<div style='margin-top:4px'>Mã đã gửi về Zalo admin, dùng trong 10 phút. <button type='button' class='qmk-l' data-qmk='lai'" + (dem > 0 ? " disabled" : "") + ">" + (dem > 0 ? "Gửi lại sau " + dem + "s" : "Gửi lại") + "</button></div>";
    }
    h += "<div class='qmk-e' id='qmkErr' role='alert' aria-live='polite'></div><div class='qmk-o' id='qmkOk'></div>";
    if (!(kenh && kenh.co_kenh === false)) h += "<div style='margin-top:2px'><button type='button' class='qmk-l' data-qmk='thucong'>Cách làm thủ công</button></div>";
    panel.innerHTML = h;
  }
  function loi(m) { var e = $("qmkErr"); if (e) e.textContent = m || ""; }
  function ok(m) { var e = $("qmkOk"); if (e) e.textContent = m || ""; }
  function batDem(giay) {
    dem = giay; clearInterval(timerDem);
    timerDem = setInterval(function () { dem--; if (dem <= 0) { dem = 0; clearInterval(timerDem); } if (buoc === "doi") capNhatNutLai(); }, 1000);
  }
  function capNhatNutLai() {
    var b = panel && panel.querySelector("[data-qmk='lai']");
    if (!b) return;
    b.disabled = dem > 0; b.textContent = dem > 0 ? "Gửi lại sau " + dem + "s" : "Gửi lại";
  }

  function gui(nut) {
    loi(""); ok("");
    if (nut) { nut.disabled = true; }
    api("/auth/quen/gui", {}).then(function (r) {
      if (r && r.ok) { buoc = "doi"; batDem(60); ve(); var m = $("qmkMa"); if (m) m.focus(); return; }
      if (r && r.co_kenh === false) { daNoi = Object.assign({}, daNoi || {}, { co_kenh: false }); ve(); return; }
      if (r && r.cho) batDem(r.cho);
      if (buoc === "doi") { capNhatNutLai(); } else { ve(); }
      loi((r && r.loi) || "Không gửi được mã. Thử lại giúp bạn.");
    });
  }
  function doi(nut) {
    var ma = ($("qmkMa") || {}).value || "", mk = ($("qmkMk") || {}).value || "";
    loi(""); ok("");
    if (!/^\d{6}$/.test(ma.replace(/\s/g, ""))) { loi("Nhập đủ mã 6 số trong tin Zalo."); return; }
    if (mk.length < 8) { loi("Mật khẩu mới tối thiểu 8 ký tự."); return; }
    nut.disabled = true;
    api("/auth/quen/doi", { code: ma, password: mk }).then(function (r) {
      mk = "";
      var a = $("qmkMk"); if (a) a.value = "";
      if (r && r.ok) {
        ok(r.thong_bao || "Đã đặt lại mật khẩu. Đăng nhập bằng mật khẩu mới.");
        panel.querySelectorAll("input,button[data-qmk='doi']").forEach(function (x) { x.disabled = true; });
        var u = $("authPass"); if (u) { u.value = ""; try { u.focus(); } catch (e) {} }
        return;
      }
      nut.disabled = false;
      loi((r && r.loi) || "Không đặt lại được. Thử lại giúp bạn.");
    });
  }

  function mo() {
    var nut = $("authForgot");
    if (!nut) return;
    if (!panel) {
      panel = D.createElement("div"); panel.id = "tisaQmk"; panel.style.display = "none";
      var help = nut.closest(".tdn-help") || nut.parentNode;
      help.parentNode.insertBefore(panel, help.nextSibling);
      panel.addEventListener("click", function (e) {
        var t = e.target.closest && e.target.closest("[data-qmk]");
        if (!t || t.disabled) return;
        var a = t.getAttribute("data-qmk");
        if (a === "gui" || a === "lai") gui(t);
        else if (a === "doi") doi(t);
        else if (a === "thucong") { var r = $("authResetInfo"); if (r) r.style.display = r.style.display === "none" ? "block" : "none"; }
      });
    }
    if (panel.style.display === "block") { panel.style.display = "none"; return; }
    panel.style.display = "block";
    api("/auth/quen/trang-thai").then(function (r) {
      daNoi = r || {};
      ve();
    });
    ve();
  }

  function gan() {
    var nut = $("authForgot");
    if (!nut || nut.dataset.qmk === "1") return;
    nut.dataset.qmk = "1";
    // Chạy TRƯỚC trình xử lý gốc (chỉ bật tắt phần hướng dẫn thủ công): phần thủ công giờ là một mục phụ trong khung mới.
    nut.addEventListener("click", function (e) { e.stopImmediatePropagation(); e.preventDefault(); mo(); }, true);
  }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", gan); else gan();
  W.TISAQuenMatKhau = { mo: mo };
})();
