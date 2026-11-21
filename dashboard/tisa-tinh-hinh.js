/* tisa-tinh-hinh.js - THANH BÁO CÁO TÌNH HÌNH khi giao việc bằng giọng nói (V2.91).

   Chủ báo: giao việc xong mà màn hình không cho biết AI đang làm hay đang làm tới đâu, có triển
   khai hay không. Server gửi khung {"type":"jobs", jobs:[...], xong:[...]} mỗi khi việc nhận,
   đổi bước, hoặc xong (voice-live.js chuyển nó thành sự kiện "tisa-live-jobs"). Thanh này vẽ:
   tên việc, giai đoạn (nhận lệnh / tìm hiểu / triển khai / soạn kết quả), đồng hồ chạy, số bước
   đã chạy, vài bước gần nhất, và dòng "Xong" hoặc "Lỗi" vài giây sau khi việc kết thúc.
   Chỉ vẽ số liệu thật server báo, không đoán phần trăm. Không dùng ký tự em dash. */
(function () {
  "use strict";
  var bar = null, jobs = [], xong = [], t0 = {}, timer = null;

  function t(k, fb) {
    try { var v = window.TISAi18n && window.TISAi18n.t ? window.TISAi18n.t(k) : ""; if (v && v !== k) return v; } catch (e) {}
    return fb;
  }
  function lang() { try { return (document.documentElement.lang || "vi").slice(0, 2); } catch (e) { return "vi"; } }
  function L(vi, en) { return lang() === "en" ? en : vi; }

  function ensure() {
    if (bar && document.body.contains(bar)) return bar;
    bar = document.getElementById("tinhHinhBar");
    if (!bar) {
      var area = document.getElementById("chatArea");
      if (!area || !area.parentNode) return null;
      bar = document.createElement("div");
      bar.id = "tinhHinhBar";
      bar.hidden = true;
      area.parentNode.insertBefore(bar, area);
    }
    bar.className = "tinh-hinh";
    bar.setAttribute("role", "status");
    bar.setAttribute("aria-live", "polite");
    return bar;
  }

  function injectCss() {
    if (document.getElementById("tinhHinhCss")) return;
    var s = document.createElement("style");
    s.id = "tinhHinhCss";
    s.textContent = [
      ".tinh-hinh{flex:none;margin:0 0 8px;padding:6px 12px;border:1px solid var(--border,rgba(120,130,170,.28));border-radius:12px;background:var(--bg2,rgba(91,124,255,.06));font-size:13px;display:flex;flex-direction:column;gap:8px}",
      ".tinh-hinh[hidden]{display:none}",
      ".th-head{display:none}",
      ".th-job{display:flex;flex-direction:column;gap:3px}",
      ".th-job + .th-job{margin-top:6px;padding-top:6px;border-top:1px solid var(--border,rgba(120,130,170,.22))}",
      ".th-row{display:flex;align-items:center;gap:8px;min-width:0}",
      ".th-dot{width:9px;height:9px;border-radius:50%;flex:none;background:#8a96c8}",
      ".th-job[data-gd=doc] .th-dot{background:#3b82f6;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=lam] .th-dot{background:#22c55e;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=soan] .th-dot{background:#f59e0b;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=nhan] .th-dot{animation:th-pulse 1.6s ease-in-out infinite}",
      ".th-ten{flex:1;min-width:0;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
      ".th-pill{flex:none;padding:1px 9px;border-radius:999px;font-size:12px;font-weight:600;background:rgba(138,150,200,.18)}",
      ".th-job[data-gd=doc] .th-pill{background:rgba(59,130,246,.16);color:#2563eb}",
      ".th-job[data-gd=lam] .th-pill{background:rgba(34,197,94,.16);color:#15803d}",
      ".th-job[data-gd=soan] .th-pill{background:rgba(245,158,11,.18);color:#b45309}",
      ".th-time{flex:none;font-variant-numeric:tabular-nums;opacity:.7;font-size:12px}",
      ".th-row2{display:flex;align-items:center;gap:6px;padding-left:17px;min-width:0;font-size:12px}",
      ".th-chip{flex:none;padding:0 8px;border-radius:8px;background:rgba(138,150,200,.14);opacity:.85}",
      ".th-chip.lam{background:rgba(34,197,94,.14)}",
      ".th-chip.now{opacity:1;font-weight:600;outline:1px solid rgba(91,124,255,.5)}",
      ".th-now{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:.85}",
      ".th-sum{flex:none;opacity:.6;white-space:nowrap}",
      ".th-warn{padding-left:17px;color:#b45309;font-size:12px}",
      ".th-end{display:flex;gap:8px;align-items:center;color:#15803d;font-weight:600}",
      ".th-end.loi{color:#dc2626}",
      "@keyframes th-pulse{0%,100%{opacity:1}50%{opacity:.35}}",
      "@media (prefers-reduced-motion:reduce){.th-dot{animation:none!important}}"
    ].join("\n");
    document.head.appendChild(s);
  }

  function clock(sec) {
    sec = Math.max(0, Math.floor(sec));
    var m = Math.floor(sec / 60), s = sec % 60;
    return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function render() {
    var b = ensure();
    if (!b) return;
    if (!jobs.length && !xong.length) { b.hidden = true; b.textContent = ""; return; }
    b.hidden = false;
    b.textContent = "";
    b.title = L("Tình hình công việc", "Work status");
    jobs.slice(0, 3).forEach(function (j) {
      var box = el("div", "th-job");
      box.dataset.gd = j.giai_doan || "nhan";
      // Dòng 1: chấm, tên việc (một dòng), giai đoạn, đồng hồ.
      var row = el("div", "th-row");
      row.appendChild(el("span", "th-dot"));
      var ten = el("span", "th-ten", j.ten || ""); ten.title = j.ten || "";
      row.appendChild(ten);
      row.appendChild(el("span", "th-pill", j.nhan || ""));
      var tm = el("span", "th-time", clock((Date.now() - (t0[j.id] || Date.now())) / 1000));
      tm.dataset.jid = String(j.id);
      row.appendChild(tm);
      box.appendChild(row);
      // Dòng 2: hai bước gần nhất + việc đang làm + số liệu thật, tất cả trên MỘT dòng.
      var row2 = el("div", "th-row2");
      var bs = (j.buoc || []).slice(-2);
      bs.forEach(function (s, i) {
        var dang = i === bs.length - 1 && j.giai_doan !== "soan";
        row2.appendChild(el("span", "th-chip" + (s.loai === "lam" ? " lam" : "") + (dang ? " now" : ""), (dang ? "● " : "✓ ") + s.ten));
      });
      var now = j.gan_nhat ? el("span", "th-now", j.gan_nhat) : null;
      if (now) { now.title = j.gan_nhat; row2.appendChild(now); } else row2.appendChild(el("span", "th-now", ""));
      var sum;
      if (!j.so_buoc) sum = L("đang suy nghĩ", "thinking");
      else if (j.so_lam) sum = j.so_lam + L(" thao tác thật · ", " real actions · ") + j.so_buoc + L(" bước", " steps");
      else sum = L("mới đọc, chưa ghi/chạy · ", "read only so far · ") + j.so_buoc + L(" bước", " steps");
      row2.appendChild(el("span", "th-sum", sum));
      box.appendChild(row2);
      // Cảnh báo chỉ khi thật sự im lặng lâu: tính ở trình duyệt từ lần đổi bước gần nhất, không tin con số "giây trước" của máy chủ.
      var im = el("div", "th-warn th-im", ""); im.dataset.jid = String(j.id); im.hidden = true;
      box.appendChild(im);
      if (j.canh_bao) box.appendChild(el("div", "th-warn", "⚠ " + j.canh_bao));
      b.appendChild(box);
    });
    if (jobs.length > 3) b.appendChild(el("div", "th-sum", "+" + (jobs.length - 3) + L(" việc nữa đang chạy.", " more running.")));
    xong.forEach(function (x) {
      var d = el("div", "th-end" + (x.loi ? " loi" : ""),
                 (x.loi ? "✕ " + L("Gặp lỗi: ", "Failed: ") : "✓ " + L("Xong: ", "Done: ")) + (x.ten || ""));
      b.appendChild(d);
    });
  }

  var dauVet = {};   // id việc -> {kh: dấu hiệu bước, luc: mốc đổi bước gần nhất}
  function tick() {
    if (!bar) return;
    var spans = bar.querySelectorAll(".th-time");
    for (var i = 0; i < spans.length; i++) {
      var id = spans[i].dataset.jid;
      spans[i].textContent = clock((Date.now() - (t0[id] || Date.now())) / 1000);
    }
    var ims = bar.querySelectorAll(".th-im");
    for (var k = 0; k < ims.length; k++) {
      var v = dauVet[ims[k].dataset.jid];
      var im = v ? Math.floor((Date.now() - v.luc) / 1000) : 0;
      if (im >= 90) { ims[k].hidden = false; ims[k].textContent = "⏳ " + L("Im lặng ", "Quiet for ") + Math.floor(im / 60) + L(" phút, vẫn đang chờ kết quả.", " min, still waiting for the result."); }
      else ims[k].hidden = true;
    }
  }
  function ensureTimer() {
    if (jobs.length && !timer) timer = setInterval(tick, 1000);
    if (!jobs.length && timer) { clearInterval(timer); timer = null; }
  }

  var xongTimers = [];
  function onJobs(d) {
    d = d || {};
    jobs = Array.isArray(d.jobs) ? d.jobs : [];
    jobs.forEach(function (j) {
      t0[j.id] = Date.now() - (j.giay || 0) * 1000;
      var kh = String(j.so_buoc || 0) + "|" + String(j.gan_nhat || "") + "|" + String(j.giai_doan || "");
      if (!dauVet[j.id] || dauVet[j.id].kh !== kh) dauVet[j.id] = { kh: kh, luc: Date.now() };
    });
    if (Array.isArray(d.xong) && d.xong.length) {
      d.xong.forEach(function (x) {
        xong.push(x);
        var h = setTimeout(function () { xong = xong.filter(function (y) { return y !== x; }); render(); }, 9000);
        xongTimers.push(h);
      });
      xong = xong.slice(-3);
    }
    if (d.reset) { xong = []; xongTimers.forEach(clearTimeout); xongTimers = []; }
    render();
    ensureTimer();
  }

  function start() {
    injectCss();
    window.addEventListener("tisa-live-jobs", function (e) { onJobs(e.detail); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
  window.TISATinhHinh = { onJobs: onJobs, clock: clock };
})();
