#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng Business Model Canvas 9 ô từ file JSON:
  - In bảng Markdown 9 ô + điểm từng ô + sơ đồ Mermaid.
  - Xuất file .canvas (chuẩn JSON Canvas, mở bằng Obsidian) theo bố cục 9 ô chuẩn.
Thuộc skill /ts-mo-hinh-kinh-doanh (Bộ skill TISA AI Agent).

CÁCH CHẠY (chỉ cần Python 3):
  macOS:    python3 tao_canvas.py vi-du-canvas.json --canvas mo-hinh.canvas --out mo-hinh.md
  Windows:  py tao_canvas.py vi-du-canvas.json --canvas mo-hinh.canvas --out mo-hinh.md

ĐỊNH DẠNG JSON: xem vi-du-canvas.json. Mỗi ô có:
  "noi_dung": ["ý 1", "ý 2", ...]   (bắt buộc, 1–6 ý ngắn)
  "diem": 1–10                       (độ rõ ràng & có bằng chứng; tùy chọn)
  "ghi_chu": "..."                   (tùy chọn)
"""

import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# (mã, tên tiếng Việt, thứ tự điền, màu JSON Canvas "1"–"6")
O = [
    ("khach_hang", "Phân khúc khách hàng", 1, "4"),
    ("gia_tri", "Giá trị mang lại", 2, "6"),
    ("kenh", "Kênh tiếp cận & phân phối", 3, "4"),
    ("quan_he", "Quan hệ khách hàng", 4, "4"),
    ("doanh_thu", "Dòng doanh thu", 5, "3"),
    ("nguon_luc", "Nguồn lực chính", 6, "5"),
    ("hoat_dong", "Hoạt động chính", 7, "5"),
    ("doi_tac", "Đối tác chính", 8, "5"),
    ("chi_phi", "Cơ cấu chi phí", 9, "1"),
]
TEN = {ma: ten for ma, ten, _, _ in O}

# Bố cục chuẩn: 5 cột trên + 2 khối dưới
C, G = 360, 20          # độ rộng cột, khoảng cách
H_TREN = 760            # chiều cao hàng trên
H_NUA = (H_TREN - G) // 2
H_DUOI = 300
X = [i * (C + G) for i in range(5)]
RONG_TONG = 5 * C + 4 * G
VI_TRI = {
    "doi_tac":   (X[0], 0, C, H_TREN),
    "hoat_dong": (X[1], 0, C, H_NUA),
    "nguon_luc": (X[1], H_NUA + G, C, H_NUA),
    "gia_tri":   (X[2], 0, C, H_TREN),
    "quan_he":   (X[3], 0, C, H_NUA),
    "kenh":      (X[3], H_NUA + G, C, H_NUA),
    "khach_hang": (X[4], 0, C, H_TREN),
    "chi_phi":   (0, H_TREN + G, (RONG_TONG - G) // 2, H_DUOI),
    "doanh_thu": ((RONG_TONG - G) // 2 + G, H_TREN + G, (RONG_TONG - G) // 2, H_DUOI),
}


def loi(tb):
    print("LỖI: " + tb, file=sys.stderr)
    sys.exit(1)


def md(x):
    return str(x if x is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def vn(x):
    """6.4 -> '6,4' (dấu thập phân kiểu Việt Nam)."""
    return f"{float(x):g}".replace(".", ",")


def mer(x):
    """Làm sạch chữ cho Mermaid (bỏ ngoặc kép, ngoặc vuông)."""
    return str(x).replace('"', "'").replace("[", "(").replace("]", ")").replace("\n", " ")


def doc(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        loi(f"Không tìm thấy file '{path}'.")
    except json.JSONDecodeError as e:
        loi(f"JSON sai cú pháp dòng {e.lineno}, cột {e.colno}: {e.msg}.")


def kiem_tra(d):
    o = d.get("o", {})
    thieu, canh_bao = [], []
    for ma, ten, _, _ in O:
        muc = o.get(ma)
        if not isinstance(muc, dict) or not [x for x in muc.get("noi_dung", []) if str(x).strip()]:
            thieu.append(ten)
            continue
        if "diem" in muc:
            try:
                diem = float(muc["diem"])
            except (TypeError, ValueError):
                loi(f"Ô '{ten}': 'diem' phải là số 1–10.")
            if not 1 <= diem <= 10:
                loi(f"Ô '{ten}': điểm {diem} nằm ngoài 1–10.")
            if diem < 5:
                canh_bao.append(f"- Ô **{ten}** chỉ {vn(diem)}/10 → cần làm rõ hoặc kiểm chứng trước.")
        if len(muc.get("noi_dung", [])) > 6:
            canh_bao.append(f"- Ô **{ten}** có hơn 6 ý → nên rút gọn, chọn ý quan trọng nhất.")
    return thieu, canh_bao


def bang_md(d):
    o = d["o"]
    dong = ["| # | Ô | Nội dung | Điểm /10 | Ghi chú |", "|---:|---|---|---:|---|"]
    tong, dem = 0.0, 0
    for ma, ten, thu_tu, _ in O:
        muc = o.get(ma, {})
        nd = "<br>".join("• " + md(x) for x in muc.get("noi_dung", [])) or "_[CẦN BỔ SUNG]_"
        diem = muc.get("diem")
        if diem is not None:
            tong += float(diem)
            dem += 1
        dong.append(f"| {thu_tu} | **{ten}** | {nd} | {'' if diem is None else vn(diem)} | {md(muc.get('ghi_chu', ''))} |")
    tb = round(tong / dem, 1) if dem else None
    return "\n".join(dong), tb


def so_do_mermaid(d):
    o = d["o"]

    def nut(ma):
        nd = o.get(ma, {}).get("noi_dung", [])[:3]
        return f'{ma}["<b>{mer(TEN[ma])}</b><br/>' + "<br/>".join("• " + mer(x) for x in nd) + '"]'

    return "\n".join([
        "```mermaid",
        "flowchart LR",
        "  subgraph HAU[\"Phía sau — vận hành\"]",
        "    direction TB",
        "    " + nut("doi_tac"),
        "    " + nut("hoat_dong"),
        "    " + nut("nguon_luc"),
        "  end",
        "  " + nut("gia_tri"),
        "  subgraph TRUOC[\"Phía trước — khách hàng\"]",
        "    direction TB",
        "    " + nut("quan_he"),
        "    " + nut("kenh"),
        "    " + nut("khach_hang"),
        "  end",
        "  " + nut("chi_phi"),
        "  " + nut("doanh_thu"),
        "  HAU --> gia_tri --> TRUOC",
        "  HAU -.-> chi_phi",
        "  TRUOC -.-> doanh_thu",
        "```",
    ])


def xuat_canvas(d, path):
    o = d["o"]
    nodes = [{
        "id": "tieu_de", "type": "text",
        "text": f"# {d.get('ten', 'Mô hình kinh doanh')}\n" + (f"_{d.get('mo_ta', '')}_" if d.get("mo_ta") else ""),
        "x": 0, "y": -170, "width": RONG_TONG, "height": 140,
    }]
    for ma, ten, thu_tu, mau in O:
        muc = o.get(ma, {})
        x, y, w, h = VI_TRI[ma]
        diem = muc.get("diem")
        dong = [f"## {thu_tu}. {ten}" + (f" — {vn(diem)}/10" if diem is not None else ""), ""]
        dong += ["- " + str(v) for v in muc.get("noi_dung", [])] or ["- [CẦN BỔ SUNG]"]
        if muc.get("ghi_chu"):
            dong += ["", "> " + str(muc["ghi_chu"])]
        nodes.append({"id": ma, "type": "text", "text": "\n".join(dong),
                      "x": x, "y": y, "width": w, "height": h, "color": mau})
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": []}, f, ensure_ascii=False, indent=2)


def main():
    p = argparse.ArgumentParser(description="Dựng Business Model Canvas 9 ô từ JSON.")
    p.add_argument("file_json")
    p.add_argument("--canvas", help="Xuất file .canvas cho Obsidian")
    p.add_argument("--out", help="Lưu bảng Markdown + Mermaid ra file .md")
    a = p.parse_args()

    d = doc(a.file_json)
    if not isinstance(d.get("o"), dict):
        loi("File cần có khóa 'o' chứa 9 ô. Xem vi-du-canvas.json.")
    thieu, canh_bao = kiem_tra(d)

    bang, tb = bang_md(d)
    ra = [f"# {md(d.get('ten', 'Mô hình kinh doanh'))}", ""]
    if d.get("mo_ta"):
        ra += [md(d["mo_ta"]), ""]
    ra += ["## Bản canvas 9 ô (theo thứ tự điền)", "", bang, ""]
    if tb is not None:
        muc = "Vững" if tb >= 7.5 else ("Khá, cần kiểm chứng vài ô" if tb >= 5.5 else "Còn mơ hồ, chưa nên bỏ vốn lớn")
        ra += [f"**Điểm trung bình 9 ô: {vn(tb)}/10 — {muc}.**", ""]
    ra += ["## Sơ đồ", "", so_do_mermaid(d), ""]
    ra += ["## Kiểm tra nhanh", ""]
    if thieu:
        ra += [f"- Ô còn trống: {', '.join(thieu)} → điền trước khi đánh giá."]
    ra += canh_bao
    if not thieu and not canh_bao:
        ra += ["- Đủ 9 ô, không ô nào dưới 5 điểm."]
    van_ban = "\n".join(ra) + "\n"
    print(van_ban)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(van_ban)
        print(f"Đã lưu: {a.out}", file=sys.stderr)
    if a.canvas:
        xuat_canvas(d, a.canvas)
        print(f"Đã xuất file canvas: {a.canvas} (mở bằng Obsidian)", file=sys.stderr)


if __name__ == "__main__":
    main()
