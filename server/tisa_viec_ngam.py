"""tisa_viec_ngam.py - Thẻ "đang chạy ngầm" nói rõ việc gì và đang tới đâu (Bộ TISA V3.55, 24/11/2026).

Chuyện thật 24/11: thẻ chỉ hiện đường dẫn dài của lệnh ("/opt/homebrew/Cellar/python@3.11/.../Python -u up_drive.py"), không có tên dễ hiểu
và không có tiến độ, nên một việc đang tải 40 GB lên Drive chạy rất đều vẫn trông như bị treo. Mô-đun này bổ sung hai thứ cho mỗi việc nền:

  ten      tên ngắn: "up_drive.py · dua video anh len drive" (tên tệp lệnh + tên thư mục việc đang làm). Không nhận ra được tệp lệnh thì giữ
           nguyên mô tả cũ, không bịa.
  tien_do  dòng cuối của tệp nhật ký mà việc đó đang ghi (dò bằng lsof trên đầu ra chuẩn của nhóm tiến trình, hoặc tệp .log mới nhất trong
           thư mục làm việc), kèm giờ ghi lần cuối để thẻ nói "ghi 3 giây trước" hay "ghi 25 phút trước".

Chỉ ĐỌC, không ghi gì, không gọi mạng. Hỏng chỗ nào cũng trả rỗng: đây là chữ để đọc cho dễ, không phải điều kiện theo dõi. Tắt bằng
TISA_VIEC_NGAM=0. Kết quả nhớ 10 giây mỗi việc để thẻ hỏi liên tục không làm máy chủ chạy lsof liên tục.
"""
from __future__ import annotations

import os
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

TTL = 10.0
DOC_CUOI = 4096
TRAN_DONG = 140
_KHOA = threading.Lock()
_NHO: Dict[str, Tuple[float, dict]] = {}

_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07")
_SCRIPT = re.compile(r"\.(py|js|mjs|cjs|ts|mts|sh|rb|pl)$", re.I)
_VO = re.compile(r"^(python[0-9.]*|node|bash|sh|zsh|nohup|caffeinate|env|time|timeout|sudo|uv|npx|tsx|ts-node|bun|deno)$", re.I)
_NGAY = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def ten_tep_lenh(mo_ta: str) -> str:
    """Tên tệp lệnh trong một dòng lệnh ("... Python -u up_drive.py" -> "up_drive.py"). Không thấy thì trả rỗng."""
    toks = str(mo_ta or "").replace('"', " ").replace("'", " ").split()
    for tok in toks:
        if tok.startswith("-"):
            continue
        base = tok.rstrip("/").rsplit("/", 1)[-1]
        if _SCRIPT.search(base) and not _VO.match(base):
            return base[:60]
    return ""


def ten_thu_muc(duong: str, goc: str = "") -> str:
    """"…/2026-11-24-dua-video-anh-len-drive" -> "dua video anh len drive". Thư mục gốc bộ não hay rỗng thì trả rỗng."""
    d = str(duong or "").rstrip("/")
    if not d or (goc and os.path.normpath(d) == os.path.normpath(goc)):
        return ""
    ten = _NGAY.sub("", d.rsplit("/", 1)[-1])
    ten = re.sub(r"[-_]+", " ", ten).strip()
    return ten[:50]


def dat_ten(mo_ta: str, cwd_that: str = "", goc: str = "") -> str:
    """Tên dễ hiểu, hoặc rỗng nếu không có gì hay hơn mô tả cũ."""
    script = ten_tep_lenh(mo_ta)
    if not script:
        return ""
    tm = ten_thu_muc(cwd_that, goc)
    return f"{script} · {tm}" if tm else script


def lam_sach_dong(raw: bytes) -> str:
    """Dòng cuối có chữ của nhật ký. Thanh tiến độ ghi đè bằng \\r thì lấy đoạn sau cùng; bỏ mã màu và ký tự điều khiển."""
    txt = raw.decode("utf-8", "replace")
    for dong in reversed(txt.splitlines() or [txt]):
        dong = _ANSI.sub("", dong.rsplit("\r", 1)[-1] if "\r" in dong else dong)
        dong = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", dong).strip()
        if dong:
            return (dong[:TRAN_DONG - 3] + "...") if len(dong) > TRAN_DONG else dong
    return ""


def doc_dong_cuoi(duong: str) -> Tuple[str, float]:
    """(dòng cuối, giờ ghi lần cuối) của một tệp văn bản. Hỏng thì ("", 0)."""
    try:
        p = Path(duong)
        st = p.stat()
        if not p.is_file():
            return "", 0.0
        with p.open("rb") as f:
            f.seek(max(0, st.st_size - DOC_CUOI))
            return lam_sach_dong(f.read()), float(st.st_mtime)
    except Exception:  # noqa: BLE001
        return "", 0.0


def _lsof(pids: List[int]) -> Tuple[str, List[str]]:
    """(thư mục làm việc, các tệp thường mà đầu ra chuẩn đang ghi vào) của nhóm pid. Chỉ macOS/Linux có lsof."""
    if os.name == "nt" or not pids:
        return "", []
    try:
        r = subprocess.run(["lsof", "-a", "-p", ",".join(str(p) for p in pids[:12]), "-d", "cwd,1,2", "-Fpfn"],
                           capture_output=True, text=True, timeout=3)
    except Exception:  # noqa: BLE001
        return "", []
    cwd, logs, fd = "", [], ""
    for dong in r.stdout.splitlines():
        if not dong:
            continue
        k, v = dong[0], dong[1:]
        if k == "p":
            fd = ""
        elif k == "f":
            fd = v
        elif k == "n" and v.startswith("/") and not v.startswith("/dev/"):
            if fd == "cwd":
                cwd = cwd or v
            elif fd in ("1", "2") and v not in logs:
                logs.append(v)
    return cwd, logs


def _tep_log_moi(thu_muc: str, tran_giay: float = 900.0) -> str:
    """Không dò được đầu ra: lấy tệp .log mới nhất trong thư mục làm việc, nếu vừa được ghi."""
    try:
        now = time.time()
        ds = [p for p in Path(thu_muc).glob("*.log") if p.is_file() and now - p.stat().st_mtime < tran_giay]
        return str(max(ds, key=lambda p: p.stat().st_mtime)) if ds else ""
    except Exception:  # noqa: BLE001
        return ""


def _phan_tich(job: dict) -> dict:
    out = {"ten": "", "tien_do": "", "ghi_luc": 0.0}
    try:
        import tien_trinh_nen
        tv = tien_trinh_nen._thanh_vien(int(job.get("pgid") or 0))
        cwd, logs = _lsof([m["pid"] for m in tv if m.get("pid")])
        cwd = cwd or next((m.get("cwd") for m in tv if m.get("cwd")), "") or ""
        out["ten"] = dat_ten(str(job.get("mo_ta") or ""), cwd, str(job.get("brain_root") or ""))
        ung = []
        for lg in logs:
            dong, mt = doc_dong_cuoi(lg)
            if mt:
                ung.append((mt, dong))
        if not ung and cwd:
            lg = _tep_log_moi(cwd)
            if lg:
                dong, mt = doc_dong_cuoi(lg)
                if mt:
                    ung.append((mt, dong))
        if ung:
            mt, dong = max(ung, key=lambda x: x[0])
            out["tien_do"], out["ghi_luc"] = dong, mt
    except Exception:  # noqa: BLE001
        pass
    return out


def bo_sung(job: dict) -> dict:
    """{ten, tien_do, ghi_luc} cho một việc nền (khoá `id`, `pgid`, `mo_ta`, `brain_root` của tien_trinh_nen). Nhớ TTL giây."""
    if os.getenv("TISA_VIEC_NGAM") == "0":
        return {"ten": "", "tien_do": "", "ghi_luc": 0.0}
    key = str(job.get("id") or job.get("pgid") or "")
    now = time.monotonic()
    with _KHOA:
        hit = _NHO.get(key)
        if hit and now - hit[0] < TTL:
            return dict(hit[1])
    kq = _phan_tich(job)
    with _KHOA:
        _NHO[key] = (now, kq)
        if len(_NHO) > 64:
            for k in sorted(_NHO, key=lambda k: _NHO[k][0])[:32]:
                _NHO.pop(k, None)
    return dict(kq)
