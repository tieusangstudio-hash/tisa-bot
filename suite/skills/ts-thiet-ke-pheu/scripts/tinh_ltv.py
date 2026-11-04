#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính giá trị phễu 4 tầng trên N người để lại thông tin (mặc định 100 lead).

Không cần cài thêm thư viện (chỉ dùng Python 3 chuẩn).

CÁCH CHẠY
  macOS / Linux:
    python3 scripts/tinh_ltv.py --mau > pheu.json        # tạo file mẫu để sửa
    python3 scripts/tinh_ltv.py pheu.json                # tính và in bảng Markdown
    python3 scripts/tinh_ltv.py pheu.json --md ket-qua.md --csv bang-ltv.csv
    python3 scripts/tinh_ltv.py pheu.json --ba-kich-ban    # thêm bảng thận trọng/kỳ vọng/tốt
    python3 scripts/tinh_ltv.py --nhanh "Ebook|0|100" "Lớp mini|99000|10" \
        "Khóa chính|1990000|20" "Kèm 1-1|12000000|10" --lead 100 --bien 60

  Windows (Command Prompt / PowerShell): thay `python3` bằng `py`
    py scripts\\tinh_ltv.py pheu.json

GIẢI THÍCH NHANH
  - Mỗi tầng có: tên, giá (đồng), tỉ lệ chuyển đổi (%), tính trên đâu:
      'tang-truoc' = % số người đã mua tầng ngay trước (mặc định)
      'lead'       = % trên tổng số lead
  - Tầng 1 là quà miễn phí: giá 0, tỉ lệ 100% trên lead.
  - 'so_lan_mua' = số lần mua trung bình của 1 khách ở tầng đó (vd gói tháng mua 3 lần = 3).
  - Số người mua có thể lẻ (vd 0,4 người) vì đây là giá trị KỲ VỌNG trên 100 lead.
  - Mọi tỉ lệ là GIẢ ĐỊNH để lập kế hoạch, phải đo lại bằng số thật sau 2–4 tuần.
"""

import argparse
import csv
import json
import sys

MAU = {
    "ghi_chu": "VÍ DỤ GIẢ ĐỊNH — tiệm bánh Mây. Sửa tên, giá, tỉ lệ theo doanh nghiệp của bạn.",
    "so_lead": 100,
    "bien_loi_nhuan_gop": 60,
    "he_so_an_toan_cpl": 50,
    "muc_tieu_doanh_thu_thang": 50000000,
    "tang": [
        {"ten": "Ebook 7 công thức bánh không cần lò", "loai": "Quà miễn phí",
         "gia": 0, "ty_le": 100, "tinh_tren": "lead", "so_lan_mua": 1},
        {"ten": "Lớp video bông lan cơ bản", "loai": "Sản phẩm mồi",
         "gia": 99000, "ty_le": 10, "tinh_tren": "lead", "so_lan_mua": 1},
        {"ten": "Khóa làm bánh bán online", "loai": "Sản phẩm chính",
         "gia": 1990000, "ty_le": 20, "tinh_tren": "tang-truoc", "so_lan_mua": 1},
        {"ten": "Kèm 1-1 mở tiệm bánh tại nhà", "loai": "Sản phẩm cao cấp",
         "gia": 12000000, "ty_le": 10, "tinh_tren": "tang-truoc", "so_lan_mua": 1},
    ],
}

LOAI_MAC_DINH = ["Quà miễn phí", "Sản phẩm mồi", "Sản phẩm chính", "Sản phẩm cao cấp"]

# Ngưỡng cảnh báo "lạc quan quá" cho tỉ lệ tính trên tầng trước (giả định thận trọng, không phải số liệu ngành)
NGUONG_LAC_QUAN = {2: 25.0, 3: 40.0, 4: 30.0}


def dinh_dang_tien(so):
    """1990000 -> '1.990.000đ' (làm tròn đến đồng)."""
    so = int(round(so))
    am = so < 0
    chuoi = f"{abs(so):,}".replace(",", ".")
    return ("-" if am else "") + chuoi + "đ"


def dinh_dang_so(so, le=1):
    if abs(so - round(so)) < 1e-9:
        return str(int(round(so)))
    return f"{so:.{le}f}".replace(".", ",")


def doc_nhanh(danh_sach):
    tang = []
    for i, muc in enumerate(danh_sach):
        phan = [p.strip() for p in muc.split("|")]
        if len(phan) < 3:
            sys.exit(f"Lỗi: '{muc}' cần dạng 'Tên|giá|tỉ lệ%' (vd 'Khóa chính|1990000|20').")
        tinh_tren = phan[3] if len(phan) > 3 and phan[3] else ("lead" if i <= 1 else "tang-truoc")
        tang.append({
            "ten": phan[0],
            "loai": LOAI_MAC_DINH[i] if i < 4 else f"Tầng {i + 1}",
            "gia": float(phan[1].replace(".", "").replace(",", "")),
            "ty_le": float(phan[2].replace("%", "").replace(",", ".")),
            "tinh_tren": tinh_tren,
            "so_lan_mua": 1,
        })
    return tang


def tinh(du_lieu):
    so_lead = float(du_lieu.get("so_lead", 100))
    bien = du_lieu.get("bien_loi_nhuan_gop")
    an_toan = float(du_lieu.get("he_so_an_toan_cpl", 50))
    muc_tieu = du_lieu.get("muc_tieu_doanh_thu_thang")
    tang = du_lieu.get("tang", [])
    if not tang:
        sys.exit("Lỗi: chưa có tầng nào trong phễu.")

    canh_bao = []
    dong = []
    so_mua_truoc = so_lead
    tong_dt = 0.0
    khach_tra_tien = 0.0
    tang_tra_phi_dau = None

    for i, t in enumerate(tang, start=1):
        gia = float(t.get("gia", 0))
        ty_le = float(t.get("ty_le", 0))
        tinh_tren = t.get("tinh_tren", "lead" if i == 1 else "tang-truoc")
        lan_mua = float(t.get("so_lan_mua", 1) or 1)
        goc = so_lead if tinh_tren == "lead" else so_mua_truoc
        so_mua = goc * ty_le / 100.0
        dt = so_mua * gia * lan_mua
        tong_dt += dt
        if gia > 0:
            if tang_tra_phi_dau is None:
                tang_tra_phi_dau = i
                khach_tra_tien += so_mua
            elif tinh_tren == "lead":
                khach_tra_tien += so_mua  # giả định không trùng với tầng trước
        dong.append({
            "stt": i, "ten": t.get("ten", f"Tầng {i}"), "loai": t.get("loai", ""),
            "gia": gia, "ty_le": ty_le,
            "tinh_tren": "tổng lead" if tinh_tren == "lead" else "người mua tầng trước",
            "so_mua": so_mua, "lan_mua": lan_mua, "doanh_thu": dt,
        })

        # Kiểm tra logic
        if ty_le > 100 or ty_le < 0:
            canh_bao.append(f"Tầng {i}: tỉ lệ {dinh_dang_so(ty_le)}% không hợp lệ (phải từ 0 đến 100).")
        if i == 1 and gia > 0:
            canh_bao.append("Tầng 1 nên là quà MIỄN PHÍ (giá 0) để đổi lấy thông tin liên hệ.")
        if i > 1 and gia <= float(tang[i - 2].get("gia", 0)):
            canh_bao.append(f"Tầng {i} có giá không cao hơn tầng {i - 1} — bậc thang giá nên tăng dần.")
        if i > 2:
            gia_truoc = float(tang[i - 2].get("gia", 0))
            if gia_truoc > 0 and gia / gia_truoc > 30:
                canh_bao.append(f"Tầng {i} đắt gấp {dinh_dang_so(gia / gia_truoc)} lần tầng {i - 1} — "
                                "bước nhảy lớn, cân nhắc thêm 1 gói ở giữa hoặc chia trả góp.")
        nguong = NGUONG_LAC_QUAN.get(i)
        if nguong and tinh_tren != "lead" and ty_le > nguong:
            canh_bao.append(f"Tầng {i}: tỉ lệ {dinh_dang_so(ty_le)}% khá lạc quan cho kế hoạch đầu tiên — "
                            "nên lập thêm kịch bản thận trọng.")
        if i == 2 and tinh_tren == "lead" and ty_le > 20:
            canh_bao.append(f"Tầng 2: {dinh_dang_so(ty_le)}% lead mua ngay là lạc quan — nên thử với 5–10%.")
        so_mua_truoc = so_mua

    dt_moi_lead = tong_dt / so_lead if so_lead else 0
    ltv = tong_dt / khach_tra_tien if khach_tra_tien else 0
    ket = {
        "so_lead": so_lead, "dong": dong, "tong_dt": tong_dt,
        "dt_moi_lead": dt_moi_lead, "khach_tra_tien": khach_tra_tien, "ltv": ltv,
        "canh_bao": canh_bao, "bien": bien, "an_toan": an_toan, "muc_tieu": muc_tieu,
    }
    if bien is not None:
        lg_moi_lead = dt_moi_lead * float(bien) / 100.0
        ket["lg_moi_lead"] = lg_moi_lead
        ket["cpl_tran"] = lg_moi_lead * an_toan / 100.0
    if muc_tieu:
        ket["lead_can"] = float(muc_tieu) / dt_moi_lead if dt_moi_lead else 0
    return ket


def xuat_markdown(k):
    n = dinh_dang_so(k["so_lead"])
    out = []
    out.append(f"## Bảng giá trị phễu trên {n} người để lại thông tin\n")
    out.append("| Tầng | Loại | Tên | Giá | Tỉ lệ | Tính trên | Số người mua | Số lần mua | Doanh thu |")
    out.append("|---|---|---|---:|---:|---|---:|---:|---:|")
    for d in k["dong"]:
        out.append(f"| {d['stt']} | {d['loai']} | {d['ten']} | {dinh_dang_tien(d['gia'])} | "
                   f"{dinh_dang_so(d['ty_le'])}% | {d['tinh_tren']} | {dinh_dang_so(d['so_mua'], 2)} | "
                   f"{dinh_dang_so(d['lan_mua'])} | {dinh_dang_tien(d['doanh_thu'])} |")
    out.append(f"| | | **Tổng** | | | | | | **{dinh_dang_tien(k['tong_dt'])}** |")
    out.append("")
    out.append("## Chỉ số chính\n")
    out.append("| Chỉ số | Giá trị | Cách tính |")
    out.append("|---|---:|---|")
    out.append(f"| Tổng doanh thu kỳ vọng | {dinh_dang_tien(k['tong_dt'])} | cộng cột Doanh thu |")
    out.append(f"| Doanh thu trung bình mỗi lead | {dinh_dang_tien(k['dt_moi_lead'])} | tổng doanh thu ÷ {n} lead |")
    out.append(f"| Số khách trả tiền (ước tính) | {dinh_dang_so(k['khach_tra_tien'], 2)} | người mua tầng trả phí đầu tiên"
               " (+ tầng tính trên lead) |")
    out.append(f"| LTV — giá trị vòng đời 1 khách trả tiền | {dinh_dang_tien(k['ltv'])} | tổng doanh thu ÷ số khách trả tiền |")
    if "lg_moi_lead" in k:
        out.append(f"| Lợi nhuận gộp mỗi lead (biên {dinh_dang_so(float(k['bien']))}%) | "
                   f"{dinh_dang_tien(k['lg_moi_lead'])} | doanh thu mỗi lead × biên lợi nhuận gộp |")
        out.append(f"| Chi phí tối đa nên trả cho 1 lead | {dinh_dang_tien(k['cpl_tran'])} | lợi nhuận gộp mỗi lead × "
                   f"{dinh_dang_so(k['an_toan'])}% (hệ số an toàn) |")
    if k.get("muc_tieu"):
        out.append(f"| Số lead cần mỗi tháng để đạt {dinh_dang_tien(float(k['muc_tieu']))} | "
                   f"{dinh_dang_so(k.get('lead_can', 0), 0)} lead | mục tiêu ÷ doanh thu mỗi lead |")
    out.append("")
    out.append("## Kiểm tra logic tự động\n")
    if k["canh_bao"]:
        for c in k["canh_bao"]:
            out.append(f"- [CẦN XEM LẠI] {c}")
    else:
        out.append("- [ĐẠT] Giá tăng dần, tầng 1 miễn phí, tỉ lệ nằm trong vùng thận trọng.")
    out.append("")
    out.append("_Lưu ý: tỉ lệ chuyển đổi là giả định để lập kế hoạch. Đo lại bằng số thật sau 2–4 tuần "
               "và chạy lại bảng này._")
    return "\n".join(out)


def ba_kich_ban(du_lieu):
    """So sánh 3 kịch bản: tỉ lệ (trừ tầng 1) nhân 0,5 / 1 / 1,5 (tối đa 100%)."""
    import copy
    out = ["## So sánh 3 kịch bản\n",
           "| Kịch bản | Hệ số tỉ lệ | Doanh thu / 100 lead | Doanh thu mỗi lead | LTV 1 khách trả tiền |",
           "|---|---:|---:|---:|---:|"]
    for ten, he_so in (("Thận trọng", 0.5), ("Kỳ vọng", 1.0), ("Tốt", 1.5)):
        d = copy.deepcopy(du_lieu)
        for i, t in enumerate(d["tang"]):
            if i > 0:
                t["ty_le"] = min(100.0, float(t.get("ty_le", 0)) * he_so)
        k = tinh(d)
        quy_doi = 100.0 / k["so_lead"] if k["so_lead"] else 0
        out.append(f"| {ten} | ×{dinh_dang_so(he_so)} | {dinh_dang_tien(k['tong_dt'] * quy_doi)} | "
                   f"{dinh_dang_tien(k['dt_moi_lead'])} | {dinh_dang_tien(k['ltv'])} |")
    out.append("")
    out.append("_Lập kế hoạch ngân sách theo kịch bản Thận trọng; kịch bản Tốt chỉ để tham khảo._")
    return "\n".join(out)


def xuat_csv(k, duong_dan):
    with open(duong_dan, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Tầng", "Loại", "Tên", "Giá (đ)", "Tỉ lệ (%)", "Tính trên",
                    "Số người mua", "Số lần mua", "Doanh thu (đ)"])
        for d in k["dong"]:
            w.writerow([d["stt"], d["loai"], d["ten"], int(round(d["gia"])), d["ty_le"], d["tinh_tren"],
                        round(d["so_mua"], 2), d["lan_mua"], int(round(d["doanh_thu"]))])
        w.writerow([])
        w.writerow(["Tổng doanh thu", int(round(k["tong_dt"]))])
        w.writerow(["Doanh thu mỗi lead", int(round(k["dt_moi_lead"]))])
        w.writerow(["LTV 1 khách trả tiền", int(round(k["ltv"]))])
        if "cpl_tran" in k:
            w.writerow(["Chi phí tối đa cho 1 lead", int(round(k["cpl_tran"]))])
        if k.get("muc_tieu"):
            w.writerow(["Số lead cần mỗi tháng", int(round(k.get("lead_can", 0)))])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Tính giá trị phễu 4 tầng và LTV trên N lead.")
    p.add_argument("file_json", nargs="?", help="File JSON mô tả phễu (tạo mẫu bằng --mau).")
    p.add_argument("--mau", action="store_true", help="In file JSON mẫu rồi thoát.")
    p.add_argument("--nhanh", nargs="+", metavar="'Tên|giá|tỉ lệ'", help="Nhập nhanh các tầng.")
    p.add_argument("--lead", type=float, help="Số lead (mặc định 100).")
    p.add_argument("--bien", type=float, help="Biên lợi nhuận gộp %% (vd 60).")
    p.add_argument("--an-toan", type=float, help="Hệ số an toàn chi phí lead %% (mặc định 50).")
    p.add_argument("--muc-tieu", type=float, help="Mục tiêu doanh thu/tháng (đồng).")
    p.add_argument("--md", help="Ghi kết quả ra file Markdown.")
    p.add_argument("--csv", help="Ghi bảng ra file CSV (mở được bằng Excel/Google Sheets).")
    p.add_argument("--ba-kich-ban", action="store_true",
                   help="Thêm bảng so sánh 3 kịch bản thận trọng / kỳ vọng / tốt.")
    a = p.parse_args()

    if a.mau:
        print(json.dumps(MAU, ensure_ascii=False, indent=2))
        return
    if a.file_json:
        with open(a.file_json, encoding="utf-8") as f:
            du_lieu = json.load(f)
    elif a.nhanh:
        du_lieu = {"tang": doc_nhanh(a.nhanh)}
    else:
        p.print_help()
        sys.exit(1)

    if a.lead is not None:
        du_lieu["so_lead"] = a.lead
    if a.bien is not None:
        du_lieu["bien_loi_nhuan_gop"] = a.bien
    if a.an_toan is not None:
        du_lieu["he_so_an_toan_cpl"] = a.an_toan
    if a.muc_tieu is not None:
        du_lieu["muc_tieu_doanh_thu_thang"] = a.muc_tieu

    k = tinh(du_lieu)
    md = xuat_markdown(k)
    if a.ba_kich_ban:
        md += "\n\n" + ba_kich_ban(du_lieu)
    print(md)
    if a.md:
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(md + "\n")
        print(f"\nĐã ghi: {a.md}")
    if a.csv:
        xuat_csv(k, a.csv)
        print(f"Đã ghi: {a.csv}")


if __name__ == "__main__":
    main()
