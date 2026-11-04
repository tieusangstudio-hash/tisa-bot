// Chọn model trong khung chat với nhân sự: cùng danh sách, cùng ghim theo phiên với TISA BOT.
(function () {
  var data = null, CHINH = "auto";
  var EFF = [["off", "Off"], ["low", "Low"], ["medium", "Medium"], ["high", "High"], ["xhigh", "XHigh"], ["ultra", "Ultra"]];
  var css = document.createElement("style");
  css.textContent = ".tm-btn{display:inline-flex!important;align-items:center;gap:6px;border:0!important;background:none!important;box-shadow:none!important;font:inherit;color:inherit;cursor:pointer;padding:0!important;margin:0!important;min-height:0!important;height:auto!important;width:auto!important;white-space:nowrap}" +
    ".tm-dot{width:7px;height:7px;border-radius:50%;background:#16a34a;flex:none}" +
    ".tm-pop{position:fixed;z-index:99999;box-sizing:border-box;width:320px!important;max-width:calc(100vw - 16px)!important;max-height:60vh;overflow:auto;background:#fff;color:#172033;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 12px 32px rgba(15,23,42,.18);padding:8px;font-size:13px;line-height:1.35}" +
    ".tm-pop .tm-row{display:flex!important;align-items:center;gap:8px;width:100%!important;max-width:none!important;min-height:0!important;height:auto!important;box-sizing:border-box;border:0!important;background:none!important;box-shadow:none!important;text-align:left;justify-content:flex-start;padding:8px!important;margin:0!important;border-radius:8px;font:inherit!important;color:inherit!important;cursor:pointer;white-space:nowrap;transform:none!important}" +
    ".tm-pop .tm-row:hover{background:#f3f4f6!important}.tm-pop .tm-row.on{background:#fff1ea!important;color:#c2410c!important;font-weight:600!important}" +
    ".tm-pop .tm-main{border:1px dashed #e5e7eb!important;margin-bottom:6px!important}.tm-pop .tm-find{display:block;width:100%!important;box-sizing:border-box;border:1px solid #fdba74;border-radius:8px;padding:8px;font:inherit;margin:0 0 6px;outline:none;height:auto;min-height:0}" +
    ".tm-pop .tm-prov{font-size:11px!important;font-weight:700!important;letter-spacing:.04em;text-transform:uppercase;color:#6b7280!important;justify-content:space-between}.tm-ok{color:#16a34a;margin-left:6px}.tm-off{color:#9ca3af;font-weight:400;text-transform:none;letter-spacing:0;margin-left:6px}.tm-note{padding:8px;color:#6b7280}";
  document.head.appendChild(css);

  function ten(id) {
    var m = String(id || "").split("/").pop().replace(/[-@]\d{8}$/, "").replace(/^claude-/, "");
    var a = /^(fable|opus|sonnet|haiku)(?:-(\d+)(?:-(\d+))?)?$/.exec(m);
    if (!a) return m;
    return a[1][0].toUpperCase() + a[1].slice(1) + (a[2] ? " " + a[2] + (a[3] ? "." + a[3] : "") : " (mới nhất)");
  }
  function nhanSu() { try { return localStorage.getItem("vp-dm-cur") || "tam"; } catch (e) { return "tam"; } }
  function giaTri() {
    var p = data && data.pins && data.pins[nhanSu()];
    return p && p.provider ? p.provider + "|" + (p.model || "") : CHINH;
  }
  function nhan(v) {
    if (v === CHINH) return "Theo model chính";
    var x = v.split("|");
    return ten(x[1]) || (data.providers.filter(function (p) { return p.id === x[0]; })[0] || {}).label || x[0];
  }
  function dat(sel, v) {
    if (![].some.call(sel.options, function (o) { return o.value === v; })) sel.add(new Option(nhan(v), v));
    sel.value = v;
    sel.dispatchEvent(new Event("change", { bubbles: true }));
    var b = sel.parentNode.querySelector(".tm-btn span:last-child");
    if (b) b.textContent = nhan(v);
  }
  function dong() { var o = document.querySelector(".tm-pop"); if (o) o.remove(); }
  function mo(btn, sel) {
    dong();
    var pop = document.createElement("div"), mo1 = (data.providers.filter(function (p) { return sel.value.indexOf(p.id + "|") === 0; })[0] || data.providers.filter(function (p) { return p.configured; })[0] || {}).id;
    pop.className = "tm-pop";
    function ve(loc) {
      var q = String(loc || "").toLowerCase(), h = "";
      h += '<button type="button" class="tm-row tm-main' + (sel.value === CHINH ? " on" : "") + '" data-v="' + CHINH + '">↻ Theo model của khung chat chính</button>';
      h += '<input class="tm-find" placeholder="Tìm model..." value="' + String(loc || "").replace(/"/g, "&quot;") + '">';
      data.providers.forEach(function (p) {
        var ds = (p.models || []).filter(function (m) { return !q || (m + " " + ten(m)).toLowerCase().indexOf(q) >= 0; });
        if (q && !ds.length) return;
        h += '<button type="button" class="tm-row tm-prov" data-p="' + p.id + '"><span>' + p.label + (p.configured ? '<span class="tm-ok">✓</span>' : '<span class="tm-off">chưa kết nối</span>') + "</span><span>" + (q || mo1 === p.id ? "⌄" : "›") + "</span></button>";
        if (q || mo1 === p.id) {
          if (!p.configured) h += '<div class="tm-note">Vào TISA BOT, trang Models để kết nối ' + p.label + ".</div>";
          else ds.forEach(function (m) { var v = p.id + "|" + m; h += '<button type="button" class="tm-row' + (sel.value === v ? " on" : "") + '" data-v="' + v + '">' + ten(m) + "</button>"; });
        }
      });
      pop.innerHTML = h;
      var i = pop.querySelector(".tm-find");
      i.oninput = function () { ve(i.value); var j = pop.querySelector(".tm-find"); j.focus(); j.setSelectionRange(j.value.length, j.value.length); };
    }
    pop.onclick = function (e) {
      var r = e.target.closest(".tm-row");
      if (!r) return;
      e.preventDefault(); e.stopPropagation();
      if (r.dataset.p) { mo1 = mo1 === r.dataset.p ? "" : r.dataset.p; ve(pop.querySelector(".tm-find").value); return; }
      dat(sel, r.dataset.v); dong();
    };
    ve("");
    document.body.appendChild(pop);
    var b = btn.getBoundingClientRect(), h = pop.offsetHeight;
    pop.style.left = Math.max(8, Math.min(b.left, innerWidth - 310)) + "px";
    pop.style.top = (b.top - h - 8 > 8 ? b.top - h - 8 : b.bottom + 8) + "px";
    pop.querySelector(".tm-find").focus();
  }
  document.addEventListener("click", function (e) { if (!e.target.closest(".tm-pop") && !e.target.closest(".tm-btn")) dong(); });

  function gan() {
    var sel = document.getElementById("dm-model"), eff = document.getElementById("dm-effort");
    if (!sel || !data) return;
    var ma = nhanSu();
    if (sel.dataset.tm !== ma) {
      sel.dataset.tm = ma;
      sel.innerHTML = "";
      sel.add(new Option("Theo model chính", CHINH));
      sel.style.display = "none";
      var cu = sel.parentNode.querySelector(".tm-btn");
      if (cu) cu.remove();
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = "tm-btn";
      btn.innerHTML = '<i class="tm-dot"></i><span></span>';
      btn.onclick = function (e) { e.preventDefault(); e.stopPropagation(); document.querySelector(".tm-pop") ? dong() : mo(btn, sel); };
      sel.parentNode.appendChild(btn);
      dat(sel, giaTri());
    }
    if (eff && eff.dataset.tm !== ma) {
      eff.dataset.tm = ma;
      var mucTheoTrang = (data.levels && data.levels[ma]) || data.reasoning || "off";
      eff.innerHTML = EFF.map(function (x) { return '<option value="' + x[0] + '">' + x[1] + "</option>"; }).join("");
      eff.value = mucTheoTrang;
    }
  }
  async function tai() {
    try {
      var r = await fetch("/api/db/settings/mo_hinh", { credentials: "same-origin" });
      if (r.ok) { data = await r.json(); gan(); }
    } catch (e) { /* vòng sau thử lại */ }
  }
  tai();
  setInterval(tai, 15000);
  new MutationObserver(gan).observe(document.documentElement, { childList: true, subtree: true });
})();
