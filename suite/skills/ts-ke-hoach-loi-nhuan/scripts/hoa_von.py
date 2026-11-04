#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kế hoạch lợi nhuận & điểm hòa vốn: số đơn hòa vốn, số đơn cần để đạt mục tiêu,
số tháng hồi vốn, bảng dự toán 3 kịch bản, tính ngược số khách / lượt tiếp cận.
Thuộc skill /ts-ke-hoach-loi-nhuan (Bộ skill TISA AI Agent).

CÁCH CHẠY (chỉ cần Python 3):
  macOS:    python3 hoa_von.py vi-du-ke-hoach.json
            python3 hoa_von.py vi-du-ke-hoach.json --out ke-hoach.md --csv du-toan.csv
  Windows:  py hoa_von.py vi-du-ke-hoach.json --csv du-toan.csv
  Excel mở CSV bị dồn vào 1 cột? Chạy lại thêm:  --csv-sep ";"

CÔNG THỨC (lời đơn giản):
  Chi phí biến đổi/đơn (V) = tiền tốn thêm cho mỗi đơn (giá vốn, giao hàng, phí thanh toán, quảng cáo/đơn…)
  Lãi gộp/đơn (P − V)      = Giá bán − Chi phí biến đổi/đơn  (tiền còn lại để trả chi phí cố định và lời)
  Chi phí cố định (FC)     = tiền phải trả mỗi tháng dù bán được hay không (mặt bằng, lương cứng, phần mềm…)
  Điểm hòa vốn Q           = FC ÷ (P − V)      → bán đủ Q đơn/tháng thì không lời không lỗ
  Đơn cần cho mục tiêu     = (FC + Lợi nhuận mục tiêu) ÷ (P − V)
  Tháng hồi vốn            = Vốn ban đầu ÷ Lợi nhuận mỗi tháng
  Nhiều sản phẩm: P và V lấy bình quân theo tỉ trọng số đơn của từng sản phẩm.
  Tính ngược: Khách cần = Đơn cần ÷ Số đơn mỗi khách/tháng; Người hỏi = Khách ÷ Tỉ lệ chốt;
              Lượt tiếp cận = Người hỏi ÷ Tỉ lệ (tiếp cận → hỏi). Tỉ lệ là GIẢ ĐỊNH, cần đo thực tế.
"""

import argparse
import csv
import json
import math
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
    if x is None:
        return "—"
    s = f"{round(abs(x)):,}".replace(",", ".") + " đ"
    return ("−" + s) if x < 0 else s


def nghin(x):
    return f"{int(round(x)):,}".replace(",", ".")


def pt(x):
    if x is None:
        return "—"
    return f"{x * 100:.1f}".replace(".", ",").replace("-", "−") + "%"


def so(x, ten, mac_dinh=None):
    if x is None:
        if mac_dinh is not None:
            return float(mac_dinh)
        loi(f"Thiếu '{ten}'.")
    try:
        return float(x)
    except (TypeError, ValueError):
        loi(f"'{ten}' phải là số, đang là '{x}'.")


def tong(muc, ten):
    """Số hoặc danh sách {ten, so_tien} → (tổng, chi tiết)."""
    if muc is None:
        return 0.0, []
    if isinstance(muc, (int, float)):
        return float(muc), []
    if isinstance(muc, list):
        t, ct = 0.0, []
        for i, m in enumerate(muc, 1):
            if not isinstance(m, dict):
                loi(f"'{ten}' mục {i} cần dạng {{\"ten\": ..., \"so_tien\": ...}}.")
            v = so(m.get("so_tien"), f"{ten}[{i}].so_tien")
            t += v
            ct.append((m.get("ten", f"Mục {i}"), v))
        return t, ct
    loi(f"'{ten}' phải là số hoặc danh sách khoản chi.")


def thang_hoi_von(von, ln):
    if von <= 0:
        return 0.0
    if ln <= 0:
        return None
    return von / ln


def doc_thang(x):
    if x is None:
        return "Không hồi vốn (đang lỗ)"
    if x == 0:
        return "Không cần vốn ban đầu"
    return f"{x:.1f} tháng".replace(".", ",")


def main():
    p = argparse.ArgumentParser(description="Kế hoạch lợi nhuận & điểm hòa vốn.")
    p.add_argument("file_json")
    p.add_argument("--out", help="Lưu báo cáo Markdown")
    p.add_argument("--csv", help="Xuất bảng dự toán 3 kịch bản ra CSV (mở bằng Excel/Google Sheets)")
    p.add_argument("--csv-sep", default=",", help="Dấu phân cách CSV: ',' (mặc định) hoặc ';'")
    a = p.parse_args()

    def so_csv(x):
        """Số thập phân cho CSV: dùng dấu phẩy khi phân cách bằng ';' (Excel tiếng Việt)."""
        if x is None:
            return ""
        s = str(round(x, 1))
        return s.replace(".", ",") if a.csv_sep == ";" else s

    try:
        with open(a.file_json, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
    except FileNotFoundError:
        loi(f"Không tìm thấy file '{a.file_json}'.")
    except json.JSONDecodeError as e:
        loi(f"JSON sai cú pháp dòng {e.lineno}, cột {e.colno}: {e.msg}.")

    muc_tieu = so(d.get("muc_tieu_loi_nhuan_thang"), "muc_tieu_loi_nhuan_thang", 0)
    phi_pt = so(d.get("phi_phan_tram_tren_gia"), "phi_phan_tram_tren_gia", 0)
    fc, ct_fc = tong(d.get("chi_phi_co_dinh_thang"), "chi_phi_co_dinh_thang")
    von, ct_von = tong(d.get("von_ban_dau"), "von_ban_dau")
    sp_ds = d.get("san_pham") or []
    if not sp_ds:
        loi("Cần ít nhất 1 sản phẩm trong 'san_pham'.")

    # Bình quân theo tỉ trọng
    tong_tt = sum(so(s.get("ti_trong"), "ti_trong", 1) for s in sp_ds)
    if tong_tt <= 0:
        loi("Tổng 'ti_trong' của sản phẩm phải > 0.")
    P = V = 0.0
    bang_sp, canh_bao = [], []
    for i, s in enumerate(sp_ds, 1):
        ten = s.get("ten", f"Sản phẩm {i}")
        gia = so(s.get("gia_ban"), f"{ten}.gia_ban")
        v_sp, _ = tong(s.get("chi_phi_bien_doi"), f"{ten}.chi_phi_bien_doi")
        v_sp += gia * phi_pt
        tt = so(s.get("ti_trong"), "ti_trong", 1) / tong_tt
        lg = gia - v_sp
        P += gia * tt
        V += v_sp * tt
        bang_sp.append(f"| {md(ten)} | {tien(gia)} | {tien(v_sp)} | {tien(lg)} | {pt(lg / gia if gia else None)} | {pt(tt)} |")
        if lg <= 0:
            canh_bao.append(f"- **{ten}**: giá bán không đủ bù chi phí biến đổi → bán càng nhiều càng lỗ.")
        elif gia and lg / gia < 0.2:
            canh_bao.append(f"- **{ten}**: tỉ lệ lãi gộp chỉ {pt(lg / gia)} → rất mỏng, một chút biến động chi phí là lỗ.")

    lg_don = P - V
    if lg_don <= 0:
        loi("Lãi gộp bình quân mỗi đơn ≤ 0 → không bao giờ hòa vốn. Tăng giá hoặc giảm chi phí biến đổi trước.")

    q_hv = fc / lg_don
    q_mt = (fc + muc_tieu) / lg_don
    dt_hv = q_hv * P
    dt_mt = q_mt * P

    # Kịch bản
    don_co_so = d.get("so_don_du_kien_thang")
    kb = d.get("kich_ban")
    if not kb:
        goc = so(don_co_so, "so_don_du_kien_thang", math.ceil(q_mt))
        kb = [
            {"ten": "Thận trọng", "so_don_thang": goc * 0.6, "he_so_gia": 1, "he_so_chi_phi_bien_doi": 1.1},
            {"ten": "Cơ sở", "so_don_thang": goc, "he_so_gia": 1, "he_so_chi_phi_bien_doi": 1},
            {"ten": "Tốt", "so_don_thang": goc * 1.4, "he_so_gia": 1, "he_so_chi_phi_bien_doi": 0.95},
        ]
    hang_kb, csv_rows = [], []
    ln_co_so = None
    for k in kb:
        ten = k.get("ten", "?")
        q = so(k.get("so_don_thang"), f"{ten}.so_don_thang")
        hs_gia = so(k.get("he_so_gia"), "he_so_gia", 1)
        hs_v = so(k.get("he_so_chi_phi_bien_doi"), "he_so_chi_phi_bien_doi", 1)
        fc_k = fc + so(k.get("chi_phi_co_dinh_them"), "chi_phi_co_dinh_them", 0)
        p_k, v_k = P * hs_gia, V * hs_v
        dt = q * p_k
        cpbd = q * v_k
        lg = dt - cpbd
        ln = lg - fc_k
        bien = ln / dt if dt else None
        hv_k = fc_k / (p_k - v_k) if p_k > v_k else None
        an_toan = (q - hv_k) / q if (hv_k is not None and q) else None
        hoi_von = thang_hoi_von(von, ln)
        if ten.lower().startswith("cơ sở") or ten.lower().startswith("co so"):
            ln_co_so = ln
        hang_kb.append(
            f"| {md(ten)} | {nghin(q)} | {tien(dt)} | {tien(cpbd)} | {tien(lg)} | {tien(fc_k)} | **{tien(ln)}** | "
            f"{pt(bien)} | {nghin(math.ceil(hv_k)) if hv_k else '—'} | "
            f"{pt(an_toan) if (an_toan is None or an_toan >= 0) else 'Dưới hòa vốn'} | {doc_thang(hoi_von)} |"
        )
        csv_rows.append([ten, round(q), round(dt), round(cpbd), round(lg), round(fc_k), round(ln),
                         f"{round(bien * 100)}%" if bien is not None else "",
                         math.ceil(hv_k) if hv_k else "", (f"{round(an_toan * 100)}%" if an_toan >= 0 else "Dưới hòa vốn") if an_toan is not None else "",
                         so_csv(hoi_von)])
        if ln < 0:
            thang_du_tru = 3
            canh_bao.append(f"- Kịch bản **{ten}** lỗ {tien(-ln)}/tháng → cần quỹ dự phòng ít nhất "
                            f"{tien(-ln * thang_du_tru)} ({thang_du_tru} tháng) để không đứt dòng tiền.")
        if an_toan is not None and 0 <= an_toan < 0.2:
            canh_bao.append(f"- Kịch bản **{ten}**: chỉ bán hơn điểm hòa vốn {pt(an_toan)} → sát mép, "
                            "doanh số giảm nhẹ là lỗ.")
    if ln_co_so is None and len(kb) >= 2:
        k = kb[1]
        q = so(k.get("so_don_thang"), "so_don_thang")
        ln_co_so = q * (P * so(k.get("he_so_gia"), "", 1) - V * so(k.get("he_so_chi_phi_bien_doi"), "", 1)) - fc

    if ln_co_so is not None and muc_tieu > 0 and ln_co_so < muc_tieu:
        hien_tai = f"lời {tien(ln_co_so)}" if ln_co_so >= 0 else f"lỗ {tien(-ln_co_so)}"
        canh_bao.append(f"- Kịch bản **Cơ sở** {hien_tai}/tháng, chưa đạt mục tiêu {tien(muc_tieu)} → "
                        f"cần thêm {nghin(math.ceil((muc_tieu - ln_co_so) / lg_don))} đơn/tháng, "
                        "hoặc tăng lãi gộp mỗi đơn (tăng giá trị rồi tăng giá, giảm chi phí biến đổi).")
    hv_thang = thang_hoi_von(von, ln_co_so if ln_co_so is not None else muc_tieu)
    if hv_thang is not None and hv_thang > 18:
        canh_bao.append(f"- Hồi vốn mất {doc_thang(hv_thang)} (kịch bản cơ sở) → dài, cân nhắc giảm vốn ban đầu "
                        "hoặc thuê thay vì mua.")
    cong_suat = d.get("cong_suat_toi_da_don_thang")
    if cong_suat is not None and q_mt > so(cong_suat, "cong_suat_toi_da_don_thang"):
        canh_bao.append(f"- Cần {nghin(math.ceil(q_mt))} đơn/tháng để đạt mục tiêu nhưng công suất tối đa chỉ "
                        f"{nghin(so(cong_suat, 'cong_suat'))} → phải tăng giá, tăng lãi gộp hoặc mở rộng công suất.")
    if fc > 0 and von > 0 and von < fc * 3:
        canh_bao.append(f"- Vốn ban đầu {tien(von)} chưa bằng 3 tháng chi phí cố định ({tien(fc * 3)}) → "
                        "nên để riêng quỹ dự phòng.")

    # Tính ngược
    pheu = d.get("tinh_nguoc") or {}
    ra_pheu = []
    if pheu:
        don_moi_khach = so(pheu.get("so_don_moi_khach_thang"), "so_don_moi_khach_thang", 1)
        chot = so(pheu.get("ti_le_chot"), "ti_le_chot")
        hoi = so(pheu.get("ti_le_tiep_can_thanh_hoi"), "ti_le_tiep_can_thanh_hoi")
        if not (0 < chot <= 1 and 0 < hoi <= 1):
            loi("Tỉ lệ trong 'tinh_nguoc' phải lớn hơn 0 và không quá 1 (vd 0.2 = 20%).")
        don = math.ceil(q_mt)
        khach = math.ceil(don / don_moi_khach)
        nguoi_hoi = math.ceil(khach / chot)
        tiep_can = math.ceil(nguoi_hoi / hoi)
        ra_pheu = ["## Tính ngược: muốn lời " + tien(muc_tieu) + "/tháng cần bao nhiêu khách, bao nhiêu lượt tiếp cận", "",
                   "| Bước | Cách tính | Mỗi tháng | Mỗi ngày (30 ngày) |", "|---|---|---:|---:|",
                   f"| Đơn cần bán | (Cố định + Mục tiêu) ÷ Lãi gộp/đơn | {nghin(don)} | {str(round(don / 30, 1)).replace('.', ',')} |",
                   f"| Khách cần có | Đơn ÷ {str(don_moi_khach).replace('.', ',')} đơn/khách | {nghin(khach)} | {str(round(khach / 30, 1)).replace('.', ',')} |",
                   f"| Người hỏi/nhắn tin | Khách ÷ tỉ lệ chốt {pt(chot)} | {nghin(nguoi_hoi)} | {str(round(nguoi_hoi / 30, 1)).replace('.', ',')} |",
                   f"| Lượt tiếp cận | Người hỏi ÷ tỉ lệ {pt(hoi)} | {nghin(tiep_can)} | {nghin(tiep_can / 30)} |",
                   ""]
        if pheu.get("chi_phi_moi_1000_tiep_can"):
            cpm = so(pheu["chi_phi_moi_1000_tiep_can"], "chi_phi_moi_1000_tiep_can")
            ra_pheu += [f"Nếu toàn bộ tiếp cận đến từ quảng cáo với chi phí {tien(cpm)}/1.000 lượt: "
                        f"ngân sách ≈ **{tien(tiep_can / 1000 * cpm)}/tháng** "
                        f"(≈ {tien(tiep_can / 1000 * cpm / don)}/đơn). Đối chiếu với khoản quảng cáo/đơn đã đưa vào chi phí biến đổi; "
                        "chênh nhiều thì sửa lại cho khớp rồi chạy lại.", ""]
        ra_pheu += ["**Giả định:** " + md(pheu.get("gia_dinh", "các tỉ lệ trên là giả định, cần đo lại sau 2–4 tuần bán thật.")), ""]

    # Xuất báo cáo
    ra = [f"# Kế hoạch lợi nhuận — {md(d.get('ten', 'doanh nghiệp'))}", ""]
    ra += ["## 1. Sản phẩm và lãi gộp mỗi đơn", "",
           "| Sản phẩm | Giá bán | Chi phí biến đổi/đơn (gồm phí %) | Lãi gộp/đơn | Tỉ lệ lãi gộp | Tỉ trọng đơn |",
           "|---|---:|---:|---:|---:|---:|"] + bang_sp
    ra += [f"| **Bình quân** | **{tien(P)}** | **{tien(V)}** | **{tien(lg_don)}** | **{pt(lg_don / P)}** | 100% |", ""]
    ra += ["## 2. Chi phí cố định mỗi tháng", ""]
    ra += [f"- {md(t)}: {tien(v)}" for t, v in ct_fc] or [f"- Tổng: {tien(fc)}"]
    ra += [f"- **Tổng: {tien(fc)}**", ""]
    ra += ["## 3. Điểm hòa vốn và mục tiêu", "",
           "| Chỉ số | Công thức | Kết quả |", "|---|---|---:|",
           f"| Điểm hòa vốn | {tien(fc)} ÷ {tien(lg_don)} | **{nghin(math.ceil(q_hv))} đơn/tháng** (≈ {tien(dt_hv)} doanh thu) |",
           f"| Mục tiêu lợi nhuận | — | {tien(muc_tieu)}/tháng |",
           f"| Đơn cần để đạt mục tiêu | ({tien(fc)} + {tien(muc_tieu)}) ÷ {tien(lg_don)} | **{nghin(math.ceil(q_mt))} đơn/tháng** "
           f"(≈ {nghin(math.ceil(q_mt / 30))} đơn/ngày, {tien(dt_mt)} doanh thu) |", ""]
    ra += ["## 4. Vốn ban đầu và hồi vốn", ""]
    ra += [f"- {md(t)}: {tien(v)}" for t, v in ct_von]
    ra += [f"- **Tổng vốn ban đầu: {tien(von)}**",
           f"- Thời gian hồi vốn (kịch bản cơ sở): **{doc_thang(hv_thang)}**", ""]
    ra += ["## 5. Dự toán 3 kịch bản (mỗi tháng)", "",
           "| Kịch bản | Số đơn | Doanh thu | Chi phí biến đổi | Lãi gộp | Chi phí cố định | Lợi nhuận | Biên lợi nhuận | Đơn hòa vốn | Vùng an toàn | Hồi vốn |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"] + hang_kb
    ra += ["", "Vùng an toàn = bán vượt điểm hòa vốn bao nhiêu % (càng cao càng an toàn; dưới 20% là sát mép).", ""]
    ra += ra_pheu
    ra += ["## Cảnh báo", ""] + (canh_bao or ["- Không có cảnh báo lớn."])
    van_ban = "\n".join(ra) + "\n"
    print(van_ban)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(van_ban)
        print(f"Đã lưu báo cáo: {a.out}", file=sys.stderr)
    if a.csv:
        with open(a.csv, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=a.csv_sep)
            w.writerow(["Kịch bản", "Số đơn/tháng", "Doanh thu (đ)", "Chi phí biến đổi (đ)", "Lãi gộp (đ)",
                        "Chi phí cố định (đ)", "Lợi nhuận (đ)", "Biên lợi nhuận", "Đơn hòa vốn",
                        "Vùng an toàn", "Tháng hồi vốn"])
            w.writerows(csv_rows)
        print(f"Đã xuất CSV: {a.csv}", file=sys.stderr)


if __name__ == "__main__":
    main()
