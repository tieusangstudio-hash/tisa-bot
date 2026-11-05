// Hộp chọn thư mục bộ não: thêm lối tắt tới thư mục quen và gợi ý thư mục giống bộ não.
window.TISAChonThuMuc = async function (moi) {
  var host = document.getElementById("tisaFmQuen");
  if (!host) return;
  host.innerHTML = "";
  var d;
  try { d = await (await fetch("/browse/goi-y")).json(); } catch (e) { return; }
  var nut = function (o, lop, bieuTuong) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = lop;
    b.title = o.duong_dan;
    b.innerHTML = window.ic(bieuTuong);
    var ten = document.createElement("span");
    ten.textContent = o.ten;
    b.appendChild(ten);
    b.onclick = function () { moi(o.duong_dan); };
    return b;
  };
  var hang = document.createElement("div");
  hang.className = "tisa-fm-noi";
  (d.noi || []).forEach(function (o) { hang.appendChild(nut(o, "tisa-fm-chip", "folder")); });
  host.appendChild(hang);
  if ((d.goi_y || []).length) {
    var tieuDe = document.createElement("div");
    tieuDe.className = "tisa-fm-tieu-de";
    tieuDe.textContent = "Có thể là bộ não của bạn";
    host.appendChild(tieuDe);
    d.goi_y.forEach(function (o) { host.appendChild(nut(o, "tisa-fm-goi-y", "brain")); });
  }
};
