"""tisa_tim_tep.py - tìm tệp theo TÊN trong bộ não khi đường dẫn trong chat không khớp (V2.85).

AI hay viết tên tệp trần (ví dụ `01-Nguyen-Truong-Giang.jpg`) hoặc thiếu thư mục con, nên bấm vào link tệp trong chat báo lỗi
không thấy tệp. Hàm này dò trong gốc bộ não, ưu tiên tệp khớp phần thư mục còn lại của đường dẫn, rồi tới tệp mới nhất.
Chỉ ĐỌC, chỉ trả tệp nằm trong gốc bộ não, có giới hạn thời gian và số mục quét, nhớ kết quả 60 giây.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

BO_QUA = {"node_modules", ".git", ".obsidian", "__pycache__", ".venv", "venv", ".cache", ".trash", "connector-home", ".next", "dist-electron"}
_NHO: dict = {}
MAX_MUC, MAX_GIAY = 80000, 4.0


def tim(goc: Path, rel: str):
    rel = (rel or "").replace("\\", "/").strip("/")
    ten = rel.rsplit("/", 1)[-1]
    if not ten or "." not in ten or ten.startswith("."):
        return None
    goc = Path(goc).resolve()
    khoa = (str(goc), rel)
    cu = _NHO.get(khoa)
    if cu and time.time() - cu[0] < 60:
        return cu[1]
    phan_thu_muc = [x for x in rel.split("/")[:-1] if x and x not in (".", "..")]
    bat_dau, dem, khop = time.time(), 0, []
    for thu_muc, ds, tep in os.walk(goc):
        ds[:] = [d for d in ds if d not in BO_QUA and not d.startswith(".")]
        dem += len(tep) + len(ds)
        if ten in tep:
            khop.append(Path(thu_muc) / ten)
        if dem > MAX_MUC or time.time() - bat_dau > MAX_GIAY:
            break
    kq = None
    if khop:
        def diem(p: Path):
            cha = [x.lower() for x in p.parent.relative_to(goc).parts]
            trung = sum(1 for x in phan_thu_muc if x.lower() in cha)
            try:
                m = p.stat().st_mtime
            except OSError:
                m = 0
            return (trung, m)
        kq = max(khop, key=diem)
        try:
            kq = kq.resolve()
            if kq != goc and goc not in kq.parents:
                kq = None
        except OSError:
            kq = None
    _NHO[khoa] = (time.time(), kq)
    if len(_NHO) > 500:
        _NHO.clear()
    return kq
