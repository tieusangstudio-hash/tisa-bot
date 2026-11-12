"""tisa_quang_cao_bo_nao.py - đọc Bộ Não của chính doanh nghiệp để AI viết và vẽ ĐÚNG sản phẩm (V2.78).

Khi anh bấm tạo bài, ảnh hay video quảng cáo, trang không để AI đoán sản phẩm từ vài chữ anh gõ. Trước hết trang đọc bộ não trên máy này:
quy tắc chung (00-DOC-TRUOC), hồ sơ doanh nghiệp (01-ho-so: sản phẩm, khách hàng, thương hiệu, mục tiêu và quy tắc), rồi các trang kiến thức
(02-kien-thuc, wiki) KHỚP với sản phẩm anh đang quảng cáo. Kết quả là một đoạn chữ gọn, đưa kèm cho AI hoặc cho cộng sự.

Trang hồ sơ còn là mẫu trống (trang-thai: chua-dien) thì bỏ qua và báo thiếu, để trang nhắc anh điền thay vì để AI bịa.
Chỉ ĐỌC, không sửa gì trong bộ não.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

THU_MUC_KIEN_THUC = ("02-kien-thuc", "wiki")
UU_TIEN_HO_SO = ("san-pham", "thuong-hieu", "khach-hang", "doanh-nghiep", "muc-tieu")
MAX_QUET = 500
MAX_BYTE = 250_000


def _kd(s) -> str:
    x = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", x)


def vault_mac_dinh() -> Path | None:
    try:
        import image_gen
        p = Path(image_gen._default_vault())
        return p if p.is_dir() else None
    except Exception:  # noqa: BLE001
        return None


def _doc(p: Path, toi_da: int):
    """(nội dung đã làm sạch, là mẫu trống?)."""
    try:
        if p.stat().st_size > MAX_BYTE:
            return "", False
        t = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return "", False
    mau = bool(re.search(r"^trang-thai:\s*chua-dien\s*$", t[:600], re.M))
    t = re.sub(r"\A---.*?\n---\s*", "", t, count=1, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"^\|[\s|:-]*\|\s*$", "", t, flags=re.M)      # dòng kẻ bảng
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:toi_da], mau


def _tu_khoa(chu_de: str) -> list:
    ds = []
    for w in re.findall(r"[a-z0-9]{3,}", _kd(chu_de)):
        if w not in ds and w not in ("cho", "cua", "cac", "mot", "nhung", "khong", "duoc", "voi", "the", "and"):
            ds.append(w)
    return ds[:14]


def doc_bo_nao(chu_de: str = "", toi_da: int = 6000, vault: Path | None = None) -> dict:
    """{text, da_doc:[đường dẫn], thieu:[tên trang còn trống], co: bool}. text rỗng nếu bộ não chưa có gì dùng được."""
    v = vault or vault_mac_dinh()
    ra = {"text": "", "da_doc": [], "thieu": [], "co": False}
    if not v or not v.is_dir():
        return ra
    khuc, dung = [], 0

    def them(nhan: str, rel: str, nd: str):
        nonlocal dung
        if not nd or dung >= toi_da:
            return
        nd = nd[:max(0, toi_da - dung)]
        khuc.append("### %s (%s)\n%s" % (nhan, rel, nd))
        ra["da_doc"].append(rel)
        dung += len(nd) + len(nhan) + len(rel) + 10

    nd, _ = _doc(v / "00-DOC-TRUOC.md", 800)
    them("Quy tắc chung của doanh nghiệp", "00-DOC-TRUOC.md", nd)
    hs = v / "01-ho-so"
    if hs.is_dir():
        files = sorted((p for p in hs.glob("*.md") if p.is_file()), key=lambda p: next((i for i, k in enumerate(UU_TIEN_HO_SO) if k in p.name), 99))
        for p in files:
            nd, mau = _doc(p, 1300)
            ten = p.stem
            if mau or len(nd) < 80:
                ra["thieu"].append(ten)
                continue
            them(ten.replace("-", " ").strip(), "01-ho-so/" + p.name, nd)
    tk = _tu_khoa(chu_de)
    if tk and dung < toi_da:
        ung = []
        dem = 0
        for ten in THU_MUC_KIEN_THUC:
            goc = v / ten
            if not goc.is_dir():
                continue
            for p in goc.rglob("*.md"):
                dem += 1
                if dem > MAX_QUET:
                    break
                if not p.is_file():
                    continue
                nd, mau = _doc(p, 1600)
                if mau or len(nd) < 120:
                    continue
                van, ten_k = _kd(nd[:6000]), _kd(p.stem)
                diem = sum(van.count(k) for k in tk) + 6 * sum(1 for k in tk if k in ten_k)
                if diem > 0:
                    ung.append((diem, p, nd))
        ung.sort(key=lambda x: -x[0])
        for diem, p, nd in ung[:3]:
            them("Kiến thức liên quan: " + p.stem, str(p.relative_to(v)).replace("\\", "/"), nd[:1200])
    ra["text"] = "\n\n".join(khuc)
    ra["co"] = any(x != "00-DOC-TRUOC.md" for x in ra["da_doc"])
    return ra
