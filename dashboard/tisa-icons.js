// Bộ icon riêng của TISA BOT: nét mảnh kèm mảng màu nhạt. icons.js tra ở đây trước khi dùng Lucide.
(function () {
  var nen = function (d) { return '<path d="' + d + '" fill="currentColor" fill-opacity=".22" stroke="none"/>'; };
  var o = function (x, y, w, h, r) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '"/>'; };
  var oNen = function (x, y, w, h, r) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="currentColor" fill-opacity=".22" stroke="none"/>'; };
  var tron = function (x, y, r) { return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '"/>'; };
  var tronNen = function (x, y, r) { return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="currentColor" fill-opacity=".22" stroke="none"/>'; };
  var net = function (d) { return '<path d="' + d + '"/>'; };

  window.TISA_ICONS = {
    "tisa-giao-viec": nen("M21 3 3 11l7.5 2.5L13 21z") + net("M21 3 3 11l7.5 2.5L13 21z") + net("M21 3 10.5 13.5"),
    "tisa-cong-su": tronNen(10, 8, 4) + tron(10, 8, 4) + net("M3 20c0-3.9 3.1-6 7-6 1.4 0 2.7.3 3.8.8") + nen("M18 12.5l1.1 2.9 2.9 1.1-2.9 1.1-1.1 2.9-1.1-2.9-2.9-1.1 2.9-1.1z") + net("M18 12.5l1.1 2.9 2.9 1.1-2.9 1.1-1.1 2.9-1.1-2.9-2.9-1.1 2.9-1.1z"),
    "tisa-do-thi": tronNen(12, 12, 3.5) + tron(12, 12, 3.5) + tron(5, 5.5, 2) + tron(19, 5.5, 2) + tron(5.5, 19, 2) + tron(18.5, 18.5, 2) + net("M9.4 9.6 6.4 7M14.6 9.6l3-2.6M9.4 14.4l-2.5 3.2M14.6 14.4l2.6 2.8"),
    "tisa-nao": nen("M12 5a3.2 3.2 0 0 0-6-1 3.2 3.2 0 0 0-2.3 5 3.6 3.6 0 0 0 .4 6.1A3.2 3.2 0 0 0 7.5 20 3 3 0 0 0 12 20.5z") + net("M12 5a3.2 3.2 0 0 0-6-1 3.2 3.2 0 0 0-2.3 5 3.6 3.6 0 0 0 .4 6.1A3.2 3.2 0 0 0 7.5 20 3 3 0 0 0 12 20.5z") + net("M12 5a3.2 3.2 0 0 1 6-1 3.2 3.2 0 0 1 2.3 5 3.6 3.6 0 0 1-.4 6.1 3.2 3.2 0 0 1-3.4 4.9 3 3 0 0 1-4.5.5z") + net("M12 5v15.5M8 10.5c1.3 0 2.4.6 2.4 2M16 10.5c-1.3 0-2.4.6-2.4 2"),
    "tisa-tep": nen("M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z") + net("M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z") + net("M8 13h8M8 16h5"),
    "tisa-tu-hoc": nen("M12 4 2 9l10 5 10-5z") + net("M12 4 2 9l10 5 10-5z") + net("M6 11.5V16c1.7 1.6 3.8 2.4 6 2.4s4.3-.8 6-2.4v-4.5M22 9v5"),
    "tisa-nang-luc": tronNen(12, 12, 9) + tron(12, 12, 9) + net("M13 6.5 8.5 13H12l-1 4.5 4.5-6.5H12z"),
    "tisa-team": tronNen(9, 8, 3.5) + tron(9, 8, 3.5) + net("M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.8c1.9.7 3 2.5 3 5.2"),
    "tisa-chatbot": nen("M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-7l-4 4v-4H6a2 2 0 0 1-2-2z") + net("M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-7l-4 4v-4H6a2 2 0 0 1-2-2z") + net("M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"),
    "tisa-ky-nang": nen("M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6-4.5-4.1 6-.7z") + net("M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6-4.5-4.1 6-.7z"),
    "tisa-cong-cu": oNen(4, 4, 7, 7, 2) + o(4, 4, 7, 7, 2) + o(13, 4, 7, 7, 2) + o(4, 13, 7, 7, 2) + tronNen(16.5, 16.5, 3.5) + tron(16.5, 16.5, 3.5),
    "tisa-terminal": oNen(3, 4, 18, 16, 3) + o(3, 4, 18, 16, 3) + net("M7 9l3 3-3 3M12.5 15H17"),
    "tisa-viec": oNen(4, 4, 16, 16, 4) + o(4, 4, 16, 16, 4) + net("M8 12l3 3 5-6"),
    "tisa-danh-sach": oNen(3.5, 5, 4, 4, 1) + o(3.5, 5, 4, 4, 1) + oNen(3.5, 15, 4, 4, 1) + o(3.5, 15, 4, 4, 1) + net("M11 7h9.5M11 17h9.5M11 12h6"),
    "tisa-webhook": tronNen(12, 6, 2.6) + tron(12, 6, 2.6) + tron(6, 18, 2.6) + tron(18, 18, 2.6) + net("M10.8 8.3 7.2 15.7M13.2 8.3l3.6 7.4M8.6 18h6.8"),
    "tisa-ket-noi": oNen(2.5, 8, 11, 8, 4) + o(2.5, 8, 11, 8, 4) + o(10.5, 8, 11, 8, 4),
    "tisa-cam": nen("M6 8h12v4a6 6 0 0 1-12 0z") + net("M8 3v5M16 3v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v3"),
    "tisa-kho": nen("M5 8h14l1 12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z") + net("M5 8h14l1 12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1zM9 11V6a3 3 0 0 1 6 0v5"),
    "tisa-kenh": nen("M4 10h3l10-5v14L7 14H4z") + net("M4 10h3l10-5v14L7 14H4zM20.5 9.5v5M8 14l1.5 6h2.6l-1.4-5"),
    "tisa-cookie": tronNen(12, 12, 9) + tron(12, 12, 9) + net("M9 9h.01M15 10h.01M10 15h.01M15 15h.01"),
    "tisa-he-thong": oNen(3, 4, 18, 7, 2) + o(3, 4, 18, 7, 2) + o(3, 13, 18, 7, 2) + net("M7 7.5h.01M7 16.5h.01M11 7.5h6M11 16.5h6"),
    "tisa-model": oNen(6, 6, 12, 12, 3) + o(6, 6, 12, 12, 3) + net("M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3M12 9.5l.8 1.7 1.7.8-1.7.8-.8 1.7-.8-1.7-1.7-.8 1.7-.8z"),
    "tisa-cai-dat": tronNen(15, 7, 2.4) + tron(15, 7, 2.4) + tronNen(9, 17, 2.4) + tron(9, 17, 2.4) + net("M4 7h8.6M17.4 7H20M4 17h2.6M11.4 17H20"),
    "tisa-chia-se": nen("M5 13v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5z") + net("M12 15V4M8 8l4-4 4 4M5 13v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5"),
    "tisa-tai-khoan": oNen(3, 5, 18, 14, 3) + o(3, 5, 18, 14, 3) + tron(8.5, 11, 2) + net("M5.5 16c.6-1.4 1.7-2 3-2s2.4.6 3 2M14.5 10h4M14.5 14h4"),
    "tisa-thu-gon": o(3, 4, 18, 16, 3) + oNen(3, 4, 7, 16, 3) + net("M10 4v16M17 9l-3 3 3 3"),
    "tisa-doi-quan": nen("M12 3 4 7v5c0 4.5 3.2 8 8 9.5 4.8-1.5 8-5 8-9.5V7z") + net("M12 3 4 7v5c0 4.5 3.2 8 8 9.5 4.8-1.5 8-5 8-9.5V7z") + tron(12, 10, 2.2) + net("M8.5 16c.7-1.7 2-2.5 3.5-2.5s2.8.8 3.5 2.5"),
    // Vai trò của từng cộng sự, dùng trong ảnh đại diện (tisa-avatar.js).
    "vt-vuong-mien": net("M4 18h16M5 15 4 7l5 4 3-6 3 6 5-4-1 8z"),
    "vt-tim-kiem": tron(11, 11, 6.5) + net("m16 16 4.5 4.5M8.5 11h5"),
    "vt-viet": net("M4 20l1-4L16 5l3 3L8 19zM13.5 7.5l3 3M12 20h8"),
    "vt-thiet-ke": net("M12 3a9 9 0 1 0 0 18c1.4 0 2-1 2-2 0-1.5-1-2 0-3.2.7-.8 1.7-.8 3-.8 2.2 0 4-1.3 4-3.6C21 6.5 17 3 12 3z") + net("M7.5 11h.01M9.5 7.5h.01M14 7h.01M17 10h.01"),
    "vt-video": o(3, 8, 18, 12, 2) + net("M3 8l2.5-5 15 1.5.5 3.5M8 4l-1.5 4M13.5 4.5 12 8M10 11.5v5l4.5-2.5z"),
    "vt-da-kenh": tron(18, 5, 2.5) + tron(6, 12, 2.5) + tron(18, 19, 2.5) + net("m8.3 10.8 7.4-4.5M8.3 13.2l7.4 4.5"),
    "vt-quang-cao": net("M4 10h3l10-5v14L7 14H4zM20.5 9.5v5M8 14l1.5 6h2.6l-1.4-5"),
    "vt-bao-cao": net("M4 4v15a1 1 0 0 0 1 1h15M8.5 16v-5M13 16V7M17.5 16v-8"),
    "vt-tu-van": net("M4 13v-1a8 8 0 0 1 16 0v1M4 13a2 2 0 0 1 2-2v6a2 2 0 0 1-2-2zM20 13a2 2 0 0 0-2-2v6a2 2 0 0 0 2-2zM18 17c0 2-2 3-5 3"),
    "vt-cham-soc": net("M12 20.5S3.5 15.5 3.5 9.3C3.5 6.4 5.8 4.5 8.2 4.5c1.6 0 3 .8 3.8 2.2.8-1.4 2.2-2.2 3.8-2.2 2.4 0 4.7 1.9 4.7 4.8 0 6.2-8.5 11.2-8.5 11.2z"),
    "vt-huan-luyen": net("M12 4 2 9l10 5 10-5zM6 11.5V16c1.7 1.6 3.8 2.4 6 2.4s4.3-.8 6-2.4v-4.5"),
    "vt-ke-toan": o(5, 3, 14, 18, 2.5) + net("M9 7h6M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"),
    "vt-kiem-duyet": net("M12 3 4 6.5v5.5c0 4.5 3.2 7.6 8 9 4.8-1.4 8-4.5 8-9V6.5zM8.5 12l2.5 2.5 4.5-5"),
    "vt-san-pham": net("M12 3 3.5 7.5v9L12 21l8.5-4.5v-9zM3.5 7.5 12 12l8.5-4.5M12 12v9"),
    "vt-ky-thuat": net("M14.5 6.5a4 4 0 0 1 5-1.5l-2.8 2.8 1.5 1.5L21 6a4 4 0 0 1-5.4 5l-7.8 7.8a2 2 0 0 1-2.8-2.8L12.8 8a4 4 0 0 1 1.7-1.5z"),
    "vt-tro-ly": net("M12 3l2 5.5L19.5 10.5 14 12.5 12 18l-2-5.5L4.5 10.5 10 8.5zM19 16l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"),
    // 3 cấp giao việc và các trang Đội Quân AI trên thanh menu (09/11/2026).
    "tisa-hoi-nhanh": nen("M3 7a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9l-4 4v-4H5a2 2 0 0 1-2-2z") + net("M3 7a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9l-4 4v-4H5a2 2 0 0 1-2-2z") + net("M7 10h4M7 13h2") + nen("M19 2.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z") + net("M19 2.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z"),
    "tisa-chuyen-gia": tronNen(9, 7, 3.5) + tron(9, 7, 3.5) + net("M2.5 20c0-3.6 2.9-6 6.5-6 1.3 0 2.5.3 3.5.8") + tronNen(17.5, 16.5, 4) + tron(17.5, 16.5, 4) + net("M15.8 16.5l1.2 1.2 2.2-2.4"),
    "tisa-du-an": nen("M12 2.5c3.5 2 5.5 5.6 5.5 9.5L15 15.5H9L6.5 12c0-3.9 2-7.5 5.5-9.5z") + net("M12 2.5c3.5 2 5.5 5.6 5.5 9.5L15 15.5H9L6.5 12c0-3.9 2-7.5 5.5-9.5z") + tron(12, 9, 1.8) + net("M8 13.2 4.5 15.5 6 19l3-1.5M16 13.2l3.5 2.3L18 19l-3-1.5M10.5 18.5 12 21.5l1.5-3"),
    "tisa-truc-khach": net("M4 14v-2a8 8 0 0 1 16 0v2") + oNen(3, 13, 4, 6, 1.6) + o(3, 13, 4, 6, 1.6) + oNen(17, 13, 4, 6, 1.6) + o(17, 13, 4, 6, 1.6) + net("M20 19c0 1.6-1.6 2.5-4 2.5h-2"),
    "tisa-van-phong": oNen(4, 3, 11, 18, 1.5) + o(4, 3, 11, 18, 1.5) + net("M7.5 7h1.2M10.5 7h1.2M7.5 10.5h1.2M10.5 10.5h1.2M7.5 14h1.2M10.5 14h1.2M8.5 21v-3h2v3") + o(15, 9, 5.5, 12, 1.2) + net("M17.5 12.5h.8M17.5 15.5h.8"),
    "tisa-tien-do": o(3, 4, 18, 16, 2.5) + oNen(6, 8, 9, 2.4, 1.2) + o(6, 8, 12, 2.4, 1.2) + oNen(6, 13.5, 5, 2.4, 1.2) + o(6, 13.5, 12, 2.4, 1.2),
    "tisa-ket-qua": nen("M8 4h8v5a4 4 0 0 1-8 0z") + net("M8 4h8v5a4 4 0 0 1-8 0z") + net("M8 6H5.5a3 3 0 0 0 3 4M16 6h2.5a3 3 0 0 1-3 4M12 13v4M8.5 20.5h7M10 17h4"),
    "tisa-nap": nen("M4 5a2 2 0 0 1 2-2h12v14H6a2 2 0 0 0-2 2z") + net("M4 19V5a2 2 0 0 1 2-2h12v14H6a2 2 0 0 0-2 2 2 2 0 0 0 2 2h12v-4") + net("M11 13V7M8.5 9.5 11 7l2.5 2.5"),
    "tisa-web": tron(12, 12, 9) + net("M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18") + nen("M12 3a9 9 0 0 1 0 18z"),
    "tisa-kho-tu-lieu": oNen(3, 7, 14, 13, 2) + o(3, 7, 14, 13, 2) + net("M7 4h12a2 2 0 0 1 2 2v10") + net("M3 17l4-4 3 3 2.5-2 4.5 4") + tron(8, 11, 1.4),
  };

  // Icon từng trang trên thanh bên và đầu trang.
  window.TISA_VIEW_ICONS = {
    home: "tisa-do-thi", chat: "tisa-hoi-nhanh", workspace: "tisa-chuyen-gia", teams: "tisa-team", conversations: "tisa-truc-khach", chatbots: "tisa-truc-khach",
    skills: "tisa-ky-nang", plugins: "tisa-cong-cu", terminal: "tisa-terminal", files: "tisa-tep", learn: "tisa-tu-hoc",
    tasks: "tisa-danh-sach", webhooks: "tisa-webhook", mcp: "tisa-cam", packs: "tisa-kho", channels: "tisa-kenh", logins: "tisa-cookie",
    models: "tisa-model", settings: "tisa-cai-dat", share: "tisa-chia-se", account: "tisa-tai-khoan",
  };

  // Mục trên thanh menu mở một trang của Đội Quân AI (tisa-doi-quan.js). console.js nối vào RAIL_ITEMS; `launch` mở trang
  // trong khung TISA BOT thay vì đổi trang của TISA BOT.
  var DQ = [
    ["dq-du-an", "tisa-du-an", "Giao dự án", "ban-lam-viec"],
    ["dq-van-phong", "tisa-van-phong", "Văn phòng", "van-phong"],
    ["dq-tien-do", "tisa-tien-do", "Tiến độ", "tien-do"],
    ["dq-ket-qua", "tisa-ket-qua", "Kết quả", "ket-qua"],
    ["dq-doi-ngu", "tisa-team", "Đội ngũ", "doi-ngu"],
    ["dq-cai-dat", "tisa-cai-dat", "Cài đặt đội", "cai-dat/nhan-su"],
    ["dq-nap-kien-thuc", "tisa-nap", "Nạp kiến thức", "nap-kien-thuc"],
    ["dq-kho", "tisa-kho-tu-lieu", "Kho tư liệu", "kho"],
  ];
  // Trang riêng của TISA mở trong cùng khung (không phải trang của bảng).
  var TRANG_RIENG = [["dq-nhan-vien", "tisa-tai-khoan", "Tài khoản nhân viên", "/tisa-nv/"], ["dq-web", "tisa-web", "Quản lý web", "/tisa-web/"]];
  // Dòng chữ nhỏ dưới 3 cấp giao việc và Chatbot ở khối trên cùng thanh menu.
  window.TISA_RAIL_PHU = { chat: "Hỏi gì cũng được", workspace: "Đúng người, đúng nghề", "dq-du-an": "Tâm chia việc cả đội", conversations: "Trực khách 24/7" };
  window.TISA_DQ_TRANG = {};
  DQ.forEach(function (x) { window.TISA_DQ_TRANG[x[0]] = x[3]; });
  window.TISA_RAIL_THEM = function (ic) {
    return DQ.map(function (x) {
      return { id: x[0], icon: ic(x[1]), label: x[2],
        launch: function () { if (window.TISADoiQuan) window.TISADoiQuan.mo(x[3], x[0]); } };
    }).concat(TRANG_RIENG.map(function (x) {
      return { id: x[0], icon: ic(x[1]), label: x[2],
        launch: function () { if (window.TISADoiQuan) window.TISADoiQuan.moTrang(x[3], x[0]); } };
    }));
  };
})();
