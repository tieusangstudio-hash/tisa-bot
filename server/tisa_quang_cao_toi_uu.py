"""tisa_quang_cao_toi_uu.py - GỢI Ý TỐI ƯU DỰA TRÊN SỐ TIỀN CHẠY THẬT (V2.91).

Chủ dặn: phần gợi ý tối ưu phải dựa trên số liệu thật trả về, thêm các lựa chọn tối ưu theo số tiền đang chạy của từng nền tảng để tư vấn
sát nhất. Module này chỉ TÍNH từ số liệu đã có (không gọi nền tảng, không ghi gì, không bật tắt gì):
  - them_goi_y():  các gợi ý thêm (tiền chưa ra kết quả, so sánh nền tảng, tiền chia quá mỏng, tần suất, nhóm lệch nhau trong một chiến dịch,
                   chi tăng nhanh hơn kết quả, ngân sách không tiêu hết, dự báo chi cả tháng).
  - phuong_an():   3 phương án phân bổ lại tiền ngày (An toàn, Cân bằng, Tăng tốc), mỗi phương án liệt kê từng chiến dịch giữ, giảm, tăng hay dừng.
Con số "kết quả thêm dự kiến" là ƯỚC TÍNH THÔ (giả định giá mỗi kết quả của phần tiền tăng thêm kém hơn hiện tại), luôn ghi rõ như vậy.
Mọi hành động chỉ là gợi ý; chủ duyệt rồi mới làm (nút Bật, Tắt, Ngân sách ở bảng vẫn hỏi xác nhận).
"""
from __future__ import annotations

from typing import Dict, List

THU_TU = {"nghiem_trong": 0, "canh_bao": 1, "tu_van": 2, "tot": 3}
_DUNG = ("PAUSED", "DISABLE", "DISABLED", "REMOVED", "ARCHIVED", "CAMPAIGN_PAUSED", "ADSET_PAUSED")
_TEN_NEN = {"facebook": "Facebook / Meta", "tiktok": "TikTok", "google": "Google Ads"}


def _so(v) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def _fmt(v: float, tt: str) -> str:
    return ("{:,.0f}".format(v).replace(",", ".") + " đ") if tt == "VND" else "{:,.2f} {}".format(v, tt)


def _tron(v: float, tt: str) -> float:
    """Làm tròn số tiền cho dễ đọc: VND tròn nghìn, tiền khác tròn 1 đơn vị."""
    return round(v / 1000.0) * 1000.0 if tt == "VND" else round(v, 0)


def _dang_chay(c: dict) -> bool:
    return str(c.get("trang_thai") or "").upper() not in _DUNG


def _chuan(gom: dict, muc_tieu: dict) -> dict:
    tong, tt = gom["tong"], gom["tien_te"]
    cpa_mt, roas_mt = _so(muc_tieu.get("muc_tieu_cpa")), _so(muc_tieu.get("muc_tieu_roas"))
    cpa = cpa_mt or _so(tong.get("cpa"))
    nguong = cpa * 2 if cpa else (200_000 if tt == "VND" else 10)
    # Chỉ xếp hạng theo ROAS khi chủ đặt mục tiêu ROAS, hoặc doanh thu thật sự là thước đo (ROAS chung từ 0,5 trở lên). Tài khoản kéo tin nhắn, khách để lại số thì doanh thu gần như 0, phải xét theo giá mỗi kết quả.
    dung_roas = _so(tong.get("doanh_thu")) > 0 and (roas_mt > 0 or (_so(tong.get("roas")) >= 0.5 and sum(1 for c in gom["chien_dich"] if _so(c.get("doanh_thu")) > 0) >= 2))
    return {"cpa": cpa, "cpa_la_muc_tieu": bool(cpa_mt), "roas": roas_mt or _so(tong.get("roas")), "nguong": nguong, "dung_roas": dung_roas}


def _hq(c: dict, ch: dict) -> str:
    """tot | kem | dung (tiền chưa ra kết quả) | vua | it_so (chưa đủ số để kết luận)."""
    chi = _so(c.get("chi_phi"))
    if chi < ch["nguong"]:
        return "it_so"
    kq, dt = _so(c.get("ket_qua")), _so(c.get("doanh_thu"))
    if ch["dung_roas"] and ch["roas"]:
        if kq == 0 and dt == 0:
            return "dung"
        r = _so(c.get("roas"))
        if r >= ch["roas"] * 1.3 and kq >= 3:
            return "tot"
        return "kem" if r < ch["roas"] * 0.7 else "vua"
    if kq == 0:
        return "dung"
    cpa = _so(c.get("cpa"))
    if ch["cpa"]:
        if kq >= 5 and 0 < cpa <= ch["cpa"] * 0.7:
            return "tot"
        if kq >= 3 and cpa >= ch["cpa"] * 1.3:
            return "kem"
    return "vua"


def _ten(c: dict) -> str:
    return "%s (%s)" % (c.get("cd") or "?", _TEN_NEN.get(c.get("nen"), c.get("nen") or ""))


# ---------------------------------------------------------------- 3 phương án phân bổ
def phuong_an(gom: dict, muc_tieu: dict, so_ngay: int) -> dict:
    tt, so_ngay = gom["tien_te"], max(1, int(so_ngay))
    ch = _chuan(gom, muc_tieu)
    cds = [c for c in gom["chien_dich"] if _so(c.get("chi_phi")) > 0 and _dang_chay(c)]
    if not cds:
        return {"co": False, "ly_do": "Chưa có chiến dịch nào đang chạy có chi phí trong kỳ này."}
    hang = []
    for c in cds:
        hq = _hq(c, ch)
        hang.append({"c": c, "hq": hq, "ngay": _so(c["chi_phi"]) / so_ngay})
    tong_ngay = sum(h["ngay"] for h in hang)
    tot = [h for h in hang if h["hq"] == "tot"]
    kem = [h for h in hang if h["hq"] == "kem"]
    dung = [h for h in hang if h["hq"] == "dung"]
    cpa_tot = (sum(_so(h["c"]["chi_phi"]) for h in tot) / max(1.0, sum(_so(h["c"]["ket_qua"]) for h in tot))) if tot else 0.0

    def dung_phuong_an(pid, ten, mo_ta, ty_le_giam_kem, ty_le_dua_sang, tran_tang, he_so_giam):
        dong, giai_phong = [], 0.0
        mat_kq = 0.0
        for h in hang:
            c, ng = h["c"], h["ngay"]
            moi, hd, ly = ng, "Giữ nguyên", ""
            if h["hq"] == "dung":
                moi, hd = 0.0, "Tạm dừng"
                ly = "Đã chi %s trong %d ngày mà chưa có kết quả nào." % (_fmt(_so(c["chi_phi"]), tt), so_ngay)
            elif h["hq"] == "kem":
                moi, hd = ng * (1 - ty_le_giam_kem), "Giảm %d%%" % round(ty_le_giam_kem * 100)
                ly = "%s mỗi kết quả, cao hơn %s." % (_fmt(_so(c["cpa"]), tt), "mục tiêu" if ch["cpa_la_muc_tieu"] else "mức trung bình") if not ch["dung_roas"] else "ROAS %.2f, thấp hơn chuẩn %.2f." % (_so(c["roas"]), ch["roas"])
                mat_kq += _so(c["ket_qua"]) / so_ngay * ty_le_giam_kem * 0.6   # phần cắt đi chủ yếu là phần kém nên chỉ mất khoảng 60% kết quả tương ứng
            elif h["hq"] == "tot":
                ly = "Hiệu quả tốt: %s mỗi kết quả, %d kết quả." % (_fmt(_so(c["cpa"]), tt), _so(c["ket_qua"])) if not ch["dung_roas"] else "ROAS %.2f, tốt hơn chuẩn." % _so(c["roas"])
            elif h["hq"] == "it_so":
                ly = "Chi còn ít, chưa đủ số liệu để kết luận. Cứ để chạy thêm."
            else:
                ly = "Trong mức bình thường."
            giai_phong += max(0.0, ng - moi)
            dong.append({"nen": c.get("nen"), "cd": c.get("cd"), "hien_tai": _tron(ng, tt), "de_xuat": _tron(moi, tt), "hanh_dong": hd, "ly_do": ly, "_h": h})
        chuyen, them_kq = 0.0, 0.0
        if tot and ty_le_dua_sang > 0:
            can_dua = giai_phong * ty_le_dua_sang
            tong_tot = sum(h["ngay"] for h in tot)
            for d in dong:
                h = d["_h"]
                if h["hq"] != "tot":
                    continue
                them = min(can_dua * (h["ngay"] / tong_tot), h["ngay"] * tran_tang)
                d["de_xuat"] = _tron(h["ngay"] + them, tt)
                d["hanh_dong"] = "Tăng %d%%" % round(them / h["ngay"] * 100) if h["ngay"] else "Tăng"
                chuyen += them
            them_kq = (chuyen / (cpa_tot * he_so_giam)) if cpa_tot else 0.0
        for d in dong:
            d.pop("_h", None)
        tiet_kiem = max(0.0, giai_phong - chuyen)
        return {"id": pid, "ten": ten, "mo_ta": mo_ta, "dong": dong, "tong_de_xuat": _tron(tong_ngay - tiet_kiem, tt), "tiet_kiem_ngay": _tron(tiet_kiem, tt),
                "chuyen_ngay": _tron(chuyen, tt), "them_ket_qua_ngay": round(them_kq, 1), "mat_ket_qua_ngay": round(mat_kq, 1),
                "luu_y": "Số kết quả thêm là ước tính thô: giả định phần tiền tăng thêm cho giá mỗi kết quả kém hơn hiện tại %d%%. Tăng ngân sách từng bước, theo dõi 2 ngày rồi tăng tiếp." % round((he_so_giam - 1) * 100) if chuyen else
                        ("Phương án này chỉ cắt phần chưa hiệu quả, không đổ thêm tiền vào đâu." if tiet_kiem else "Chưa có phần nào cần cắt hoặc tăng.")}

    ds = [dung_phuong_an("an_toan", "An toàn: chỉ cắt phần lãng phí", "Dừng phần chưa ra kết quả, giảm phần kém. Không tăng chỗ nào. Hợp khi muốn giữ tiền, chưa chắc về nền tảng.", 0.30, 0.0, 0.0, 1.0),
          dung_phuong_an("can_bang", "Cân bằng: cắt rồi dồn một phần sang chỗ tốt", "Cắt phần kém như trên, dồn khoảng 70% số tiền đó sang các chiến dịch hiệu quả (mỗi chiến dịch tăng tối đa 25%), phần còn lại tiết kiệm.", 0.30, 0.7, 0.25, 1.3),
          dung_phuong_an("tang_toc", "Tăng tốc: dồn hết tiền sang chỗ tốt", "Cắt phần kém mạnh hơn và dồn gần hết sang các chiến dịch hiệu quả (mỗi chiến dịch tăng tối đa 40%). Nhanh hơn nhưng rủi ro hơn, cần theo dõi sát.", 0.40, 1.0, 0.40, 1.6)]
    nhan_xet = []
    if dung:
        nhan_xet.append("%d chiến dịch đã chi %s mà chưa có kết quả." % (len(dung), _fmt(sum(_so(h["c"]["chi_phi"]) for h in dung), tt)))
    if kem:
        nhan_xet.append("%d chiến dịch có giá mỗi kết quả cao." % len(kem))
    if tot:
        nhan_xet.append("%d chiến dịch đang tốt, đáng được tăng ngân sách." % len(tot))
    elif kem or dung:
        nhan_xet.append("Chưa có chiến dịch nào đủ tốt để dồn thêm tiền, nên ưu tiên phương án An toàn rồi thử mẫu mới.")
    if not (dung or kem or tot):
        nhan_xet.append("Các chiến dịch đang ở mức bình thường, chưa có chỗ nào đáng chuyển tiền.")
    return {"co": True, "ky_ngay": so_ngay, "tien_te": tt, "tong_hien_tai_ngay": _tron(tong_ngay, tt), "chuan": {"cpa": round(ch["cpa"]), "roas": round(ch["roas"], 2), "theo_muc_tieu": ch["cpa_la_muc_tieu"]},
            "lua_chon": ds, "nhan_xet": " ".join(nhan_xet)}


# ---------------------------------------------------------------- gợi ý thêm
def them_goi_y(gom: dict, g0: dict, muc_tieu: dict, so_ngay: int, nhom: List[dict]) -> List[Dict]:
    ra: List[Dict] = []
    tt, so_ngay = gom["tien_te"], max(1, int(so_ngay))
    tong = gom["tong"]
    tong_chi = _so(tong.get("chi_phi"))
    if tong_chi <= 0:
        return ra
    ch = _chuan(gom, muc_tieu)
    cds = [c for c in gom["chien_dich"] if _so(c.get("chi_phi")) > 0 and _dang_chay(c)]

    def them(muc, tieu_de, chi_tiet, hanh_dong, nen="", cd=""):
        ra.append({"muc": muc, "nen": nen, "cd": cd, "tieu_de": tieu_de, "chi_tiet": chi_tiet, "hanh_dong": hanh_dong})

    # 1. Tiền đã chi mà chưa ra kết quả (cả tài khoản)
    phi = [c for c in cds if _hq(c, ch) == "dung"]
    if phi:
        s = sum(_so(c["chi_phi"]) for c in phi)
        them("nghiem_trong" if s / tong_chi >= 0.15 else "canh_bao", "Tiền chạy mà chưa ra kết quả: %s (%d%% tổng chi)" % (_fmt(s, tt), round(s / tong_chi * 100)),
             "%d chiến dịch đã chi tổng %s trong %d ngày nhưng chưa có kết quả: %s." % (len(phi), _fmt(s, tt), so_ngay, "; ".join(c["cd"] for c in phi[:4])),
             "Tạm dừng các chiến dịch này sẽ giữ lại khoảng %s mỗi ngày. Xem phương án An toàn bên trên." % _fmt(s / so_ngay, tt))
    # 2. So sánh giữa các nền tảng
    nn = {n: v for n, v in gom["theo_nen"].items() if _so(v.get("chi_phi")) > 0 and _so(v.get("ket_qua")) >= 5 and _so(v.get("cpa")) > 0}
    if len(nn) >= 2:
        tot_n = min(nn, key=lambda n: nn[n]["cpa"])
        te_n = max(nn, key=lambda n: nn[n]["cpa"])
        if nn[te_n]["cpa"] > nn[tot_n]["cpa"] * 1.3:
            chuyen = _so(nn[te_n]["chi_phi"]) / so_ngay * 0.15
            them("tu_van", "%s đang rẻ hơn %s khoảng %d%%" % (_TEN_NEN.get(tot_n, tot_n), _TEN_NEN.get(te_n, te_n), round((1 - nn[tot_n]["cpa"] / nn[te_n]["cpa"]) * 100)),
                 "%s: %s mỗi kết quả (%d kết quả). %s: %s mỗi kết quả (%d kết quả)." % (_TEN_NEN.get(tot_n, tot_n), _fmt(nn[tot_n]["cpa"], tt), nn[tot_n]["ket_qua"],
                                                                                     _TEN_NEN.get(te_n, te_n), _fmt(nn[te_n]["cpa"], tt), nn[te_n]["ket_qua"]),
                 "Thử chuyển khoảng 15%% ngân sách của %s (%s mỗi ngày) sang %s, theo dõi 3 ngày. Hai nền tảng khác tính kết quả khác nhau nên chỉ coi là gợi ý." % (_TEN_NEN.get(te_n, te_n), _fmt(chuyen, tt), _TEN_NEN.get(tot_n, tot_n)))
    # 3. Một chiến dịch chiếm gần hết tiền
    if len(cds) >= 2:
        lon = max(cds, key=lambda c: _so(c["chi_phi"]))
        ty = _so(lon["chi_phi"]) / tong_chi
        if ty >= 0.6:
            hq = _hq(lon, ch)
            them("canh_bao" if hq in ("kem", "dung") else "tu_van", "Một chiến dịch ăn %d%% tổng tiền" % round(ty * 100),
                 "%s chiếm %s trên tổng %s. %s" % (_ten(lon), _fmt(_so(lon["chi_phi"]), tt), _fmt(tong_chi, tt), "Chiến dịch này đang kém nên rủi ro cao." if hq in ("kem", "dung") else "Nếu chiến dịch này giảm hiệu quả thì cả tài khoản bị kéo xuống."),
                 "Giữ 1 đến 2 chiến dịch dự phòng chạy song song với khoảng 20 đến 30% ngân sách để có đường lui.", lon.get("nen", ""), lon.get("cd", ""))
    # 4. Tiền chia quá mỏng
    nho = [c for c in cds if _so(c["chi_phi"]) / tong_chi < 0.05 and _so(c.get("ket_qua")) < 10]
    if len(cds) >= 6 and len(nho) >= 4:
        s = sum(_so(c["chi_phi"]) for c in nho)
        them("tu_van", "Tiền đang chia quá mỏng cho %d chiến dịch nhỏ" % len(nho),
             "%d chiến dịch mỗi cái dưới 5%% tổng chi và dưới 10 kết quả, cộng lại %s. Chi ít quá thì nền tảng không đủ số liệu để học, giá thường cao." % (len(nho), _fmt(s, tt)),
             "Gộp lại còn 2 đến 3 chiến dịch, hoặc tắt các chiến dịch yếu nhất rồi dồn tiền cho phần còn lại.")
    # 5. Chi tăng nhanh hơn kết quả so với kỳ trước
    t0 = (g0 or {}).get("tong") or {}
    chi0, kq0, kq = _so(t0.get("chi_phi")), _so(t0.get("ket_qua")), _so(tong.get("ket_qua"))
    if chi0 > 0 and kq0 > 0:
        dchi, dkq = tong_chi / chi0 - 1, kq / kq0 - 1
        if dchi >= 0.2 and dkq < dchi / 2:
            them("canh_bao", "Chi tăng %d%% nhưng kết quả chỉ tăng %d%%" % (round(dchi * 100), round(dkq * 100)),
                 "So với kỳ trước: chi %s (trước %s), kết quả %d (trước %d). Giá mỗi kết quả đang xấu đi." % (_fmt(tong_chi, tt), _fmt(chi0, tt), kq, kq0),
                 "Xem lại các chiến dịch mới bật hoặc mới tăng ngân sách. Nếu vừa tăng ngân sách thì chờ 2 đến 3 ngày để nền tảng ổn định rồi đánh giá lại.")
        elif dkq >= 0.2 and dchi < dkq / 2 and dchi < 0.15:
            them("tot", "Kết quả tăng %d%% mà tiền gần như giữ nguyên" % round(dkq * 100),
                 "Chi %s (trước %s), kết quả %d (trước %d). Hiệu quả đang tốt lên." % (_fmt(tong_chi, tt), _fmt(chi0, tt), kq, kq0),
                 "Ghi lại những gì vừa thay đổi (mẫu mới, đối tượng mới) để lặp lại. Có thể thử tăng ngân sách phần tốt nhất thêm 20%.")
    # 6. Ngân sách đặt cao mà không tiêu hết
    for c in cds:
        ns = _so(c.get("ngan_sach_ngay"))
        if ns > 0 and so_ngay >= 3:
            tb = _so(c["chi_phi"]) / so_ngay
            if tb < ns * 0.5:
                them("tu_van", "Chiến dịch chỉ tiêu được %d%% ngân sách" % round(tb / ns * 100),
                     "%s: ngân sách %s mỗi ngày nhưng thực chi trung bình %s mỗi ngày." % (_ten(c), _fmt(ns, tt), _fmt(tb, tt)),
                     "Đối tượng có thể quá hẹp hoặc bài kém hấp dẫn nên nền tảng không tiêu được tiền. Mở rộng đối tượng hoặc thêm mẫu mới; chưa nên tăng ngân sách.", c.get("nen", ""), c.get("cd", ""))
                break
    # 7. Cấp nhóm quảng cáo: tần suất, nhóm lệch nhau trong một chiến dịch, nhóm chi nhiều mà ít kết quả
    nhom = [r for r in (nhom or []) if _so(r.get("chi_phi")) > 0 and str(r.get("trang_thai") or "").upper() not in _DUNG]
    for r in sorted(nhom, key=lambda r: -_so(r["chi_phi"])):
        if _so(r.get("tan_suat")) >= 3 and _so(r["chi_phi"]) >= ch["nguong"]:
            them("canh_bao", "Nhóm quảng cáo bị lặp quá nhiều (tần suất %.1f)" % _so(r["tan_suat"]),
                 "%s › %s: mỗi người đã thấy quảng cáo khoảng %.1f lần, chi %s." % (r.get("cd"), r.get("nhom"), _so(r["tan_suat"]), _fmt(_so(r["chi_phi"]), tt)),
                 "Người xem bắt đầu chán. Thay hình hoặc video mới, hoặc mở rộng đối tượng.", r.get("nen", ""), r.get("cd", ""))
            break
    theo_cd: Dict[str, List[dict]] = {}
    for r in nhom:
        theo_cd.setdefault("%s|%s" % (r.get("tk_id") or r.get("tk_ten"), r.get("cd_id")), []).append(r)
    for ds in theo_cd.values():
        ok = [r for r in ds if _so(r.get("ket_qua")) >= 3 and _so(r.get("cpa")) > 0]
        if len(ok) >= 2:
            tot_g, te_g = min(ok, key=lambda r: r["cpa"]), max(ok, key=lambda r: r["cpa"])
            if te_g["cpa"] > tot_g["cpa"] * 2 and _so(te_g["chi_phi"]) >= ch["nguong"]:
                chuyen = _so(te_g["chi_phi"]) / so_ngay * 0.5
                them("tu_van", "Trong chiến dịch \"%s\", một nhóm đắt gấp %.1f lần nhóm kia" % (te_g.get("cd"), te_g["cpa"] / tot_g["cpa"]),
                     "Nhóm \"%s\": %s mỗi kết quả (%d kết quả). Nhóm \"%s\": %s mỗi kết quả (%d kết quả)." % (tot_g.get("nhom"), _fmt(tot_g["cpa"], tt), tot_g["ket_qua"], te_g.get("nhom"), _fmt(te_g["cpa"], tt), te_g["ket_qua"]),
                     "Chuyển khoảng 50%% ngân sách nhóm đắt (%s mỗi ngày) sang nhóm rẻ, hoặc tắt nhóm đắt." % _fmt(chuyen, tt), te_g.get("nen", ""), te_g.get("cd", ""))
                break
    if so_ngay >= 7:
        for r in sorted(nhom, key=lambda r: -_so(r["chi_phi"])):
            if r.get("nen") == "facebook" and _so(r["chi_phi"]) >= ch["nguong"] * 1.5 and 0 < _so(r.get("ket_qua")) < 10 * (so_ngay / 7.0):
                them("tu_van", "Nhóm chi nhiều nhưng ít kết quả để nền tảng học",
                     "%s › %s: chi %s trong %d ngày, chỉ %d kết quả. Meta cần khoảng 50 kết quả mỗi tuần cho mỗi nhóm để chạy ổn định." % (r.get("cd"), r.get("nhom"), _fmt(_so(r["chi_phi"]), tt), so_ngay, _so(r["ket_qua"])),
                     "Gộp các nhóm giống nhau lại thành ít nhóm hơn, mỗi nhóm nhận nhiều tiền hơn.", r.get("nen", ""), r.get("cd", ""))
                break
    # 8. Dự báo chi cả tháng theo nhịp hiện tại
    if so_ngay >= 3:
        tb = tong_chi / so_ngay
        them("tu_van", "Dự báo: nhịp này cả tháng chi khoảng %s" % _fmt(tb * 30, tt),
             "Trung bình %s mỗi ngày (tính trên %d ngày vừa xem)." % (_fmt(tb, tt), so_ngay),
             "Muốn giữ ngân sách tháng thì đặt mức chi tối đa mỗi ngày ở ô Mục tiêu phía trên, trang sẽ cảnh báo khi vượt.")
    return ra
