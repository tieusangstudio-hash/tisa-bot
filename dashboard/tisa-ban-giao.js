/* tisa-ban-giao.js - Nút "Bàn giao" dưới câu trả lời của cộng sự + Phiếu bàn giao tích chọn + chuỗi nối đuôi (V3.39, chủ yêu cầu 21/11/2026).

   Bấm nút: bộ não đọc cuộc chat và soạn phiếu (mục tiêu, các việc, đã chốt, tệp đầu vào, câu còn treo, tiêu chí xong) kèm gợi ý cộng sự nhận.
   Anh tích chọn việc nào giao đi, chọn người nhận, có thể khai thêm các bước nối đuôi, rồi bấm Giao. Máy chủ lưu phiếu thành tệp trong bộ não và
   giao một việc cho cộng sự nhận (server/tisa_ban_giao.py). Khi một bước xong, phiếu cho bước kế được soạn sẵn và hiện ở nút "Phiếu bàn giao chờ anh".
   Nền viết cứng luôn kèm màu chữ (biến --mm-*, tối là mặc định). Không dùng ký tự em dash. */
(function () {
  "use strict";
  var W = typeof window !== "undefined" ? window : {}, D = typeof document !== "undefined" ? document : null;

  function esc(t) {
    return String(t == null ? "" : t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function dong(t) {   // textarea nhiều dòng -> mảng dòng không rỗng
    return String(t || "").split(/\r?\n/).map(function (x) { return x.replace(/^\s*(?:[-*]|\d+[.)])\s*/, "").trim(); }).filter(Boolean);
  }
  function brain() { try { return (typeof W.currentBrainPath === "function" && W.currentBrainPath()) || "brain"; } catch (e) { return "brain"; } }
  function lay(url, opt) {
    return fetch(url, opt).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { j = j || {}; j._http = r.status; return j; }); });
  }
  function guiJson(url, body) { return lay(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) }); }

  var S = null;          // trạng thái phiếu đang mở
  var dangSoan = false;

  var CSS = [
    ".bgx-ov{position:fixed;inset:0;z-index:2147482000;background:rgba(10,18,40,.55);display:flex;align-items:center;justify-content:center;padding:16px}",
    ".bgx-box{width:min(760px,100%);max-height:calc(100vh - 32px);overflow:auto;background:var(--mm-card,#fff);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,#d8deee);border-radius:18px;box-shadow:0 24px 70px rgba(0,0,0,.35);padding:20px 22px;font:14px/1.5 inherit}",
    ".bgx-box h3{margin:0 0 2px;font-size:19px;color:var(--mm-ink,#172033)}",
    ".bgx-sub{color:var(--mm-muted,#5b6478);font-size:13px;margin-bottom:12px}",
    ".bgx-box label.bgx-l{display:block;margin:12px 0 4px;font-weight:700;font-size:13px;color:var(--mm-ink,#172033)}",
    ".bgx-box input[type=text],.bgx-box textarea,.bgx-box select{width:100%;box-sizing:border-box;background:var(--mm-soft2,#f4f6fc);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,#d8deee);border-radius:10px;padding:8px 10px;font:inherit}",
    ".bgx-box textarea{min-height:76px;resize:vertical}",
    ".bgx-viec{display:flex;gap:8px;align-items:flex-start;margin:6px 0}",
    ".bgx-viec input[type=checkbox]{margin-top:10px;width:18px;height:18px;flex:none;accent-color:#ff5a1f}",
    ".bgx-viec textarea{flex:1;min-height:48px}",
    ".bgx-viec button,.bgx-chuoi button{flex:none}",
    ".bgx-chuoi{display:flex;gap:8px;align-items:center;margin:6px 0}",
    ".bgx-chuoi .bgx-so{flex:none;width:26px;height:26px;border-radius:50%;background:#ff5a1f;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:13px}",
    ".bgx-btn{background:var(--mm-soft2,#f4f6fc);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,#d8deee);border-radius:10px;padding:8px 14px;font:inherit;font-weight:700;cursor:pointer}",
    ".bgx-btn.pri{background:#ff5a1f;border-color:#ff5a1f;color:#fff}",
    ".bgx-btn[disabled]{opacity:.55;cursor:default}",
    ".bgx-foot{display:flex;gap:10px;justify-content:flex-end;margin-top:18px;flex-wrap:wrap}",
    ".bgx-warn{background:rgba(255,160,0,.14);color:var(--mm-ink,#172033);border:1px solid rgba(255,160,0,.5);border-radius:10px;padding:8px 10px;margin:8px 0;font-size:13px}",
    ".bgx-hint{color:var(--mm-muted,#5b6478);font-size:12.5px;margin-top:4px}",
    ".bgx-chk{display:flex;gap:8px;align-items:center;margin:10px 0 0;color:var(--mm-ink,#172033)}",
    ".bgx-wait{padding:34px 8px;text-align:center;color:var(--mm-muted,#5b6478)}",
    ".bgx-pill{position:fixed;right:18px;bottom:96px;z-index:2147481000;background:#ff5a1f;color:#fff;border:0;border-radius:999px;padding:10px 16px;font:700 13.5px/1 inherit;cursor:pointer;box-shadow:0 10px 28px rgba(255,90,31,.45)}",
    ".bgx-toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:2147483000;max-width:min(560px,calc(100vw - 24px));padding:12px 16px;border-radius:14px;background:#172f72;color:#fff;font:600 13.5px/1.5 inherit;box-shadow:0 18px 50px rgba(0,0,0,.35)}",
    ".bgx-row{margin:8px 0 2px;display:flex}",
    ".bgx-row .bgx-vis{background:var(--mm-soft2,#f4f6fc);color:var(--mm-ink,#172033);border:1px solid var(--mm-line2,#d8deee);border-radius:999px;padding:6px 14px;font:700 12.5px/1.2 inherit;cursor:pointer;display:inline-flex;align-items:center;gap:6px}",
    ".bgx-row .bgx-vis:hover{border-color:#ff5a1f;color:#ff5a1f}",
    ".msg-act.bgx-act{font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:4px;white-space:nowrap}"
  ].join("\n");

  function nap() {
    if (!D || D.getElementById("bgxCss")) return;
    var st = D.createElement("style"); st.id = "bgxCss"; st.textContent = CSS; D.head.appendChild(st);
  }
  function toast(t, loi) {
    if (!D) return;
    var e = D.createElement("div"); e.className = "bgx-toast"; e.textContent = t; D.body.appendChild(e);
    setTimeout(function () { if (e.parentNode) e.remove(); }, loi ? 12000 : 6000);
  }
  function dong_hop() { var o = D.getElementById("bgOv"); if (o) o.remove(); S = null; }

  /* ---------- vẽ hộp phiếu ---------- */
  function optCs(ds, chon, tru) {
    return '<option value="">Chọn cộng sự...</option>' + ds.filter(function (x) { return !tru || x.slug !== tru; }).map(function (x) {
      return '<option value="' + esc(x.slug) + '"' + (x.slug === chon ? " selected" : "") + ">" + esc(x.name + (x.role ? " - " + x.role : "")) + "</option>";
    }).join("");
  }
  function veViec(v, i) {
    return '<div class="bgx-viec" data-i="' + i + '"><input type="checkbox" class="bgx-ck"' + (v.giao !== false ? " checked" : "") + ' title="Tích để giao việc này">' +
      '<textarea class="bgx-vt" rows="2">' + esc(v.text) + '</textarea><button type="button" class="bgx-btn" data-bgx="xoa-viec" data-i="' + i + '" title="Bỏ dòng này">x</button></div>';
  }
  function veChuoi(sl, i) {
    return '<div class="bgx-chuoi" data-i="' + i + '"><span class="bgx-so">' + (i + 2) + '</span><select class="bgx-cs">' + optCs(S.ds, sl, S.den) + '</select>' +
      '<button type="button" class="bgx-btn" data-bgx="xoa-chuoi" data-i="' + i + '" title="Bỏ bước này">x</button></div>';
  }
  function veHop() {
    var p = S.phieu || {}, h = "";
    h += "<h3>" + (S.cha ? "Phiếu bàn giao tiếp theo" : "Bàn giao việc") + '</h3><div class="bgx-sub">Từ <b>' + esc(S.tu && S.tu.name || "TISA BOT") + "</b>. Tích chọn việc muốn giao đi, người nhận chỉ đọc phiếu này, không đọc cả ô chat.</div>";
    if (S.ai_loi) h += '<div class="bgx-warn">Bộ não chưa soạn được phiếu nên em lập phiếu thô từ câu trả lời. Anh sửa lại các dòng rồi giao nhé.</div>';
    if (S.ai_gia) h += '<div class="bgx-warn">' + esc(S.ai_gia) + "</div>";
    h += '<label class="bgx-l">Giao cho</label><select id="bgDen">' + optCs(S.ds, S.den, S.tu && S.tu.slug) + "</select>";
    if (S.goiY && S.goiY.length) {
      var ten = S.ds.filter(function (x) { return x.slug === S.goiY[0]; })[0];
      if (ten) h += '<div class="bgx-hint">Gợi ý theo chuyên môn: ' + esc(ten.name) + "</div>";
    }
    h += '<label class="bgx-l">Tên phiếu</label><input type="text" id="bgTieu" value="' + esc(p.tieu_de) + '">';
    h += '<label class="bgx-l">Mục tiêu (kết quả cuối cần có)</label><textarea id="bgMuc">' + esc(p.muc_tieu) + "</textarea>";
    h += '<label class="bgx-l">Việc giao đi (tích việc nào giao, bỏ tích việc người bàn giao giữ lại)</label><div id="bgViec">' + (p.viec || []).map(veViec).join("") + "</div>";
    h += '<button type="button" class="bgx-btn" data-bgx="them-viec">+ Thêm việc</button>';
    h += '<label class="bgx-l">Đã chốt / ràng buộc (mỗi dòng một ý)</label><textarea id="bgChot">' + esc((p.da_chot || []).join("\n")) + "</textarea>";
    h += '<label class="bgx-l">Tệp đầu vào (đường dẫn, mỗi dòng một tệp)</label><textarea id="bgVao">' + esc((p.dau_vao || []).join("\n")) + "</textarea>";
    h += '<label class="bgx-l">Còn treo, cần anh xác nhận (mỗi dòng một ý)</label><textarea id="bgTreo">' + esc((p.con_treo || []).join("\n")) + "</textarea>";
    h += '<label class="bgx-l">Xong khi</label><input type="text" id="bgXong" value="' + esc(p.xong_khi) + '">';
    h += '<label class="bgx-l">Sau khi xong, chuyển tiếp cho (nối đuôi, tuỳ chọn)</label><div id="bgChuoi">' + (S.chuoi || []).map(veChuoi).join("") + "</div>";
    if ((S.chuoi || []).length < 5) h += '<button type="button" class="bgx-btn" data-bgx="them-chuoi">+ Thêm bước nối đuôi</button>';
    h += '<label class="bgx-chk"><input type="checkbox" id="bgTuChay"' + (S.tuChay ? " checked" : "") + '> Tự chạy tiếp khi bước trước xong (không bật thì em soạn sẵn phiếu và chờ anh duyệt từng bước)</label>';
    h += '<div class="bgx-hint">Việc đối ngoại như đăng bài, gửi tin, chạy quảng cáo, đưa web lên mạng, thanh toán luôn xin anh duyệt, kể cả khi chạy tự động.</div>';
    h += '<div class="bgx-foot">' + (S.cha ? '<button type="button" class="bgx-btn" data-bgx="bo-qua">Bỏ qua, dừng chuỗi</button>' : "") +
      '<button type="button" class="bgx-btn" data-bgx="dong">Hủy</button><button type="button" class="bgx-btn pri" data-bgx="giao" id="bgGiao">Giao việc</button></div>';
    return h;
  }
  function mo(htmlTrong) {
    nap();
    var o = D.getElementById("bgOv");
    if (!o) {
      o = D.createElement("div"); o.id = "bgOv"; o.className = "bgx-ov";
      o.innerHTML = '<div class="bgx-box" id="bgBox"></div>';
      o.addEventListener("mousedown", function (e) { if (e.target === o) dong_hop(); });
      D.body.appendChild(o);
    }
    D.getElementById("bgBox").innerHTML = htmlTrong;
  }
  function veLai() { mo(veHop()); }

  /* ---------- đọc lại các ô ---------- */
  function thu() {
    if (!S || !D.getElementById("bgTieu")) return;
    var v = []; var rows = D.querySelectorAll("#bgViec .bgx-viec");
    for (var i = 0; i < rows.length; i++) {
      var t = rows[i].querySelector(".bgx-vt").value.trim();
      if (t) v.push({ text: t, giao: rows[i].querySelector(".bgx-ck").checked });
    }
    S.phieu = {
      tieu_de: D.getElementById("bgTieu").value.trim(), muc_tieu: D.getElementById("bgMuc").value.trim(), viec: v,
      da_chot: dong(D.getElementById("bgChot").value), dau_vao: dong(D.getElementById("bgVao").value), con_treo: dong(D.getElementById("bgTreo").value),
      xong_khi: D.getElementById("bgXong").value.trim()
    };
    S.den = D.getElementById("bgDen").value;
    var ch = []; var cs = D.querySelectorAll("#bgChuoi .bgx-cs");
    for (var j = 0; j < cs.length; j++) ch.push(cs[j].value);
    S.chuoi = ch;
    S.tuChay = !!D.getElementById("bgTuChay").checked;
  }
  function giaoNgay() {
    thu();
    if (!S.den) { toast("Anh chọn cộng sự nhận việc trước nhé.", true); return; }
    if (!(S.phieu.viec || []).some(function (x) { return x.giao; })) { toast("Anh tích ít nhất một việc để giao.", true); return; }
    var nut = D.getElementById("bgGiao"); if (nut) { nut.disabled = true; nut.textContent = "Đang giao..."; }
    var chuoi = (S.chuoi || []).filter(Boolean);
    guiJson("/tisa-ban-giao/giao", { sid: S.sid || "", brain: brain(), den: S.den, phieu: S.phieu, chuoi: chuoi, tu_chay: S.tuChay, cha: S.cha || "",
      tu: S.tu && S.tu.slug || "", tu_ten: S.tu && S.tu.name || "" }).then(function (r) {
      if (!r.ok) { if (nut) { nut.disabled = false; nut.textContent = "Giao việc"; } toast(r.loi || "Chưa giao được, anh thử lại.", true); return; }
      dong_hop();
      toast("Đã giao cho " + (r.den_ten || "cộng sự") + " (" + (r.so_viec || 0) + " việc)." + (chuoi.length ? " Xong sẽ chuyển tiếp theo chuỗi." : ""));
      kiemChoDuyet();
    }).catch(function () { if (nut) { nut.disabled = false; nut.textContent = "Giao việc"; } toast("Mất kết nối, anh thử lại.", true); });
  }

  /* ---------- mở phiếu ---------- */
  function moTuTin(sid, mid) {
    if (dangSoan) return;
    dangSoan = true;
    S = { sid: sid, mid: mid, tu: { name: "TISA BOT" }, ds: [], phieu: { viec: [] }, chuoi: [], tuChay: false, den: "", goiY: [], cha: "" };
    mo('<div class="bgx-wait"><b>Đang soạn phiếu bàn giao...</b><br>Bộ não đang đọc cuộc chat và gom việc cho người nhận, thường mất khoảng một phút.<div class="bgx-foot" style="justify-content:center"><button type="button" class="bgx-btn" data-bgx="dong">Hủy</button></div></div>');
    guiJson("/tisa-ban-giao/soan", { sid: sid, mid: mid, brain: brain() }).then(function (r) {
      dangSoan = false;
      if (!D.getElementById("bgOv") || !S) return;     // anh đã hủy trong lúc chờ
      if (!r.ok) { dong_hop(); toast(r.loi || "Chưa soạn được phiếu.", true); return; }
      S.tu = r.tu || S.tu; S.ds = r.ds || []; S.phieu = r.phieu || { viec: [] }; S.ai_loi = !!r.ai_loi; S.goiY = r.goi_y_den || [];
      S.den = S.goiY[0] || "";
      S.chuoi = (r.chuoi_goi_y || []).slice(0, 5);
      veLai();
    }).catch(function () { dangSoan = false; dong_hop(); toast("Mất kết nối khi soạn phiếu, anh thử lại.", true); });
  }
  function moTuNhap(d) {
    S = { sid: "", cha: d.id, tu: { name: d.tu_ten || "TISA BOT" }, ds: [], phieu: d.ban_nhap.phieu, den: d.ban_nhap.den, chuoi: (d.ban_nhap.chuoi || []).map(function (c) { return c.slug || c; }),
      tuChay: !!d.tu_chay, goiY: [d.ban_nhap.den], ai_loi: false, ai_gia: d.ban_nhap.ai_loi || "" };
    lay("/tisa-ban-giao/cong-su?brain=" + encodeURIComponent(brain())).then(function (r) {
      S.ds = (r && r.ds) || [];
      // Người nhận tiếp theo cũng phải nằm trong danh sách (loại người vừa bàn giao khỏi ô nhận, nhưng giữ ở ô chuỗi).
      veLai();
    });
  }

  /* ---------- nút trên mỗi câu trả lời ---------- */
  var ICON = '<svg class="ic" width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="m13 6 6 6-6 6"></path><path d="M3 5v14"></path></svg>';
  function gan(msg) {
    if (!msg || msg.getAttribute("data-bgx") === "1") return;
    var acts = msg.querySelector(".msg-acts"); var sid = msg.getAttribute("data-sid"), mid = msg.getAttribute("data-mid");
    if (!acts || !sid || !mid) return;
    msg.setAttribute("data-bgx", "1");
    var b = D.createElement("button"); b.type = "button"; b.className = "msg-act bgx-act"; b.setAttribute("data-act", "ban-giao");
    b.title = "Bàn giao cho cộng sự khác làm tiếp"; b.innerHTML = ICON + "<span>Bàn giao</span>";
    acts.appendChild(b);
  }
  function laTinBanGiao(m) { var t = String(m.getAttribute("data-md") || m.textContent || "").trim(); return /^(Đã bàn giao cho|.{0,40}đã xong việc được bàn giao)/.test(t) || t.length < 80; }
  /* Nút trong hàng hành động chỉ hiện khi rê chuột, nên câu trả lời CUỐI có thêm một nút hiện sẵn bên dưới (anh khỏi phải đi tìm). */
  function nutHienSan() {
    var ds = D.querySelectorAll("#chatArea .msg-tisa[data-mid][data-sid]"), cuoi = null;
    for (var i = ds.length - 1; i >= 0; i--) { if (!laTinBanGiao(ds[i])) { cuoi = ds[i]; break; } }
    var cu = D.querySelectorAll("#chatArea .bgx-row");
    for (var j = 0; j < cu.length; j++) { if (cu[j].parentNode !== cuoi) cu[j].remove(); }
    if (!cuoi || cuoi.querySelector(".bgx-row")) return;
    var r = D.createElement("div"); r.className = "bgx-row";
    r.innerHTML = '<button type="button" class="bgx-vis" data-act="ban-giao" title="Soạn phiếu rồi giao việc này cho cộng sự khác làm tiếp">' + ICON + "<span>Bàn giao cho cộng sự khác</span></button>";
    cuoi.appendChild(r);
  }
  function quet(goc) {
    if (!D) return;
    var ds = (goc || D).querySelectorAll ? (goc || D).querySelectorAll(".msg-tisa") : [];
    for (var i = 0; i < ds.length; i++) gan(ds[i]);
    if (goc && goc.classList && goc.classList.contains("msg-tisa")) gan(goc);
    nutHienSan();
  }
  function batDau() {
    nap();
    var area = D.getElementById("chatArea");
    var dem = 0;
    function lap() { clearTimeout(dem); dem = setTimeout(function () { quet(D); }, 120); }
    if (area && typeof MutationObserver === "function") {
      new MutationObserver(lap).observe(area, { childList: true, subtree: true });
    } else { setInterval(function () { quet(D); }, 3000); }
    quet(D);
    // Trang Cộng sự có thể dựng khung chat sau: dò lại thưa thớt.
    setInterval(function () { if (!area || !D.contains(area)) { area = D.getElementById("chatArea"); if (area && typeof MutationObserver === "function") new MutationObserver(lap).observe(area, { childList: true, subtree: true }); } quet(D); }, 4000);
    D.addEventListener("click", function (e) {
      var t = e.target && e.target.closest ? e.target.closest("[data-act='ban-giao'],[data-bgx]") : null;
      if (!t) return;
      var act = t.getAttribute("data-bgx");
      if (t.getAttribute("data-act") === "ban-giao") {
        e.preventDefault(); e.stopPropagation();
        var m = t.closest(".msg-tisa"); if (m) moTuTin(m.getAttribute("data-sid"), m.getAttribute("data-mid"));
        return;
      }
      if (!act || !S && act !== "dong") return;
      e.preventDefault(); e.stopPropagation();
      if (act === "dong") { dangSoan = false; dong_hop(); return; }
      if (act === "them-viec") { thu(); S.phieu.viec.push({ text: "", giao: true }); veLai(); return; }
      if (act === "xoa-viec") { thu(); S.phieu.viec.splice(+t.getAttribute("data-i"), 1); veLai(); return; }
      if (act === "them-chuoi") { thu(); S.chuoi.push(""); veLai(); return; }
      if (act === "xoa-chuoi") { thu(); S.chuoi.splice(+t.getAttribute("data-i"), 1); veLai(); return; }
      if (act === "giao") { giaoNgay(); return; }
      if (act === "bo-qua") {
        var id = S.cha; dong_hop();
        guiJson("/tisa-ban-giao/bo-qua", { id: id }).then(function () { toast("Đã dừng chuỗi bàn giao."); kiemChoDuyet(); });
      }
    }, true);
  }

  /* ---------- phiếu chờ anh duyệt (bước kế của chuỗi) ---------- */
  var pill = null, dsCho = [];
  function kiemChoDuyet() {
    if (!D || D.hidden) return;
    lay("/tisa-ban-giao/cho-duyet").then(function (r) {
      dsCho = (r && r.ds) || [];
      if (!dsCho.length) { if (pill) { pill.remove(); pill = null; } return; }
      nap();
      if (!pill) {
        pill = D.createElement("button"); pill.type = "button"; pill.className = "bgx-pill";
        pill.addEventListener("click", function () { if (dsCho.length) moTuNhap(dsCho[0]); });
        D.body.appendChild(pill);
      }
      pill.textContent = "Phiếu bàn giao chờ anh (" + dsCho.length + ")";
    }).catch(function () {});
  }

  if (D) {
    var chay = function () { batDau(); kiemChoDuyet(); setInterval(kiemChoDuyet, 30000); };
    if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", chay); else chay();
  }
  W.TISABanGiao = { esc: esc, dong: dong, moTuTin: moTuTin };
  if (typeof module !== "undefined" && module.exports) module.exports = { esc: esc, dong: dong };
})();
