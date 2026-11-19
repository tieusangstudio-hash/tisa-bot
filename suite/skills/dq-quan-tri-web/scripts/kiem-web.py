#!/usr/bin/env python3
"""Kiểm một web đã đưa lên mạng: mã trả về, chuyển hướng, https, chứng chỉ, tiêu đề, meta, tốc độ, trang con cơ bản.
Dùng: python3 kiem-web.py https://ten-mien.vn [--www]   (--www: kiểm thêm bản www và bản apex chuyển hướng đúng chưa)
Chỉ đọc, không sửa gì. Thoát 0 nếu không có lỗi nặng, 1 nếu có. Chỉ dùng thư viện chuẩn của Python."""
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

UA = "Mozilla/5.0 (compatible; TISA-Quan-Tri-Web/1.0)"
loi, canh_bao, ok = [], [], []


class KhongTuDi(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def lay(url, theo_chuyen_huong=True, gioi_han=1_500_000, timeout=20):
    """Trả (mã, headers, nội dung, thời gian giây, chuỗi chuyển hướng)."""
    chuoi, hien = [], url
    t0 = time.time()
    for _ in range(8):
        op = urllib.request.build_opener(KhongTuDi)
        req = urllib.request.Request(hien, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
        try:
            r = op.open(req, timeout=timeout)
            return r.status, r.headers, r.read(gioi_han), time.time() - t0, chuoi
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                nxt = urljoin(hien, e.headers["Location"])
                chuoi.append((e.code, hien, nxt))
                if not theo_chuyen_huong:
                    return e.code, e.headers, b"", time.time() - t0, chuoi
                hien = nxt
                continue
            return e.code, e.headers, e.read(gioi_han), time.time() - t0, chuoi
    raise RuntimeError("Chuyển hướng vòng lặp")


def chung_chi(host):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as s:
            with ctx.wrap_socket(s, server_hostname=host) as ss:
                c = ss.getpeercert()
        het = datetime.strptime(c["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        return (het - datetime.now(timezone.utc)).days
    except ssl.SSLCertVerificationError as e:
        loi.append("Chứng chỉ https không hợp lệ: %s" % (e.verify_message or e))
    except Exception as e:  # noqa: BLE001
        canh_bao.append("Chưa đọc được chứng chỉ https (%s)" % type(e).__name__)
    return None


def phan_tich(html, url):
    t = html.decode("utf-8", "replace")
    g = lambda p: (re.search(p, t, re.I | re.S) or [None, ""])[1].strip() if re.search(p, t, re.I | re.S) else ""
    title = re.sub(r"\s+", " ", g(r"<title[^>]*>(.*?)</title>"))
    if not title:
        loi.append("Thiếu thẻ <title>")
    elif len(title) > 70:
        canh_bao.append("Tiêu đề dài %d ký tự (nên dưới 60 đến 70)" % len(title))
    mota = g(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)')
    if not mota:
        canh_bao.append("Thiếu meta description")
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', t, re.I):
        loi.append("Thiếu meta viewport: web sẽ vỡ trên điện thoại")
    if not re.search(r'<html[^>]+lang=', t, re.I):
        canh_bao.append("Thẻ <html> thiếu lang")
    if not re.search(r'property=["\']og:image["\']', t, re.I):
        canh_bao.append("Thiếu og:image: chia sẻ lên Facebook/Zalo sẽ không có ảnh")
    h1 = len(re.findall(r"<h1[\s>]", t, re.I))
    if h1 != 1:
        canh_bao.append("Có %d thẻ <h1> (nên đúng 1)" % h1)
    thieu_alt = len([m for m in re.findall(r"<img\b[^>]*>", t, re.I) if not re.search(r"\balt=", m, re.I)])
    if thieu_alt:
        canh_bao.append("%d ảnh thiếu alt" % thieu_alt)
    if re.search(r"(src|href)=[\"']http://(?!localhost)", t, re.I):
        canh_bao.append("Có tài nguyên gọi bằng http (không bảo mật), nên đổi sang https")
    if re.search(r"<form\b", t, re.I) and not re.search(r"<input[^>]+(tel|phone|sdt|name=[\"'](phone|sdt|dien_thoai))", t, re.I):
        canh_bao.append("Có form nhưng chưa thấy ô số điện thoại (kiểm lại nếu đây là trang thu lead)")
    return title, mota


def kiem(url):
    p = urlparse(url)
    host = p.hostname
    print("== %s ==" % url)
    try:
        ma, hd, nd, giay, chuoi = lay(url)
    except Exception as e:  # noqa: BLE001
        loi.append("Không mở được: %s" % e)
        return
    for c in chuoi:
        print("  chuyển hướng %s: %s -> %s" % c)
    if ma >= 400:
        loi.append("Mã trả về %s" % ma)
    else:
        ok.append("Mã %s, %d byte, %.2f giây" % (ma, len(nd), giay))
    if giay > 3:
        canh_bao.append("Phản hồi chậm (%.1f giây)" % giay)
    if len(nd) > 1_000_000:
        canh_bao.append("Trang nặng (%.1f MB HTML), kiểm ảnh và mã nhúng" % (len(nd) / 1e6))
    if p.scheme == "http" and not any(u.startswith("https://") for _, _, u in chuoi):
        canh_bao.append("Địa chỉ http không tự chuyển sang https")
    if p.scheme == "https" or any(u.startswith("https://") for _, _, u in chuoi):
        ngay = chung_chi(host)
        if ngay is not None:
            (ok if ngay > 14 else canh_bao).append("Chứng chỉ https còn %d ngày" % ngay)
    ctype = hd.get("Content-Type", "")
    if "text/html" in ctype and nd:
        title, mota = phan_tich(nd, url)
        ok.append("Tiêu đề: %s" % (title or "(trống)"))
    for h, ten in (("Strict-Transport-Security", "HSTS"), ("X-Content-Type-Options", "X-Content-Type-Options"), ("Content-Security-Policy", "CSP")):
        if h not in hd:
            canh_bao.append("Chưa có header %s (không bắt buộc, nên có khi web có form/đăng nhập)" % ten)
    goc = "%s://%s" % (p.scheme, p.netloc)
    for duong in ("/robots.txt", "/sitemap.xml", "/favicon.ico"):
        try:
            m, *_ = lay(goc + duong, timeout=10)
            (ok if m == 200 else canh_bao).append("%s: %s" % (duong, "có" if m == 200 else "mã %s" % m))
        except Exception:  # noqa: BLE001
            canh_bao.append("%s: không đọc được" % duong)
    try:
        m, *_ = lay(goc + "/trang-khong-ton-tai-kiem-404", timeout=10)
        if m == 200:
            canh_bao.append("Đường dẫn không tồn tại vẫn trả 200 (nên là 404, trừ khi là web một trang)")
    except Exception:  # noqa: BLE001
        pass


def kiem_www(url):
    p = urlparse(url)
    host = p.hostname
    kia = host[4:] if host.startswith("www.") else "www." + host
    print("== đối chiếu %s với %s ==" % (host, kia))
    try:
        ma, hd, _, _, chuoi = lay("%s://%s%s" % (p.scheme, kia, p.path or "/"), theo_chuyen_huong=False)
        if ma in (301, 302, 307, 308):
            ok.append("%s chuyển hướng (%s) tới %s" % (kia, ma, hd.get("Location", "?")))
        elif ma == 200:
            canh_bao.append("%s cũng trả 200: hai địa chỉ cùng hiện web, nên chuyển hướng một bên sang bên còn lại" % kia)
        else:
            canh_bao.append("%s trả mã %s (chưa trỏ hoặc chưa gắn tên miền)" % (kia, ma))
    except Exception as e:  # noqa: BLE001
        canh_bao.append("%s không mở được: %s" % (kia, e))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        print(__doc__)
        sys.exit(2)
    u = a[0] if re.match(r"^https?://", a[0]) else "https://" + a[0]
    kiem(u)
    if "--www" in sys.argv:
        kiem_www(u)
    print("\nĐẠT:")
    print("\n".join("  + " + x for x in ok) or "  (không có)")
    print("CẢNH BÁO:" + ("" if canh_bao else " không"))
    print("\n".join("  ! " + x for x in canh_bao))
    print("LỖI:" + ("" if loi else " không"))
    print("\n".join("  X " + x for x in loi))
    sys.exit(1 if loi else 0)
