"""Thanh báo cáo tình hình khi giao việc bằng giọng nói (V2.91).

Chủ báo: giao việc xong thì màn hình không cho biết AI đang làm hay đang làm tới đâu, có triển
khai hay không. Sổ việc của phiên Live (`jobs`) vốn đã giữ câu trạng thái mới nhất của bộ não;
module này biến nó thành bản tóm tắt đưa ra giao diện: việc gì, bao lâu, giai đoạn nào, đã chạy
những bước nào, đã thật sự ghi/sửa/chạy lệnh chưa.

Chỉ dùng số liệu thật từ bộ não (các câu "⚙ Đang dùng công cụ: X"), không đoán tiến độ phần trăm.
Không đụng mạng, không đọc ghi đĩa: thuần hàm, thử được ngay."""
from __future__ import annotations

import re
import time
from typing import Any, Dict, Iterable, List, Tuple

try:  # noqa: SIM105
    import localefmt
    _chu = localefmt.chu
except Exception:  # pragma: no cover
    def _chu(vi: str, en: str) -> str:
        return vi

# Công cụ làm thay đổi thứ gì đó (ghi file, chạy lệnh, gửi, tạo...) => "triển khai".
_LAM = ("write", "edit", "bash", "notebook", "create", "update", "delete", "send", "post", "publish",
        "push", "exec", "upload", "save", "deploy", "schedule", "move", "apply", "patch", "commit",
        "run_", "shell", "terminal", "remove", "rename", "insert")
# Công cụ chỉ đọc/tìm => "tìm hiểu".
_DOC = ("read", "grep", "glob", "search", "fetch", "list", "get_", "find", "view", "query", "web",
        "ls", "cat", "open", "show", "lookup", "browse", "screenshot", "snapshot")

_NHAN = {
    "write": ("Ghi file", "Writing a file"), "edit": ("Sửa file", "Editing a file"),
    "multiedit": ("Sửa file", "Editing a file"), "bash": ("Chạy lệnh", "Running a command"),
    "read": ("Đọc file", "Reading a file"), "grep": ("Tìm trong file", "Searching files"),
    "glob": ("Tìm file", "Finding files"), "websearch": ("Tìm trên mạng", "Searching the web"),
    "webfetch": ("Đọc trang web", "Reading a web page"), "task": ("Giao cho trợ lý phụ", "Delegating"),
    "agent": ("Giao cho trợ lý phụ", "Delegating"), "notebookedit": ("Sửa sổ tay", "Editing a notebook"),
    "todowrite": ("Lập danh sách việc", "Planning steps"),
}

_MAX_BUOC = 12   # giữ vài bước gần nhất để vẽ, không giữ cả lịch sử


def _ten_cong_cu(raw: str) -> str:
    t = re.sub(r"\s+", " ", str(raw or "")).strip().rstrip(".… ")
    t = re.sub(r"^mcp__[^_]+(?:_[^_]+)*?__", "", t)   # mcp__server__tool -> tool
    return t[:60]


def _loai(ten: str) -> str:
    low = ten.lower()
    if any(k in low for k in _LAM):
        return "lam"
    if any(k in low for k in _DOC):
        return "doc"
    return "khac"


def _nhan_dep(ten: str) -> str:
    key = re.sub(r"[^a-z]", "", ten.lower())
    if key in _NHAN:
        vi, en = _NHAN[key]
        return _chu(vi, en)
    return ten.replace("_", " ").replace("-", " ")[:40]


def ghi(job: Dict[str, Any], step: Any) -> None:
    """Ghi một câu trạng thái của bộ não vào việc: đếm bước, nhớ vài bước gần nhất, đánh dấu đang soạn.

    Bộ não chính nói nhiều kiểu: "⚙ Đang gọi: Read", "⚙ Đang dùng công cụ: Write", "⚙ Đang gọi công cụ: X", "⚙ Lịch: ...",
    "✓ Nhận kết quả - đang phân tích…", "✍ Đang soạn câu trả lời…", "↻ ..." (nối lại), "⚡ Đường tắt…". Mọi dòng bắt đầu bằng ⚙ là một lần gọi công cụ."""
    s = str(step or "").strip()
    if not s:
        return
    job.setdefault("buoc", [])
    job.setdefault("so_buoc", 0)
    job.setdefault("so_lam", 0)
    job["luc"] = time.monotonic()
    low = s.lower()
    if s.startswith("⚙") or (("công cụ" in low or "tool" in low) and ":" in s):
        ten = _ten_cong_cu(s.split(":", 1)[1] if ":" in s else s.lstrip("⚙ "))
        if not ten:
            return
        loai = _loai(ten)
        job["soan"] = False
        job["phan_tich"] = False
        job["so_buoc"] += 1
        if loai == "lam":
            job["so_lam"] += 1
        job["buoc"].append({"ten": _nhan_dep(ten), "loai": loai})
        del job["buoc"][:-_MAX_BUOC]
        job["gan_nhat"] = _chu("Đang " + _nhan_dep(ten).lower(), "Now: " + _nhan_dep(ten))
    elif s.startswith("✓") or "nhận kết quả" in low:
        job["phan_tich"] = True
        job["gan_nhat"] = _chu("Đang phân tích kết quả vừa nhận", "Analysing the result just received")
    elif "soạn" in low or "composing" in low or "drafting" in low:
        job["soan"] = True
        job["gan_nhat"] = _chu("Đang soạn kết quả", "Writing up the result")
    elif s.startswith("↻"):
        job["thu_lai"] = s.lstrip("↻ ").strip()[:80]
        job["gan_nhat"] = _chu("Đang nối lại phiên làm việc", "Reconnecting the session")
    elif s.startswith("⚡"):
        job["gan_nhat"] = _chu("Đang đi đường tắt", "Taking a shortcut")
    else:
        job["gan_nhat"] = re.sub(r"\s+", " ", s.lstrip("⚙✓✍↻⚡ ").strip())[:80]


def giai_doan(job: Dict[str, Any]) -> str:
    """nhan = mới nhận lệnh, chưa có bước nào | doc = đang tìm hiểu | lam = đang triển khai | soan = soạn kết quả."""
    if job.get("soan"):
        return "soan"
    if not job.get("so_buoc"):
        return "nhan"
    if job.get("so_lam"):
        return "lam"
    if any(b.get("loai") == "doc" for b in job.get("buoc", [])):
        return "doc"
    return "lam"   # có bước công cụ lạ: coi là đang xử lý, không nhận bừa là chỉ đọc


_TEN_GD = {
    "nhan": ("Đã nhận lệnh, bộ não đang suy nghĩ", "Got it, the brain is thinking"),
    "doc": ("Đang tìm hiểu, chưa ghi gì", "Researching, nothing changed yet"),
    "lam": ("Đang triển khai", "Carrying it out"),
    "soan": ("Đang soạn kết quả", "Writing up the result"),
}


def _rut_gon(text: str, n: int = 90) -> str:
    t = re.sub(r"\s+", " ", str(text or "")).strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def tom_tat(jobs: Iterable[Tuple[Any, Dict[str, Any]]], now: float) -> List[Dict[str, Any]]:
    """Danh sách việc đang chạy cho giao diện. `jobs`: (số thứ tự, {request, started, step, ...})."""
    ra: List[Dict[str, Any]] = []
    for jid, j in sorted(list(jobs), key=lambda kv: kv[1].get("started", 0.0)):
        gd = giai_doan(j)
        giay = max(0, int(now - j.get("started", now)))
        vi, en = _TEN_GD[gd]
        canh_bao = ""
        if gd == "nhan" and giay >= 40:
            canh_bao = _chu("Đã hơn %d giây bộ não chưa báo bước nào. Có thể đang suy nghĩ lâu; nếu quá 2 phút anh nói \"em xong chưa\" để hỏi tiến độ." % giay,
                            "Over %d seconds with no report from the brain. It may be thinking; after 2 minutes ask for a status." % giay)
        elif gd == "nhan" and giay >= 5:
            canh_bao = ""
        elif j.get("thu_lai"):
            canh_bao = _chu("Đang thử lại: ", "Retrying: ") + str(j["thu_lai"])
        ra.append({
            "id": jid,
            "ten": _rut_gon(j.get("request", "")),
            "giay": giay,
            "giai_doan": gd,
            "nhan": _chu(vi, en),
            "so_buoc": int(j.get("so_buoc", 0)),
            "so_lam": int(j.get("so_lam", 0)),
            "buoc": [dict(b) for b in j.get("buoc", [])][-6:],
            "canh_bao": canh_bao,
            "gan_nhat": str(j.get("gan_nhat") or ""),
            "im_giay": max(0, int(now - j.get("luc", j.get("started", now)))),
            "phan_tich": bool(j.get("phan_tich")),
        })
    return ra
