// Khung chat đang mở tự hiện tin mới đến từ Đội Quân AI, không phải tải lại trang.
(function () {
  var cuoi = {};
  async function tick() {
    if (document.hidden) return;
    var phien = window.TISASessions, chat = window.TISAChatApi;
    var sid = phien && phien.current && phien.current();
    if (!sid) return;
    // Lượt đang chạy thì chữ đang chảy về trang: đợi xong rồi mới xét.
    if (chat && chat.dangChay && chat.dangChay(sid)) return;
    try {
      var r = await fetch("/sessions/" + encodeURIComponent(sid) + "/messages?limit=2", { credentials: "same-origin" });
      if (!r.ok) return;
      var ds = (await r.json()).messages || [], m = ds[ds.length - 1];
      var id = m ? m.id : 0;
      if (cuoi[sid] === undefined) { cuoi[sid] = id; return; }
      if (id === cuoi[sid]) return;
      cuoi[sid] = id;
      // Tin đã có trên trang (do chính trang này gửi) thì khỏi vẽ lại cho đỡ giật.
      var trang = document.body.innerText;
      var thieu = ds.some(function (x) { return trang.indexOf(String(x.content || "").trim().slice(0, 30)) < 0; });
      if (thieu && phien.current() === sid) phien.open(sid);
    } catch (e) { /* mất mạng thoáng qua: vòng sau thử lại */ }
  }
  setInterval(tick, 2000);
})();
