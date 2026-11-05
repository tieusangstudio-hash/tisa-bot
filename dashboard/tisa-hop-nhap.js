// Hộp nhập của TISA BOT, thay hộp prompt() của trình duyệt. Trả về Promise: chữ đã nhập, hoặc null khi huỷ.
window.TISANhap = function (hoi, macDinh) {
  return new Promise(function (xong) {
    var kq = null;
    var hop = document.createElement("dialog");
    hop.className = "tisa-hop-nhap";
    hop.innerHTML = '<form><label><span class="tisa-hop-hoi"></span><input type="text" autocomplete="off" spellcheck="false"></label>' +
      '<div class="tisa-hop-nut"><button type="button" class="tisa-hop-huy"></button><button type="submit" class="tisa-hop-ok"></button></div></form>';
    var o = hop.querySelector("input"), ok = hop.querySelector(".tisa-hop-ok");
    hop.querySelector(".tisa-hop-hoi").textContent = String(hoi || "").replace(/\s*:\s*$/, "");
    hop.querySelector(".tisa-hop-huy").textContent = window.t("common.cancel");
    ok.textContent = window.t("common.save");
    o.value = macDinh || "";
    var doi = function () { ok.disabled = !o.value.trim(); };
    o.addEventListener("input", doi);
    doi();
    hop.querySelector(".tisa-hop-huy").onclick = function () { hop.close(); };
    hop.querySelector("form").onsubmit = function (e) {
      e.preventDefault();
      if (!o.value.trim()) return;
      kq = o.value;
      hop.close();
    };
    // Bấm ra ngoài khung là huỷ: phần đệm nằm trong form nên chỉ nền mờ mới trúng chính hộp.
    hop.onclick = function (e) { if (e.target === hop) hop.close(); };
    hop.addEventListener("close", function () { hop.remove(); xong(kq); });
    document.body.appendChild(hop);
    hop.showModal();
    o.select();
  });
};

// Hộp thông báo và hộp xác nhận của TISA BOT. `coHuy`: có nút Huỷ, trả về true khi đồng ý.
function tisaHop(loiNhan, coHuy) {
  return new Promise(function (xong) {
    var kq = false;
    var hop = document.createElement("dialog");
    var nguyHiem = coHuy && /xo[áa]|gỡ|huỷ|hủy|thu hồi/i.test(String(loiNhan));
    hop.className = "tisa-hop-nhap";
    hop.innerHTML = '<form><p class="tisa-hop-loi"></p><div class="tisa-hop-nut">' +
      (coHuy ? '<button type="button" class="tisa-hop-huy"></button>' : "") +
      '<button type="submit" class="tisa-hop-ok' + (nguyHiem ? " nguy-hiem" : "") + '"></button></div></form>';
    hop.querySelector(".tisa-hop-loi").textContent = String(loiNhan == null ? "" : loiNhan);
    var huy = hop.querySelector(".tisa-hop-huy"), ok = hop.querySelector(".tisa-hop-ok");
    ok.textContent = window.t("common.ok");
    if (huy) {
      huy.textContent = window.t("common.cancel");
      huy.onclick = function () { hop.close(); };
    }
    hop.querySelector("form").onsubmit = function (e) {
      e.preventDefault();
      kq = true;
      hop.close();
    };
    hop.onclick = function (e) { if (e.target === hop) hop.close(); };
    hop.addEventListener("close", function () { hop.remove(); xong(kq); });
    document.body.appendChild(hop);
    hop.showModal();
    ok.focus();
  });
}
window.TISAHoi = function (loiNhan) { return tisaHop(loiNhan, true); };
window.alert = function (loiNhan) { tisaHop(loiNhan, false); };
