/* tisa-dau-noi.js - Cộng sự "Đạt Đấu Nối" làm mọi việc nối công cụ (V3.25, chủ yêu cầu 19/11/2026).
   - moPhien(): mở cuộc chat kênh agent:tisa-dau-noi (TISA BOT nạp lời nhắc, kỹ năng, mô hình, mức nỗ lực của cộng sự này), không rời trang Kết nối.
   - moCaiDat(): hộp chọn mô hình + mức nỗ lực cho trợ lý đấu nối (ghi vào hồ sơ cộng sự qua /tisa-dau-noi/cai-dat).
   Không dùng ký tự em dash. */
(function () {
  "use strict";
  var W = window, D = document;
  var SLUG = "tisa-dau-noi", KENH = "agent:" + SLUG;
  var MUC = [["off", "Tắt", "Không suy nghĩ thêm, nhanh nhất"], ["low", "Thấp", "Việc đơn giản"], ["medium", "Vừa", "Cân bằng"],
             ["high", "Cao", "Khuyên dùng: nối chính xác, vẫn nhanh"], ["xhigh", "Rất cao", "Việc khó, nhiều bước"], ["ultra", "Tối đa", "Khó nhất, chậm và tốn hơn"]];
  var MAU = [
    { ten: "Mạnh nhất", mo_ta: "Claude Opus, nỗ lực rất cao", p: "anthropic-cli", m: "claude-opus-5-5", r: "xhigh" },
    { ten: "Cân bằng (khuyên dùng)", mo_ta: "Claude Opus, nỗ lực cao", p: "anthropic-cli", m: "claude-opus-5-5", r: "high" },
    { ten: "Nhanh", mo_ta: "Claude Sonnet, nỗ lực vừa", p: "anthropic-cli", m: "claude-sonnet-5-5", r: "medium" },
    { ten: "Theo mặc định TISA BOT", mo_ta: "Dùng mô hình đang chọn ở khung chat", p: "", m: "", r: "high" }
  ];

  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;"); }
  function lay(url, opt) {
    return fetch(url, opt).then(function (r) { return r.json().catch(function () { return {}; }); });
  }
  function brain() { try { return (typeof W.currentBrainPath === "function" && W.currentBrainPath()) || "brain"; } catch (e) { return "brain"; } }

  /* ---------- mở cuộc chat của cộng sự ---------- */
  function moPhien() {
    if (!W.TISASessions || typeof W.TISASessions.open !== "function") return Promise.resolve(false);
    return lay("/tisa-dau-noi/cai-dat").then(function (t) {
      if (!t || !t.co_ho_so) return false;      // chưa có hồ sơ cộng sự trong bộ não: quay về chat thường
      var fd = new FormData(); fd.append("brain", brain()); fd.append("channel", KENH);
      return fetch("/sessions/new", { method: "POST", body: fd }).then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (n) {
        if (!n || !n.id) return false;
        return Promise.resolve(W.TISASessions.open(n.id, function () { return true; }, { empty: true })).then(function () { return true; });
      });
    }).catch(function () { return false; });
  }

  /* ---------- hộp cài đặt mô hình + mức nỗ lực ---------- */
  var hop = null;
  function dong() { if (hop) { hop.remove(); hop = null; } D.removeEventListener("keydown", phim, true); }
  function phim(e) { if (e.key === "Escape") { e.stopPropagation(); dong(); } }
  function duLieuNhaCungCap() {
    return lay("/providers").then(function (d) { return ((d && d.providers) || []).filter(function (p) { return p && p.configured; }); }).catch(function () { return []; });
  }
  function tenModel(x) { return typeof x === "string" ? x : String((x && (x.id || x.name || x.model)) || ""); }
  function moCaiDat() {
    dong();
    hop = D.createElement("div"); hop.id = "tdnHop";
    hop.style.cssText = "position:fixed;inset:0;z-index:2147483300;display:grid;place-items:center;background:rgba(10,18,48,.55);padding:16px";
    hop.innerHTML = "<div role='dialog' aria-label='Cài đặt trợ lý đấu nối' style='width:min(560px,100%);max-height:calc(100vh - 32px);overflow:auto;background:var(--mm-base,#fff);color:var(--mm-ink,#172033);border-radius:18px;padding:20px;box-shadow:0 30px 80px -20px rgba(8,16,48,.6);font:14px/1.5 inherit'>" +
      "<div style='display:flex;align-items:center;gap:10px'><b style='flex:1;font-size:17px'>Trợ lý đấu nối · Đạt Đấu Nối</b><button type='button' data-tdn='dong' aria-label='Đóng' style='border:0;background:rgba(23,47,114,.08);width:32px;height:32px;border-radius:9px;cursor:pointer;font-size:15px'>✕</button></div>" +
      "<p style='margin:6px 0 12px;color:var(--mm-muted,#5b6478)'>Cộng sự chuyên nối MCP và API cho TISA BOT: nghiên cứu trước, làm liên tục, tự gỡ lỗi. Chọn mô hình mạnh và mức nỗ lực cao thì nối chính xác hơn, chậm hơn một chút.</p>" +
      "<div id='tdnNoi'>Đang tải...</div></div>";
    D.body.appendChild(hop);
    hop.addEventListener("click", function (e) { if (e.target === hop) dong(); });
    hop.addEventListener("click", bam);
    D.addEventListener("keydown", phim, true);
    Promise.all([lay("/tisa-dau-noi/cai-dat"), duLieuNhaCungCap(), lay("/may-ai/chrome-ho-so").catch(function () { return {}; })]).then(function (r) { TT.hs = (r[2] && r[2].ho_so) || []; ve(r[0] || {}, r[1] || []); });
  }
  var TT = { ds: [], cd: {}, hs: [], td: { loai: "", ho_so: "" }, doiTd: false };
  function ve(t, ds) {
    var o = D.getElementById("tdnNoi"); if (!o) return;
    TT.ds = ds; TT.cd = t.cai_dat || {}; TT.td = { loai: (t.trinh_duyet || {}).loai || "", ho_so: (t.trinh_duyet || {}).ho_so || "" }; TT.doiTd = false;
    if (!t.co_ho_so) { o.innerHTML = "<div style='color:#b45309'>Chưa có hồ sơ cộng sự Đạt Đấu Nối trong bộ não. Khởi động lại TISA BOT rồi mở lại hộp này.</div>"; return; }
    var cd = TT.cd, md = t.mac_dinh || {};
    var p = cd.model_provider || "", m = cd.model || "", r = cd.reasoning || md.reasoning || "high";
    var nut = function (css) { return "padding:8px 14px;border-radius:10px;font:600 13px inherit;cursor:pointer;" + css; };
    var h = "<div style='display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-bottom:14px'>" + MAU.map(function (x, i) {
      return "<button type='button' data-tdn='mau' data-i='" + i + "' style='text-align:left;padding:10px 12px;border-radius:12px;border:1px solid var(--mm-line2,rgba(23,47,114,.2));background:var(--mm-soft2,#f4f6fc);cursor:pointer;color:var(--mm-ink,#172033)'><b style='display:block'>" + esc(x.ten) + "</b><small style='color:var(--mm-muted,#5b6478)'>" + esc(x.mo_ta) + "</small></button>";
    }).join("") + "</div>";
    h += "<label style='display:block;font-weight:600;margin:8px 0 4px'>Nhà cung cấp</label><select id='tdnP' style='width:100%;height:40px;border-radius:10px;border:1px solid rgba(23,47,114,.25);padding:0 10px;background:var(--mm-base,#fff);color:inherit'></select>";
    h += "<label style='display:block;font-weight:600;margin:10px 0 4px'>Mô hình</label><select id='tdnM' style='width:100%;height:40px;border-radius:10px;border:1px solid rgba(23,47,114,.25);padding:0 10px;background:var(--mm-base,#fff);color:inherit'></select>";
    h += "<label style='display:block;font-weight:600;margin:10px 0 4px'>Mức nỗ lực</label><select id='tdnR' style='width:100%;height:40px;border-radius:10px;border:1px solid rgba(23,47,114,.25);padding:0 10px;background:var(--mm-base,#fff);color:inherit'>" +
      MUC.map(function (x) { return "<option value='" + x[0] + "'" + (x[0] === r ? " selected" : "") + ">" + esc(x[1] + " · " + x[2]) + "</option>"; }).join("") + "</select>";
    h += "<label style='display:block;font-weight:600;margin:14px 0 4px'>Trình duyệt khi nối (để nối đúng tài khoản)</label><div id='tdnTd'></div>";
    h += "<div id='tdnTt' style='min-height:22px;margin-top:10px;font-size:13px'></div>";
    h += "<div style='display:flex;gap:8px;justify-content:flex-end;margin-top:8px'><button type='button' data-tdn='dong' style='" + nut("border:1px solid var(--mm-line2,rgba(23,47,114,.25));background:var(--mm-soft2,#f4f6fc);color:var(--mm-ink,#172033)") + "'>Đóng</button><button type='button' data-tdn='luu' style='" + nut("border:0;background:#ff6b35;color:#fff;font-weight:700") + "'>Lưu</button></div>";
    o.innerHTML = h;
    veNha(p, m); veTd();
    D.getElementById("tdnP").addEventListener("change", function () { veMo(this.value, ""); });
  }
  function theTd(v, tieu, mo_ta, bat) {
    return "<button type='button' data-tdn='td' data-v='" + v + "' style='text-align:left;padding:10px 12px;border-radius:12px;cursor:pointer;color:var(--mm-ink,#172033);border:2px solid " + (bat ? "#ff6b35" : "var(--mm-line2,rgba(23,47,114,.2))") + ";background:" + (bat ? "rgba(255,107,53,.08)" : "var(--mm-soft2,#f4f6fc)") + "'><b>" + esc(tieu) + "</b><div style='font-size:12px;color:var(--mm-muted,#5b6478);margin-top:2px'>" + esc(mo_ta) + "</div></button>";
  }
  function veTd() {
    var o = D.getElementById("tdnTd"); if (!o) return;
    var td = TT.td, hs = TT.hs || [];
    var h = "<div style='display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))'>" +
      theTd("rieng", "① Chạy ngầm", "Trình duyệt riêng của TISA BOT, hiện ngay trong khung bên phải. Anh đăng nhập tài khoản cần nối một lần ngay trong khung, lần sau tự nhớ.", td.loai === "rieng") +
      theTd("chrome", "② Chrome ngoài", "Mở tab ở cửa sổ Chrome bên ngoài, dùng hồ sơ Chrome đã đăng nhập sẵn ĐÚNG tài khoản cần nối (Google, Meta, Cloudflare...).", td.loai === "chrome") + "</div>";
    if (td.loai === "chrome") {
      h += "<select id='tdnH' style='width:100%;height:40px;border-radius:10px;border:1px solid rgba(23,47,114,.25);padding:0 10px;margin-top:8px;background:var(--mm-base,#fff);color:inherit'>" +
        (td.ho_so ? "" : "<option value=''>Chọn hồ sơ Chrome...</option>") +
        hs.map(function (x) { return "<option value='" + esc(x.thu_muc) + "'" + (x.thu_muc === td.ho_so ? " selected" : "") + ">" + esc((x.ten || x.thu_muc) + (x.email ? " (" + x.email + ")" : " (chưa đăng nhập tài khoản)")) + "</option>"; }).join("") + "</select>";
      if (!hs.length) h += "<div style='margin-top:6px;font-size:12px;color:#b45309'>Không đọc được danh sách hồ sơ Chrome (máy chưa cài Google Chrome, hoặc Chrome chưa mở lần nào).</div>";
    }
    if (!td.loai) h += "<div style='margin-top:6px;font-size:12px;color:var(--mm-muted,#5b6478)'>Chưa chọn: lần đầu bấm \"Nhờ TISA BOT kết nối giúp\", em sẽ hỏi anh một lần rồi nhớ.</div>";
    o.innerHTML = h;
    var sel = D.getElementById("tdnH");
    if (sel) sel.addEventListener("change", function () { TT.td.ho_so = this.value; TT.doiTd = true; });
  }
  function veNha(p, m) {
    var s = D.getElementById("tdnP"); if (!s) return;
    var ds = TT.ds.slice();
    if (p && !ds.some(function (x) { return x.id === p; })) ds.push({ id: p, label: p + " (chưa kết nối)" });
    s.innerHTML = "<option value=''>Theo mặc định của TISA BOT</option>" + ds.map(function (x) { return "<option value='" + esc(x.id) + "'" + (x.id === p ? " selected" : "") + ">" + esc(x.label || x.id) + "</option>"; }).join("");
    veMo(p, m);
  }
  function veMo(p, m) {
    var s = D.getElementById("tdnM"); if (!s) return;
    if (!p) { s.innerHTML = "<option value=''>Theo mặc định</option>"; s.disabled = true; return; }
    s.disabled = false;
    var it = TT.ds.filter(function (x) { return x.id === p; })[0];
    var ds = ((it && it.models) || []).map(tenModel).filter(Boolean);
    var xong = function (lst) {
      if (m && lst.indexOf(m) < 0) lst.unshift(m);
      if (!m && lst.length) m = lst[0];
      var el = D.getElementById("tdnM"); if (!el) return;
      el.innerHTML = lst.map(function (x) { return "<option value='" + esc(x) + "'" + (x === m ? " selected" : "") + ">" + esc(x) + "</option>"; }).join("") || "<option value=''>Chưa có danh sách mô hình</option>";
    };
    xong(ds.slice());
    if (!ds.length && W.TISAModelList && W.TISAModelList.models) {
      Promise.resolve(W.TISAModelList.models(p)).then(function (l) { xong((l || []).map(tenModel).filter(Boolean)); }).catch(function () {});
    }
  }
  function tt(t, loi) { var e = D.getElementById("tdnTt"); if (e) { e.textContent = t || ""; e.style.color = loi ? "#d93025" : "#16a34a"; } }
  function luu(p, m, r) {
    var b = { model_provider: p, model: m, reasoning: r };
    if (TT.doiTd && TT.td.loai) b.trinh_duyet = { loai: TT.td.loai, ho_so: TT.td.loai === "chrome" ? TT.td.ho_so : "" };
    return lay("/tisa-dau-noi/cai-dat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) });
  }
  function bam(e) {
    var b = e.target.closest && e.target.closest("[data-tdn]"); if (!b) return;
    var k = b.getAttribute("data-tdn");
    if (k === "dong") dong();
    else if (k === "td") {
      var v = b.getAttribute("data-v"); if (TT.td.loai === v) return;
      TT.td = { loai: v, ho_so: v === "chrome" && TT.hs.length === 1 ? TT.hs[0].thu_muc : "" }; TT.doiTd = true; veTd();
      tt(v === "chrome" ? "Chọn hồ sơ Chrome đã đăng nhập đúng tài khoản cần nối, rồi bấm Lưu." : "Đã chọn chạy ngầm. Bấm Lưu để áp dụng.", false);
    }
    else if (k === "mau") {
      var x = MAU[Number(b.getAttribute("data-i"))]; if (!x) return;
      veNha(x.p, x.m);
      var r = D.getElementById("tdnR"); if (r) r.value = x.r;
      tt("Đã chọn \"" + x.ten + "\". Bấm Lưu để áp dụng.", false);
    } else if (k === "luu") {
      var p = (D.getElementById("tdnP") || {}).value || "", m = (D.getElementById("tdnM") || {}).value || "", rr = (D.getElementById("tdnR") || {}).value || "high";
      if (TT.doiTd && TT.td.loai === "chrome" && !TT.td.ho_so) { tt("Anh chọn một hồ sơ Chrome trước khi lưu.", true); return; }
      b.disabled = true; tt("Đang lưu...", false);
      luu(p, m, rr).then(function (d) {
        b.disabled = false;
        if (d && d.ok) { tt("Đã lưu. Áp dụng từ lần nhờ kế tiếp.", false); try { W.dispatchEvent(new CustomEvent("tisa-dau-noi-doi")); } catch (x) {} }
        else tt((d && d.loi) || "Chưa lưu được.", true);
      }).catch(function () { b.disabled = false; tt("Chưa lưu được: mất kết nối với TISA BOT.", true); });
    }
  }

  W.TISADauNoi = { slug: SLUG, kenh: KENH, moPhien: moPhien, moCaiDat: moCaiDat, nhan: function (t) { return t && t.cai_dat ? t.cai_dat : {}; } };
})();
