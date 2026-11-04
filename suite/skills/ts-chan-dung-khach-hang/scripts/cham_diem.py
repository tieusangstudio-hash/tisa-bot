#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chấm điểm và xếp hạng nỗi đau / mong muốn của khách hàng.
Thuộc skill /ts-chan-dung-khach-hang (Bộ skill TISA AI Agent).

CÁCH CHẠY (chỉ cần Python 3, không cài thêm gì):
  macOS:    python3 cham_diem.py vi-du-noi-dau.json
  Windows:  py cham_diem.py vi-du-noi-dau.json      (hoặc: python cham_diem.py ...)

TÙY CHỌN:
  --out bang-xep-hang.md   Lưu kết quả ra file Markdown (vẫn in ra màn hình).

CÔNG THỨC:
  Điểm = Mức đau × Mức phổ biến × Khả năng mình giải được ÷ 10   (thang 0,1 – 100)
  Với mong muốn: dùng 'muc_khao_khat' thay cho 'muc_dau'.
  >= 40  : Ưu tiên 1 (làm ngay)
  20–39  : Ưu tiên 2 (làm sau cụm ưu tiên 1)
  < 20   : Để sau

ĐỊNH DẠNG JSON: xem file vi-du-noi-dau.json cùng thư mục.
"""

import argparse
import json
import sys

try:  # Windows hay in lỗi font tiếng Việt, ép UTF-8 nếu được
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

NGUONG_UU_TIEN_1 = 40
NGUONG_UU_TIEN_2 = 20


def loi(thong_bao):
    print("LỖI: " + thong_bao, file=sys.stderr)
    sys.exit(1)


def md(text):
    """Làm sạch chữ để không vỡ bảng Markdown."""
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def lay_diem(muc, truong, vi_tri, nhom):
    gia_tri = muc.get(truong)
    if gia_tri is None:
        loi(f"{nhom} số {vi_tri} ('{muc.get('ten', '?')}') thiếu trường '{truong}'.")
    try:
        so = float(gia_tri)
    except (TypeError, ValueError):
        loi(f"{nhom} số {vi_tri}: '{truong}' phải là số từ 1 đến 10, đang là '{gia_tri}'.")
    if so < 1 or so > 10:
        loi(f"{nhom} số {vi_tri}: '{truong}' = {gia_tri} nằm ngoài thang 1–10.")
    return so


def muc_uu_tien(diem):
    if diem >= NGUONG_UU_TIEN_1:
        return "Ưu tiên 1"
    if diem >= NGUONG_UU_TIEN_2:
        return "Ưu tiên 2"
    return "Để sau"


def can_kiem_chung(muc):
    """Cần kiểm chứng nếu là phán đoán, hoặc chưa ghi bằng chứng."""
    if muc.get("phan_doan") is True:
        return True
    return not str(muc.get("bang_chung", "")).strip()


def cham_danh_sach(ds, truong_chinh, nhom):
    ket_qua = []
    for i, muc in enumerate(ds, start=1):
        if not isinstance(muc, dict) or not str(muc.get("ten", "")).strip():
            loi(f"{nhom} số {i} thiếu trường 'ten'.")
        truong = truong_chinh if truong_chinh in muc else "muc_dau"
        a = lay_diem(muc, truong, i, nhom)
        b = lay_diem(muc, "pho_bien", i, nhom)
        c = lay_diem(muc, "giai_duoc", i, nhom)
        diem = round(a * b * c / 10, 1)
        ket_qua.append({
            "ten": muc["ten"],
            "a": a, "b": b, "c": c,
            "diem": diem,
            "uu_tien": muc_uu_tien(diem),
            "bang_chung": muc.get("bang_chung", ""),
            "kiem_chung": can_kiem_chung(muc),
            "cum": str(muc.get("cum", "")).strip() or "(chưa gom cụm)",
            "nhom": nhom,
        })
    ket_qua.sort(key=lambda x: (-x["diem"], -x["a"]))
    return ket_qua


def so(x):
    return f"{x:g}".replace(".", ",")


def bang(ds, cot_a):
    dong = [
        f"| Hạng | Nội dung | {cot_a} | Phổ biến | Giải được | Điểm /100 | Mức | Bằng chứng | Cần kiểm chứng? |",
        "|---:|---|---:|---:|---:|---:|---|---|---|",
    ]
    for hang, m in enumerate(ds, start=1):
        dong.append(
            f"| {hang} | {md(m['ten'])} | {so(m['a'])} | {so(m['b'])} | {so(m['c'])} | "
            f"**{so(m['diem'])}** | {m['uu_tien']} | {md(m['bang_chung']) or '—'} | "
            f"{'CÓ' if m['kiem_chung'] else 'Không'} |"
        )
    return "\n".join(dong)


def gom_cum(tat_ca):
    cum = {}
    for m in tat_ca:
        c = cum.setdefault(m["cum"], {"so_muc": 0, "tong": 0.0, "cao_nhat": 0.0, "phan_doan": 0, "muc": []})
        c["so_muc"] += 1
        c["tong"] += m["diem"]
        c["cao_nhat"] = max(c["cao_nhat"], m["diem"])
        c["phan_doan"] += 1 if m["kiem_chung"] else 0
        c["muc"].append(m["ten"])
    return sorted(cum.items(), key=lambda kv: -kv[1]["tong"])


def canh_bao(tat_ca):
    ds = []
    for m in tat_ca:
        if m["kiem_chung"] and m["diem"] >= NGUONG_UU_TIEN_1:
            ds.append(f"- '{m['ten']}' điểm cao ({so(m['diem'])}) nhưng chưa có bằng chứng → "
                      "kiểm chứng (hỏi 5 khách / đọc bình luận) trước khi đổ tiền làm quảng cáo.")
        if m["a"] >= 8 and m["c"] <= 4:
            ds.append(f"- '{m['ten']}' rất đau ({so(m['a'])}/10) nhưng mình mới giải được {so(m['c'])}/10 → "
                      "cơ hội bổ sung vào sản phẩm, hoặc đừng hứa điều chưa làm được.")
    return ds


def main():
    p = argparse.ArgumentParser(description="Chấm điểm & xếp hạng nỗi đau khách hàng (thang 1–10).")
    p.add_argument("file_json", help="Đường dẫn file JSON (xem vi-du-noi-dau.json)")
    p.add_argument("--out", help="Lưu kết quả ra file Markdown")
    args = p.parse_args()

    try:
        with open(args.file_json, "r", encoding="utf-8-sig") as f:
            du_lieu = json.load(f)
    except FileNotFoundError:
        loi(f"Không tìm thấy file '{args.file_json}'. Kiểm tra lại tên/đường dẫn.")
    except json.JSONDecodeError as e:
        loi(f"File JSON sai cú pháp ở dòng {e.lineno}, cột {e.colno}: {e.msg}. "
            "Thường do thiếu dấu phẩy hoặc dấu ngoặc.")

    noi_dau = cham_danh_sach(du_lieu.get("noi_dau", []), "muc_dau", "Nỗi đau")
    mong_muon = cham_danh_sach(du_lieu.get("mong_muon", []), "muc_khao_khat", "Mong muốn")
    if not noi_dau and not mong_muon:
        loi("File chưa có 'noi_dau' hoặc 'mong_muon' nào để chấm.")

    ra = []
    ra.append(f"# Bảng xếp hạng nỗi đau & mong muốn — {md(du_lieu.get('chu_de', 'chưa đặt chủ đề'))}")
    ra.append("")
    ra.append("Công thức: **Điểm = Mức đau (hoặc khao khát) × Phổ biến × Giải được ÷ 10** (tối đa 100). "
              f"≥{NGUONG_UU_TIEN_1}: Ưu tiên 1 · {NGUONG_UU_TIEN_2}–{NGUONG_UU_TIEN_1 - 1}: Ưu tiên 2 · "
              f"<{NGUONG_UU_TIEN_2}: Để sau.")
    if noi_dau:
        ra += ["", "## Nỗi đau", "", bang(noi_dau, "Đau")]
    if mong_muon:
        ra += ["", "## Mong muốn", "", bang(mong_muon, "Khao khát")]

    tat_ca = noi_dau + mong_muon
    ra += ["", "## Gom theo cụm nội dung (xếp theo tổng điểm)", "",
           "| Hạng | Cụm | Số mục | Tổng điểm | Điểm cao nhất | Mục cần kiểm chứng |",
           "|---:|---|---:|---:|---:|---:|"]
    for hang, (ten, c) in enumerate(gom_cum(tat_ca), start=1):
        ra.append(f"| {hang} | {md(ten)} | {c['so_muc']} | {so(round(c['tong'], 1))} | "
                  f"{so(c['cao_nhat'])} | {c['phan_doan']}/{c['so_muc']} |")

    cb = canh_bao(tat_ca)
    ra += ["", "## Cảnh báo", ""]
    ra += cb if cb else ["- Không có cảnh báo đặc biệt."]
    tong_kc = sum(1 for m in tat_ca if m["kiem_chung"])
    ra += ["", f"Tổng cộng {len(tat_ca)} mục, trong đó {tong_kc} mục **cần kiểm chứng**."]

    van_ban = "\n".join(ra) + "\n"
    print(van_ban)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(van_ban)
        print(f"Đã lưu: {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
