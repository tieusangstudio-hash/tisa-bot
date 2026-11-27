"""tisa_nhieu_may.py - NHIỀU MÁY: một bộ não, nhiều máy chạy TISA BOT, một máy làm chủ (chủ yêu cầu 21/11/2026; có trong bản học viên từ V3.72).

Chủ muốn: máy yếu lo trả lời khách và viết content, máy mạnh dựng video; đi xa thì tắt máy công ty, bật máy khác làm máy chủ; đổi vai chỉ bằng
cài đặt trong TISA BOT, tên miền cài một lần, máy phụ nhân bản từ máy chính thật đơn giản, chạy được cả Mac và Windows.

Cách làm:
  - TRẠM TISA (Cloudflare Worker của chính chủ, tram/tram-tisa.js) giữ sổ máy, vai, kho tệp đã mã hóa, và làm CỔNG cho tên miền.
  - Mỗi máy giữ 0..n VAI: cong (tên miền trỏ về máy này), khach (kênh nhận tin: Telegram, Zalo...), lich (lịch tự động, vòng nền, Kanban),
    bang (đồng bộ bảng Đội Quân trên Cloudflare), viec_nang (dựng video, việc nặng). Máy chủ = máy giữ "cong".
    Bốn chế độ trong Cài đặt chỉ là bốn cách chia vai: Máy chủ (máy này giữ hết), Máy phụ (máy kia giữ hết), Chạy chung (máy chủ giữ cong/khach/lich/bang,
    máy phụ giữ viec_nang), Chia ba (cho ai có 3 máy: máy chủ giữ cong/khach/bang = mặt tiền, máy lịch giữ lich, máy nặng giữ viec_nang).
    Trạm và sổ vai không giới hạn số máy; chế độ chỉ là bộ chia sẵn, ai muốn chia khác thì dùng "Tự chia từng phần việc" (dat_vai).
  - Máy KHÔNG giữ vai nào thì tắt đúng những thứ mà cơ chế CÁCH LY của Chuyển máy (tisa_chuyen_may.ap_cach_ly) vẫn tắt: kênh nhận tin, Zalo MCP,
    lịch tự động, bảng Đội Quân. Vai đổi thì máy ghi lại vai mới rồi KHỞI ĐỘNG LẠI; lần khởi động sau áp vai trước khi mở cấu hình (an toàn,
    không bị máy chủ ghi đè settings đang nằm trong bộ nhớ).
  - Vai có SỐ NHIỆM KỲ ở Trạm: máy cũ mất mạng lúc bị tiếp quản, có mạng lại thấy nhiệm kỳ mới hơn là tự buông vai.
  - BỘ NÃO đồng bộ hai chiều theo tệp, MÃ HÓA ngay trên máy (AES-GCM, khóa từ mật khẩu bộ não qua scrypt). Trạm chỉ thấy bản mã.
    Không đồng bộ: kho nặng (video, ảnh lớn, âm thanh, dữ liệu làm dở), CSDL, thư mục máy tự sinh (.claude, .tisa, node_modules...).
    Hai máy cùng sửa một tệp: bản đã lên Trạm trước thắng, bản còn lại cất vào <bộ não>/_xung-dot/ để không mất.
  - CẤU HÌNH (MCP, kết nối, settings) đi theo bộ não: máy chủ đẩy bản mới lên (một người ghi, không xung đột), máy khác nhận về và áp ở lần khởi động sau.
  - NHÂN BẢN máy phụ: máy chính đóng gói Chuyển máy (nền tảng, không kho nặng), tải lên R2 qua Trạm, sinh mã ghép 8 ký tự.
    Máy mới dán "dòng ghép" + mật khẩu bộ não: tải gói, áp dụng (cơ chế Chuyển máy sẵn có: đổi đường dẫn Mac/Windows, cất bản cũ), khởi động lại thành máy phụ.

Không bao giờ: lưu mật khẩu bộ não (chỉ lưu khóa dẫn xuất, đã mã hóa bằng khóa máy), gửi khóa máy chủ lên Trạm, tự tiếp quản khi chủ chưa bấm.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import platform
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import tisa_chuyen_may as cm

# Bộ cài thử (launchd) đặt PATH thiếu /usr/sbin: `screencapture` (chụp màn hình) và `scutil` nằm ở đó nên AI không chụp được
# màn hình, không đọc được tên máy (thấy 21/11/2026 trên M4 của chủ). Bổ sung ngay lúc nạp, mọi tiến trình con (kể cả AI) đều nhận.
if sys.platform == "darwin":
    _pt = os.environ.get("PATH", "").split(os.pathsep)
    _them = [d for d in ("/usr/bin", "/bin", "/usr/sbin", "/sbin") if d not in _pt]
    if _them:
        os.environ["PATH"] = os.pathsep.join([p for p in _pt if p] + _them)

try:    # ở cấp module: tệp dùng `from __future__ import annotations`, FastAPI đọc chú thích kiểu theo tên TOÀN CỤC.
    from fastapi import Request    # Import trong gan() thì `req: Request` bị hiểu là tham số ?req= và mọi POST trả 422 "Field required".
except Exception:  # noqa: BLE001 - dòng lệnh, test thuần không cần FastAPI
    Request = None

STATE_DIR = cm.STATE_DIR
BRAINS_DIR = cm.BRAINS_DIR
ROOT = cm.ROOT
NM = STATE_DIR / "nhieu-may"
CAU_HINH = NM / "cau-hinh.json"
VAI_TT = NM / "vai.json"
DONG_BO = NM / "dong-bo.json"
CHI_MUC = NM / "chi-muc.json"
NHAT_KY = NM / "nhat-ky.jsonl"
THUNG_RAC = NM / "thung-rac"
CHO_CAU_HINH = NM / "cau-hinh-cho-ap"

VAI = ("cong", "khach", "lich", "bang", "viec_nang")
TEN_VAI = {"cong": "Tên miền chính trỏ về", "khach": "Nhận khách (Zalo, Telegram...)", "lich": "Lịch tự động, việc nền",
           "bang": "Bảng Đội Quân", "viec_nang": "Dựng video, việc nặng"}
NHIP_GIAY = 30
DONG_BO_GIAY = 120
TEP_TOI_DA = 90 * 1024 * 1024
LUOT_TAI_LEN = 3000                 # tối đa số tệp đẩy lên mỗi vòng (vòng sau làm tiếp)
PHAN_GOI = 64 * 1024 * 1024
BO_THU_MUC_NAO = set(cm.BO_THU_MUC) | {".claude", ".tisa", "_xung-dot", ".obsidian", ".trash", ".Trash"}
# Cấu hình đi cùng (tên trong STATE_DIR). Chỉ máy chủ đẩy lên.
TEP_CAU_HINH = ("settings.json", "mcp_servers.json", ".oauth_mcp.json", "chatbots.json")
# Khóa settings thuộc về TỪNG máy: không đẩy lên, không ghi đè khi nhận.
KHOA_RIENG_MAY = ("remote_tunnel", "schedules_off_here", "backup") + tuple(cm.KENH_NHAN_TIN)
TIEN_TO_CAU_HINH = "_cau-hinh/"
_WIN_CAM = re.compile(r'[<>:"|?*\x00-\x1f]')

_khoa = threading.RLock()
_viec = {}                          # việc nền đang chạy cho giao diện: {"loai", "phan_tram", "chu", "loi", "xong", "ket_qua"}
_tt = {"nhip": None, "loi_nhip": "", "luc_nhip": 0, "dong_bo": {}, "dang_dong_bo": False}
_luong = {"chay": False}


# ================================================================ tiện ích
def _doc(p: Path, mac_dinh=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return mac_dinh


def _ghi(p: Path, d) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_name(p.name + ".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        os.chmod(tam, 0o600)
    except OSError:
        pass
    os.replace(tam, p)


def nhat_ky(viec: str, **chi_tiet) -> None:
    try:
        NM.mkdir(parents=True, exist_ok=True)
        with open(NHAT_KY, "a", encoding="utf-8") as f:
            f.write(json.dumps({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "viec": viec, **chi_tiet}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _fernet():
    """Khóa riêng của Nhiều máy (NM/.khoa), KHÔNG dùng .secret_key chung: gói nhân bản mang .secret_key của máy chính sang máy phụ,
    áp gói xong máy phụ sẽ không giải được khóa Trạm của chính nó. Thư mục nhieu-may/ không bao giờ vào gói."""
    from cryptography.fernet import Fernet
    p = NM / ".khoa"
    if not p.is_file():
        NM.mkdir(parents=True, exist_ok=True)
        p.write_bytes(Fernet.generate_key())
        try:
            os.chmod(p, 0o600)
        except OSError:
            pass
    return Fernet(p.read_bytes().strip())


def _ma_hoa_may(s: str) -> str:
    return "nm:" + _fernet().encrypt(s.encode()).decode()


def _giai_may(s: str) -> str:
    if not s or not s.startswith("nm:"):
        return ""
    try:
        return _fernet().decrypt(s[3:].encode()).decode()
    except Exception:  # noqa: BLE001
        return ""


def cau_hinh() -> dict:
    return _doc(CAU_HINH, {}) or {}


def dang_bat() -> bool:
    c = cau_hinh()
    return bool(c.get("bat") and c.get("tram") and c.get("may_id"))


def _he() -> str:
    return {"darwin": "mac", "win32": "windows"}.get(sys.platform, sys.platform)


def ten_may() -> str:
    return cau_hinh().get("ten") or platform.node() or "Máy"


# ================================================================ mã hóa bộ não
def khoa_tu_mat_khau(mat_khau: str, muoi: bytes) -> bytes:
    return hashlib.scrypt(mat_khau.encode("utf-8"), salt=muoi, n=2 ** 15, r=8, p=1, maxmem=128 * 1024 * 1024, dklen=32)


def _aes(khoa: bytes):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    return AESGCM(khoa)


def ma_hoa(khoa: bytes, du_lieu: bytes, aad: bytes = b"tisa-nm") -> bytes:
    n = os.urandom(12)
    return n + _aes(khoa).encrypt(n, du_lieu, aad)


def giai_ma(khoa: bytes, goi: bytes, aad: bytes = b"tisa-nm") -> bytes:
    return _aes(khoa).decrypt(goi[:12], goi[12:], aad)


MAU = b"tisa-nhieu-may-kiem-mat-khau"


def tao_mau_kiem(khoa: bytes) -> str:
    return base64.b64encode(ma_hoa(khoa, MAU, b"kiem")).decode()


def dung_mat_khau(khoa: bytes, mau_kiem: str) -> bool:
    try:
        return giai_ma(khoa, base64.b64decode(mau_kiem), b"kiem") == MAU
    except Exception:  # noqa: BLE001 - sai khóa ném InvalidTag
        return False


def _khoa_nao() -> bytes:
    k = _giai_may(cau_hinh().get("khoa_nao") or "")
    if not k:
        raise ValueError("Máy này chưa có khóa bộ não (chưa ghép với Trạm).")
    return base64.b64decode(k)


def dau_tep(khoa: bytes, du_lieu: bytes) -> str:
    return hmac.new(khoa, du_lieu, hashlib.sha256).hexdigest()[:48]


# ================================================================ nói chuyện với Trạm
class LoiTram(Exception):
    def __init__(self, chu, ma=0, d=None):
        super().__init__(chu)
        self.ma, self.d = ma, d or {}


def _goi(method: str, duong: str, body=None, raw: bytes = None, tram: str = "", xac_thuc=True, them_h=None, tra_tho=False, cho=60):
    c = cau_hinh()
    tram = (tram or c.get("tram") or "").rstrip("/")
    if not tram:
        raise LoiTram("Máy này chưa nối Trạm.")
    h = {"User-Agent": "tisa-bot", "Accept": "application/json"}
    if xac_thuc:
        h["Authorization"] = "Bearer %s.%s" % (c.get("may_id"), _giai_may(c.get("khoa") or ""))
    data = None
    if raw is not None:
        data, h["Content-Type"] = raw, "application/octet-stream"
    elif body is not None:
        data, h["Content-Type"] = json.dumps(body).encode(), "application/json"
    h.update(them_h or {})
    req = urllib.request.Request(tram + "/_tram/api" + duong, data=data, method=method, headers=h)
    try:
        if tra_tho:
            return urllib.request.urlopen(req, timeout=cho)      # bên gọi tự đóng (with r: ...)
        with urllib.request.urlopen(req, timeout=cho) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            d = json.loads(e.read().decode() or "{}")
        except ValueError:
            d = {}
        raise LoiTram(d.get("loi") or f"Trạm trả lỗi {e.code}", e.code, d)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise LoiTram(f"Không kết nối được Trạm: {getattr(e, 'reason', e)}")


def chuan_tram(u: str) -> str:
    u = (u or "").strip().rstrip("/")
    if u and not u.startswith("http"):
        u = "https://" + u
    if not re.fullmatch(r"https://[A-Za-z0-9.-]+(:\d+)?", u) and not re.fullmatch(r"http://(127\.0\.0\.1|localhost)(:\d+)?", u):
        raise ValueError("Địa chỉ Trạm không đúng (ví dụ https://tram-tisa.ten.workers.dev).")
    return u


def tach_dong_ghep(dong: str):
    """'https://tram...#ABCD2345' -> (tram, ma)."""
    dong = (dong or "").strip()
    if "#" not in dong:
        raise ValueError("Dòng ghép phải có dạng https://địa-chỉ-trạm#MÃ (chép nguyên dòng ở máy chính).")
    tram, ma = dong.rsplit("#", 1)
    ma = re.sub(r"[^A-Za-z0-9]", "", ma).upper()
    if len(ma) != 8:
        raise ValueError("Mã ghép phải đủ 8 ký tự.")
    return chuan_tram(tram), ma


# ================================================================ máy đầu tiên
def khoi_tao(tram: str, quan_tri: str, mat_khau: str, ten: str = "") -> dict:
    """Ghép máy ĐẦU TIÊN (máy đang chạy, thành máy chủ) với Trạm vừa dựng. Đặt mật khẩu bộ não."""
    if len(mat_khau or "") < 8:
        raise ValueError("Mật khẩu bộ não cần ít nhất 8 ký tự. Ghi nhớ kỹ: mất mật khẩu thì máy mới không giải mã được bộ não.")
    tram = chuan_tram(tram)
    chao = _goi("GET", "/chao", tram=tram, xac_thuc=False)
    if chao.get("da_co_may"):
        raise ValueError("Trạm này đã có máy ghép rồi. Máy này muốn vào thì dùng dòng ghép tạo ở máy đang ghép.")
    muoi = os.urandom(16)
    khoa = khoa_tu_mat_khau(mat_khau, muoi)
    ten = (ten or platform.node() or "Máy chính")[:60]
    d = _goi("POST", "/khoi-tao", {"ten": ten, "he": _he(), "ban": cm._ban(), "muoi": base64.b64encode(muoi).decode(), "mau_kiem": tao_mau_kiem(khoa)},
             tram=tram, xac_thuc=False, them_h={"x-tram-quan-tri": quan_tri})
    _luu_noi(tram, d["may_id"], d["khoa"], khoa, ten, {"muoi": base64.b64encode(muoi).decode(), "mau_kiem": tao_mau_kiem(khoa)})
    _ghi(VAI_TT, {"giu": list(VAI), "nhiem_ky": {k: (v or {}).get("nhiem_ky") for k, v in (d.get("vai") or {}).items()}, "luc": time.time()})
    nhat_ky("khoi_tao", tram=tram)
    _dam_bao_duong_ham()
    bat_luong()
    return {"ok": True, "may_id": d["may_id"], "tram": tram}


def _luu_noi(tram, may_id, khoa_may, khoa_nao: bytes, ten: str, them=None) -> None:
    c = cau_hinh()
    c.update({"bat": True, "tram": tram, "may_id": may_id, "khoa": _ma_hoa_may(khoa_may),
              "khoa_nao": _ma_hoa_may(base64.b64encode(khoa_nao).decode()), "ten": ten, "luc_noi": time.time()})
    c.update(them or {})
    _ghi(CAU_HINH, c)


# ================================================================ vai và cách ly
def vai_dang_giu() -> list:
    return list((_doc(VAI_TT, {}) or {}).get("giu") or [])


def _giu_theo_tram(vai_tram: dict, may_id: str) -> list:
    return [k for k in VAI if ((vai_tram or {}).get(k) or {}).get("may_id") == may_id]


def ap_vai_khi_khoi_dong() -> dict:
    """Gọi ngay sau tisa_chuyen_may.ap_dung_khi_khoi_dong(), MỖI lần máy chủ khởi động. Không bật Nhiều máy thì không làm gì.

    Thứ tự: (1) nhận lại việc tắt mà gói nhân bản đã làm (chế độ thử của Chuyển máy) để sổ vai của máy phụ biết cái gì cần bật lại khi lên chủ,
    (2) áp cấu hình máy chủ gửi về (nếu có bản chờ), (3) ép trạng thái kênh/lịch/bảng đúng theo vai đang giữ, (4) đặt biến môi trường cho vòng nền."""
    if not dang_bat():
        return {}
    vt = _doc(VAI_TT, {}) or {}
    da_tat = vt.setdefault("da_tat", {})
    ct = cm.doc_che_do_thu()
    if ct and ct.get("nhieu_may") and ct.get("giai_doan") in cm.CACH_LY_GD:
        # Gói nhân bản đã cách ly máy này. Từ giờ sổ vai của Nhiều máy giữ danh sách, chế độ thử của Chuyển máy kết thúc (không bật lại gì).
        da_tat["kenh"] = sorted(set(da_tat.get("kenh") or []) | {k for k in (ct.get("kenh_tam_tat") or []) if k != "remote_tunnel"})
        da_tat["mcp"] = sorted(set(da_tat.get("mcp") or []) | set(ct.get("mcp_tam_tat") or []))
        if ct.get("dq_tam_tat"):
            da_tat["dq"] = True
        if ct.get("lich_truoc") is False:
            da_tat["lich_truoc"] = False
        ct.update({"giai_doan": "xong", "cach_ly": False, "luc_chinh_thuc": time.time(), "boi": "nhieu_may"})
        cm._luu_che_do_thu(ct)
        os.environ.pop("TISA_CACH_LY", None)
        vt.setdefault("giu", [])
    try:
        _ap_cau_hinh_cho()
    except Exception as e:  # noqa: BLE001
        nhat_ky("loi_ap_cau_hinh", loi=str(e)[:200])
    # Hỏi Trạm NGAY lúc khởi động, trước khi bật kênh nào: máy chủ cũ bị tắt rồi bật lại sau khi máy khác đã tiếp quản không được làm chủ
    # thêm phút nào (đợi 2 nhịp như lúc đang chạy thì có khoảng 1 phút hai máy cùng trả lời khách). Trạm không trả lời thì giữ vai đã biết.
    try:
        d = _goi("POST", "/nhip", {"dia_chi": "", "ban": cm._ban(), "he": _he(), "ten": ten_may()}, cho=6)
        giu_tram = _giu_theo_tram(d.get("vai") or {}, cau_hinh().get("may_id"))
        if sorted(giu_tram) != sorted(vt.get("giu") or []):
            nhat_ky("doi_vai_khi_khoi_dong", tu=vt.get("giu"), thanh=giu_tram)
            vt["giu"] = giu_tram
            vt.pop("cho_doi", None)
        vt["nhiem_ky"] = {k: (v or {}).get("nhiem_ky") for k, v in (d.get("vai") or {}).items()}
    except Exception as e:  # noqa: BLE001
        nhat_ky("khoi_dong_khong_hoi_duoc_tram", loi=str(e)[:150])
    giu = set(vt.get("giu") or [])
    # Máy đang CÁCH LY của Chuyển máy (vừa nhận gói thường, chưa bấm chuyển chính thức): giữ vai nào cũng KHÔNG bật lại kênh, lịch, bảng.
    # Ví dụ bản sao chạy thử cạnh máy thật trên cùng một máy: làm chủ Trạm được nhưng không được trả lời khách trùng máy thật.
    cach_ly = cm.dang_cach_ly()
    st = cm._doc_cai_dat()
    doi = False
    # khach: kênh nhận tin + Zalo MCP
    if "khach" not in giu:
        tat = set(da_tat.get("kenh") or [])
        for k in cm.KENH_NHAN_TIN:
            v = st.get(k)
            if isinstance(v, dict) and v.get("enabled") is True:
                v["enabled"] = False; doi = True; tat.add(k)
        da_tat["kenh"] = sorted(tat)
        m = cm._doi_trang_thai_mcp(None, False, loc_zalo=True)
        if m:
            da_tat["mcp"] = sorted(set(da_tat.get("mcp") or []) | set(m))
    elif not cach_ly:
        for k in da_tat.get("kenh") or []:
            v = st.get(k)
            if isinstance(v, dict) and v.get("enabled") is False:
                v["enabled"] = True; doi = True
        if da_tat.get("mcp"):
            cm._doi_trang_thai_mcp(da_tat["mcp"], True)
        da_tat["kenh"], da_tat["mcp"] = [], []
    # lich: lịch tự động của máy
    if "lich" not in giu:
        if not st.get("schedules_off_here"):
            da_tat.setdefault("lich_truoc", False)
            st["schedules_off_here"] = True; doi = True
        b = st.get("backup")
        if isinstance(b, dict) and b.get("enabled") is True:
            b["enabled"] = False; doi = True; da_tat["backup"] = True
        os.environ["TISA_CACH_LY"] = "1"
        for k in cm.BIEN_TAM_DUNG:
            os.environ[k] = "1"
    elif not cach_ly:
        if "lich_truoc" in da_tat:
            st["schedules_off_here"] = bool(da_tat.pop("lich_truoc")); doi = True
        if da_tat.pop("backup", False):
            b = st.get("backup")
            if isinstance(b, dict):
                b["enabled"] = True; doi = True
        if not (cm.doc_che_do_thu() or {}).get("cach_ly"):
            os.environ.pop("TISA_CACH_LY", None)
    # bang: bảng Đội Quân dùng chung
    if "bang" not in giu:
        if cm._tam_tat_dq() or cm._dq_da_tat_san():
            da_tat["dq"] = True
    elif not cach_ly and da_tat.pop("dq", False):
        cm._bat_lai_dq()
    if doi:
        cm._ghi_cai_dat(st)
    vt["da_tat"] = da_tat
    vt["luc_ap"] = time.time()
    _ghi(VAI_TT, vt)
    _dam_bao_duong_ham()
    return vt


def _dam_bao_duong_ham() -> None:
    """Máy nào trong Nhiều máy cũng cần một địa chỉ riêng để cổng chuyển tới. Chưa có đường hầm thì bật kiểu nhanh (trycloudflare, không cần tài khoản).
    Đường hầm theo TOKEN của máy khác (mang theo trong gói nhân bản, đã bị tắt) thì bỏ token đó, chuyển sang kiểu nhanh của chính máy này."""
    st = cm._doc_cai_dat()
    rt = st.get("remote_tunnel") if isinstance(st.get("remote_tunnel"), dict) else {}
    if rt.get("enabled") is True:
        return
    if rt.get("mode") == "token" and rt.get("token") and (cau_hinh().get("nhan_ban") or cm.dang_cach_ly()) and not cau_hinh().get("token_cua_may_nay"):
        rt.pop("token", None)        # token này là của máy gốc (đi theo gói), máy này không được nối vào đường hầm đó
    rt.update({"enabled": True, "mode": "quick" if rt.get("mode") != "tailscale" else "tailscale"})
    st["remote_tunnel"] = rt
    cm._ghi_cai_dat(st)
    nhat_ky("bat_duong_ham", che_do=rt["mode"])


def dia_chi_may() -> str:
    try:
        import remote_tunnel
        s = remote_tunnel.MANAGER.status()
        url = (s.get("url") or "") if s.get("enabled") else ""
        if not url and time.time() - _tt.get("luc_chan_doan", 0) > 600:
            _tt["luc_chan_doan"] = time.time()
            nhat_ky("chua_co_dia_chi", trang_thai=s.get("state"), che_do=s.get("mode"), bat=s.get("enabled"), loi=s.get("error"),
                    ten_mien=s.get("hostnames"), log=list(getattr(remote_tunnel.MANAGER, "log", []))[-4:])
        return url
    except Exception as e:  # noqa: BLE001
        if time.time() - _tt.get("luc_chan_doan", 0) > 600:
            _tt["luc_chan_doan"] = time.time()
            nhat_ky("loi_doc_duong_ham", loi=f"{type(e).__name__}: {e}"[:300])
        return ""


def nhip() -> dict:
    """Báo Trạm máy này còn sống + địa chỉ; nhận bảng vai. Vai đổi thì hẹn khởi động lại để áp (xác nhận 2 nhịp liên tiếp)."""
    d = _goi("POST", "/nhip", {"dia_chi": dia_chi_may(), "ban": cm._ban(), "he": _he(), "ten": ten_may()}, cho=20)
    _tt.update({"nhip": d, "loi_nhip": "", "luc_nhip": time.time()})
    giu_moi = _giu_theo_tram(d.get("vai") or {}, cau_hinh().get("may_id"))
    vt = _doc(VAI_TT, {}) or {}
    if sorted(giu_moi) != sorted(vt.get("giu") or []):
        if vt.get("cho_doi") == sorted(giu_moi):
            if "cong" in giu_moi and "cong" not in (vt.get("giu") or []):
                _chuan_bi_len_chu()                       # kéo bộ não + cấu hình TRƯỚC khi sổ vai ghi "cong" (lúc đó máy còn là phụ nên nhận cấu hình)
            vt["giu"] = giu_moi
            vt.pop("cho_doi", None)
            vt["nhiem_ky"] = {k: (v or {}).get("nhiem_ky") for k, v in (d.get("vai") or {}).items()}
            _ghi(VAI_TT, vt)
            nhat_ky("doi_vai", giu=giu_moi)
            _khoi_dong_lai("Nhiều máy: đổi vai thành " + (", ".join(giu_moi) or "máy phụ"))
        else:
            vt["cho_doi"] = sorted(giu_moi)
            _ghi(VAI_TT, vt)
    elif vt.get("cho_doi") is not None:
        vt.pop("cho_doi", None)
        _ghi(VAI_TT, vt)
    return d


def _chuan_bi_len_chu() -> None:
    """Sắp lên máy chủ: kéo bộ não và cấu hình mới nhất về trước khi khởi động lại."""
    try:
        dong_bo_nao(chi_keo=True)
    except Exception as e:  # noqa: BLE001
        nhat_ky("loi_keo_truoc_khi_len_chu", loi=str(e)[:200])


def _khoi_dong_lai(ly_do: str) -> None:
    try:
        import tisa_khoi_dong_lai
        tisa_khoi_dong_lai.hen_khoi_dong_lai(ly_do)
    except Exception as e:  # noqa: BLE001
        nhat_ky("loi_khoi_dong_lai", loi=str(e)[:200])


def chia_ba(may_chu: str, may_lich: str, may_nang: str, ds_may: list = None) -> dict:
    """Bảng vai cho chế độ CHIA BA (ai có đúng 3 máy trở lên). Thuần tính toán, không gọi mạng, để dễ kiểm thử.

    Mặt tiền (cong + khach + bang) đi CÙNG một máy: tên miền, kênh nhận tin và bảng Đội Quân phải ở chung chỗ, vì máy không giữ vai bang bị tắt
    Đội Quân mà tên miền lại đổ người dùng vào máy giữ cong. Máy lịch giữ lich (lịch tự động, vòng nền, Kanban) để máy mặt tiền rảnh trả lời khách.
    Máy nặng giữ viec_nang (dựng video). Ba máy phải khác nhau và đều có trong sổ của Trạm (nếu sổ đã biết)."""
    ba = [may_chu, may_lich, may_nang]
    if not all(ba):
        raise ValueError("Chia ba cần chọn đủ ba máy: máy chủ, máy chạy lịch, máy làm việc nặng.")
    if len(set(ba)) < 3:
        raise ValueError("Chia ba cần ba máy KHÁC nhau. Chỉ có hai máy thì dùng \"Chia đôi\".")
    ten = {m.get("id"): m for m in (ds_may or [])}
    if ten:
        for x in ba:
            if x not in ten:
                raise ValueError("Có máy không nằm trong nhóm (đã gỡ hoặc chưa ghép). Làm mới trang rồi chọn lại.")
        for x, vai in ((may_chu, "máy chủ"), (may_lich, "máy chạy lịch")):
            if not ten[x].get("dang_bat"):
                raise ValueError(f"Máy {ten[x].get('ten')} đang tắt, không làm {vai} được. Bật máy đó lên trước.")
    return {"cong": may_chu, "khach": may_chu, "bang": may_chu, "lich": may_lich, "viec_nang": may_nang}


def dat_che_do(che_do: str, may_chu: str = "", may_phu: str = "", may_lich: str = "") -> dict:
    """Bốn chế độ trong Cài đặt. Trả bảng vai mới. Máy nào đổi vai sẽ tự khởi động lại ở nhịp kế tiếp (tối đa khoảng 1 phút)."""
    toi = cau_hinh().get("may_id")
    if che_do == "chu":
        gan = {k: toi for k in VAI}
    elif che_do == "phu":
        if not may_chu or may_chu == toi:
            raise ValueError("Chọn máy sẽ làm máy chủ (một máy khác đang bật).")
        gan = {k: may_chu for k in VAI}
    elif che_do == "chung":
        may_chu = may_chu or toi
        may_phu = may_phu or ""
        if not may_phu or may_phu == may_chu:
            raise ValueError("Chạy chung cần hai máy khác nhau: một máy chủ, một máy phụ làm việc nặng.")
        gan = {"cong": may_chu, "khach": may_chu, "lich": may_chu, "bang": may_chu, "viec_nang": may_phu}
    elif che_do == "chia_ba":
        gan = chia_ba(may_chu or toi, may_lich, may_phu, (_tt.get("nhip") or {}).get("may") or [])
    elif che_do == "tuy_chinh":
        raise ValueError("Dùng dat_vai cho tùy chỉnh.")
    else:
        raise ValueError("Chế độ không hợp lệ.")
    return dat_vai(gan)


def dat_vai(gan: dict) -> dict:
    gan = {k: v for k, v in (gan or {}).items() if k in VAI}
    if not gan.get("cong", "x"):
        raise ValueError("Phải có một máy chủ.")
    may = {m["id"]: m for m in ((_tt.get("nhip") or {}).get("may") or [])}
    toi = cau_hinh().get("may_id")
    for k, v in gan.items():
        if v and v != toi and v in may and not may[v].get("dang_bat") and k in ("cong", "khach"):
            raise ValueError(f"Máy {may[v].get('ten')} đang tắt, không giao vai {TEN_VAI[k]} được. Bật máy đó lên trước.")
    d = _goi("POST", "/dat-vai", {"gan": gan})
    nhat_ky("dat_vai", gan=gan)
    try:
        nhip()
    except LoiTram:
        pass
    return d


# ================================================================ đồng bộ bộ não
def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _ten_win(phan: str) -> str:
    """Tên tệp tạo trên Mac có thể có ký tự Windows cấm (: ? * " < > |) hoặc đuôi dấu chấm/cách."""
    t = _WIN_CAM.sub("_", phan).rstrip(" .")
    if t.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}:
        t = "_" + t
    return t or "_"


def _local_cua(remote: str, ten_map: dict) -> str:
    if remote in ten_map:
        return ten_map[remote]
    if os.name == "nt" or sys.platform == "win32":
        return "/".join(_ten_win(x) for x in remote.split("/"))
    return remote


def _duoc_dong_bo(rel: str, kich_thuoc: int) -> bool:
    phan = rel.split("/")
    if len(phan) < 2 or any(x in BO_THU_MUC_NAO for x in phan[:-1]):
        return False
    ten = phan[-1]
    if ten.startswith(".~") or ten in cm.BO_TEP or ten.endswith(cm.BO_DUOI) or ten.lower().endswith(cm.DUOI_SQLITE) or ten in (".DS_Store", "Thumbs.db", "desktop.ini"):
        return False
    if kich_thuoc > TEP_TOI_DA:
        return False
    return not cm.phan_loai_nang("bo-nao/" + rel, kich_thuoc)


def quet_nao() -> dict:
    """{remote_path: (Path, size, mtime_ns)} các tệp được đồng bộ, đường dẫn dạng NFC, gạch xuôi, bắt đầu bằng tên bộ não."""
    ra = {}
    if not BRAINS_DIR.is_dir():
        return ra
    for dp, dn, fn in os.walk(BRAINS_DIR):
        dn[:] = [d for d in dn if d not in BO_THU_MUC_NAO and not d.startswith("_truoc-")]
        for f in fn:
            p = Path(dp) / f
            try:
                stt = p.stat()
            except OSError:
                continue
            rel = _nfc(p.relative_to(BRAINS_DIR).as_posix())
            if _duoc_dong_bo(rel, stt.st_size):
                ra[rel] = (p, stt.st_size, stt.st_mtime_ns)
    return ra


# Đường dẫn riêng của máy trong tệp chữ (kế hoạch dựng video, cấu hình kỹ năng... hay ghi đường dẫn tuyệt đối). Gói nhân bản đổi chúng sang
# đường dẫn máy mới, nên cùng một tệp ở hai máy khác nhau từng chữ -> đồng bộ tưởng xung đột và ghi đường dẫn máy kia đè lên (thấy khi chạy thử 21/11).
# Gửi lên Trạm: thay đường dẫn của máy bằng KÝ HIỆU; nhận về: thay ký hiệu bằng đường dẫn của máy nhận. Dấu tệp tính trên bản đã chuẩn hóa.
KY_HIEU = (("bo_nao", "⟦TISA:BO_NAO⟧"), ("trang_thai", "⟦TISA:TRANG_THAI⟧"), ("goc", "⟦TISA:GOC⟧"), ("nha", "⟦TISA:NHA⟧"))
TOI_DA_CHUAN_HOA = 5_000_000


def _goc_may() -> list:
    duong = {"bo_nao": str(BRAINS_DIR), "trang_thai": str(STATE_DIR), "goc": str(ROOT), "nha": str(Path.home())}
    return sorted(((duong[k], kh) for k, kh in KY_HIEU if duong[k]), key=lambda x: -len(x[0]))


def _la_chu(rel: str) -> bool:
    return rel.lower().endswith(cm.DUOI_CHU)


def chuan_hoa(rel: str, du_lieu: bytes) -> bytes:
    if not _la_chu(rel) or len(du_lieu) > TOI_DA_CHUAN_HOA:
        return du_lieu
    try:
        t = du_lieu.decode("utf-8")
    except UnicodeDecodeError:
        return du_lieu
    moi = t
    for duong, kh in _goc_may():
        for dang in dict.fromkeys((json.dumps(duong)[1:-1], duong, duong.replace("\\", "/"))):
            if dang and dang in moi:
                moi = moi.replace(dang, kh)
    return moi.encode("utf-8") if moi != t else du_lieu


def tra_ve(rel: str, du_lieu: bytes) -> bytes:
    if not _la_chu(rel):
        return du_lieu
    try:
        t = du_lieu.decode("utf-8")
    except UnicodeDecodeError:
        return du_lieu
    if "⟦TISA:" not in t:
        return du_lieu
    js = rel.lower().endswith((".json", ".jsonl"))
    for duong, kh in _goc_may():
        t = t.replace(kh, json.dumps(duong)[1:-1] if js else duong)
    return t.encode("utf-8")


def _bam_tep(khoa: bytes, p: Path, size: int, mt: int, chi_muc: dict, rel: str) -> str:
    c = chi_muc.get(rel)
    if c and c[0] == size and c[1] == mt:
        return c[2]
    b = dau_tep(khoa, chuan_hoa(rel, p.read_bytes()))
    chi_muc[rel] = [size, mt, b]
    return b


def _ghi_tep_nao(dich: Path, du_lieu: bytes) -> None:
    dich.parent.mkdir(parents=True, exist_ok=True)
    tam = dich.with_name(dich.name + ".tisa-tai")
    tam.write_bytes(du_lieu)
    os.replace(tam, dich)


def _cat_thung_rac(p: Path, rel: str) -> None:
    dich = THUNG_RAC / time.strftime("%Y%m%d") / rel
    dich.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(p), str(dich))
    except OSError:
        pass


def _cat_xung_dot(p: Path, rel: str) -> str:
    phan = rel.split("/", 1)
    dich = BRAINS_DIR / phan[0] / "_xung-dot" / (phan[1] if len(phan) > 1 else phan[0])
    dich = dich.with_name(dich.name + f".{_ten_win(ten_may())}-{time.strftime('%Y%m%d-%H%M')}")
    dich.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dich)
    return str(dich)


def dong_bo_nao(chi_keo: bool = False, bao=None) -> dict:
    """Một vòng đồng bộ: KÉO các thay đổi từ Trạm, rồi ĐẨY thay đổi của máy này. Trả số liệu."""
    if not dang_bat():
        return {}
    with _khoa:
        _tt["dang_dong_bo"] = True
        try:
            return _dong_bo(chi_keo, bao)
        finally:
            _tt["dang_dong_bo"] = False


def _dong_bo(chi_keo: bool, bao) -> dict:
    khoa = _khoa_nao()
    db = _doc(DONG_BO, {}) or {}
    goc = db.setdefault("goc", {})            # remote -> dấu tệp lúc hai bên khớp lần cuối
    ten_map = db.setdefault("ten", {})        # remote -> local (khi tên phải đổi trên Windows)
    seq = int(db.get("seq") or 0)
    moi_ghep = bool(cau_hinh().get("moi_ghep"))
    chi_muc = _doc(CHI_MUC, {}) or {}
    so = {"keo": 0, "day": 0, "xoa": 0, "xung_dot": 0, "giong": 0, "loi": 0}
    dia = quet_nao()
    dia_theo_local = {}
    nguoc = {v: k for k, v in ten_map.items()}
    for rel, x in dia.items():
        dia_theo_local[nguoc.get(rel, rel)] = (rel, x)

    # ---- KÉO (phân loại tuần tự, TẢI song song: mỗi tệp một vòng đi về Cloudflare khoảng nửa giây, tải lần lượt thì hàng chục nghìn tệp mất hàng giờ)
    while True:
        d = _goi("GET", f"/tep?sau={seq}", cho=60)
        hang = d.get("tep") or []
        can_tai = []
        for r in hang:
            seq = max(seq, int(r["seq"]))
            remote = _nfc(r["duong_dan"])
            if remote.startswith(TIEN_TO_CAU_HINH):
                try:
                    _nhan_cau_hinh(khoa, r, goc)
                except Exception as e:  # noqa: BLE001
                    so["loi"] += 1
                    nhat_ky("loi_nhan_cau_hinh", tep=remote, loi=str(e)[:150])
                continue
            local_rel = _local_cua(remote, ten_map)
            if local_rel != remote:
                ten_map[remote] = local_rel
            p = BRAINS_DIR / local_rel
            co = dia_theo_local.get(remote)
            try:
                L = _bam_tep(khoa, co[1][0], co[1][1], co[1][2], chi_muc, co[0]) if co else ""
            except OSError:
                L, co = "", None
            B = goc.get(remote, "")
            if r.get("xoa"):
                if co and L == B:
                    _cat_thung_rac(p, local_rel); so["xoa"] += 1
                    dia_theo_local.pop(remote, None)
                goc.pop(remote, None)
                continue
            if L == r["bam"]:
                goc[remote] = r["bam"]; so["giong"] += 1
                continue
            if co and not moi_ghep and (B == "" or L != B):
                try:
                    duong = _cat_xung_dot(p, local_rel); so["xung_dot"] += 1
                    nhat_ky("xung_dot", tep=remote, cat_o=duong)
                except OSError as e:
                    so["loi"] += 1
                    nhat_ky("loi_cat_xung_dot", tep=remote, loi=str(e)[:150])
                    continue
            can_tai.append((r, remote, local_rel, p))
        for (r, remote, local_rel, p), kq in _song_song(lambda t: giai_ma(khoa, _tai_noi_dung(t[0]["bam"]), b"tep"), can_tai):
            try:
                if isinstance(kq, Exception):
                    raise kq
                if dau_tep(khoa, kq) != r["bam"]:
                    raise ValueError("dấu tệp không khớp")
                _ghi_tep_nao(p, tra_ve(remote, kq))
                stt = p.stat()
                chi_muc[local_rel] = [stt.st_size, stt.st_mtime_ns, r["bam"]]
                dia_theo_local[remote] = (local_rel, (p, stt.st_size, stt.st_mtime_ns))
                goc[remote] = r["bam"]; so["keo"] += 1
            except Exception as e:  # noqa: BLE001 - một tệp lỗi không dừng cả vòng
                so["loi"] += 1
                nhat_ky("loi_keo", tep=remote, loi=str(e)[:150])
            if bao and so["keo"] % 100 == 0:
                bao(None, f"Đã nhận {so['keo']} tệp")
        db.update({"seq": seq, "goc": goc, "ten": ten_map})
        _ghi(DONG_BO, db)
        _ghi(CHI_MUC, chi_muc)
        if len(hang) < 1000:
            break
    if moi_ghep:
        c = cau_hinh(); c.pop("moi_ghep", None); _ghi(CAU_HINH, c)
    if chi_keo:
        _ghi(CHI_MUC, chi_muc)
        return so

    # ---- ĐẨY (chọn tệp đổi khác tuần tự, GỬI song song, lưu tiến độ mỗi 200 tệp để khởi động lại giữa chừng không phải gửi lại)
    can_day = []
    for remote, (local_rel, (p, size, mt)) in list(dia_theo_local.items()):
        if len(can_day) >= LUOT_TAI_LEN:
            so["con_lai"] = True
            break
        try:
            L = _bam_tep(khoa, p, size, mt, chi_muc, local_rel)
        except OSError:
            continue
        B = goc.get(remote, "")
        if L != B:
            can_day.append((remote, p, L, B))

    def gui(t):
        remote, p, L, B = t
        noi_dung = chuan_hoa(remote, p.read_bytes())
        if dau_tep(khoa, noi_dung) != L:
            return "dang_ghi"                               # tệp đang được ghi dở, để vòng sau
        goi = ma_hoa(khoa, noi_dung, b"tep")
        for lan in range(3):                                # lỗi tạm thời của Trạm/D1/mạng: thử lại ngay, không đợi vòng sau
            try:
                _goi("PUT", "/tep?" + urllib.parse.urlencode({"duong_dan": remote, "bam": L, "goc": B}), raw=goi, cho=300)
                return "ok"
            except LoiTram as e:
                if lan == 2 or not (e.ma == 0 or e.ma >= 500):
                    raise
                time.sleep(1 + lan * 2)
    dung_som = False
    for n, ((remote, p, L, B), kq) in enumerate(_song_song(gui, can_day, dung=lambda: dung_som), 1):
        if kq == "ok":
            goc[remote] = L; so["day"] += 1
        elif isinstance(kq, LoiTram):
            if kq.ma == 409:
                so["xung_dot"] += 1                         # vòng kéo sau sẽ xử lý
            else:
                so["loi"] += 1
                nhat_ky("loi_day", tep=remote, loi=str(kq)[:150])
                if kq.ma in (0, 401, 501):
                    dung_som = True
        elif isinstance(kq, Exception):
            so["loi"] += 1
        if n % 200 == 0:
            db.update({"seq": seq, "goc": goc, "ten": ten_map})
            _ghi(DONG_BO, db)
            _ghi(CHI_MUC, chi_muc)
            if bao:
                bao(None, f"Đã gửi {so['day']} tệp")
    if dung_som:
        so["con_lai"] = False
    # tệp đã xóa ở máy này. Chặn xóa hàng loạt: thư mục bộ não tạm vắng (ổ ngoài rút ra, đổi đường dẫn) trông giống "xóa hết".
    mat = [k for k in goc if k not in dia_theo_local and not k.startswith(TIEN_TO_CAU_HINH)]
    if mat and (not dia_theo_local or (len(mat) > 50 and len(mat) > len(goc) * 0.2)):
        nhat_ky("chan_xoa_hang_loat", so=len(mat), con=len(dia_theo_local))
        so["chan_xoa"] = len(mat)
        mat = []
    for remote in mat:
        try:
            _goi("POST", "/tep/xoa", {"duong_dan": remote, "goc": goc[remote]})
            goc.pop(remote, None); so["xoa"] += 1
        except LoiTram as e:
            if e.ma != 409:
                so["loi"] += 1
    # cấu hình: chỉ máy chủ đẩy
    if "cong" in vai_dang_giu():
        try:
            so["cau_hinh"] = _day_cau_hinh(khoa, goc, chi_muc)
        except Exception as e:  # noqa: BLE001
            nhat_ky("loi_day_cau_hinh", loi=str(e)[:150])
    db.update({"seq": seq, "goc": goc, "ten": ten_map, "luc": time.time(), "so": so})
    _ghi(DONG_BO, db)
    _ghi(CHI_MUC, chi_muc)
    _tt["dong_bo"] = {**so, "luc": time.time()}
    return so


LUONG_SONG_SONG = 8


def _song_song(ham, viec, dung=None):
    """Chạy ham(x) cho từng x trong `viec` bằng 8 luồng; trả lần lượt (x, kết quả hoặc Exception) theo thứ tự xong.
    `dung()` True thì không gửi thêm việc mới (việc đang chạy vẫn chạy xong)."""
    from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
    viec = list(viec)
    if not viec:
        return
    with ThreadPoolExecutor(max_workers=LUONG_SONG_SONG) as ex:
        dang, i = {}, 0
        while i < len(viec) or dang:
            while i < len(viec) and len(dang) < LUONG_SONG_SONG * 2 and not (dung and dung()):
                dang[ex.submit(ham, viec[i])] = viec[i]
                i += 1
            if not dang:
                break
            xong, _ = wait(list(dang), return_when=FIRST_COMPLETED)
            for f in xong:
                x = dang.pop(f)
                try:
                    yield x, f.result()
                except Exception as e:  # noqa: BLE001
                    yield x, e
            if dung and dung():
                i = len(viec)


def _tai_noi_dung(bam: str) -> bytes:
    for lan in range(3):
        try:
            r = _goi("GET", "/noi-dung/" + bam, tra_tho=True, cho=300)
            with r:
                return r.read()
        except LoiTram as e:
            if lan == 2 or not (e.ma == 0 or e.ma >= 500):
                raise
            time.sleep(1 + lan * 2)


# ---- cấu hình
def _cau_hinh_cho_gui(ten: str) -> bytes:
    p = STATE_DIR / ten
    raw = p.read_bytes()
    if ten == "settings.json":
        d = json.loads(raw.decode("utf-8"))
        for k in KHOA_RIENG_MAY:
            d.pop(k, None)
        raw = json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")
    goc_may = {"goc": str(ROOT), "nha": str(Path.home()), "bo_nao": str(BRAINS_DIR), "trang_thai": str(STATE_DIR), "doi_quan_home": str(cm.DQ_HOME)}
    return json.dumps({"ten": ten, "may": goc_may, "noi_dung": base64.b64encode(raw).decode()}).encode()


def _day_cau_hinh(khoa: bytes, goc: dict, chi_muc: dict) -> int:
    n = 0
    for ten in TEP_CAU_HINH:
        p = STATE_DIR / ten
        if not p.is_file():
            continue
        du_lieu = _cau_hinh_cho_gui(ten)
        noi = json.loads(du_lieu)
        b = dau_tep(khoa, base64.b64decode(noi["noi_dung"]))
        remote = TIEN_TO_CAU_HINH + ten
        if goc.get(remote) == b:
            continue
        try:
            _goi("PUT", "/tep?" + urllib.parse.urlencode({"duong_dan": remote, "bam": b, "goc": goc.get(remote, "")}), raw=ma_hoa(khoa, du_lieu, b"tep"), cho=120)
        except LoiTram as e:
            if e.ma != 409:
                raise
            # bản trên Trạm khác bản ta biết: máy chủ là người ghi duy nhất, ghi đè bằng bản của mình
            _goi("PUT", "/tep?" + urllib.parse.urlencode({"duong_dan": remote, "bam": b, "goc": (e.d or {}).get("bam_tram", "")}), raw=ma_hoa(khoa, du_lieu, b"tep"), cho=120)
        goc[remote] = b
        n += 1
    return n


def _nhan_cau_hinh(khoa: bytes, r: dict, goc: dict) -> None:
    remote = r["duong_dan"]
    if r.get("xoa") or goc.get(remote) == r["bam"]:
        return
    if "cong" in vai_dang_giu():
        goc[remote] = r["bam"]                     # máy chủ là nguồn, không nhận lại
        return
    du_lieu = giai_ma(khoa, _tai_noi_dung(r["bam"]), b"tep")
    CHO_CAU_HINH.mkdir(parents=True, exist_ok=True)
    ten = remote[len(TIEN_TO_CAU_HINH):]
    if ten not in TEP_CAU_HINH:
        return
    (CHO_CAU_HINH / (ten + ".json")).write_bytes(du_lieu)
    goc[remote] = r["bam"]
    nhat_ky("nhan_cau_hinh", tep=ten)


def _ap_cau_hinh_cho() -> int:
    """Áp cấu hình máy chủ gửi về (đầu lần khởi động, trước khi máy chủ đọc cấu hình). Giữ nguyên khóa riêng của máy này."""
    if not CHO_CAU_HINH.is_dir():
        return 0
    n = 0
    for f in sorted(CHO_CAU_HINH.glob("*.json")):
        try:
            goi = json.loads(f.read_text(encoding="utf-8"))
            ten = goi.get("ten")
            if ten not in TEP_CAU_HINH:
                continue
            chu = base64.b64decode(goi["noi_dung"]).decode("utf-8")
            chu = cm._thay(chu, cm._cap_doi({"may": goi.get("may") or {}}), "json")
            moi = json.loads(chu)
            dich = STATE_DIR / ten
            if ten == "settings.json":
                cu = _doc(dich, {}) or {}
                for k in KHOA_RIENG_MAY:
                    if k in cu:
                        moi[k] = cu[k]
                    else:
                        moi.pop(k, None)
            if dich.exists():
                du_phong = NM / "cau-hinh-truoc" / time.strftime("%Y%m%d-%H%M%S")
                du_phong.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dich, du_phong / ten)
            _ghi(dich, moi)
            n += 1
        except Exception as e:  # noqa: BLE001
            nhat_ky("loi_ap_cau_hinh", tep=f.name, loi=str(e)[:150])
        finally:
            try:
                f.unlink()
            except OSError:
                pass
    if n:
        nhat_ky("ap_cau_hinh", so=n)
    return n


# ================================================================ nhân bản máy phụ
def _bao_viec(loai, phan_tram=None, chu=None, **kw):
    v = _viec.setdefault("v", {"loai": loai, "phan_tram": 0, "chu": "", "bat_dau": time.time()})
    v["loai"] = loai
    if phan_tram is not None:
        v["phan_tram"] = int(phan_tram)
    if chu is not None:
        v["chu"] = chu
    v.update(kw)


def _chay_nen(loai, ham, *a):
    if (_viec.get("v") or {}).get("dang_chay"):
        raise ValueError("Đang có việc khác chạy, đợi xong đã.")
    _viec["v"] = {"loai": loai, "phan_tram": 0, "chu": "Bắt đầu...", "dang_chay": True, "bat_dau": time.time()}

    def chay():
        try:
            kq = ham(*a)
            _bao_viec(loai, 100, "Xong", ket_qua=kq, xong=True, dang_chay=False)
        except Exception as e:  # noqa: BLE001
            _bao_viec(loai, chu="Lỗi", loi=str(e)[:400], xong=True, dang_chay=False)
            nhat_ky("loi_" + loai, loi=str(e)[:300])
    threading.Thread(target=chay, name="tisa-nm-" + loai, daemon=True).start()


BO_TIEN_TO_GOI = ("trang-thai/trinh-duyet/", "trang-thai/local-ear/", "trang-thai/nhieu-may/", "trang-thai/chuyen-may/")


def tao_ma_ghep(mat_khau: str) -> dict:
    """Máy đang ghép: kiểm mật khẩu bộ não, đóng gói nền tảng, tải lên Trạm, sinh mã ghép. Chạy ở luồng nền (giao diện xem tiến độ)."""
    c = cau_hinh()
    if not _kiem_mat_khau(mat_khau):
        raise ValueError("Mật khẩu bộ não không đúng.")
    # Gói đã mang cả bộ não, đồng bộ trước chỉ để Trạm mới nhất. Đồng bộ đang chạy (lần đầu có thể lâu) thì bỏ qua, không bắt anh chờ.
    if _khoa.acquire(blocking=False):
        try:
            _bao_viec("ma_ghep", 2, "Đang đồng bộ bộ não lên Trạm trước...")
            _tt["dang_dong_bo"] = True
            _dong_bo(False, None)
        except Exception as e:  # noqa: BLE001
            nhat_ky("loi_dong_bo_truoc_ghep", loi=str(e)[:200])
        finally:
            _tt["dang_dong_bo"] = False
            _khoa.release()
    cm.VIEC.mkdir(parents=True, exist_ok=True)
    tep = cm.VIEC / f"nhan-ban-{time.strftime('%Y%m%d-%H%M%S')}.tisapack"
    _bao_viec("ma_ghep", 5, "Đang đóng gói cấu hình, MCP, API, kênh, tin nhắn...")
    kq = cm.dong_goi(mat_khau, tep, bao=lambda pt, chu: _bao_viec("ma_ghep", 5 + pt * 0.45, chu), bo_tien_to=BO_TIEN_TO_GOI)
    try:
        ten = _tai_goi_len(tep, lambda pt, chu: _bao_viec("ma_ghep", 50 + pt * 0.48, chu))
    finally:
        try:
            tep.unlink()
        except OSError:
            pass
    d = _goi("POST", "/ma-ghep", {"goi": ten})
    dong = f"{c['tram']}#{d['ma'][:4]}-{d['ma'][4:]}"
    nhat_ky("tao_ma_ghep", goi=ten, dung_luong=kq.get("kich_thuoc"))
    return {"ma": d["ma"], "het": d["het"], "dong_ghep": dong, "dung_luong_goi": kq.get("kich_thuoc"), "so_tep": kq.get("so_tep")}


def _kiem_mat_khau(mat_khau: str) -> bool:
    c = cau_hinh()
    muoi, mau = c.get("muoi"), c.get("mau_kiem")
    if not muoi or not mau:
        return False
    return dung_mat_khau(khoa_tu_mat_khau(mat_khau, base64.b64decode(muoi)), mau)


def _tai_goi_len(tep: Path, bao) -> str:
    d = _goi("POST", "/goi/bat-dau", {})
    ten, up = d["ten"], d["upload_id"]
    tong = tep.stat().st_size
    parts, da = [], 0
    with open(tep, "rb") as f:
        so = 0
        while True:
            khuc = f.read(PHAN_GOI)
            if not khuc:
                break
            so += 1
            for lan in range(4):
                try:
                    r = _goi("PUT", "/goi/phan?" + urllib.parse.urlencode({"ten": ten, "so": so, "upload_id": up}), raw=khuc, cho=600)
                    break
                except LoiTram:
                    if lan == 3:
                        raise
                    time.sleep(3 * (lan + 1))
            parts.append(r["part"])
            da += len(khuc)
            bao(da * 100 / max(tong, 1), f"Đã tải lên {da / 1024 ** 3:.2f}/{tong / 1024 ** 3:.2f} GB")
    _goi("POST", "/goi/xong", {"ten": ten, "upload_id": up, "parts": parts}, cho=120)
    return ten


def ghep(dong: str, mat_khau: str, ten: str = "") -> dict:
    """Máy MỚI: dán dòng ghép + mật khẩu bộ não. Kiểm mật khẩu trước (mã không cháy nếu gõ sai), ghép, tải gói, nhận, hẹn áp dụng + khởi động lại."""
    if dang_bat():
        raise ValueError("Máy này đã ghép với Trạm rồi.")
    tram, ma = tach_dong_ghep(dong)
    _bao_viec("ghep", 2, "Đang kiểm mã ghép...")
    k = _goi("POST", "/ghep", {"ma": ma, "chi_kiem": True}, tram=tram, xac_thuc=False)
    muoi = base64.b64decode(k.get("muoi") or "")
    khoa = khoa_tu_mat_khau(mat_khau, muoi)
    if not muoi or not dung_mat_khau(khoa, k.get("mau_kiem") or ""):
        raise ValueError("Mật khẩu bộ não không đúng (mã ghép vẫn còn dùng được, gõ lại mật khẩu).")
    ten = (ten or platform.node() or "Máy phụ")[:60]
    d = _goi("POST", "/ghep", {"ma": ma, "ten": ten, "he": _he(), "ban": cm._ban()}, tram=tram, xac_thuc=False)
    _luu_noi(tram, d["may_id"], d["khoa"], khoa, ten, {"muoi": base64.b64encode(muoi).decode(), "mau_kiem": k["mau_kiem"], "moi_ghep": True, "nhan_ban": True})
    _ghi(VAI_TT, {"giu": [], "da_tat": {}, "luc": time.time()})
    nhat_ky("ghep", tram=tram)
    if not d.get("goi"):
        _dam_bao_duong_ham()
        return {"ok": True, "can_khoi_dong_lai": False, "ghi_chu": "Mã ghép không kèm gói nhân bản: máy này chỉ nhận bộ não qua đồng bộ."}
    try:
        return _ghep_nhan_goi(d, mat_khau)
    except Exception:
        # Hỏng giữa chừng (mất mạng, hết chỗ trống...): gỡ máy này khỏi Trạm và xóa sổ ghép để anh tạo dòng ghép mới rồi ghép lại được.
        try:
            _goi("POST", "/go-may", {"may_id": d["may_id"]})
        except Exception:  # noqa: BLE001
            pass
        for p in (CAU_HINH, VAI_TT):
            try:
                p.unlink()
            except OSError:
                pass
        nhat_ky("ghep_hong_da_go")
        raise


def _ghep_nhan_goi(d: dict, mat_khau: str) -> dict:
    tep = cm.VIEC / "nhan-ban.tisapack"
    cm.VIEC.mkdir(parents=True, exist_ok=True)
    _tai_goi_ve(d["goi"], tep, lambda pt, chu: _bao_viec("ghep", 5 + pt * 0.6, chu))
    _bao_viec("ghep", 66, "Đang giải mã và kiểm gói...")
    tom = cm.nhan(tep, mat_khau, bao=lambda pt, chu: _bao_viec("ghep", 66 + pt * 0.3, chu))
    try:
        tep.unlink()
    except OSError:
        pass
    try:
        _goi("POST", "/goi/xoa", {"ten": d["goi"]})
    except LoiTram:
        pass
    # Đánh dấu cho chế độ thử của Chuyển máy biết đây là máy phụ của Nhiều máy (ap_vai_khi_khoi_dong nhận lại danh sách đã tắt).
    _bao_viec("ghep", 97, "Đang hẹn áp dụng và khởi động lại...")
    c = cau_hinh(); c["cho_ap_goi"] = True; _ghi(CAU_HINH, c)
    cm.hen_ap_dung(khoi_dong_lai=True, dong_y_quay_lai=True)
    return {"ok": True, "can_khoi_dong_lai": True, "so_tep": tom.get("so_tep"), "may_goc": tom.get("ten_may_goc")}


def _tai_goi_ve(ten: str, tep: Path, bao) -> None:
    da = tep.stat().st_size if tep.exists() else 0
    for lan in range(6):
        try:
            r = _goi("GET", "/goi?" + urllib.parse.urlencode({"ten": ten}), tra_tho=True, them_h={"Range": f"bytes={da}-"} if da else None, cho=600)
            tong = int(r.headers.get("x-tong") or 0)
            with r, open(tep, "ab" if da else "wb") as f:
                while True:
                    khuc = r.read(4 * 1024 * 1024)
                    if not khuc:
                        break
                    f.write(khuc)
                    da += len(khuc)
                    bao(da * 100 / max(tong, 1), f"Đã tải về {da / 1024 ** 3:.2f}/{tong / 1024 ** 3:.2f} GB")
            if tong and da >= tong:
                return
        except LoiTram:
            if lan == 5:
                raise
            time.sleep(5 * (lan + 1))
    raise LoiTram("Tải gói về không trọn vẹn, thử lại.")


def sau_khi_ap_goi() -> None:
    """Gọi ở đầu khởi động: gói nhân bản vừa áp xong thì đánh dấu chế độ thử là của Nhiều máy."""
    c = cau_hinh()
    if not c.get("cho_ap_goi"):
        return
    ct = cm.doc_che_do_thu()
    if ct and ct.get("giai_doan") in cm.CACH_LY_GD:
        ct["nhieu_may"] = True
        cm._luu_che_do_thu(ct)
        c.pop("cho_ap_goi", None)
        _ghi(CAU_HINH, c)


def khi_khoi_dong() -> None:
    """Một lối vào duy nhất cho main.py, gọi ngay sau tisa_chuyen_may.ap_dung_khi_khoi_dong()."""
    try:
        sau_khi_ap_goi()
        ap_vai_khi_khoi_dong()
    except Exception as e:  # noqa: BLE001 - không bao giờ chặn máy chủ khởi động
        nhat_ky("loi_khoi_dong", loi=f"{type(e).__name__}: {e}"[:300])


# ================================================================ tắt Nhiều máy trên máy này
def tat(xac_nhan: bool = False) -> dict:
    """Rời Nhiều máy: máy này chạy một mình như cũ, bật lại mọi thứ đã tắt vì vai. Đang là máy chủ của máy khác thì cần xác nhận."""
    if not xac_nhan:
        raise ValueError("Cần xác nhận. Nếu máy khác vẫn đang làm chủ, hai máy sẽ cùng nhận khách.")
    vt = _doc(VAI_TT, {}) or {}
    vt["giu"] = list(VAI)
    _ghi(VAI_TT, vt)
    ap_vai_khi_khoi_dong()           # bật lại kênh, lịch, bảng đã ghi trong da_tat
    c = cau_hinh()
    c["bat"] = False
    _ghi(CAU_HINH, c)
    nhat_ky("tat_nhieu_may")
    _khoi_dong_lai("Nhiều máy: rời, chạy một mình")
    return {"ok": True}


# ================================================================ luồng nền
def bat_luong() -> None:
    """Hai luồng riêng: NHỊP (30 giây, báo Trạm còn sống + nhận vai) và ĐỒNG BỘ (2 phút, lâu cũng không làm trễ nhịp:
    lần đầu đẩy hàng chục nghìn tệp mà nhịp đứng chờ thì Trạm tưởng máy chủ đã tắt và cổng hiện trang bảo trì)."""
    if _luong["chay"]:
        return
    _luong["chay"] = True

    def vong_nhip():
        while True:
            if dang_bat():
                try:
                    nhip()
                except Exception as e:  # noqa: BLE001
                    _tt["loi_nhip"] = str(e)[:200]
            time.sleep(NHIP_GIAY)

    def vong_dong_bo():
        time.sleep(20)
        while True:
            cho = DONG_BO_GIAY
            if dang_bat() and not (_viec.get("v") or {}).get("dang_chay"):
                try:
                    so = dong_bo_nao()
                    if (so or {}).get("con_lai"):
                        cho = 5
                except Exception as e:  # noqa: BLE001
                    _tt["dong_bo"] = {"loi": str(e)[:200], "luc": time.time()}
            time.sleep(cho)
    threading.Thread(target=vong_nhip, name="tisa-nhieu-may-nhip", daemon=True).start()
    threading.Thread(target=vong_dong_bo, name="tisa-nhieu-may-dong-bo", daemon=True).start()


# ================================================================ giao diện
def tinh_trang() -> dict:
    c = cau_hinh()
    vt = _doc(VAI_TT, {}) or {}
    n = _tt.get("nhip") or {}
    db = _doc(DONG_BO, {}) or {}
    return {"ok": True, "bat": dang_bat(), "tram": c.get("tram") or "", "may_id": c.get("may_id") or "", "ten_may": ten_may(), "he": _he(),
            "ban": cm._ban(), "giu": vt.get("giu") or [], "cho_doi": vt.get("cho_doi"), "da_tat": vt.get("da_tat") or {},
            "may": n.get("may") or [], "vai": n.get("vai") or {}, "loi_nhip": _tt.get("loi_nhip"), "luc_nhip": _tt.get("luc_nhip"),
            "dia_chi": dia_chi_may(), "dong_bo": _tt.get("dong_bo") or db.get("so") or {}, "luc_dong_bo": db.get("luc"),
            "so_tep_dong_bo": len(db.get("goc") or {}), "dang_dong_bo": _tt.get("dang_dong_bo"),
            "viec": {k: v for k, v in (_viec.get("v") or {}).items()}, "ten_vai": TEN_VAI, "link_token": _link_token(),
            "lenh_cai": _lenh_cai(), "dong_bo_giay": DONG_BO_GIAY, "tep_toi_da_mb": TEP_TOI_DA // (1024 * 1024),
            "may_that": _ten_may_he(), "co_token_dat": (not dang_bat()) and _co_token_dat()}


# Chìa khóa Cloudflare do Đạt Đấu Nối lấy giúp (V3.74, chủ 28/11/2026: "bổ sung nút Đạt Đấu Nối hỗ trợ token ở bước Cloudflare").
# Đạt tạo token trên trang Cloudflare rồi cất thẳng vào Keychain (Windows: tệp mã hóa) bằng tisa_browser op=luu_keychain ten=tram-cloudflare:
# token không bao giờ hiện ra chat hay qua mô hình. Bấm Dựng thì lấy ra dùng MỘT lần rồi xóa, như token dán tay (không lưu ở đâu).
KC_TOKEN = "tisa-bot-tram-cloudflare"


def _co_token_dat() -> bool:
    try:
        import tisa_keychain as KC
        return bool(KC.co(KC_TOKEN))
    except Exception:  # noqa: BLE001
        return False


def _lay_token_dat() -> str:
    try:
        import tisa_keychain as KC
        return str(KC.doc(KC_TOKEN) or "").strip()
    except Exception:  # noqa: BLE001
        return ""


def _bo_token_dat() -> None:
    try:
        import tisa_keychain as KC
        KC.xoa(KC_TOKEN)
    except Exception:  # noqa: BLE001
        pass


def _ten_may_he() -> str:
    """Tên máy theo hệ điều hành (Mac: Tên máy tính ở Cài đặt), để trang nói rõ AI đang điều khiển máy nào."""
    if sys.platform == "darwin":
        try:
            t = subprocess.run(["scutil", "--get", "ComputerName"], capture_output=True, text=True, timeout=5).stdout.strip()
            if t:
                return t
        except Exception:  # noqa: BLE001
            pass
    return platform.node() or ""


def _lenh_cai() -> dict:
    """Lệnh cài TISA BOT cho máy thứ 2, hiện ở bước "Thêm máy". Kho lấy theo nơi bản này được tải về (git remote), để máy phụ cài đúng bản
    của máy chính. Bản mang bộ cài thử nghiệm (packaging/thu-nghiem) cài song song ở cổng 7790; bản thường (học viên, V3.72) dùng bộ cài
    một dòng như lúc cài lần đầu, cổng 7777."""
    thu = (ROOT / "packaging" / "thu-nghiem" / "cai-ban-thu.sh").is_file()
    thuong = (ROOT / "packaging" / "macos" / "get-tisa-bot.sh").is_file()
    if not thu and not thuong:
        return {}
    kho = "tieusangstudio-hash/tisa-bot-thu-nghiem" if thu else "tieusangstudio-hash/tisa-bot"
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10)
        m = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?/?$", (r.stdout or "").strip())
        if m:
            kho = m.group(1)
    except Exception:  # noqa: BLE001
        pass
    if thu:
        goc = "https://raw.githubusercontent.com/%s/main/packaging/thu-nghiem/" % kho
        return {"mac": "curl -fsSL %scai-ban-thu.sh | bash" % goc,
                "win": 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm %scai-ban-thu.ps1 | iex"' % goc,
                "cong": 7790}
    goc = "https://raw.githubusercontent.com/%s/main/packaging/" % kho
    return {"mac": "curl -fsSL %smacos/get-tisa-bot.sh | bash" % goc,
            "win": 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm %swindows/get-tisa-bot.ps1 | iex"' % goc,
            "tai_win": "https://github.com/%s/releases/download/desktop/TISA-BOT-Setup.exe" % kho,
            "cong": 7777}


def _link_token() -> str:
    try:
        import tisa_tram_cf
        return tisa_tram_cf.LINK_TAO_TOKEN
    except Exception:  # noqa: BLE001
        return ""


def gan(app) -> None:
    from fastapi.responses import HTMLResponse, JSONResponse

    trang = ROOT / "dashboard" / "tisa-nhieu-may.html"

    def _loi(e, ma=400):
        return JSONResponse({"ok": False, "loi": str(e)}, status_code=ma)

    async def _body(req):
        try:
            return await req.json()
        except Exception:  # noqa: BLE001
            return {}

    @app.get("/tisa-nhieu-may/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang Nhiều máy", status_code=500)

    @app.get("/tisa-nhieu-may/api/tinh-trang")
    async def _tinh_trang():
        return tinh_trang()

    @app.post("/tisa-nhieu-may/api/dung-tram")
    async def _dung_tram(req: Request):
        b = await _body(req)
        if dang_bat():
            return _loi("Máy này đã nối Trạm.")
        if len(b.get("mat_khau") or "") < 8:
            return _loi("Mật khẩu bộ não cần ít nhất 8 ký tự.")

        def lam(token, ten_mien, mat_khau):
            import tisa_tram_cf
            kq = tisa_tram_cf.dung(token, ten_mien, bao=lambda pt, chu: _bao_viec("dung_tram", pt * 0.7, chu))
            if tu_dat:
                _bo_token_dat()            # dùng xong là bỏ, như token dán tay
            _bao_viec("dung_tram", 75, "Đang chờ Trạm sẵn sàng...")
            for _ in range(20):
                try:
                    _goi("GET", "/chao", tram=kq["tram"], xac_thuc=False, cho=15)
                    break
                except LoiTram:
                    time.sleep(3)
            _bao_viec("dung_tram", 85, "Đang ghép máy này làm máy chủ...")
            r = khoi_tao(kq["tram"], kq["quan_tri"], mat_khau)
            _bao_viec("dung_tram", 90, "Đang gửi bộ não lên Trạm lần đầu (có thể lâu)...")
            try:
                dong_bo_nao(bao=lambda pt, chu: _bao_viec("dung_tram", 92, chu))
            except Exception as e:  # noqa: BLE001
                nhat_ky("loi_dong_bo_dau", loi=str(e)[:200])
            return {**r, "ten_mien": kq.get("ten_mien")}
        token = str(b.get("token") or "").strip()
        tu_dat = False
        if not token:
            token = _lay_token_dat()
            tu_dat = bool(token)
            if not token:
                return _loi("Chưa có chìa khóa Cloudflare. Bấm \"Nhờ Đạt Đấu Nối lấy giúp\" ở bước 1, hoặc tự tạo token rồi dán vào ô.")
        try:
            import tisa_tram_cf
            tisa_tram_cf.CF(token)             # token sai dạng thì báo ngay
            _chay_nen("dung_tram", lam, token, b.get("ten_mien") or "", b.get("mat_khau"))
        except Exception as e:  # noqa: BLE001 - ValueError, LoiCF
            return _loi(e)
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/bo-token-dat")
    async def _bo_token():
        """Bỏ chìa khóa Đạt đã lấy (anh muốn tạo lại, hoặc dùng tài khoản Cloudflare khác)."""
        _bo_token_dat()
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/noi-tram")
    async def _noi_tram(req: Request):
        """Đã có Trạm dựng sẵn (dựng tay bằng wrangler): nhập địa chỉ + khóa dựng."""
        b = await _body(req)
        try:
            return khoi_tao(b.get("tram") or "", b.get("quan_tri") or "", b.get("mat_khau") or "")
        except (ValueError, LoiTram) as e:
            return _loi(e)

    @app.post("/tisa-nhieu-may/api/ma-ghep")
    async def _ma_ghep(req: Request):
        b = await _body(req)
        try:
            if not dang_bat():
                raise ValueError("Máy này chưa nối Trạm.")
            if not _kiem_mat_khau(b.get("mat_khau") or ""):
                raise ValueError("Mật khẩu bộ não không đúng.")
            _chay_nen("ma_ghep", tao_ma_ghep, b.get("mat_khau"))
        except (ValueError, LoiTram) as e:
            return _loi(e)
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/ghep")
    async def _ghep(req: Request):
        b = await _body(req)
        t = cm.truy_cap(req)
        if t["qua_ten_mien"] and not b.get("xac_nhan_may"):
            return _loi(f"Anh đang mở trang này qua {t['host']}. Ghép máy phụ sẽ THAY dữ liệu của máy đang trả lời (tên {t['ten_may']}). "
                        "Hãy mở TISA BOT ngay trên máy mới (http://localhost:cổng) rồi làm lại, hoặc tick ô xác nhận nếu chắc chắn.")
        try:
            if dang_bat():
                raise ValueError("Máy này đã ghép với Trạm rồi.")
            tach_dong_ghep(b.get("dong") or "")             # báo dòng ghép sai NGAY, không đợi việc nền
            if not (b.get("mat_khau") or ""):
                raise ValueError("Nhập mật khẩu bộ não.")
            _chay_nen("ghep", ghep, b.get("dong") or "", b.get("mat_khau") or "", b.get("ten") or "")
        except ValueError as e:
            return _loi(e)
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/che-do")
    async def _che_do(req: Request):
        b = await _body(req)
        try:
            if b.get("gan"):
                return dat_vai(b["gan"])
            return dat_che_do(b.get("che_do") or "", b.get("may_chu") or "", b.get("may_phu") or "", b.get("may_lich") or "")
        except (ValueError, LoiTram) as e:
            return _loi(e)

    @app.post("/tisa-nhieu-may/api/dong-bo")
    async def _dong_bo_ngay():
        try:
            _chay_nen("dong_bo", dong_bo_nao, False, lambda pt, chu: _bao_viec("dong_bo", None, chu))
        except ValueError as e:
            return _loi(e)
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/go-may")
    async def _go_may(req: Request):
        b = await _body(req)
        try:
            return _goi("POST", "/go-may", {"may_id": b.get("may_id") or ""})
        except LoiTram as e:
            return _loi(e)

    @app.post("/tisa-nhieu-may/api/doi-ten")
    async def _doi_ten(req: Request):
        b = await _body(req)
        ten = re.sub(r"\s+", " ", str(b.get("ten") or "")).strip()[:60]
        if not ten:
            return _loi("Tên máy trống.")
        c = cau_hinh(); c["ten"] = ten; _ghi(CAU_HINH, c)
        return {"ok": True}

    @app.post("/tisa-nhieu-may/api/tat")
    async def _tat(req: Request):
        b = await _body(req)
        try:
            return tat(bool(b.get("xac_nhan")))
        except ValueError as e:
            return _loi(e)

    if dang_bat():
        bat_luong()
