"""tisa_quen_mat_khau.py - Nút "Quên mật khẩu?" ở màn đăng nhập TISA BOT: gửi MÃ đặt lại về Zalo admin của chính người dùng (chủ xác nhận 19/11/2026).

Chủ: "nhiều học viên đăng ký tài khoản đăng nhập TISA BOT mà quên mật khẩu; sau khi nối kênh Zalo admin, bấm Quên mật khẩu thì mật khẩu được gửi về Zalo admin
để họ lấy lại và đăng nhập."

Vì sao gửi MÃ chứ không gửi chính mật khẩu: mật khẩu được băm một chiều (pbkdf2) nên chính TISA BOT cũng không đọc lại được, và gửi mật khẩu cũ qua tin nhắn là xấu.
Cách làm chuẩn: gửi một MÃ 6 số dùng một lần về kênh admin (Zalo Bot mà người dùng đã nối và cho phép), người dùng nhập mã + mật khẩu mới ngay trên màn đăng nhập.

Luật an toàn:
  - Mã chỉ đi tới các chat Zalo admin đã được người dùng cho phép (cấu hình zalo_bot.chat_id). Chưa nối thì báo thật, không gửi đi đâu khác.
  - Mã ngẫu nhiên mật mã học, hiệu lực 10 phút, dùng một lần, tối đa 5 lần nhập sai rồi hủy; lưu dạng băm (không lưu mã thật), không ghi nhật ký, không trả về qua web.
  - Giới hạn gửi: cách nhau 60 giây, tối đa 5 lần mỗi giờ cho cả máy (không để ai đó spam Zalo của chủ); 10 lần nhập sai mỗi giờ thì khóa cả máy 1 giờ.
  - Đổi mật khẩu chỉ ghi đè đúng mật khẩu (giữ nguyên tên đăng nhập và 2FA), hạ mọi phiên đăng nhập cũ, báo lại về Zalo admin "mật khẩu vừa được đặt lại".
  - Chưa đặt mật khẩu lần đầu thì không có gì để lấy lại.

Đường (công khai, không cần đăng nhập, vì chính là lối cho người quên mật khẩu):
  GET  /auth/quen/trang-thai   {"co_kenh": bool}
  POST /auth/quen/gui          gửi mã về Zalo admin
  POST /auth/quen/doi          {code, password}: nhập mã + mật khẩu mới
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import secrets
import sys
import threading
import time
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

HIEU_LUC = 10 * 60          # giây
TOI_DA_SAI = 5              # số lần nhập sai cho một mã
GIAN_CACH_GUI = 60          # giây giữa hai lần gửi
TOI_DA_GUI_GIO = 5          # số lần gửi mỗi giờ cho cả máy
TOI_DA_SAI_GIO = 10         # số lần nhập sai mỗi giờ cho cả máy trước khi khóa
KHOA_GIAY = 3600
_khoa = threading.RLock()
_gui_luc: list = []         # thời điểm các lần gửi gần đây
_sai_luc: list = []         # thời điểm các lần nhập sai gần đây
_khoa_den = 0.0


def _cfg():
    import config
    return config


def _state_dir() -> Path:
    try:
        return Path(_cfg().STATE_DIR)
    except Exception:  # noqa: BLE001
        return Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)


def _tep() -> Path:
    return _state_dir() / "quen-mat-khau.json"


def _doc() -> dict:
    try:
        d = json.loads(_tep().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _ghi(d: dict) -> None:
    t = _tep()
    tam = t.with_suffix(".json.tmp")
    tam.write_text(json.dumps(d), encoding="utf-8")
    try:
        os.chmod(tam, 0o600)
    except OSError:
        pass
    os.replace(tam, t)


def _main():
    for ten in ("main", "__main__"):
        m = sys.modules.get(ten)
        if m is not None and hasattr(m, "_zalo_send_to"):
            return m
    return None


def kenh_admin() -> list:
    """Danh sách chat Zalo admin được phép nhận mã (rỗng = chưa nối hoặc chưa cho phép ai)."""
    try:
        z = (_cfg().read_settings().get("zalo_bot") or {})
    except Exception:  # noqa: BLE001
        return []
    if not (z.get("enabled") and str(z.get("token") or "").strip()):
        return []
    raw = z.get("chat_id")
    if isinstance(raw, (list, tuple)):
        ids = [str(x).strip() for x in raw]
    else:
        ids = [x.strip() for x in str(raw or "").replace(";", ",").replace("\n", ",").split(",")]
    return [x for x in ids if x][:5]


def _bam(ma: str, muoi: str) -> str:
    return hashlib.sha256((muoi + ":" + ma).encode("utf-8")).hexdigest()


def _tia(ds: list, now: float, cua_so: float) -> list:
    return [t for t in ds if now - t < cua_so]


def _ip(request) -> str:
    try:
        return request.client.host if request and request.client else "?"
    except Exception:  # noqa: BLE001
        return "?"


async def _gui_tin(noi_dung: str) -> tuple[int, str]:
    """Gửi tới mọi chat Zalo admin. Trả (số chat nhận được, lỗi cuối)."""
    m = _main()
    ids = kenh_admin()
    if m is None or not ids:
        return 0, "chưa nối Zalo admin"
    ok, loi = 0, ""
    for cid in ids:
        try:
            r = await m._zalo_send_to(cid, noi_dung)
            if r and r[0]:
                ok += 1
            else:
                loi = str((r or (False, ""))[1])[:120]
        except Exception as e:  # noqa: BLE001
            loi = type(e).__name__
    return ok, loi


def trang_thai() -> dict:
    cfg = _cfg()
    try:
        co_tk = bool(cfg.auth_enabled(cfg.read_settings()))
    except Exception:  # noqa: BLE001
        co_tk = False
    return {"ok": True, "co_kenh": bool(kenh_admin()), "co_tai_khoan": co_tk}


async def gui_ma(ip: str = "?") -> dict:
    """Tạo mã, gửi về Zalo admin. Không bao giờ trả mã trong kết quả."""
    global _khoa_den
    cfg = _cfg()
    now = time.time()
    try:
        if not cfg.auth_enabled(cfg.read_settings()):
            return {"ok": False, "loi": "Máy này chưa đặt mật khẩu nên chưa có gì để lấy lại."}
    except Exception:  # noqa: BLE001
        return {"ok": False, "loi": "Không đọc được cài đặt đăng nhập."}
    if not kenh_admin():
        return {"ok": False, "co_kenh": False, "loi": "Máy này chưa nối kênh Zalo admin (hoặc chưa cho phép tài khoản Zalo nào) nên chưa gửi mã được. "
                                                        "Dùng cách thủ công bên dưới, hoặc nối Zalo admin trong Cài đặt khi đã đăng nhập."}
    with _khoa:
        _gui_luc[:] = _tia(_gui_luc, now, 3600)
        if _gui_luc and now - _gui_luc[-1] < GIAN_CACH_GUI:
            return {"ok": False, "cho": int(GIAN_CACH_GUI - (now - _gui_luc[-1])) + 1, "loi": "Mã vừa được gửi. Chờ ít giây rồi mới gửi lại được."}
        if len(_gui_luc) >= TOI_DA_GUI_GIO:
            return {"ok": False, "loi": "Đã gửi mã quá nhiều lần trong một giờ. Thử lại sau."}
        ma = "%06d" % secrets.randbelow(1_000_000)
        muoi = secrets.token_hex(8)
        _ghi({"bam": _bam(ma, muoi), "muoi": muoi, "het_han": now + HIEU_LUC, "sai": 0})
        _gui_luc.append(now)
    noi_dung = ("TISA BOT: mã đặt lại mật khẩu của bạn là %s. Mã dùng một lần, hết hạn sau %d phút. "
                "Nếu không phải bạn vừa bấm \"Quên mật khẩu\", hãy bỏ qua tin này và đừng đưa mã cho ai." % (ma, HIEU_LUC // 60))
    ok, loi = await _gui_tin(noi_dung)
    ma = ""
    noi_dung = ""
    if not ok:
        with _khoa:
            try:
                _tep().unlink()
            except OSError:
                pass
            if _gui_luc:
                _gui_luc.pop()
        return {"ok": False, "loi": "Không gửi được tin về Zalo admin (%s). Kiểm tra bot Zalo admin đang bật rồi thử lại." % (loi or "không rõ lỗi")}
    return {"ok": True, "het_han_phut": HIEU_LUC // 60, "thong_bao": "Đã gửi mã 6 số về Zalo admin của bạn. Mở Zalo, lấy mã rồi nhập vào đây."}


async def doi_mat_khau(ma: str, mat_khau: str, ip: str = "?") -> dict:
    global _khoa_den
    cfg = _cfg()
    now = time.time()
    ma = "".join(c for c in str(ma or "") if c.isdigit())
    with _khoa:
        if now < _khoa_den:
            return {"ok": False, "loi": "Nhập sai quá nhiều lần. Chờ khoảng %d phút rồi thử lại." % (int(_khoa_den - now) // 60 + 1)}
        d = _doc()
    if not d or now > float(d.get("het_han") or 0):
        return {"ok": False, "loi": "Mã đã hết hạn hoặc chưa được gửi. Bấm \"Gửi mã về Zalo\" để lấy mã mới."}
    mk = cfg.clean_password(mat_khau) if hasattr(cfg, "clean_password") else str(mat_khau or "")
    if len(mk) < 8:
        return {"ok": False, "loi": "Mật khẩu mới tối thiểu 8 ký tự."}
    dung = len(ma) == 6 and hmac.compare_digest(_bam(ma, str(d.get("muoi") or "")), str(d.get("bam") or ""))
    if not dung:
        await asyncio.sleep(0.5)
        with _khoa:
            _sai_luc[:] = _tia(_sai_luc, now, 3600)
            _sai_luc.append(now)
            d["sai"] = int(d.get("sai") or 0) + 1
            if len(_sai_luc) >= TOI_DA_SAI_GIO:
                _khoa_den = now + KHOA_GIAY
            if d["sai"] >= TOI_DA_SAI:
                try:
                    _tep().unlink()
                except OSError:
                    pass
                return {"ok": False, "loi": "Nhập sai %d lần nên mã đã bị hủy. Bấm \"Gửi mã về Zalo\" để lấy mã mới." % TOI_DA_SAI}
            _ghi(d)
        return {"ok": False, "loi": "Mã không đúng (còn %d lần thử)." % (TOI_DA_SAI - d["sai"])}
    # Đúng mã: dùng một lần, hủy ngay.
    with _khoa:
        try:
            _tep().unlink()
        except OSError:
            pass
    s = cfg.read_settings()
    a = dict(s.get("auth") or {})          # ghi đè TỪNG KHÓA: 2FA nằm trong cùng khối `auth`, gán đè cả khối sẽ lặng lẽ tắt 2FA
    a["password_hash"], a["salt"] = cfg.hash_password(mk)
    s["auth"] = a
    cfg.write_settings(s)
    try:
        cfg.clear_sessions()                # mọi thiết bị đang đăng nhập bằng mật khẩu cũ bị đăng xuất
    except Exception:  # noqa: BLE001
        pass
    m = _main()
    try:                                    # gỡ khóa đăng nhập sai của IP này nếu có
        if m is not None and hasattr(m, "_LOGIN_FAILS"):
            m._LOGIN_FAILS.pop(ip, None)
    except Exception:  # noqa: BLE001
        pass
    try:
        await _gui_tin("TISA BOT: mật khẩu đăng nhập vừa được đặt lại bằng mã gửi về Zalo này. Nếu không phải bạn, hãy vào Cài đặt đổi mật khẩu ngay.")
    except Exception:  # noqa: BLE001
        pass
    return {"ok": True, "thong_bao": "Đã đặt lại mật khẩu. Đăng nhập bằng mật khẩu mới (nếu bạn bật xác thực 2 lớp thì vẫn nhập mã như cũ)."}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    async def _json(request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return d if isinstance(d, dict) else {}

    @app.get("/auth/quen/trang-thai")
    async def _qmk_tt():
        return JSONResponse(await asyncio.to_thread(trang_thai))

    @app.post("/auth/quen/gui")
    async def _qmk_gui(request: Request):
        r = await gui_ma(_ip(request))
        return JSONResponse(r, status_code=200 if r.get("ok") else (429 if r.get("cho") else 400))

    @app.post("/auth/quen/doi")
    async def _qmk_doi(request: Request):
        d = await _json(request)
        r = await doi_mat_khau(d.get("code"), d.get("password"), _ip(request))
        d.clear()
        return JSONResponse(r, status_code=200 if r.get("ok") else 400)
