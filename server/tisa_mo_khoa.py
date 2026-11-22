"""tisa_mo_khoa.py - Mở khóa máy Mac khi anh ở xa (chủ xác nhận 18/11/2026, yêu cầu gốc trong brain: 2026-11-18-yeu-cau-mo-khoa-may).

Công cụ `tisa_desktop_do` vẫn CHẶN mọi click/type/key khi ứng dụng ở trước là loginwindow (trả CAN_NGUOI_DUNG). Thao tác `op=mo_khoa` là
MỘT đường riêng, hẹp, không nới chốt chặn cho thao tác khác:

  1. Mật khẩu chỉ lấy từ macOS Keychain (mục `tisa-bot-mo-khoa`, tài khoản = tên người dùng máy). Không nhận mật khẩu qua tham số tool
     (có tham số kiểu mật khẩu là từ chối ngay), không lưu vào tệp, brain, log, chat; không in ra kết quả trả về cho AI.
  2. Chỉ chạy khi yêu cầu đến từ kênh đã xác thực của anh: dashboard TISA BOT (cuộc chat của chủ với chính TISA BOT) hoặc đúng id Zalo của
     anh (khai trong dieu-khien-may/mo-khoa-cau-hinh.json, mặc định KHÔNG có ai). Nhóm chat, khách, bot Fanpage, cộng sự, việc nền: từ chối.
  3. Mỗi lần xin duyệt (CAN_DUYET) trừ khi phiên đang Toàn quyền. Tối đa 3 lần thử liên tiếp thất bại rồi dừng 30 phút; mỗi lần gọi chỉ gõ
     MỘT lần (không tự thử lại trong cùng lần gọi), không bao giờ thử mật khẩu khác.
  4. Nhật ký mỗi lần: giờ, kênh, kết quả (dieu-khien-may/mo-khoa-nhat-ky.jsonl và nhật ký chung "may_mo_khoa"). Không ghi mật khẩu,
     không ghi chữ do AI viết.
  5. Gõ xong chụp màn hình, kiểm đã vào màn hình chính. Hộp Touch ID, mã khóa, xác minh hay vẫn ở màn hình khóa thì DỪNG và báo anh.

  mo_khoa(p, a, muc, turn) -> chuỗi kết quả cho AI. Chạy ở thread nền (nhiều lệnh chờ). Không gọi ở máy không phải macOS.
"""
from __future__ import annotations

import asyncio
import getpass
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    import os
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

try:
    import tisa_browser as B       # dùng chung nhật ký và thẻ xin duyệt với Trình duyệt TISA
except Exception:  # noqa: BLE001
    B = None

DICH_VU = "tisa-bot-mo-khoa"       # tên mục trong Keychain (anh tự thêm, xem HUONG_DAN_CAI)
DIR = STATE_DIR / "dieu-khien-may"
TEP_NK = DIR / "mo-khoa-nhat-ky.jsonl"
TEP_DEM = DIR / "mo-khoa-dem.json"
TEP_CH = DIR / "mo-khoa-cau-hinh.json"
TOI_DA = 3                         # số lần thử thất bại liên tiếp tối đa
KHOA_GIAY = 30 * 60                # dừng bao lâu sau khi đủ 3 lần thất bại
CHO_SAU_GO = 3.0                   # giây chờ macOS mở màn hình sau khi nhấn Enter

# Tham số mà tool tuyệt đối không nhận (mật khẩu không được đi qua đường này).
_THAM_SO_CAM = {"text", "password", "pass", "passwd", "pw", "matkhau", "mat_khau", "secret", "pin", "ma_khoa"}
_MAN_HINH_KHOA = ("loginwindow", "screensaverengine")
_HOP_XAC_MINH = re.compile(r"coreautha|securityagent|touch ?id|usernotification|apple ?watch|passkey|verification|xác minh|mã khóa|unlock", re.I)

HUONG_DAN_CAI = ("Anh tự thêm mật khẩu máy vào Keychain MỘT lần, gõ trong Terminal của anh (lệnh sẽ tự hỏi mật khẩu, KHÔNG gõ mật khẩu vào chat): "
                 "security add-generic-password -s %s -a \"$USER\" -w   (rồi nhập mật khẩu máy khi được hỏi)." % DICH_VU)

_chay = threading.Lock()
_ghi_lock = threading.Lock()


# ---------------------------------------------------------------- nhật ký (không bao giờ chứa mật khẩu)
def _ghi(kenh: str, ket_qua: str, ghi_chu: str = "") -> None:
    row = {"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "kenh": str(kenh)[:60], "ket_qua": str(ket_qua)[:60], "ghi_chu": str(ghi_chu)[:120]}
    try:
        with _ghi_lock:
            DIR.mkdir(parents=True, exist_ok=True)
            with open(TEP_NK, "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass
    if B is not None:
        try:
            B._ghi_nk({"op": "may_mo_khoa", "ket_qua": row["ket_qua"], "mo_ta": ("Mở khóa máy, kênh %s. %s" % (row["kenh"], row["ghi_chu"]))[:200], "ten": "", "host": "Máy tính"})
        except Exception:  # noqa: BLE001
            pass


def doc_nhat_ky(n: int = 20) -> list:
    try:
        return [json.loads(x) for x in TEP_NK.read_text(encoding="utf-8").splitlines()[-n:] if x.strip()]
    except (OSError, ValueError):
        return []


# ---------------------------------------------------------------- kênh được phép
def _cau_hinh() -> dict:
    try:
        d = json.loads(TEP_CH.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _luu_cau_hinh(**kw) -> None:
    with _ghi_lock:
        d = _cau_hinh()
        d.update(kw)
        DIR.mkdir(parents=True, exist_ok=True)
        tam = TEP_CH.with_suffix(".json.tmp")
        tam.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        os.replace(tam, TEP_CH)


def _zalo_ids() -> set:
    return {str(x).strip().split(":")[-1] for x in (_cau_hinh().get("zalo_ids") or []) if str(x).strip()}


def dang_bat() -> bool:
    """Tính năng đang BẬT? Anh bật/tắt ở Cài đặt (khóa `bat`). Chưa từng bấm thì coi là bật nếu Keychain đã có mật khẩu (máy đã cài từ bản trước)."""
    d = _cau_hinh()
    if "bat" in d:
        return bool(d["bat"])
    return da_cai_mat_khau()


def _nho_zalo_cho(sid: str) -> None:
    """Zalo vừa nhắn xin mở khóa nhưng chưa được khai: nhớ lại để anh bấm 'Đây là Zalo của anh' ở Cài đặt (không phải đi tìm mã)."""
    sid = str(sid or "").strip().split(":")[-1]
    if not sid or len(sid) > 40:
        return
    try:
        d = _cau_hinh()
        ds = [x for x in (d.get("zalo_cho") or []) if isinstance(x, dict) and x.get("id") != sid][-4:]
        ds.append({"id": sid, "luc": time.strftime("%Y-%m-%d %H:%M:%S")})
        _luu_cau_hinh(zalo_cho=ds)
    except (OSError, ValueError, TypeError):
        pass


def _che(s: str) -> str:
    s = str(s or "")
    return ("…" + s[-4:]) if len(s) > 4 else "…"


def kiem_kenh(turn) -> tuple[bool, str, str]:
    """(được phép, tên kênh để ghi nhật ký, lý do từ chối). `turn` = turn_context.current(); None hoặc thiếu = không ai = từ chối."""
    if not isinstance(turn, dict):
        return False, "không rõ", "Không xác định được ai đang yêu cầu (không có thông tin kênh)."
    kenh = str(turn.get("kenh") or "").strip().lower() or "không rõ"
    if not turn.get("la_chu"):
        return False, kenh, "Yêu cầu không đến từ bề mặt của chủ (khách, bot Fanpage hay bot chuyên trách)."
    if turn.get("bot_id"):
        return False, kenh, "Yêu cầu đến từ một bot chuyên trách, không phải anh."
    # (19/11/2026) anh nhắn ở ô chat nào trong dashboard TISA BOT cũng được, kể cả chat với cộng sự: đó vẫn là anh đang gõ. Chỉ chặn việc nền / bước việc nhóm (không có anh đang nhắn).
    if turn.get("job") or turn.get("team_gate"):
        return False, kenh, "Yêu cầu đến từ việc nền hoặc bước việc nhóm, không có anh đang nhắn."
    if str(turn.get("chat_type") or "") != "private":
        return False, kenh, "Yêu cầu đến từ nhóm chat."
    if kenh == "dashboard":
        return True, "dashboard", ""
    if kenh in ("zalo", "zalo_personal"):
        sid = str(turn.get("sender_id") or "").strip().split(":")[-1]
        if sid and sid in _zalo_ids():
            return True, "zalo(%s)" % _che(sid), ""
        _nho_zalo_cho(sid)
        return False, "zalo(%s)" % _che(sid), ("Tài khoản Zalo này (…%s) chưa được anh xác nhận là Zalo của anh. Em đã ghi lại: anh mở TISA BOT → Điều khiển của AI → tab Máy tính → "
                                                "mục Mở khóa máy → bấm \"Đây là Zalo của anh\", rồi nhắn lại một lần. Hoặc anh nhắn thẳng ở ô chat trong dashboard TISA BOT thì làm được ngay." % _che(sid)[-4:])
    return False, kenh, "Kênh này không nằm trong danh sách được mở khóa máy (chỉ ô chat trong dashboard TISA BOT, và Zalo của anh sau khi anh xác nhận ở Cài đặt)."


# ---------------------------------------------------------------- Keychain
def _doc_mat_khau(dich_vu: str = "", tai_khoan: str = "") -> str | None:
    """Đọc mật khẩu từ Keychain bằng lệnh `security`. Trả None nếu không có hoặc không đọc được. KHÔNG bao giờ ghi/in giá trị này."""
    dich_vu = dich_vu or DICH_VU
    try:       # tisa_keychain.doc giải mã đúng cả mật khẩu có chữ có dấu / ký tự lạ (security -w trả dạng hex)
        import tisa_keychain as K
        v = K.doc(dich_vu, tai_khoan)
        if v:
            return v
    except Exception:  # noqa: BLE001
        pass
    try:
        tk = tai_khoan or getpass.getuser()
        r = subprocess.run(["/usr/bin/security", "find-generic-password", "-s", dich_vu, "-a", tk, "-w"],
                           capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    pw = (r.stdout or "").rstrip("\n")
    return pw or None


def kiem_mat_khau_may(pw: str, tai_khoan: str = "") -> bool | None:
    """Mật khẩu có ĐÚNG với tài khoản đăng nhập của máy không (dscl -authonly, mật khẩu đi qua stdin, không nằm trong danh sách tiến trình).
    True = đúng, False = sai, None = không kiểm được (không phải macOS, lệnh lỗi). Sai mật khẩu ở đây KHÔNG làm máy khóa thêm."""
    if sys.platform != "darwin" or not pw:
        return None
    try:
        r = subprocess.run(["/usr/bin/dscl", ".", "-authonly", tai_khoan or getpass.getuser()], input=pw + "\n", capture_output=True, text=True, timeout=12)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode == 0:
        return True
    if r.returncode == 10 or "eDSAuthFailed" in (r.stderr or ""):
        return False
    return None


def luu_mat_khau(pw: str) -> dict:
    """Anh nhập mật khẩu ở Cài đặt: kiểm đúng với máy rồi mới cất vào Keychain (mục tisa-bot-mo-khoa). Không bao giờ ghi ở nơi nào khác."""
    pw = str(pw or "")
    if sys.platform != "darwin":
        return {"ok": False, "loi": "Mở khóa máy bằng mật khẩu hiện chỉ làm được trên máy Mac."}
    if not pw.strip():
        return {"ok": False, "loi": "Anh chưa nhập mật khẩu."}
    if len(pw) > 200 or "\n" in pw or "\r" in pw:
        return {"ok": False, "loi": "Mật khẩu có ký tự không hợp lệ."}
    dung = KIEM_MAT_KHAU(pw)
    if dung is False:
        return {"ok": False, "loi": "Mật khẩu này KHÔNG đúng với tài khoản đăng nhập của máy. Anh nhập lại đúng mật khẩu anh dùng để mở máy."}
    try:
        import tisa_keychain as K
        ok = K.luu(DICH_VU, pw)
    except Exception:  # noqa: BLE001
        ok = False
    if not ok:
        return {"ok": False, "loi": "Không cất được vào Keychain của máy. Anh kiểm tra Keychain có đang bị khóa không rồi thử lại."}
    _luu_cau_hinh(bat=True)
    _dem_ghi(0)
    _ghi("cài đặt", "đã lưu mật khẩu", "đã kiểm khớp mật khẩu máy" if dung else "chưa kiểm được khớp")
    return {"ok": True, "da_kiem": dung is True}


def xoa_mat_khau() -> dict:
    try:
        import tisa_keychain as K
        K.xoa(DICH_VU)
    except Exception:  # noqa: BLE001
        pass
    _luu_cau_hinh(bat=False)
    _ghi("cài đặt", "đã xóa mật khẩu", "")
    return {"ok": True}


def da_cai_mat_khau(dich_vu: str = "") -> bool:
    """Chỉ kiểm có mục trong Keychain (không lấy giá trị)."""
    dich_vu = dich_vu or DICH_VU
    try:
        r = subprocess.run(["/usr/bin/security", "find-generic-password", "-s", dich_vu, "-a", getpass.getuser()], capture_output=True, text=True, timeout=8)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# ---------------------------------------------------------------- đếm lần thất bại (bền, qua các lần gọi)
def _dem_doc() -> dict:
    try:
        d = json.loads(TEP_DEM.read_text(encoding="utf-8"))
        return {"that_bai": int(d.get("that_bai") or 0), "luc": float(d.get("luc") or 0)}
    except (OSError, ValueError):
        return {"that_bai": 0, "luc": 0.0}


def _dem_ghi(that_bai: int) -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_DEM.write_text(json.dumps({"that_bai": that_bai, "luc": time.time()}), encoding="utf-8")
    except OSError:
        pass


def lan_con_lai() -> tuple[int, int]:
    """(số lần còn được thử, số giây còn bị dừng). Hết hạn dừng thì tự về 3 lần."""
    d = _dem_doc()
    if d["that_bai"] >= TOI_DA:
        con = int(d["luc"] + KHOA_GIAY - time.time())
        if con > 0:
            return 0, con
        _dem_ghi(0)
        return TOI_DA, 0
    return TOI_DA - d["that_bai"], 0


# ---------------------------------------------------------------- thực hiện
CHO_O_MAT_KHAU = 8                 # số giây chờ tối đa tới khi thấy màn hình đăng nhập sau khi đánh thức
CHO_SAU_THUC = 2.5                 # giây chờ sau khi đánh thức (màn hình sáng rồi ô mật khẩu mới nhận phím)
TRE_PHIM = 0.09                    # giây giữa hai phím khi gõ mật khẩu (gõ chậm cho chắc)
CHO_MO_GIAY = 15.0                 # sau khi gõ xong chờ tối đa bấy nhiêu giây cho macOS mở màn hình (mở thật mất 4 đến 6 giây)
KIEM_MAT_KHAU = kiem_mat_khau_may  # hàm kiểm mật khẩu với máy (kiểm thử thay bằng hàm giả)


def _danh_thuc(p) -> None:
    """Đánh thức màn hình: báo macOS 'có người dùng' (caffeinate -u), nhích chuột 2 lần (chuột không bao giờ về góc trên trái, chỗ đó là lệnh Dừng), rồi chờ. Không gõ phím nào."""
    f = getattr(p, "danh_thuc_man_hinh", None)
    if callable(f):
        try:
            f()
        except Exception:  # noqa: BLE001
            pass
    try:
        x, y = p.vi_tri_chuot()
        dx = 3 if x < 100 else -3
        dy = 3 if y < 100 else -3
        for _ in range(2):
            p.di_chuyen(x + dx, y + dy)
            time.sleep(0.25)
            p.di_chuyen(x, y)
            time.sleep(0.25)
    except Exception:  # noqa: BLE001
        pass
    time.sleep(CHO_SAU_THUC)


def _dang_khoa(p) -> bool:
    """Máy có đang khóa không. Ưu tiên cờ khóa của hệ điều hành (chính xác); không có thì xem ứng dụng ở trước là loginwindow / trình bảo vệ màn hình."""
    f = getattr(p, "man_hinh_khoa", None)
    if callable(f):
        try:
            v = f()
            if v is not None:
                return bool(v)
        except Exception:  # noqa: BLE001
            pass
    return str(p.ung_dung_truoc() or "").lower() in _MAN_HINH_KHOA


def _cho_mo_khoa(p) -> tuple[bool, str]:
    """Sau khi gõ mật khẩu: chờ tới khi máy mở (mở thật mất 4 đến 6 giây, chờ 3 giây là báo hỏng oan), hoặc hiện hộp xác minh, hoặc hết giờ. Trả (còn khóa, ứng dụng ở trước)."""
    han = time.time() + CHO_MO_GIAY
    while True:
        front = str(p.ung_dung_truoc() or "")
        if not _dang_khoa(p):
            return False, front
        if _HOP_XAC_MINH.search(front) and front.lower() not in _MAN_HINH_KHOA:
            return True, front
        if time.time() >= han:
            return True, front
        time.sleep(0.6)


def _ban_phim_abc():
    try:
        import tisa_ban_phim
        return tisa_ban_phim.tam_dung_abc()
    except Exception:  # noqa: BLE001
        import contextlib
        return contextlib.nullcontext({"truoc": "", "da_doi": False})


def _chup(p) -> str:
    """Chụp màn hình bằng đúng đường chụp của tisa_desktop (ảnh gửi kèm cho AI)."""
    try:
        import tisa_desktop as D
        return D._lam(p, "screenshot", {})
    except Exception as e:  # noqa: BLE001
        return "(Không chụp được ảnh: %s)" % type(e).__name__


CHO_ANH_PHUT = 15                  # phút chờ anh xác thực (Touch ID, mã khóa...) trong MỘT lần gọi; hết giờ thì trả CAN_NGUOI_DUNG, gọi lại sẽ chờ tiếp


def _cho_anh(p, kenh: str, bao, ly_do: str) -> str:
    """Báo anh một tin ngắn rồi tạm dừng tới khi hộp xác minh biến mất (anh đã làm xong). Trả XONG | ANH_BAO_XONG | DA_DUNG | HET_GIO."""
    import tisa_bao_anh as BA
    try:
        import tisa_desktop as D
        dung = lambda: bool(D._tt.get("dung"))   # noqa: E731
    except Exception:  # noqa: BLE001
        dung = None
    xong = (lambda: bool(B and B._tt.pop("nguoi_xong", False))) if B is not None and hasattr(B, "_tt") else None
    het = lambda: not _HOP_XAC_MINH.search(str(p.ung_dung_truoc() or ""))   # noqa: E731
    _ghi(kenh, "chờ anh xác thực", ly_do[:60])
    return BA.cho_nguoi_that(het, ly_do, phut=CHO_ANH_PHUT, dung=dung, xong=xong, bao_fn=bao)


HUONG_DAN_CAI_DAT = ("Anh mở TISA BOT → Điều khiển của AI → tab Máy tính → mục Mở khóa máy, nhập mật khẩu đăng nhập của máy rồi bật. "
                     "Mật khẩu nhập ở đó được kiểm đúng với máy và cất vào Keychain, không nằm trong chat.")


def _o_mat_khau_loginwindow():
    """(cx, cy) tâm ô "Nhập mật khẩu" của màn hình khóa (đọc bằng Trợ năng), hoặc None nếu ô chưa hiện."""
    try:
        import ctypes
        import tisa_hop_thoai as H
        r = subprocess.run(["/usr/bin/pgrep", "-x", "loginwindow"], capture_output=True, text=True, timeout=5)
        pid = int((r.stdout or "0").split()[0])
    except Exception:  # noqa: BLE001
        return None
    cay = H.Cay(pid)
    try:
        if not cay.CR:
            return None
        ag = cay.CR._P["ag"]
        ag.AXValueGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
        ag.AXValueGetValue.restype = ctypes.c_bool

        class _Hai(ctypes.Structure):
            _fields_ = [("a", ctypes.c_double), ("b", ctypes.c_double)]
        for w in cay.cua_so():
            for n in cay.duyet(w, 12):
                if n["vai"] not in ("AXTextField", "AXSecureTextField"):
                    continue
                vt, co = _Hai(), _Hai()
                v1, v2 = cay.CR._thuoc_tinh(n["el"], "AXPosition"), cay.CR._thuoc_tinh(n["el"], "AXSize")
                try:
                    if v1 and v2 and ag.AXValueGetValue(v1.value, 1, ctypes.byref(vt)) and ag.AXValueGetValue(v2.value, 2, ctypes.byref(co)) and co.a > 20:
                        return vt.a + co.a / 2, vt.b + co.b / 2
                finally:
                    for v in (v1, v2):
                        if v:
                            cay.CR._P["cf"].CFRelease(v)
        return None
    finally:
        cay.dong()


def _bam_vao_o_mat_khau(p) -> bool:
    """(22/11/2026, chủ báo nút Mở khóa máy và ô gõ từ máy 2 đều không vào) Màn hình khóa macOS 26 thu gọn chỉ còn ảnh đại diện;
    phím gõ khi ô "Nhập mật khẩu" CHƯA được bấm vào thì bị bỏ (đã thử trên máy thật: gõ không hiện dấu chấm nào). Bấm ảnh đại diện cho ô hiện ra,
    rồi bấm thẳng vào ô cho nó nhận con trỏ, sau đó mới gõ. Trả True nếu đã bấm vào ô."""
    try:
        o = _o_mat_khau_loginwindow()
        w, h = p.kich_thuoc()
        # Luôn bấm ảnh đại diện trước (ô thu gọn thì nó bung ra; ô đã mở thì vô hại), rồi mới bấm vào ô: đúng thứ tự đã thử chạy trên máy thật.
        p.bam(int(o[0]) if o else int(w / 2), int(o[1] - 54) if o else int(h * 0.858))
        o = None
        for _ in range(10):
            time.sleep(0.25)
            o = _o_mat_khau_loginwindow()
            if o:
                break
        if not o:
            return False
        p.bam(int(o[0]), int(o[1]))
        time.sleep(0.35)
        return True
    except Exception:  # noqa: BLE001
        return False


def _go_mot_lan(p, kenh: str, pw: str) -> None:
    """Gõ mật khẩu đúng MỘT lần rồi Enter (bàn phím ABC để Telex/VNI không biến chữ)."""
    _bam_vao_o_mat_khau(p)
    with _ban_phim_abc() as bp:
        _ghi(kenh, "đang gõ", "bàn phím trước: %s; đổi sang ABC: %s" % (str(bp.get("truoc") or "?")[-28:], "có" if bp.get("da_doi") else "không cần"))
        try:
            p.go(pw, "phim", tre=TRE_PHIM)
        except TypeError:
            p.go(pw, "phim")
        time.sleep(0.25)
        p.nhan_phim(set(), "enter")


def _mo_khoa_nen(p, a: dict, muc: str, turn, uy_quyen=None, bao=None) -> str:
    # 0. Mật khẩu không bao giờ đi qua tham số của tool.
    vi_pham = sorted(k for k in (a or {}) if str(k).lower() in _THAM_SO_CAM)
    if vi_pham:
        _ghi("không rõ", "từ chối (tham số)", "Có tham số kiểu mật khẩu: %s" % ",".join(vi_pham)[:60])
        return ("TU_CHOI: op=mo_khoa KHÔNG nhận mật khẩu qua tham số (đã gặp: %s). Mật khẩu chỉ lấy từ Keychain của máy. Đừng hỏi hay nhận mật khẩu trong chat; "
                "gọi lại op=mo_khoa không kèm tham số đó." % ", ".join(vi_pham))
    if getattr(p, "ten", "") != "macOS":
        return ("KHONG_HO_TRO: Mở khóa máy bằng mật khẩu hiện chỉ làm được trên máy Mac (macOS). Trên Windows, màn hình khóa nằm ngoài tầm với của chương trình chạy trong phiên đăng nhập, "
                "nên em chưa mở khóa từ xa được. Nói thật với anh như vậy; cách phòng: anh bật giữ máy thức (op=giu_may_thuc) cho việc dài và tắt yêu cầu đăng nhập khi thức dậy trong Cài đặt Windows nếu anh chấp nhận rủi ro.")
    # 1. Kênh yêu cầu.
    if uy_quyen:        # việc nền đã được dashboard của anh cấp quyền mở khóa lại (tisa_thuc_giac); vẫn giới hạn 3 lần
        ok, kenh, ly_do = True, "việc nền (quyền cấp từ %s)" % str(uy_quyen)[:30], ""
    else:
        ok, kenh, ly_do = kiem_kenh(turn)
    if not ok:
        _ghi(kenh, "từ chối (kênh)", ly_do)
        return ("TU_CHOI: Không mở khóa máy theo yêu cầu này. %s Nói ĐÚNG lý do này với anh (và cách xử lý nếu có). Đừng bảo anh \"nhắn lại ở dashboard hoặc Zalo\" khi anh đã nhắn ở đó, "
                "đừng nói vòng vo, đừng tìm cách vòng, đừng xin mật khẩu." % ly_do)
    if not dang_bat():
        _ghi(kenh, "từ chối (đang tắt)", "Tính năng mở khóa máy đang tắt hoặc chưa có mật khẩu")
        return ("TAT: Tính năng mở khóa máy đang TẮT hoặc chưa có mật khẩu trong Keychain. %s Nói đúng như vậy với anh, đừng xin mật khẩu trong chat. "
                "Anh nhập xong thì nhắn lại \"mở khóa máy\" là em làm ngay." % HUONG_DAN_CAI_DAT)
    if not _chay.acquire(blocking=False):
        return "DANG_CHAY: Đang có một lần mở khóa chạy dở. Chờ nó xong rồi xem màn hình."
    try:
        # 2. Số lần thử.
        con, giay = lan_con_lai()
        if con <= 0:
            _ghi(kenh, "dừng (hết lần thử)", "Đã đủ %d lần thất bại, dừng %d giây" % (TOI_DA, giay))
            return ("DA_DUNG_THU: Đã thử %d lần không mở được nên TISA BOT dừng để không khóa máy lâu hơn (còn khoảng %d phút mới thử lại được). "
                    "Báo anh: anh tự mở khóa, hoặc vào Cài đặt → Mở khóa máy bấm \"Cho thử lại\"." % (TOI_DA, max(1, giay // 60)))
        vt = p.vi_tri_chuot()
        if vt[0] <= 2 and vt[1] <= 2:
            _ghi(kenh, "dừng (chuột góc)", "Chuột ở góc trên trái")
            return "DA_DUNG: Chuột đang ở góc trên trái màn hình, coi như anh muốn dừng. Không mở khóa."
        # 3. Máy có đang ở màn hình khóa không (chỉ đọc).
        front = str(p.ung_dung_truoc() or "")
        if _HOP_XAC_MINH.search(front) and front.lower() not in _MAN_HINH_KHOA:
            ket = _cho_anh(p, kenh, bao, "máy đang hiện hộp xác minh (%s): Touch ID, Apple Watch, mã khóa" % front[:30])
            if ket not in ("XONG", "ANH_BAO_XONG"):
                _ghi(kenh, "dừng (hộp xác minh)", "%s; ứng dụng ở trước: %s" % (ket, front[:40]))
                return ("CAN_NGUOI_DUNG: Đang hiện hộp xác minh (%s), em không gõ gì và đã báo anh (%s). Anh xác thực xong thì gọi lại op=mo_khoa hoặc op=cho_nguoi_that." % (front, ket))
            front = str(p.ung_dung_truoc() or "")
        if not _dang_khoa(p):
            _ghi(kenh, "bỏ qua (máy không khóa)", "Ứng dụng ở trước: %s" % front[:40])
            return "KHONG_CAN: Máy không ở màn hình khóa (ứng dụng ở trước: %s). Không cần mở khóa, làm việc tiếp." % (front or "không rõ")
        # 4. Duyệt (trừ Toàn quyền).
        if muc != "toan_quyen" and not uy_quyen:
            if B is None:
                return "LOI: thiếu mô-đun duyệt."
            nc = {"host": "Máy tính", "url": "", "tag": "", "ten": ("mo_khoa: mở khóa máy (kênh %s)" % kenh)[:100], "tieu_de": "loginwindow"}
            if not B.dung_duyet(str((a or {}).get("duyet_id") or ""), "may_mo_khoa", nc):
                k = B.xin_duyet("may_mo_khoa", nc, "Mở khóa máy Mac bằng mật khẩu trong Keychain (kênh %s)" % kenh)
                _ghi(kenh, "chờ duyệt", "")
                return ("CAN_DUYET: Mở khóa máy bằng mật khẩu lưu trong Keychain (kênh %s, còn %d lần thử). Anh phải bấm Duyệt trong TISA BOT (có thẻ nổi). "
                        "Nói rõ với anh rồi gọi lại tisa_desktop_do op=mo_khoa duyet_id=\"%s\" sau khi anh duyệt. Chưa duyệt thì KHÔNG làm. "
                        "(Muốn khỏi phải duyệt mỗi lần: anh bật Toàn quyền ở bảng Điều khiển của AI → Máy tính.)" % (kenh, con, k))
        # 5. Lấy mật khẩu từ Keychain (không in, không ghi) và KIỂM đúng với máy TRƯỚC khi gõ: sai thì không gõ, không tốn lần thử.
        pw = _doc_mat_khau()
        if not pw:
            _ghi(kenh, "lỗi (chưa có mật khẩu Keychain)", "")
            return "CHUA_CAI_MAT_KHAU: Keychain chưa có mật khẩu mở khóa của TISA BOT (hoặc không đọc được). Báo anh. %s" % HUONG_DAN_CAI_DAT
        dung = KIEM_MAT_KHAU(pw)
        if dung is False:
            pw = None
            _ghi(kenh, "dừng (mật khẩu lưu không khớp máy)", "Keychain khác mật khẩu đăng nhập hiện tại của máy")
            return ("SAI_MAT_KHAU_LUU: Mật khẩu TISA BOT đang lưu KHÔNG khớp mật khẩu đăng nhập hiện tại của máy (có thể anh vừa đổi mật khẩu máy). Em KHÔNG gõ gì và không tốn lần thử nào. "
                    "Nói với anh: nhập lại mật khẩu máy ở TISA BOT → Điều khiển của AI → Máy tính → Mở khóa máy (có kiểm đúng ngay lúc nhập). Đừng xin mật khẩu trong chat.")
        # 6. Đánh thức màn hình (nếu đang trình bảo vệ màn hình), rồi kiểm lại.
        _danh_thuc(p)
        front = str(p.ung_dung_truoc() or "")
        for _ in range(CHO_O_MAT_KHAU):         # màn hình vừa sáng: chờ tới khi ô mật khẩu sẵn sàng (không gõ vội, phím gõ sớm bị nuốt)
            if front.lower() == "loginwindow":
                break
            if not _dang_khoa(p):                # trong lúc chờ máy đã tự mở (Apple Watch, người ngồi mở): xong
                _ghi(kenh, "bỏ qua (máy tự mở)", "Ứng dụng ở trước: %s" % front[:40])
                pw = None
                return "DA_MO_KHOA: Máy đã được mở khóa (ứng dụng ở trước: %s). Làm việc tiếp." % (front or "không rõ")
            time.sleep(1.0)
            front = str(p.ung_dung_truoc() or "")
        if front.lower() != "loginwindow":
            pw = None
            _ghi(kenh, "dừng (không thấy ô mật khẩu)", "Ứng dụng ở trước: %s" % front[:40])
            return "KHONG_MO_DUOC: Sau khi đánh thức, ứng dụng ở trước là \"%s\" chứ không phải màn hình đăng nhập nên em không gõ. Chụp màn hình xem rồi báo anh.\n%s" % (front or "không rõ", _chup(p))
        # 7. Gõ. Mỗi lần gõ được tính TRƯỚC (lỡ chương trình chết giữa chừng vẫn bị tính). Mật khẩu đã kiểm đúng thì được thử lại MỘT lần trong cùng lần gọi
        #    (lần gõ đầu có thể bị nuốt vì màn hình chưa kịp sáng); chưa kiểm được thì chỉ gõ đúng một lần. Không bao giờ thử mật khẩu khác.
        tong = 2 if dung is True else 1
        that_bai, khoa, sau = 0, True, front
        for lan in range(tong):
            if lan_con_lai()[0] <= 0:
                break
            if lan > 0:
                _ghi(kenh, "thử lại", "mật khẩu đã kiểm đúng nên lần gõ trước chưa vào; xóa ô, đánh thức lại, gõ lần nữa")
                try:
                    p.nhan_phim(set(), "escape")
                except Exception:  # noqa: BLE001
                    pass
                _danh_thuc(p)
                if not _dang_khoa(p):
                    khoa, sau = False, str(p.ung_dung_truoc() or "")
                    break
            that_bai = _dem_doc()["that_bai"] + 1
            _dem_ghi(that_bai)
            try:
                _go_mot_lan(p, kenh, pw)
            except Exception as e:  # noqa: BLE001
                pw = None
                _ghi(kenh, "lỗi (khi gõ)", type(e).__name__)
                return "LOI: Không gõ được (%s). Em đã dừng. Đã tính %d lần thử (%d/%d)." % (type(e).__name__, that_bai, that_bai, TOI_DA)
            time.sleep(CHO_SAU_GO)
            khoa, sau = _cho_mo_khoa(p)
            if not khoa or (_HOP_XAC_MINH.search(sau) and sau.lower() not in _MAN_HINH_KHOA):
                break
        pw = None
        # 8. Kiểm kết quả (cờ khóa của hệ điều hành + ảnh chụp).
        if khoa and _HOP_XAC_MINH.search(sau) and sau.lower() not in _MAN_HINH_KHOA:
            ket = _cho_anh(p, kenh, bao, "sau khi gõ, máy hiện hộp xác minh (%s): Touch ID, mã khóa hoặc xác minh" % sau[:30])
            if ket in ("XONG", "ANH_BAO_XONG"):
                time.sleep(CHO_SAU_GO)
                khoa, sau = _cho_mo_khoa(p)
            else:
                _ghi(kenh, "dừng (hộp xác minh)", "%s; lần %d/%d" % (ket, that_bai, TOI_DA))
                return ("CAN_NGUOI_DUNG: Sau khi gõ, máy hiện hộp xác minh (%s). Em đã báo anh (%s) và dừng, không gõ thêm. Anh xác thực xong thì gọi lại op=mo_khoa (em kiểm tra rồi làm tiếp). Đã dùng %d/%d lần.\n%s"
                        % (sau, ket, that_bai, TOI_DA, _chup(p)))
        anh = _chup(p)
        if khoa and sau.lower() in _MAN_HINH_KHOA:
            _ghi(kenh, "thất bại (vẫn ở màn hình khóa)", "lần %d/%d%s" % (that_bai, TOI_DA, "; mật khẩu đã kiểm đúng" if dung is True else ""))
            if dung is True:
                return ("KHONG_MO_DUOC: Mật khẩu trong Keychain ĐÚNG (đã kiểm với máy) nhưng sau khi gõ máy vẫn ở màn hình khóa. Nên KHÔNG phải sai mật khẩu: có thể màn hình chưa nhận phím hoặc đang hiện hộp xác minh. "
                        "Em đã dừng, không thử mật khẩu khác. Đã dùng %d/%d lần. Xem ảnh rồi báo anh đúng như vậy (đừng nói là sai mật khẩu).\n%s" % (that_bai, TOI_DA, anh))
            return ("KHONG_MO_DUOC: Máy vẫn ở màn hình khóa (có thể sai mật khẩu trong Keychain, hoặc đang hiện hộp xác minh). Em đã dừng, KHÔNG tự thử lại, KHÔNG thử mật khẩu khác. "
                    "Đã dùng %d/%d lần. Xem ảnh rồi báo anh.\n%s" % (that_bai, TOI_DA, anh))
        if khoa:
            _ghi(kenh, "dừng (hộp xác minh)", "Ứng dụng ở trước: %s (lần %d/%d)" % (sau[:40], that_bai, TOI_DA))
            return "CAN_NGUOI_DUNG: Sau khi gõ, máy hiện hộp xác minh (%s). Em dừng, không gõ thêm. Báo anh tự xử lý (Touch ID, mã khóa, xác minh). Đã dùng %d/%d lần.\n%s" % (sau, that_bai, TOI_DA, anh)
        _dem_ghi(0)
        _ghi(kenh, "thành công", "Đã vào máy, ứng dụng ở trước: %s" % sau[:40])
        return "DA_MO_KHOA: Máy đã mở khóa (ứng dụng ở trước: %s). Xem ảnh chụp để chắc đã vào màn hình chính rồi làm việc tiếp.\n%s" % (sau or "không rõ", anh)
    finally:
        _chay.release()


async def mo_khoa(p, a: dict, muc: str, turn) -> str:
    import tisa_bao_anh as BA
    loop = asyncio.get_running_loop()
    return await asyncio.to_thread(_mo_khoa_nen, p, a or {}, muc, turn, None, lambda t: BA.bao(t, loop))


def mo_khoa_tu_dong(p, kenh_cap: str, bao=None) -> str:
    """Mở khóa lại giữa việc nền, CHỈ gọi từ tisa_thuc_giac khi phiên giữ thức đã được kênh `kenh_cap` cấp quyền. Chạy ở luồng nền."""
    return _mo_khoa_nen(p, {}, "toan_quyen", None, uy_quyen=kenh_cap, bao=bao)


# ---------------------------------------------------------------- Cài đặt (ô nhập mật khẩu ở bảng Điều khiển của AI → Máy tính)
def trang_thai() -> dict:
    """Dữ liệu cho mục Mở khóa máy ở Cài đặt. KHÔNG bao giờ trả mật khẩu; chỉ trả có/không."""
    mac = sys.platform == "darwin"
    cau = _cau_hinh()
    con, giay = lan_con_lai()
    cho = [x for x in (cau.get("zalo_cho") or []) if isinstance(x, dict) and x.get("id") and str(x["id"]) not in _zalo_ids()]
    return {"ok": True, "ho_tro": mac, "he": "macOS" if mac else ("Windows" if sys.platform.startswith("win") else sys.platform),
            "da_cai": da_cai_mat_khau() if mac else False, "bat": dang_bat() if mac else False,
            "con_lai": con, "toi_da": TOI_DA, "giay_dung": giay,
            "zalo": [{"id": i, "che": _che(i)} for i in sorted(_zalo_ids())],
            "zalo_cho": [{"id": str(x["id"]), "che": _che(str(x["id"])), "luc": str(x.get("luc") or "")} for x in cho][-3:],
            "nhat_ky": doc_nhat_ky(6)}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    async def _doc_json(request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return d if isinstance(d, dict) else {}

    @app.get("/mo-khoa/trang-thai")
    async def _mk_tt():
        return JSONResponse(await asyncio.to_thread(trang_thai))

    @app.post("/mo-khoa/mat-khau")
    async def _mk_mk(request: Request):
        d = await _doc_json(request)
        pw = d.get("mat_khau")
        r = await asyncio.to_thread(luu_mat_khau, pw if isinstance(pw, str) else "")
        pw = None
        d.clear()
        return JSONResponse(r, status_code=200 if r.get("ok") else 400)

    @app.post("/mo-khoa/xoa-mat-khau")
    async def _mk_xoa():
        return JSONResponse(await asyncio.to_thread(xoa_mat_khau))

    @app.post("/mo-khoa/bat")
    async def _mk_bat(request: Request):
        d = await _doc_json(request)
        bat = bool(d.get("bat"))
        if bat and not await asyncio.to_thread(da_cai_mat_khau):
            return JSONResponse({"ok": False, "loi": "Chưa có mật khẩu. Anh nhập mật khẩu máy trước rồi mới bật."}, status_code=400)
        _luu_cau_hinh(bat=bat)
        _ghi("cài đặt", "đã bật" if bat else "đã tắt", "")
        return JSONResponse({"ok": True, "bat": bat})

    @app.post("/mo-khoa/cho-thu-lai")
    async def _mk_lai():
        _dem_ghi(0)
        _ghi("cài đặt", "đặt lại bộ đếm", "anh bấm Cho thử lại")
        return JSONResponse({"ok": True})

    @app.post("/mo-khoa/zalo")
    async def _mk_zalo(request: Request):
        d = await _doc_json(request)
        sid = str(d.get("id") or "").strip().split(":")[-1]
        hanh = str(d.get("hanh") or "")
        if not sid or len(sid) > 40 or not re.fullmatch(r"[A-Za-z0-9._-]+", sid):
            return JSONResponse({"ok": False, "loi": "Mã Zalo không hợp lệ."}, status_code=400)
        ids = sorted(_zalo_ids())
        if hanh == "them":
            if sid not in ids:
                ids.append(sid)
            _luu_cau_hinh(zalo_ids=ids, zalo_cho=[x for x in (_cau_hinh().get("zalo_cho") or []) if isinstance(x, dict) and x.get("id") != sid])
            _ghi("cài đặt", "xác nhận Zalo của anh", _che(sid))
        elif hanh == "bo":
            _luu_cau_hinh(zalo_ids=[x for x in ids if x != sid])
            _ghi("cài đặt", "bỏ Zalo", _che(sid))
        elif hanh == "bo_cho":
            _luu_cau_hinh(zalo_cho=[x for x in (_cau_hinh().get("zalo_cho") or []) if isinstance(x, dict) and x.get("id") != sid])
        else:
            return JSONResponse({"ok": False, "loi": "Thao tác không hợp lệ."}, status_code=400)
        return JSONResponse({"ok": True})
