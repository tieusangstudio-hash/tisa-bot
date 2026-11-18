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
import re
import subprocess
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
def _zalo_ids() -> set:
    try:
        d = json.loads(TEP_CH.read_text(encoding="utf-8"))
        return {str(x).strip().split(":")[-1] for x in (d.get("zalo_ids") or []) if str(x).strip()}
    except (OSError, ValueError, AttributeError):
        return set()


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
    if turn.get("agent"):
        return False, kenh, "Yêu cầu đến từ cuộc chat với một cộng sự, không phải TISA BOT chính của anh."
    if turn.get("job") or turn.get("team_gate"):
        return False, kenh, "Yêu cầu đến từ việc nền hoặc bước việc nhóm, không có anh đang nhắn."
    if str(turn.get("chat_type") or "") != "private":
        return False, kenh, "Yêu cầu đến từ nhóm chat."
    if kenh == "dashboard":
        return True, "dashboard", ""
    if kenh == "zalo":
        sid = str(turn.get("sender_id") or "").strip().split(":")[-1]
        if sid and sid in _zalo_ids():
            return True, "zalo(%s)" % _che(sid), ""
        return False, "zalo(%s)" % _che(sid), "Tài khoản Zalo này chưa được anh khai là của anh để mở khóa máy."
    return False, kenh, "Kênh này không nằm trong danh sách được mở khóa máy (chỉ dashboard TISA BOT và Zalo của anh)."


# ---------------------------------------------------------------- Keychain
def _doc_mat_khau(dich_vu: str = DICH_VU, tai_khoan: str = "") -> str | None:
    """Đọc mật khẩu từ Keychain bằng lệnh `security`. Trả None nếu không có hoặc không đọc được. KHÔNG bao giờ ghi/in giá trị này."""
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


def da_cai_mat_khau(dich_vu: str = DICH_VU) -> bool:
    """Chỉ kiểm có mục trong Keychain (không lấy giá trị)."""
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


def _mo_khoa_nen(p, a: dict, muc: str, turn, uy_quyen=None, bao=None) -> str:
    # 0. Mật khẩu không bao giờ đi qua tham số của tool.
    vi_pham = sorted(k for k in (a or {}) if str(k).lower() in _THAM_SO_CAM)
    if vi_pham:
        _ghi("không rõ", "từ chối (tham số)", "Có tham số kiểu mật khẩu: %s" % ",".join(vi_pham)[:60])
        return ("TU_CHOI: op=mo_khoa KHÔNG nhận mật khẩu qua tham số (đã gặp: %s). Mật khẩu chỉ lấy từ Keychain của máy. Đừng hỏi hay nhận mật khẩu trong chat; "
                "gọi lại op=mo_khoa không kèm tham số đó." % ", ".join(vi_pham))
    if getattr(p, "ten", "") != "macOS":
        return "KHONG_HO_TRO: op=mo_khoa chỉ dùng cho máy Mac (macOS)."
    # 1. Kênh yêu cầu.
    if uy_quyen:        # việc nền đã được dashboard của anh cấp quyền mở khóa lại (tisa_thuc_giac); vẫn giới hạn 3 lần
        ok, kenh, ly_do = True, "việc nền (quyền cấp từ %s)" % str(uy_quyen)[:30], ""
    else:
        ok, kenh, ly_do = kiem_kenh(turn)
    if not ok:
        _ghi(kenh, "từ chối (kênh)", ly_do)
        return ("TU_CHOI: Không mở khóa máy theo yêu cầu này. %s Chỉ anh nhắn trực tiếp qua dashboard TISA BOT hoặc đúng tài khoản Zalo của anh mới được. "
                "Không tìm cách vòng, không xin mật khẩu." % ly_do)
    if not _chay.acquire(blocking=False):
        return "DANG_CHAY: Đang có một lần mở khóa chạy dở. Chờ nó xong rồi xem màn hình."
    try:
        # 2. Số lần thử.
        con, giay = lan_con_lai()
        if con <= 0:
            _ghi(kenh, "dừng (hết lần thử)", "Đã đủ %d lần thất bại, dừng %d giây" % (TOI_DA, giay))
            return ("DA_DUNG_THU: Đã thử %d lần không mở được nên TISA BOT dừng để không khóa máy lâu hơn (còn khoảng %d phút mới thử lại được). "
                    "Báo anh: anh tự mở khóa, hoặc kiểm tra mật khẩu trong Keychain (mục %s) có đúng không." % (TOI_DA, max(1, giay // 60), DICH_VU))
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
        if front.lower() not in _MAN_HINH_KHOA:
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
                        "Nói rõ với anh rồi gọi lại tisa_desktop_do op=mo_khoa duyet_id=\"%s\" sau khi anh duyệt. Chưa duyệt thì KHÔNG làm." % (kenh, con, k))
        # 5. Đánh thức màn hình (nếu đang trình bảo vệ màn hình), rồi kiểm lại.
        try:
            p.nhan_phim(set(), "escape")        # phím vô hại, chỉ để màn hình sáng và hiện ô mật khẩu
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1.2)
        front = str(p.ung_dung_truoc() or "")
        if front.lower() != "loginwindow":
            _ghi(kenh, "dừng (không thấy ô mật khẩu)", "Ứng dụng ở trước: %s" % front[:40])
            return "KHONG_MO_DUOC: Sau khi đánh thức, ứng dụng ở trước là \"%s\" chứ không phải màn hình đăng nhập nên em không gõ. Chụp màn hình xem rồi báo anh.\n%s" % (front or "không rõ", _chup(p))
        # 6. Lấy mật khẩu từ Keychain (không in, không ghi).
        pw = _doc_mat_khau()
        if not pw:
            pw = None
            _ghi(kenh, "lỗi (chưa có mật khẩu Keychain)", "")
            return "CHUA_CAI_MAT_KHAU: Keychain chưa có mật khẩu mở khóa của TISA BOT (hoặc không đọc được). Báo anh. %s" % HUONG_DAN_CAI
        # 7. Tính một lần thử TRƯỚC khi gõ (lỡ chương trình chết giữa chừng vẫn bị tính), rồi gõ đúng một lần.
        that_bai = _dem_doc()["that_bai"] + 1
        _dem_ghi(that_bai)
        try:
            p.go(pw, "phim")
            pw = None
            p.nhan_phim(set(), "enter")
        except Exception as e:  # noqa: BLE001
            pw = None
            _ghi(kenh, "lỗi (khi gõ)", type(e).__name__)
            return "LOI: Không gõ được (%s). Em đã dừng. Đã tính 1 lần thử (%d/%d)." % (type(e).__name__, that_bai, TOI_DA)
        finally:
            pw = None
        time.sleep(CHO_SAU_GO)
        # 8. Kiểm kết quả bằng ứng dụng ở trước + ảnh chụp.
        sau = str(p.ung_dung_truoc() or "")
        if _HOP_XAC_MINH.search(sau) and sau.lower() not in _MAN_HINH_KHOA:
            ket = _cho_anh(p, kenh, bao, "sau khi gõ, máy hiện hộp xác minh (%s): Touch ID, mã khóa hoặc xác minh" % sau[:30])
            if ket in ("XONG", "ANH_BAO_XONG"):
                time.sleep(CHO_SAU_GO)
                sau = str(p.ung_dung_truoc() or "")
            else:
                _ghi(kenh, "dừng (hộp xác minh)", "%s; lần %d/%d" % (ket, that_bai, TOI_DA))
                return ("CAN_NGUOI_DUNG: Sau khi gõ, máy hiện hộp xác minh (%s). Em đã báo anh (%s) và dừng, không gõ thêm. Anh xác thực xong thì gọi lại op=mo_khoa (em kiểm tra rồi làm tiếp). Đã dùng %d/%d lần.\n%s"
                        % (sau, ket, that_bai, TOI_DA, _chup(p)))
        anh = _chup(p)
        if sau.lower() in _MAN_HINH_KHOA:
            _ghi(kenh, "thất bại (vẫn ở màn hình khóa)", "lần %d/%d" % (that_bai, TOI_DA))
            return ("KHONG_MO_DUOC: Máy vẫn ở màn hình khóa (có thể sai mật khẩu trong Keychain, hoặc đang hiện hộp xác minh). Em đã dừng, KHÔNG tự thử lại, KHÔNG thử mật khẩu khác. "
                    "Đã dùng %d/%d lần. Xem ảnh rồi báo anh.\n%s" % (that_bai, TOI_DA, anh))
        if _HOP_XAC_MINH.search(sau):
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
