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
      ".tinh-hinh{flex:none;margin:0 0 8px;padding:8px 12px;border:1px solid var(--border,rgba(120,130,170,.28));border-radius:12px;background:var(--bg2,rgba(91,124,255,.06));font-size:13px;display:flex;flex-direction:column;gap:8px}",
      ".tinh-hinh[hidden]{display:none}",
      ".th-head{font-size:11px;letter-spacing:.04em;text-transform:uppercase;opacity:.65;font-weight:600}",
      ".th-job{display:flex;flex-direction:column;gap:5px}",
      ".th-row{display:flex;align-items:center;gap:8px;min-width:0}",
      ".th-dot{width:9px;height:9px;border-radius:50%;flex:none;background:#8a96c8}",
      ".th-job[data-gd=doc] .th-dot{background:#3b82f6;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=lam] .th-dot{background:#22c55e;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=soan] .th-dot{background:#f59e0b;animation:th-pulse 1.3s ease-in-out infinite}",
      ".th-job[data-gd=nhan] .th-dot{animation:th-pulse 1.6s ease-in-out infinite}",
      ".th-ten{flex:1;min-width:0;font-weight:600;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.35}",
      ".th-row2{display:flex;align-items:center;gap:8px;padding-left:17px;flex-wrap:wrap}",
      ".th-pill{flex:none;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:600;background:rgba(138,150,200,.18)}",
      ".th-job[data-gd=doc] .th-pill{background:rgba(59,130,246,.16);color:#2563eb}",
      ".th-job[data-gd=lam] .th-pill{background:rgba(34,197,94,.16);color:#15803d}",
      ".th-job[data-gd=soan] .th-pill{background:rgba(245,158,11,.18);color:#b45309}",
      ".th-time{flex:none;font-variant-numeric:tabular-nums;opacity:.7}",
      ".th-steps{display:flex;flex-wrap:wrap;gap:5px;padding-left:17px}",
      ".th-chip{padding:1px 8px;border-radius:8px;font-size:12px;background:rgba(138,150,200,.14);opacity:.85}",
      ".th-chip.lam{background:rgba(34,197,94,.14)}",
      ".th-chip.now{opacity:1;font-weight:600;outline:1px solid rgba(91,124,255,.5)}",
      ".th-sum{padding-left:17px;opacity:.75;font-size:12px}",
      ".th-now{padding-left:17px;font-weight:600;font-size:13px}",
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
    if (jobs.length) b.appendChild(el("div", "th-head", L("Tình hình công việc", "Work status")));
    jobs.slice(0, 3).forEach(function (j) {
      var box = el("div", "th-job");
      box.dataset.gd = j.giai_doan || "nhan";
      var row = el("div", "th-row");
      row.appendChild(el("span", "th-dot"));
      row.appendChild(el("span", "th-ten", j.ten || ""));
      box.appendChild(row);
      var row2 = el("div", "th-row2");
      row2.appendChild(el("span", "th-pill", j.nhan || ""));
      var tm = el("span", "th-time", clock((Date.now() - (t0[j.id] || Date.now())) / 1000));
      tm.dataset.jid = String(j.id);
      row2.appendChild(tm);
      box.appendChild(row2);
      var bs = j.buoc || [];
      if (bs.length) {
        var steps = el("div", "th-steps");
        bs.forEach(function (s, i) {
          var c = el("span", "th-chip" + (s.loai === "lam" ? " lam" : "") + (i === bs.length - 1 && j.giai_doan !== "soan" ? " now" : ""),
                     (i === bs.length - 1 && j.giai_doan !== "soan" ? "● " : "✓ ") + s.ten);
          steps.appendChild(c);
        });
        box.appendChild(steps);
      }
      var sum;
      if (!j.so_buoc) sum = L("Bộ não đã nhận lệnh và đang suy nghĩ, chưa gọi công cụ nào.", "The brain has the task and is thinking, no tool called yet.");
      else if (j.so_lam) sum = L("Đã triển khai thật: ", "Actually carried out: ") + j.so_lam + L(" thao tác ghi/sửa/chạy, ", " write/edit/run actions, ") + j.so_buoc + L(" bước tất cả.", " steps in all.");
      else sum = L("Mới đọc và tìm hiểu (", "Only reading so far (") + j.so_buoc + L(" bước), chưa ghi hay chạy gì.", " steps), nothing written or run yet.");
      if (j.gan_nhat) box.appendChild(el("div", "th-now", "▶ " + j.gan_nhat));
      box.appendChild(el("div", "th-sum", sum));
      var im = el("div", "th-sum th-im", ""); im.dataset.jid = String(j.id); im.dataset.luc = String(Date.now() - (j.im_giay || 0) * 1000);
      im.textContent = L("Hoạt động gần nhất: ", "Last activity: ") + (j.im_giay || 0) + L(" giây trước", " s ago");
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

  function tick() {
    if (!bar) return;
    var spans = bar.querySelectorAll(".th-time");
    for (var i = 0; i < spans.length; i++) {
      var id = spans[i].dataset.jid;
      spans[i].textContent = clock((Date.now() - (t0[id] || Date.now())) / 1000);
    }
    var ims = bar.querySelectorAll(".th-im");
    for (var k = 0; k < ims.length; k++) {
      ims[k].textContent = L("Hoạt động gần nhất: ", "Last activity: ") + Math.max(0, Math.floor((Date.now() - (+ims[k].dataset.luc || Date.now())) / 1000)) + L(" giây trước", " s ago");
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
    jobs.forEach(function (j) { t0[j.id] = Date.now() - (j.giay || 0) * 1000; });
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
