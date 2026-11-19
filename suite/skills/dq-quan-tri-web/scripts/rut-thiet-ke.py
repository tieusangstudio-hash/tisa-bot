#!/usr/bin/env python3
"""Rút "bản thiết kế" từ một web mẫu để làm theo (học cấu trúc và phong cách, KHÔNG chép nội dung, ảnh, logo, mã nguồn):
màu hay dùng, font, cỡ chữ, biến CSS, khối (section) theo thứ tự, tiêu đề, chữ trên nút, thẻ SEO.
Dùng: python3 rut-thiet-ke.py https://web-mau.com   hoặc   python3 rut-thiet-ke.py duong-dan/tep.html
Chỉ đọc. Chỉ phân tích HTML và CSS tĩnh (không chạy JavaScript): trang dựng bằng JS thì kết quả thiếu, khi đó dùng trình duyệt chụp ảnh và đọc style thật.
Chỉ dùng thư viện chuẩn của Python."""
import collections
import ipaddress
import re
import socket
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; TISA-Quan-Tri-Web/1.0)"


def an_toan(url):
    h = urlparse(url).hostname
    if not h:
        raise ValueError("Địa chỉ không hợp lệ")
    for i in socket.getaddrinfo(h, None):
        ip = ipaddress.ip_address(i[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise ValueError("Địa chỉ nội bộ, không phân tích")


def tai(url, gioi_han=1_500_000):
    if urlparse(url).scheme not in ("http", "https"):
        raise ValueError("Chỉ nhận http/https")
    an_toan(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(gioi_han).decode(r.headers.get_content_charset() or "utf-8", "replace")


def chuan_hex(m):
    m = m.lower()
    if len(m) == 4:
        m = "#" + "".join(c * 2 for c in m[1:])
    return m[:7]


def rgb_hex(r, g, b):
    return "#%02x%02x%02x" % (min(255, int(r)), min(255, int(g)), min(255, int(b)))


def main(nguon):
    la_url = bool(re.match(r"^https?://", nguon))
    html = tai(nguon) if la_url else Path(nguon).read_text(encoding="utf-8", errors="replace")
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.I | re.S))
    lien_ket = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.I)
    for l in lien_ket[:6]:
        m = re.search(r'href=["\']([^"\']+)', l)
        if not m:
            continue
        try:
            if la_url:
                css += "\n" + tai(urljoin(nguon, m.group(1)), 800_000)
            elif not re.match(r"^(https?:)?//", m.group(1)):
                css += "\n" + (Path(nguon).parent / m.group(1).split("?")[0]).read_text(encoding="utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            print("  (không tải được CSS %s: %s)" % (m.group(1)[:60], type(e).__name__))
    so_mau = collections.Counter()
    for m in re.findall(r"#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b", css + html):
        so_mau[chuan_hex(m)] += 1
    for r, g, b in re.findall(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", css + html):
        so_mau[rgb_hex(r, g, b)] += 1
    print("== MÀU hay dùng (đếm số lần xuất hiện) ==")
    for m, n in so_mau.most_common(12):
        print("  %s  x%d" % (m, n))
    fonts = collections.Counter(f.strip().strip("'\"") for blk in re.findall(r"font-family\s*:\s*([^;}{]+)", css + html, re.I) for f in blk.split(",")[:2])
    print("\n== FONT ==")
    for f, n in fonts.most_common(6):
        print("  %s  x%d" % (f, n))
    for g in re.findall(r"fonts\.googleapis\.com/css2?\?[^\"'\s>]+", html + css)[:3]:
        print("  Google Fonts: " + g[:140])
    sizes = collections.Counter(re.findall(r"font-size\s*:\s*([\d.]+(?:px|rem|em|vw|clamp\([^)]*\)))", css, re.I))
    print("\n== CỠ CHỮ hay dùng ==")
    print("  " + ", ".join("%s (x%d)" % (s, n) for s, n in sizes.most_common(8)))
    bien = re.findall(r"(--[a-zA-Z0-9-]+)\s*:\s*([^;}{]+)", css)
    if bien:
        print("\n== BIẾN CSS (design tokens, tối đa 25) ==")
        for k, v in bien[:25]:
            print("  %s: %s" % (k, v.strip()[:60]))
    rad = collections.Counter(re.findall(r"border-radius\s*:\s*([^;}{]+)", css, re.I))
    if rad:
        print("\n== BO GÓC ==\n  " + ", ".join("%s (x%d)" % (s.strip(), n) for s, n in rad.most_common(5)))
    print("\n== CẤU TRÚC KHỐI (theo thứ tự trang) ==")
    thanh = re.findall(r"<(header|nav|section|main|article|aside|footer)\b([^>]*)>", html, re.I)
    for i, (t, attr) in enumerate(thanh[:30], 1):
        ident = re.search(r'(?:id|class)=["\']([^"\']{0,50})', attr)
        print("  %2d. <%s> %s" % (i, t.lower(), ident.group(1) if ident else ""))
    print("\n== TIÊU ĐỀ (h1 đến h3, chỉ để hiểu mạch, đừng chép) ==")
    for t, x in re.findall(r"<(h[1-3])[^>]*>(.*?)</\1>", html, re.I | re.S)[:25]:
        print("  %s: %s" % (t.upper(), re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()[:90]))
    nut = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<(?:button|a)[^>]*class=[\"'][^\"']*(?:btn|button|cta)[^\"']*[\"'][^>]*>(.*?)</(?:button|a)>", html, re.I | re.S)]
    nut += [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<button[^>]*>(.*?)</button>", html, re.I | re.S)]
    print("\n== CHỮ TRÊN NÚT KÊU GỌI ==")
    print("  " + " | ".join(dict.fromkeys(n for n in nut if n and len(n) < 60))[:600])
    seo = {k: (re.search(p, html, re.I | re.S) or [None, ""])[1].strip()[:120] for k, p in (
        ("title", r"<title[^>]*>(.*?)</title>"), ("description", r'name=["\']description["\'][^>]+content=["\']([^"\']*)'),
        ("og:image", r'property=["\']og:image["\'][^>]+content=["\']([^"\']*)'))}
    print("\n== SEO ==")
    for k, v in seo.items():
        print("  %s: %s" % (k, v or "(trống)"))
    print("\nLƯU Ý: lấy CẤU TRÚC và PHONG CÁCH làm cảm hứng; đổi màu, chữ, ảnh theo thương hiệu của chủ; viết lại toàn bộ nội dung; không dùng logo, ảnh, mã nguồn của web mẫu.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    try:
        main(sys.argv[1])
    except Exception as e:  # noqa: BLE001
        print("LỖI: %s" % e)
        sys.exit(1)
