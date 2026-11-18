/* tisa-quang-cao-thiet-lap.js - tab "Tạo quảng cáo" của trang Quảng Cáo (V2.78, làm gọn 18/11/2026).
   Hai cách: "Nhờ AI làm" (kể ý tưởng, AI chọn nền tảng và soạn phiếu; gộp chế độ Tự động và Nhập ý tưởng cũ, che_do vẫn là "tu_dong")
   và "Tự chọn từng bước" (che_do "tu_chon"). Chọn nền tảng nào thì chữ, lựa chọn, lời nhắc đổi theo nền tảng đó
   (bộ khung nằm ở server: tisa_quang_cao_thiet_lap.py). Hai nút lên chiến dịch: "⚡ AI lên tự động" (API/MCP) và "🌐 AI bấm trên trình duyệt", kèm khung báo kết nối.
   TRANG KHÔNG TỰ BẬT QUẢNG CÁO: chiến dịch luôn tạo ở trạng thái tạm dừng và chờ anh duyệt. */
(function () {
  "use strict";
  var Q = window.TisaQC;
  var esc = Q.esc, api = Q.api;
  var goc = null, KH = null, MAU = [], NGANH = [], KN = {}, TEP = {}, DA_TAI = [], PHIEU = [], HO_SO = [], ThemHs = false, CSDS = {}, CS_LOI = {}, GV = null, csChon = "", henGv = 0, DUONG_TAY = null;
  var S = moi();

  /* "Nhờ AI làm" gồm che_do tu_dong (lưu được lên máy chủ) và y_tuong (chế độ cũ, chỉ còn để đọc dữ liệu cũ) */
  function laAi() { return S.che_do === "tu_dong" || S.che_do === "y_tuong"; }
  function dauXong(ok) { return ok ? '<span class="nhan-tt ok tl-xong">✓ Đã điền</span>' : ""; }
  function coBai() { return S.nguon === "bai_dang" ? S.links.some(function (x) { return x.ok; }) : (S.media.length > 0 || S.texts.some(function (t) { return t.noi_dung || (t.slides && t.slides.length); })); }
  function moi() {
    return { id: "", nen: "", che_do: "tu_dong", kieu: "", muc_tieu: "", cau_truc: { id: "1-1-1", nhom: 1, bai: 1 }, ten: "", ngan_sach_ngay: "", tu_ngay: "", den_ngay: "", tai_khoan: "",
      mo_ta_san_pham: "", dich_den: "", media: [], texts: [{ tieu_de: "", noi_dung: "", cta: "" }], slotMedia: {}, slotText: {}, nhom: [], tuy_chinh: [], tuong_tu: { bat: false, nguon: "", phan_tram: 1 },
      loai_tru: [], ai: {}, ho_so_id: "", nguon: "moi", links: [], linksText: "", studio: null, cau_chon: "auto", ai_tay: false, target: { khu_vuc: "", tuoi_tu: 22, tuoi_den: 55, gioi_tinh: "Cả nam và nữ", so_thich: [], hanh_vi: [], tu_khoa: [] }, file_khach: [], ghi_chu: "", y_tuong: "", giao_luon: true, yt_msg: "", ly_do: [], da_ai: false };
  }
  function K() { return KH && KH[S.nen]; }
  function so(n) { return Number(n || 0).toLocaleString("vi-VN"); }
  function hom() { var d = new Date(); return String(d.getDate()).padStart(2, "0") + "/" + String(d.getMonth() + 1).padStart(2, "0"); }

  /* ---------- ghép bài: số bài = số nhóm x bài mỗi nhóm; hình, video và chữ tự điền theo thứ tự ---------- */
  function soBai() { return S.cau_truc.nhom * S.cau_truc.bai; }
  function ghep() {
    var n = soBai(), ra = [], m = S.media, ds = [], ct = S.cau_truc, lk = S.links.filter(function (x) { return x.ok; });
    S.texts.forEach(function (x, i) { if (x.tieu_de || x.noi_dung || (x.slides && x.slides.length)) ds.push(i); });
    if (!ds.length) ds = [0];
    for (var k = 0; k < n; k++) {
      var kk = ct.chung ? 0 : k;
      var mi = S.slotMedia[k] !== undefined ? S.slotMedia[k] : (m.length ? m[kk % m.length] : "");
      var ti = S.slotText[k] !== undefined ? S.slotText[k] : ds[kk % ds.length];
      var tx = S.texts[ti] || S.texts[0] || {};
      var b = { k: k, nhom: Math.floor(k / ct.bai) + 1, stt: (k % ct.bai) + 1, media_id: mi, ti: ti, tieu_de: tx.tieu_de || "", noi_dung: tx.noi_dung || "", cta: tx.cta || defCta(), slides: tx.slides || [], link: "",
        dung_lai: !ct.chung && m.length > 0 && S.slotMedia[k] === undefined && k >= m.length };
      if (S.nguon === "bai_dang") { b.link = lk.length ? lk[kk % lk.length].url : ""; b.media_id = ""; b.tieu_de = ""; b.noi_dung = ""; b.slides = []; b.dung_lai = !ct.chung && lk.length > 0 && k >= lk.length; }
      ra.push(b);
    }
    return ra;
  }
  function defCta() { var k = K(); return (k && k.cta_theo_muc_tieu[S.muc_tieu]) || (k ? k.cta[0] : ""); }
  function canhBao() {
    var w = [], k = K(); if (!k) return w;
    var n = soBai(), m = S.media.length, t = S.texts.filter(function (x) { return x.noi_dung || x.tieu_de; }).length;
    var khongMedia = S.nen === "google" && S.kieu === "search";
    if (S.nguon === "bai_dang") {
      var lk = S.links.filter(function (x) { return x.ok; }).length;
      if (!lk) w.push("Chưa có link bài đã đăng nào hợp lệ. Dán link bài ở phần Bài quảng cáo.");
      else if (lk < n && !S.cau_truc.chung && lk > 1) w.push("Có " + lk + " bài đã đăng cho " + n + " bài trong mẫu: các bài sau dùng lại từ đầu.");
      else if (lk > n) w.push("Có " + lk + " link nhưng mẫu chỉ có " + n + " bài, " + (lk - n) + " link chưa dùng. Chọn mẫu nhiều bài hơn để dùng hết.");
    } else {
      if (!khongMedia) {
        if (m === 0 && !S.texts.some(function (x) { return x.slides && x.slides.length; })) w.push("Chưa có hình hoặc video. Trợ lý sẽ hỏi lại anh trước khi tạo.");
        else if (m < n && !S.cau_truc.chung) w.push("Có " + m + " hình/video cho " + n + " bài: các bài sau sẽ dùng lại từ đầu. Tải thêm hoặc chọn mẫu ít bài hơn.");
        else if (m > n) w.push("Có " + m + " hình/video nhưng mẫu chỉ có " + n + " bài, " + (m - n) + " cái chưa dùng. Chọn mẫu nhiều bài hơn để dùng hết.");
      }
      if (t === 0) w.push("Chưa có nội dung bài viết. Trợ lý sẽ đề xuất nội dung, chờ anh duyệt.");
      else if (t < n && t > 1 && !S.cau_truc.chung) w.push("Có " + t + " nội dung cho " + n + " bài: các bài sau dùng lại từ đầu.");
    }
    if (S.nen === "google" && S.kieu === "search" && !S.target.tu_khoa.length) w.push("Google Tìm kiếm cần từ khoá. Bấm Gợi ý hoặc tự nhập ở phần Đối tượng.");
    if (S.cau_truc.nhom > 1 && Number(S.ngan_sach_ngay) && Number(S.ngan_sach_ngay) / S.cau_truc.nhom < 100000) w.push("Ngân sách chia cho " + S.cau_truc.nhom + " nhóm còn dưới 100.000 mỗi nhóm mỗi ngày, mỗi nhóm khó có đủ dữ liệu để nền tảng học.");
    if (!S.target.khu_vuc) w.push("Chưa ghi khu vực chạy quảng cáo.");
    return w;
  }

  /* ---------- tải lên ---------- */
  function tai(loai, file, tiendo) {
    return new Promise(function (ok, loi) {
      var x = new XMLHttpRequest();
      x.open("POST", "/tisa-quang-cao/api/tai-len?loai=" + loai + "&ten=" + encodeURIComponent(file.name));
      x.withCredentials = true;
      x.upload.onprogress = function (e) { if (e.lengthComputable && tiendo) tiendo(Math.round(e.loaded / e.total * 100)); };
      x.onload = function () { var j = {}; try { j = JSON.parse(x.responseText); } catch (e) {} if (j.ok) ok(j.tep); else loi(new Error(j.error || "Tải lên không được.")); };
      x.onerror = function () { loi(new Error("Mạng chập chờn, tải lên chưa xong.")); };
      x.send(file);
    });
  }
  function loaiTep(f) { return /^video\//.test(f.type) || /\.(mp4|mov|m4v|webm)$/i.test(f.name) ? "video" : /^image\//.test(f.type) || /\.(jpe?g|png|webp|gif)$/i.test(f.name) ? "anh" : "danh_sach"; }
  function dungLuong(n) { return n >= 1048576 ? (n / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(n / 1024)) + " KB"; }
  function thumb(id) {
    var t = TEP[id]; if (!t) return '<div class="tl-thumb mo">?</div>';
    var u = "/tisa-quang-cao/api/tep/" + id;
    if (t.loai === "anh") return '<img class="tl-thumb" src="' + u + '" alt="' + esc(t.ten) + '">';
    if (t.loai === "video") return '<video class="tl-thumb" src="' + u + '#t=0.5" preload="metadata" muted playsinline></video>';
    return '<div class="tl-thumb tl-file">CSV</div>';
  }
  function khuTai(loai, nhan, chiTiet, dsId) {
    var ds = dsId.map(function (id) { return '<div class="tl-tep">' + thumb(id) + '<div class="tl-tep-ten">' + esc((TEP[id] || {}).ten || id) + '<br><span class="mo">' + dungLuong((TEP[id] || {}).kich_thuoc || 0) + '</span></div><button type="button" class="nut phu nho" data-bo="' + id + '" data-loai="' + loai + '" aria-label="Bỏ tệp">✕</button></div>'; }).join("");
    var cu = DA_TAI.filter(function (t) { return t.loai === loai && dsId.indexOf(t.id) < 0; }).slice(0, 8);
    return '<div class="tl-tai" data-tai="' + loai + '"><div class="tl-keo" tabindex="0" role="button" data-chon="' + loai + '"><b>' + nhan + '</b><span class="mo">' + chiTiet + '</span></div>' +
      '<input type="file" class="an" data-file="' + loai + '" ' + (loai === "anh" ? 'accept="image/*"' : loai === "video" ? 'accept="video/*"' : 'accept=".csv,.txt,.xlsx"') + ' multiple>' +
      '<div class="tl-tt mo" data-tt="' + loai + '"></div><div class="tl-ds">' + ds + "</div>" +
      (cu.length ? '<div class="tl-cu"><span class="mo">Đã tải trước đó:</span>' + cu.map(function (t) { return '<button type="button" class="chip nho" data-dung="' + t.id + '" data-loai="' + loai + '" title="' + esc(t.ten) + '">+ ' + esc(t.ten.slice(0, 22)) + "</button>"; }).join("") + "</div>" : "") + "</div>";
  }
  async function nhanFile(loai, files) {
    var tt = goc.querySelector('[data-tt="' + loai + '"]'), n = 0;
    for (var i = 0; i < files.length; i++) {
      var f = files[i], l = loai === "danh_sach" ? "danh_sach" : loaiTep(f);
      if (loai !== "danh_sach" && l === "danh_sach") { if (tt) tt.textContent = "Bỏ qua " + f.name + ": chỉ nhận hình hoặc video."; continue; }
      try {
        if (tt) tt.textContent = "Đang tải " + f.name + "...";
        var t = await tai(l, f, function (p) { if (tt) tt.textContent = "Đang tải " + f.name + " (" + p + "%)..."; });
        TEP[t.id] = t; DA_TAI.push(t); n++;
        if (l === "danh_sach") S.file_khach.push(t.id); else S.media.push(t.id);
      } catch (e) { if (tt) tt.textContent = e.message; ve(); return; }
    }
    ve();
  }

  /* ---------- vẽ ---------- */
  function badge(n) {
    var v = KN[n] || {}, k = KH[n];
    var apiOk = (v.api || []).some(function (x) { return x.ok; }), mcpGhi = (v.mcp || []).some(function (x) { return x.ok && !x.chi_doc; });
    var tt = apiOk || mcpGhi ? '<span class="nhan-tt ok">● Đã nối' + (mcpGhi ? " (MCP)" : " (API)") + "</span>" : v.ok ? '<span class="nhan-tt dung">◐ Đã nối MCP · chỉ xem số</span>' : v.co ? '<span class="nhan-tt loi">⚠ Có kết nối, chưa chạy được</span>' : '<span class="nhan-tt dung">Chưa nối</span>';
    return tt;
  }
  var NT_ICO = { facebook: "f", tiktok: "♪", google: "G" };
  var NT_GT = { facebook: "Facebook và Instagram", tiktok: "Video ngắn TikTok", google: "Tìm kiếm, YouTube, Gmail" };
  var CACH = [
    ["tu_dong", "🤖", "Nhờ AI làm", "Hợp người mới", "Nói hoặc gõ ý tưởng. AI chọn nền tảng, đối tượng, nội dung, soạn phiếu cho anh duyệt rồi lên chiến dịch."],
    ["tu_chon", "🛠", "Tự chọn từng bước", "Cho người đã biết chạy", "Anh tự chọn nền tảng, mẫu chiến dịch, hình, video, đối tượng, nút bấm, bật tắt AI."]
  ];
  function boPhieuLuu() {
    if (!PHIEU.length) return "";
    return '<details class="tl-pl"><summary>Phiếu đã lưu (' + PHIEU.length + ') ▾</summary><div class="tl-pl-ds">' + PHIEU.map(function (p, i) { return '<div class="tl-phieu"><div><b>' + esc(p.ten) + '</b><div class="mo" style="font-size:12.5px">' + esc((KH[p.nen] || {}).ten || p.nen) + " · " + so(p.ngan_sach_ngay) + "/ngày · " + esc(p.sua) + '</div></div><div class="hang"><button type="button" class="nut phu nho" data-mo="' + i + '">Mở</button><button type="button" class="nut phu nho" data-xp="' + p.id + '">Xoá</button></div></div>'; }).join("") + "</div></details>";
  }
  function bo1() {
    /* Câu đầu: chọn cách làm (2 cách). Phiếu đã lưu nằm góc phải. */
    var h = '<div class="the bc-the"><div class="tl-dau-cach"><div><h2 style="margin:0 0 2px">Anh muốn làm thế nào?</h2><p class="sub" style="margin:0 0 12px">Chọn một cách. Đổi lúc nào cũng được, thông tin đã nhập vẫn giữ.</p></div>' + boPhieuLuu() + '</div><div class="luoi l2 ca-luoi">';
    CACH.forEach(function (m) {
      var on = m[0] === "tu_dong" ? laAi() : S.che_do === m[0];
      h += '<button type="button" class="tl-the ca-the' + (on ? " on" : "") + '" data-che="' + m[0] + '" aria-pressed="' + (on ? "true" : "false") + '">' +
        '<span class="ca-ico" aria-hidden="true">' + m[1] + '</span><b>' + m[2] + '</b><span class="ca-tag">' + m[3] + '</span><span class="mo">' + m[4] + "</span>" + (on ? '<span class="nt-tick" aria-hidden="true">✓</span>' : "") + "</button>";
    });
    h += "</div>";
    if (!S.che_do) h += '<p class="mo bc-goiy">Chưa biết chọn gì? Bấm <b>Nhờ AI làm</b>: anh chỉ cần kể, AI tự chọn nền tảng và soạn phiếu.</p>';
    h += "</div>";
    if (S.che_do === "tu_chon") h += boNen();
    return h;
  }
  function boNen() {
    /* Chỉ dùng ở "Tự chọn từng bước": chọn nền tảng (nơi chạy quảng cáo) */
    var h = '<div class="the bc-the"><div class="bc-dau"><div><h2>Chạy ở đâu?</h2><p class="sub">Chọn nền tảng. Các phần bên dưới đổi theo nền tảng anh chọn.</p></div></div><div class="luoi l3 nt-luoi">';
    Object.keys(KH).forEach(function (n) {
      var on = S.nen === n, co = (KN[n] || {}).co;
      h += '<button type="button" class="tl-the nt-the' + (on ? " on" : "") + '" data-nen="' + n + '" aria-pressed="' + (on ? "true" : "false") + '">' +
        '<span class="nt-tren"><span class="nt-ico nen-' + n + '" aria-hidden="true">' + (NT_ICO[n] || "•") + '</span><span class="nt-ten"><b>' + esc(KH[n].ten) + '</b><span class="mo">' + esc(NT_GT[n] || "") + "</span></span>" +
        (on ? '<span class="nt-tick" aria-hidden="true">✓</span>' : "") + "</span>" +
        '<span class="nt-tt">' + badge(n) + "</span>" +
        '<span class="nt-cap" title="Thứ tự cấp bậc trong quảng cáo">' + esc(KH[n].cap.join(" › ")) + "</span>" +
        (!co ? '<span class="tl-noi nt-noi" data-noi="' + n + '">Nối tài khoản →</span>' : "") + "</button>";
    });
    return h + "</div></div>";
  }
  function boGoc() {
    var k = K(), ai = laAi();
    var lienHe = '<label class="truong">Khách liên hệ ở đâu? (link, Zalo, số điện thoại)<input type="text" data-f="dich_den" value="' + esc(S.dich_den) + '" placeholder="Ví dụ: Zalo 09xx xxx xxx"></label>';
    return '<div class="the"><h2>' + (ai ? "Sản phẩm và mục tiêu" : "Anh muốn quảng cáo gì?") + dauXong(!!(S.mo_ta_san_pham.trim() && S.muc_tieu)) + '</h2><p class="sub">' + (ai ? "AI điền sẵn từ ý tưởng của anh. Sửa lại chỗ nào chưa đúng." : "Viết như đang kể với nhân viên. Càng rõ thì gợi ý đối tượng và nội dung càng đúng.") + "</p>" + boHoSo() +
      '<label class="truong">Sản phẩm hoặc dịch vụ (kèm giá, điểm mạnh nếu có)<textarea data-f="mo_ta_san_pham" rows="3" placeholder="Ví dụ: Bán nhà phố 4 tầng, giá 5 tỷ, gần chợ, sổ hồng riêng">' + esc(S.mo_ta_san_pham) + "</textarea></label>" +
      (ai ? lienHe : '<div class="cot2"><label class="truong">Khu vực chạy quảng cáo<input type="text" data-t="khu_vuc" value="' + esc(S.target.khu_vuc) + '" placeholder="Quận hoặc tỉnh thành"></label>' + lienHe + "</div>") +
      '<div class="truong">Anh muốn quảng cáo mang lại điều gì?</div><div class="tl-mt">' + k.muc_tieu.map(function (m) { return '<button type="button" class="tl-the nho' + (S.muc_tieu === m.id ? " on" : "") + '" data-mt="' + m.id + '"><b>' + esc(m.ten) + '</b><span class="mo">' + esc(m.mo_ta) + "</span></button>"; }).join("") + "</div></div>";
  }
  function boHoSo() {
    var k = K(), ds = HO_SO.filter(function (h) { return h.nen === S.nen; });
    var nhan = { facebook: ["Quảng cáo cho Fanpage nào?", "Fanpage", "Tên Fanpage"], tiktok: ["Quảng cáo cho kênh TikTok nào?", "kênh TikTok", "Tên kênh TikTok (ví dụ @tenkenh)"], google: ["Quảng cáo cho website hoặc thương hiệu nào?", "website", "Tên thương hiệu hoặc địa chỉ website"] }[S.nen];
    var h = '<div class="tl-hs"><div class="truong">' + nhan[0] + '</div><div class="hang"><select data-hs-chon aria-label="' + nhan[0] + '"><option value="">' + (ds.length ? "Chọn từ danh sách đã lưu" : "Chưa có, bấm Thêm bên cạnh") + "</option>" +
      ds.map(function (x) { return '<option value="' + x.id + '"' + (S.ho_so_id === x.id ? " selected" : "") + ">" + esc(x.ten) + "</option>"; }).join("") + '</select><button type="button" class="nut phu nho" data-hs-them>+ Thêm ' + nhan[1] + "</button>" +
      (S.ho_so_id ? '<button type="button" class="nut phu nho" data-hs-xoa="' + S.ho_so_id + '" title="Xoá khỏi danh sách đã lưu">Xoá</button>' : "") + "</div>";
    if (ThemHs) h += '<div class="tl-hs-form"><label class="truong">' + nhan[2] + '<input type="text" id="hsTen" placeholder="Nhập tên rồi bấm Lưu, lần sau chỉ cần chọn"></label>' +
      '<label class="truong">Link ' + nhan[1] + ' (không bắt buộc)<input type="text" id="hsLink" placeholder="https://..."></label>' +
      '<label class="truong">Giọng thương hiệu (không bắt buộc, giúp AI viết đúng chất)<input type="text" id="hsGiong" placeholder="Ví dụ: thân thiện, gần gũi, xưng em gọi anh chị"></label>' +
      '<div class="hang" style="margin-top:8px"><button type="button" class="nut nho" data-hs-luu>Lưu</button><button type="button" class="nut phu nho" data-hs-them>Đóng</button><span class="mo" id="hsTt"></span></div></div>';
    return h + "</div>";
  }
  function boCauTruc(auto) {
    var k = K(), h = '<div class="the"><h2>Mẫu chiến dịch: bao nhiêu ' + esc(k.cap[1].split(" (")[0].toLowerCase()) + ", bao nhiêu bài?</h2><p class=\"sub\">1 " + esc(k.cap[0].toLowerCase()) + " chứa nhiều " + esc(k.cap[1].split(" (")[0].toLowerCase()) +
      ", mỗi nhóm chứa nhiều bài. Ký hiệu: CD là chiến dịch, N là một " + esc(k.cap[1].split(" (")[0].toLowerCase()) + ".</p><div class=\"luoi l4m\">";
    if (auto) h += '<button type="button" class="tl-the' + (S.cau_chon === "auto" ? " on" : "") + '" data-ct-auto><div class="tl-so"><span class="tl-cd">🤖</span></div><b>Để AI chọn</b><span class="mo">AI chọn mẫu hợp ngân sách và số bài anh có.</span></button>';
    MAU.forEach(function (m) { h += '<button type="button" class="tl-the' + (S.cau_chon !== "auto" && S.cau_truc.id === m.id ? " on" : "") + '" data-ct="' + m.id + '"><div class="tl-so">' + sodo(m.nhom, m.bai, m.chung) + "</div><b>" + esc(m.ten) + '</b><span class="mo">' + esc(m.hop) + "</span></button>"; });
    h += "</div>";
    if (!auto) h += '<div class="hang" style="margin-top:10px"><label class="mo">Tự chọn: <input type="number" min="1" max="5" data-ctn="nhom" value="' + S.cau_truc.nhom + '" style="width:64px"> ' + esc(k.cap[1].split(" (")[0].toLowerCase()) + ', mỗi nhóm <input type="number" min="1" max="5" data-ctn="bai" value="' + S.cau_truc.bai + '" style="width:64px"> bài</label><span class="mo">Tổng ' + soBai() + " bài</span></div>";
    var m = S.media.length;
    if (!auto && S.nguon !== "bai_dang" && m > 1 && m !== soBai() && S.nen !== "google" && !S.cau_truc.chung) {
      h += '<div class="canh" style="margin-top:12px">Anh đã tải ' + m + " hình/video. " + (m === 3 ? 'Muốn mỗi cái là một bài thì chọn <a href="#" data-ct="1-3-3">3 nhóm, mỗi nhóm 1 bài</a> hoặc <a href="#" data-ct="1-1-3">1 nhóm 3 bài</a>.' : "Chọn số nhóm và bài sao cho tổng là " + m + " để dùng hết.") + "</div>";
    }
    return h + "</div>";
  }
  function boNguon(don, anThe) {
    var k = K(), nv = { facebook: "Fanpage", tiktok: "kênh TikTok", google: "kênh YouTube" }[S.nen];
    var cards = [["bai_dang", "🔗 Dùng bài đã đăng", "Chạy đúng một bài đã có trên " + nv + ". Chỉ cần dán link."], ["moi", "📎 Tải lên và tự viết", "Tải hình, video có sẵn và dán nội dung anh đã soạn."], ["ai", "✨ AI tạo giúp", "AI viết nội dung, tạo ảnh, dựng video theo tầng phễu anh chọn."]];
    var h = anThe ? "" : '<div class="luoi l3">' + cards.map(function (c) { return '<button type="button" class="tl-the nho' + (S.nguon === c[0] ? " on" : "") + '" data-nguon="' + c[0] + '"><b>' + c[1] + '</b><span class="mo">' + c[2] + "</span></button>"; }).join("") + "</div>";
    if (S.nguon === "bai_dang") h += '<div style="margin-top:14px">' + boLinks() + "</div>";
    else if (S.nguon === "ai") h += '<div style="margin-top:14px">' + (window.TisaStudio ? TisaStudio.html() : '<div class="canh">Đang tải bộ tạo bài AI...</div>') + '</div><h3 style="margin-top:18px">Đã thêm vào chiến dịch</h3>' + boMedia(don);
    else h += '<div style="margin-top:14px">' + boMedia(don) + "</div>";
    return h;
  }
  var HD_LINK = {
    facebook: ["Mở Fanpage của anh, tìm đúng bài cần chạy quảng cáo.", "Trên máy tính: bấm vào dòng thời gian đăng bài (ví dụ \"2 giờ\" hoặc \"12 tháng 11\") để mở riêng bài đó, rồi sao chép đường dẫn trên thanh địa chỉ. Hoặc bấm dấu ba chấm (...) góc bài, chọn Sao chép liên kết.",
      "Trên điện thoại: bấm Chia sẻ dưới bài, chọn Sao chép liên kết.", "Dán vào ô bên dưới, mỗi dòng một link. Muốn chạy nhiều bài thì dán nhiều dòng.", "Lưu ý: bài phải để chế độ Công khai và do chính Fanpage đăng. Link của cả trang, của nhóm hay của trang cá nhân thì chưa đúng. Link rút gọn dạng facebook.com/share/... vẫn dùng được."],
    tiktok: ["Mở video đã đăng trên kênh TikTok của anh.", "Bấm Chia sẻ, chọn Sao chép liên kết (trên máy tính thì chép đường dẫn trên thanh địa chỉ).", "Dán vào ô bên dưới, mỗi dòng một video.", "Muốn chạy quảng cáo bằng video đã đăng (Spark Ads), anh cần cho phép dùng video: TikTok > Cài đặt > Quyền riêng tư > Quảng cáo > bật Ủy quyền video quảng cáo, rồi lấy mã nếu nền tảng yêu cầu."],
    google: ["Mở video trên kênh YouTube của anh.", "Bấm Chia sẻ, chọn Sao chép.", "Dán vào ô bên dưới, mỗi dòng một video.", "Kênh YouTube cần được nối với tài khoản Google Ads thì mới chạy được video này làm quảng cáo."]
  };
  function boLinks() {
    var nv = { facebook: "bài trên Fanpage", tiktok: "video TikTok", google: "video YouTube" }[S.nen];
    var h = '<p class="mo" style="margin:0 0 8px">Dán link ' + nv + " anh muốn chạy quảng cáo, mỗi dòng một link. Hệ thống sẽ chạy đúng " + (S.nen === "facebook" ? "bài" : "video") + " đó, không tạo bài mới.</p>" +
      '<textarea id="tlLinkTxt" rows="4" placeholder="' + (S.nen === "facebook" ? "https://www.facebook.com/tenfanpage/posts/..." : S.nen === "tiktok" ? "https://www.tiktok.com/@tenkenh/video/..." : "https://www.youtube.com/watch?v=...") + '" style="width:100%">' + esc(S.linksText) + "</textarea>" +
      '<div id="tlLinks">' + veLinks() + "</div>" +
      '<details style="margin-top:10px"><summary>Cách lấy link ' + nv + ' (bấm để xem)</summary><ol>' + HD_LINK[S.nen].map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol></details>";
    return h;
  }
  function veLinks() {
    if (!S.links.length) return "";
    return S.links.map(function (l, i) {
      return '<div class="tl-lk ' + (l.ok ? "ok" : "loi") + '"><span>' + (l.ok ? "✓" : "⚠") + "</span><div><b>" + (l.ok ? esc(l.mo_ta || "Bài") : "Link chưa dùng được") + "</b>" + (l.ma_bai ? ' <span class="mo">mã ' + esc(l.ma_bai.slice(0, 24)) + "</span>" : "") + '<div class="mo" style="font-size:12.5px;word-break:break-all">' + esc(l.url) + "</div>" +
        (l.loi ? '<div style="color:var(--do);font-size:13px">' + esc(l.loi) + "</div>" : "") + (l.ghi_chu ? '<div class="mo" style="font-size:13px">' + esc(l.ghi_chu) + "</div>" : "") + "</div></div>";
    }).join("");
  }
  var tLk = 0;
  function docLinks(txt) {
    S.linksText = txt;
    clearTimeout(tLk);
    tLk = setTimeout(async function () {
      var ds = txt.split(/\n+/).map(function (x) { return x.trim(); }).filter(Boolean).slice(0, 10), ra = [];
      for (var i = 0; i < ds.length; i++) {
        var j = await api("/tisa-quang-cao/api/phan-tich-link?nen=" + S.nen + "&url=" + encodeURIComponent(ds[i]));
        ra.push(j.ok ? { url: j.chuan || ds[i], ok: true, loai: j.loai, mo_ta: j.mo_ta, ma_bai: j.ma_bai, trang: j.trang, rut_gon: j.rut_gon, ghi_chu: j.ghi_chu } : { url: ds[i], ok: false, loi: j.error });
      }
      S.links = ra;
      var el = goc.querySelector("#tlLinks"); if (el) el.innerHTML = veLinks();
      vePhai();
    }, 450);
  }
  function boYTuong() {
    return '<div class="the tl-ytuong yt-the"><div class="yt-dau"><span class="yt-bong" aria-hidden="true">💡</span><div><h2>Ý tưởng anh muốn chạy</h2>' +
      '<p class="sub">Gõ như đang nhắn cho nhân viên: chạy cái gì, bán cho ai, ở đâu, khuyến mãi gì. Trợ lý tự viết nội dung, chọn đối tượng, cấu trúc rồi dựng cả chiến dịch. Chiến dịch luôn ở trạng thái <b>tạm dừng</b>, anh duyệt mới chạy.</p></div></div>' +
      '<div class="yt-o"><textarea data-f="y_tuong" rows="5" aria-label="Ý tưởng quảng cáo" placeholder="Ví dụ: Chạy quảng cáo nhận tin nhắn cho căn nhà phố 4 tầng ở Gò Vấp giá 5 tỷ, nhắm người 28 đến 50 tuổi ở TP.HCM, nhấn mạnh sổ hồng riêng, gần chợ, khách nhắn Zalo để xem nhà cuối tuần." style="padding-right:16px">' + esc(S.y_tuong) + "</textarea></div>" +
      '<label class="tl-ai yt-giao"><input type="checkbox" role="switch" data-yt-giao' + (S.giao_luon !== false ? " checked" : "") + '><span class="tl-sw"></span><span><b>Giao luôn cho cộng sự dựng chiến dịch</b><br><span class="mo">Tạo chiến dịch trên nền tảng ở trạng thái tạm dừng. Tắt thì chỉ soạn nội dung, anh tự dựng.</span></span></label>' +
      '<button type="button" class="nut cam yt-pt yt-rong" data-ytuong-chay>✨ AI viết nội dung và setup toàn bộ</button>' +
      '<div id="ytTt" class="mo" style="margin-top:8px;font-size:13px">' + esc(S.yt_msg || "") + "</div></div>";
  }
  /* ---------- nhập ý tưởng: nói hoặc gõ, AI phân tích và hướng dẫn chi tiết ---------- */
  var YT = { text: "", kq: null, dang: false, msg: "", mic: "idle", dict: null };
  function ytVan(k) {
    var n = (KH && KH[k.nen_tang] || {}).ten || k.nen_tang, mt = "";
    try { mt = (KH[k.nen_tang].muc_tieu.filter(function (m) { return m.id === k.muc_tieu_id; })[0] || {}).ten || k.muc_tieu_id; } catch (e) { mt = k.muc_tieu_id; }
    var t = "KẾ HOẠCH QUẢNG CÁO\n" + k.tom_tat + "\n\nNền tảng: " + n + " (" + k.ly_do_nen_tang + ")\nMục tiêu: " + mt + "\nSản phẩm: " + k.san_pham + "\nKhu vực: " + (k.khu_vuc || "chưa nói") + "\nĐối tượng: " + k.tuoi_tu + " đến " + k.tuoi_den + " tuổi. " + k.doi_tuong +
      "\nNgân sách đề xuất: " + so(k.ngan_sach_ngay) + " mỗi ngày. " + k.ngan_sach_ly_do + "\n\nNỘI DUNG BÀI\n" + (k.noi_dung.tieu_de ? k.noi_dung.tieu_de + "\n" : "") + k.noi_dung.noi_dung_bai + "\nNút: " + k.noi_dung.cta + "\n\nHÌNH, VIDEO CẦN CHUẨN BỊ\n" + k.hinh_video + "\n\nCÁC BƯỚC\n" +
      k.buoc.map(function (b, i) { return (i + 1) + ". " + b.ten + (b.ai_lam ? " (AI làm được)" : " (anh làm)") + ": " + b.chi_tiet; }).join("\n") + "\n\nDẤU HIỆU TỐT\n" + k.dau_hieu_tot.join("\n") + "\nKhi nào dừng: " + k.khi_nao_dung;
    return t;
  }
  function boYT() {
    var nghe = YT.mic === "listening", bat = YT.mic === "transcribing";
    var h = '<div class="the tl-ytuong yt-the"><div class="yt-dau"><span class="yt-bong" aria-hidden="true">💡</span><div><h2>Kể cho AI nghe</h2>' +
      '<p class="sub">Nói hoặc gõ như đang kể với nhân viên: bán gì, cho ai, ở đâu, khuyến mãi gì. AI chọn nền tảng, đối tượng, soạn nội dung và điền phiếu cho anh xem.</p></div></div>' +
      '<div class="yt-o' + (nghe ? " dang-nghe" : "") + '"><textarea data-yt2 rows="5" aria-label="Ý tưởng quảng cáo" placeholder="Ví dụ: Em bán căn nhà phố 4 tầng ở Gò Vấp giá 5 tỷ, muốn chạy quảng cáo kéo khách nhắn Zalo xem nhà cuối tuần, khoảng 300 nghìn mỗi ngày.">' + esc(YT.text) + "</textarea>" +
      '<button type="button" class="yt-mic' + (nghe ? " on" : "") + '" data-yt-mic aria-label="Bấm để nói" title="' + (nghe ? "Bấm để dừng ghi" : "Bấm để nói") + '">' + (bat ? "⏳" : nghe ? "⏹" : "🎤") + '</button></div>' +
      '<div class="tl-nhanh"><label class="truong">Chạy ở<select data-chay-o aria-label="Chạy ở"><option value="">✨ Để AI chọn</option>' + Object.keys(KH).map(function (n) { return '<option value="' + n + '"' + (S.nen === n ? " selected" : "") + ">" + esc(KH[n].ten) + "</option>"; }).join("") + "</select></label>" +
      '<label class="truong">Tiền mỗi ngày<input type="number" min="0" step="any" data-f="ngan_sach_ngay" value="' + esc(S.ngan_sach_ngay) + '" placeholder="200000"></label>' +
      '<label class="truong">Khu vực<input type="text" data-t="khu_vuc" value="' + esc(S.target.khu_vuc) + '" placeholder="Quận hoặc tỉnh thành"></label>' +
      '<label class="truong">Bài quảng cáo<select data-nguon-o aria-label="Bài quảng cáo">' + [["moi", "Tải video, ảnh lên"], ["bai_dang", "Bài đã đăng"], ["ai", "✨ AI tạo giúp"]].map(function (c) { return '<option value="' + c[0] + '"' + (S.nguon === c[0] ? " selected" : "") + ">" + c[1] + "</option>"; }).join("") + "</select></label></div>" +
      '<div class="hang" style="margin-top:6px">' + [100000, 200000, 300000, 500000].map(function (v) { return '<button type="button" class="chip" data-ns="' + v + '">' + so(v) + "</button>"; }).join("") + "</div>" +
      '<div class="yt-chan"><button type="button" class="nut cam yt-pt" data-yt-pt' + (YT.dang ? " disabled" : "") + '>' + (YT.dang ? "AI đang soạn..." : "✨ AI soạn kế hoạch") + '</button>' +
      '<span class="mo yt-luu">Chưa có gì được tạo hay bật. Anh xem kế hoạch rồi mới quyết.</span></div>' +
      '<div class="mo" id="ytTt2" style="margin-top:8px;font-size:13px">' + esc(YT.msg) + "</div></div>";
    var k = YT.kq; if (!k) return h;
    var kh = KH && KH[k.nen_tang], mt = ""; try { mt = kh.muc_tieu.filter(function (m) { return m.id === k.muc_tieu_id; })[0].ten; } catch (e) { mt = k.muc_tieu_id; }
    h += '<div class="the"><h2>Kế hoạch AI đề xuất</h2><p class="sub">' + esc(k.tom_tat) + "</p>" +
      '<div class="luoi l2"><div class="tl-lk ok"><div><b>Nền tảng:</b> ' + esc(kh ? kh.ten : k.nen_tang) + '<div class="mo" style="font-size:13px">' + esc(k.ly_do_nen_tang) + "</div></div></div>" +
      '<div class="tl-lk ok"><div><b>Mục tiêu:</b> ' + esc(mt) + '<div class="mo" style="font-size:13px">Sản phẩm: ' + esc(k.san_pham) + "</div></div></div>" +
      '<div class="tl-lk ok"><div><b>Đối tượng:</b> ' + k.tuoi_tu + " đến " + k.tuoi_den + " tuổi" + (k.khu_vuc ? ", " + esc(k.khu_vuc) : "") + '<div class="mo" style="font-size:13px">' + esc(k.doi_tuong) + "</div></div></div>" +
      '<div class="tl-lk ok"><div><b>Ngân sách:</b> ' + so(k.ngan_sach_ngay) + ' mỗi ngày<div class="mo" style="font-size:13px">' + esc(k.ngan_sach_ly_do) + "</div></div></div></div></div>";
    h += '<div class="the"><h2>Nội dung bài quảng cáo (sẵn để dùng)</h2>' + (k.noi_dung.tieu_de ? "<p><b>" + esc(k.noi_dung.tieu_de) + "</b></p>" : "") + '<div class="pa-ai" style="margin-top:0">' + esc(k.noi_dung.noi_dung_bai) + "</div>" +
      (k.noi_dung.cta ? '<p class="mo" style="margin:8px 0 0">Nút kêu gọi: <b>' + esc(k.noi_dung.cta) + "</b></p>" : "") + '<p style="margin:10px 0 0"><b>Hình, video cần chuẩn bị:</b> ' + esc(k.hinh_video) + "</p></div>";
    if (k.thieu.length) h += '<div class="the" style="border-color:var(--vang)"><h3>AI cần anh bổ sung thêm</h3><ul style="margin:6px 0 0;padding-left:20px">' + k.thieu.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + '</ul><p class="mo" style="margin:8px 0 0;font-size:13px">Nói hoặc gõ thêm vào ô bên trên rồi bấm phân tích lại.</p></div>';
    h += '<div class="the"><h2>Hướng dẫn chi tiết từng bước</h2><p class="sub">Bước có nhãn <b>AI làm được</b> thì TISA BOT hoặc cộng sự làm giúp anh. Bước <b>Anh làm</b> là phần phải do chính anh bấm hoặc quyết.</p><ol class="tk-buoc">' +
      k.buoc.map(function (b) { return "<li><b>" + esc(b.ten) + '</b> <span class="pa-hd ' + (b.ai_lam ? "pa-tang" : "pa-giam") + '">' + (b.ai_lam ? "AI làm được" : "Anh làm") + "</span><br>" + esc(b.chi_tiet) + "</li>"; }).join("") + "</ol>" +
      (k.dau_hieu_tot.length ? '<h3 style="margin-top:12px">Chạy tốt khi</h3><ul style="margin:4px 0 0;padding-left:20px">' + k.dau_hieu_tot.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "") +
      (k.khi_nao_dung ? '<p style="margin:10px 0 0"><b>Khi nào dừng hoặc đổi:</b> ' + esc(k.khi_nao_dung) + "</p>" : "") +
      '<div class="hang" style="margin-top:14px"><button type="button" class="nut cam" data-yt-dung>✅ Dùng kế hoạch này</button><button type="button" class="nut phu" data-yt-hoi>Hỏi AI</button><button type="button" class="nut phu nho" data-yt-chep>Chép kế hoạch</button></div>' +
      '<p class="mo" style="font-size:12.5px;margin:8px 0 0">"Dùng kế hoạch này" điền sẵn phiếu bên dưới để anh xem lại, rồi bấm <b>⚡ AI lên tự động</b> hoặc <b>🌐 AI bấm trên trình duyệt</b> ở cột bên phải. Chiến dịch luôn tạo ở trạng thái tạm dừng, anh duyệt mới chạy.</p></div>';
    return h;
  }
  function ytMicSon() {
    var b = goc && goc.querySelector("[data-yt-mic]"), o = goc && goc.querySelector(".yt-o");
    if (b) { b.textContent = YT.mic === "transcribing" ? "⏳" : YT.mic === "listening" ? "⏹" : "🎤"; b.classList.toggle("on", YT.mic === "listening"); b.title = YT.mic === "listening" ? "Bấm để dừng ghi" : "Bấm để nói"; }
    if (o) o.classList.toggle("dang-nghe", YT.mic === "listening");
  }
  function ytMic() {
    var D = window.TISADictate;
    if (!D) { YT.msg = "Trình duyệt này chưa ghi âm được. Anh gõ chữ vào ô bên trên nhé."; var m = goc.querySelector("#ytTt2"); if (m) m.textContent = YT.msg; return; }
    if (YT.dict && YT.mic !== "idle") { try { YT.dict.stop(); } catch (e) {} return; }
    var ta = goc.querySelector("[data-yt2]"), base = (ta ? ta.value : YT.text).replace(/\s+$/, ""); base = base ? base + " " : "";
    YT.dict = D.create({
      onText: function (t) { YT.text = base + t; var a = goc.querySelector("[data-yt2]"); if (a) a.value = YT.text; },
      onState: function (s) { YT.mic = s === "listening" || s === "transcribing" ? s : "idle"; ytMicSon(); },
      onError: function (c) { var m = goc.querySelector("#ytTt2"); YT.msg = c === "denied" ? "Trình duyệt chưa cho dùng mic. Bấm biểu tượng ổ khoá cạnh địa chỉ, cho phép micro rồi thử lại." : c === "nothing" ? ((D.lyDo && D.lyDo()) || "Em chưa nghe thấy tiếng nào. Anh nói lại gần mic hơn nhé.") : "Ghi âm chưa được, anh gõ chữ giúp em nhé."; if (m) m.textContent = YT.msg; }
    });
    try { YT.dict.start(); } catch (e) { YT.mic = "idle"; ytMicSon(); }
  }
  /* thông tin ở các ô nhanh gửi kèm ý tưởng để AI soạn đúng */
  function ytThem() {
    var p = [];
    if (S.nen && KH[S.nen]) p.push("Muốn chạy trên " + KH[S.nen].ten + ".");
    if (Number(S.ngan_sach_ngay) > 0) p.push("Tiền quảng cáo mỗi ngày: " + so(S.ngan_sach_ngay) + " đồng.");
    if (S.target.khu_vuc) p.push("Khu vực: " + S.target.khu_vuc + ".");
    if (S.nguon === "bai_dang") p.push("Muốn chạy bài đã đăng sẵn.");
    else if (S.nguon === "ai") p.push("Muốn AI tạo nội dung, hình, video.");
    else if (S.media.length) p.push("Đã có " + S.media.length + " hình hoặc video để tải lên.");
    return p.length ? "\n\n" + p.join(" ") : "";
  }
  async function ytPhanTich() {
    var ta = goc.querySelector("[data-yt2]"); if (ta) { YT.text = ta.value; S.y_tuong = ta.value; }
    if (YT.dict && YT.mic !== "idle") { try { YT.dict.stop(); } catch (e) {} }
    if (YT.text.trim().length < 8) { YT.msg = "Anh nói hoặc gõ ý tưởng dài hơn một chút nhé."; ve(); return; }
    YT.dang = true; YT.msg = "AI đang đọc ý tưởng và soạn kế hoạch (khoảng 20 đến 40 giây)..."; ve();
    var j = await api("/tisa-quang-cao/api/ai/y-tuong", { y_tuong: YT.text + ytThem(), nen: S.nen || "" });
    YT.dang = false;
    if (!j.ok) { YT.msg = j.error || "Chưa soạn được kế hoạch."; ve(); return; }
    YT.kq = j.kq; YT.msg = "Xong. Kế hoạch ở bên dưới, bấm Dùng kế hoạch này để điền phiếu."; ve();
    var cu = goc.querySelector(".tl-ytuong + .the"); if (cu) cu.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  /* đổi nền tảng: giữ những gì anh đã nhập, các lựa chọn riêng của nền tảng cũ thì về mặc định */
  function chonNen(n) {
    if (S.nen === n) return;
    DUONG_TAY = null;
    if (!n || !KH[n]) { S.nen = ""; return; }
    var cu = S; S = moi(); S.id = ""; S.nen = n; S.che_do = cu.che_do; S.mo_ta_san_pham = cu.mo_ta_san_pham; S.y_tuong = cu.y_tuong; S.giao_luon = cu.giao_luon; S.dich_den = cu.dich_den; S.ngan_sach_ngay = cu.ngan_sach_ngay; S.target.khu_vuc = cu.target.khu_vuc; S.media = cu.media; S.texts = cu.texts; S.file_khach = cu.file_khach; GY = null; S.cau_chon = cu.cau_chon; S.ai_tay = false; S.nguon = cu.nguon === "bai_dang" && cu.nen ? "moi" : cu.nguon; S.studio = cu.studio;
    var k0 = KH[S.nen]; S.muc_tieu = (k0.muc_tieu.filter(function (m) { return m.id === cu.muc_tieu; })[0] || k0.muc_tieu[0]).id; S.kieu = k0.kieu[0].id; k0.ai.forEach(function (a) { S.ai[a.id] = a.mac_dinh; });
  }
  async function ytDung() {
    var k = YT.kq; if (!k) return;
    if (!KH[k.nen_tang]) { YT.msg = "Kế hoạch chưa có nền tảng hợp lệ. Anh chọn ở ô Chạy ở rồi bấm AI soạn kế hoạch lại."; ve(); return; }
    var nsCu = Number(S.ngan_sach_ngay) > 0 ? S.ngan_sach_ngay : "", kvCu = S.target.khu_vuc;
    chonNen(k.nen_tang);
    var k1 = KH[S.nen];
    S.che_do = "tu_dong";
    if (k1.muc_tieu.some(function (m) { return m.id === k.muc_tieu_id; })) S.muc_tieu = k.muc_tieu_id;
    S.mo_ta_san_pham = k.san_pham || S.mo_ta_san_pham; S.ngan_sach_ngay = nsCu || String(k.ngan_sach_ngay || ""); S.y_tuong = YT.text;
    S.target.khu_vuc = kvCu || k.khu_vuc || "";
    if (!S.kieu) S.kieu = k1.kieu[0].id;
    if (k.noi_dung && k.noi_dung.noi_dung_bai) S.texts = [{ tieu_de: k.noi_dung.tieu_de, noi_dung: k.noi_dung.noi_dung_bai, cta: k.noi_dung.cta }];
    YT.msg = "Đã điền phiếu theo kế hoạch. AI đang chọn mẫu chiến dịch và đối tượng..."; ve();
    await tuDong();
    if (S.da_ai && k.tuoi_tu && k.tuoi_den) {   // giữ độ tuổi theo kế hoạch AI vừa soạn
      S.target.tuoi_tu = k.tuoi_tu; S.target.tuoi_den = k.tuoi_den;
      S.ly_do = S.ly_do.map(function (x) { return /^Đối tượng theo ngành/.test(x) ? "Đối tượng: " + k.tuoi_tu + " đến " + k.tuoi_den + " tuổi theo kế hoạch AI" + (GY && GY.nganh ? ", sở thích và hành vi theo ngành " + GY.nganh : "") + "." : x; });
      ve();
    }
    YT.msg = S.da_ai ? "Phiếu đã sẵn sàng. Anh xem lại rồi chọn một trong hai nút lên chiến dịch ở cột bên phải." : YT.msg;
    var m = goc.querySelector("#ytTt2"); if (m) m.textContent = YT.msg;
  }
  function boTuDong() {
    var h = '<div class="the"><h2>Bài quảng cáo <span class="mo" style="font-weight:500;font-size:14px">(có thể bỏ qua)</span>' + dauXong(coBai()) + '</h2><p class="sub">Có bài đã đăng hoặc hình, video sẵn thì dùng luôn. Chưa có thì để AI tạo, hoặc bỏ qua để AI hỏi lại trước khi tạo. Đổi kiểu bài ở ô <b>Bài quảng cáo</b> phía trên.</p>' + boNguon(true, true) + "</div>";
    h += boCauTruc(true);
    h += boAi(true);
    h += '<div class="the"><button type="button" class="nut cam" data-tudong style="width:100%;padding:14px">' + (S.da_ai ? "🔄 Để AI chọn lại phương án" : "🤖 Để AI lên phương án cho tôi") + "</button>" +
      (S.da_ai ? '<div class="ok-hop" style="margin-top:12px"><b>AI đã chọn giúp anh:</b><ul style="margin:6px 0 0;padding-left:20px">' + S.ly_do.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + '</ul><div class="hang" style="margin-top:10px"><button type="button" class="nut phu nho" data-che="tu_chon">Xem và chỉnh chi tiết</button></div></div>'
        : '<p class="mo" style="font-size:12.5px;margin:8px 0 0">AI chọn dạng chiến dịch, mẫu, đối tượng và ghi lý do từng lựa chọn. Anh vẫn sửa được.</p>') + "</div>";
    return h;
  }
  function boMucTieu() {
    var k = K();
    var h = '<div class="the"><h2>Dạng chiến dịch' + dauXong(!!S.kieu) + '</h2><p class="sub">' + esc(k.ten) + ": chọn kiểu chạy.</p><div class=\"luoi l2\">" + k.kieu.map(function (x) { return '<button type="button" class="tl-the nho' + (S.kieu === x.id ? " on" : "") + '" data-kieu="' + x.id + '"><b>' + esc(x.ten) + '</b><span class="mo">' + esc(x.mo_ta) + "</span></button>"; }).join("") + "</div>";
    h += '<p class="mo" style="margin:10px 0 0;font-size:13px">Tên gọi trong ' + esc(k.ten) + " (khi anh mở trang quản lý của họ): " + esc(k.muc_tieu.filter(function (m) { return m.id === S.muc_tieu; }).map(function (m) { return m.goc; })[0] || "chọn mục tiêu ở phần Anh muốn quảng cáo gì") + ".</p></div>";
    return h + boCauTruc(false);
  }
  function sodo(n, b, chung) { var s = '<span class="tl-cd">CD</span>'; for (var i = 0; i < n; i++) { s += '<span class="tl-nh">N</span>'; } return s + '<span class="mo">' + (chung ? "cùng 1 bài" : "×" + b + " bài") + "</span>"; }
  function boMedia(don) {
    var k = K(), h = "";
    if (S.nen === "google" && S.kieu === "search") h += '<div class="canh">Google Tìm kiếm là quảng cáo chữ: không cần hình hay video. Hình và video chỉ dùng cho Performance Max và Demand Gen.</div>';
    else if (S.nen === "tiktok") h += '<div class="mo" style="margin-bottom:8px">TikTok ưu tiên video dọc 9:16, 15 đến 60 giây. Có thể tải hình nếu chưa có video.</div>';
    h += '<div class="luoi l2">' + khuTai("video", "🎬 Tải video lên", "Kéo thả hoặc bấm chọn. Tải nhiều video, mỗi video là một bài.", S.media.filter(function (id) { return (TEP[id] || {}).loai === "video"; })) +
      khuTai("anh", "🖼 Tải hình ảnh lên", "Kéo thả hoặc bấm chọn. Tải nhiều hình, mỗi hình là một bài.", S.media.filter(function (id) { return (TEP[id] || {}).loai === "anh"; })) + "</div>";
    h += '<h3 style="margin-top:16px">Nội dung bài viết</h3><p class="mo" style="margin:0 0 8px">Dán 1, 2 hoặc 3 nội dung. Mẫu nhiều bài thì mỗi bài dùng một nội dung theo thứ tự.</p>';
    S.texts.forEach(function (t, i) {
      h += '<div class="tl-bai"><div class="hang" style="justify-content:space-between"><b>Nội dung ' + (i + 1) + "</b>" + (S.texts.length > 1 ? '<button type="button" class="nut phu nho" data-xt="' + i + '">Bỏ</button>' : "") + "</div>" +
        '<input type="text" data-tx="' + i + '" data-k="tieu_de" placeholder="Tiêu đề (không bắt buộc)" value="' + esc(t.tieu_de) + '"><textarea rows="3" data-tx="' + i + '" data-k="noi_dung" placeholder="Dán nội dung bài quảng cáo vào đây">' + esc(t.noi_dung) + "</textarea></div>";
    });
    if (S.texts.length < 6) h += '<button type="button" class="nut phu nho" data-them-t>+ Thêm nội dung</button>';
    if (!don) {
      h += '<h3 style="margin-top:16px">Nút kêu gọi</h3><p class="mo" style="margin:0 0 8px">Nút hiện dưới quảng cáo. Mặc định theo mục tiêu, anh đổi cho từng nội dung được.</p><div class="hang">' + S.texts.map(function (t, i) {
        return '<label class="mo">Nội dung ' + (i + 1) + ': <select data-tx="' + i + '" data-k="cta"><option value="">Theo mục tiêu (' + esc(defCta()) + ")</option>" + k.cta.map(function (c) { return "<option" + (t.cta === c ? " selected" : "") + ">" + esc(c) + "</option>"; }).join("") + "</select></label>"; }).join("") + "</div>";
    }
    return h;
  }
  function boNoiDung() {
    var k = K(), n = soBai(), g = ghep(), bd = S.nguon === "bai_dang";
    var h = '<div class="the"><h2>Bài quảng cáo lấy từ đâu?' + dauXong(coBai()) + '</h2><p class="sub">' + esc(k.chi_tiet_bai) + "</p>" + boNguon(false) + "</div>";
    h += '<div class="the"><h2>Ghép thành ' + n + " bài</h2><p class=\"sub\">" + (S.cau_truc.chung ? "Mẫu này chạy cùng một bài ở mọi nhóm." : "Trang tự ghép vào từng bài theo thứ tự. Anh đổi lại được ở từng dòng.") + '</p><div class="bang-cuon"><table><thead><tr><th class="trai">Bài</th>' + (bd ? "<th>Bài đã đăng</th>" : "<th>Hình/video</th><th>Nội dung</th>") + "<th>Nút</th></tr></thead><tbody>";
    g.forEach(function (b) {
      h += '<tr><td class="trai"><b>' + esc(k.cap[1].split(" (")[0]) + " " + b.nhom + "</b>, bài " + b.stt + "</td>";
      if (bd) h += "<td>" + (b.link ? '<span class="mo" style="word-break:break-all">' + esc(b.link.slice(0, 60)) + "</span>" : "Chưa có link") + "</td>";
      else h += '<td><select data-sm="' + b.k + '"><option value="">' + (S.media.length ? "(chưa chọn)" : "Chưa có") + "</option>" + S.media.map(function (id) { return '<option value="' + id + '"' + (b.media_id === id ? " selected" : "") + ">" + esc((TEP[id] || {}).ten || id) + "</option>"; }).join("") + "</select></td>" +
        '<td><select data-st="' + b.k + '">' + S.texts.map(function (t, i) { return '<option value="' + i + '"' + (b.ti === i ? " selected" : "") + ">Nội dung " + (i + 1) + (t.slides && t.slides.length ? " (" + t.slides.length + " tấm)" : "") + (t.tieu_de ? ": " + esc(t.tieu_de.slice(0, 18)) : "") + "</option>"; }).join("") + "</select></td>";
      h += "<td>" + esc(b.cta) + "</td></tr>";
    });
    h += "</tbody></table></div>";
    var w = canhBao().filter(function (x) { return /hình|video|nội dung|link|bài đã đăng/i.test(x); });
    if (w.length) h += '<div class="canh" style="margin-top:12px">' + w.map(esc).join("<br>") + "</div>";
    return h + "</div>";
  }
  function chips(key, ds, goiY, nhanThem) {
    var cs = (ds.length ? ds.map(function (x, i) { return '<span class="tl-chip">' + esc(x) + '<button type="button" data-xc="' + key + '|' + i + '" aria-label="Bỏ">✕</button></span>'; }).join("") : '<span class="mo">Chưa chọn</span>');
    var gy = (goiY || []).filter(function (x) { return ds.indexOf(x) < 0; });
    return '<div class="tl-chips">' + cs + '</div>' + (gy.length ? '<div class="tl-goiy"><span class="mo">Gợi ý:</span> ' + gy.map(function (x) { return '<button type="button" class="chip nho" data-tc="' + key + '|' + esc(x) + '">+ ' + esc(x) + "</button>"; }).join(" ") + "</div>" : "") +
      '<input type="text" data-add="' + key + '" placeholder="' + (nhanThem || "Gõ rồi bấm Enter để thêm") + '" class="tl-them">';
  }
  var GY = null;
  function boDoiTuong() {
    var k = K(), t = S.target, g = GY || {};
    var h = '<div class="the"><h2>Đối tượng: quảng cáo cho ai?' + dauXong(!!S.target.khu_vuc) + '</h2><p class="sub">Bấm Gợi ý để trang đề xuất theo sản phẩm của anh. Anh chỉnh lại thoải mái.</p>' +
      '<div class="hang" style="margin-bottom:10px"><button type="button" class="nut" data-goiy>✨ Gợi ý đối tượng cho sản phẩm của tôi</button>' + (g.nganh ? '<span class="mo">Nhận ra ngành: <b>' + esc(g.nganh) + "</b></span>" : "") + "</div>" +
      (g.ghi_chu ? '<div class="mo" style="margin-bottom:8px;font-size:13px">' + esc(g.ghi_chu) + "</div>" : "") +
      '<div class="cot2"><label class="truong">Khu vực<input type="text" data-t="khu_vuc" value="' + esc(t.khu_vuc) + '"></label><label class="truong">Giới tính<select data-t="gioi_tinh">' + ["Cả nam và nữ", "Nam", "Nữ", "Nữ là chính", "Cả nam và nữ (phụ huynh)"].map(function (x) { return "<option" + (t.gioi_tinh === x ? " selected" : "") + ">" + x + "</option>"; }).join("") + "</select></label>" +
      '<label class="truong">Tuổi từ<input type="number" min="13" max="65" data-t="tuoi_tu" value="' + t.tuoi_tu + '"></label><label class="truong">Tuổi đến<input type="number" min="13" max="65" data-t="tuoi_den" value="' + t.tuoi_den + '"></label></div>';
    if (S.nen === "google") h += '<div class="truong">Từ khoá khách hay gõ trên Google</div>' + chips("tu_khoa", t.tu_khoa, g.tu_khoa, "Gõ từ khoá rồi Enter");
    else h += '<div class="truong">Sở thích</div>' + chips("so_thich", t.so_thich, g.so_thich) + '<div class="truong" style="margin-top:10px">Hành vi</div>' + chips("hanh_vi", t.hanh_vi, g.hanh_vi);
    h += '<div class="truong" style="margin-top:10px">Loại trừ (không muốn hiện cho ai)</div>' + chips("loai_tru", S.loai_tru, (g.loai_tru || []).concat(k.loai_tru));
    if (S.cau_truc.nhom > 1) {
      h += '<h3 style="margin-top:16px">Mỗi ' + esc(k.cap[1].split(" (")[0].toLowerCase()) + " một kiểu đối tượng</h3><p class=\"mo\" style=\"margin:0 0 8px\">Mẫu có " + S.cau_truc.nhom + " nhóm. Mỗi nhóm nên khác nhau để biết kiểu nào ra khách tốt.</p>";
      for (var i = 0; i < S.cau_truc.nhom; i++) { var gi = S.nhom[i] || { ten: "", mo_ta: "" }; h += '<div class="tl-bai"><b>Nhóm ' + (i + 1) + '</b><input type="text" data-nh="' + i + '" data-k="ten" placeholder="Tên nhóm" value="' + esc(gi.ten) + '"><input type="text" data-nh="' + i + '" data-k="mo_ta" placeholder="Đối tượng của nhóm này" value="' + esc(gi.mo_ta) + '"></div>'; }
      if (g.nhom) h += '<button type="button" class="nut phu nho" data-nhom-goiy>Điền nhóm theo gợi ý</button>';
    }
    return h + "</div>";
  }
  function boTuyChinh() {
    var k = K(), h = '<div class="the"><h2>Quảng cáo tuỳ chỉnh: nhắm lại người đã quan tâm <span class="mo" style="font-weight:500;font-size:14px">(có thể bỏ qua)</span>' + dauXong(S.tuy_chinh.length > 0 || S.tuong_tu.bat) + '</h2><p class="sub">Người từng tương tác với anh thường mua dễ và rẻ hơn người lạ. Tick nhóm muốn chạy cho họ.</p>';
    k.tuy_chinh.forEach(function (x) { h += '<label class="tl-ck"><input type="checkbox" data-tc2="' + x.id + '"' + (S.tuy_chinh.indexOf(x.id) >= 0 ? " checked" : "") + '><span><b>' + esc(x.ten) + '</b> <span class="mo">' + esc(x.mo_ta) + "</span>" + (x.can ? '<br><span class="tl-can">Cần: ' + esc(x.can) + "</span>" : "") + "</span></label>"; });
    if (S.tuy_chinh.indexOf("danh_sach") >= 0) h += '<div style="margin:8px 0 0 28px">' + khuTai("danh_sach", "Tải file danh sách khách hàng", "CSV gồm số điện thoại hoặc email. Chỉ dùng cho tài khoản quảng cáo này.", S.file_khach) + "</div>";
    var tt = k.tuong_tu;
    h += '<div class="tl-tt-hop"><label class="tl-ck"><input type="checkbox" data-tt-bat' + (S.tuong_tu.bat ? " checked" : "") + '><span><b>' + esc(tt.ten) + '</b> <span class="mo">' + esc(tt.mo_ta) + "</span></span></label>";
    if (S.tuong_tu.bat) h += '<div class="hang" style="margin:6px 0 0 28px"><label class="mo">Lấy theo: <select data-tt-nguon><option value="">Khách tốt nhất</option>' + k.tuy_chinh.map(function (x) { return "<option value=\"" + x.id + '"' + (S.tuong_tu.nguon === x.id ? " selected" : "") + ">" + esc(x.ten) + "</option>"; }).join("") + '</select></label><label class="mo">Mức giống: <select data-tt-pt>' + tt.phan_tram.map(function (p) { return "<option" + (S.tuong_tu.phan_tram === p ? " selected" : "") + " value=\"" + p + "\">" + p + "%</option>"; }).join("") + "</select></label></div>";
    return h + "</div></div>";
  }
  function boAi() {
    var k = K(), h = '<div class="the"><h2>AI tự tối ưu: bật hay tắt? <span class="mo" style="font-weight:500;font-size:14px">(có thể bỏ qua)</span></h2><p class="sub">' + esc(k.ten) + " có nhiều chức năng AI tự điều chỉnh. Mặc định đang TẮT hết để anh kiểm soát. Muốn nền tảng tự tối ưu thì bật từng cái, hoặc bấm Bật theo khuyến nghị.</p>" +
      '<div class="hang" style="margin-bottom:8px"><button type="button" class="nut phu nho" data-ai="khuyen">Bật theo khuyến nghị</button><button type="button" class="nut phu nho" data-ai="tat">Tắt hết AI</button><button type="button" class="nut phu nho" data-ai="bat">Bật hết</button></div>';
    k.ai.forEach(function (a) { var on = S.ai[a.id] !== undefined ? S.ai[a.id] : a.mac_dinh; h += '<label class="tl-ai"><input type="checkbox" role="switch" data-aid="' + a.id + '"' + (on ? " checked" : "") + '><span class="tl-sw"></span><span><b>' + esc(a.ten) + '</b><br><span class="mo">' + (on ? "Đang bật: " + esc(a.bat) : "Đang tắt: " + esc(a.tat)) + "</span></span></label>"; });
    return h + "</div>";
  }
  function boNganSach() {
    var k = K();
    var h = '<div class="the"><h2>Ngân sách và lịch' + dauXong(Number(S.ngan_sach_ngay) > 0) + '</h2><div class="cot2"><label class="truong">Ngân sách mỗi ngày<input type="number" min="0" step="any" data-f="ngan_sach_ngay" value="' + esc(S.ngan_sach_ngay) + '"></label>' +
      '<label class="truong">Tài khoản chạy<select data-f="tai_khoan"><option value="">Để AI chọn</option>' + taiKhoanOpts() + "</select></label>" +
      '<label class="truong">Chạy từ ngày<input type="date" data-f="tu_ngay" value="' + esc(S.tu_ngay) + '"></label><label class="truong">Đến ngày (bỏ trống nếu chạy liên tục)<input type="date" data-f="den_ngay" value="' + esc(S.den_ngay) + '"></label></div>' +
      '<div class="hang" style="margin-top:8px">' + [100000, 200000, 300000, 500000, 1000000].map(function (v) { return '<button type="button" class="chip" data-ns="' + v + '">' + so(v) + "</button>"; }).join("") + '</div><div id="tlDuKien" class="mo" style="margin-top:10px"></div>';
    h += '<label class="truong" style="margin-top:12px">Tên chiến dịch<input type="text" data-f="ten" value="' + esc(S.ten) + '" placeholder="Tự đặt tên nếu để trống"></label><label class="truong">Ghi chú thêm cho AI<textarea rows="2" data-f="ghi_chu">' + esc(S.ghi_chu) + "</textarea></label></div>";
    return h;
  }
  function taiKhoanOpts() {
    var v = KN[S.nen] || { api: [], mcp: [] }, o = "";
    v.api.forEach(function (a) { o += '<option value="' + esc(a.ma_tk) + '"' + (S.tai_khoan === a.ma_tk ? " selected" : "") + ">" + esc(a.ten) + " (API)</option>"; });
    v.mcp.forEach(function (a) { o += '<option value="mcp:' + esc(a.id) + '"' + (S.tai_khoan === "mcp:" + a.id ? " selected" : "") + ">" + esc(a.ten) + " (MCP)</option>"; });
    return o;
  }
  var tDk = 0;
  function duKien() {
    clearTimeout(tDk);
    tDk = setTimeout(async function () {
      var el = goc.querySelector("#tlDuKien"), ns = Number(S.ngan_sach_ngay); if (!el) return;
      if (!(ns > 0)) { el.textContent = "Nhập ngân sách để xem dự kiến."; return; }
      var j = await api("/tisa-quang-cao/api/du-kien?nen=" + S.nen + "&ngan_sach=" + ns); if (!j.ok) { el.textContent = j.error || ""; return; }
      var dv = j.tien_te === "VND" ? " đ" : " " + j.tien_te;
      el.innerHTML = j.cpa_tham_chieu ? "<b>Dự kiến " + (j.ket_qua_ngay).toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + " kết quả mỗi ngày</b>, khoảng " + so(j.ket_qua_thang) + " kết quả và " + so(j.chi_phi_thang) + dv + " trong 30 ngày (giá mỗi kết quả tham chiếu " + so(j.cpa_tham_chieu) + dv + (j.che_do === "mau" ? ", dữ liệu mẫu" : "") + "). Chỉ là ước lượng." : esc(j.ghi_chu);
    }, 400);
  }
  function boPhieuNho() { return '<div id="tlTt" class="mo" style="margin-top:6px;font-size:13px"></div>'; }
  function tomTat() {
    var k = K(); if (!k) return '<div class="the"><h3>Tóm tắt</h3><p class="mo">' + (laAi() ? "AI sẽ chọn nền tảng khi soạn kế hoạch. Anh kể ý tưởng rồi bấm <b>AI soạn kế hoạch</b>, hoặc chọn sẵn ở ô <b>Chạy ở</b>." : "Chọn nền tảng ở phần <b>Chạy ở đâu?</b> để bắt đầu.") + "</p>" + boPhieuNho() + "</div>";
    var g = ghep(), ct = S.cau_truc, mt = k.muc_tieu.filter(function (m) { return m.id === S.muc_tieu; })[0], ky = k.kieu.filter(function (m) { return m.id === S.kieu; })[0];
    var hs = HO_SO.filter(function (x) { return x.id === S.ho_so_id; })[0];
    var h = '<div class="the tl-tt-the"><h3>Tóm tắt phiếu</h3><div class="mo" style="font-size:13px">' + esc(k.ten) + " · " + (laAi() ? "Nhờ AI làm" : "Tự chọn từng bước") + (hs ? " · " + esc(hs.ten) : "") + "</div>";
    h += '<div class="tl-cay"><div class="tl-c0"><b>' + esc(k.cap[0]) + ":</b> " + esc(S.ten || autoTen()) + '<div class="mo">' + esc(mt ? mt.ten : "Chưa chọn mục tiêu") + (ky ? " · " + esc(ky.ten) : "") + (Number(S.ngan_sach_ngay) ? " · " + so(S.ngan_sach_ngay) + "/ngày" : "") + "</div></div>";
    for (var n = 1; n <= ct.nhom; n++) {
      var gi = S.nhom[n - 1] || {};
      h += '<div class="tl-c1"><b>' + esc(k.cap[1].split(" (")[0]) + " " + n + "</b>" + (gi.ten ? ": " + esc(gi.ten) : "");
      g.filter(function (b) { return b.nhom === n; }).forEach(function (b) { h += '<div class="tl-c2">' + (b.link ? '<span class="tl-thumb tl-file">🔗</span>' : b.media_id ? thumb(b.media_id) : (b.slides && b.slides.length ? '<span class="tl-thumb tl-file">' + b.slides.length + " tấm</span>" : "")) + "<div><b>Bài " + b.stt + "</b> " + (b.link ? '<span class="mo">bài đã đăng</span>' : b.tieu_de ? esc(b.tieu_de.slice(0, 40)) : '<span class="mo">chưa có tiêu đề</span>') + '<div class="mo">Nút: ' + esc(b.cta) + (b.dung_lai ? " · dùng lại" : "") + "</div></div></div>"; });
      h += "</div>";
    }
    h += "</div>";
    var ai = k.ai.map(function (a) { var on = S.ai[a.id] !== undefined ? S.ai[a.id] : a.mac_dinh; return (on ? "● " : "○ ") + a.ten; });
    h += '<div class="mo" style="font-size:13px;margin-top:8px">Đối tượng: ' + esc(S.target.khu_vuc || "chưa ghi khu vực") + ", " + S.target.tuoi_tu + " đến " + S.target.tuoi_den + " tuổi" + (S.tuy_chinh.length ? ", tuỳ chỉnh " + S.tuy_chinh.length + " nhóm" : "") + (S.tuong_tu.bat ? ", tương tự " + S.tuong_tu.phan_tram + "%" : "") + "</div>" +
      '<details style="margin-top:8px"><summary>AI tự tối ưu</summary><div class="mo" style="font-size:13px">' + ai.map(esc).join("<br>") + "</div></details>";
    var w = canhBao();
    h += (w.length ? '<div class="canh" style="margin-top:10px;font-size:13px"><b>Cần xem lại:</b><br>' + w.map(esc).join("<br>") + "</div>" : '<div class="ok-hop" style="margin-top:10px;font-size:13px">Phiếu đã đủ thông tin chính.</div>');
    h += giaoHtml();
    return h;
  }
  /* ---------- giao việc cho cộng sự quảng cáo ---------- */
  var TT_VIEC = { "hang-doi": "Chờ TISA BOT nhận việc", "dang-chay": "Đang làm", "can-sua": "Đang sửa theo góp ý", "da-duyet": "Đã duyệt, đang làm tiếp", "cho-duyet": "Làm xong, chờ anh duyệt", "xong": "Xong", "dung": "Đang tạm dừng", "cho-that": "Chờ thao tác thật" };
  var TT_PHAN = { wait: "Chờ", recv: "Đã nhận", run: "Đang làm", done: "Xong", duyet: "Chờ anh duyệt", owner: "Cần anh làm", err: "Kẹt", sua: "Đang sửa", given: "Đã giao", that: "Đang làm thật" };
  async function taiCS() {
    var nen = S.nen; if (!nen || CSDS[nen] !== undefined) return;
    CSDS[nen] = null;
    var j = await api("/tisa-quang-cao/api/cong-su?nen=" + nen);
    if (j.ok) { CSDS[nen] = j.ung_vien; delete CS_LOI[nen]; } else { CSDS[nen] = []; CS_LOI[nen] = j.error || "Chưa đọc được đội hình."; }
    vePhai();
  }
  function giaoHtml() {
    var h = "";
    if (GV) {
      var st = GV.st || {}, tt = TT_VIEC[st.status] || "Đã gửi, chờ TISA BOT nhận";
      h += '<div class="tl-gv"><div class="hang" style="justify-content:space-between"><b>🚀 Đã giao cho ' + esc(GV.cs.ten) + '</b><span class="nhan-tt ' + (st.xong ? "ok" : "dung") + '">' + (st.xong ? "●" : "◌") + " " + esc(tt) + '</span></div><div class="mo" style="font-size:12.5px">' + esc(GV.cs.chuc_danh || "") + (GV.cs.phong ? " · " + esc(GV.cs.phong) : "") + "</div>";
      if (st.plan && st.plan.length) h += '<div style="margin-top:8px">' + st.plan.map(function (p) { return '<div class="tl-gv-p"><b>' + esc(p.ten || p.agent) + '</b> <span class="mo">' + esc(TT_PHAN[p.state] || p.state || "") + (p.pct && p.state === "run" ? " " + p.pct + "%" : "") + "</span>" + ((p.log && p.log.length) ? '<div class="mo" style="font-size:12.5px">' + esc(p.log[p.log.length - 1]) + "</div>" : "") + "</div>"; }).join("") + "</div>";
      else h += '<div class="mo" style="font-size:13px;margin-top:6px">' + (st.status === "hang-doi" || !st.status ? "Tâm Tổng Quản đang nhận việc và chuyển cho " + esc(GV.cs.ten) + "..." : "Đang chờ kế hoạch từ Tâm...") + "</div>";
      if (st.summary) h += '<div class="doc" style="font-size:13px;margin-top:8px;white-space:pre-wrap">' + esc(st.summary) + "</div>";
      h += '<div class="hang" style="margin-top:10px"><button type="button" class="nut nho" data-gv-mo>Mở trong Giao dự án</button><button type="button" class="nut phu nho" data-gv-moi>Giao việc khác</button></div>' +
        '<p class="mo" style="font-size:12.5px;margin:8px 0 0">' + (st.xong ? "Xong rồi thì anh xem chiến dịch ở tab Chiến dịch hoặc trên nền tảng (đang tạm dừng). Anh nhắn đồng ý thì mới bật." : "Cộng sự làm xong sẽ để chiến dịch ở trạng thái tạm dừng và báo anh duyệt.") + "</p></div>";
      return h;
    }
    /* HAI nút lên chiến dịch, anh tự chọn:
       ⚡ AI lên tự động = giao cộng sự quảng cáo làm qua API/MCP (cần kết nối có quyền tạo chiến dịch).
       🌐 AI bấm trên trình duyệt = TISA BOT mở trang quản lý quảng cáo và tự bấm (luôn dùng được).
       Phía trên là khung báo API, MCP, trình duyệt đã sẵn sàng chưa. */
    var dg = duongGiao(), ds = CSDS[S.nen], loi = CS_LOI[S.nen], csOk = !!(ds && ds.length);
    h += '<div class="tl-giao">' + khungKn(dg);
    h += '<button type="button" class="tl-len' + (dg.san ? " chinh" : "") + '" data-giao-api' + (dg.san && csOk ? "" : " disabled") + '><span class="tl-len-ico" aria-hidden="true">⚡</span><span><b>AI lên tự động</b><small>' + (dg.san ? "Qua API/MCP · nhanh, không cần mở trang" : "Cần nối API hoặc MCP có quyền tạo chiến dịch") + "</small></span></button>";
    if (dg.san) {
      if (ds === undefined || ds === null) h += '<div class="tl-duong">Đang xem ai phụ trách quảng cáo...</div>';
      else if (loi) h += '<div class="canh" style="font-size:13px;margin-top:6px">' + esc(loi) + "</div>";
      else if (!ds.length) h += '<div class="canh" style="font-size:13px;margin-top:6px">Chưa có cộng sự nào phụ trách quảng cáo. Vào Cài đặt đội thêm một người, hoặc dùng nút trình duyệt bên dưới.</div>';
      if (csOk) { var cur = ds.filter(function (x) { return x.id === csChon; })[0] || ds[0];
        h += '<label class="tl-duong">Người làm: <select data-cs aria-label="Cộng sự phụ trách">' + ds.map(function (x) { return '<option value="' + esc(x.id) + '"' + (x.id === cur.id ? " selected" : "") + ">" + esc(x.ten) + (x.chuc_danh ? " · " + esc(x.chuc_danh) : "") + "</option>"; }).join("") + "</select></label>"; }
      if (loi || (ds && !ds.length)) h += '<button type="button" class="nut phu nho" data-gui-chat style="margin-top:6px;width:100%">Dán vào chat</button>';
    }
    h += '<button type="button" class="tl-len' + (dg.san ? "" : " chinh") + '" data-giao-td><span class="tl-len-ico" aria-hidden="true">🌐</span><span><b>AI bấm trên trình duyệt</b><small>Mở trang quảng cáo, bấm từng bước như người · anh xem được</small></span></button>';
    h += '<p class="mo" style="font-size:12.5px;margin:10px 0 0">Cả hai cách đều tạo chiến dịch ở trạng thái <b>tạm dừng</b>, anh bấm Bật mới tốn tiền.</p>' +
      '<div class="hang" style="margin-top:10px"><button type="button" class="nut phu nho" data-luu>Lưu nháp</button></div><div id="tlTt" class="mo" style="margin-top:6px;font-size:13px"></div></div>';
    return h;
  }
  /* Khung báo kết nối của nền tảng đang chọn: API, MCP, trình duyệt; kết luận nút nào dùng được */
  function khungKn(dg) {
    var v = KN[S.nen] || {}, apis = v.api || [], mcp = v.mcp || [], ten = (K() || {}).ten || "nền tảng";
    var dong = function (loai, tt, phu) { return '<div class="tl-kn-dong"><span class="tl-kn-loai">' + loai + '</span><span class="tl-kn-gt"><span class="nhan-tt ' + tt[0] + '">' + tt[1] + "</span>" + (phu ? "<small>" + phu + "</small>" : "") + "</span></div>"; };
    var apiOk = apis.filter(function (x) { return x.ok; }), apiTt = apiOk.length ? ["ok", "● Đã nối · " + apiOk.length + " tài khoản"] : apis.length ? (apis.some(function (x) { return x.da_kiem_tra; }) ? ["loi", "⚠ Có mã nhưng đang lỗi"] : ["dung", "◌ Có mã, chưa kiểm tra"]) : ["dung", "○ Chưa nối"];
    var apiPhu = apiOk.length ? "Tạo được nếu mã có quyền Quản lý chiến dịch" : apis.length ? esc(apis.map(function (x) { return x.ten; }).join(", ")) : "";
    var ghi = mcp.filter(function (x) { return x.ok && !x.chi_doc; }), doc = mcp.filter(function (x) { return x.ok && x.chi_doc; }), bat = mcp.filter(function (x) { return x.bat; });
    var mcpTt = ghi.length ? ["ok", "● Đã nối · tạo được chiến dịch"] : doc.length ? ["dung", "◐ Đã nối · chỉ xem số"] : bat.length ? (bat.some(function (x) { return x.da_kiem_tra; }) ? ["loi", "⚠ Đang lỗi"] : ["dung", "◌ Chưa kiểm tra"]) : mcp.length ? ["dung", "○ Đang tắt"] : ["dung", "○ Chưa nối"];
    var mcpDs = (ghi.length ? ghi : doc.length ? doc : bat.length ? bat : mcp), mcpPhu = mcpDs.length ? esc(mcpDs.map(function (x) { return x.ten; }).join(", ")) + (!ghi.length && doc.length ? ". Chưa tạo được chiến dịch" : "") : "";
    if (!ghi.length && !doc.length && bat.length) { var tb2 = bat.map(function (x) { return x.thong_bao; }).filter(Boolean)[0]; if (tb2) mcpPhu += (mcpPhu ? ". " : "") + esc(tb2.slice(0, 120)); }
    var h = '<div class="tl-kn"><div class="tl-kn-dau"><b>Kết nối của ' + esc(ten) + '</b><button type="button" class="tl-kn-lai" data-kn-lai>↻ Kiểm tra lại</button></div>' +
      dong("API", apiTt, apiPhu) + dong("MCP", mcpTt, mcpPhu) +
      dong("Trình duyệt", ["ok", "● Luôn dùng được"], "Anh đăng nhập trang quảng cáo một lần khi AI nhờ");
    h += '<div class="tl-kn-kl ' + (dg.san ? "ok" : "chua") + '">' + (dg.san ? "✅ Đủ điều kiện cho nút <b>⚡ AI lên tự động</b>." : "Nút <b>⚡ AI lên tự động</b> chưa dùng được: " + esc(dg.lyDo.charAt(0).toLowerCase() + dg.lyDo.slice(1)) + ". Nút <b>🌐 trình duyệt</b> vẫn dùng được.") +
      ' <span class="tl-noi" data-noi="' + esc(S.nen) + '">Nối thêm ở tab Kết nối →</span></div></div>';
    return h;
  }
  async function kiemLaiKn(nut) {
    var v = KN[S.nen] || {}; if (nut) { nut.disabled = true; nut.textContent = "Đang kiểm tra..."; }
    var viec = (v.api || []).map(function (x) { return api("/tisa-quang-cao/api/tai-khoan/" + x.id + "/kiem-tra", {}); })
      .concat((v.mcp || []).filter(function (x) { return x.bat; }).map(function (x) { return api("/connect/health/check", { id: x.id }); }));
    try { await Promise.all(viec); } catch (e) {}
    await quet(true); vePhai(); Q.toast("Đã kiểm tra lại kết nối " + ((K() || {}).ten || "") + ".");
  }
  function duongGiao() {
    var v = KN[S.nen] || {}, tenTrang = (K() || {}).ten || "nền tảng";
    var mcpGhi = (v.mcp || []).some(function (x) { return x.ok && !x.chi_doc; }), mcpDoc = (v.mcp || []).some(function (x) { return x.ok && x.chi_doc; }), apiOk = (v.api || []).some(function (x) { return x.ok; });
    var san = mcpGhi || apiOk;
    var lyDo = mcpGhi ? "đã có kết nối MCP có quyền tạo chiến dịch" : apiOk ? "đã nối bằng API (cần mã có quyền Quản lý chiến dịch, thiếu quyền thì cộng sự báo và anh đổi sang trình duyệt)" : mcpDoc ? "Kết nối MCP mới chỉ đọc số liệu, chưa tạo được chiến dịch" : "Chưa nối API hay MCP cho " + tenTrang;
    return { duong: DUONG_TAY || (san ? "api" : "td"), san: san, lyDo: lyDo };
  }
  /* Cách 2: lưu phiếu rồi giao thẳng cho TISA BOT (tự cấp Toàn quyền, không xóa tệp) */
  async function cach2() {
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Nhập ngân sách mỗi ngày trước nhé."); return; }
    tb("Đang chuẩn bị phiếu...");
    var j = await luu(); if (!j) return;
    if (!j.lenh_tisabot) { tb("Chưa soạn được lời nhờ. Anh thử lưu nháp rồi bấm lại."); return; }
    tb("Đã giao cho TISA BOT, xem tiến độ ở khung chat.");
    if (window.TisaQC && window.TisaQC.nho) window.TisaQC.nho(j.lenh_tisabot, "Tạo chiến dịch quảng cáo");
  }
  async function giaoViec() {
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Nhập ngân sách mỗi ngày trước nhé."); return; }
    var nut = goc.querySelector("[data-giao-api]") || goc.querySelector("[data-gui]"); if (nut) nut.disabled = true; tb("Đang giao việc...");
    var j = await api("/tisa-quang-cao/api/giao-viec", { phieu: phieu(), cong_su: csChon || ((CSDS[S.nen] || [])[0] || {}).id || "" });
    if (!j.ok) { if (nut) nut.disabled = false; tb(j.error || "Chưa giao được."); if (j.chua_co_bang) { CS_LOI[S.nen] = j.error; vePhai(); } return; }
    S.id = j.phieu_id || S.id; GV = { viec: j.viec, cs: j.cong_su, st: { status: "hang-doi" } }; vePhai(); batGv();
  }
  function batGv() {
    clearInterval(henGv); var t0 = Date.now();
    var chay = async function () {
      if (!GV || Date.now() - t0 > 40 * 60 * 1000) { clearInterval(henGv); return; }
      if (document.visibilityState !== "visible") return;
      var j = await api("/tisa-quang-cao/api/giao-viec/" + GV.viec); if (!j.ok || !GV) return;
      GV.st = j; vePhai(); if (j.xong) clearInterval(henGv);
    };
    chay(); henGv = setInterval(chay, 4000);
  }
  function autoTen() { var m = K().muc_tieu.filter(function (x) { return x.id === S.muc_tieu; })[0]; return (GY && GY.nganh ? GY.nganh + " - " : "") + (m ? m.ten : "Chiến dịch mới") + " - " + hom(); }

  function ve() {
    if (!goc || !KH) return;
    var vi = goc.querySelector(".tl-trai"), cuon = vi ? vi.scrollTop : 0, ts = window.scrollY;
    var cot = bo1();
    if (laAi()) {   // Nhờ AI làm: hộp kể ý tưởng + ô nhanh, kế hoạch AI, rồi phiếu khi đã có nền tảng
      cot += boYT();
      if (S.nen) cot += boGoc() + boTuDong();
    } else if (S.che_do === "tu_chon" && S.nen) {
      cot += boGoc() + boMucTieu() + boNoiDung() + boDoiTuong() + boTuyChinh() + boAi() + boNganSach();
    }
    goc.innerHTML = '<div class="tl-luoi"><div class="tl-trai">' + cot + '</div><div class="tl-phai" id="tlPhai">' + tomTat() + "</div></div>";
    window.scrollTo(0, ts);
    duKien();
    if (window.TisaStudio && S.nguon === "ai") TisaStudio.sauVe();
    if (S.nen && CSDS[S.nen] === undefined) taiCS();
  }
  function vePhai() { var p = goc.querySelector("#tlPhai"); if (p) p.innerHTML = tomTat(); }

  /* ---------- tự động: luật chọn giúp người mới ---------- */
  async function tuDong() {
    var k = K(), ly = [];
    if (!S.mo_ta_san_pham.trim()) { tb("Anh viết vài dòng về sản phẩm hoặc dịch vụ trước nhé."); return; }
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb(laAi() ? "Anh nhập tiền mỗi ngày ở ô Tiền mỗi ngày phía trên trước nhé." : "Anh nhập ngân sách mỗi ngày trước nhé."); return; }
    if (!S.muc_tieu) S.muc_tieu = k.muc_tieu[0].id;
    var mt = k.muc_tieu.filter(function (m) { return m.id === S.muc_tieu; })[0];
    ly.push("Mục tiêu: " + mt.ten + ".");
    var ns = Number(S.ngan_sach_ngay), co = Math.max(S.media.length, S.texts.filter(function (x) { return x.noi_dung; }).length, 1);
    if (S.nen === "facebook") S.kieu = S.muc_tieu === "ban_hang" ? "advantage_plus" : "thuong";
    else if (S.nen === "tiktok") S.kieu = ["ban_hang", "khach", "truy_cap"].indexOf(S.muc_tieu) >= 0 ? "smart_plus" : "thu_cong";
    else S.kieu = ["nhan_dien", "xem_video"].indexOf(S.muc_tieu) >= 0 ? "demand_gen" : (S.muc_tieu === "ban_hang" && S.media.length >= 3 ? "pmax" : "search");
    ly.push("Dạng chiến dịch: " + k.kieu.filter(function (x) { return x.id === S.kieu; })[0].ten + ".");
    var co2 = S.nguon === "bai_dang" ? Math.max(S.links.filter(function (x) { return x.ok; }).length, 1) : co;
    if (S.cau_chon !== "auto") {
      var mc = MAU.filter(function (x) { return x.id === S.cau_chon; })[0];
      if (mc) S.cau_truc = { id: mc.id, nhom: mc.nhom, bai: mc.bai, chung: !!mc.chung };
      ly.push("Cấu trúc " + (mc ? mc.ten : S.cau_truc.nhom + " nhóm, mỗi nhóm " + S.cau_truc.bai + " bài") + ": theo lựa chọn của anh.");
    } else {
      var id = "1-1-1";
      if (ns >= 300000 && co2 >= 3) id = "1-3-3"; else if (ns >= 150000 && co2 >= 2) id = "1-1-3"; else if (ns >= 400000 && co2 === 1) id = "1-3-1";
      var m = MAU.filter(function (x) { return x.id === id; })[0];
      S.cau_truc = { id: m.id, nhom: m.nhom, bai: m.bai, chung: !!m.chung };
      ly.push("Cấu trúc " + m.ten + (id === "1-1-1" ? ": ngân sách còn nhỏ nên dồn vào một bài cho dễ theo dõi." : id === "1-1-3" ? ": thử vài bài trong cùng một nhóm, tiết kiệm hơn." : id === "1-3-1" ? ": chỉ có một bài nên thử 3 nhóm đối tượng cùng bài đó." : ": đủ ngân sách để thử nhiều kiểu đối tượng."));
    }
    S.slotMedia = {}; S.slotText = {};
    var g = await api("/tisa-quang-cao/api/goi-y-target?nen=" + S.nen + "&khu_vuc=" + encodeURIComponent(S.target.khu_vuc) + "&mo_ta=" + encodeURIComponent(S.mo_ta_san_pham));
    if (g.ok) { GY = g; S.target.tuoi_tu = g.tuoi_tu; S.target.tuoi_den = g.tuoi_den; S.target.gioi_tinh = g.gioi_tinh; S.target.so_thich = g.so_thich.slice(0, 5); S.target.hanh_vi = g.hanh_vi.slice(0, 3); S.target.tu_khoa = g.tu_khoa.slice(0, 8); S.loai_tru = g.loai_tru.slice(0, 5);
      S.nhom = g.nhom.slice(0, S.cau_truc.nhom).map(function (x) { return { ten: x.ten, mo_ta: x.mo_ta }; });
      ly.push("Đối tượng theo ngành " + g.nganh + ": " + g.tuoi_tu + " đến " + g.tuoi_den + " tuổi" + (S.nen === "google" ? ", từ khoá khách hay gõ." : ", sở thích và hành vi liên quan.")); }
    if (!S.ai_tay) { S.ai = {}; k.ai.forEach(function (a) { S.ai[a.id] = a.mac_dinh; }); ly.push("AI tự tối ưu: đang TẮT hết (mặc định). Anh bật từng cái ở phần AI tự tối ưu nếu muốn."); }
    else ly.push("AI tự tối ưu: theo lựa chọn bật tắt của anh.");
    S.texts.forEach(function (t) { if (!t.cta) t.cta = ""; });
    if (S.nguon === "bai_dang") ly.push(S.links.some(function (x) { return x.ok; }) ? "Chạy đúng " + S.links.filter(function (x) { return x.ok; }).length + " bài đã đăng anh dán link." : "Anh chưa dán link bài nào hợp lệ.");
    else if (!S.media.length && !(S.nen === "google" && S.kieu === "search")) ly.push("Anh chưa có hình hoặc video: hãy chọn AI tạo giúp ở phần Bài quảng cáo, hoặc để AI hỏi lại trước khi tạo.");
    if (!S.ten) S.ten = autoTen();
    S.ly_do = ly; S.da_ai = true; ve();
    var p = goc.querySelector("[data-tudong]"); if (p) p.scrollIntoView({ block: "center", behavior: "smooth" });
  }
  async function ytChay() {
    var say = function (m) { S.yt_msg = m; var e = goc.querySelector("#ytTt"); if (e) e.textContent = m; };
    if ((S.y_tuong || "").trim().length < 12) { say("Anh gõ ý tưởng dài hơn một chút nhé: chạy cái gì, cho ai, ở đâu."); return; }
    if (!(Number(S.ngan_sach_ngay) > 0)) { say("Anh nhập tiền mỗi ngày ở ô Tiền mỗi ngày trước nhé."); return; }
    var nut = goc.querySelector("[data-ytuong-chay]"); if (nut) nut.disabled = true;
    if (!S.mo_ta_san_pham.trim()) S.mo_ta_san_pham = S.y_tuong.trim().slice(0, 1500);
    say("Trợ lý đang chọn mục tiêu, cấu trúc và đối tượng...");
    await tuDong();
    if (!S.da_ai) { if (nut) nut.disabled = false; return; }
    say("AI đang viết nội dung bài quảng cáo (khoảng 20 đến 60 giây)...");
    var cau = S.cau_truc || {}, so = Math.max(1, Math.min(3, cau.chung ? 1 : (cau.nhom || 1) * (cau.bai || 1)));
    var j = await api("/tisa-quang-cao/api/ai/viet", { nen: S.nen, tang: 3, kieu: "chu", san_pham: (S.y_tuong + "\n" + S.mo_ta_san_pham).slice(0, 1500), khach: (S.target || {}).khu_vuc || "", so_phuong_an: so, ho_so: hoSoHienTai(), cta: "" });
    if (j && j.ok && (j.phuong_an || []).length) {
      S.texts = j.phuong_an.slice(0, so).map(function (x) { return { tieu_de: x.tieu_de || "", noi_dung: x.noi_dung || "", cta: x.cta || "" }; });
      S.ly_do.push("Nội dung bài: AI đã viết " + S.texts.length + " phương án từ ý tưởng của anh, anh xem và sửa ở phần Bài quảng cáo.");
    } else {
      S.ly_do.push("AI chưa viết được nội dung (" + ((j && j.error) || "chưa nối được AI") + "). Cộng sự sẽ tự viết theo ý tưởng của anh khi dựng chiến dịch.");
    }
    S.da_ai = true; ve();
    if (S.giao_luon !== false) { say("Đang giao cho cộng sự dựng chiến dịch..."); await giaoViec(); say(""); }
    else say("Xong. Anh xem phương án bên phải rồi bấm Giao cho cộng sự làm luôn.");
    var nut2 = goc.querySelector("[data-ytuong-chay]"); if (nut2) nut2.disabled = false;
  }
  function tb(m) { var el = goc.querySelector("#tlTt"); if (el) el.textContent = m; else alert(m); }

  /* ---------- gửi và lưu ---------- */
  function phieu() {
    var g = ghep();
    return { id: S.id, nen: S.nen, ten: S.ten || autoTen(), che_do: S.che_do, kieu: S.kieu, muc_tieu: S.muc_tieu, cau_truc: S.cau_truc, ngan_sach_ngay: S.ngan_sach_ngay, tu_ngay: S.tu_ngay, den_ngay: S.den_ngay, tai_khoan: S.tai_khoan,
      mo_ta_san_pham: S.mo_ta_san_pham, dich_den: S.dich_den, nguon: S.nguon, ho_so: hoSoHienTai(), bai_dang: S.links.filter(function (x) { return x.ok; }),
      bai: g.map(function (b) { return { nhom: b.nhom, stt: b.stt, media_id: b.media_id, tieu_de: b.tieu_de, noi_dung: b.noi_dung, cta: b.cta, link: b.link, slides: (b.slides || []).map(function (x) { return { media_id: x.media_id, tieu_de: x.tieu_de, mo_ta: x.mo_ta }; }) }; }), nhom: S.nhom, tuy_chinh: S.tuy_chinh, tuong_tu: S.tuong_tu,
      loai_tru: S.loai_tru, ai: aiDay(), target: S.target, file_khach: S.file_khach, ghi_chu: S.ghi_chu, y_tuong: S.y_tuong, ui: { media: S.media, texts: S.texts, slotMedia: S.slotMedia, slotText: S.slotText, links: S.links, linksText: S.linksText, ho_so_id: S.ho_so_id, studio: S.studio, cau_chon: S.cau_chon, ai_tay: S.ai_tay } };
  }
  function hoSoHienTai() { var h = HO_SO.filter(function (x) { return x.id === S.ho_so_id; })[0]; return h ? { id: h.id, ten: h.ten, link: h.link, giong_van: h.giong_van } : {}; }
  function aiDay() { var o = {}; K().ai.forEach(function (a) { o[a.id] = S.ai[a.id] !== undefined ? S.ai[a.id] : a.mac_dinh; }); return o; }
  async function luu() {
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Nhập ngân sách mỗi ngày trước nhé."); return null; }
    var j = await api("/tisa-quang-cao/api/phieu", phieu());
    if (!j.ok) { tb(j.error || "Không lưu được."); return null; }
    S.id = j.phieu.id; if (!S.ten) S.ten = j.phieu.ten; tb("Đã lưu nháp."); await taiPhieu(); return j;
  }
  async function taiHoSo() { var j = await api("/tisa-quang-cao/api/ho-so"); HO_SO = j.ho_so || []; }
  async function taiPhieu() { var j = await api("/tisa-quang-cao/api/phieu"); PHIEU = j.phieu || []; }
  function mo(p) {
    S = moi(); S.id = p.id; S.nen = p.nen; S.che_do = p.che_do || "tu_chon"; S.kieu = p.kieu; S.muc_tieu = p.muc_tieu; S.cau_truc = p.cau_truc || S.cau_truc; S.ten = p.ten; S.ngan_sach_ngay = p.ngan_sach_ngay; S.tu_ngay = p.tu_ngay; S.den_ngay = p.den_ngay; S.tai_khoan = p.tai_khoan;
    S.mo_ta_san_pham = p.mo_ta_san_pham || ""; S.dich_den = p.dich_den || ""; S.nhom = p.nhom || []; S.tuy_chinh = p.tuy_chinh || []; S.tuong_tu = p.tuong_tu || S.tuong_tu; S.loai_tru = p.loai_tru || []; S.ai = p.ai || {};
    S.target = Object.assign(S.target, p.target || {}); S.file_khach = p.file_khach || []; S.ghi_chu = p.ghi_chu || ""; S.y_tuong = p.y_tuong || "";
    S.nguon = p.nguon || "moi"; var u = p.ui || {}; S.links = u.links || []; S.linksText = u.linksText || ""; S.ho_so_id = u.ho_so_id || (p.ho_so && p.ho_so.id) || ""; S.studio = u.studio || null; if (S.studio) { S.studio.dang = ""; S.studio.bangAnh = {}; S.studio.loi = ""; } S.cau_chon = u.cau_chon || (p.cau_truc && p.cau_truc.id) || "auto"; S.ai_tay = !!u.ai_tay; S.media = (u.media || []).filter(function (id) { return TEP[id]; }); S.texts = u.texts && u.texts.length ? u.texts : S.texts; S.slotMedia = u.slotMedia || {}; S.slotText = u.slotText || {};
    YT.text = S.y_tuong || ""; YT.kq = null; YT.msg = ""; DUONG_TAY = null; GV = null;
    ve(); window.scrollTo(0, 0);
  }

  /* ---------- sự kiện ---------- */
  function gan() {
    if (window.TisaStudio) TisaStudio.gan(goc, ctx);
    goc.addEventListener("click", async function (e) {
      var t = e.target, x;
      if ((x = t.closest("[data-noi]"))) { e.stopPropagation(); Q.chonNenKetNoi(x.dataset.noi); return; }
      if ((x = t.closest("[data-nen]"))) { chonNen(x.dataset.nen); ve(); return; }
      if ((x = t.closest("[data-che]"))) { S.che_do = x.dataset.che; if (S.nen && !S.kieu) { var k1 = K(); S.kieu = k1.kieu[0].id; if (!S.muc_tieu) S.muc_tieu = k1.muc_tieu[0].id; k1.ai.forEach(function (a) { if (S.ai[a.id] === undefined) S.ai[a.id] = a.mac_dinh; }); } ve(); return; }
      if ((x = t.closest("[data-mt]"))) { S.muc_tieu = x.dataset.mt; ve(); return; }
      if ((x = t.closest("[data-kieu]"))) { S.kieu = x.dataset.kieu; ve(); return; }
      if ((x = t.closest("[data-ct]"))) { e.preventDefault(); var m = MAU.filter(function (y) { return y.id === x.dataset.ct; })[0]; S.cau_truc = { id: m.id, nhom: m.nhom, bai: m.bai, chung: !!m.chung }; S.cau_chon = m.id; S.slotMedia = {}; S.slotText = {}; ve(); return; }
      if (t.closest("[data-ct-auto]")) { S.cau_chon = "auto"; ve(); return; }
      if ((x = t.closest("[data-nguon]"))) { S.nguon = x.dataset.nguon; ve(); return; }
      if (t.closest("[data-hs-them]")) { ThemHs = !ThemHs; ve(); return; }
      if (t.closest("[data-hs-luu]")) { var nm = (goc.querySelector("#hsTen").value || "").trim(), tt0 = goc.querySelector("#hsTt"); if (!nm) { if (tt0) tt0.textContent = "Nhập tên trước nhé."; return; }
        var jh = await api("/tisa-quang-cao/api/ho-so", { nen: S.nen, ten: nm, link: goc.querySelector("#hsLink").value, giong_van: goc.querySelector("#hsGiong").value });
        if (!jh.ok) { if (tt0) tt0.textContent = jh.error || "Không lưu được."; return; } HO_SO.unshift(jh.ho_so); S.ho_so_id = jh.ho_so.id; ThemHs = false; ve(); return; }
      if ((x = t.closest("[data-hs-xoa]"))) { if (!(await window.TISAHoi("Xoá khỏi danh sách đã lưu? (Không ảnh hưởng gì tới trang thật.)"))) return; await api("/tisa-quang-cao/api/ho-so/" + x.dataset.hsXoa + "/xoa", {}); HO_SO = HO_SO.filter(function (h) { return h.id !== x.dataset.hsXoa; }); S.ho_so_id = ""; ve(); return; }
      if ((x = t.closest("[data-ns]"))) { S.ngan_sach_ngay = x.dataset.ns; ve(); return; }
      if ((x = t.closest("[data-chon]"))) { goc.querySelector('[data-file="' + x.dataset.chon + '"]').click(); return; }
      if ((x = t.closest("[data-bo]"))) { var id = x.dataset.bo; S.media = S.media.filter(function (y) { return y !== id; }); S.file_khach = S.file_khach.filter(function (y) { return y !== id; }); S.slotMedia = {}; await api("/tisa-quang-cao/api/tep/" + id + "/xoa", {}); delete TEP[id]; DA_TAI = DA_TAI.filter(function (y) { return y.id !== id; }); ve(); return; }
      if ((x = t.closest("[data-dung]"))) { if (x.dataset.loai === "danh_sach") S.file_khach.push(x.dataset.dung); else S.media.push(x.dataset.dung); ve(); return; }
      if (t.closest("[data-them-t]")) { S.texts.push({ tieu_de: "", noi_dung: "", cta: "" }); ve(); return; }
      if ((x = t.closest("[data-xt]"))) { S.texts.splice(+x.dataset.xt, 1); S.slotText = {}; ve(); return; }
      if ((x = t.closest("[data-xc]"))) { var pr = x.dataset.xc.split("|"); (pr[0] === "loai_tru" ? S.loai_tru : S.target[pr[0]]).splice(+pr[1], 1); ve(); return; }
      if ((x = t.closest("[data-tc]"))) { var q = x.dataset.tc.split("|"), ds = q[0] === "loai_tru" ? S.loai_tru : S.target[q[0]]; if (ds.indexOf(q[1]) < 0) ds.push(q[1]); ve(); return; }
      if (t.closest("[data-goiy]")) { if (!S.mo_ta_san_pham.trim()) { tb("Anh viết mô tả sản phẩm ở phần Anh muốn quảng cáo gì trước để trang gợi ý cho đúng."); alert("Anh viết mô tả sản phẩm ở phần Anh muốn quảng cáo gì trước để trang gợi ý cho đúng."); return; }
        var g = await api("/tisa-quang-cao/api/goi-y-target?nen=" + S.nen + "&khu_vuc=" + encodeURIComponent(S.target.khu_vuc) + "&mo_ta=" + encodeURIComponent(S.mo_ta_san_pham)); if (g.ok) { GY = g; S.target.tuoi_tu = g.tuoi_tu; S.target.tuoi_den = g.tuoi_den; S.target.gioi_tinh = g.gioi_tinh; if (S.nen === "google") S.target.tu_khoa = g.tu_khoa.slice(0, 6); else { S.target.so_thich = g.so_thich.slice(0, 5); S.target.hanh_vi = g.hanh_vi.slice(0, 3); } S.loai_tru = g.loai_tru.slice(0, 4); ve(); } return; }
      if (t.closest("[data-nhom-goiy]")) { S.nhom = (GY.nhom || []).slice(0, S.cau_truc.nhom).map(function (y) { return { ten: y.ten, mo_ta: y.mo_ta }; }); ve(); return; }
      if ((x = t.closest("[data-ai]"))) { S.ai_tay = true; K().ai.forEach(function (a) { S.ai[a.id] = x.dataset.ai === "khuyen" ? !!a.khuyen : x.dataset.ai === "bat"; }); ve(); return; }
      if (t.closest("[data-ytuong-chay]")) { ytChay(); return; }
      if (t.closest("[data-yt-mic]")) { ytMic(); return; }
      if (t.closest("[data-yt-pt]")) { ytPhanTich(); return; }
      if (t.closest("[data-yt-dung]")) { ytDung(); return; }
      if (t.closest("[data-yt-hoi]")) { if (YT.kq) Q.hoi("Anh vừa nhờ AI lên kế hoạch quảng cáo. Em xem giúp anh kế hoạch này ổn chưa, chỗ nào nên sửa và vì sao. Chỉ góp ý bằng lời, chưa tạo hay bật gì trên tài khoản quảng cáo:\n\n" + ytVan(YT.kq)); return; }
      if (t.closest("[data-yt-chep]")) { if (YT.kq) { try { await navigator.clipboard.writeText(ytVan(YT.kq)); Q.toast("Đã chép kế hoạch."); } catch (er) { Q.toast("Trình duyệt chưa cho chép."); } } return; }
      if (t.closest("[data-tudong]")) { tuDong(); return; }
      if ((x = t.closest("[data-mo]"))) { mo(PHIEU[+x.dataset.mo]); return; }
      if ((x = t.closest("[data-xp]"))) { await api("/tisa-quang-cao/api/phieu/" + x.dataset.xp + "/xoa", {}); await taiPhieu(); ve(); return; }
      if (t.closest("[data-luu]")) { await luu(); return; }
      if (t.closest("[data-cach2]")) { cach2(); return; }
      if (t.closest("[data-giao-api]")) { giaoViec(); return; }
      if (t.closest("[data-giao-td]")) { cach2(); return; }
      if ((x = t.closest("[data-kn-lai]"))) { kiemLaiKn(x); return; }
      if (t.closest("[data-giao-ai]")) { if (duongGiao().duong === "api") giaoViec(); else cach2(); return; }
      if (t.closest("[data-doi-duong]")) { var dg0 = duongGiao(), moiD = dg0.duong === "api" ? "td" : "api"; DUONG_TAY = moiD === (dg0.san ? "api" : "td") ? null : moiD; vePhai(); return; }
      if (t.closest("[data-gui-chat]")) { if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Nhập ngân sách mỗi ngày trước nhé."); return; } var kq = await luu(); if (kq) Q.hoi(kq.loi_nhac); return; }
      if (t.closest("[data-gui]")) { giaoViec(); return; }
      if (t.closest("[data-gv-mo]")) { if (window.parent !== window) window.parent.postMessage({ tisa: "mo-doi-quan", trang: "tien-do" }, location.origin); return; }
      if (t.closest("[data-gv-moi]")) { clearInterval(henGv); GV = null; vePhai(); return; }
    });
    goc.addEventListener("change", function (e) {
      var t = e.target, x;
      if (t.matches("[data-file]")) { nhanFile(t.dataset.file, Array.prototype.slice.call(t.files)); t.value = ""; return; }
      if (t.matches("[data-tc2]")) { var id = t.dataset.tc2, i = S.tuy_chinh.indexOf(id); if (t.checked && i < 0) S.tuy_chinh.push(id); if (!t.checked && i >= 0) S.tuy_chinh.splice(i, 1); ve(); return; }
      if (t.matches("[data-tt-bat]")) { S.tuong_tu.bat = t.checked; ve(); return; }
      if (t.matches("[data-tt-nguon]")) { S.tuong_tu.nguon = t.value; vePhai(); return; }
      if (t.matches("[data-tt-pt]")) { S.tuong_tu.phan_tram = +t.value; vePhai(); return; }
      if (t.matches("[data-aid]")) { S.ai[t.dataset.aid] = t.checked; S.ai_tay = true; ve(); return; }
      if (t.matches("[data-cs]")) { csChon = t.value; vePhai(); return; }
      if (t.matches("[data-hs-chon]")) { S.ho_so_id = t.value; var hh = HO_SO.filter(function (h) { return h.id === t.value; })[0]; if (hh && hh.san_pham && !S.mo_ta_san_pham) S.mo_ta_san_pham = hh.san_pham; ve(); return; }
      if (t.matches("[data-sm]")) { S.slotMedia[+t.dataset.sm] = t.value; ve(); return; }
      if (t.matches("[data-st]")) { S.slotText[+t.dataset.st] = +t.value; ve(); return; }
      if (t.matches("[data-ctn]")) { S.cau_truc[t.dataset.ctn] = Math.max(1, Math.min(5, +t.value || 1)); S.cau_truc.id = "tuy-chinh"; S.cau_truc.chung = false; S.cau_chon = "tuy"; S.slotMedia = {}; S.slotText = {}; ve(); return; }
      if (t.matches('select[data-tx]')) { S.texts[+t.dataset.tx][t.dataset.k] = t.value; ve(); return; }
      if (t.matches("[data-yt-giao]")) { S.giao_luon = t.checked; return; }
      if (t.matches("[data-chay-o]")) { chonNen(t.value); ve(); return; }
      if (t.matches("[data-nguon-o]")) { S.nguon = t.value; ve(); return; }
      if (t.matches("[data-f]") && t.tagName === "SELECT") { S[t.dataset.f] = t.value; vePhai(); return; }
    });
    goc.addEventListener("input", function (e) {
      var yt = e.target.closest && e.target.closest("[data-yt2]"); if (yt) { YT.text = yt.value; S.y_tuong = yt.value; return; }
      var t = e.target;
      if (t.id === "tlLinkTxt") { docLinks(t.value); return; }
      if (t.matches("[data-f]") && t.tagName !== "SELECT") { S[t.dataset.f] = t.value; if (t.dataset.f === "ngan_sach_ngay") duKien(); vePhai(); return; }
      if (t.matches("[data-t]")) { var k = t.dataset.t; S.target[k] = (k === "tuoi_tu" || k === "tuoi_den") ? (+t.value || 18) : t.value; if (t.tagName !== "SELECT") vePhai(); return; }
      if (t.matches("input[data-tx],textarea[data-tx]")) { S.texts[+t.dataset.tx][t.dataset.k] = t.value; vePhai(); return; }
      if (t.matches("[data-nh]")) { var i = +t.dataset.nh; S.nhom[i] = S.nhom[i] || { ten: "", mo_ta: "" }; S.nhom[i][t.dataset.k] = t.value; vePhai(); }
    });
    goc.addEventListener("keydown", function (e) {
      var t = e.target;
      if (t.matches("[data-add]") && e.key === "Enter") { e.preventDefault(); var v = t.value.trim(); if (!v) return; var key = t.dataset.add, ds = key === "loai_tru" ? S.loai_tru : S.target[key]; if (ds.indexOf(v) < 0) ds.push(v); ve(); var n = goc.querySelector('[data-add="' + key + '"]'); if (n) n.focus(); return; }
      if (t.matches("[data-chon]") && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); t.click(); }
    });
    ["dragover", "drop"].forEach(function (ev) { goc.addEventListener(ev, function (e) { var z = e.target.closest("[data-chon]"); if (!z) return; e.preventDefault(); if (ev === "drop") nhanFile(z.dataset.chon, Array.prototype.slice.call(e.dataTransfer.files)); }); });
  }

  /* ---------- tự quét kết nối ---------- */
  /* Kết nối có chữ "chỉ đọc" trong tên thì coi là chỉ đọc dù máy lưu quyền đầy đủ (vd "Meta Ads (tự tạo app, chỉ đọc)") */
  function chuanKN(o) { Object.keys(o || {}).forEach(function (n) { ((o[n] || {}).mcp || []).forEach(function (x) { if (/chỉ đọc|chi doc|read.?only/i.test(x.ten || "")) x.chi_doc = true; }); }); return o; }
  var truoc = null;
  async function quet(yenLang) {
    var j = await api("/tisa-quang-cao/api/ket-noi"); if (!j.ok) return;
    var cu = KN; KN = chuanKN(j.ket_noi);
    if (truoc) Object.keys(KN).forEach(function (n) { if (KN[n].ok && !(truoc[n] && truoc[n].ok)) Q.toast("Vừa nối được " + KH[n].ten + ". Trang đã tự cập nhật."); });
    truoc = JSON.parse(JSON.stringify(KN));
    if (!yenLang && goc && goc.isConnected && JSON.stringify(cu) !== JSON.stringify(KN)) ve();
  }
  var hen = 0;
  function batQuet() { clearInterval(hen); hen = setInterval(function () { if (document.visibilityState === "visible" && Q.tabHienTai() === "tl") quet(); }, 15000); document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible" && Q.tabHienTai() === "tl") quet(); }); }

  /* vài kiểu nhỏ cho bố cục mới; trang chính không cần sửa CSS */
  function themKieu() {
    if (document.getElementById("tlKieuGon")) return;
    var st = document.createElement("style"); st.id = "tlKieuGon";
    st.textContent = ".tl-dau-cach{display:flex;justify-content:space-between;align-items:flex-start;gap:8px 16px;flex-wrap:wrap}" +
      ".tl-pl{position:relative}.tl-pl>summary{list-style:none;cursor:pointer;color:var(--fb);font-weight:700;font-size:13.5px;padding:6px 0;white-space:nowrap}.tl-pl>summary::-webkit-details-marker{display:none}" +
      ".tl-pl-ds{position:absolute;right:0;top:100%;z-index:30;width:min(420px,86vw);background:var(--the);border:1px solid var(--vien);border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.16);padding:4px 14px}" +
      ".tl-nhanh{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 12px;margin-top:4px}@media (max-width:820px){.tl-nhanh{grid-template-columns:1fr 1fr}}" +
      ".tl-xong{margin-left:8px;vertical-align:middle;font-size:11.5px;font-weight:700}" +
      ".tl-duong{display:block;font-size:13px;color:var(--mo);margin-top:8px;line-height:1.55}.tl-duong select{margin-left:4px;max-width:100%}" +
      ".tl-duong button{background:none;border:0;padding:0;color:var(--fb);font-weight:700;cursor:pointer;font-size:13px;min-height:0}" +
      ".tl-kn{border:1px solid var(--vien);border-radius:12px;padding:10px 12px;margin:12px 0 4px;background:var(--nen2,rgba(127,127,127,.05))}" +
      ".tl-kn-dau{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:4px;font-size:13.5px}" +
      ".tl-kn-lai{background:none;border:0;padding:4px 0;color:var(--fb);font-weight:700;cursor:pointer;font-size:12.5px;min-height:0;white-space:nowrap}" +
      ".tl-kn-dong{display:grid;grid-template-columns:84px 1fr;gap:8px;padding:6px 0;border-top:1px dashed var(--vien);font-size:13px;align-items:start}" +
      ".tl-kn-loai{font-weight:700;padding-top:2px}.tl-kn-gt small{display:block;color:var(--mo);font-size:12px;margin-top:2px;line-height:1.45}" +
      ".tl-kn-kl{font-size:12.5px;line-height:1.5;margin-top:6px;padding:7px 9px;border-radius:9px}.tl-kn-kl.ok{background:rgba(22,163,74,.1)}.tl-kn-kl.chua{background:rgba(234,122,11,.1)}" +
      ".tl-kn-kl .tl-noi{display:inline;cursor:pointer;color:var(--fb);font-weight:700;margin-left:2px}" +
      ".tl-len{display:flex;align-items:center;gap:10px;width:100%;text-align:left;margin-top:10px;padding:11px 14px;border-radius:12px;border:1.5px solid var(--vien);background:var(--the);color:inherit;cursor:pointer;font:inherit;min-height:56px}" +
      ".tl-len b{display:block;font-size:15px}.tl-len small{display:block;font-size:12.5px;color:var(--mo);margin-top:1px;line-height:1.4}.tl-len-ico{font-size:20px;line-height:1}" +
      ".tl-len:hover:not([disabled]){border-color:var(--fb)}" +
      ".tl-len.chinh{background:linear-gradient(90deg,#ff7a1a,#ff3d6e);border-color:transparent;color:#fff}.tl-len.chinh small{color:rgba(255,255,255,.9)}" +
      ".tl-len[disabled]{opacity:.55;cursor:not-allowed}";
    document.head.appendChild(st);
  }
  async function khoiTao(el) {
    goc = el; themKieu();
    var kh = await api("/tisa-quang-cao/api/khung"); if (!kh.ok) { el.innerHTML = '<div class="loi-hop">Không tải được bộ khung thiết lập.</div>'; return; }
    KH = kh.khung; MAU = kh.mau_cau_truc; NGANH = kh.nganh;
    var ds = await api("/tisa-quang-cao/api/tep"); (ds.tep || []).forEach(function (t) { TEP[t.id] = t; }); DA_TAI = ds.tep || [];
    await Promise.all([quet(true), taiPhieu(), taiHoSo()]);
    gan(); batQuet(); ve();
  }
  var ctx = { S: function () { return S; }, K: K, TEP: TEP, ve: function () { ve(); }, vePhai: function () { vePhai(); }, themTep: function (t) { TEP[t.id] = t; DA_TAI.push(t); }, hoSo: function () { return hoSoHienTai(); }, defCta: defCta, tb: tb };
  window.TisaThietLap = { khoiTao: khoiTao, quet: quet, ve: ve };
})();
