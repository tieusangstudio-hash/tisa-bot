#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xuất file HTML infographic ra ảnh PNG — bộ skill /ts-infographic.

Không bắt buộc cài thêm thư viện. Thứ tự thử:
  1. Playwright (nếu đã cài: pip install playwright && python -m playwright install chromium)
  2. Chrome / Edge / Chromium có sẵn trên máy, chạy ẩn (headless) — tự dò đường dẫn macOS, Windows, Linux
  3. Không có gì → in hướng dẫn mở file bằng trình duyệt và tự chụp

CÁCH CHẠY
  macOS / Linux:
    python3 scripts/xuat_anh.py infographic.html
    python3 scripts/xuat_anh.py infographic.html --kho 1080x1080 --ra anh-vuong.png
    python3 scripts/xuat_anh.py thu-muc-chua-html/            # xuất cả loạt
    python3 scripts/xuat_anh.py infographic.html --scale 2    # ảnh nét gấp đôi (2160 px ngang)
  Windows (Command Prompt / PowerShell):
    py scripts\\xuat_anh.py infographic.html

TÙY CHỌN
  --kho 1080x1350|1080x1080|1080x1920   khổ ảnh; mặc định đọc từ data-kho trong file HTML, không có thì 1080x1350
  --ra <file.png>                       tên file ảnh (mặc định: cùng tên file HTML, đuôi .png)
  --scale 1|2                           độ nét (mặc định 1)
  --cach auto|playwright|chrome         ép dùng một cách cụ thể (mặc định auto)
  --chrome <đường dẫn>                  chỉ đường tới chrome.exe / msedge.exe nếu script không tự tìm thấy
  --font-offline                        bỏ qua Google Fonts, dùng font có sẵn trên máy (khi mạng chậm/chặn)
"""

import argparse
import glob
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

KHO_HOP_LE = {"1080x1350", "1080x1080", "1080x1920"}
KHO_MAC_DINH = "1080x1350"
FONT_URL = "https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;700&display=swap"
MIEN_FONT = ("fonts.googleapis.com", "fonts.gstatic.com")


def in_ra(*args):
    print(*args, flush=True)


# ---------------------------------------------------------------- tiện ích
def doc_kho_tu_html(duong_dan):
    try:
        noi_dung = Path(duong_dan).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = re.search(r'<body[^>]*data-kho="(\d{3,4}x\d{3,4})"', noi_dung)
    return m.group(1) if m else None


def kich_thuoc_png(duong_dan):
    try:
        with open(duong_dan, "rb") as f:
            dau = f.read(24)
        if dau[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", dau[16:24])
    except OSError:
        return None


def mang_tai_duoc_font(giay=4):
    """Thử tải CSS của Google Fonts (tôn trọng proxy của hệ thống)."""
    try:
        req = urllib.request.Request(FONT_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=giay) as r:
            return r.status == 200
    except Exception:
        return False


def _thu_muc_playwright():
    """Các nơi Playwright cất trình duyệt (để tận dụng bản chrome-headless-shell nếu đã cài)."""
    ds = []
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        ds.append(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    if sys.platform == "darwin":
        ds.append(os.path.expanduser("~/Library/Caches/ms-playwright"))
    elif os.name == "nt":
        if os.environ.get("LOCALAPPDATA"):
            ds.append(os.path.join(os.environ["LOCALAPPDATA"], "ms-playwright"))
    else:
        ds += [os.path.expanduser("~/.cache/ms-playwright"), "/opt/pw-browsers", "/ms-playwright"]
    return ds


def tim_chrome(chi_dinh=None):
    """Trả về DANH SÁCH đường dẫn trình duyệt dùng được, theo thứ tự ưu tiên."""
    if chi_dinh:
        p = chi_dinh if Path(chi_dinh).exists() else shutil.which(chi_dinh)
        return [p] if p else []
    ung_vien = []
    if os.environ.get("CHROME_PATH"):
        ung_vien.append(os.environ["CHROME_PATH"])
    if sys.platform == "darwin":
        for app in ("Google Chrome", "Microsoft Edge", "Chromium", "Brave Browser", "Google Chrome Canary"):
            ung_vien.append(f"/Applications/{app}.app/Contents/MacOS/{app}")
            ung_vien.append(os.path.expanduser(f"~/Applications/{app}.app/Contents/MacOS/{app}"))
    elif os.name == "nt":
        goc = [os.environ.get(k) for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
        for g in filter(None, goc):
            ung_vien += [
                os.path.join(g, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(g, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(g, "Chromium", "Application", "chrome.exe"),
                os.path.join(g, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
            ]
        for ten in ("chrome", "msedge"):
            ung_vien.append(shutil.which(ten))
    else:
        for ten in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                    "microsoft-edge", "microsoft-edge-stable", "brave-browser"):
            ung_vien.append(shutil.which(ten))
        ung_vien += ["/snap/bin/chromium", "/usr/bin/google-chrome", "/usr/bin/chromium"]
    # Bản chrome-headless-shell do Playwright cài (nhẹ, chuyên chụp ảnh) — dùng làm dự phòng
    for d in _thu_muc_playwright():
        for mau in ("chromium_headless_shell-*/*/chrome-headless-shell*", "chromium_headless_shell-*/*/headless_shell*"):
            for p in sorted(glob.glob(os.path.join(d, mau)), reverse=True):
                if p.endswith((".real", ".pak", ".dat")):
                    continue
                ung_vien.append(p)
    ket_qua, da_co = [], set()
    for p in ung_vien:
        if p and Path(p).is_file() and os.path.realpath(p) not in da_co:
            da_co.add(os.path.realpath(p))
            ket_qua.append(p)
    return ket_qua


# ---------------------------------------------------------------- cách 1: Playwright
def chup_playwright(html, png, rong, cao, scale, chan_font, chrome_he_thong=()):
    from playwright.sync_api import sync_playwright  # noqa: lỗi import được xử lý ở ngoài

    with sync_playwright() as p:
        trinh_duyet = None
        loi_cuoi = None
        cach_mo = [dict(), dict(channel="chrome"), dict(channel="msedge")]
        cach_mo += [dict(executable_path=p) for p in chrome_he_thong]
        for tuy_chon in cach_mo:
            try:
                trinh_duyet = p.chromium.launch(timeout=30000, **tuy_chon)
                break
            except Exception as e:  # trình duyệt của Playwright chưa cài → thử Chrome/Edge thật
                loi_cuoi = e
        if trinh_duyet is None:
            raise RuntimeError(f"Playwright không mở được trình duyệt: {loi_cuoi}")
        trang = trinh_duyet.new_page(viewport={"width": rong, "height": cao}, device_scale_factor=scale)
        if chan_font:
            trang.route(re.compile(r"https://fonts\.(googleapis|gstatic)\.com/.*"), lambda r: r.abort())
        try:
            trang.goto(Path(html).resolve().as_uri(), wait_until="load", timeout=20000)
        except Exception:
            in_ra("  (Trang tải chậm — vẫn tiếp tục chụp)")
        try:
            trang.evaluate("() => document.fonts ? document.fonts.ready.then(() => true) : true")
        except Exception:
            pass
        trang.wait_for_timeout(400)
        tran = trang.evaluate("() => document.documentElement.getAttribute('data-tran') === '1'")
        trang.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": rong, "height": cao})
        trinh_duyet.close()
        return bool(tran)


# ---------------------------------------------------------------- cách 2: Chrome/Edge headless
def chup_chrome(chrome, html, png, rong, cao, scale, chan_font, gioi_han=60):
    url = Path(html).resolve().as_uri()
    la_shell = "headless" in Path(chrome).name.lower()
    with tempfile.TemporaryDirectory(prefix="ts-infographic-") as ho_so:
        chung = [
            chrome, "--headless" if la_shell else "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
            "--no-first-run", "--no-default-browser-check", f"--user-data-dir={ho_so}",
            f"--window-size={rong},{cao}", f"--force-device-scale-factor={scale}",
            "--virtual-time-budget=8000", "--allow-file-access-from-files",
            "--disable-background-networking", "--disable-component-update", "--disable-sync",
            "--disable-extensions", "--disable-dev-shm-usage",
        ]
        if sys.platform.startswith("linux") and hasattr(os, "geteuid") and os.geteuid() == 0:
            chung.append("--no-sandbox")
        if chan_font:
            chung.append("--host-resolver-rules=" + ", ".join(f"MAP {m} ~NOTFOUND" for m in MIEN_FONT))
        lenh = chung + [f"--screenshot={Path(png).resolve()}", url]
        try:
            kq = subprocess.run(lenh, capture_output=True, text=True, timeout=gioi_han,
                                encoding="utf-8", errors="ignore")
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"{Path(chrome).name} không phản hồi sau {gioi_han} giây")
        if not Path(png).exists() and lenh[1] == "--headless=new":
            # Chrome bản cũ không hiểu --headless=new
            lenh[1] = "--headless"
            try:
                kq = subprocess.run(lenh, capture_output=True, text=True, timeout=gioi_han,
                                    encoding="utf-8", errors="ignore")
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"{Path(chrome).name} không phản hồi sau {gioi_han} giây")
        if not Path(png).exists():
            raise RuntimeError(f"{Path(chrome).name} không tạo được ảnh. " + (kq.stderr or "")[-300:])
        # Kiểm tra tràn chữ bằng cách đọc DOM sau khi trang chạy xong
        tran = False
        try:
            dom = subprocess.run(chung + ["--dump-dom", url], capture_output=True, text=True,
                                 timeout=gioi_han, encoding="utf-8", errors="ignore")
            the_html = re.search(r"<html\b[^>]*>", dom.stdout or "")
            tran = bool(the_html and 'data-tran="1"' in the_html.group(0))
        except Exception:
            pass
        return tran


# ---------------------------------------------------------------- điều phối
def huong_dan_tu_chup(html, rong, cao):
    in_ra(f"""
CHƯA XUẤT ĐƯỢC ẢNH TỰ ĐỘNG (không có Playwright/Chrome/Edge, hoặc trình duyệt không chạy ẩn được).
Cách tự chụp (2 phút):
  1. Mở file bằng Chrome hoặc Edge: {Path(html).resolve()}
  2. Bấm F12 (macOS: Cmd+Option+I) để mở công cụ nhà phát triển.
  3. Bấm biểu tượng điện thoại/máy tính bảng (Toggle device toolbar) — hoặc Ctrl+Shift+M (macOS: Cmd+Shift+M).
  4. Ở thanh trên cùng chọn 'Responsive', gõ kích thước {rong} × {cao}, tỉ lệ thu phóng 100%.
  5. Bấm dấu ba chấm ⋮ của thanh đó → 'Capture screenshot' → ảnh PNG tự tải về.
Hoặc cài Playwright một lần:  pip install playwright  rồi  python -m playwright install chromium
""")


def xuat_mot(html, png, kho, scale, cach, chrome_chi_dinh, chan_font):
    rong, cao = (int(x) for x in kho.split("x"))
    ds_chrome = tim_chrome(chrome_chi_dinh)
    loi = []

    if cach in ("auto", "playwright"):
        try:
            tran = chup_playwright(html, png, rong, cao, scale, chan_font, ds_chrome)
            return "Playwright", tran
        except ImportError:
            loi.append("chưa cài Playwright")
        except Exception as e:
            loi.append(f"Playwright lỗi: {str(e)[:200]}")
        if cach == "playwright":
            raise RuntimeError("; ".join(loi))

    if cach in ("auto", "chrome"):
        if not ds_chrome:
            loi.append("không tìm thấy Chrome/Edge")
        for chrome in ds_chrome:
            try:
                tran = chup_chrome(chrome, html, png, rong, cao, scale, chan_font)
                return f"trình duyệt chạy ẩn ({Path(chrome).name})", tran
            except Exception as e:
                loi.append(str(e)[:200])
                in_ra(f"  ({e} — thử cách khác)")

    raise LookupError("; ".join(loi))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Xuất HTML infographic ra ảnh PNG.")
    p.add_argument("dau_vao", nargs="+", help="File .html hoặc thư mục chứa nhiều file .html")
    p.add_argument("--kho", choices=sorted(KHO_HOP_LE), help="Khổ ảnh (mặc định đọc từ data-kho trong HTML)")
    p.add_argument("--ra", help="Tên file PNG (chỉ dùng khi xuất 1 file)")
    p.add_argument("--scale", type=int, default=1, choices=[1, 2, 3], help="Độ nét (1 = 1080 px ngang)")
    p.add_argument("--cach", default="auto", choices=["auto", "playwright", "chrome"])
    p.add_argument("--chrome", help="Đường dẫn tới Chrome/Edge nếu không tự tìm thấy")
    p.add_argument("--font-offline", action="store_true", help="Không tải Google Fonts, dùng font trên máy")
    a = p.parse_args()

    danh_sach = []
    for muc in a.dau_vao:
        if os.path.isdir(muc):
            danh_sach += sorted(glob.glob(os.path.join(muc, "*.html")))
        elif os.path.isfile(muc):
            danh_sach.append(muc)
        else:
            in_ra(f"Bỏ qua (không thấy file): {muc}")
    if not danh_sach:
        sys.exit("Không có file HTML nào để xuất.")
    if a.ra and len(danh_sach) > 1:
        sys.exit("--ra chỉ dùng khi xuất 1 file.")

    chan_font = a.font_offline or not mang_tai_duoc_font()
    if chan_font and not a.font_offline:
        in_ra("Lưu ý: không tải được font Be Vietnam Pro từ Google Fonts → dùng font dự phòng có sẵn trên máy "
              "(vẫn đủ dấu tiếng Việt). Muốn đúng font: cài font Be Vietnam Pro vào máy rồi xuất lại.")

    thanh_cong = 0
    for html in danh_sach:
        kho = a.kho or doc_kho_tu_html(html) or KHO_MAC_DINH
        if kho not in KHO_HOP_LE:
            in_ra(f"  Khổ {kho} không chuẩn, vẫn xuất theo đúng kích thước này.")
        png = a.ra or str(Path(html).with_suffix(".png"))
        in_ra(f"→ Đang xuất {html} ({kho}) ...")
        # --kho khác data-kho trong file → tạo bản tạm cùng thư mục (giữ đúng đường dẫn logo/ảnh) với data-kho mới
        nguon, ban_tam = html, None
        kho_trong_file = doc_kho_tu_html(html)
        if a.kho and kho_trong_file and kho_trong_file != a.kho:
            noi_dung = Path(html).read_text(encoding="utf-8", errors="ignore")
            noi_dung = re.sub(r'(<body[^>]*data-kho=")\d{3,4}x\d{3,4}(")', r"\g<1>" + a.kho + r"\g<2>", noi_dung, count=1)
            ban_tam = str(Path(html).with_name(f".{Path(html).stem}.{a.kho}.tam.html"))
            Path(ban_tam).write_text(noi_dung, encoding="utf-8")
            nguon = ban_tam
        try:
            cach, tran = xuat_mot(nguon, png, kho, a.scale, a.cach, a.chrome, chan_font)
        except LookupError as e:
            in_ra(f"  Không xuất được: {e}")
            huong_dan_tu_chup(html, *(int(x) for x in kho.split("x")))
            sys.exit(2)
        except Exception as e:
            in_ra(f"  Lỗi: {e}")
            continue
        finally:
            if ban_tam and os.path.exists(ban_tam):
                os.remove(ban_tam)
        kt = kich_thuoc_png(png)
        kt_chu = f"{kt[0]}×{kt[1]} px" if kt else "không đọc được kích thước"
        in_ra(f"  ✓ Đã lưu: {png} — {kt_chu} — bằng {cach}")
        if tran:
            in_ra("  ⚠ Nội dung bị TRÀN khung (ảnh có viền đỏ). Rút gọn chữ hoặc bớt thẻ rồi xuất lại.")
        thanh_cong += 1

    in_ra(f"Xong: {thanh_cong}/{len(danh_sach)} ảnh.")
    if thanh_cong < len(danh_sach):
        sys.exit(1)


if __name__ == "__main__":
    main()
