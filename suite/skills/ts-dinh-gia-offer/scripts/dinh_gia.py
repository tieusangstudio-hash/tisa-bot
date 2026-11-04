#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính GIÁ SÀN, GIÁ TRẦN và biên lãi cho bảng giá 3 gói (Cơ bản – Tiêu chuẩn – Cao cấp).
Thuộc skill /ts-dinh-gia-offer (Bộ skill TISA AI Agent).

CÁCH CHẠY (chỉ cần Python 3):
  macOS:    python3 dinh_gia.py vi-du-dinh-gia.json
  Windows:  py dinh_gia.py vi-du-dinh-gia.json
TÙY CHỌN:  --out bang-gia.md   (lưu kết quả ra file Markdown)

CÔNG THỨC (giải thích đơn giản):
  Chi phí biến đổi/đơn  = tiền tốn thêm mỗi khi bán thêm 1 đơn của gói đó
  Phân bổ cố định/đơn   = Chi phí cố định 1 tháng ÷ Tổng số đơn dự kiến 1 tháng
  Phí theo % giá        = phí cổng thanh toán, phí sàn, hoa hồng, thuế khoán… (tính trên giá bán)
  Giá hòa vốn           = (Biến đổi + Phân bổ cố định) ÷ (1 − Phí %)              → bán thấp hơn là LỖ
  GIÁ SÀN               = (Biến đổi + Phân bổ cố định) ÷ (1 − Phí % − Biên mong muốn)
  GIÁ TRẦN (tham chiếu) = thấp hơn trong 2 mốc:
                            • Theo giá trị: Giá trị khách cảm nhận × Tỉ lệ chia sẻ giá trị (mặc định 30%)
                            • Theo đối thủ: Giá đối thủ cao nhất cùng tầng × (1 + Phần bù khác biệt, mặc định 20%)
  Biên lãi gộp          = (Giá − Biến đổi − Phí) ÷ Giá
  Lãi ròng/đơn          = Giá − Biến đổi − Phí − Phân bổ cố định
  Chỉ số giá trị        = (Kết quả mơ ước × Khả năng tin đạt được) ÷ (Thời gian chờ × Công sức)  [mỗi yếu tố 1–10]
"""

import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def loi(tb):
    print("LỖI: " + tb, file=sys.stderr)
    sys.exit(1)


def md(x):
    return str(x if x is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def tien(x):
    """1234567 -> '1.234.567 đ' (làm tròn nghìn khi lớn)."""
    if x is None:
        return "—"
    am = x < 0
    x = abs(x)
    s = f"{round(x):,}".replace(",", ".") + " đ"
    return ("−" + s) if am else s


def pt(x):
    if x is None:
        return "—"
    return f"{x * 100:.1f}".replace(".", ",").replace("-", "−") + "%"


def so(x, ten):
    try:
        return float(x)
    except (TypeError, ValueError):
        loi(f"'{ten}' phải là số, đang là '{x}'.")


def tong_chi_phi(muc, ten):
    """Nhận số hoặc danh sách {ten, so_tien} → tổng."""
    if isinstance(muc, (int, float)):
        return float(muc), []
    if isinstance(muc, list):
        tong, chi_tiet = 0.0, []
        for i, m in enumerate(muc, 1):
            if not isinstance(m, dict):
                loi(f"'{ten}' mục {i} phải có dạng {{\"ten\": ..., \"so_tien\": ...}}.")
            v = so(m.get("so_tien"), f"{ten}[{i}].so_tien")
            tong += v
            chi_tiet.append((m.get("ten", f"Mục {i}"), v))
        return tong, chi_tiet
    loi(f"'{ten}' phải là số hoặc danh sách khoản chi.")


def chi_so_gia_tri(pt_gt):
    if not isinstance(pt_gt, dict):
        return None
    try:
        kq = float(pt_gt["ket_qua"])
        tin = float(pt_gt["kha_nang_tin"])
        tg = float(pt_gt["thoi_gian_cho"])
        cs = float(pt_gt["cong_suc"])
    except (KeyError, TypeError, ValueError):
        loi("'phuong_trinh_gia_tri' cần đủ 4 số 1–10: ket_qua, kha_nang_tin, thoi_gian_cho, cong_suc.")
    for v in (kq, tin, tg, cs):
        if not 1 <= v <= 10:
            loi("Điểm phương trình giá trị phải nằm trong 1–10.")
    return round(kq * tin / (tg * cs), 2)


def main():
    p = argparse.ArgumentParser(description="Tính giá sàn, giá trần, biên lãi cho 3 gói.")
    p.add_argument("file_json")
    p.add_argument("--out")
    a = p.parse_args()

    try:
        with open(a.file_json, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
    except FileNotFoundError:
        loi(f"Không tìm thấy file '{a.file_json}'.")
    except json.JSONDecodeError as e:
        loi(f"JSON sai cú pháp dòng {e.lineno}, cột {e.colno}: {e.msg}.")

    co_dinh, ct_co_dinh = tong_chi_phi(d.get("chi_phi_co_dinh_thang", 0), "chi_phi_co_dinh_thang")
    phi_pt = so(d.get("phi_phan_tram_tren_gia", 0), "phi_phan_tram_tren_gia")
    bien_mm = so(d.get("bien_loi_nhuan_mong_muon", 0.3), "bien_loi_nhuan_mong_muon")
    chia_se = so(d.get("ti_le_chia_se_gia_tri", 0.3), "ti_le_chia_se_gia_tri")
    phan_bu = so(d.get("phan_bu_khac_biet", 0.2), "phan_bu_khac_biet")
    if phi_pt + bien_mm >= 1:
        loi("Phí % cộng biên mong muốn phải nhỏ hơn 100%.")
    goi = d.get("goi", [])
    if not goi:
        loi("Chưa có gói nào trong 'goi'.")

    tong_don = sum(so(g.get("so_don_du_kien_thang", 0), "so_don_du_kien_thang") for g in goi)
    if tong_don <= 0:
        loi("Cần 'so_don_du_kien_thang' > 0 cho ít nhất 1 gói để phân bổ chi phí cố định.")
    phan_bo = co_dinh / tong_don

    dong, canh_bao, kq_goi = [], [], []
    tong_doanh_thu = tong_lai_gop = 0.0
    for i, g in enumerate(goi, 1):
        ten = g.get("ten", f"Gói {i}")
        gia = so(g.get("gia_ban"), f"{ten}.gia_ban")
        bd, _ = tong_chi_phi(g.get("chi_phi_bien_doi", 0), f"{ten}.chi_phi_bien_doi")
        don = so(g.get("so_don_du_kien_thang", 0), f"{ten}.so_don_du_kien_thang")

        hoa_von = (bd + phan_bo) / (1 - phi_pt)
        san = (bd + phan_bo) / (1 - phi_pt - bien_mm)

        moc_tran = []
        gtcn = g.get("gia_tri_cam_nhan")
        if gtcn is not None:
            moc_tran.append(("giá trị", so(gtcn, f"{ten}.gia_tri_cam_nhan") * chia_se))
        dt = [so(x, f"{ten}.gia_doi_thu") for x in (g.get("gia_doi_thu") or [])]
        if dt:
            moc_tran.append(("đối thủ", max(dt) * (1 + phan_bu)))
        tran = min(v for _, v in moc_tran) if moc_tran else None
        tran_theo = min(moc_tran, key=lambda x: x[1])[0] if moc_tran else None

        phi = gia * phi_pt
        lai_gop = gia - bd - phi
        bien_gop = lai_gop / gia if gia else None
        lai_rong = lai_gop - phan_bo
        csgt = chi_so_gia_tri(g.get("phuong_trinh_gia_tri"))

        if gia < hoa_von:
            tt = "LỖ"
            canh_bao.append(f"- **{ten}** giá {tien(gia)} thấp hơn giá hòa vốn {tien(hoa_von)} (đã gồm phần chi phí cố định) → mỗi đơn đang LỖ. "
                            "Tăng giá trị rồi tăng giá, hoặc cắt chi phí biến đổi — không giảm giá thêm.")
        elif gia < san:
            tt = "DƯỚI SÀN"
            canh_bao.append(f"- **{ten}** giá {tien(gia)} dưới giá sàn {tien(san)} → có lời nhưng chưa đạt biên "
                            f"mong muốn {pt(bien_mm)}.")
        elif tran is not None and gia > tran:
            tt = "TRÊN TRẦN"
            canh_bao.append(f"- **{ten}** giá {tien(gia)} cao hơn giá trần tham chiếu {tien(tran)} (theo {tran_theo}) → "
                            "khách dễ chê đắt. Cần thêm bằng chứng, bảo hành, thành phần giá trị trước khi bán giá này.")
        else:
            tt = "OK"
        if tran is not None and san > tran:
            canh_bao.append(f"- **{ten}**: giá sàn {tien(san)} > giá trần {tien(tran)} → gói này khó có lời ở biên "
                            "mong muốn. Phải tăng giá trị cảm nhận hoặc giảm chi phí.")

        tong_doanh_thu += gia * don
        tong_lai_gop += lai_gop * don
        kq_goi.append({"ten": ten, "gia": gia, "csgt": csgt})
        dong.append(
            f"| {md(ten)} | **{tien(gia)}** | {tien(bd)} | {tien(hoa_von)} | {tien(san)} | "
            f"{tien(tran)}{f' ({tran_theo})' if tran_theo else ''} | {pt(bien_gop)} | {tien(lai_rong)} | "
            f"{'' if csgt is None else str(csgt).replace('.', ',')} | {tt} |"
        )

    # Kiểm tra bậc thang giá (neo giá)
    for trc, sau in zip(kq_goi, kq_goi[1:]):
        if sau["gia"] <= trc["gia"]:
            canh_bao.append(f"- Giá **{sau['ten']}** không cao hơn **{trc['ten']}** → sắp xếp gói từ thấp đến cao.")
        elif sau["gia"] / trc["gia"] < 1.3:
            canh_bao.append(f"- **{sau['ten']}** chỉ đắt hơn **{trc['ten']}** {pt(sau['gia'] / trc['gia'] - 1)} → "
                            "khoảng cách quá gần, khách khó thấy khác biệt (gợi ý gói sau gấp 1,5–3 lần gói trước).")
        if trc["csgt"] is not None and sau["csgt"] is not None and sau["csgt"] <= trc["csgt"]:
            canh_bao.append(f"- Chỉ số giá trị của **{sau['ten']}** không cao hơn **{trc['ten']}** → gói đắt hơn "
                            "phải cho kết quả lớn hơn, nhanh hơn hoặc nhẹ nhàng hơn.")

    loi_nhuan_thang = tong_lai_gop - co_dinh
    ra = [f"# Bảng định giá — {md(d.get('ten', 'sản phẩm'))}", ""]
    ra += ["## Thông số chung", "",
           f"- Chi phí cố định/tháng: **{tien(co_dinh)}**" +
           (" (" + "; ".join(f"{md(t)} {tien(v)}" for t, v in ct_co_dinh) + ")" if ct_co_dinh else ""),
           f"- Tổng số đơn dự kiến/tháng: **{tong_don:g}** → phân bổ cố định mỗi đơn: **{tien(phan_bo)}**",
           f"- Phí theo % giá bán: **{pt(phi_pt)}** · Biên lợi nhuận mong muốn: **{pt(bien_mm)}**",
           f"- Giá trần theo giá trị = {pt(chia_se)} giá trị khách cảm nhận · "
           f"Giá trần theo đối thủ = giá cao nhất + {pt(phan_bu)}", ""]
    ra += ["## Bảng 3 gói", "",
           "| Gói | Giá bán | Chi phí biến đổi | Giá hòa vốn | Giá sàn | Giá trần (theo) | Biên lãi gộp | Lãi ròng/đơn | Chỉ số giá trị | Trạng thái |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    ra += dong
    ra += ["", "## Tổng tháng (theo số đơn dự kiến)", "",
           f"- Doanh thu: **{tien(tong_doanh_thu)}**",
           f"- Lãi gộp (sau chi phí biến đổi và phí): **{tien(tong_lai_gop)}**",
           f"- Lợi nhuận sau chi phí cố định: **{tien(loi_nhuan_thang)}**", ""]
    if loi_nhuan_thang < 0:
        canh_bao.insert(0, "- **Cả tháng đang LỖ** với số đơn dự kiến → xem lại giá hoặc chạy `/ts-ke-hoach-loi-nhuan` "
                           "để tính số đơn cần bán.")
    ra += ["## Cảnh báo", ""]
    ra += canh_bao if canh_bao else ["- Không có cảnh báo. Các gói đều trên sàn và dưới trần."]
    ra += ["", "> Khách chê đắt → **tăng giá trị** (thêm bảo hành, rút ngắn thời gian, giảm công sức, thêm bằng chứng) "
           "chứ không giảm giá."]
    van_ban = "\n".join(ra) + "\n"
    print(van_ban)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(van_ban)
        print(f"Đã lưu: {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
