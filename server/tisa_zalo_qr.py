"""Đăng nhập Zalo bằng QR không còn đứng (bộ TISA, chủ báo 10/11/2026: "quét QR bị đứng lại không quét thêm được").

Thay luồng của zalo_login (giữ nguyên status/cancel và cách lưu kết nối):
- Mã QR Zalo chết sau 100 giây. Bộ đăng nhập chỉ báo "đã tạo QR", không tự tạo mã mới, nên mã chết vẫn nằm trên màn hình.
  Bấm "Từ chối" trên điện thoại thì thư viện chờ mãi. Ở đây: quá 95 giây kể từ mã gần nhất mà chưa xong, hoặc tiến trình
  thoát khi chưa xong, thì tự chạy lại để có mã mới (cùng thư mục tài khoản), tối đa 10 phút.
- Đọc cả kênh nhật ký (stderr) song song, tránh tiến trình bị nghẽn khi nhật ký đầy bộ đệm.
- Đăng nhập xong thì đợi tiến trình tự thoát tối đa 15 giây rồi tắt hẳn, không để sót tiến trình giữ cổng QR.
"""
import os
import subprocess
import threading
import time
import uuid

import localefmt
import mcp_store
import winproc
import zalo_login as zl
from config import STATE_DIR

QR_SONG = 95          # mã QR Zalo sống 100 giây: làm mới trước đó một chút
TONG = 600            # cả phiên đăng nhập tối đa 10 phút
LAM_MOI_TOI_DA = 8


def _tat(proc):
    try:
        if proc and proc.poll() is None:
            if not winproc.kill_tree(proc.pid):
                proc.kill()
    except Exception:  # noqa: BLE001
        pass


def _chay(sess):
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen(sess["argv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                            text=True, encoding="utf-8", errors="replace", env=sess["env"], **kwargs)
    sess["proc"] = proc
    sess["qr_luc"] = 0.0
    nhat_ky = []

    def doc_loi():
        try:
            for dong in iter(proc.stderr.readline, ""):
                nhat_ky.append(dong)
                del nhat_ky[:-40]
        except Exception:  # noqa: BLE001
            pass
    threading.Thread(target=doc_loi, daemon=True).start()
    return proc, nhat_ky


def _mot_luot(sess):
    """Một lần chạy bộ đăng nhập. Trả "xong" | "loi" | "lam_moi"."""
    import json
    proc, nhat_ky = _chay(sess)
    ket, co_qr = "", False
    try:
        for raw in iter(proc.stdout.readline, ""):
            if sess.get("state") in ("done", "error"):
                break
            raw = (raw or "").strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(obj, dict):
                continue
            ev = str(obj.get("event") or "").lower()
            if ev == "qr":
                qr = zl._qr_from_event(obj, sess["home"])
                if qr:
                    co_qr = True
                    sess.update(state="qr", qr=qr, qr_luc=time.time())
                continue
            if ev in zl._SUCCESS_EVENTS or (not ev and (obj.get("ownId") or obj.get("own_id"))):
                zl._finish_ok(sess, obj)
                ket = "xong"
                break
            if ev in zl._ERROR_EVENTS:
                sess["loi_cuoi"] = str(obj.get("message") or obj.get("error") or "")
                ket = "lam_moi"
                break
    except Exception as e:  # noqa: BLE001
        sess["loi_cuoi"] = "%s: %s" % (type(e).__name__, e)
        ket = "lam_moi"
    if ket == "xong":
        try:
            proc.wait(timeout=15)
        except Exception:  # noqa: BLE001
            pass
        _tat(proc)
        return "xong"
    _tat(proc)
    if sess.get("state") in ("done", "error"):
        return "loi"
    if not co_qr and not ket:
        # Chưa từng ra mã QR mà đã thoát: lỗi thật (thiếu mạng, không tải được gói), không làm mới.
        sess["loi_cuoi"] = sess.get("loi_cuoi") or "".join(nhat_ky)[-300:]
        return "loi"
    return "lam_moi"


def _dieu_phoi(sid):
    sess = zl._sessions.get(sid)
    if not sess:
        return
    lan = 0
    while True:
        kq = _mot_luot(sess)
        if kq == "xong" or sess.get("state") in ("done", "error"):
            return
        lan += 1
        het_gio = time.time() - sess["bat_dau"] > TONG
        if kq == "loi" or het_gio or lan > LAM_MOI_TOI_DA:
            if sess.get("state") not in ("done", "error"):
                loi = localefmt.chu("Mã QR hết hạn, bấm thử lại", "The QR code expired, press try again") if (het_gio or lan > LAM_MOI_TOI_DA) \
                    else localefmt.chu("Đăng nhập chưa hoàn tất", "Sign-in did not complete") + (": " + sess.get("loi_cuoi", "")[-200:] if sess.get("loi_cuoi") else "")
                sess.update(state="error", error=loi)
            return
        sess["lam_moi"] = lan        # giữ mã cũ trên màn hình tới khi mã mới về
        time.sleep(1)


def _canh(sid):
    """Mã QR đứng quá lâu (chết hoặc bị từ chối trên điện thoại): tắt lượt hiện tại để _dieu_phoi tạo mã mới."""
    while True:
        time.sleep(3)
        sess = zl._sessions.get(sid)
        if not sess or sess.get("state") in ("done", "error"):
            return
        if sess.get("state") == "qr" and sess.get("qr_luc") and time.time() - sess["qr_luc"] > QR_SONG:
            sess["qr_luc"] = 0.0
            sess["loi_cuoi"] = ""
            _tat(sess.get("proc"))
        if time.time() - sess["bat_dau"] > TONG + 30:
            _tat(sess.get("proc"))
            return


def start(label=None):
    zl._sweep()
    argv = zl._npx_argv()
    if not argv:
        return {"ok": False, "error": localefmt.chu("Cần cài Node.js 20+ (lệnh npx) trên máy chạy TISA BOT - tải tại nodejs.org",
                                                    "Node.js 20+ (the npx command) must be installed on the machine running TISA BOT - download it at nodejs.org")}
    sid = uuid.uuid4().hex[:10]
    slug = mcp_store._slugify(label or "zalo")
    home = str(STATE_DIR / "connector-home" / f"zalo-{slug}-{sid[:6]}")
    os.makedirs(home, exist_ok=True)
    env = dict(os.environ)
    env["HOME"] = home
    env["USERPROFILE"] = home
    sess = {"state": "starting", "qr": "", "label": (label or "").strip(), "conn_id": "", "error": "", "proc": None,
            "home": home, "ts": time.time(), "bat_dau": time.time(), "argv": argv, "env": env}
    zl._sessions[sid] = sess
    try:
        threading.Thread(target=_dieu_phoi, args=(sid,), daemon=True).start()
        threading.Thread(target=_canh, args=(sid,), daemon=True).start()
    except RuntimeError as e:
        return {"ok": False, "error": str(e)}
    return {"ok": True, "sid": sid}


def gan():
    """Thay start của zalo_login (main.py gọi zalo_login.start qua tên module nên thay là ăn ngay)."""
    zl.start = start
    zl._SESS_TTL = max(getattr(zl, "_SESS_TTL", 900), TONG + 300)
