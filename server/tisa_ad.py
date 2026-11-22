"""tisa_ad.py - (V3.45, chủ duyệt 22/11) Điều khiển máy bằng CÂY TRỢ NĂNG qua agent-desktop (Vercel Labs, Apache-2.0, vendor/agent-desktop).

Vì sao: mỗi ảnh chụp màn hình đưa cho AI tốn khoảng 1.200 token. Tìm đúng một nút theo tên (`find`) chỉ tốn khoảng 150 token và trả mã
nút để bấm thẳng (không đoán toạ độ, không di chuột thật của anh, không giành cửa sổ). Đo trên máy chủ 22/11: tìm nút ~150 token,
đọc gọn một cửa sổ ~2.000 token, đọc cả cửa sổ nhiều chữ (Facebook, thư mục nhiều tệp) 5.000-6.000 token (đắt hơn ảnh), nên thứ tự
nên dùng là: tìm theo tên -> đọc gọn một vùng -> ảnh chụp sau cùng.

Mô-đun này chỉ gọi tệp chạy và RÚT GỌN kết quả thành dòng chữ ngắn cho AI. Mọi chốt an toàn (ứng dụng mật khẩu/ngân hàng, mức duyệt,
Dừng AI, nhật ký) nằm ở tisa_desktop.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import threading
import time
from pathlib import Path

PHIEN_BAN = "1.3.1"
_GOC = Path(__file__).resolve().parent.parent / "vendor" / "agent-desktop"
_STATE = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent) / "agent-desktop"
TOI_DA_DONG = 220          # số dòng tối đa của một lần đọc cây (quá thì cắt và chỉ cách đọc từng vùng)
TOI_DA_KY_TU = 9000
_khoa = threading.Lock()
_ANH_XA: dict = {}         # snapshot_id -> {"app", "cua_so", "luc"} (biết ứng dụng nào khi bấm theo mã, để kiểm an toàn)
_GAN_NHAT: dict = {}       # mã ô chat -> snapshot_id gần nhất (AI chỉ cần đưa "e8")


def khoa_may() -> str:
    m = platform.machine().lower()
    arch = "arm64" if m in ("arm64", "aarch64") else "x64"
    if sys.platform == "darwin":
        return "darwin-" + arch
    if os.name == "nt":
        return "win32-" + arch
    return ""


def duong_dan() -> Path | None:
    """Tệp chạy agent-desktop của máy này (đi kèm TISA BOT). TISA_AD_BIN để thử bản khác."""
    if os.getenv("TISA_AD_BIN"):
        p = Path(os.environ["TISA_AD_BIN"])
        return p if p.is_file() else None
    k = khoa_may()
    if not k:
        return None
    p = _GOC / k / ("agent-desktop.exe" if k.startswith("win32") else "agent-desktop")
    if not p.is_file():
        return None
    if os.name != "nt" and not os.access(p, os.X_OK):
        try:
            for f in p.parent.iterdir():
                if f.is_file() and not f.name.endswith((".md", ".txt")):
                    f.chmod(0o755)
        except OSError:
            return None
    return p


def co_san() -> bool:
    return duong_dan() is not None


def chay(doi_so: list, timeout: float = 25, nhap: str | None = None) -> dict:
    """Chạy một lệnh, trả envelope JSON ({"ok":..., "data"|"error"}). Không bao giờ ném lỗi."""
    p = duong_dan()
    if p is None:
        return {"ok": False, "error": {"code": "KHONG_CO", "message": "Máy này chưa có agent-desktop đi kèm TISA BOT (chỉ có cho macOS và Windows)."}}
    env = dict(os.environ)
    env["AGENT_DESKTOP_HOME"] = str(_STATE)          # ảnh chụp cây (có thể chứa nội dung riêng) nằm trong thư mục trạng thái TISA, không ở ~
    try:
        _STATE.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            _STATE.chmod(0o700)      # agent-desktop từ chối thư mục trạng thái mà người khác đọc được ("private file parent is accessible")
    except OSError:
        pass
    try:
        r = subprocess.run([str(p)] + [str(x) for x in doi_so], capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, input=nhap, env=env)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": {"code": "QUA_GIO", "message": "agent-desktop không trả lời sau %d giây." % timeout}}
    except OSError as e:
        return {"ok": False, "error": {"code": "KHONG_CHAY", "message": "Không chạy được agent-desktop: %s" % e}}
    out = (r.stdout or "").strip()
    for dong in reversed(out.splitlines()):
        dong = dong.strip()
        if dong.startswith("{"):
            try:
                return json.loads(dong)
            except ValueError:
                break
    return {"ok": False, "error": {"code": "KHONG_DOC_DUOC", "message": (r.stderr or out or "không có kết quả")[:300]}}


# ---------------------------------------------------------------- rút gọn cho AI
_BO_HANH_DONG = {"SetFocus", "RightClick", "ShowMenu", "Scroll"}
_TEN_HANH_DONG = {"Click": "bấm", "TypeText": "gõ", "SetValue": "đặt", "Select": "chọn", "Toggle": "bật/tắt", "Expand": "mở", "Collapse": "thu",
                  "Increment": "tăng", "Decrement": "giảm", "Check": "tích", "Uncheck": "bỏ tích"}


def _ma_ngan(ref: str) -> str:
    return str(ref or "").split(":")[-1] if ref else ""


def _mot_dong(n: dict) -> str:
    ten = str(n.get("name") or "").strip()
    mo_ta = str(n.get("description") or "").strip()
    gt = n.get("value")
    hd = [_TEN_HANH_DONG.get(x, x) for x in (n.get("available_actions") or []) if x not in _BO_HANH_DONG]
    st = [x for x in (n.get("states") or []) if x in ("checked", "selected", "disabled", "focused", "expanded")]
    phan = [n.get("role") or "?"]
    if ten:
        phan.append('"%s"' % ten[:90])
    if mo_ta and mo_ta != ten:
        phan.append("(%s)" % mo_ta[:60])
    if gt not in (None, "") and str(gt) != ten:
        phan.append("=%s" % str(gt)[:60])
    if st:
        phan.append("[%s]" % ",".join(st))
    if n.get("children_count"):
        phan.append("{%d con, đọc thêm: cay goc=%s}" % (n["children_count"], _ma_ngan(n.get("ref_id"))))
    if hd:
        phan.append("<%s>" % ",".join(hd[:4]))
    ma = _ma_ngan(n.get("ref_id"))
    return ("%s " % ma if ma else "") + " ".join(phan)


def cay_thanh_chu(d: dict) -> tuple[str, int]:
    """Cây snapshot -> các dòng thụt lề. Bỏ nhóm không tên không mã (đưa con lên). Trả (chữ, số dòng)."""
    dong: list = []
    bi_cat = [False]

    def di(n, sau):
        if len(dong) >= TOI_DA_DONG:
            bi_cat[0] = True
            return
        co_ich = bool(n.get("ref_id") or n.get("name") or n.get("value") not in (None, ""))
        if co_ich:
            dong.append(" " * min(sau, 12) + _mot_dong(n))
        for c in n.get("children") or []:
            di(c, sau + (1 if co_ich else 0))
    di((d.get("data") or {}).get("tree") or {}, 0)
    chu = "\n".join(dong)
    if len(chu) > TOI_DA_KY_TU:
        chu, bi_cat[0] = chu[:TOI_DA_KY_TU].rsplit("\n", 1)[0], True
    if bi_cat[0]:
        chu += "\n…(đã cắt bớt: đọc từng vùng bằng op=cay goc=<mã vùng>, hoặc tìm thẳng bằng op=tim ten=...)"
    return chu, len(dong)


def ghi_anh_xa(d: dict, chat: str = "") -> str:
    data = d.get("data") or {}
    sid = str(data.get("snapshot_id") or "")
    if sid:
        with _khoa:
            _ANH_XA[sid] = {"app": str(data.get("app") or ""), "cua_so": str(((data.get("window") or {}).get("title")) or (data.get("tree") or {}).get("name") or ""),
                            "luc": time.time()}
            if len(_ANH_XA) > 200:
                for k in sorted(_ANH_XA, key=lambda x: _ANH_XA[x]["luc"])[:50]:
                    _ANH_XA.pop(k, None)
            if chat is not None:
                _GAN_NHAT[chat] = sid
    return sid


def ma_day_du(ma: str, chat: str = "") -> str:
    """"e8" -> "@<snapshot gần nhất của ô chat>:e8"; mã đầy đủ thì giữ nguyên."""
    ma = str(ma or "").strip()
    if not ma:
        return ""
    if ma.startswith("@") and ":" in ma:
        return ma
    if ":" in ma:
        return "@" + ma.lstrip("@")
    sid = _GAN_NHAT.get(chat or "")
    return ("@%s:%s" % (sid, ma.lstrip("@"))) if sid else ""


def ung_dung_cua_ma(ma_du: str) -> dict:
    sid = ma_du.split(":", 1)[0].lstrip("@") if ma_du else ""
    return dict(_ANH_XA.get(sid) or {})


def loi_ngan(d: dict) -> str:
    e = d.get("error") or {}
    ma = str(e.get("code") or "LOI")
    goi_y = {"STALE_REF": "Giao diện đã đổi: tìm lại (op=tim) rồi bấm mã mới.",
             "SNAPSHOT_NOT_FOUND": "Mã cũ hoặc của lần đọc khác: tìm lại (op=tim) rồi dùng mã mới.",
             "AMBIGUOUS_TARGET": "Ứng dụng có nhiều cửa sổ: thêm cua_so=<mã cửa sổ> (xem op=cua_so).",
             "WINDOW_NOT_FOUND": "Ứng dụng chưa có cửa sổ nào đang mở (hoặc đang thu nhỏ).",
             "APP_NOT_FOUND": "Ứng dụng chưa mở. Mở bằng tisa_desktop_do op=open_app.",
             "APP_UNRESPONSIVE": "Ứng dụng này không trả lời cây trợ năng: dùng screenshot + click toạ độ.",
             "PERM_DENIED": "Thiếu quyền Trợ năng: gọi tisa_desktop_do op=cai_dat_quyen."}.get(ma, "")
    return "LOI_AD %s: %s%s" % (ma, str(e.get("message") or "")[:200], (" " + goi_y) if goi_y else "")
