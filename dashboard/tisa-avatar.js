// Ảnh đại diện cộng sự của TISA BOT: khung có màu riêng và biểu tượng theo vai trò, không dùng hình có mắt của linh vật.
(function () {
  "use strict";
  var VAI_TRO = [
    [/tong-quan|tam\b/, "vt-vuong-mien"], [/nghien-cuu|tim-kiem/, "vt-tim-kiem"], [/content|noi-dung|viet/, "vt-viet"],
    [/thiet-ke/, "vt-thiet-ke"], [/video/, "vt-video"], [/da-kenh|fanpage|mang-xa-hoi/, "vt-da-kenh"], [/quang-cao|marketing/, "vt-quang-cao"],
    [/bao-cao|phan-tich|tom-tat/, "vt-bao-cao"], [/tu-van|ban-hang/, "vt-tu-van"], [/cham-soc|khach/, "vt-cham-soc"],
    [/huan-luyen|dao-tao/, "vt-huan-luyen"], [/ke-toan|tai-chinh/, "vt-ke-toan"], [/kiem-duyet|phan-bien/, "vt-kiem-duyet"],
    [/hoc-vu|san-pham/, "vt-san-pham"], [/ky-thuat|cong-nghe/, "vt-ky-thuat"], [/core|thu-ky|tro-ly/, "vt-tro-ly"],
  ];
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  function chuCai(ten) {
    var tu = String(ten || "").trim().split(/\s+/).filter(Boolean);
    return ((tu[0] || "?").charAt(0) + (tu.length > 1 ? tu[tu.length - 1].charAt(0) : "")).toUpperCase();
  }

  function veTrong(agent) {
    // Bản nhân bản có tên tự đặt: xét thêm chức danh để giữ biểu tượng của vai trò.
    var chuc = String((agent && agent.role) || "").split(":")[0].normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/gi, "d").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    var slug = String((agent && agent.slug) || "") + " " + chuc;
    for (var i = 0; i < VAI_TRO.length; i++) {
      if (VAI_TRO[i][0].test(slug)) {
        return '<g transform="translate(101 101) scale(4.9)" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">' + window.TISA_ICONS[VAI_TRO[i][1]] + "</g>";
      }
    }
    if (agent && agent.name) {
      return '<text x="160" y="160" text-anchor="middle" dominant-baseline="central" font-size="66" font-weight="800" fill="currentColor">' + esc(chuCai(agent.name)) + "</text>";
    }
    return '<g transform="translate(101 101) scale(4.9)" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">' + window.TISA_ICONS["vt-tro-ly"] + "</g>";
  }

  // Bản không có `avatar.shape` thì dùng khung bo tròn như nhân sự bên Đội Quân AI.
  window.TISAThe = function (agent, a, size, state) {
    var P = window.TISAPet;
    var chon = agent && agent.avatar && agent.avatar.shape;
    var d = P.shapes()[chon] ? P.shapes()[chon].d : P.shapes().squircle.d;
    var mau = (P.toneOf(a.palette, a.color) || ["#172f72"])[0];
    return '<span class="agent-avatar has-img tisa-the" data-state="' + esc(state) + '" style="--avatar-size:' + Number(size) + "px;--the:" + esc(mau) + '">' +
      '<svg viewBox="70 70 180 180" aria-hidden="true"><path class="tisa-the-nen" d="' + esc(d) + '"/>' + veTrong(agent) + "</svg></span>";
  };
})();
