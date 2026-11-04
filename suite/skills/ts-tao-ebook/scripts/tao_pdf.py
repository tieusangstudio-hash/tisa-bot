#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Biến file Markdown thành ebook PDF có bìa thương hiệu — bộ skill /ts-tao-ebook.

Chỉ dùng thư viện chuẩn của Python 3 (không cần cài thêm). Thứ tự dựng PDF:
  1. Playwright (nếu đã cài)   2. Chrome / Edge chạy ẩn (tự dò trên macOS, Windows, Linux)
  3. Không có gì → vẫn tạo file HTML để mở bằng trình duyệt và bấm In → Lưu thành PDF.

CÁCH CHẠY
  macOS / Linux:
    python3 scripts/tao_pdf.py ebook.md
    python3 scripts/tao_pdf.py ebook.md --ra ebook.pdf --kho A4 --mau-chinh "#123B6D" --mau-nhan "#F5B700"
    python3 scripts/tao_pdf.py --mau > ebook.md        # in ra file Markdown mẫu để bắt đầu
  Windows:
    py scripts\\tao_pdf.py ebook.md

THÔNG TIN BÌA — ghi ở đầu file Markdown (khối giữa hai dòng ---), hoặc truyền bằng tùy chọn dòng lệnh:
  ---
  ten_sach: 7 ngày quay video bán hàng bằng điện thoại
  phu_de: Cẩm nang cho người mới, không cần máy quay
  tac_gia: Nguyễn Lan
  nhan_bia: Ebook miễn phí
  logo: logo.png                (đường dẫn tương đối so với file .md)
  mau_chinh: "#1F2A44"
  mau_nhan: "#F5B700"
  kho: A5                       (A5 hoặc A4)
  kieu_chu: sans                (sans = chữ không chân · serif = chữ có chân)
  nam: 2026
  lien_he: Zalo 09xx xxx xxx · trang-cua-ban.vn
  ---

CÚ PHÁP MARKDOWN HỖ TRỢ
  # Phần …            → trang mở phần (tiêu đề cấp 1)
  ## Chương …         → mỗi chương sang trang mới (tiêu đề cấp 2)
  ### / ####          → tiêu đề nhỏ
  Đoạn văn, **đậm**, *nghiêng*, `mã`, [chữ](link), ![chú thích](anh.png)
  - gạch đầu dòng · 1. danh sách số (lùi 2–4 dấu cách để lồng cấp)
  > trích dẫn thường
  > [!CTA] Tiêu đề hộp       → HỘP KÊU GỌI HÀNH ĐỘNG (các dòng > tiếp theo là nội dung)
  > [!MEO] Tiêu đề hộp       → hộp mẹo / ghi chú
  ---                  → đường kẻ ngang
"""

import argparse
import base64
import html
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
from datetime import date
from pathlib import Path

THU_MUC_SKILL = Path(__file__).resolve().parent.parent
MAU_HTML = THU_MUC_SKILL / "templates" / "bia-va-noi-dung.html"
KHO_GIAY = {"A5": ("148mm", "210mm"), "A4": ("210mm", "297mm")}
FONT_SANS = '"Be Vietnam Pro", "Inter", "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", "DejaVu Sans", sans-serif'
FONT_SERIF = '"Lora", "Noto Serif", Georgia, "Times New Roman", "DejaVu Serif", serif'

MARKDOWN_MAU = """---
ten_sach: 5 bước bán hàng online cho người mới
phu_de: Ví dụ minh họa — cẩm nang ngắn cho chủ shop nhỏ
tac_gia: Tên Tác Giả
nhan_bia: Ebook miễn phí
mau_chinh: "#1F2A44"
mau_nhan: "#F5B700"
kho: A5
lien_he: Zalo [số của bạn] · [website của bạn]
---

# Phần 1: Chuẩn bị

## Chương 1: Chọn đúng một sản phẩm

Người mới thường muốn bán **nhiều thứ cùng lúc**. Thực tế, tập trung vào *một* sản phẩm giúp bạn hiểu khách nhanh hơn.

### Ba câu hỏi để chọn

1. Sản phẩm này giải quyết vấn đề gì?
2. Ai đang gặp vấn đề đó nhiều nhất?
   - Họ ở đâu trên mạng?
   - Họ đã thử cách nào?
3. Bạn có lãi ít nhất 30% sau chi phí không?

> [!MEO] Mẹo nhỏ
> Viết câu trả lời ra giấy. Nếu không trả lời được câu 1 trong một dòng, hãy chọn sản phẩm khác.

> [!CTA] Chưa chắc sản phẩm của bạn có bán được không?
> Gửi tên sản phẩm cho [kênh liên hệ của bạn] — mình góp ý miễn phí trong 24 giờ.

## Chương 2: Hiểu khách hàng

Hãy đọc bình luận của khách trong các nhóm cùng ngành và ghi lại **đúng chữ họ dùng**.

> [!CTA] Bạn muốn có bảng chân dung khách hàng làm sẵn?
> Nhắn **"CHÂN DUNG"** cho [kênh liên hệ của bạn] để nhận mẫu miễn phí.

# Phần 2: Bắt đầu bán

## Chương 3: Bài đăng đầu tiên

- Mở đầu bằng vấn đề của khách.
- Kể một câu chuyện có thật.
- Kết bằng **một** lời mời rõ ràng.

> [!CTA] Muốn có 10 mẫu bài đăng viết sẵn?
> Nhắn **"MẪU BÀI"** cho [kênh liên hệ của bạn] để nhận ngay.

---

Chúc bạn có đơn hàng đầu tiên thật sớm!
"""


def in_ra(*a):
    print(*a, flush=True)


# =============================================================== 1. ĐỌC THÔNG TIN ĐẦU FILE
def tach_thong_tin(van_ban):
    """Tách khối --- ... --- ở đầu file (dạng 'khóa: giá trị' đơn giản)."""
    thong_tin = {}
    dong = van_ban.splitlines()
    if dong and dong[0].strip() == "---":
        for i in range(1, len(dong)):
            if dong[i].strip() == "---":
                for d in dong[1:i]:
                    if ":" in d and not d.lstrip().startswith("#"):
                        k, v = d.split(":", 1)
                        v = v.strip()
                        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                            v = v[1:-1]
                        thong_tin[k.strip().lower()] = v
                return thong_tin, "\n".join(dong[i + 1:])
    return thong_tin, van_ban


# =============================================================== 2. PARSER MARKDOWN TỐI GIẢN
class ChuyenMarkdown:
    def __init__(self, thu_muc_goc, nhung_anh=True):
        self.goc = Path(thu_muc_goc)
        self.nhung_anh = nhung_anh
        self.muc_luc = []          # (cấp, tiêu đề, id)
        self.dem_id = 0
        self.canh_bao = []

    # ---------- định dạng trong dòng
    def _anh_src(self, duong_dan):
        if re.match(r"^(https?:|data:)", duong_dan):
            return duong_dan
        p = (self.goc / duong_dan).resolve()
        if not p.exists():
            self.canh_bao.append(f"Không thấy ảnh: {duong_dan}")
            return duong_dan
        if self.nhung_anh:
            loai = mimetypes.guess_type(str(p))[0] or "image/png"
            return f"data:{loai};base64," + base64.b64encode(p.read_bytes()).decode("ascii")
        return p.as_uri()

    def trong_dong(self, s):
        giu = []

        def cat(m):
            giu.append(m.group(0))
            return f"\x00{len(giu) - 1}\x00"

        # bảo vệ `mã`
        s = re.sub(r"`[^`]+`", cat, s)
        s = html.escape(s, quote=False)

        def ma(i):
            return "<code>" + html.escape(giu[i][1:-1], quote=False) + "</code>"

        s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                   lambda m: f'<img src="{html.escape(self._anh_src(html.unescape(m.group(2))))}" alt="{m.group(1)}">', s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"__(.+?)__", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"(?<![_\w])_(?!\s)(.+?)(?<!\s)_(?![_\w])", r"<em>\1</em>", s)
        s = re.sub(r"\x00(\d+)\x00", lambda m: ma(int(m.group(1))), s)
        return s

    def _id(self):
        self.dem_id += 1
        return f"muc-{self.dem_id}"

    # ---------- danh sách (hỗ trợ lồng theo thụt lề)
    def _danh_sach(self, cac_dong):
        ket_qua, ngan_xep = [], []   # ngăn xếp: (thụt lề, thẻ)
        for thut, the, noi_dung in cac_dong:
            while ngan_xep and thut < ngan_xep[-1][0]:
                ket_qua.append(f"</li></{ngan_xep.pop()[1]}>")
            if ngan_xep and thut == ngan_xep[-1][0] and the != ngan_xep[-1][1]:
                ket_qua.append(f"</li></{ngan_xep.pop()[1]}>")
            if not ngan_xep or thut > ngan_xep[-1][0]:
                ket_qua.append(f"<{the}>")
                ngan_xep.append((thut, the))
            else:
                ket_qua.append("</li>")
            ket_qua.append("<li>" + self.trong_dong(noi_dung))
        while ngan_xep:
            ket_qua.append(f"</li></{ngan_xep.pop()[1]}>")
        return "".join(ket_qua)

    # ---------- trích dẫn / hộp CTA
    def _trich_dan(self, cac_dong):
        dau = cac_dong[0].strip() if cac_dong else ""
        m = re.match(r"^\[!(CTA|MEO|MẸO|NOTE|TIP)\]\s*(.*)$", dau, re.I)
        if m:
            loai = "cta" if m.group(1).upper() == "CTA" else "meo"
            tieu_de = m.group(2).strip()
            than = self._doan_tu_dong(cac_dong[1:])
            nhan = "Hành động ngay" if loai == "cta" else "Mẹo"
            phan_tieu_de = f"<p><strong>{self.trong_dong(tieu_de)}</strong></p>" if tieu_de else ""
            return (f'<aside class="hop-{loai}"><span class="nhan-cta">{nhan}</span>'
                    f"{phan_tieu_de}{than}</aside>")
        return "<blockquote>" + self._doan_tu_dong(cac_dong) + "</blockquote>"

    def _doan_tu_dong(self, cac_dong):
        doan, hien_tai = [], []
        for d in cac_dong:
            if d.strip():
                hien_tai.append(d.strip())
            elif hien_tai:
                doan.append(hien_tai)
                hien_tai = []
        if hien_tai:
            doan.append(hien_tai)
        out = []
        for d in doan:
            if all(re.match(r"^([-*+]|\d+[.)])\s+", x) for x in d):
                out.append(self._danh_sach([(0, "ol" if re.match(r"^\d", x) else "ul",
                                              re.sub(r"^([-*+]|\d+[.)])\s+", "", x)) for x in d]))
            else:
                out.append("<p>" + "<br>".join(self.trong_dong(x) for x in d) + "</p>")
        return "".join(out)

    # ---------- chính
    def chuyen(self, van_ban):
        van_ban = unicodedata.normalize("NFC", van_ban.replace("\r\n", "\n").replace("\t", "    "))
        dong = van_ban.split("\n")
        out = []
        trong_chuong = False
        doan = []
        i = 0

        def xa_doan():
            if doan:
                out.append("<p>" + " ".join(self.trong_dong(x.strip()) for x in doan) + "</p>")
                doan.clear()

        def dong_chuong():
            nonlocal trong_chuong
            if trong_chuong:
                out.append("</section>")
                trong_chuong = False

        while i < len(dong):
            d = dong[i]
            s = d.strip()

            if not s:
                xa_doan()
                i += 1
                continue

            m = re.match(r"^(#{1,4})\s+(.*?)\s*#*$", s)
            if m:
                xa_doan()
                cap, tieu_de = len(m.group(1)), m.group(2)
                ma_id = self._id()
                if cap == 1:
                    dong_chuong()
                    m2 = re.match(r"^(Phần\s+[^:.\-–—]+)\s*[:.\-–—]\s*(.+)$", tieu_de, re.I)
                    so, ten = (m2.group(1), m2.group(2)) if m2 else ("", tieu_de)
                    so_html = f'<div class="so-phan">{self.trong_dong(so)}</div>' if so else ""
                    out.append(f'<section class="phan" id="{ma_id}">{so_html}<h1>{self.trong_dong(ten)}</h1></section>')
                    self.muc_luc.append((1, tieu_de, ma_id))
                elif cap == 2:
                    dong_chuong()
                    out.append(f'<section class="chuong"><h2 id="{ma_id}">{self.trong_dong(tieu_de)}</h2>')
                    trong_chuong = True
                    self.muc_luc.append((2, tieu_de, ma_id))
                else:
                    out.append(f'<h{cap} id="{ma_id}">{self.trong_dong(tieu_de)}</h{cap}>')
                i += 1
                continue

            if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
                xa_doan()
                out.append("<hr>")
                i += 1
                continue

            m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", s)
            if m:
                xa_doan()
                chu_thich = self.trong_dong(m.group(1))
                src = html.escape(self._anh_src(m.group(2)))
                cap_html = f"<figcaption>{chu_thich}</figcaption>" if m.group(1) else ""
                out.append(f'<figure><img src="{src}" alt="{html.escape(m.group(1))}">{cap_html}</figure>')
                i += 1
                continue

            if s.startswith(">"):
                xa_doan()
                khoi = []
                while i < len(dong) and dong[i].strip().startswith(">"):
                    khoi.append(re.sub(r"^\s*>\s?", "", dong[i]))
                    i += 1
                out.append(self._trich_dan(khoi))
                continue

            if re.match(r"^\s*([-*+]|\d+[.)])\s+", d):
                xa_doan()
                cac_muc = []
                while i < len(dong):
                    mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", dong[i])
                    if mm:
                        the = "ol" if mm.group(2)[0].isdigit() else "ul"
                        cac_muc.append((len(mm.group(1)), the, mm.group(3)))
                        i += 1
                    elif dong[i].strip() and dong[i].startswith("  ") and cac_muc:
                        t, th, nd = cac_muc[-1]
                        cac_muc[-1] = (t, th, nd + " " + dong[i].strip())
                        i += 1
                    else:
                        break
                out.append(self._danh_sach(cac_muc))
                continue

            doan.append(d)
            i += 1

        xa_doan()
        dong_chuong()
        return "\n".join(out)

    def html_muc_luc(self):
        if len([m for m in self.muc_luc if m[0] == 2]) < 2:
            return ""
        dong = []
        for cap, ten, ma_id in self.muc_luc:
            lop = "ml-phan" if cap == 1 else "ml-chuong"
            dong.append(f'<li class="{lop}"><a href="#{ma_id}" style="color:inherit;text-decoration:none">'
                        f"{self.trong_dong(ten)}</a></li>")
        return '<section class="muc-luc"><h2>Mục lục</h2><ol>' + "".join(dong) + "</ol></section>"


# =============================================================== 3. DỰNG HTML
def dung_html(md_path, tuy_chon):
    van_ban = Path(md_path).read_text(encoding="utf-8")
    thong_tin, than = tach_thong_tin(van_ban)

    def lay(khoa, mac_dinh=""):
        v = getattr(tuy_chon, khoa, None)
        return v if v else thong_tin.get(khoa, mac_dinh)

    kho = (lay("kho", "A5") or "A5").upper()
    if kho not in KHO_GIAY:
        in_ra(f"Khổ {kho} chưa hỗ trợ, dùng A5.")
        kho = "A5"
    rong, cao = KHO_GIAY[kho]

    chuyen = ChuyenMarkdown(Path(md_path).parent, nhung_anh=True)
    noi_dung = chuyen.chuyen(than)

    ten_sach = lay("ten_sach")
    if not ten_sach:
        m = re.search(r"^#{1,2}\s+(.+)$", than, re.M)
        ten_sach = m.group(1).strip() if m else Path(md_path).stem.replace("-", " ").title()

    logo = lay("logo")
    logo_html, logo_cuoi = "", ""
    if logo:
        src = chuyen._anh_src(logo)
        logo_html = f'<img class="bia-logo" src="{html.escape(src)}" alt="Logo">'
        logo_cuoi = f'<img src="{html.escape(src)}" alt="Logo"><br>'

    lien_he = lay("lien_he")
    trang_cuoi = ""
    if lien_he or logo:
        trang_cuoi = (f'<section class="trang-cuoi">{logo_cuoi}<h2>Cảm ơn bạn đã đọc!</h2>'
                      f'<div class="lien-he">{html.escape(lien_he).replace(" · ", chr(10))}</div></section>')

    kieu_chu = (lay("kieu_chu", "sans") or "sans").lower()
    thay = {
        "TEN_SACH": html.escape(ten_sach),
        "PHU_DE": html.escape(lay("phu_de")),
        "TAC_GIA": html.escape(lay("tac_gia")),
        "NHAN_BIA": html.escape(lay("nhan_bia", "Ebook")),
        "NAM": html.escape(str(lay("nam", str(date.today().year)))),
        "MAU_CHINH": lay("mau_chinh", "#1F2A44"),
        "MAU_NHAN": lay("mau_nhan", "#F5B700"),
        "KHO_GIAY": kho,
        "RONG_TRANG": rong,
        "CAO_TRANG": cao,
        "FONT_THAN": FONT_SERIF if kieu_chu.startswith("serif") else FONT_SANS,
        "LOGO_BIA": logo_html,
        "MUC_LUC": "" if tuy_chon.khong_muc_luc else chuyen.html_muc_luc(),
        "NOI_DUNG": noi_dung,
        "TRANG_CUOI": trang_cuoi,
    }
    for k in ("MAU_CHINH", "MAU_NHAN"):
        if not re.match(r"^#[0-9A-Fa-f]{3,8}$|^[a-zA-Z]+$|^rgb", thay[k]):
            in_ra(f"Mã màu '{thay[k]}' không hợp lệ, dùng màu mặc định.")
            thay[k] = "#1F2A44" if k == "MAU_CHINH" else "#F5B700"

    mau = MAU_HTML.read_text(encoding="utf-8")
    for k, v in thay.items():
        mau = mau.replace("{{" + k + "}}", v)

    so_cta = noi_dung.count('class="hop-cta"')
    so_chuong = len([m for m in chuyen.muc_luc if m[0] == 2])
    return mau, {"so_chuong": so_chuong, "so_cta": so_cta, "canh_bao": chuyen.canh_bao, "kho": kho}


# =============================================================== 4. DỰNG PDF
def mang_tai_duoc_font(giay=4):
    try:
        req = urllib.request.Request("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=giay) as r:
            return r.status == 200
    except Exception:
        return False


def tim_trinh_duyet(chi_dinh=None):
    if chi_dinh:
        p = chi_dinh if Path(chi_dinh).exists() else shutil.which(chi_dinh)
        return [p] if p else []
    ung_vien = [os.environ.get("CHROME_PATH")]
    if sys.platform == "darwin":
        for app in ("Google Chrome", "Microsoft Edge", "Chromium", "Brave Browser"):
            ung_vien += [f"/Applications/{app}.app/Contents/MacOS/{app}",
                         os.path.expanduser(f"~/Applications/{app}.app/Contents/MacOS/{app}")]
    elif os.name == "nt":
        for g in filter(None, (os.environ.get(k) for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"))):
            ung_vien += [os.path.join(g, "Google", "Chrome", "Application", "chrome.exe"),
                         os.path.join(g, "Microsoft", "Edge", "Application", "msedge.exe")]
        ung_vien += [shutil.which("chrome"), shutil.which("msedge")]
    else:
        for ten in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
            ung_vien.append(shutil.which(ten))
    # bản chrome-headless-shell do Playwright cài (nếu có)
    thu_muc_pw = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"),
                  os.path.expanduser("~/.cache/ms-playwright"),
                  os.path.expanduser("~/Library/Caches/ms-playwright"),
                  os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright"),
                  "/opt/pw-browsers"]
    import glob
    for d in filter(None, thu_muc_pw):
        for p in sorted(glob.glob(os.path.join(d, "chromium_headless_shell-*", "*", "chrome-headless-shell*")),
                        reverse=True):
            if not p.endswith((".real", ".pak", ".dat")):
                ung_vien.append(p)
    ket_qua, da_co = [], set()
    for p in ung_vien:
        if p and Path(p).is_file() and os.path.realpath(p) not in da_co:
            da_co.add(os.path.realpath(p))
            ket_qua.append(p)
    return ket_qua


def pdf_playwright(html_path, pdf_path, chan_font, ds_trinh_duyet):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        tb, loi = None, None
        for tc in [dict(), dict(channel="chrome"), dict(channel="msedge")] + \
                  [dict(executable_path=x) for x in ds_trinh_duyet]:
            try:
                tb = p.chromium.launch(timeout=30000, **tc)
                break
            except Exception as e:
                loi = e
        if tb is None:
            raise RuntimeError(f"Playwright không mở được trình duyệt: {loi}")
        trang = tb.new_page()
        if chan_font:
            trang.route(re.compile(r"https://fonts\.(googleapis|gstatic)\.com/.*"), lambda r: r.abort())
        try:
            trang.goto(Path(html_path).resolve().as_uri(), wait_until="load", timeout=30000)
        except Exception:
            in_ra("  (Trang tải chậm — vẫn tiếp tục)")
        try:
            trang.evaluate("() => document.fonts ? document.fonts.ready.then(() => true) : true")
        except Exception:
            pass
        trang.emulate_media(media="print")
        trang.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        tb.close()


def pdf_chrome(trinh_duyet, html_path, pdf_path, chan_font, gioi_han=90):
    la_shell = "headless" in Path(trinh_duyet).name.lower()
    with tempfile.TemporaryDirectory(prefix="ts-ebook-") as ho_so:
        lenh = [trinh_duyet, "--headless" if la_shell else "--headless=new", "--disable-gpu",
                "--no-first-run", "--no-default-browser-check", f"--user-data-dir={ho_so}",
                "--disable-background-networking", "--disable-component-update", "--disable-extensions",
                "--disable-dev-shm-usage", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                "--allow-file-access-from-files", f"--print-to-pdf={Path(pdf_path).resolve()}"]
        if sys.platform.startswith("linux") and hasattr(os, "geteuid") and os.geteuid() == 0:
            lenh.append("--no-sandbox")
        if chan_font:
            lenh.append("--host-resolver-rules=MAP fonts.googleapis.com ~NOTFOUND, MAP fonts.gstatic.com ~NOTFOUND")
        lenh.append(Path(html_path).resolve().as_uri())
        try:
            kq = subprocess.run(lenh, capture_output=True, text=True, timeout=gioi_han,
                                encoding="utf-8", errors="ignore")
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"{Path(trinh_duyet).name} không phản hồi sau {gioi_han} giây")
        if not Path(pdf_path).exists() or Path(pdf_path).stat().st_size < 1000:
            raise RuntimeError(f"{Path(trinh_duyet).name} không tạo được PDF. " + (kq.stderr or "")[-300:])


def dem_trang_pdf(pdf_path):
    try:
        du_lieu = Path(pdf_path).read_bytes()
        return len(re.findall(rb"/Type\s*/Page[^s]", du_lieu))
    except OSError:
        return 0


def huong_dan_tu_in(html_path, kho):
    in_ra(f"""
CHƯA TẠO ĐƯỢC PDF TỰ ĐỘNG (không có Playwright/Chrome/Edge, hoặc trình duyệt không chạy ẩn được).
File HTML đã sẵn sàng: {Path(html_path).resolve()}
Tự lưu PDF (1 phút):
  1. Mở file trên bằng Chrome hoặc Edge (chuột phải → Mở bằng).
  2. Bấm Ctrl+P (macOS: Cmd+P).
  3. Máy in / Đích: chọn 'Lưu dưới dạng PDF' (Save as PDF).
  4. Bấm 'Tùy chọn khác': Khổ giấy {kho} · Lề: Mặc định · BẬT 'Đồ họa nền' · TẮT 'Đầu trang và chân trang'.
  5. Bấm Lưu.
""")


# =============================================================== 5. CHƯƠNG TRÌNH CHÍNH
def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Biến Markdown thành ebook PDF có bìa thương hiệu.")
    p.add_argument("md", nargs="?", help="File Markdown của ebook")
    p.add_argument("--mau", action="store_true", help="In file Markdown mẫu rồi thoát")
    p.add_argument("--ra", help="Tên file PDF (mặc định: cùng tên file .md)")
    p.add_argument("--chi-html", action="store_true", help="Chỉ tạo file HTML, không tạo PDF")
    p.add_argument("--ten-sach", dest="ten_sach")
    p.add_argument("--phu-de", dest="phu_de")
    p.add_argument("--tac-gia", dest="tac_gia")
    p.add_argument("--nhan-bia", dest="nhan_bia")
    p.add_argument("--logo")
    p.add_argument("--mau-chinh", dest="mau_chinh", help="Màu chính, vd #1F2A44")
    p.add_argument("--mau-nhan", dest="mau_nhan", help="Màu nhấn, vd #F5B700")
    p.add_argument("--kho", choices=["A5", "A4", "a5", "a4"])
    p.add_argument("--kieu-chu", dest="kieu_chu", choices=["sans", "serif"],
                   help="sans = chữ không chân (mặc định) · serif = chữ có chân")
    p.add_argument("--lien-he", dest="lien_he")
    p.add_argument("--khong-muc-luc", action="store_true", help="Bỏ trang mục lục")
    p.add_argument("--cach", default="auto", choices=["auto", "playwright", "chrome"])
    p.add_argument("--chrome", help="Đường dẫn Chrome/Edge nếu không tự tìm thấy")
    a = p.parse_args()

    if a.mau:
        print(MARKDOWN_MAU)
        return
    if not a.md:
        p.print_help()
        sys.exit(1)
    if not Path(a.md).exists():
        sys.exit(f"Không thấy file: {a.md}")

    noi_dung_html, tk = dung_html(a.md, a)
    html_path = Path(a.md).with_suffix(".html")
    html_path.write_text(noi_dung_html, encoding="utf-8")
    in_ra(f"✓ Đã tạo HTML: {html_path}  ({tk['so_chuong']} chương, {tk['so_cta']} hộp CTA, khổ {tk['kho']})")
    for c in tk["canh_bao"]:
        in_ra(f"  ⚠ {c}")
    if tk["so_cta"] < 3:
        in_ra("  ⚠ Ebook nên có 3–5 hộp CTA (cú pháp: > [!CTA] Tiêu đề).")
    elif tk["so_cta"] > 5:
        in_ra("  ⚠ Hơn 5 hộp CTA có thể khiến người đọc thấy bị bán hàng quá nhiều.")
    if a.chi_html:
        return

    pdf_path = Path(a.ra) if a.ra else Path(a.md).with_suffix(".pdf")
    chan_font = not mang_tai_duoc_font()
    if chan_font:
        in_ra("  Lưu ý: không tải được Google Fonts → dùng font có sẵn trên máy (vẫn đủ dấu tiếng Việt).")

    ds = tim_trinh_duyet(a.chrome)
    loi = []
    cach_dung = None
    if a.cach in ("auto", "playwright"):
        try:
            pdf_playwright(html_path, pdf_path, chan_font, ds)
            cach_dung = "Playwright"
        except ImportError:
            loi.append("chưa cài Playwright")
        except Exception as e:
            loi.append(f"Playwright lỗi: {str(e)[:200]}")
    if cach_dung is None and a.cach in ("auto", "chrome"):
        if not ds:
            loi.append("không tìm thấy Chrome/Edge")
        for tb in ds:
            try:
                pdf_chrome(tb, html_path, pdf_path, chan_font)
                cach_dung = f"trình duyệt chạy ẩn ({Path(tb).name})"
                break
            except Exception as e:
                loi.append(str(e)[:200])
                in_ra(f"  ({e} — thử cách khác)")
    if cach_dung is None:
        in_ra("  Không tạo được PDF: " + "; ".join(loi))
        huong_dan_tu_in(html_path, tk["kho"])
        sys.exit(2)

    kb = Path(pdf_path).stat().st_size // 1024
    in_ra(f"✓ Đã tạo PDF: {pdf_path} — {dem_trang_pdf(pdf_path)} trang, {kb} KB — bằng {cach_dung}")


if __name__ == "__main__":
    main()
