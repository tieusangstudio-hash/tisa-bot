"""tisa_cai_quyen.py - Cài đặt quyền điều khiển máy LẦN ĐẦU cho học viên (macOS và Windows) và hướng dẫn TỪNG BƯỚC khi còn thiếu quyền.

Mục tiêu (chủ yêu cầu 18/11/2026): học viên cài TISA BOT xong, ra lệnh cho AI điều khiển máy, AI KHÔNG được trả lời "em chưa đọc được màn hình, chưa bấm được" rồi dừng.
Vì thế khi TISA BOT khởi động lần đầu (và mỗi khi AI gặp thiếu quyền) nó TỰ làm phần máy làm được, và hướng dẫn người dùng phần còn lại.

Điều phải nói thật: macOS KHÔNG cho phần mềm tự bật quyền cho chính nó (Trợ năng, Ghi màn hình, Truy cập toàn bộ ổ đĩa, Tự động hóa là do người dùng bấm công tắc).
Phần máy làm được thay người dùng:
  1. Gọi đúng hộp xin quyền của hệ điều hành (AXIsProcessTrustedWithOptions, CGRequestScreenCaptureAccess) để hộp "Mở Cài đặt Hệ thống" hiện sẵn.
  2. "Chạm" vào Màn hình nền, Tài liệu, Tải xuống và hỏi Tự động hóa Chrome / System Events để macOS hiện hộp xin quyền đúng lúc, người dùng chỉ bấm Cho phép.
  3. Mở thẳng đúng trang Cài đặt, chép sẵn đường dẫn chương trình vào clipboard (để dán vào hộp chọn tệp), và đợi tới khi người dùng bật xong rồi báo lại.
  4. Hướng dẫn từng bước thật chi tiết (chữ trên màn hình, bấm đâu), cho cả macOS và Windows, qua dashboard, chuông thông báo và qua AI.

Giới hạn giữ nguyên (không bỏ): không xóa tệp của người dùng; không bấm bước tiền bạc (thanh toán, mua, nạp, nâng gói); không tự vượt mật khẩu/OTP/CAPTCHA/Touch ID.

  trang_thai(p)                  danh sách mục quyền: {id, ten, ok (True/False/None), bat_buoc}
  huong_dan(p, ma=None)          văn bản hướng dẫn từng bước cho các mục còn thiếu (hoặc một mục)
  yeu_cau_he_thong(p)            gọi hộp xin quyền + chạm thư mục + Tự động hóa (macOS); Windows: không cần
  chay_lan_dau(p, bao)           làm một lần lúc cài; thread nền đợi người dùng bật xong, báo đủ quyền
"""
from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "dieu-khien-may"
TEP_LAN_DAU = DIR / "cai-quyen-lan-dau.json"
CHO_BAO_THIEU = 120          # giây: sau khi hiện hộp xin quyền, còn thiếu thì gửi hướng dẫn từng bước
DOI_TOI_DA = 20 * 60         # giây: thời gian đợi người dùng bật xong
CHU_KY = 5.0
_lock = threading.Lock()
_dang_cho = {"thread": None}


def _he() -> str:
    return "mac" if sys.platform == "darwin" else ("win" if sys.platform == "win32" else "khac")


# ---------------------------------------------------------------- đọc trạng thái
def _chay(cmd, timeout=6):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except (OSError, subprocess.SubprocessError):
        return 1, "", ""


def _doc_duoc(duong_dan: Path):
    """True đọc được, False bị macOS chặn (Operation not permitted), None không có thư mục."""
    try:
        if not duong_dan.exists():
            return None
        os.listdir(duong_dan)
        return True
    except PermissionError:
        return False
    except OSError:
        return None


def _tu_dong_hoa_nhe(bundle_id: str) -> bool | None:
    """Hỏi macOS xem đã được phép Tự động hóa ứng dụng đó chưa MÀ KHÔNG hiện hộp xin quyền (AEDeterminePermissionToAutomateTarget, askUserIfNeeded=False).
    True đã cho, False bị từ chối (-1743), None chưa hỏi lần nào (-1744) hoặc ứng dụng không chạy / không rõ."""
    try:
        ct = ctypes.CDLL("/System/Library/Frameworks/CoreServices.framework/CoreServices")

        class AEDesc(ctypes.Structure):
            _fields_ = [("tipo", ctypes.c_uint32), ("data", ctypes.c_void_p)]
        ct.AECreateDesc.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_long, ctypes.POINTER(AEDesc)]
        ct.AECreateDesc.restype = ctypes.c_int16
        ct.AEDeterminePermissionToAutomateTarget.argtypes = [ctypes.POINTER(AEDesc), ctypes.c_uint32, ctypes.c_uint32, ctypes.c_ubyte]
        ct.AEDeterminePermissionToAutomateTarget.restype = ctypes.c_int32
        d = AEDesc()
        b = bundle_id.encode()
        if ct.AECreateDesc(0x62756E64, b, len(b), ctypes.byref(d)) != 0:       # 'bund'
            return None
        st = ct.AEDeterminePermissionToAutomateTarget(ctypes.byref(d), 0x2A2A2A2A, 0x2A2A2A2A, 0)
        if st == 0:
            return True
        if st == -1743:
            return False
        return None
    except Exception:  # noqa: BLE001
        return None


def _tu_dong_hoa(app: str) -> bool | None:
    """Tự động hóa (Apple Events): hỏi nhẹ một ứng dụng. -1743 = bị từ chối."""
    rc, out, err = _chay(["/usr/bin/osascript", "-e", 'tell application "%s" to get name' % app], 8)
    if rc == 0:
        return True
    if "-1743" in err or "not authorized" in err.lower():
        return False
    return None


def trang_thai(p) -> list:
    """Các mục quyền cần có. ok: True đã có, False chưa có, None không rõ / không áp dụng."""
    he = _he()
    ds = []
    if he == "mac":
        q = p.quyen() if p is not None else {}
        ds.append({"id": "tro_nang", "ten": "Trợ năng (điều khiển chuột, bàn phím)", "ok": bool(q.get("tro_nang")), "bat_buoc": True})
        ds.append({"id": "man_hinh", "ten": "Ghi màn hình (nhìn và quay màn hình)", "ok": q.get("ghi_man_hinh"), "bat_buoc": True})
        h = Path.home()
        for ma, ten, d in (("thu_muc_man_hinh_nen", "Thư mục Màn hình nền", h / "Desktop"), ("thu_muc_tai_lieu", "Thư mục Tài liệu", h / "Documents"), ("thu_muc_tai_xuong", "Thư mục Tải xuống", h / "Downloads")):
            ds.append({"id": ma, "ten": ten, "ok": _doc_duoc(d), "bat_buoc": False})
        ds.append({"id": "toan_bo_o_dia", "ten": "Truy cập toàn bộ ổ đĩa (đọc, sao chép mọi thư mục)", "ok": _doc_duoc(h / "Library" / "Safari"), "bat_buoc": False})
        ds.append({"id": "tu_dong_hoa", "ten": "Tự động hóa (điều khiển ứng dụng, Chrome)", "ok": _tu_dong_hoa_nhe("com.apple.systemevents"), "bat_buoc": True})
    elif he == "win":
        ds.append({"id": "dieu_khien", "ten": "Điều khiển chuột, bàn phím, chụp màn hình", "ok": True, "bat_buoc": True})
    try:
        import tisa_browser_ngoai as N
        co_chrome = N.co_tren_may("chrome")
        cong = N.doc_cong("chrome") if co_chrome else None
        ds.append({"id": "chrome_tu_xa", "ten": "Google Chrome cho TISA BOT dùng (chrome://inspect/#remote-debugging)", "ok": (bool(cong) if co_chrome else None), "bat_buoc": False})
    except Exception:  # noqa: BLE001
        pass
    return ds


def thieu(ds: list, chi_bat_buoc: bool = False) -> list:
    return [x for x in ds if x["ok"] is False and (x["bat_buoc"] or not chi_bat_buoc)]


# ---------------------------------------------------------------- hướng dẫn từng bước
def _chuong_trinh(p) -> str:
    try:
        return str(p.quyen().get("chuong_trinh") or os.path.realpath(sys.executable))
    except Exception:  # noqa: BLE001
        return os.path.realpath(sys.executable)


def _buoc_mac(ma: str, chuong_trinh: str) -> list:
    ten_ct = Path(chuong_trinh).name
    cd = "Cài đặt Hệ thống (System Settings)"
    if ma == "tro_nang":
        return [
            "Bấm biểu tượng quả táo ở góc TRÊN BÊN TRÁI màn hình, chọn %s." % cd,
            "Ở cột bên trái, kéo xuống chọn \"Quyền riêng tư & Bảo mật\" (Privacy & Security), rồi bấm vào mục \"Trợ năng\" (Accessibility) ở khung bên phải.",
            "Tìm dòng \"%s\" (hoặc \"TISA BOT\") trong danh sách. Có thì BẬT công tắc sang màu xanh. Chưa có dòng nào: bấm dấu + ở góc dưới danh sách, nhấn Cmd+Shift+G, nhấn Cmd+V (em đã chép sẵn đường dẫn %s), bấm Enter, chọn tệp rồi bấm Mở." % (ten_ct, chuong_trinh),
            "Macbook hỏi mật khẩu máy hoặc Touch ID thì anh/chị nhập (em không nhìn thấy và không nhập thay được). Bật xong, quay lại nói \"xong\" hoặc đợi em tự nhận ra.",
        ]
    if ma == "man_hinh":
        return [
            "Mở %s > \"Quyền riêng tư & Bảo mật\" > \"Ghi màn hình & Âm thanh hệ thống\" (Screen & System Audio Recording)." % cd,
            "BẬT công tắc ở dòng \"%s\" (hoặc \"TISA BOT\"). Chưa có dòng: bấm dấu +, Cmd+Shift+G, Cmd+V (đường dẫn %s đã chép sẵn), Enter, chọn Mở." % (ten_ct, chuong_trinh),
            "Hệ thống hỏi \"Thoát & mở lại\" (Quit & Reopen) thì bấm đồng ý; TISA BOT sẽ tự mở lại. Mở lại xong gõ lại lệnh cho AI.",
        ]
    if ma == "toan_bo_o_dia":
        return [
            "Mở %s > \"Quyền riêng tư & Bảo mật\" > \"Truy cập toàn bộ ổ đĩa\" (Full Disk Access)." % cd,
            "BẬT công tắc ở dòng \"%s\" (hoặc \"TISA BOT\"); chưa có dòng thì bấm dấu +, Cmd+Shift+G, Cmd+V (đường dẫn %s), Enter, chọn Mở." % (ten_ct, chuong_trinh),
            "Làm bước này để AI sao chép, đọc mọi thư mục (không có quyền xóa: TISA BOT vẫn bị chặn xóa tệp). Có thể bỏ qua nếu chỉ dùng Màn hình nền, Tài liệu, Tải xuống.",
        ]
    if ma.startswith("thu_muc_"):
        ten = {"thu_muc_man_hinh_nen": "Màn hình nền (Desktop)", "thu_muc_tai_lieu": "Tài liệu (Documents)", "thu_muc_tai_xuong": "Tải xuống (Downloads)"}[ma]
        return [
            "Khi macOS hiện hộp \"%s muốn truy cập các tệp trong thư mục %s\" thì bấm \"Cho phép\" (Allow)." % (ten_ct, ten),
            "Không thấy hộp: mở %s > \"Quyền riêng tư & Bảo mật\" > \"Tệp và Thư mục\" (Files & Folders), tìm \"%s\" và BẬT thư mục %s." % (cd, ten_ct, ten),
        ]
    if ma == "tu_dong_hoa":
        return [
            "Khi macOS hỏi \"%s muốn điều khiển System Events / Google Chrome\" thì bấm \"OK\" (Cho phép)." % ten_ct,
            "Không thấy hộp: mở %s > \"Quyền riêng tư & Bảo mật\" > \"Tự động hóa\" (Automation), tìm \"%s\" và BẬT System Events, Google Chrome, Finder." % (cd, ten_ct),
        ]
    if ma == "chrome_tu_xa":
        return [
            "Mở Google Chrome, gõ vào thanh địa chỉ: chrome://inspect/#remote-debugging rồi nhấn Enter.",
            "BẬT mục \"Allow remote debugging for this browser instance\" (cho phép gỡ lỗi từ xa cho trình duyệt này).",
            "Chrome hiện hộp hỏi cho TISA BOT nối vào: bấm \"Cho phép\" (Allow). Chỉ cần bấm một lần cho tới khi đóng Chrome.",
            "Anh/chị có nhiều hồ sơ Chrome: chọn đúng hồ sơ muốn AI dùng (bảng Điều khiển máy tính > Chọn hồ sơ Chrome). TISA BOT chỉ mở trang trong hồ sơ đã chọn.",
        ]
    return []


def _buoc_win(ma: str) -> list:
    if ma == "chrome_tu_xa":
        return _buoc_mac("chrome_tu_xa", "")
    return [
        "Windows không có công tắc quyền riêng cho việc điều khiển chuột, bàn phím, chụp màn hình: TISA BOT dùng được ngay.",
        "Nếu Windows hiện hộp \"Bạn có muốn cho phép ứng dụng này thực hiện thay đổi?\" (UAC) thì bấm \"Có\" (Yes).",
        "Nếu phần mềm diệt virus hoặc Windows Defender chặn: mở Bảo mật Windows > Bảo vệ khỏi vi-rút & mối đe dọa > Quản lý cài đặt > Loại trừ, thêm thư mục TISA BOT.",
        "Cửa sổ ứng dụng đang chạy bằng quyền quản trị (Run as administrator) thì TISA BOT chưa bấm vào được: chạy lại ứng dụng đó bình thường, hoặc chạy TISA BOT bằng quyền quản trị.",
    ]


def huong_dan(p, ma: str | None = None, ds: list | None = None) -> str:
    """Văn bản hướng dẫn từng bước cho các mục còn thiếu (hoặc một mục `ma`). Dùng để AI đọc lại cho người dùng, hoặc hiện trên dashboard."""
    he = _he()
    ds = trang_thai(p) if ds is None else ds
    chon = [x for x in ds if (x["id"] == ma if ma else x["ok"] is False)]
    if not chon:
        return "Đã đủ quyền (xem màn hình, ghi màn hình, điều khiển chuột bàn phím, thư mục). Làm tiếp được." if not ma else "Mục này đã ổn."
    ct = _chuong_trinh(p)
    out = []
    for i, x in enumerate(chon, 1):
        buoc = _buoc_mac(x["id"], ct) if he == "mac" or x["id"] == "chrome_tu_xa" else _buoc_win(x["id"])
        out.append("%d. %s%s" % (i, x["ten"], " (bắt buộc)" if x["bat_buoc"] else " (nên bật)"))
        out += ["   Bước %d: %s" % (j, b) for j, b in enumerate(buoc, 1)]
    return "\n".join(out)


# ---------------------------------------------------------------- hộp xin quyền của hệ điều hành
def _hop_xin_tro_nang() -> bool:
    try:
        ax = ctypes.CDLL("/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices")
        cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        vp = ctypes.c_void_p
        khoa = vp.in_dll(ax, "kAXTrustedCheckOptionPrompt")
        dung = vp.in_dll(cf, "kCFBooleanTrue")
        cf.CFDictionaryCreate.argtypes = [vp, ctypes.POINTER(vp), ctypes.POINTER(vp), ctypes.c_long, vp, vp]
        cf.CFDictionaryCreate.restype = vp
        ax.AXIsProcessTrustedWithOptions.argtypes = [vp]
        ax.AXIsProcessTrustedWithOptions.restype = ctypes.c_bool
        d = cf.CFDictionaryCreate(None, (vp * 1)(khoa.value), (vp * 1)(dung.value), 1, None, None)
        return bool(ax.AXIsProcessTrustedWithOptions(d))
    except Exception:  # noqa: BLE001
        return False


def _hop_xin_man_hinh() -> bool:
    try:
        ax = ctypes.CDLL("/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices")
        f = ax.CGRequestScreenCaptureAccess
        f.restype = ctypes.c_bool
        return bool(f())
    except Exception:  # noqa: BLE001
        return False


def yeu_cau_he_thong(p) -> dict:
    """Làm những gì máy làm được để hộp xin quyền hiện ra đúng lúc. Trả {"da_goi": [...]}. Windows không cần gì."""
    da = []
    if _he() != "mac":
        return {"da_goi": da}
    q = p.quyen() if p is not None else {}
    if not q.get("tro_nang"):
        _hop_xin_tro_nang()
        da.append("hộp xin Trợ năng")
    if q.get("ghi_man_hinh") is False:
        _hop_xin_man_hinh()
        da.append("hộp xin Ghi màn hình")
    h = Path.home()
    for d in (h / "Desktop", h / "Documents", h / "Downloads"):
        if _doc_duoc(d) is not None:          # chạm vào để macOS hiện hộp "muốn truy cập các tệp trong thư mục..."
            da.append("chạm " + d.name)
    for app in ("System Events",) + (("Google Chrome",) if Path("/Applications/Google Chrome.app").exists() else ()):
        _tu_dong_hoa(app)                     # lần đầu macOS hiện hộp "muốn điều khiển ..."
        da.append("hỏi Tự động hóa " + app)
    try:         # chép sẵn đường dẫn chương trình để dán vào hộp chọn tệp (Cmd+Shift+G, Cmd+V)
        subprocess.run(["/usr/bin/pbcopy"], input=_chuong_trinh(p).encode(), timeout=4)
    except (OSError, subprocess.SubprocessError):
        pass
    return {"da_goi": da}


def mo_cai_dat(loai: str) -> None:
    if _he() != "mac":
        return
    pane = {"tro_nang": "Privacy_Accessibility", "man_hinh": "Privacy_ScreenCapture", "toan_bo_o_dia": "Privacy_AllFiles", "tu_dong_hoa": "Privacy_Automation"}.get(loai, "Privacy_Accessibility")
    _chay(["/usr/bin/open", "x-apple.systempreferences:com.apple.preference.security?" + pane], 6)


# ---------------------------------------------------------------- lần đầu
def da_chay_lan_dau() -> bool:
    return TEP_LAN_DAU.exists()


def _ghi_lan_dau(d: dict) -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_LAN_DAU.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def _vong_cho(p, bao, bat_dau: float) -> None:
    da_gui_thieu = False
    while time.time() - bat_dau < DOI_TOI_DA:
        time.sleep(CHU_KY)
        ds = trang_thai(p)
        thieu_bb = thieu(ds, True)
        if not thieu_bb:
            if bao:
                bao("TISA BOT đã đủ quyền điều khiển máy: xem màn hình, ghi màn hình, điều khiển chuột bàn phím. Anh/chị ra lệnh cho AI được rồi.")
            _ghi_lan_dau({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "ket_qua": "đủ quyền bắt buộc", "thieu_nen_bat": [x["id"] for x in thieu(ds)]})
            return
        if not da_gui_thieu and time.time() - bat_dau >= CHO_BAO_THIEU:
            da_gui_thieu = True
            if bao:
                bao("TISA BOT còn thiếu quyền để điều khiển máy: %s. Mở Cài đặt Hệ thống > Quyền riêng tư & Bảo mật và bật cho TISA BOT; hoặc nhắn AI \"hướng dẫn cấp quyền\" để được chỉ từng bước." % ", ".join(x["ten"].split(" (")[0] for x in thieu_bb))
            for x in thieu_bb[:1]:
                mo_cai_dat(x["id"])
    _ghi_lan_dau({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "ket_qua": "hết giờ đợi", "con_thieu": [x["id"] for x in thieu(trang_thai(p), True)]})


def chay_lan_dau(p, bao=None, ep: bool = False) -> dict:
    """Chạy MỘT lần khi cài (hoặc ép chạy lại). Gọi hộp xin quyền, mở đúng trang Cài đặt cho mục còn thiếu, rồi thread nền đợi người dùng bật xong. Không chặn."""
    with _lock:
        if da_chay_lan_dau() and not ep:
            return {"ok": True, "bo_qua": "đã chạy lần đầu"}
        if _dang_cho["thread"] is not None and _dang_cho["thread"].is_alive():
            return {"ok": True, "bo_qua": "đang đợi"}
        ds = trang_thai(p)
        res = {"ok": True, "he": _he(), "da_goi": yeu_cau_he_thong(p)["da_goi"], "thieu": [x["id"] for x in thieu(ds, True)]}
        _ghi_lan_dau({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "ket_qua": "đang đợi người dùng bật", "thieu": res["thieu"]})
        if res["thieu"]:
            mo_cai_dat(res["thieu"][0])
            t = threading.Thread(target=_vong_cho, args=(p, bao, time.time()), daemon=True, name="tisa-cai-quyen")
            _dang_cho["thread"] = t
            t.start()
        else:
            _ghi_lan_dau({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "ket_qua": "đủ quyền bắt buộc", "thieu_nen_bat": [x["id"] for x in thieu(ds)]})
        return res
