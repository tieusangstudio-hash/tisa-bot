/* tisa-quang-cao-studio.js - "Tạo bài quảng cáo bằng AI" ngay trong tab Thiết lập quảng cáo (V2.78).
   Chọn tầng phễu (5 tầng), loại quảng cáo (chữ, ảnh 1 tấm, nhiều tấm, video), nhập thông tin sản phẩm; AI viết nội dung theo công thức
   đúng tầng, tạo ảnh, dựng video từ ảnh cảnh. Mọi thứ sửa được ngay tại đây: viết lại theo yêu cầu, tạo lại ảnh, sửa ảnh, đổi chữ.
   "Dùng bài này" đưa nội dung và hình vào chiến dịch, không phải sao chép sang nơi khác. Chỉ SOẠN, không đăng, không bật quảng cáo. */
(function () {
  "use strict";
  var Q = window.TisaQC, esc = Q.esc, api = Q.api;
  var C = null, goc = null, DATA = null, TT = { chu: true, anh: false, video: false }, DOI = null, DANG_THEO = {};

  function S() { return C.S(); }
  function ST() {
    var s = S();
    if (!s.studio) {
      var t = (DATA && DATA.tang.filter(function (x) { return x.muc_tieu_qc.indexOf(s.muc_tieu) >= 0; })[0]) || { id: 3 };
      s.studio = { tang: t.id, kieu: "anh_1", so_tam: 3, do_dai: 30, do_dai_tuy: false, refs: { nhan_vat: [], logo: [], san_pham: [] }, gia: "", khac_biet: "", khach: "", giong: "", phong_cach: "", so_pa: 2, chen_chu: false, pa: [], dang: "", loi: "" };
    }
    return s.studio;
  }
  function refs() { var st = ST(), r = st.refs || (st.refs = { nhan_vat: [], logo: [], san_pham: [] }); ["nhan_vat", "logo", "san_pham"].forEach(function (k) { r[k] = (r[k] || []).filter(function (id) { return C.TEP[id]; }); }); return r; }
  function nCs(vai) { var c = DOI && (vai === "video" ? DOI.video : DOI.thiet_ke); return c ? c.ten : "cộng sự"; }
  function cho(ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); }
  function nenTiktok() { return S().nen === "tiktok"; }
  function tyLe(pa) { return pa.kieu === "video" || nenTiktok() ? "portrait" : "square"; }
  function ds(pa) { return pa.kieu === "video" ? pa.canh : pa.kieu === "anh_nhieu" ? pa.slides : [pa]; }

  /* ---------- vẽ ---------- */
  function html() {
    if (!DATA) return '<div class="mo">Đang tải bộ tạo bài AI...</div>';
    var st = ST(), s = S(), k = C.K(), search = s.nen === "google" && s.kieu === "search";
    if (search && st.kieu !== "chu") st.kieu = "chu";
    var h = '<div class="stu"><div class="hang" style="justify-content:space-between"><h3 style="margin:0">✨ Tạo bài quảng cáo bằng AI</h3><span class="stu-tt">' +
      '<span class="nhan-tt ' + (TT.chu ? "ok" : "loi") + '">' + (TT.chu ? "● Viết chữ" : "⚠ Chưa có AI viết chữ") + "</span> " +
      '<span class="nhan-tt ' + (TT.anh ? "ok" : "dung") + '">' + (TT.anh ? "● Tạo ảnh" : "○ Chưa đăng nhập ChatGPT") + "</span> " +
      '<span class="nhan-tt ' + (TT.video ? "ok" : "dung") + '">' + (TT.video ? "● Dựng video" : "○ Thiếu ffmpeg") + "</span></span></div>";
    var bn = TT.bo_nao || {};
    h += bn.co ? '<div class="mo" style="font-size:13px;margin-top:6px">✓ Trước khi viết, vẽ, dựng, AI và cộng sự đọc <b>bộ não</b> của anh để hiểu đúng sản phẩm, khách hàng, giọng thương hiệu và quy tắc.</div>' :
      '<div class="canh" style="font-size:13px;margin-top:6px">⚠ Bộ não của anh chưa có thông tin sản phẩm' + ((bn.thieu || []).length ? " (còn trống: " + esc(bn.thieu.slice(0, 3).join(", ")) + ")" : "") + '. AI chỉ dựa vào phần anh nhập bên dưới. Nhờ <b>Hà Hồ Sơ</b> điền bộ não trước thì bài, ảnh, video sẽ đúng sản phẩm hơn nhiều.</div>';
    if (!TT.anh) h += '<div class="mo" style="font-size:13px;margin-top:6px">Tạo ảnh trực tiếp dùng gói ChatGPT của anh. Chưa đăng nhập thì vào Cài đặt, Mô hình để đăng nhập ChatGPT. Hoặc bấm <b>Giao ' + esc(nCs("thiet-ke")) + ' làm ảnh</b>, hoặc tải ảnh có sẵn lên.</div>';
    h += '<div class="truong" style="margin-top:12px">A. Chọn tầng phễu: khách của anh đang ở đâu?</div><div class="stu-tang">' + DATA.tang.map(function (t) {
      return '<button type="button" class="tl-the nho' + (st.tang === t.id ? " on" : "") + '" data-sd-tang="' + t.id + '"><b>' + t.id + ". " + esc(t.ten) + '</b><span class="mo">' + esc(t.khach) + "</span></button>"; }).join("") + "</div>";
    var tg = DATA.tang.filter(function (t) { return t.id === st.tang; })[0];
    h += '<div class="ok-hop" style="margin-top:8px;font-size:13px"><b>Tầng ' + tg.id + ", " + esc(tg.ngan) + ".</b> " + esc(tg.muc_tieu) + '<br><span class="mo">Công thức AI dùng: ' + esc(tg.cong_thuc) + ". Gợi ý loại bài: " + esc({ video: "video ngắn", anh_nhieu: "ảnh nhiều tấm", anh_1: "ảnh 1 tấm", chu: "chữ" }[tg.loai_goi_y]) + ".</span></div>";
    var kinds = [["chu", "Chỉ chữ", "Nội dung bài viết, tiêu đề, nút"], ["anh_1", "Ảnh 1 tấm", "1 ảnh quảng cáo kèm chữ"], ["anh_nhieu", "Ảnh nhiều tấm", "Carousel, mỗi tấm một ý"], ["video", "Video", "Kịch bản từng cảnh, ảnh cảnh, dựng video"]];
    h += '<div class="truong" style="margin-top:12px">B. Loại quảng cáo</div><div class="stu-tang">' + kinds.map(function (x) {
      var off = search && x[0] !== "chu";
      return '<button type="button" class="tl-the nho' + (st.kieu === x[0] ? " on" : "") + '" data-sd-kieu="' + x[0] + '"' + (off ? " disabled" : "") + "><b>" + x[1] + '</b><span class="mo">' + x[2] + "</span></button>"; }).join("") + "</div>";
    if (st.kieu === "anh_nhieu") h += '<label class="mo" style="display:block;margin-top:8px">Số tấm ảnh: <input type="number" min="2" max="10" data-sd="so_tam" value="' + st.so_tam + '" style="width:70px"> (2 đến 10)</label>';
    if (st.kieu === "video") {
      var pre = [10, 15, 20, 30, 45, 60, 90, 120], tuy = st.do_dai_tuy || pre.indexOf(st.do_dai) < 0;
      h += '<div class="mo" style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px">Độ dài video: <select data-sd="do_dai">' + pre.map(function (v) { return "<option" + (!tuy && st.do_dai === v ? " selected" : "") + ' value="' + v + '">' + v + " giây</option>"; }).join("") + "<option" + (tuy ? " selected" : "") + ' value="khac">Số khác, tự nhập...</option></select>' +
        (tuy ? '<input type="number" min="5" max="180" data-sd="do_dai_so" value="' + st.do_dai + '" style="width:80px"> giây <span class="mo" style="font-size:12.5px">(5 đến 180)</span>' : "") + "</div>";
    }
    if (search) h += '<div class="mo" style="font-size:13px;margin-top:6px">Google Tìm kiếm là quảng cáo chữ nên chỉ viết chữ. Muốn ảnh, video thì đổi dạng chiến dịch sang Performance Max hoặc Demand Gen ở bước 3.</div>';
    h += '<div class="truong" style="margin-top:12px">C. Thông tin sản phẩm, dịch vụ</div><textarea rows="3" data-f="mo_ta_san_pham" style="width:100%" placeholder="Anh bán gì, cho ai, điểm mạnh. Ví dụ: Khoá học quay video bằng điện thoại cho chủ shop, học 2 ngày, có thực hành">' + esc(s.mo_ta_san_pham) + "</textarea>" +
      '<div class="cot2"><label class="truong">Giá, ưu đãi (chỉ ghi nếu muốn quảng cáo nêu)<input type="text" data-sd="gia" value="' + esc(st.gia) + '"></label><label class="truong">Điểm khác biệt<input type="text" data-sd="khac_biet" value="' + esc(st.khac_biet) + '"></label>' +
      '<label class="truong">Khách hàng mục tiêu<input type="text" data-sd="khach" value="' + esc(st.khach) + '" placeholder="Ví dụ: chủ shop online 25 đến 45 tuổi"></label>' +
      '<label class="truong">Giọng văn<select data-sd="giong"><option value="">Để AI chọn</option>' + DATA.giong.map(function (g) { return "<option" + (st.giong === g ? " selected" : "") + ">" + esc(g) + "</option>"; }).join("") + "</select></label>" +
      (st.kieu !== "chu" ? '<label class="truong">Phong cách hình<select data-sd="phong_cach"><option value="">Để AI chọn</option>' + DATA.phong_cach_anh.map(function (g) { return "<option" + (st.phong_cach === g ? " selected" : "") + ">" + esc(g) + "</option>"; }).join("") + "</select></label>" : "") +
      '<label class="truong">Số phương án<select data-sd="so_pa">' + [1, 2, 3].map(function (v) { return "<option" + (st.so_pa === v ? " selected" : "") + ' value="' + v + '">' + v + " phương án</option>"; }).join("") + "</select></label></div>" +
      (st.kieu !== "chu" ? '<label class="tl-ck" style="margin-top:6px"><input type="checkbox" data-sd="chen_chu"' + (st.chen_chu ? " checked" : "") + '><span><b>Chèn chữ lên ảnh</b> <span class="mo">AI in câu ngắn lên ảnh. Chữ tiếng Việt trên ảnh đôi khi sai dấu, nhớ kiểm tra. Để trống thì ảnh sạch, chữ nằm ở nội dung bài.</span></span></label>' : "");
    if (st.kieu !== "chu") h += refHtml();
    h += '<div class="hang" style="margin-top:12px"><button type="button" class="nut cam" data-sd-viet' + (st.dang ? " disabled" : "") + ">✨ AI viết và tạo bài quảng cáo</button>" + (st.dang ? '<span class="mo">' + esc(st.dang) + "</span>" : "") + "</div>";
    if (st.loi) h += '<div class="loi-hop" style="margin-top:10px">' + esc(st.loi) + (st.loiGiao != null && st.pa[st.loiGiao] ? '<div class="hang" style="margin-top:8px"><button type="button" class="nut cam nho" data-sd-giao="' + st.loiGiao + '|thiet-ke">🎨 Giao ' + esc(nCs("thiet-ke")) + " làm ảnh này</button></div>" : "") + "</div>";
    if (st.bo_nao_ghi) h += '<div class="mo" style="font-size:12.5px;margin-top:8px">' + esc(st.bo_nao_ghi) + "</div>";
    h += '<div id="sdKq">' + st.pa.map(function (pa, i) { return the(pa, i); }).join("") + "</div></div>";
    return h;
  }
  function refHtml() {
    var r = refs(), def = [["nhan_vat", "Nhân vật xuất hiện", "Ảnh người sẽ có mặt trong quảng cáo. AI giữ đúng khuôn mặt, kiểu tóc.", 2], ["logo", "Logo", "Logo thương hiệu, AI đặt nguyên vẹn vào một góc ảnh.", 1], ["san_pham", "Hình sản phẩm", "Ảnh sản phẩm thật, AI vẽ đúng hình dáng và màu sắc.", 2]];
    var tong = r.nhan_vat.length + r.logo.length + r.san_pham.length;
    var h = '<div class="truong" style="margin-top:12px">Ảnh tham chiếu <span class="mo">(không bắt buộc, nên có để ảnh ra đúng người, đúng logo, đúng sản phẩm)</span></div><div class="stu-ref">';
    def.forEach(function (d) {
      var ds0 = r[d[0]];
      h += '<div class="stu-ref-o"><b>' + d[1] + '</b><div class="mo" style="font-size:12.5px">' + d[2] + '</div><div class="stu-ref-ds">' + ds0.map(function (id) { return '<span class="stu-ref-t"><img src="/tisa-quang-cao/api/tep/' + id + '" alt="' + d[1] + '"><button type="button" data-sd-ref-bo="' + d[0] + '|' + id + '" aria-label="Bỏ ảnh">✕</button></span>'; }).join("") + "</div>" +
        (ds0.length < d[3] && tong < 4 ? '<label class="nut phu nho" style="cursor:pointer;margin:0;display:inline-block">+ Tải ảnh lên<input type="file" accept="image/png,image/jpeg,image/webp" class="an" data-sd-ref="' + d[0] + '"></label>' : "") + "</div>";
    });
    return h + '</div><div class="mo" style="font-size:12.5px;margin-top:4px">Tối đa 4 ảnh tham chiếu mỗi lần tạo ảnh. Đang dùng ' + tong + "/4.</div>";
  }
  function anh(pa, j, nhan, mo_ta, chu) {
    var st = ST(), id = pa.imgs[j], k = "ai|" + (st.pa.indexOf(pa)) + "|" + j, dang = st.bangAnh && st.bangAnh[k];
    var h = '<div class="stu-anh"><div class="stu-khung">' + (id ? thumbLon(id) : '<div class="stu-trong mo">' + (dang ? "Đang tạo ảnh..." : "Chưa có ảnh") + "</div>") + "</div><div class='stu-anh-bt'>" +
      '<button type="button" class="nut phu nho" data-sd-anh="' + k + '"' + (!TT.anh || dang ? " disabled" : "") + ">" + (id ? "Tạo lại" : "Tạo ảnh") + "</button>" +
      '<label class="nut phu nho" style="cursor:pointer;margin:0">Tải ảnh khác<input type="file" accept="image/*" class="an" data-sd-up="' + k + '"></label></div>';
    if (id) h += '<div class="hang" style="margin-top:6px"><input type="text" data-sd-sua-anh-in="' + k + '" placeholder="Sửa ảnh: ví dụ nền sáng hơn, thêm cây xanh" style="flex:1;min-width:140px"><button type="button" class="nut nho" data-sd-sua-anh="' + k + '"' + (!TT.anh || dang ? " disabled" : "") + ">Sửa</button></div>";
    return h + "</div>";
  }
  function thumbLon(id) {
    var t = C.TEP[id], u = "/tisa-quang-cao/api/tep/" + id;
    return t && t.loai === "video" ? '<video src="' + u + '" controls playsinline preload="metadata" style="width:100%;max-height:420px;border-radius:12px;background:#000"></video>' : '<img src="' + u + '" alt="Ảnh quảng cáo" style="width:100%;border-radius:12px;display:block">';
  }
  function the(pa, i) {
    var k = C.K(), st = ST(), kn = { chu: "Chỉ chữ", anh_1: "Ảnh 1 tấm", anh_nhieu: "Ảnh nhiều tấm", video: "Video" }[pa.kieu];
    var h = '<div class="stu-pa"><div class="hang" style="justify-content:space-between"><div><b>Phương án ' + (i + 1) + (pa.ten ? ": " + esc(pa.ten) : "") + '</b> <span class="mo">' + kn + (pa.cong_thuc ? " · công thức " + esc(pa.cong_thuc) : "") + '</span></div><button type="button" class="nut phu nho" data-sd-xoa="' + i + '">Bỏ</button></div>';
    h += '<label class="truong">Tiêu đề<input type="text" data-sp="' + i + '|tieu_de" value="' + esc(pa.tieu_de) + '"></label><label class="truong">Nội dung chính<textarea rows="7" data-sp="' + i + '|noi_dung">' + esc(pa.noi_dung) + "</textarea></label>" +
      '<div class="cot2"><label class="truong">Nút kêu gọi<select data-sp="' + i + '|cta">' + k.cta.map(function (c) { return "<option" + (pa.cta === c ? " selected" : "") + ">" + esc(c) + "</option>"; }).join("") + '</select></label><label class="truong">Hashtag<input type="text" data-sp="' + i + '|hashtag" value="' + esc((pa.hashtag || []).join(" ")) + '"></label></div>';
    if (S().nen === "google" && (pa.tieu_de_phu.length || pa.mo_ta_ngan.length)) h += '<label class="truong">Tiêu đề phụ cho Google (mỗi dòng một tiêu đề, tối đa 30 ký tự)<textarea rows="5" data-sp="' + i + '|tieu_de_phu">' + esc(pa.tieu_de_phu.join("\n")) + '</textarea></label><label class="truong">Mô tả ngắn (mỗi dòng một mô tả, tối đa 90 ký tự)<textarea rows="3" data-sp="' + i + '|mo_ta_ngan">' + esc(pa.mo_ta_ngan.join("\n")) + "</textarea></label>";
    h += '<div class="hang" style="margin-top:6px"><input type="text" data-sd-sua-in="' + i + '" placeholder="Muốn sửa gì? Ví dụ: ngắn hơn, thêm ưu đãi giảm 10%, giọng trẻ trung hơn" style="flex:1;min-width:180px"><button type="button" class="nut nho" data-sd-sua="' + i + '"' + (st.dang ? " disabled" : "") + ">Viết lại theo yêu cầu</button></div>";
    if (pa.kieu === "anh_1") h += '<h4 class="stu-h">Ảnh quảng cáo</h4>' + anh(pa, 0) + '<div class="hang" style="margin-top:6px"><button type="button" class="nut phu nho" data-sd-giao="' + i + '|thiet-ke"' + (st.dang ? " disabled" : "") + '>🎨 Giao ' + esc(nCs("thiet-ke")) + ' làm ảnh</button><span class="mo" style="font-size:12.5px">' + (pa.chi_dao ? "Đã có chỉ đạo hình từ " + esc(pa.chi_dao_tu || "cộng sự thiết kế") + ". " : "") + 'Cộng sự đọc bộ não, làm ảnh đúng sản phẩm.</span></div>' + '<label class="truong">Mô tả ảnh (AI dùng để vẽ, anh sửa được)<textarea rows="3" data-sp="' + i + '|mo_ta_anh">' + esc(pa.mo_ta_anh) + '</textarea></label><label class="truong">Chữ in trên ảnh (nếu bật Chèn chữ)<input type="text" data-sp="' + i + '|chu_tren_anh" value="' + esc(pa.chu_tren_anh) + '"></label>';
    if (pa.kieu === "anh_nhieu") {
      h += '<h4 class="stu-h">' + pa.slides.length + ' tấm ảnh</h4><div class="hang" style="margin-bottom:6px"><button type="button" class="nut phu nho" data-sd-tat="' + i + '"' + (!TT.anh || st.dang ? " disabled" : "") + ">Tạo ảnh cho tất cả tấm</button>" + '<button type="button" class="nut phu nho" data-sd-giao="' + i + '|thiet-ke"' + (st.dang ? " disabled" : "") + '>🎨 Giao ' + esc(nCs("thiet-ke")) + ' làm ảnh</button></div><div class="stu-luoi">';
      pa.slides.forEach(function (sl, j) { h += '<div class="stu-tam"><b>Tấm ' + (j + 1) + "</b>" + anh(pa, j) + '<input type="text" data-sp="' + i + "|slides|" + j + '|tieu_de" value="' + esc(sl.tieu_de) + '" placeholder="Tiêu đề tấm"><input type="text" data-sp="' + i + "|slides|" + j + '|mo_ta" value="' + esc(sl.mo_ta) + '" placeholder="Mô tả tấm"><details><summary>Mô tả ảnh</summary><textarea rows="3" data-sp="' + i + "|slides|" + j + '|mo_ta_anh">' + esc(sl.mo_ta_anh) + '</textarea><input type="text" data-sp="' + i + "|slides|" + j + '|chu_tren_anh" value="' + esc(sl.chu_tren_anh) + '" placeholder="Chữ in trên ảnh"></details></div>'; });
      h += "</div>";
    }
    if (pa.kieu === "video") {
      h += '<h4 class="stu-h">Kịch bản ' + pa.canh.length + ' cảnh</h4><div class="hang" style="margin-bottom:6px"><button type="button" class="nut phu nho" data-sd-tat="' + i + '"' + (!TT.anh || st.dang ? " disabled" : "") + ">Tạo ảnh cho tất cả cảnh</button><button type=\"button\" class=\"nut nho\" data-sd-video=\"" + i + '"' + (!TT.video || st.dang ? " disabled" : "") + ">Dựng nhanh từ ảnh cảnh (bản nháp)</button><button type=\"button\" class=\"nut phu nho\" data-sd-chep=\"" + i + '">Chép kịch bản</button><button type="button" class="nut cam nho" data-sd-giao="' + i + '|video"' + (st.dang ? " disabled" : "") + '>🎬 Giao ' + esc(nCs("video")) + ' làm video</button></div>';
      if (pa.video_id) h += '<div class="stu-vd"><b>Video đã dựng</b>' + thumbLon(pa.video_id) + '<div class="mo" style="font-size:12.5px">Video từ ảnh cảnh, chuyển động nhẹ, có phụ đề. Đây là bản nháp ghép từ ảnh. Muốn video đúng sản phẩm, chuyển động và giọng đọc đẹp hơn thì bấm Giao cộng sự làm video, hoặc tải video riêng ở bước Tải lên.</div></div>';
      h += '<div class="stu-luoi">';
      pa.canh.forEach(function (c, j) { h += '<div class="stu-tam"><b>Cảnh ' + (j + 1) + " · " + esc(c.giay || "") + "s</b>" + anh(pa, j) + '<label class="mo" style="font-size:12.5px">Thời lượng (giây) <input type="number" min="2" max="20" data-sp="' + i + "|canh|" + j + '|giay" value="' + esc(String(c.giay || 3).replace(/[^0-9.]/g, "").split(".")[0] || 3) + '" style="width:60px"></label>' +
        '<input type="text" data-sp="' + i + "|canh|" + j + '|loi" value="' + esc(c.loi) + '" placeholder="Lời thoại"><input type="text" data-sp="' + i + "|canh|" + j + '|chu" value="' + esc(c.chu) + '" placeholder="Chữ hiện trên màn hình (phụ đề)"><details><summary>Hình và mô tả ảnh</summary><textarea rows="2" data-sp="' + i + "|canh|" + j + '|hinh">' + esc(c.hinh) + '</textarea><textarea rows="3" data-sp="' + i + "|canh|" + j + '|mo_ta_anh">' + esc(c.mo_ta_anh) + "</textarea></details></div>"; });
      h += "</div>";
    }
    if (pa.viec) h += viecHtml(pa);
    h += '<div class="hang" style="margin-top:12px"><button type="button" class="nut cam" data-sd-dung="' + i + '">' + (pa.da_dung ? "✓ Đã dùng. Thêm lần nữa" : "Dùng bài này cho chiến dịch") + '</button><span class="mo" style="font-size:12.5px">Đưa nội dung' + (pa.kieu === "chu" ? "" : " và hình") + " vào chiến dịch, anh không phải sao chép sang đâu.</span></div></div>";
    return h;
  }

  /* ---------- gọi AI ---------- */
  function khoiPa(p, kieu) {
    p.kieu = kieu; p.imgs = [];
    var n = kieu === "video" ? p.canh.length : kieu === "anh_nhieu" ? p.slides.length : kieu === "anh_1" ? 1 : 0;
    for (var i = 0; i < n; i++) p.imgs.push("");
    p.video_id = ""; p.da_dung = false; p.hashtag = p.hashtag || []; p.tieu_de_phu = p.tieu_de_phu || []; p.mo_ta_ngan = p.mo_ta_ngan || [];
    return p;
  }
  function yeuCauViet(st, extra) {
    var s = S(), o = { nen: s.nen, tang: st.tang, kieu: st.kieu, so_tam: st.so_tam, do_dai: st.do_dai, san_pham: s.mo_ta_san_pham, gia: st.gia, khac_biet: st.khac_biet, khach: st.khach, giong: st.giong, so_phuong_an: st.so_pa, phong_cach: st.phong_cach, ho_so: C.hoSo(), cta: C.defCta() };
    return Object.assign(o, extra || {});
  }
  async function viet() {
    var st = ST(); st.loi = ""; st.dang = "AI đang viết nội dung (khoảng 20 đến 60 giây)...";
    C.ve();
    var j = await api("/tisa-quang-cao/api/ai/viet", yeuCauViet(st));
    if (!j.ok) { st.dang = ""; st.loi = j.error || "AI chưa viết được."; C.ve(); return; }
    st.pa = j.phuong_an.map(function (p) { return khoiPa(p, j.kieu); });
    var b = j.bo_nao || {}; st.bo_nao_ghi = b.co ? "AI đã đọc bộ não: " + (b.da_doc || []).length + " trang (" + (b.da_doc || []).slice(0, 4).join(", ") + ")." : "Bộ não chưa có thông tin sản phẩm nên AI chỉ dựa vào phần anh nhập.";
    st.dang = ""; C.ve();
    if (st.kieu !== "chu" && TT.anh) await tatCaAnh(0, true);
    var el = goc.querySelector("#sdKq"); if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function lenhAnh(pa, j) {
    var st = ST(), s = S(), it = ds(pa)[j] || pa;
    return { nen: s.nen, tang: st.tang, mo_ta_anh: it.mo_ta_anh || pa.mo_ta_anh || "", chu_tren_anh: it.chu_tren_anh || it.chu || pa.chu_tren_anh || "", chen_chu: !!st.chen_chu, phong_cach: st.phong_cach, san_pham: s.mo_ta_san_pham, khac_biet: st.khac_biet, ty_le: tyLe(pa), tham_chieu: refs(), ho_so: C.hoSo(),
      chi_dao: (pa.chi_dao && pa.chi_dao[j] && pa.chi_dao[j].prompt) || "" };
  }
  async function mot(i, j, sua) {
    var st = ST(), pa = st.pa[i]; if (!pa) return;
    var key = "ai|" + i + "|" + j; st.bangAnh = st.bangAnh || {}; st.bangAnh[key] = true; st.loi = ""; st.loiGiao = null; C.ve();
    if (!sua && !pa.chi_dao_xong) await chiDao(i);
    var o = lenhAnh(pa, j);
    if (sua) { o.anh_mau = pa.imgs[j]; o.yeu_cau_sua = sua; }
    var r = await api("/tisa-quang-cao/api/ai/anh", o);
    delete st.bangAnh[key];
    if (r.ok) { C.themTep(r.tep); pa.imgs[j] = r.tep.id; } else { st.loi = r.error || "Tạo ảnh chưa được."; st.loiGiao = r.giao_viec ? i : null; }
    C.ve();
    return !!r.ok;
  }
  function mucCua(pa) {
    return ds(pa).map(function (it) {
      return { y: pa.kieu === "video" ? [it.hinh].filter(Boolean).join(" ") : (it.tieu_de || it.mo_ta || pa.tieu_de || ""), chu: it.chu_tren_anh || it.chu || pa.chu_tren_anh || "", mo_ta: pa.kieu === "video" ? (it.hinh || it.mo_ta_anh || "") : (it.mo_ta_anh || pa.mo_ta_anh || ""), loi: it.loi || "", giay: it.giay || "" };
    });
  }
  function nenYeuCau(pa) {
    var st = ST(), s = S();
    return { nen: s.nen, tang: st.tang, kieu: pa.kieu, san_pham: s.mo_ta_san_pham, khach: st.khach, khac_biet: st.khac_biet, phong_cach: st.phong_cach, chen_chu: !!st.chen_chu, do_dai: st.do_dai, ty_le: tyLe(pa), tieu_de: pa.tieu_de, noi_dung: pa.noi_dung, muc: mucCua(pa), tham_chieu: refs(), ho_so: C.hoSo(), pa: { tieu_de: pa.tieu_de, noi_dung: pa.noi_dung, cta: pa.cta } };
  }
  /* Cộng sự thiết kế đọc bộ não rồi viết lời chỉ đạo cho TỪNG ảnh; chưa có bảng hoặc không kịp thì dùng lời tả có sẵn */
  async function chiDao(i) {
    var st = ST(), pa = st.pa[i]; if (!pa || pa.chi_dao_xong) return;
    pa.chi_dao_xong = true;
    if (!DOI || !DOI.thiet_ke) return;
    var cu = st.dang; st.dang = DOI.thiet_ke.ten + " đang đọc bộ não và viết chỉ đạo hình ảnh (khoảng 1 đến 3 phút)..."; C.ve();
    var r = await api("/tisa-quang-cao/api/ai/chi-dao", nenYeuCau(pa));
    if (r.ok) { pa.chi_dao = r.anh; pa.chi_dao_tu = r.cong_su.ten; } else { pa.chi_dao = null; st.bo_nao_ghi = (r.error || "Cộng sự thiết kế chưa chỉ đạo được.") + " Ảnh được tạo từ lời tả có sẵn."; }
    st.dang = cu === "" ? "" : cu; C.ve();
  }
  async function giao(i, vai) {
    var st = ST(), pa = st.pa[i]; if (!pa) return;
    st.loi = ""; st.loiGiao = null; st.dang = "Đang giao việc cho " + nCs(vai) + "..."; C.ve();
    var o = nenYeuCau(pa); o.vai = vai;
    var r = await api("/tisa-quang-cao/api/giao-sang-tao", o);
    st.dang = "";
    if (!r.ok) { st.loi = r.error || "Chưa giao được việc."; C.ve(); return; }
    pa.viec = { id: r.viec, vai: vai, ten: r.cong_su.ten, chuc: r.cong_su.chuc_danh, status: "hang-doi", plan: [], xong: false, nhan: [] };
    Q.toast("Đã giao việc cho " + r.cong_su.ten + ". Tiến độ hiện ngay dưới phương án này."); C.ve(); theoDoi(pa);
  }
  function nhanTep(pa, ds0) {
    var v = pa.viec; if (!v) return;
    ds0.forEach(function (t) {
      if (v.nhan.indexOf(t.id) >= 0) return;
      v.nhan.push(t.id); C.themTep(t);
      if (t.loai === "video") { if (pa.kieu === "video" && !pa.video_id) pa.video_id = t.id; }
      else { var k = pa.imgs.indexOf(""); if (k >= 0) pa.imgs[k] = t.id; }
    });
  }
  function theoDoi(pa) {
    var v = pa.viec; if (!v || v.xong || DANG_THEO[v.id]) return;
    DANG_THEO[v.id] = true;
    (async function () {
      var lan = 0;
      while (pa.viec && !pa.viec.xong && lan < 480 && goc && document.body.contains(goc)) {
        await cho(6000); lan++;
        var r = await api("/tisa-quang-cao/api/giao-sang-tao/" + v.id);
        if (!r.ok) { v.loi = r.error; C.ve(); continue; }
        v.loi = ""; v.status = r.status; v.plan = r.plan || []; v.xong = !!r.xong; nhanTep(pa, r.tep || []); C.ve();
      }
      delete DANG_THEO[v.id];
    })();
  }
  function viecHtml(pa) {
    var v = pa.viec, tt = { "hang-doi": "Đang chờ nhận việc", "dang-chay": "Đang làm", "cho-duyet": "Đã xong, chờ anh duyệt", "xong": "Đã xong", "dung": "Đã dừng" }[v.status] || v.status || "Đang chờ";
    var h = '<div class="stu-viec"><div class="hang" style="justify-content:space-between"><div><b>Việc đã giao cho ' + esc(v.ten) + '</b> <span class="mo">' + esc(v.chuc || "") + '</span></div><span class="nhan-tt ' + (v.xong ? "ok" : "dung") + '">' + (v.xong ? "● " : "◔ ") + esc(tt) + "</span></div>";
    if ((v.plan || []).length) h += '<div class="mo" style="font-size:12.5px;margin-top:4px">' + v.plan.map(function (p) { return esc((p.ten || "") + ": " + (p.viec || "") + " (" + (p.state || "") + ")"); }).join("<br>") + "</div>";
    h += '<div class="mo" style="font-size:12.5px;margin-top:4px">' + (v.xong ? (v.nhan.length ? "Đã nhận " + v.nhan.length + " tệp cộng sự lưu về, xem ở khung hình ở trên." : "Cộng sự báo xong nhưng chưa thấy ảnh hoặc video trong thư mục của việc. Anh xem ở Giao dự án, hoặc tải tệp lên.") : "Cộng sự đọc bộ não rồi làm. Trang tự nhận ảnh, video khi cộng sự lưu xong (khoảng 2 đến 10 phút).") + (v.loi ? " " + esc(v.loi) : "") + "</div></div>";
    return h;
  }
  async function tatCaAnh(i, tuDong) {
    var st = ST(), pa = st.pa[i], n = pa.imgs.length;
    for (var j = 0; j < n; j++) {
      if (pa.imgs[j] && tuDong) continue;
      st.dang = "Đang tạo ảnh " + (j + 1) + "/" + n + " (mỗi ảnh khoảng 30 đến 60 giây)...";
      var ok = await mot(i, j);
      if (!ok) break;
    }
    st.dang = ""; C.ve();
  }
  function taiLen(file) {
    return new Promise(function (ok, loi) {
      var x = new XMLHttpRequest(); x.open("POST", "/tisa-quang-cao/api/tai-len?loai=anh&ten=" + encodeURIComponent(file.name)); x.withCredentials = true;
      x.onload = function () { var j = {}; try { j = JSON.parse(x.responseText); } catch (e) {} if (j.ok) ok(j.tep); else loi(new Error(j.error || "Tải lên không được.")); };
      x.onerror = function () { loi(new Error("Mạng chập chờn.")); }; x.send(file);
    });
  }
  async function suaChu(i) {
    var st = ST(), pa = st.pa[i], yc = (goc.querySelector('[data-sd-sua-in="' + i + '"]') || {}).value || "";
    if (!yc.trim()) { st.loi = "Anh ghi muốn sửa gì ở ô bên cạnh nút."; C.ve(); return; }
    st.loi = ""; st.dang = "AI đang viết lại..."; C.ve();
    var cu = { ten: pa.ten, cong_thuc: pa.cong_thuc, tieu_de: pa.tieu_de, noi_dung: pa.noi_dung, cta: pa.cta, hashtag: pa.hashtag, tieu_de_phu: pa.tieu_de_phu, mo_ta_ngan: pa.mo_ta_ngan, mo_ta_anh: pa.mo_ta_anh, chu_tren_anh: pa.chu_tren_anh, slides: pa.slides, canh: pa.canh };
    var j = await api("/tisa-quang-cao/api/ai/viet", yeuCauViet(st, { noi_dung_cu: cu, yeu_cau_sua: yc, kieu: pa.kieu, so_phuong_an: 1 }));
    st.dang = "";
    if (!j.ok) { st.loi = j.error || "AI chưa sửa được."; C.ve(); return; }
    var moi = j.phuong_an[0], imgs = pa.imgs, vid = pa.video_id;
    khoiPa(moi, pa.kieu);
    if (moi.imgs.length === imgs.length) moi.imgs = imgs;        // cùng số tấm, cảnh thì giữ ảnh đã tạo
    moi.video_id = vid; st.pa[i] = moi; C.ve();
  }
  async function dungVideo(i) {
    var st = ST(), pa = st.pa[i];
    var canh = pa.canh.map(function (c, j) { return { tep_id: pa.imgs[j], chu: c.chu, giay: parseFloat(String(c.giay).replace(/[^0-9.]/g, "")) || 3 }; });
    if (canh.some(function (c) { return !c.tep_id; })) { st.loi = "Cần tạo ảnh cho đủ các cảnh trước khi dựng video."; C.ve(); return; }
    st.loi = ""; st.dang = "Đang dựng video từ " + canh.length + " cảnh (khoảng 20 đến 60 giây)..."; C.ve();
    var r = await api("/tisa-quang-cao/api/ai/video", { canh: canh, ten: (pa.tieu_de || "video-quang-cao").slice(0, 50) });
    st.dang = "";
    if (!r.ok) st.loi = r.error || "Dựng video chưa được."; else { C.themTep(r.tep); pa.video_id = r.tep.id; }
    C.ve();
  }
  function kichBan(pa) {
    return "KỊCH BẢN VIDEO QUẢNG CÁO: " + (pa.tieu_de || "") + "\nNút kêu gọi: " + pa.cta + "\n\n" + pa.canh.map(function (c, j) { return "Cảnh " + (j + 1) + " (" + c.giay + "s)\n- Hình: " + c.hinh + "\n- Lời: " + c.loi + "\n- Chữ trên màn hình: " + c.chu + "\n- Prompt ảnh/video AI: " + c.mo_ta_anh; }).join("\n\n") + "\n\nNội dung bài đăng kèm:\n" + pa.noi_dung;
  }
  function dung(i) {
    var s = S(), st = ST(), pa = st.pa[i];
    var item = { tieu_de: pa.tieu_de, noi_dung: pa.noi_dung, cta: pa.cta };
    if (s.texts.length === 1 && !s.texts[0].tieu_de && !s.texts[0].noi_dung && !(s.texts[0].slides || []).length) s.texts = [];
    if (pa.kieu === "anh_nhieu") item.slides = pa.slides.map(function (sl, j) { return { media_id: pa.imgs[j] || "", tieu_de: sl.tieu_de, mo_ta: sl.mo_ta }; });
    else if (pa.kieu === "anh_1" && pa.imgs[0]) s.media.push(pa.imgs[0]);
    else if (pa.kieu === "video" && pa.video_id) s.media.push(pa.video_id);
    s.texts.push(item); pa.da_dung = true;
    if (s.nguon === "bai_dang") s.nguon = "ai";
    Q.toast("Đã đưa phương án " + (i + 1) + " vào chiến dịch. Xem ở mục Đã thêm vào chiến dịch bên dưới.");
    C.ve();
  }

  /* ---------- sự kiện ---------- */
  function setSp(pa, path, v) {
    var p = path.split("|"), f = p[0];
    if (/mo_ta_anh$/.test(path)) pa.chi_dao = null;
    if (p.length === 1) {
      if (f === "hashtag") pa.hashtag = v.split(/\s+/).filter(Boolean);
      else if (f === "tieu_de_phu" || f === "mo_ta_ngan") pa[f] = v.split(/\n+/).map(function (x) { return x.trim(); }).filter(Boolean);
      else pa[f] = v;
    } else { var ar = pa[p[0]]; if (ar && ar[+p[1]]) ar[+p[1]][p[2]] = v; }
  }
  function gan(el, ctx) {
    if (goc === el) return;
    goc = el; C = ctx;
    if (!DOI) api("/tisa-quang-cao/api/ai/doi-hinh").then(function (j) { if (j && j.ok) { DOI = j; C.ve(); } });
    if (!DATA) api("/tisa-quang-cao/api/ai/tang").then(function (j) { if (j.ok) { DATA = j; TT = j.trang_thai; C.ve(); } });
    el.addEventListener("click", async function (e) {
      var t = e.target, x;
      if ((x = t.closest("[data-sd-tang]"))) { ST().tang = +x.dataset.sdTang; C.ve(); return; }
      if ((x = t.closest("[data-sd-kieu]"))) { if (!x.disabled) { ST().kieu = x.dataset.sdKieu; C.ve(); } return; }
      if (t.closest("[data-sd-viet]")) { viet(); return; }
      if ((x = t.closest("[data-sd-giao]"))) { var g = x.dataset.sdGiao.split("|"); giao(+g[0], g[1]); return; }
      if ((x = t.closest("[data-sd-ref-bo]"))) { var rb = x.dataset.sdRefBo.split("|"), rr = refs(); rr[rb[0]] = rr[rb[0]].filter(function (id) { return id !== rb[1]; }); C.ve(); return; }
      if ((x = t.closest("[data-sd-anh]"))) { var p = x.dataset.sdAnh.split("|"); mot(+p[1], +p[2]); return; }
      if ((x = t.closest("[data-sd-sua-anh]"))) { var q = x.dataset.sdSuaAnh.split("|"), yc = (goc.querySelector('[data-sd-sua-anh-in="' + x.dataset.sdSuaAnh + '"]') || {}).value || ""; if (!yc.trim()) { ST().loi = "Anh ghi muốn sửa gì ở ảnh nhé."; C.ve(); return; } mot(+q[1], +q[2], yc); return; }
      if ((x = t.closest("[data-sd-tat]"))) { tatCaAnh(+x.dataset.sdTat, false); return; }
      if ((x = t.closest("[data-sd-sua]"))) { suaChu(+x.dataset.sdSua); return; }
      if ((x = t.closest("[data-sd-video]"))) { dungVideo(+x.dataset.sdVideo); return; }
      if ((x = t.closest("[data-sd-xoa]"))) { ST().pa.splice(+x.dataset.sdXoa, 1); C.ve(); return; }
      if ((x = t.closest("[data-sd-dung]"))) { dung(+x.dataset.sdDung); return; }
      if ((x = t.closest("[data-sd-chep]"))) { try { await navigator.clipboard.writeText(kichBan(ST().pa[+x.dataset.sdChep])); Q.toast("Đã chép kịch bản."); } catch (er) { Q.toast("Trình duyệt chưa cho chép. Anh bôi đen và chép tay."); } return; }
      if ((x = t.closest("[data-sd-tro-ly]"))) { Q.hoi("Hãy dựng video quảng cáo theo kịch bản dưới đây bằng công cụ video AI đã nối (nếu chưa nối công cụ nào thì nói rõ và hướng dẫn tôi nối). Video dọc 9:16, giữ đúng lời và chữ. Làm xong báo tôi đường dẫn tệp.\n\n" + kichBan(ST().pa[+x.dataset.sdTroLy])); return; }
    });
    el.addEventListener("input", function (e) {
      var t = e.target, x;
      if (t.matches("[data-sd]") && t.tagName !== "SELECT") { var k = t.dataset.sd; if (k === "do_dai_so") { ST().do_dai = Math.max(5, Math.min(180, Math.round(+t.value) || 5)); ST().do_dai_tuy = true; return; } ST()[k] = t.type === "checkbox" ? t.checked : (t.type === "number" ? Math.max(+t.min || 0, Math.min(+t.max || 99, +t.value || +t.min || 0)) : t.value); return; }
      if (t.matches("[data-sp]")) { var p = t.dataset.sp.split("|"), pa = ST().pa[+p[0]]; if (pa) setSp(pa, p.slice(1).join("|"), t.value); return; }
    });
    el.addEventListener("change", async function (e) {
      var t = e.target;
      if (t.matches("[data-sd]") && (t.tagName === "SELECT" || t.type === "checkbox")) { var k = t.dataset.sd; if (k === "do_dai") { if (t.value === "khac") { ST().do_dai_tuy = true; C.ve(); } else { ST().do_dai_tuy = false; ST().do_dai = +t.value; C.ve(); } return; } ST()[k] = t.type === "checkbox" ? t.checked : (k === "so_pa" ? +t.value : t.value); return; }
      if (t.matches("[data-sd-ref]")) {
        var vai = t.dataset.sdRef, fs = Array.prototype.slice.call(t.files || []), rr2 = refs(), tong = rr2.nhan_vat.length + rr2.logo.length + rr2.san_pham.length, toiDa = vai === "logo" ? 1 : 2;
        for (var q = 0; q < fs.length; q++) {
          if (tong >= 4 || rr2[vai].length >= toiDa) { ST().loi = "Tối đa 4 ảnh tham chiếu (nhân vật 2, logo 1, sản phẩm 2)."; break; }
          try { var tp = await taiLen(fs[q]); C.themTep(tp); rr2[vai].push(tp.id); tong++; } catch (er) { ST().loi = er.message; break; }
        }
        C.ve(); return;
      }
      if (t.matches("[data-sd-up]")) {
        var p = t.dataset.sdUp.split("|"), pa = ST().pa[+p[1]], f = t.files && t.files[0]; if (!f || !pa) return;
        try { var tep = await taiLen(f); C.themTep(tep); pa.imgs[+p[2]] = tep.id; } catch (er) { ST().loi = er.message; }
        C.ve();
      }
    });
  }
  window.TisaStudio = { html: html, gan: gan, sauVe: function () { try { ST().pa.forEach(function (pa) { if (pa.viec && !pa.viec.xong) theoDoi(pa); }); } catch (e) {} } };
})();
