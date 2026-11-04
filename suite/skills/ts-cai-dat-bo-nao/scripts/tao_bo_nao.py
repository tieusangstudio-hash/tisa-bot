#!/usr/bin/env python3
"""Tạo (hoặc bổ sung) cấu trúc Bộ Não Thứ 2 từ mẫu đi kèm skill.

Cách dùng:
  macOS / Linux:  python3 tao_bo_nao.py "/Users/ban/Documents/Bộ Não Thứ 2 - Lan" --ten "Lan"
  Windows:        py tao_bo_nao.py "D:\\Bộ Não Thứ 2 - Lan" --ten "Lan"
  Chỉ tạo file zip để tải về (khi AI không ghi được vào máy):
                  python3 tao_bo_nao.py --zip "Bo-Nao-Thu-2-Lan.zip" --ten "Lan"

Nguyên tắc: KHÔNG BAO GIỜ ghi đè tệp đã có. Chỉ thêm thư mục/tệp còn thiếu.
Chỉ dùng thư viện chuẩn của Python 3.8+.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import sys
import zipfile
from pathlib import Path

MAU = Path(__file__).resolve().parent.parent / "assets" / "bo-nao-mau"
DUOI_VAN_BAN = {".md", ".json", ".txt", ".yaml", ".yml"}


def thay_bien(noi_dung: str, ten: str, ngay: str) -> str:
    return noi_dung.replace("{{TEN}}", ten).replace("{{NGAY}}", ngay)


def tao(dich: Path, ten: str, ngay: str) -> tuple[list[str], list[str]]:
    da_tao, da_co = [], []
    dich.mkdir(parents=True, exist_ok=True)
    for goc in sorted(MAU.rglob("*")):
        tuong_doi = goc.relative_to(MAU)
        moi = dich / tuong_doi
        if goc.is_dir():
            moi.mkdir(parents=True, exist_ok=True)
            continue
        if moi.exists():
            da_co.append(str(tuong_doi))
            continue
        moi.parent.mkdir(parents=True, exist_ok=True)
        if goc.suffix.lower() in DUOI_VAN_BAN:
            moi.write_text(thay_bien(goc.read_text(encoding="utf-8"), ten, ngay), encoding="utf-8")
        else:
            shutil.copy2(goc, moi)
        da_tao.append(str(tuong_doi))
    return da_tao, da_co


def tao_zip(duong_zip: Path, ten: str, ngay: str) -> None:
    goc_trong_zip = f"Bộ Não Thứ 2 - {ten}"
    with zipfile.ZipFile(duong_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for goc in sorted(MAU.rglob("*")):
            if goc.is_dir():
                continue
            ten_trong_zip = f"{goc_trong_zip}/{goc.relative_to(MAU).as_posix()}"
            if goc.suffix.lower() in DUOI_VAN_BAN:
                z.writestr(ten_trong_zip, thay_bien(goc.read_text(encoding="utf-8"), ten, ngay))
            else:
                z.write(goc, ten_trong_zip)


def main() -> int:
    p = argparse.ArgumentParser(description="Tạo cấu trúc Bộ Não Thứ 2")
    p.add_argument("thu_muc", nargs="?", help="Đường dẫn thư mục Bộ Não (đã tạo hoặc sẽ tạo)")
    p.add_argument("--ten", required=True, help="Tên chủ Bộ Não, vd: Lan")
    p.add_argument("--zip", help="Chỉ xuất file zip mẫu thay vì ghi vào thư mục")
    a = p.parse_args()

    if not MAU.exists():
        print(f"Không tìm thấy mẫu tại {MAU}", file=sys.stderr)
        return 1
    ngay = dt.date.today().isoformat()

    if a.zip:
        tao_zip(Path(a.zip), a.ten, ngay)
        print(f"Đã tạo file zip: {Path(a.zip).resolve()}")
        print("Giải nén ra ổ còn trống dung lượng, rồi kết nối thư mục đó với AI.")
        return 0

    if not a.thu_muc:
        p.error("Cần đường dẫn thư mục hoặc --zip")
    dich = Path(os.path.expanduser(a.thu_muc))
    da_tao, da_co = tao(dich, a.ten, ngay)
    print(f"Bộ Não: {dich.resolve()}")
    print(f"- Đã tạo mới: {len(da_tao)} tệp")
    print(f"- Đã có sẵn (giữ nguyên, không ghi đè): {len(da_co)} tệp")
    for t in da_tao[:60]:
        print(f"  + {t}")
    print("Xong. Mở thư mục này bằng Obsidian: Open folder as vault.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
