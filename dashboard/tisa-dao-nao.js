// Trang bộ não của TISA BOT: tên khu vực có tiếng Việt, kéo note tới đâu giữ nguyên chỗ đó.
var KHOA_VI_TRI = "tisa.graph.ghim";
// Tên tiếng Việt của các thư mục thường gặp trong bộ não.
var TEN_VIET = {
  reference: "Tham khảo", references: "Tài liệu dẫn", facts: "Dữ kiện", raw: "Tài liệu thô", concepts: "Khái niệm", examples: "Ví dụ",
  agents: "Cộng sự", skills: "Kỹ năng", workflows: "Quy trình", memory: "Bộ nhớ", sources: "Nguồn", entities: "Thực thể", output: "Kết quả",
  analyses: "Phân tích", attachments: "Đính kèm", templates: "Mẫu", notes: "Ghi chú", projects: "Dự án", tasks: "Công việc", dashboard: "Bảng tổng quan",
  "daily log": "Nhật ký ngày", "weekly log": "Nhật ký tuần", "monthly log": "Nhật ký tháng", "future log": "Kế hoạch", runs: "Lượt chạy", scripts: "Tập lệnh",
  "ho-so": "Hồ sơ", "kien-thuc": "Kiến thức", "tai-lieu-tho": "Tài liệu thô", "ket-qua": "Kết quả", "du-an": "Dự án", mau: "Mẫu", "luu-tru": "Lưu trữ",
};
window.TISADao = {
  // "Facts" thành "Facts (Dữ kiện)". Tên đã là tiếng Việt hoặc tên riêng thì giữ nguyên.
  tenDao: function (ten) {
    var goc = String(ten || "").replace(/^\d+\s*[-_.]\s*/, "").trim();
    var viet = TEN_VIET[goc.toLowerCase()];
    var hoa = goc.charAt(0).toUpperCase() + goc.slice(1);
    return viet ? (/[-]/.test(goc) ? viet : hoa + " (" + viet + ")") : hoa;
  },

  trongCum: function (l, cum) {
    return !!l.source && !!l.target && l.source.__cat === cum && l.target.__cat === cum;
  },
  // Đồ thị nghỉ vẽ khi đứng yên, nên đổi khu vực phải chủ động thu khung để nó vẽ lại. Bỏ lọc thì về toàn cảnh.
  roiCum: function (g) {
    if (!g.graph) return;
    var cum = g._catFilter;
    g.graph.zoomToFit(600, g._fitPad(), cum ? function (n) { return n.__cat === cum; } : function () { return true; });
    document.querySelectorAll(".concept-label").forEach(function (d) { d.classList.toggle("cl-active", !!cum && d.dataset.cat === cum); });
  },

  // Vị trí note đã kéo, lưu trên trình duyệt này.
  _doc: function () {
    try { return JSON.parse(localStorage.getItem(KHOA_VI_TRI) || "{}") || {}; } catch (e) { return {}; }
  },
  _ghi: function (d) {
    try { localStorage.setItem(KHOA_VI_TRI, JSON.stringify(d)); } catch (e) { /* trình duyệt chặn lưu: chỉ mất phần nhớ */ }
  },
  giu: function (n) {
    n.fx = n.x; n.fy = n.y;
    var d = this._doc();
    d[n.id] = [Math.round(n.x), Math.round(n.y)];
    this._ghi(d);
  },
  tha: function (n) {
    n.fx = null; n.fy = null;
    var d = this._doc();
    delete d[n.id];
    this._ghi(d);
  },
  khoiPhuc: function (nodes) {
    var d = this._doc();
    (nodes || []).forEach(function (n) {
      if (d[n.id]) { n.x = n.fx = d[n.id][0]; n.y = n.fy = d[n.id][1]; }
    });
  },
};
