"""tisa_canh_gac_luot.py - Khi người dùng nhắn thêm mà lượt đang chạy KHÔNG đọc (đứng im), báo tình hình THẬT thay vì im lặng (V3.53, chủ báo 23/11/2026).

Ca thật: AI chờ video dựng xong bằng lệnh `tail -n0 -F r21b.log` (chỉ báo dòng MỚI) trong khi video đã dựng xong từ trước, nên lệnh chờ mãi.
Tin nhắn của chủ ("sao im rồi, làm chưa?") nằm trong hộp thư của lượt vì lượt chỉ đọc sau mỗi bước làm; không có bước nào tới. Chủ thấy chat im ru, không biết tới đâu.

Cách làm: sau khi tin nằm quá 90 giây chưa được đọc, máy chủ nhìn cây tiến trình con (ps) rồi tự nhắn một câu nói rõ: lượt đã chạy bao lâu, có việc nào đang tốn CPU không,
đang chờ lệnh gì, và cách thoát (Dừng rồi nhắn "làm tiếp"). KHÔNG tự ngắt lượt: theo luật của repo, cắt một lượt đang chạy tốt tệ hơn để nó chạy lâu (xem tran_watchdog).
Chỉ đọc `ps`, không ghi gì, lỗi thì trả rỗng. Không dùng được trên Windows (không có ps): khi đó câu báo chỉ nói thời gian.
"""
from __future__ import annotations

import os
import re
import subprocess

_CHO = re.compile(r"(^|/)tail\s+(-\S*\s+)*-[a-zA-Z0-9]*[fF]|(^|/)sleep\s|(^|\s)until\s|(^|\s)inotifywait|(^|\s)fswatch", re.I)


def _giay(etime: str) -> int:
    """`[[dd-]hh:]mm:ss` của ps -> giây."""
    try:
        d = 0
        if "-" in etime:
            ds, etime = etime.split("-", 1)
            d = int(ds)
        p = [int(x) for x in etime.split(":")]
        while len(p) < 3:
            p.insert(0, 0)
        return d * 86400 + p[0] * 3600 + p[1] * 60 + p[2]
    except (ValueError, TypeError):
        return 10 ** 9


def quan_sat(goc_pid: int, tuoi_luot_s: float) -> dict:
    """Các tiến trình con (mọi cấp) của máy chủ sinh ra từ lúc lượt bắt đầu: {co: bool, ban: [(cpu, lenh)], cho: [lenh], tong_cpu: float}."""
    kq = {"co": False, "ban": [], "cho": [], "tong_cpu": 0.0}
    if os.name == "nt":
        return kq
    try:
        out = subprocess.run(["ps", "-axo", "pid=,ppid=,pcpu=,etime=,command="], capture_output=True, text=True, timeout=5).stdout
    except Exception:  # noqa: BLE001
        return kq
    rows, con = {}, {}
    for ln in out.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)\s+([\d.,]+)\s+(\S+)\s+(.*)$", ln)
        if not m:
            continue
        pid, ppid = int(m.group(1)), int(m.group(2))
        try:
            cpu = float(m.group(3).replace(",", "."))
        except ValueError:
            cpu = 0.0
        rows[pid] = (ppid, cpu, _giay(m.group(4)), m.group(5).strip())
        con.setdefault(ppid, []).append(pid)
    hang, thay = list(con.get(goc_pid, [])), set()
    while hang:
        p = hang.pop()
        if p in thay:
            continue
        thay.add(p)
        hang.extend(con.get(p, []))
    gioi_han = tuoi_luot_s + 15
    for p in thay:
        ppid, cpu, tuoi, lenh = rows[p]
        if tuoi > gioi_han or lenh.startswith("ps ") or " ps -axo" in lenh:
            continue          # tiến trình có từ trước lượt (MCP, tunnel...) không phải việc của lượt này
        kq["co"] = True
        kq["tong_cpu"] += cpu
        if cpu >= 3.0:
            kq["ban"].append((cpu, lenh))
        if _CHO.search(lenh):
            kq["cho"].append(lenh)
    kq["ban"].sort(reverse=True)
    return kq


def _ngan(lenh: str, n: int = 110) -> str:
    lenh = re.sub(r"\s+", " ", lenh or "").strip()
    return lenh if len(lenh) <= n else lenh[: n - 1] + "…"


def _phut(s: float) -> str:
    s = int(s)
    return f"{s // 60} phút {s % 60:02d} giây" if s >= 60 else f"{s} giây"


def cau_bao(tuoi_s: float, im_s: float, obs: dict, lan: int = 1, som: bool = False, viec=None) -> str:
    """Câu báo cho khung chat. `tuoi_s`: lượt đã chạy; `im_s`: bao lâu không có tín hiệu mới từ lượt.
    `som`: anh đang HỎI TIẾN ĐỘ (báo sớm, không đợi AI); `viec`: (công cụ gần nhất, cách đây bao nhiêu giây)."""
    gan = f" Việc gần nhất nó làm: `{viec[0]}` ({_phut(viec[1])} trước)." if viec and viec[0] else ""
    if som:
        dau = (f"Anh hỏi tiến độ nên em báo ngay, không đợi AI (nó chưa đọc tin của anh). Lượt này đã chạy {_phut(tuoi_s)}, "
               f"{_phut(im_s)} nay không có tín hiệu mới.{gan}")
        if im_s < 60 and obs.get("ban"):
            cpu, lenh = obs["ban"][0]
            return dau + f"\n\nNó đang làm việc: `{_ngan(lenh)}` (CPU {cpu:.0f}%). Xong bước này nó sẽ đọc và trả lời anh."
    else:
        dau = f"Em nhận được tin của anh nhưng lượt đang chạy chưa đọc được (lượt này đã chạy {_phut(tuoi_s)}, đã {_phut(im_s)} không có tín hiệu mới).{gan}"
    if obs.get("ban"):
        cpu, lenh = obs["ban"][0]
        return (dau + f"\n\nNó đang bận thật: `{_ngan(lenh)}` đang chạy (CPU {cpu:.0f}%). Tin của anh sẽ được đọc ngay khi xong bước này, "
                "anh không cần nhắn lại. Nếu anh không muốn chờ, bấm nút **Dừng việc đang làm, làm tin này ngay** dưới tin của anh.")
    if obs.get("cho"):
        return (dau + f"\n\nKhông có việc nào đang tính toán. Nó đang đứng chờ lệnh `{_ngan(obs['cho'][0])}`: lệnh kiểu này chỉ báo khi có dòng MỚI nên nếu việc kia "
                "đã xong từ trước thì sẽ chờ mãi. Anh bấm nút **Dừng việc đang làm, làm tin này ngay** dưới tin của anh là em làm tiếp phần còn lại (cảnh nào đã dựng xong sẽ được bỏ qua, không mất công).")
    if obs.get("co"):
        return (dau + "\n\nKhông có tiến trình nào đang tính toán nhiều. Có thể nó đang suy nghĩ lâu hoặc đang chờ một thứ chưa tới. Chờ thêm vài phút; "
                "nếu vẫn im, anh bấm nút **Dừng việc đang làm, làm tin này ngay** dưới tin của anh.")
    return (dau + "\n\nKhông thấy tiến trình nào đang chạy cho lượt này. Nếu thêm vài phút nữa vẫn im, anh bấm nút **Dừng việc đang làm, làm tin này ngay** dưới tin của anh.") if lan <= 1 else (
        dau + "\n\nVẫn chưa có gì mới. Anh bấm nút **Dừng việc đang làm, làm tin này ngay** dưới tin của anh để em làm tiếp ngay.")
