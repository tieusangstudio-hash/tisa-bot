/* Link tệp kết quả trong chat (bộ TISA).
   Mỗi link tệp hiện thành thẻ gọn: nhãn loại tệp có màu + tên tệp.
   Trên máy đang chạy TISA BOT: thêm hai nút biểu tượng "Mở bằng ứng dụng" và "Mở thư mục".
   Máy khác vào qua tên miền: ảnh, video, PDF bấm là xem; slide, Word, Excel tải về như bình thường. */
(function () {
  var MO = /\.(pptx?|key|docx?|pages|rtf|xlsx?|csv|numbers|pdf|png|jpe?g|gif|webp|bmp|heic|svg|mp4|mov|m4v|webm|mkv|avi|mp3|wav|m4a|ogg|flac)$/i;
  var LOAI = [
    [/^(pptx?|key)$/, "slide"], [/^(docx?|pages|rtf)$/, "doc"], [/^(xlsx?|csv|numbers)$/, "sheet"],
    [/^pdf$/, "pdf"], [/^(png|jpe?g|gif|webp|bmp|heic|svg|ico)$/, "anh"], [/^(mp4|mov|m4v|webm|mkv|avi)$/, "video"],
    [/^(mp3|wav|m4a|ogg|flac)$/, "am"], [/^(zip|rar|7z|tar|gz)$/, "nen"]
  ];
  var ICON_MO = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
  var ICON_TM = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>';
  var ICON_OK = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>';
  var maychu = false;

  function brainCua(a) {
    try { return new URL(a.getAttribute("href"), location.href).searchParams.get("brain") || "brain"; }
    catch (e) { return "brain"; }
  }
  function goi(a, cach, nut) {
    var p = a.getAttribute("data-vault-path") || "";
    var cu = nut.innerHTML;
    nut.disabled = true;
    fetch("/tisa-mo-tep", { method: "POST", credentials: "same-origin", headers: { "content-type": "application/json" },
      body: JSON.stringify({ brain: brainCua(a), path: p, cach: cach }) })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (j) {
        nut.disabled = false;
        if (!j || !j.ok) { nut.title = (j && j.error) || "Không mở được"; nut.classList.add("tmt-loi"); return; }
        nut.classList.add("tmt-xong"); nut.innerHTML = ICON_OK;
        setTimeout(function () { nut.classList.remove("tmt-xong"); nut.innerHTML = cu; }, 1400);
      })
      .catch(function () { nut.disabled = false; });
  }
  function nut(icon, tieude, cach, a) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "tmt-nut"; b.innerHTML = icon; b.title = tieude; b.setAttribute("aria-label", tieude);
    b.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); goi(a, cach, b); });
    return b;
  }
  function gan(a) {
    if (a.__tmt) return;
    a.__tmt = 1;
    var p = (a.getAttribute("data-vault-path") || "").split(/[?#]/)[0];
    var duoi = (p.match(/\.([a-z0-9]+)$/i) || ["", ""])[1].toLowerCase();
    var loai = "khac";
    for (var i = 0; i < LOAI.length; i++) if (LOAI[i][0].test(duoi)) { loai = LOAI[i][1]; break; }
    a.classList.add("tmt-the");
    a.setAttribute("data-duoi", (duoi === "jpeg" ? "jpg" : duoi).slice(0, 4).toUpperCase() || "TỆP");
    a.setAttribute("data-loai", loai);
    // Link ghi nguyên đường dẫn dài thì chỉ hiện tên tệp, đường dẫn đầy đủ vẫn ở tooltip.
    var chu = (a.textContent || "").trim();
    if (chu.indexOf("/") >= 0) {
      var w = document.createTreeWalker(a, NodeFilter.SHOW_TEXT), t;
      while ((t = w.nextNode())) if (t.nodeValue.indexOf("/") >= 0) t.nodeValue = t.nodeValue.trim().split("/").pop();
    }
    if (!maychu || (a.nextElementSibling && a.nextElementSibling.classList.contains("tmt-bo"))) return;
    var bo = document.createElement("span");
    bo.className = "tmt-bo";
    if (MO.test(p)) bo.appendChild(nut(ICON_MO, "Mở bằng ứng dụng trên máy này", "mo", a));
    bo.appendChild(nut(ICON_TM, "Mở thư mục chứa tệp", "thu-muc", a));
    a.insertAdjacentElement("afterend", bo);
  }
  function quet(goc) {
    (goc.querySelectorAll ? goc : document).querySelectorAll("a.jv-fdownload").forEach(gan);
  }
  var css = document.createElement("style");
  css.textContent = [
    "a.jv-fdownload.tmt-the{display:inline-flex;align-items:center;gap:8px;max-width:100%;vertical-align:middle;margin:2px 0;",
    "padding:4px 12px 4px 4px;border-radius:10px;border:1px solid color-mix(in srgb,currentColor 14%,transparent);",
    "background:color-mix(in srgb,currentColor 4%,transparent);color:inherit!important;text-decoration:none!important;",
    "font:600 13.5px/1.3 inherit;font-family:inherit;transition:border-color .15s,background .15s,box-shadow .15s}",
    "a.jv-fdownload.tmt-the:hover{border-color:var(--tisa-nhan,#ff6b35);background:color-mix(in srgb,var(--tisa-nhan,#ff6b35) 7%,transparent);",
    "box-shadow:0 2px 10px -4px color-mix(in srgb,var(--tisa-nhan,#ff6b35) 45%,transparent)}",
    "a.jv-fdownload.tmt-the::before{content:attr(data-duoi);flex:none;display:inline-grid;place-items:center;min-width:34px;height:26px;padding:0 5px;",
    "border-radius:7px;font:800 10px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.4px;color:#fff;background:var(--tmt-c,#64748b)}",
    "a.jv-fdownload.tmt-the{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
    "a.tmt-the[data-loai=slide]{--tmt-c:linear-gradient(135deg,#f97316,#ea580c)}",
    "a.tmt-the[data-loai=doc]{--tmt-c:linear-gradient(135deg,#3b82f6,#1d4ed8)}",
    "a.tmt-the[data-loai=sheet]{--tmt-c:linear-gradient(135deg,#22c55e,#15803d)}",
    "a.tmt-the[data-loai=pdf]{--tmt-c:linear-gradient(135deg,#ef4444,#b91c1c)}",
    "a.tmt-the[data-loai=anh]{--tmt-c:linear-gradient(135deg,#a855f7,#7c3aed)}",
    "a.tmt-the[data-loai=video]{--tmt-c:linear-gradient(135deg,#ec4899,#be185d)}",
    "a.tmt-the[data-loai=am]{--tmt-c:linear-gradient(135deg,#14b8a6,#0f766e)}",
    "a.tmt-the[data-loai=nen]{--tmt-c:linear-gradient(135deg,#a8a29e,#57534e)}",
    "a.jv-fdownload.tmt-the.jv-fcode,a.tmt-the code{font:inherit;background:none;padding:0;border:0;color:inherit}",
    ".tmt-bo{display:inline-flex;gap:3px;margin-left:5px;vertical-align:middle}",
    ".tmt-nut{display:inline-grid;place-items:center;width:30px;height:30px;padding:0;border-radius:8px;cursor:pointer;",
    "border:1px solid color-mix(in srgb,currentColor 14%,transparent);background:transparent;color:inherit;opacity:.72;",
    "transition:opacity .15s,background .15s,color .15s,border-color .15s}",
    ".tmt-nut:hover{opacity:1;color:#fff;background:var(--tisa-nhan,#ff6b35);border-color:var(--tisa-nhan,#ff6b35)}",
    ".tmt-nut:disabled{opacity:.4;cursor:default}",
    ".tmt-nut.tmt-xong{opacity:1;color:#fff;background:#16a34a;border-color:#16a34a}",
    ".tmt-nut.tmt-loi{opacity:1;color:#dc2626;border-color:#dc2626}"
  ].join("");
  document.head.appendChild(css);
  function batDau() {
    quet(document);
    new MutationObserver(function (ms) {
      ms.forEach(function (m) { m.addedNodes.forEach(function (n) { if (n.nodeType === 1) { if (n.matches && n.matches("a.jv-fdownload")) gan(n); else quet(n); } }); });
    }).observe(document.body, { childList: true, subtree: true });
  }
  fetch("/tisa-mo-tep/may-chu", { credentials: "same-origin" })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (j) { maychu = !!(j && j.may_chu); batDau(); })
    .catch(function () { batDau(); });
})();
