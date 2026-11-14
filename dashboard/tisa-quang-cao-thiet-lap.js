/* tisa-quang-cao-thiet-lap.js - tab "Thiết lập quảng cáo" của trang Quảng Cáo (V2.78).
   Đi từng bước cho người chưa rành quảng cáo; chọn nền tảng nào thì chữ, lựa chọn, lời nhắc đổi theo nền tảng đó
   (bộ khung nằm ở server: tisa_quang_cao_thiet_lap.py). Có chế độ Tự động: nhập vài thông tin, trợ lý lo phần còn lại.
   TRANG KHÔNG TỰ TẠO HAY BẬT QUẢNG CÁO: nút cuối chỉ gửi lời nhờ sang chat, luôn tạo ở trạng thái tạm dừng và chờ anh duyệt. */
(function () {
  "use strict";
  var Q = window.TisaQC;
  var esc = Q.esc, api = Q.api;
  var goc = null, KH = null, MAU = [], NGANH = [], KN = {}, TEP = {}, DA_TAI = [], PHIEU = [], HO_SO = [], ThemHs = false, CSDS = {}, CS_LOI = {}, GV = null, csChon = "", henGv = 0;
  var S = moi();

  function moi() {
    return { id: "", nen: "", che_do: "", kieu: "", muc_tieu: "", cau_truc: { id: "1-1-1", nhom: 1, bai: 1 }, ten: "", ngan_sach_ngay: "", tu_ngay: "", den_ngay: "", tai_khoan: "",
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
      if (!lk) w.push("Chưa có link bài đã đăng nào hợp lệ. Dán link bài ở bước Nguồn bài.");
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
    if (S.nen === "google" && S.kieu === "search" && !S.target.tu_khoa.length) w.push("Google Tìm kiếm cần từ khoá. Bấm Gợi ý hoặc tự nhập ở bước Đối tượng.");
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
      (cu.length ? '<div class="mo" style="margin-top:6px;font-size:13px">Đã tải trước đó: ' + cu.map(function (t) { return '<button type="button" class="chip nho" data-dung="' + t.id + '" data-loai="' + loai + '">+ ' + esc(t.ten.slice(0, 22)) + "</button>"; }).join(" ") + "</div>" : "") + "</div>";
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
    var tt = v.ok ? '<span class="nhan-tt ok">● Đã nối' + (v.mcp && v.mcp.some(function (x) { return x.ok; }) ? " (MCP)" : " (API)") + "</span>" : v.co ? '<span class="nhan-tt loi">⚠ Có kết nối, chưa chạy được</span>' : '<span class="nhan-tt dung">Chưa nối</span>';
    return tt;
  }
  function bo1() {
    var h = '<div class="the"><h2>1. Chọn nền tảng và cách làm</h2><p class="sub">Chọn nơi muốn chạy quảng cáo. Các bước bên dưới sẽ đổi theo nền tảng đó.</p><div class="luoi l3">';
    Object.keys(KH).forEach(function (n) {
      var on = S.nen === n;
      h += '<button type="button" class="tl-the' + (on ? " on" : "") + '" data-nen="' + n + '"><span class="cham nen-' + n + '"></span><b>' + esc(KH[n].ten) + "</b>" + badge(n) +
        '<span class="mo">' + esc(KH[n].cap.join(" › ")) + "</span>" + (!(KN[n] || {}).co ? '<span class="tl-noi" data-noi="' + n + '">Nối tài khoản</span>' : "") + "</button>";
    });
    h += '</div><div class="luoi l2" style="margin-top:12px">';
    [["tu_dong", "🤖 Tự động", "Anh chỉ cần nhập vài thông tin đơn giản. Trợ lý tự chọn cấu trúc, đối tượng, nội dung và thiết lập. Hợp người chưa rành quảng cáo."],
     ["tu_chon", "🛠 Tự chọn", "Anh đi từng bước và chọn mọi thứ: mẫu chiến dịch, hình, video, đối tượng, nút bấm, bật tắt AI."]].forEach(function (m) {
      h += '<button type="button" class="tl-the' + (S.che_do === m[0] ? " on" : "") + '" data-che="' + m[0] + '"><b>' + m[1] + '</b><span class="mo">' + m[2] + "</span></button>"; });
    h += "</div>";
    if (PHIEU.length) h += '<details style="margin-top:12px"><summary>Phiếu đã lưu (' + PHIEU.length + ')</summary>' + PHIEU.map(function (p, i) { return '<div class="tl-phieu"><div><b>' + esc(p.ten) + '</b><div class="mo" style="font-size:12.5px">' + esc((KH[p.nen] || {}).ten || p.nen) + " · " + so(p.ngan_sach_ngay) + "/ngày · " + esc(p.sua) + '</div></div><div class="hang"><button type="button" class="nut phu nho" data-mo="' + i + '">Mở</button><button type="button" class="nut phu nho" data-xp="' + p.id + '">Xoá</button></div></div>'; }).join("") + "</details>";
    return h + "</div>";
  }
  function boGoc() {
    var k = K(), dm = KH[S.nen];
    return '<div class="the"><h2>2. Anh muốn quảng cáo gì?</h2><p class="sub">Viết như đang kể với nhân viên. Càng rõ thì gợi ý đối tượng và nội dung càng đúng.</p>' + boHoSo() +
      '<label class="truong">Sản phẩm hoặc dịch vụ (kèm giá, điểm mạnh nếu có)<textarea data-f="mo_ta_san_pham" rows="3" placeholder="Ví dụ: Bán nhà phố 4 tầng, giá 5 tỷ, gần chợ, sổ hồng riêng">' + esc(S.mo_ta_san_pham) + "</textarea></label>" +
      '<div class="cot2"><label class="truong">Khu vực chạy quảng cáo<input type="text" data-t="khu_vuc" value="' + esc(S.target.khu_vuc) + '" placeholder="Quận hoặc tỉnh thành"></label>' +
      '<label class="truong">Khách liên hệ ở đâu? (link, Zalo, số điện thoại)<input type="text" data-f="dich_den" value="' + esc(S.dich_den) + '" placeholder="Ví dụ: Zalo 09xx xxx xxx"></label></div>' +
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
  function boCauTruc(auto, num) {
    var k = K(), h = '<div class="the"><h2>' + num + ". Mẫu chiến dịch: bao nhiêu " + esc(k.cap[1].split(" (")[0].toLowerCase()) + ", bao nhiêu bài?</h2><p class=\"sub\">1 " + esc(k.cap[0].toLowerCase()) + " chứa nhiều " + esc(k.cap[1].split(" (")[0].toLowerCase()) +
      ", mỗi nhóm chứa nhiều bài. Ký hiệu: CD là chiến dịch, N là một " + esc(k.cap[1].split(" (")[0].toLowerCase()) + ".</p><div class=\"luoi l4m\">";
    if (auto) h += '<button type="button" class="tl-the' + (S.cau_chon === "auto" ? " on" : "") + '" data-ct-auto><div class="tl-so"><span class="tl-cd">🤖</span></div><b>Để trợ lý chọn</b><span class="mo">Trợ lý chọn mẫu hợp ngân sách và số bài anh có.</span></button>';
    MAU.forEach(function (m) { h += '<button type="button" class="tl-the' + (S.cau_chon !== "auto" && S.cau_truc.id === m.id ? " on" : "") + '" data-ct="' + m.id + '"><div class="tl-so">' + sodo(m.nhom, m.bai, m.chung) + "</div><b>" + esc(m.ten) + '</b><span class="mo">' + esc(m.hop) + "</span></button>"; });
    h += "</div>";
    if (!auto) h += '<div class="hang" style="margin-top:10px"><label class="mo">Tự chọn: <input type="number" min="1" max="5" data-ctn="nhom" value="' + S.cau_truc.nhom + '" style="width:64px"> ' + esc(k.cap[1].split(" (")[0].toLowerCase()) + ', mỗi nhóm <input type="number" min="1" max="5" data-ctn="bai" value="' + S.cau_truc.bai + '" style="width:64px"> bài</label><span class="mo">Tổng ' + soBai() + " bài</span></div>";
    var m = S.media.length;
    if (!auto && S.nguon !== "bai_dang" && m > 1 && m !== soBai() && S.nen !== "google" && !S.cau_truc.chung) {
      h += '<div class="canh" style="margin-top:12px">Anh đã tải ' + m + " hình/video. " + (m === 3 ? 'Muốn mỗi cái là một bài thì chọn <a href="#" data-ct="1-3-3">3 nhóm, mỗi nhóm 1 bài</a> hoặc <a href="#" data-ct="1-1-3">1 nhóm 3 bài</a>.' : "Chọn số nhóm và bài sao cho tổng là " + m + " để dùng hết.") + "</div>";
    }
    return h + "</div>";
  }
  function boNguon(don) {
    var k = K(), nv = { facebook: "Fanpage", tiktok: "kênh TikTok", google: "kênh YouTube" }[S.nen];
    var cards = [["bai_dang", "🔗 Dùng bài đã đăng", "Chạy đúng một bài đã có trên " + nv + ". Chỉ cần dán link."], ["moi", "📎 Tải lên và tự viết", "Tải hình, video có sẵn và dán nội dung anh đã soạn."], ["ai", "✨ AI tạo giúp", "AI viết nội dung, tạo ảnh, dựng video theo tầng phễu anh chọn."]];
    var h = '<div class="luoi l3">' + cards.map(function (c) { return '<button type="button" class="tl-the nho' + (S.nguon === c[0] ? " on" : "") + '" data-nguon="' + c[0] + '"><b>' + c[1] + '</b><span class="mo">' + c[2] + "</span></button>"; }).join("") + "</div>";
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
    return '<div class="the tl-ytuong" style="border:1.5px solid var(--tim,#7c3aed)"><h2>💡 Ý tưởng anh muốn chạy</h2>' +
      '<p class="sub">Gõ như đang nhắn cho nhân viên: chạy cái gì, bán cho ai, ở đâu, khuyến mãi gì. Trợ lý tự viết nội dung, chọn đối tượng, cấu trúc rồi dựng cả chiến dịch. Chiến dịch luôn ở trạng thái <b>tạm dừng</b>, anh duyệt mới chạy.</p>' +
      '<textarea data-f="y_tuong" rows="6" aria-label="Ý tưởng quảng cáo" placeholder="Ví dụ: Chạy quảng cáo nhận tin nhắn cho căn nhà phố 4 tầng ở Gò Vấp giá 5 tỷ, nhắm người 28 đến 50 tuổi ở TP.HCM, nhấn mạnh sổ hồng riêng, gần chợ, khách nhắn Zalo để xem nhà cuối tuần.">' + esc(S.y_tuong) + "</textarea>" +
      '<label class="tl-ai" style="margin-top:8px"><input type="checkbox" data-yt-giao' + (S.giao_luon !== false ? " checked" : "") + '> Giao luôn cho cộng sự dựng chiến dịch trên nền tảng (tạm dừng)</label>' +
      '<button type="button" class="nut cam" data-ytuong-chay style="width:100%;padding:14px;margin-top:10px">✨ AI viết nội dung và setup toàn bộ</button>' +
      '<div id="ytTt" class="mo" style="margin-top:8px;font-size:13px">' + esc(S.yt_msg || "") + "</div></div>";
  }
  function boTuDong() {
    var h = boYTuong() + '<div class="the"><h2>3. Ngân sách</h2><label class="truong">Ngân sách mỗi ngày<input type="number" min="0" step="any" data-f="ngan_sach_ngay" value="' + esc(S.ngan_sach_ngay) + '" placeholder="300000"></label><div class="hang" style="margin-top:6px">' + [100000, 200000, 300000, 500000, 1000000].map(function (v) { return '<button type="button" class="chip" data-ns="' + v + '">' + so(v) + "</button>"; }).join("") + "</div></div>";
    h += boCauTruc(true, "4");
    h += '<div class="the"><h2>5. Bài quảng cáo (có thể bỏ qua)</h2><p class="sub">Có bài đã đăng hoặc hình, video sẵn thì dùng luôn. Chưa có thì để AI tạo, hoặc bỏ qua để trợ lý hỏi lại.</p>' + boNguon(true) + "</div>";
    h += boAi("6", true);
    h += '<div class="the"><button type="button" class="nut cam" data-tudong style="width:100%;padding:14px">🤖 Để trợ lý lên phương án cho tôi</button>' +
      (S.da_ai ? '<div class="ok-hop" style="margin-top:12px"><b>Trợ lý đã chọn giúp anh:</b><ul style="margin:6px 0 0;padding-left:20px">' + S.ly_do.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + '</ul><div class="hang" style="margin-top:10px"><button type="button" class="nut phu nho" data-che="tu_chon">Xem và chỉnh chi tiết</button></div></div>' : "") + "</div>";
    return h;
  }
  function boMucTieu() {
    var k = K();
    var h = '<div class="the"><h2>3. Dạng chiến dịch</h2><p class="sub">' + esc(k.ten) + ": chọn kiểu chạy.</p><div class=\"luoi l2\">" + k.kieu.map(function (x) { return '<button type="button" class="tl-the nho' + (S.kieu === x.id ? " on" : "") + '" data-kieu="' + x.id + '"><b>' + esc(x.ten) + '</b><span class="mo">' + esc(x.mo_ta) + "</span></button>"; }).join("") + "</div>";
    h += '<p class="mo" style="margin:10px 0 0;font-size:13px">Tên gọi trong ' + esc(k.ten) + " (khi anh mở trang quản lý của họ): " + esc(k.muc_tieu.filter(function (m) { return m.id === S.muc_tieu; }).map(function (m) { return m.goc; })[0] || "chọn mục tiêu ở bước 2") + ".</p></div>";
    return h + boCauTruc(false, "4");
  }
  function sodo(n, b, chung) { var s = '<span class="tl-cd">CD</span>'; for (var i = 0; i < n; i++) { s += '<span class="tl-nh">N</span>'; } return s + '<span class="mo">' + (chung ? "cùng 1 bài" : "×" + b + " bài") + "</span>"; }
  function boMedia(don) {
    var k = K(), h = "";
    if (S.nen === "google" && S.kieu === "search") h += '<div class="canh">Google Tìm kiếm là quảng cáo chữ: không cần hình hay video. Hình và video chỉ dùng cho Performance Max và Demand Gen.</div>';
    else if (S.nen === "tiktok") h += '<div class="mo" style="margin-bottom:8px">TikTok ưu tiên video dọc 9:16, 15 đến 60 giây. Có thể tải hình nếu chưa có video.</div>';
    h += '<div class="luoi l2">' + khuTai("video", "Tải video lên", "Kéo thả hoặc bấm chọn. Tải được nhiều video, mỗi video thường là một bài.", S.media.filter(function (id) { return (TEP[id] || {}).loai === "video"; })) +
      khuTai("anh", "Tải hình ảnh lên", "Kéo thả hoặc bấm chọn. Tải được nhiều hình.", S.media.filter(function (id) { return (TEP[id] || {}).loai === "anh"; })) + "</div>";
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
    var h = '<div class="the"><h2>5. Bài quảng cáo lấy từ đâu?</h2><p class="sub">' + esc(k.chi_tiet_bai) + "</p>" + boNguon(false) + "</div>";
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
    var h = '<div class="the"><h2>6. Đối tượng: quảng cáo cho ai?</h2><p class="sub">Bấm Gợi ý để trang đề xuất theo sản phẩm của anh. Anh chỉnh lại thoải mái.</p>' +
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
    var k = K(), h = '<div class="the"><h2>7. Quảng cáo tuỳ chỉnh: nhắm lại người đã quan tâm</h2><p class="sub">Người từng tương tác với anh thường mua dễ và rẻ hơn người lạ. Tick nhóm muốn chạy cho họ.</p>';
    k.tuy_chinh.forEach(function (x) { h += '<label class="tl-ck"><input type="checkbox" data-tc2="' + x.id + '"' + (S.tuy_chinh.indexOf(x.id) >= 0 ? " checked" : "") + '><span><b>' + esc(x.ten) + '</b> <span class="mo">' + esc(x.mo_ta) + "</span>" + (x.can ? '<br><span class="tl-can">Cần: ' + esc(x.can) + "</span>" : "") + "</span></label>"; });
    if (S.tuy_chinh.indexOf("danh_sach") >= 0) h += '<div style="margin:8px 0 0 28px">' + khuTai("danh_sach", "Tải file danh sách khách hàng", "CSV gồm số điện thoại hoặc email. Chỉ dùng cho tài khoản quảng cáo này.", S.file_khach) + "</div>";
    var tt = k.tuong_tu;
    h += '<div class="tl-tt-hop"><label class="tl-ck"><input type="checkbox" data-tt-bat' + (S.tuong_tu.bat ? " checked" : "") + '><span><b>' + esc(tt.ten) + '</b> <span class="mo">' + esc(tt.mo_ta) + "</span></span></label>";
    if (S.tuong_tu.bat) h += '<div class="hang" style="margin:6px 0 0 28px"><label class="mo">Lấy theo: <select data-tt-nguon><option value="">Khách tốt nhất</option>' + k.tuy_chinh.map(function (x) { return "<option value=\"" + x.id + '"' + (S.tuong_tu.nguon === x.id ? " selected" : "") + ">" + esc(x.ten) + "</option>"; }).join("") + '</select></label><label class="mo">Mức giống: <select data-tt-pt>' + tt.phan_tram.map(function (p) { return "<option" + (S.tuong_tu.phan_tram === p ? " selected" : "") + " value=\"" + p + "\">" + p + "%</option>"; }).join("") + "</select></label></div>";
    return h + "</div></div>";
  }
  function boAi(num, auto) {
    var k = K(), h = '<div class="the"><h2>' + (num || "8") + '. AI tự tối ưu: bật hay tắt?</h2><p class="sub">' + esc(k.ten) + " có nhiều chức năng AI tự điều chỉnh. Mặc định đang TẮT hết để anh kiểm soát. Muốn nền tảng tự tối ưu thì bật từng cái, hoặc bấm Bật theo khuyến nghị.</p>" +
      '<div class="hang" style="margin-bottom:8px"><button type="button" class="nut phu nho" data-ai="khuyen">Bật theo khuyến nghị</button><button type="button" class="nut phu nho" data-ai="tat">Tắt hết AI</button><button type="button" class="nut phu nho" data-ai="bat">Bật hết</button></div>';
    k.ai.forEach(function (a) { var on = S.ai[a.id] !== undefined ? S.ai[a.id] : a.mac_dinh; h += '<label class="tl-ai"><input type="checkbox" role="switch" data-aid="' + a.id + '"' + (on ? " checked" : "") + '><span class="tl-sw"></span><span><b>' + esc(a.ten) + '</b><br><span class="mo">' + (on ? "Đang bật: " + esc(a.bat) : "Đang tắt: " + esc(a.tat)) + "</span></span></label>"; });
    return h + "</div>";
  }
  function boNganSach() {
    var k = K();
    var h = '<div class="the"><h2>9. Ngân sách và lịch</h2><div class="cot2"><label class="truong">Ngân sách mỗi ngày<input type="number" min="0" step="any" data-f="ngan_sach_ngay" value="' + esc(S.ngan_sach_ngay) + '"></label>' +
      '<label class="truong">Tài khoản chạy<select data-f="tai_khoan"><option value="">Để trợ lý chọn</option>' + taiKhoanOpts() + "</select></label>" +
      '<label class="truong">Chạy từ ngày<input type="date" data-f="tu_ngay" value="' + esc(S.tu_ngay) + '"></label><label class="truong">Đến ngày (bỏ trống nếu chạy liên tục)<input type="date" data-f="den_ngay" value="' + esc(S.den_ngay) + '"></label></div>' +
      '<div class="hang" style="margin-top:8px">' + [100000, 200000, 300000, 500000, 1000000].map(function (v) { return '<button type="button" class="chip" data-ns="' + v + '">' + so(v) + "</button>"; }).join("") + '</div><div id="tlDuKien" class="mo" style="margin-top:10px"></div>';
    h += '<label class="truong" style="margin-top:12px">Tên chiến dịch<input type="text" data-f="ten" value="' + esc(S.ten) + '" placeholder="Tự đặt tên nếu để trống"></label><label class="truong">Ghi chú thêm cho trợ lý<textarea rows="2" data-f="ghi_chu">' + esc(S.ghi_chu) + "</textarea></label></div>";
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
  function tomTat() {
    var k = K(); if (!k) return '<div class="the"><h3>Tóm tắt</h3><p class="mo">Chọn nền tảng để bắt đầu.</p></div>';
    var g = ghep(), ct = S.cau_truc, mt = k.muc_tieu.filter(function (m) { return m.id === S.muc_tieu; })[0], ky = k.kieu.filter(function (m) { return m.id === S.kieu; })[0];
    var hs = HO_SO.filter(function (x) { return x.id === S.ho_so_id; })[0];
    var h = '<div class="the tl-tt-the"><h3>Tóm tắt phiếu</h3><div class="mo" style="font-size:13px">' + esc(k.ten) + " · " + (S.che_do === "tu_dong" ? "Tự động" : "Tự chọn") + (hs ? " · " + esc(hs.ten) : "") + "</div>";
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
    var ds = CSDS[S.nen], loi = CS_LOI[S.nen];
    h += '<div class="tl-giao"><div class="truong" style="margin:12px 0 4px">Giao cho cộng sự phụ trách</div>';
    if (ds === undefined || ds === null) h += '<div class="mo" style="font-size:13px">Đang xem ai phụ trách quảng cáo...</div>';
    else if (loi) h += '<div class="canh" style="font-size:13px">' + esc(loi) + "</div>";
    else if (!ds.length) h += '<div class="canh" style="font-size:13px">Chưa có cộng sự nào phụ trách quảng cáo. Vào Cài đặt đội thêm một người, hoặc bấm Dán vào chat bên dưới.</div>';
    else { var cur = ds.filter(function (x) { return x.id === csChon; })[0] || ds[0];
      h += '<select data-cs aria-label="Cộng sự phụ trách">' + ds.map(function (x) { return '<option value="' + esc(x.id) + '"' + (x.id === cur.id ? " selected" : "") + ">" + esc(x.ten) + (x.chuc_danh ? " · " + esc(x.chuc_danh) : "") + "</option>"; }).join("") + '</select><div class="mo" style="font-size:12.5px;margin-top:4px">Trang tự chọn người hợp nhất: ' + esc(cur.ly_do || "") + ". Anh đổi người được.</div>"; }
    h += '<div class="hang" style="margin-top:12px"><button type="button" class="nut phu" data-luu>Lưu nháp</button><button type="button" class="nut cam" data-gui' + (ds && ds.length ? "" : " disabled") + ">🚀 Giao cho cộng sự làm luôn</button>" + (loi || (ds && !ds.length) ? '<button type="button" class="nut phu" data-gui-chat>Dán vào chat</button>' : "") + '</div><div id="tlTt" class="mo" style="margin-top:8px;font-size:13px"></div>' +
      '<p class="mo" style="font-size:12.5px;margin:10px 0 0">Cộng sự chỉ chuẩn bị chiến dịch ở trạng thái tạm dừng. Anh nhắn đồng ý thì mới bật, không có gì tự chạy hay tự tiêu tiền.</p></div>';
    return h;
  }
  async function giaoViec() {
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Nhập ngân sách mỗi ngày trước nhé."); return; }
    var nut = goc.querySelector("[data-gui]"); if (nut) nut.disabled = true; tb("Đang giao việc...");
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
    if (S.nen && S.che_do) {
      cot += boGoc();
      if (S.che_do === "tu_dong") cot += boTuDong();
      else cot += boMucTieu() + boNoiDung() + boDoiTuong() + boTuyChinh() + boAi() + boNganSach();
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
    if (!(Number(S.ngan_sach_ngay) > 0)) { tb("Anh nhập ngân sách mỗi ngày trước nhé."); return; }
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
    if (!S.ai_tay) { S.ai = {}; k.ai.forEach(function (a) { S.ai[a.id] = a.mac_dinh; }); ly.push("AI tự tối ưu: đang TẮT hết (mặc định). Anh bật từng cái ở bước 6 nếu muốn."); }
    else ly.push("AI tự tối ưu: theo lựa chọn bật tắt của anh.");
    S.texts.forEach(function (t) { if (!t.cta) t.cta = ""; });
    if (S.nguon === "bai_dang") ly.push(S.links.some(function (x) { return x.ok; }) ? "Chạy đúng " + S.links.filter(function (x) { return x.ok; }).length + " bài đã đăng anh dán link." : "Anh chưa dán link bài nào hợp lệ.");
    else if (!S.media.length && !(S.nen === "google" && S.kieu === "search")) ly.push("Anh chưa có hình hoặc video: hãy chọn AI tạo giúp ở bước 5, hoặc để trợ lý hỏi lại trước khi tạo.");
    if (!S.ten) S.ten = autoTen();
    S.ly_do = ly; S.da_ai = true; ve();
    var p = goc.querySelector("[data-tudong]"); if (p) p.scrollIntoView({ block: "center", behavior: "smooth" });
  }
  async function ytChay() {
    var say = function (m) { S.yt_msg = m; var e = goc.querySelector("#ytTt"); if (e) e.textContent = m; };
    if ((S.y_tuong || "").trim().length < 12) { say("Anh gõ ý tưởng dài hơn một chút nhé: chạy cái gì, cho ai, ở đâu."); return; }
    if (!(Number(S.ngan_sach_ngay) > 0)) { say("Anh nhập ngân sách mỗi ngày ở bước 3 bên dưới trước nhé."); return; }
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
      S.ly_do.push("Nội dung bài: AI đã viết " + S.texts.length + " phương án từ ý tưởng của anh, anh xem và sửa ở bước 5.");
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
    ve(); window.scrollTo(0, 0);
  }

  /* ---------- sự kiện ---------- */
  function gan() {
    if (window.TisaStudio) TisaStudio.gan(goc, ctx);
    goc.addEventListener("click", async function (e) {
      var t = e.target, x;
      if ((x = t.closest("[data-noi]"))) { e.stopPropagation(); Q.chonNenKetNoi(x.dataset.noi); return; }
      if ((x = t.closest("[data-nen]"))) { if (S.nen !== x.dataset.nen) { var cu = S; S = moi(); S.id = ""; S.nen = x.dataset.nen; S.che_do = cu.che_do; S.mo_ta_san_pham = cu.mo_ta_san_pham; S.y_tuong = cu.y_tuong; S.giao_luon = cu.giao_luon; S.dich_den = cu.dich_den; S.ngan_sach_ngay = cu.ngan_sach_ngay; S.target.khu_vuc = cu.target.khu_vuc; S.media = cu.media; S.texts = cu.texts; S.file_khach = cu.file_khach; GY = null; S.cau_chon = cu.cau_chon; S.ai_tay = false; S.nguon = cu.nguon === "bai_dang" ? "moi" : cu.nguon; S.studio = cu.studio;
          var k0 = KH[S.nen]; S.muc_tieu = (k0.muc_tieu.filter(function (m) { return m.id === cu.muc_tieu; })[0] || k0.muc_tieu[0]).id; S.kieu = k0.kieu[0].id; k0.ai.forEach(function (a) { S.ai[a.id] = a.mac_dinh; }); } ve(); return; }
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
      if (t.closest("[data-goiy]")) { if (!S.mo_ta_san_pham.trim()) { tb("Anh viết mô tả sản phẩm ở bước 2 trước để trang gợi ý cho đúng."); alert("Anh viết mô tả sản phẩm ở bước 2 trước để trang gợi ý cho đúng."); return; }
        var g = await api("/tisa-quang-cao/api/goi-y-target?nen=" + S.nen + "&khu_vuc=" + encodeURIComponent(S.target.khu_vuc) + "&mo_ta=" + encodeURIComponent(S.mo_ta_san_pham)); if (g.ok) { GY = g; S.target.tuoi_tu = g.tuoi_tu; S.target.tuoi_den = g.tuoi_den; S.target.gioi_tinh = g.gioi_tinh; if (S.nen === "google") S.target.tu_khoa = g.tu_khoa.slice(0, 6); else { S.target.so_thich = g.so_thich.slice(0, 5); S.target.hanh_vi = g.hanh_vi.slice(0, 3); } S.loai_tru = g.loai_tru.slice(0, 4); ve(); } return; }
      if (t.closest("[data-nhom-goiy]")) { S.nhom = (GY.nhom || []).slice(0, S.cau_truc.nhom).map(function (y) { return { ten: y.ten, mo_ta: y.mo_ta }; }); ve(); return; }
      if ((x = t.closest("[data-ai]"))) { S.ai_tay = true; K().ai.forEach(function (a) { S.ai[a.id] = x.dataset.ai === "khuyen" ? !!a.khuyen : x.dataset.ai === "bat"; }); ve(); return; }
      if (t.closest("[data-ytuong-chay]")) { ytChay(); return; }
      if (t.closest("[data-tudong]")) { tuDong(); return; }
      if ((x = t.closest("[data-mo]"))) { mo(PHIEU[+x.dataset.mo]); return; }
      if ((x = t.closest("[data-xp]"))) { await api("/tisa-quang-cao/api/phieu/" + x.dataset.xp + "/xoa", {}); await taiPhieu(); ve(); return; }
      if (t.closest("[data-luu]")) { await luu(); return; }
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
      if (t.matches("[data-f]") && t.tagName === "SELECT") { S[t.dataset.f] = t.value; vePhai(); return; }
    });
    goc.addEventListener("input", function (e) {
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
  var truoc = null;
  async function quet(yenLang) {
    var j = await api("/tisa-quang-cao/api/ket-noi"); if (!j.ok) return;
    var cu = KN; KN = j.ket_noi;
    if (truoc) Object.keys(KN).forEach(function (n) { if (KN[n].ok && !(truoc[n] && truoc[n].ok)) Q.toast("Vừa nối được " + KH[n].ten + ". Trang đã tự cập nhật."); });
    truoc = JSON.parse(JSON.stringify(KN));
    if (!yenLang && goc && goc.isConnected && JSON.stringify(cu) !== JSON.stringify(KN)) ve();
  }
  var hen = 0;
  function batQuet() { clearInterval(hen); hen = setInterval(function () { if (document.visibilityState === "visible" && Q.tabHienTai() === "tl") quet(); }, 15000); document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible" && Q.tabHienTai() === "tl") quet(); }); }

  async function khoiTao(el) {
    goc = el;
    var kh = await api("/tisa-quang-cao/api/khung"); if (!kh.ok) { el.innerHTML = '<div class="loi-hop">Không tải được bộ khung thiết lập.</div>'; return; }
    KH = kh.khung; MAU = kh.mau_cau_truc; NGANH = kh.nganh;
    var ds = await api("/tisa-quang-cao/api/tep"); (ds.tep || []).forEach(function (t) { TEP[t.id] = t; }); DA_TAI = ds.tep || [];
    await Promise.all([quet(true), taiPhieu(), taiHoSo()]);
    gan(); batQuet(); ve();
  }
  var ctx = { S: function () { return S; }, K: K, TEP: TEP, ve: function () { ve(); }, vePhai: function () { vePhai(); }, themTep: function (t) { TEP[t.id] = t; DA_TAI.push(t); }, hoSo: function () { return hoSoHienTai(); }, defCta: defCta, tb: tb };
  window.TisaThietLap = { khoiTao: khoiTao, quet: quet, ve: ve };
})();
