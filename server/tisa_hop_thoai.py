"""tisa_hop_thoai.py - (V3.44) Hộp thoại "gốc" của macOS mà bot không gõ phím vào được: hộp chọn tệp và hộp "Cho phép gỡ lỗi từ xa?" của Chrome.

Vì sao cần:
  - Hộp chọn tệp (Mở / Tải lên) chạy ở TIẾN TRÌNH RIÊNG của macOS (com.apple.appkit.xpc.openAndSavePanelService). Phím bot gửi thẳng vào Chrome
    (chuột riêng, CGEventPostToPid) không tới được hộp này: bot bấm Enter, Esc... hộp đứng im (sự cố 22/11, phiên Linh Content).
    Cách chạy được (đã thử trên máy thật): đọc hộp bằng Trợ năng, đặt chữ vào ô bằng Trợ năng, đưa ứng dụng lên trước rồi nhấn phím thật,
    bấm nút Mở bằng AXPress.
  - Hộp "Cho phép gỡ lỗi từ xa?" của Chrome 144+ hiện mỗi khi TISA BOT nối vào Chrome của anh (sau mỗi lần TISA BOT khởi động lại).
    Anh ngồi máy khác thì không ai bấm được. Ở Toàn quyền TISA BOT tự bấm "Cho phép" NHƯNG CHỈ khi chính TISA BOT đang chờ nối
    (tisa_browser_ngoai.KetNoi.dang_noi); ngoài lúc đó không đụng hộp này (có thể là ứng dụng khác xin quyền). Không Toàn quyền: khung
    Trình duyệt trên mọi máy hiện nút "Cho phép" để anh bấm hộ từ xa.

Chỉ macOS. Windows: trả lời rõ là chưa làm.
"""
from __future__ import annotations

import ctypes
import subprocess
import sys
import time
from pathlib import Path

MAC = sys.platform == "darwin"
CHROME = ("Google Chrome", "Microsoft Edge", "Brave Browser", "Chromium")
TIEU_DE_GO_LOI = ("cho phép gỡ lỗi từ xa", "allow remote debugging")
NUT_CHO_PHEP = ("cho phép", "allow")
NUT_HUY = ("huỷ", "hủy", "cancel", "không cho phép", "don't allow", "deny")
NUT_MO = ("mở", "open", "chọn", "choose", "tải lên", "upload", "select")
SAU_TOI_DA = 40          # đi sâu tối đa (hộp của Chrome lồng ~10 cấp)
NUT_TOI_DA = 4000


def _CR():
    import tisa_chuot_rieng as CR
    return CR if CR._nap() else None


# ---------------------------------------------------------------- đọc cây Trợ năng
def _chu(CR, el, ten: str) -> str:
    v = CR._thuoc_tinh(el, ten)
    if not v:
        return ""
    try:
        if CR._P["cf"].CFGetTypeID(v.value) != CR._P["cf"].CFStringGetTypeID():
            return ""
        return CR._chuoi(v.value)
    finally:
        CR._P["cf"].CFRelease(v)


def _bool(CR, el, ten: str):
    v = CR._thuoc_tinh(el, ten)
    if not v:
        return None
    try:
        return bool(CR._P["cf"].CFBooleanGetValue(v.value))
    except Exception:  # noqa: BLE001
        return None
    finally:
        CR._P["cf"].CFRelease(v)


def _con(CR, el, ten: str = "AXChildren") -> list:
    v = CR._thuoc_tinh(el, ten)
    if not v:
        return []
    cf = CR._P["cf"]
    ra = []
    try:
        if cf.CFGetTypeID(v.value) != cf.CFArrayGetTypeID():
            return []
        for i in range(cf.CFArrayGetCount(v.value)):
            e = cf.CFArrayGetValueAtIndex(v.value, i)
            if e:
                cf.CFRetain(e)
                ra.append(e)
    finally:
        cf.CFRelease(v)
    return ra


class Cay:
    """Mọi phần tử của một ứng dụng (cửa sổ → con...), giữ tham chiếu tới khi dong()."""

    def __init__(self, pid: int):
        self.CR = _CR()
        self.pid = int(pid)
        self.app = None
        self.nut: list = []        # [{el, vai, ten, mo_ta, gia_tri, sau, cha}]
        self._giu: list = []
        if not self.CR:
            return
        ag = self.CR._P["ag"]
        cf = self.CR._P["cf"]
        cf.CFArrayGetTypeID.restype = ctypes.c_ulong
        cf.CFRetain.argtypes = [ctypes.c_void_p]
        cf.CFRetain.restype = ctypes.c_void_p
        self.app = ag.AXUIElementCreateApplication(self.pid)

    def cua_so(self) -> list:
        if not self.app:
            return []
        ds = _con(self.CR, self.app, "AXWindows")
        self._giu += ds
        return ds

    def duyet(self, goc, sau_toi_da: int = SAU_TOI_DA) -> list:
        """Duyệt rộng từ `goc`. Trả danh sách nút (mỗi nút có 'cha' là chỉ số nút cha)."""
        CR = self.CR
        ra = []
        hang = [(goc, 0, -1)]
        while hang and len(ra) < NUT_TOI_DA:
            el, sau, cha = hang.pop(0)
            n = {"el": el, "vai": CR._vai_tro(el), "ten": _chu(CR, el, "AXTitle"), "mo_ta": _chu(CR, el, "AXDescription"),
                 "gia_tri": _chu(CR, el, "AXValue"), "sau": sau, "cha": cha}
            ra.append(n)
            if sau < sau_toi_da:
                con = _con(CR, el)
                self._giu += con
                i = len(ra) - 1
                hang += [(c, sau + 1, i) for c in con]
        return ra

    def bam(self, el) -> bool:
        k = self.CR._s("AXPress")
        try:
            return self.CR._P["ag"].AXUIElementPerformAction(el, k) == 0
        finally:
            self.CR._P["cf"].CFRelease(k)

    def dat(self, el, ten: str, gia_tri) -> bool:
        CR = self.CR
        ag, cf = CR._P["ag"], CR._P["cf"]
        ag.AXUIElementSetAttributeValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        ag.AXUIElementSetAttributeValue.restype = ctypes.c_int32
        k = CR._s(ten)
        tao = None
        if isinstance(gia_tri, bool):
            v = ctypes.c_void_p.in_dll(cf, "kCFBooleanTrue" if gia_tri else "kCFBooleanFalse")
        else:
            tao = CR._s(str(gia_tri))
            v = tao
        try:
            return ag.AXUIElementSetAttributeValue(el, k, v) == 0
        finally:
            cf.CFRelease(k)
            if tao:
                cf.CFRelease(tao)

    def len_truoc(self) -> bool:
        return bool(self.app) and self.dat(self.app, "AXFrontmost", True)

    def dong(self):
        if not self.CR:
            return
        cf = self.CR._P["cf"]
        for e in self._giu:
            try:
                cf.CFRelease(e)
            except Exception:  # noqa: BLE001
                pass
        self._giu = []
        if self.app:
            cf.CFRelease(self.app)
            self.app = None


def _ten(n: dict) -> str:
    return (n.get("ten") or n.get("mo_ta") or n.get("gia_tri") or "").strip().lower()


def _khop(t: str, ds) -> bool:
    return any(t == x or t.startswith(x + " ") for x in ds)


def _pid_ung_dung(ten: str) -> list:
    """pid của các tiến trình chính có tên ứng dụng `ten` (vd Google Chrome)."""
    CR = _CR()
    if not CR:
        return []
    ra = []
    for w in CR.liet_ke_cua_so(tat_ca=True):
        if w.get("ung_dung") == ten and w["pid"] not in ra:
            ra.append(w["pid"])
    return ra


# ---------------------------------------------------------------- hộp "Cho phép gỡ lỗi từ xa?" của Chrome
def tim_hop_go_loi(ung_dung: str = "") -> dict | None:
    """{pid, ung_dung, cho_phep: el, huy: el, cay} nếu đang có hộp. Người gọi phải cay.dong()."""
    if not MAC:
        return None
    for ten in ([ung_dung] if ung_dung else CHROME):
        for pid in _pid_ung_dung(ten):
            cay = Cay(pid)
            for w in cay.cua_so():
                for sh in _con(cay.CR, w):
                    cay._giu.append(sh)
                    if cay.CR._vai_tro(sh) != "AXSheet":
                        continue
                    ds = cay.duyet(sh, 16)
                    if not any(_ten(n).startswith(TIEU_DE_GO_LOI) for n in ds if n["vai"] in ("AXHeading", "AXStaticText", "AXGroup")):
                        continue
                    nut = [n for n in ds if n["vai"] == "AXButton"]
                    cp = next((n for n in nut if _khop(_ten(n), NUT_CHO_PHEP)), None)
                    hu = next((n for n in nut if _khop(_ten(n), NUT_HUY)), None)
                    if cp:
                        return {"pid": pid, "ung_dung": ten, "cho_phep": cp["el"], "huy": hu["el"] if hu else None, "cay": cay}
            cay.dong()
    return None


def co_hop_go_loi(ung_dung: str = "") -> bool:
    h = tim_hop_go_loi(ung_dung)
    if h:
        h["cay"].dong()
    return bool(h)


def tra_loi_hop_go_loi(cho_phep: bool, ung_dung: str = "") -> str:
    """Bấm Cho phép / Huỷ trên hộp gỡ lỗi từ xa. Trả 'ok' | 'khong_co' | 'loi'."""
    h = tim_hop_go_loi(ung_dung)
    if not h:
        return "khong_co"
    try:
        el = h["cho_phep"] if cho_phep else h["huy"]
        if not el:
            return "loi"
        return "ok" if h["cay"].bam(el) else "loi"
    finally:
        h["cay"].dong()


# ---------------------------------------------------------------- hộp chọn tệp
def tim_hop_chon_tep(ung_dung: str = "") -> dict | None:
    """Hộp Mở/Tải lên đang mở trong ứng dụng (mặc định: các trình duyệt). {pid, ung_dung, sheet, mo, huy, o_di_toi, cay}."""
    if not MAC:
        return None
    ds_ten = [ung_dung] if ung_dung else list(CHROME)
    for ten in ds_ten:
        for pid in _pid_ung_dung(ten):
            cay = Cay(pid)
            for w in cay.cua_so():
                ung_vien = [w]                      # hộp đứng riêng thành cửa sổ (TextEdit, Finder...)
                for sh in _con(cay.CR, w):          # hoặc gắn vào cửa sổ trang (Chrome: AXSheet)
                    cay._giu.append(sh)
                    if cay.CR._vai_tro(sh) == "AXSheet":
                        ung_vien.insert(0, sh)
                for sh in ung_vien:
                    ds = cay.duyet(sh, 6)
                    nut = [n for n in ds if n["vai"] == "AXButton"]
                    mo = next((n for n in nut if _khop(_ten(n), NUT_MO)), None)
                    hu = next((n for n in nut if _khop(_ten(n), NUT_HUY)), None)
                    if mo and hu and not any(_ten(n).startswith(TIEU_DE_GO_LOI) for n in ds):
                        return {"pid": pid, "ung_dung": ten, "sheet": sh, "mo": mo["el"], "huy": hu["el"], "cay": cay}
            cay.dong()
    return None


def _o_di_toi(cay: Cay, sheet):
    """Ô chữ của hộp con "Đi tới thư mục" (sheet lồng trong hộp chọn tệp), nếu đang mở."""
    for sh in _con(cay.CR, sheet):
        cay._giu.append(sh)
        if cay.CR._vai_tro(sh) == "AXSheet":
            for n in cay.duyet(sh, 3):
                if n["vai"] in ("AXTextField", "AXComboBox"):
                    return sh, n["el"]
    return None, None


def _phim_that(ma: int, flags: int = 0, ung_dung: str = ""):
    """Nhấn phím vào ứng dụng ĐANG Ở TRƯỚC qua System Events (osascript). Đã thử 22/11: hộp chọn tệp nhận Enter từ đường này,
    còn CGEventPost/CGEventPostToPid thì Cmd+Shift+G lọt nhưng Enter trong ô "Đi tới thư mục" bị bỏ qua."""
    dung = []
    if flags & CMD:
        dung.append("command down")
    if flags & SHIFT:
        dung.append("shift down")
    lenh = "key code %d" % int(ma) + ((" using {%s}" % ", ".join(dung)) if dung else "")
    dich = ('tell process "%s" to ' % ung_dung.replace('"', "")) if ung_dung else ""
    try:
        subprocess.run(["/usr/bin/osascript", "-e", 'tell application "System Events" to %s%s' % (dich, lenh)], capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        pass


CMD, SHIFT = 0x100000, 0x20000
K_ENTER, K_G, K_A = 36, 5, 0


def chon_tep(duong_dan: str, tat_ca: bool = False, ung_dung: str = "", bam_mo: bool = True) -> str:
    """Trong hộp chọn tệp đang mở: đi tới `duong_dan` (thư mục hoặc tệp), chọn tất cả tệp nếu tat_ca, bấm Mở. Trả câu báo kết quả."""
    if not MAC:
        return "CHUA_HO_TRO: chọn tệp trong hộp của hệ thống mới làm cho macOS. Trên Windows dùng tisa_browser_do op=upload."
    p = Path(str(duong_dan or "")).expanduser()
    if not str(duong_dan or "").strip() or not p.exists():
        return "LOI: không có \"%s\" trên máy. Đưa đường dẫn đầy đủ tới thư mục hoặc tệp." % duong_dan
    h = tim_hop_chon_tep(ung_dung)
    if not h:
        return ("KHONG_CO_HOP: không thấy hộp chọn tệp nào đang mở%s. Nếu đang làm trong trình duyệt, dùng tisa_browser_do op=upload (không cần hộp)."
                % ((" trong " + ung_dung) if ung_dung else ""))
    cay = h["cay"]
    try:
        cay.len_truoc()                     # phím thật đi vào ứng dụng ở trước
        time.sleep(0.35)
        sh2, o = _o_di_toi(cay, h["sheet"])
        if not o:
            _phim_that(K_G, CMD | SHIFT, h["ung_dung"])    # mở "Đi tới thư mục"
            for _ in range(15):
                time.sleep(0.2)
                sh2, o = _o_di_toi(cay, h["sheet"])
                if o:
                    break
        if not o:
            return "LOI: không mở được ô \"Đi tới thư mục\" trong hộp chọn tệp của %s." % h["ung_dung"]
        cay.dat(o, "AXValue", str(p))
        time.sleep(0.25)
        cay.dat(o, "AXFocused", True)
        time.sleep(0.2)
        cay.len_truoc()
        _phim_that(K_ENTER, 0, h["ung_dung"])
        for _ in range(15):
            time.sleep(0.2)
            if not _o_di_toi(cay, h["sheet"])[1]:
                break
        else:
            return "LOI: hộp \"Đi tới thư mục\" không nhận đường dẫn %s." % p
        if tat_ca and p.is_dir():
            time.sleep(0.4)
            cay.len_truoc()
            _phim_that(K_A, CMD, h["ung_dung"])
            time.sleep(0.6)
        if not bam_mo:
            return "Đã đi tới %s trong hộp chọn tệp của %s%s (chưa bấm Mở)." % (p, h["ung_dung"], ", đã chọn tất cả" if tat_ca else "")
        if _bool(cay.CR, h["mo"], "AXEnabled") is False:
            return ("LOI: nút Mở còn mờ (chưa chọn tệp nào). %s" % ("Thêm tat_ca=true để chọn hết tệp trong thư mục, hoặc đưa đường dẫn tới đúng một tệp."
                                                                     if p.is_dir() else "Tệp có thể không đúng loại trang cho phép."))
        cay.bam(h["mo"])
        for _ in range(20):
            time.sleep(0.25)
            h2 = tim_hop_chon_tep(h["ung_dung"])
            if not h2:
                so = len([x for x in p.iterdir() if x.is_file() and not x.name.startswith(".")]) if (tat_ca and p.is_dir()) else 1
                return "Đã chọn %s và bấm Mở: %d tệp đã đưa vào %s. Chụp màn hình để kiểm tra trang đã nhận tệp." % (p, so, h["ung_dung"])
            h2["cay"].dong()
        return "LOI: đã bấm Mở nhưng hộp chọn tệp vẫn còn. Chụp màn hình xem hộp đang báo gì."
    finally:
        cay.dong()


def huy_hop_chon_tep(ung_dung: str = "") -> str:
    h = tim_hop_chon_tep(ung_dung)
    if not h:
        return "khong_co"
    try:
        return "ok" if h["cay"].bam(h["huy"]) else "loi"
    finally:
        h["cay"].dong()


def chay_osascript_thu(lenh: str) -> str:      # dùng khi chẩn đoán bằng tay
    r = subprocess.run(["osascript", "-e", lenh], capture_output=True, text=True, timeout=20)
    return (r.stdout or r.stderr).strip()
