#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
so_thanh_chu.py — Đổi số tiền thành chữ tiếng Việt để ghi vào hợp đồng, báo giá, biên bản.
Chỉ dùng thư viện có sẵn của Python 3 — không cần cài thêm.

CÁCH CHẠY
  macOS / Linux : python3 scripts/so_thanh_chu.py 15500000
  Windows       : py scripts\\so_thanh_chu.py 15500000

  Nhiều số một lần:  python3 scripts/so_thanh_chu.py 15.500.000 2,000,000 1005000
  Đổi đơn vị:        python3 scripts/so_thanh_chu.py 1200 --don-vi "đô la Mỹ"

KẾT QUẢ
  15.500.000 → Mười lăm triệu năm trăm nghìn đồng chẵn

GHI CHÚ CHO AI
  - Chỉ nhận số nguyên không âm (tiền Việt Nam không có phần lẻ). Dấu chấm/phẩy ngăn cách nghìn được bỏ qua.
  - Dùng "nghìn" (có thể đổi sang "ngàn" bằng --ngan) và "linh" (đổi sang "lẻ" bằng --le).
  - Luôn để người dùng đọc lại số bằng chữ trước khi đưa vào văn bản chính thức.
"""

import argparse
import re
import sys

CHU_SO = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def doc_ba_so(n, day_du, linh="linh"):
    """Đọc một nhóm 3 chữ số (0–999). day_du=True khi không phải nhóm đầu tiên (phải đọc 'không trăm')."""
    tram, chuc, dv = n // 100, (n // 10) % 10, n % 10
    phan = []
    if tram > 0 or day_du:
        phan.append(CHU_SO[tram] + " trăm")
    if chuc == 0:
        if dv > 0 and (tram > 0 or day_du):
            phan.append(linh)
    elif chuc == 1:
        phan.append("mười")
    else:
        phan.append(CHU_SO[chuc] + " mươi")
    if dv > 0:
        if dv == 1 and chuc >= 2:
            phan.append("mốt")
        elif dv == 5 and chuc >= 1:
            phan.append("lăm")
        elif dv == 4 and chuc >= 2:
            phan.append("tư")
        else:
            phan.append(CHU_SO[dv])
    return " ".join(phan)


def doc_duoi_ty(n, day_du, nghin, linh):
    """Đọc số 1–999.999.999. day_du=True khi phía trước đã có phần 'tỷ'."""
    nhom = [(n // 1_000_000, "triệu"), ((n // 1000) % 1000, nghin), (n % 1000, "")]
    ket_qua = []
    for gia_tri, ten in nhom:
        if gia_tri == 0:
            continue
        chu = doc_ba_so(gia_tri, day_du or bool(ket_qua), linh)
        ket_qua.append((chu + " " + ten).strip())
    return " ".join(ket_qua)


def so_thanh_chu(so, nghin="nghìn", linh="linh", day_du=False):
    """Đổi số nguyên không âm thành chữ. Phần từ 1 tỷ trở lên được đọc đệ quy (vd 'một nghìn năm trăm tỷ')."""
    if so == 0:
        return "không"
    if so >= 1_000_000_000:
        ty, du = divmod(so, 1_000_000_000)
        chu = so_thanh_chu(ty, nghin, linh, day_du) + " tỷ"
        if du:
            chu += " " + doc_duoi_ty(du, True, nghin, linh)
        return chu
    return doc_duoi_ty(so, day_du, nghin, linh)


def chuan_hoa_dau_vao(s):
    s = s.strip()
    if not re.fullmatch(r"[0-9.,\s_]+", s):
        raise ValueError(f"'{s}' không phải số tiền hợp lệ (chỉ gồm chữ số và dấu ngăn cách nghìn).")
    return int(re.sub(r"[.,\s_]", "", s))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Đổi số tiền thành chữ tiếng Việt.")
    ap.add_argument("so", nargs="+")
    ap.add_argument("--don-vi", default="đồng")
    ap.add_argument("--ngan", action="store_true", help="dùng 'ngàn' thay cho 'nghìn'")
    ap.add_argument("--le", action="store_true", help="dùng 'lẻ' thay cho 'linh'")
    ap.add_argument("--khong-chan", action="store_true", help="không thêm chữ 'chẵn' ở cuối")
    a = ap.parse_args()

    loi = False
    for s in a.so:
        try:
            n = chuan_hoa_dau_vao(s)
        except ValueError as e:
            print(e)
            loi = True
            continue
        chu = so_thanh_chu(n, "ngàn" if a.ngan else "nghìn", "lẻ" if a.le else "linh")
        chu = chu[0].upper() + chu[1:] + " " + a.don_vi + ("" if a.khong_chan else " chẵn")
        so_dep = f"{n:,}".replace(",", ".")
        print(f"{so_dep} → {chu}")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
