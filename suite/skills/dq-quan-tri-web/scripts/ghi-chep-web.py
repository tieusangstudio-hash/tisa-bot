#!/usr/bin/env python3
"""Ghi hồ sơ một web vào bộ não để trang "Quản lý web" của TISA BOT tự nhận (nút "Tìm web đã tạo" quét 04-ket-qua).
Dùng: python3 ghi-chep-web.py --bo-nao <thư mục bộ não> --ten "Tên web" --link https://... [--ten-mien https://...] [--thu-muc-ma <đường dẫn mã nguồn>] [--ten-web "Tên hiện trên thẻ"] [--nen-tang Cloudflare] [--ghi-chu "..."]
--thu-muc-ma QUAN TRỌNG với web mẫu (Web CRM, Lead Page & Sale Page): TISA BOT dựa vào đường dẫn này để biết hồ sơ thuộc thẻ nào ở trang Quản lý web, rồi tự cập nhật tên miền, tên web, SEO trên thẻ đó.
Ghi lại mỗi lần đổi tên miền hay tên web (ghi hồ sơ mới, TISA BOT lấy hồ sơ mới nhất).
Ghi vào: <bộ não>/04-ket-qua/web/<ngày>-<tên>/ghi-chep.md . Không ghi khóa hay mật khẩu."""
import argparse
import datetime
import re
import sys
import unicodedata
from pathlib import Path


def khong_dau(s):
    s = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:50] or "web"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bo-nao", required=True)
    ap.add_argument("--ten", required=True)
    ap.add_argument("--link", required=True)
    ap.add_argument("--ten-mien", default="")
    ap.add_argument("--thu-muc-ma", default="")
    ap.add_argument("--nen-tang", default="Cloudflare")
    ap.add_argument("--ten-web", default="")
    ap.add_argument("--ghi-chu", default="")
    a = ap.parse_args()
    for v in (a.link, a.ten_mien):
        if v and not re.match(r"^https?://\S+$", v):
            sys.exit("LỖI: địa chỉ phải bắt đầu bằng http:// hoặc https:// : %s" % v)
    if re.search(r"(?i)(token|secret|password|mat[ _-]?khau|cfut_)", a.ghi_chu + a.thu_muc_ma):
        sys.exit("LỖI: ghi chú có vẻ chứa khóa hoặc mật khẩu. Không ghi bí mật vào bộ não.")
    ngay = datetime.date.today().isoformat()
    goc = Path(a.bo_nao).expanduser()
    if not goc.is_dir():
        sys.exit("LỖI: không thấy thư mục bộ não: %s" % goc)
    d = goc / "04-ket-qua" / "web" / ("%s-%s" % (ngay, khong_dau(a.ten)))
    d.mkdir(parents=True, exist_ok=True)
    f = d / "ghi-chep.md"
    nd = ["---", "loai: web", "title: %s" % a.ten.replace("\n", " "), "ten-web: %s" % (a.ten_web or a.ten).replace("\n", " "), "link: %s" % a.link]
    if a.ten_mien:
        nd.append("ten-mien: %s" % a.ten_mien)
    if a.thu_muc_ma:
        nd.append("thu-muc-ma: %s" % a.thu_muc_ma.replace("\n", " "))
    nd += ["nen-tang: %s" % a.nen_tang, "ngay: %s" % ngay, "---", "", "# %s" % a.ten, "",
           "- Địa chỉ: %s" % a.link]
    if a.ten_mien:
        nd.append("- Tên miền riêng: %s" % a.ten_mien)
    if a.thu_muc_ma:
        nd.append("- Mã nguồn: %s" % a.thu_muc_ma)
    nd.append("- Nền tảng: %s" % a.nen_tang)
    if a.ghi_chu:
        nd += ["", a.ghi_chu]
    nd.append("")
    f.write_text("\n".join(nd), encoding="utf-8")
    print("Đã ghi %s" % f)


if __name__ == "__main__":
    main()
