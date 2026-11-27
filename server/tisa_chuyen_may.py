"""tisa_chuyen_may.py - Chuyển TISA BOT sang máy khác hoặc VPS bằng MỘT file (V2.76, chủ chốt 10/11/2026).

Chủ dặn: "chuyển qua phải đi kèm toàn bộ hệ thống MCP với API, bộ não và các thiết lập để không mất thời gian setup lại".

Gói gồm mọi thứ TISA BOT tự sinh ra trên máy cũ, tức mọi tệp KHÔNG thuộc mã nguồn (git không theo dõi):
- mọi bộ não (BRAINS_DIR), kể cả skill, cộng sự, quy trình, trí nhớ, tệp đính kèm;
- settings.json kèm `.secret_key` (khoá API, token kênh, MCP đều mã hoá bằng khoá này, thiếu nó là mất hết);
- mcp_servers.json, .oauth_mcp.json, .hub_token, kết nối kênh, chatbot, lịch sử chat, việc định kỳ, webhook, mọi CSDL;
- plugin, gói Store, ảnh đại diện, connector-home (phiên đăng nhập Zalo...), tệp .env của TISA BOT;
- dữ liệu Đội Quân AI (DOI_QUAN_HOME) và tệp .env của nó (DOI_QUAN_ENV).
CHỈ MANG DỮ LIỆU. Chương trình TISA BOT (mã nguồn, giao diện, tài liệu, công cụ) KHÔNG BAO GIỜ đi trong gói: máy mới giữ nguyên bản
đang cài của nó. Bản ghi tên bản TISA BOT của máy cũ nằm trong kê khai để máy mới đối chiếu: máy mới thấp bản hơn máy cũ thì
dừng, yêu cầu cập nhật trước, vì dữ liệu của bản mới không nên đặt vào chương trình bản cũ.
(V2.78: bản cũ hơn từng gói cả mã nguồn của máy cũ khi máy không có git, áp dụng xong là chương trình máy mới bị thay bằng bản cũ.)

Sau khi áp dụng, máy mới vào CHẾ ĐỘ THỬ: chạy local, các kênh nhận tin (Telegram, Zalo, ...) tạm tắt để không trả lời trùng với
máy cũ đang chạy. Chủ thử xong mới trỏ tên miền Cloudflare về máy mới, rồi bấm chuyển chính thức để bật lại các kênh.

V3.11 (chủ báo 18/11/2026, sau khi chuyển thật lần đầu): (1) máy mới KHÔNG được tự nối lại đường hầm Cloudflare của máy cũ (settings mang theo cả token đường hầm,
nên hai máy cùng trả lời một tên miền, chủ thấy lúc dữ liệu máy cũ lúc dữ liệu máy mới, tưởng là "đồng bộ" và "mất hết"); (2) gói mang thêm các kết nối MCP nằm ngoài
thư mục TISA BOT (Claude Code ~/.claude.json, Codex ~/.codex/config.toml), máy mới chỉ THÊM cái chưa có, không ghi đè.

Không mang: mã nguồn (máy mới giữ bản của nó), .venv, node_modules, bộ nhớ đệm, nhật ký, pid, phiên đăng nhập web cũ, đường dẫn
chương trình riêng của máy cũ, và đăng nhập gói Claude / ChatGPT của máy cũ (đăng nhập lại 1 lần trên máy mới).

File chứa mọi khoá nên luôn KHOÁ bằng mật khẩu chủ đặt: scrypt -> AES-256-GCM từng khúc 4MB, khúc cuối có cờ riêng nên
cắt bớt đuôi file là bị phát hiện. Sai mật khẩu hay file hỏng thì dừng trước khi đụng vào máy mới.

Áp dụng trên máy mới đi qua lần khởi động lại: dữ liệu đã giải nén nằm chờ trong thư mục `chuyen-may/cho-ap-dung`, máy chủ
khởi động lại, và NGAY ĐẦU lần chạy mới (trước khi mở bất kỳ CSDL nào, xem `ap_dung_khi_khoi_dong`) mới đổi dữ liệu:
bản đang có của máy mới chuyển sang `_truoc-chuyen-may-<giờ>` (không xoá), rồi đặt dữ liệu cũ vào chỗ và sửa đường dẫn
máy cũ thành đường dẫn máy mới trong tệp cấu hình và CSDL.

Dùng được từ dòng lệnh cho VPS (file lớn, chép bằng scp):
    python server/tisa_chuyen_may.py dong-goi <file-ra> [--kho=hinh_anh,video,am_thanh,lam_tiep,lon_khac | --tat-ca-kho]   (hỏi mật khẩu; mặc định chỉ NỀN TẢNG)
    python server/tisa_chuyen_may.py nhan <file.tisapack>         (hỏi mật khẩu, rồi khởi động lại TISA BOT)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import re
import shutil
import sqlite3
import struct
import subprocess
import sys
import threading
import time
import uuid
import zipfile
from pathlib import Path

try:    # ở cấp module: FastAPI đọc chú thích kiểu dạng chuỗi (from __future__ import annotations) theo tên toàn cục
    from fastapi import Request
except Exception:  # noqa: BLE001 - dòng lệnh không cần FastAPI
    Request = None

SERVER = Path(__file__).resolve().parent
ROOT = SERVER.parent
STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or str(SERVER))
BRAINS_DIR = Path(os.getenv("BRAINS_DIR") or str(ROOT / "brains"))
DQ_HOME = Path(os.getenv("DOI_QUAN_HOME") or (Path.home() / ".doi-quan-ai"))
DQ_ENV = Path(os.getenv("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
VIEC = STATE_DIR / "chuyen-may"            # file gói, phần tải lên, thư mục chờ áp dụng
CHO = VIEC / "cho-ap-dung"
DANH_DAU = VIEC / "cho-ap-dung.json"

MAGIC = b"TISAPACK"
PHIEN_BAN = 1
KHUC = 4 * 1024 * 1024
GIU_TRONG = 2 * 1024 ** 3                  # chừa lại 2GB đĩa trống

# Không mang theo: thư mục (tên ở bất kỳ cấp nào) và tệp riêng của máy cũ.
BO_THU_MUC = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "cache", "tmp", ".staging",
              "logs", "chatbot-logs", "learn-log", "loop-log", "chuyen-may", ".Trash", ".cache"}
BO_TEP = {"bin_paths.json", "claude-update.json", "agy-update.json", "update_state.json", "update.log",
          "mcp-stdio-pids.json", "loop_beat.json", "loop_restarts.json", "engine_down_notified.json",
          "remote-tunnel.pid", ".sessions.json", ".sessions_meta.json", "client_errors.json", ".DS_Store",
          "settings.json.bak", "packs.json.bak"}
BO_DUOI = (".pyc", ".pid", ".lock", ".log", "-shm", "-wal", ".tmp", ".swp")
DUOI_SQLITE = (".db", ".sqlite", ".sqlite3")
DUOI_CHU = (".json", ".jsonl", ".md", ".yaml", ".yml", ".txt", ".env", ".toml", ".ini", ".cfg", ".conf", ".csv")

# Chương trình KHÔNG đi trong gói. Đúng cả khi máy không có git (bản cài từ bộ cài, git theo dõi rỗng).
GOC_CHUONG_TRINH = {"server", "dashboard", "suite", "system", "docs", "packaging", "tools", "pilot", "cli", "bin", "third_party", "docker",
                    "changelog.d", ".github", ".claude", "TISA BOT.app", ".venv", "venv", "node_modules"}
GOC_TEP_DU_LIEU = {".env"}
DUOI_MA_NGUON = (".py", ".pyc", ".pyo", ".pyd", ".so", ".dylib", ".dll", ".exe", ".html", ".js", ".mjs", ".cjs", ".css", ".map",
                 ".sh", ".bat", ".ps1", ".vbs", ".command", ".service")
THU_MUC_DU_LIEU_CO_MA = {"packs", "packs-state", "packs-staging", "plugin-data", "connector-home", "tisa_web"}
THU_MUC_CHUONG_TRINH_TRONG_TRANG_THAI = {"channels", "routes", "lexicon", "data_phien_am", "offline_ear", "__pycache__"}
KENH_NHAN_TIN = ("telegram", "zalo_bot", "slack", "whatsapp", "discord", "lark", "wechat", "line", "viber", "threads", "instagram")
CHE_DO_THU = VIEC / "che-do-thu.json"


def la_ma_nguon_goc(rel: str) -> bool:
    """Tệp trong thư mục cài TISA BOT có phải CHƯƠNG TRÌNH (không mang) không. Chỉ .env và thư mục lạ của riêng máy là dữ liệu."""
    p = [x for x in rel.replace("\\", "/").split("/") if x]
    if not p:
        return True
    if len(p) == 1:
        return p[0] not in GOC_TEP_DU_LIEU
    return p[0] in GOC_CHUONG_TRINH or p[0].startswith(("_truoc-chuyen-may", "_ban-goi-da-ap-dung"))


def la_ma_nguon_trang_thai(rel: str) -> bool:
    """Tệp trong thư mục trạng thái (trùng thư mục server trên bản cài) có phải mã nguồn không. Plugin, gói Store, trang web tự tạo thì giữ."""
    p = [x for x in rel.replace("\\", "/").split("/") if x]
    if not p:
        return True
    if "__pycache__" in p:
        return True
    if p[0] in THU_MUC_DU_LIEU_CO_MA:
        return False
    if p[0] in THU_MUC_CHUONG_TRINH_TRONG_TRANG_THAI:
        return True
    n = p[-1].lower()
    return n.endswith(DUOI_MA_NGUON) or n == "requirements.txt"


def _ver(s: str):
    try:
        t = [int(x) for x in re.split(r"[.\-]", (s or "").strip().lstrip("vV"))[:3] if x.isdigit()]
        while len(t) < 3:
            t.append(0)
        return tuple(t[:3])
    except Exception:  # noqa: BLE001
        return None


def _ten_ban() -> str:
    """Tên bản hiển thị (ví dụ 2.78) từ TISA_BAN.json, rỗng nếu không có."""
    try:
        return str(json.loads((ROOT / "TISA_BAN.json").read_text(encoding="utf-8")).get("hien_tai") or "")
    except (OSError, ValueError):
        return ""


_khoa = threading.Lock()
_viec = {}       # id -> trạng thái việc đóng gói / nhận


# ---------------------------------------------------------------- mã hoá
def _khoa_tu_mat_khau(mat_khau: str, muoi: bytes) -> bytes:
    import hashlib
    return hashlib.scrypt(mat_khau.encode("utf-8"), salt=muoi, n=2 ** 15, r=8, p=1, maxmem=96 * 1024 * 1024, dklen=32)


class _GhiMaHoa(io.RawIOBase):
    """Luồng ghi: gom 4MB thì mã hoá một khúc. zipfile ghi vào đây như một tệp không tua lại được."""

    def __init__(self, ra, mat_khau: str):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        self.ra, self.dem, self.so, self.dong = ra, bytearray(), 0, False
        muoi, self.goc = os.urandom(16), os.urandom(8)
        self.dau = MAGIC + bytes([PHIEN_BAN]) + muoi + self.goc + struct.pack(">I", KHUC)
        ra.write(self.dau)
        self.aes = AESGCM(_khoa_tu_mat_khau(mat_khau, muoi))
        self.da_viet = 0

    def writable(self):
        return True

    def seekable(self):
        return False

    def tell(self):
        return self.da_viet

    def seek(self, *a):
        raise OSError("không tua được")

    def _khuc(self, du_lieu: bytes, cuoi: bool):
        nonce = self.goc + struct.pack(">I", self.so)
        aad = self.dau + struct.pack(">IB", self.so, 1 if cuoi else 0)
        ct = self.aes.encrypt(nonce, bytes(du_lieu), aad)
        self.ra.write(struct.pack(">I", len(ct)) + ct)
        self.so += 1

    def write(self, b):
        self.dem += b
        self.da_viet += len(b)
        while len(self.dem) > KHUC:
            self._khuc(self.dem[:KHUC], False)
            del self.dem[:KHUC]
        return len(b)

    def close(self):
        if not self.dong:
            self._khuc(self.dem, True)
            self.dem = bytearray()
            self.dong = True
        super().close()


def giai_ma(nguon: Path, dich: Path, mat_khau: str) -> None:
    """Giải mã cả file ra `dich`. Sai mật khẩu / file hỏng / bị cắt đuôi thì báo lỗi rõ."""
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    with open(nguon, "rb") as f, open(dich, "wb") as ra:
        dau = f.read(len(MAGIC) + 1 + 16 + 8 + 4)
        if len(dau) < 37 or not dau.startswith(MAGIC):
            raise ValueError("Đây không phải file chuyển máy của TISA BOT.")
        if dau[len(MAGIC)] != PHIEN_BAN:
            raise ValueError("File được tạo bởi bản TISA BOT khác, hãy cập nhật TISA BOT rồi thử lại.")
        muoi, goc = dau[9:25], dau[25:33]
        aes = AESGCM(_khoa_tu_mat_khau(mat_khau, muoi))
        so, het = 0, False
        while True:
            d = f.read(4)
            if not d:
                break
            n = struct.unpack(">I", d)[0]
            ct = f.read(n)
            if len(ct) != n:
                raise ValueError("File bị thiếu đuôi (tải chưa hết). Hãy chép lại file từ máy cũ.")
            nonce = goc + struct.pack(">I", so)
            pt = None
            for co in (0, 1):
                try:
                    pt = aes.decrypt(nonce, ct, dau + struct.pack(">IB", so, co))
                    het = bool(co)
                    break
                except InvalidTag:
                    continue
            if pt is None:
                raise ValueError("Sai mật khẩu, hoặc file đã bị hỏng." if so == 0 else "File bị hỏng giữa chừng.")
            ra.write(pt)
            so += 1
            if het:
                break
        if not het:
            raise ValueError("File bị thiếu đuôi (tải chưa hết). Hãy chép lại file từ máy cũ.")


# ---------------------------------------------------------------- chọn tệp
def _git_theo_doi() -> set:
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True, timeout=60)
        if r.returncode == 0:
            return {x.decode("utf-8", "replace") for x in r.stdout.split(b"\0") if x}
    except Exception:
        pass
    return set()


def _bo(rel_parts, ten: str) -> bool:
    if any(p in BO_THU_MUC for p in rel_parts[:-1]):
        return True
    return ten in BO_TEP or ten.endswith(BO_DUOI)


# Bộ não là dữ liệu của chủ: chỉ bỏ rác máy, giữ mọi thư mục kể cả .git (sao lưu GitHub của bộ não) và thư mục tên "logs".
BO_THU_MUC_NAO = {"node_modules", "__pycache__", ".Trash", ".pytest_cache"}

# Thư mục đầu "_" ở gốc cài là bản dự phòng/rác (_truoc-*, _to_delete, _work...) nên bỏ, TRỪ _mcp:
# mã các MCP tự cài (SnapGen, HeyGen, tisa-web...) nằm ở đó; thiếu nó máy nhận báo "can't open file .../_mcp/<tên>/server.py".
GIU_THU_MUC_GACH = {"_mcp"}


def _duyet(goc: Path, tien_to: str, theo_doi, bo_cap_dau_gach=False, la_nao=False):
    """(đường dẫn thật, tên trong gói) của mọi tệp nên mang theo dưới `goc`."""
    if not goc.is_dir():
        return
    bo_tm = BO_THU_MUC_NAO if la_nao else BO_THU_MUC
    for dp, dn, fn in os.walk(goc):
        rel_dp = Path(dp).relative_to(goc)
        if bo_cap_dau_gach and rel_dp == Path("."):
            # Bỏ thư mục dự phòng/rác (_truoc-*, _sao-luu...) nhưng GIỮ _mcp: mã các MCP tự cài (SnapGen, tisa-web...) nằm ở đó,
            # thiếu nó máy nhận báo "can't open file .../_mcp/<tên>/server.py" (thấy khi nhân bản thử 21/11/2026).
            dn[:] = [d for d in dn if not d.startswith("_") or d in GIU_THU_MUC_GACH]
        dn[:] = [d for d in dn if d not in bo_tm and not os.path.islink(os.path.join(dp, d))]
        for f in fn:
            p = Path(dp) / f
            rel = (rel_dp / f).as_posix() if str(rel_dp) != "." else f
            if p.is_symlink():
                continue
            if la_nao:
                if f == ".DS_Store" or f.endswith(("-wal", "-shm")):
                    continue
            elif _bo(Path(rel).parts, f):
                continue
            if theo_doi is not None and rel in theo_doi:
                continue
            yield p, f"{tien_to}/{rel}"


def _trong(p: str, goc: str) -> bool:
    return p == goc or p.startswith(goc.rstrip(os.sep) + os.sep)


def danh_sach() -> list:
    """Mọi tệp sẽ vào gói: [(đường dẫn thật, tên trong gói)].

    goc/...         tệp riêng của máy nằm trong thư mục cài TISA BOT (.env, plugin, công cụ tự thêm...)
    trang-thai/...  thư mục trạng thái (settings, khoá, CSDL, kết nối MCP, chatbot) - máy mới đặt vào TISA_STATE_DIR của nó
    bo-nao/...      mọi bộ não - máy mới đặt vào BRAINS_DIR của nó
    doi-quan-home/, doi-quan-env/  dữ liệu và cấu hình Đội Quân AI
    """
    theo_doi = _git_theo_doi()
    nao = str(BRAINS_DIR.resolve()) if BRAINS_DIR.exists() else ""
    tt = str(STATE_DIR.resolve())
    out, da = [], set()
    for p, ten in _duyet(ROOT, "goc", theo_doi, bo_cap_dau_gach=True):
        rp = str(p.resolve())
        if nao and _trong(rp, nao):
            continue
        if _trong(rp, tt):
            rel_tt = Path(rp).relative_to(tt).as_posix()
            if la_ma_nguon_trang_thai(rel_tt):
                continue
            ten = "trang-thai/" + rel_tt
        elif la_ma_nguon_goc(ten[len("goc/"):]):
            continue
        out.append((p, ten)); da.add(rp)
    if not _trong(tt, str(ROOT.resolve())):
        for p, ten in _duyet(STATE_DIR, "trang-thai", None):
            if str(p.resolve()) not in da and not la_ma_nguon_trang_thai(ten[len("trang-thai/"):]):
                out.append((p, ten))
    for p, ten in _duyet(BRAINS_DIR, "bo-nao", None, la_nao=True):
        out.append((p, ten))
    for p, ten in _duyet(DQ_HOME, "doi-quan-home", None):
        out.append((p, ten))
    if DQ_ENV.is_file():
        out.append((DQ_ENV, "doi-quan-env/.env"))
    # Sổ Nhiều máy (danh tính máy với Trạm, khóa máy) thuộc riêng máy này: mang sang máy khác là hai máy cùng một danh tính.
    return [(p, ten) for p, ten in out if not ten.startswith("trang-thai/nhieu-may/")]


# ---------------------------------------------------------------- nền tảng (bắt buộc) và kho nặng (tùy chọn) (V3.12)
# Chủ 18/11/2026: gói 37 GB vì bộ não chứa video, âm thanh, tệp làm dở. Nay chia hai phần:
#   NỀN TẢNG (luôn mang, không tắt được): bộ não (chữ, wiki, kỹ năng, kết quả nhẹ), MCP, API, mọi tin nhắn, mọi thiết lập, kênh, Đội Quân AI.
#   KHO NẶNG (tùy chọn, mặc định KHÔNG mang): hình ảnh, video, âm thanh, tệp làm dở để AI làm tiếp, tệp lớn khác. Chỉ áp cho bộ não và Đội Quân AI.
KHO_NANG = ("hinh_anh", "video", "am_thanh", "lam_tiep", "lon_khac")
NHAN_KHO = {
    "hinh_anh": ("Hình ảnh", "PNG, JPG, WEBP, HEIC, PSD... từ 1 MB trở lên (ảnh nhỏ hơn vẫn đi cùng nền tảng)"),
    "video": ("Video", "MP4, MOV, MKV, WEBM... từ 1 MB trở lên"),
    "am_thanh": ("Âm thanh", "WAV, MP3, M4A, FLAC... từ 1 MB trở lên"),
    "lam_tiep": ("Dữ liệu làm dở để AI làm tiếp", "thư mục work, asr, frames, chunks trong 04-ket-qua và tệp NPZ, NPY, PKL, mô hình"),
    "lon_khac": ("Tệp lớn khác", "mọi tệp từ 100 MB trở lên không thuộc nhóm trên (ZIP, DMG, PSD...); không gồm cơ sở dữ liệu và tệp chữ"),
}
_DUOI_ANH = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".heif", ".bmp", ".tif", ".tiff", ".psd", ".ai", ".raw", ".cr2", ".dng", ".svg")
_DUOI_VIDEO = (".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mpg", ".mpeg", ".wmv", ".flv", ".mts")
_DUOI_AM = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".aiff", ".opus")
_DUOI_LAM_TIEP = (".npz", ".npy", ".pkl", ".pickle", ".pt", ".pth", ".onnx", ".safetensors", ".ckpt")
_THU_MUC_LAM_TIEP = {"work", "asr", "frames", "chunks"}
NGUONG_PHUONG_TIEN = 1024 * 1024
NGUONG_LON = 100 * 1024 * 1024


def phan_loai_nang(ten: str, kich_thuoc: int) -> str:
    """'' nếu tệp thuộc NỀN TẢNG (luôn mang); ngược lại tên nhóm kho nặng. Chỉ xét tệp trong bộ não và Đội Quân AI."""
    if not ten.startswith(("bo-nao/", "doi-quan-home/")):
        return ""
    parts = [x.lower() for x in ten.split("/")]
    f = parts[-1]
    if "04-ket-qua" in parts and any(x in _THU_MUC_LAM_TIEP for x in parts[:-1]):
        return "lam_tiep"
    if f.endswith(_DUOI_LAM_TIEP):
        return "lam_tiep"
    if kich_thuoc >= NGUONG_PHUONG_TIEN:
        if f.endswith(_DUOI_VIDEO):
            return "video"
        if f.endswith(_DUOI_AM):
            return "am_thanh"
        if f.endswith(_DUOI_ANH):
            return "hinh_anh"
    if kich_thuoc >= NGUONG_LON and not f.endswith(DUOI_SQLITE + DUOI_CHU):
        return "lon_khac"
    return ""


def _kich_thuoc(p: Path) -> int:
    try:
        return p.stat().st_size
    except OSError:
        return 0


def uoc_tinh(tep=None) -> dict:
    """Báo cáo dung lượng TRƯỚC khi đóng gói: nền tảng bao nhiêu GB, từng nhóm kho nặng bao nhiêu GB, chỗ trống ở máy này và máy mới cần."""
    if tep is None:
        tep = danh_sach()
    nen = {"so_tep": 0, "dung_luong": 0}
    kho = {k: {"so_tep": 0, "dung_luong": 0, "ten": NHAN_KHO[k][0], "mo_ta": NHAN_KHO[k][1]} for k in KHO_NANG}
    for p, ten in tep:
        sz = _kich_thuoc(p)
        k = phan_loai_nang(ten, sz)
        d = kho[k] if k else nen
        d["so_tep"] += 1
        d["dung_luong"] += sz
    tong_kho = sum(v["dung_luong"] for v in kho.values())
    return {"nen_tang": nen, "kho_nang": kho, "tong_kho_nang": tong_kho, "tong_tat_ca": nen["dung_luong"] + tong_kho}


def can_cho_may_moi(dung_luong_goi: int) -> int:
    """Máy nhận cần trống khoảng 4 lần dung lượng gói (tải lên, giải gói, giữ bản cũ) cộng 2 GB. Cùng công thức với bước nhận gói."""
    return int(dung_luong_goi) * 4 + GIU_TRONG


def _sao_sqlite(p: Path) -> bytes:
    """Bản sao nhất quán của một CSDL đang mở (kể cả phần trong -wal)."""
    tam = VIEC / f".sao-{uuid.uuid4().hex}.db"
    try:
        nguon = sqlite3.connect(f"file:{p}?mode=ro", uri=True, timeout=30)
        dich = sqlite3.connect(str(tam))
        with dich:
            nguon.backup(dich)
        nguon.close(); dich.close()
        return tam.read_bytes()
    finally:
        try:
            tam.unlink()
        except OSError:
            pass


def _la_sqlite(p: Path) -> bool:
    if not p.name.endswith(DUOI_SQLITE):
        return False
    try:
        with open(p, "rb") as f:
            return f.read(16) == b"SQLite format 3\x00"
    except OSError:
        return False


def _dia_trong(p: Path) -> int:
    try:
        return shutil.disk_usage(str(p)).free
    except OSError:
        return 0


# ---------------------------------------------------------------- đóng gói
def nhan_dang_may() -> str:
    """Dấu nhận diện máy này: tên máy + thư mục cài. Gói tạo ở máy nào mang dấu của máy đó, để máy nhận biết gói có phải của
    chính nó không (áp dụng gói của chính mình, tạo từ lúc trước, là đưa dữ liệu QUAY VỀ lúc đó)."""
    return hashlib.sha256(f"{platform.node()}|{ROOT}".encode("utf-8")).hexdigest()[:16]


def _ban() -> str:
    try:
        return (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def _settings_cho_goi(p: Path) -> bytes:
    """Bản settings.json đi vào gói (V3.17). Máy này KHÔNG bị sửa, chỉ bản trong gói: đường hầm Cloudflare theo token bị đặt enabled=False.

    Lý do (chủ báo 18/11/2026): settings mang theo token đường hầm, máy nhận mà chạy bản chưa biết tự tắt thì nối vào ĐÚNG đường hầm của máy gốc,
    hai máy cùng trả lời một tên miền, chủ mở tên miền thấy lúc máy này lúc máy kia, thao tác nhầm máy. Token vẫn nằm trong gói để chủ bật lại
    ở máy mới khi muốn chuyển tên miền (sau khi đã tắt ở máy gốc)."""
    raw = p.read_bytes()
    try:
        d = json.loads(raw.decode("utf-8"))
        rt = d.get("remote_tunnel") if isinstance(d, dict) else None
        if isinstance(rt, dict) and rt.get("enabled") is True:
            rt["enabled"] = False
            return json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8")
    except (ValueError, UnicodeDecodeError):
        pass
    return raw


def _dq_env_cho_goi(p: Path) -> bytes:
    """Bản .env của Đội Quân AI đi vào gói (V3.17): các dòng nối BẢNG GIAO VIỆC trên Cloudflare được chú thích sẵn (máy gốc không bị sửa).

    Lý do (chủ báo 18/11/2026, thấy trong nhật ký đội hình lúc 18:01): bảng giao việc nằm trên Cloudflare, MỘT bảng dùng chung cho mọi máy có địa chỉ + khoá bảng.
    Máy nhận mà chạy bản chưa biết tự ngắt, hoặc tệp này nằm đường dẫn khác chỗ nó ngắt, thì đồng bộ đội hình của máy nhận thấy "hồ sơ cộng sự không còn"
    rồi XOÁ cộng sự khỏi bảng chung; máy gốc đọc bảng thấy mất, cất hồ sơ của 25 cộng sự. Dòng bị chú thích được `chinh_thuc` bật lại khi chủ chuyển chính thức."""
    raw = p.read_text(encoding="utf-8", errors="replace")
    dong = raw.splitlines(keepends=True)
    for i, d in enumerate(dong):
        if d.split("=", 1)[0].strip() in DQ_KHOA_CAN_TAT and "=" in d and not d.startswith(TIEN_TO_DQ):
            dong[i] = TIEN_TO_DQ + d
    return "".join(dong).encode("utf-8")


def _dq_da_tat_san() -> bool:
    try:
        return any(d.startswith(TIEN_TO_DQ) for d in DQ_ENV.read_text(encoding="utf-8").splitlines())
    except OSError:
        return False


def dong_goi(mat_khau: str, ra: Path, bao=None, chon=(), bo_tien_to=()) -> dict:
    """Đóng gói và mã hoá ra `ra`. `bao(phan_tram, chu)` báo tiến độ. Trả tóm tắt.

    `chon`: các nhóm KHO NẶNG muốn mang thêm (xem KHO_NANG). Mặc định rỗng = chỉ NỀN TẢNG. Nền tảng luôn được mang.
    `bo_tien_to`: bỏ các tệp có tên trong gói bắt đầu bằng những tiền tố này (Nhiều máy: hồ sơ trình duyệt, mô hình nghe offline không đi theo)."""
    if len(mat_khau or "") < 8:
        raise ValueError("Mật khẩu cần ít nhất 8 ký tự.")
    chon = [k for k in KHO_NANG if k in set(chon or ())]
    VIEC.mkdir(parents=True, exist_ok=True)
    tat_ca = [(p, ten) for p, ten in danh_sach() if not (bo_tien_to and ten.startswith(tuple(bo_tien_to)))]
    tep, bo_qua, thu_muc_bo = [], {k: {"so_tep": 0, "dung_luong": 0} for k in KHO_NANG}, {}
    for p, ten in tat_ca:
        sz = _kich_thuoc(p)
        k = phan_loai_nang(ten, sz)
        if k and k not in chon:
            bo_qua[k]["so_tep"] += 1
            bo_qua[k]["dung_luong"] += sz
            khoa = "/".join(ten.split("/")[1:min(5, ten.count("/"))])
            thu_muc_bo[khoa] = thu_muc_bo.get(khoa, 0) + sz
            continue
        tep.append((p, ten))
    bo_qua = {k: v for k, v in bo_qua.items() if v["so_tep"]}
    lon_bo = [{"thu_muc": k, "dung_luong": v} for k, v in sorted(thu_muc_bo.items(), key=lambda x: -x[1])[:8]]
    tong = sum((p.stat().st_size for p, _ in tep if p.exists()), 0)
    if _dia_trong(ra.parent) < tong + GIU_TRONG:
        raise ValueError(f"Máy không đủ chỗ trống để đóng gói (cần khoảng {tong / 1024 ** 3 + 2:.1f} GB).")
    ke_khai = {"loai": "tisa-chuyen-may", "phien_ban_goi": PHIEN_BAN, "chi_du_lieu": True, "duong_ham_da_tat_trong_goi": True, "bang_giao_viec_da_tat_trong_goi": True, "ban_tisa": _ban(), "ten_ban_tisa": _ten_ban(), "luc": time.strftime("%Y-%m-%d %H:%M"),
               "may": {"nhan_dang": nhan_dang_may(), "ten_may": platform.node(), "goc": str(ROOT), "nha": str(Path.home()), "bo_nao": str(BRAINS_DIR), "trang_thai": str(STATE_DIR),
                       "doi_quan_home": str(DQ_HOME), "he_dieu_hanh": sys.platform},
               "so_tep": len(tep), "dung_luong": tong,
               "tuy_chon": {"kho_nang_da_chon": chon, "kho_nang_bo_qua": bo_qua}}
    da, n_bo_nao = 0, set()
    tam = ra.with_suffix(ra.suffix + ".dang-tao")
    with open(tam, "wb") as fout:
        w = _GhiMaHoa(fout, mat_khau)
        with zipfile.ZipFile(w, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as z:
            z.writestr("tisa-chuyen-may.json", json.dumps(ke_khai, ensure_ascii=False, indent=1))
            try:
                z.writestr("mcp-may/mcp.json", json.dumps(gom_mcp_may(), ensure_ascii=False, indent=1))
            except Exception:  # noqa: BLE001 - không gom được thì gói vẫn đủ phần còn lại
                pass
            for i, (p, ten) in enumerate(tep):
                try:
                    if ten == "doi-quan-env/.env":
                        z.writestr(ten, _dq_env_cho_goi(p))        # V3.17: bản trong gói đã NGẮT bảng giao việc Cloudflare dùng chung
                    elif ten == "trang-thai/settings.json":
                        z.writestr(ten, _settings_cho_goi(p))     # V3.17: bản trong gói đã TẮT đường hầm, máy này không đổi gì
                    elif _la_sqlite(p):
                        z.writestr(ten, _sao_sqlite(p))
                    else:
                        nen = zipfile.ZIP_STORED if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov",
                                                                       ".zip", ".gz", ".tgz", ".mp3", ".m4a", ".pdf") else zipfile.ZIP_DEFLATED
                        z.write(p, ten, compress_type=nen)
                except (OSError, sqlite3.Error):
                    continue      # tệp vừa bị xoá / đang khoá: bỏ qua, không làm hỏng cả gói
                if ten.startswith("bo-nao/"):
                    n_bo_nao.add(ten.split("/")[1])
                da += p.stat().st_size if p.exists() else 0
                if bao and i % 50 == 0:
                    bao(int(da * 100 / max(tong, 1)), f"Đã gói {i + 1}/{len(tep)} tệp")
        w.close()
    os.replace(tam, ra)
    return {"so_tep": len(tep), "dung_luong": tong, "so_bo_nao": len(n_bo_nao), "file": str(ra), "kich_thuoc": ra.stat().st_size,
            "kho_nang_da_chon": chon, "kho_nang_bo_qua": bo_qua, "thu_muc_lon_bo_qua": lon_bo,
            "can_cho_may_moi": can_cho_may_moi(ra.stat().st_size)}


# ---------------------------------------------------------------- MCP nằm ngoài thư mục TISA BOT (V3.11)
# Chủ báo máy mới thiếu MCP: TISA BOT dùng cả kết nối riêng của nó (mcp_servers.json, đã vào gói) lẫn kết nối "sẵn có của máy" do Claude Code
# (~/.claude.json) và Codex (~/.codex/config.toml) giữ. Hai nơi sau không nằm trong thư mục TISA BOT nên bản V2.76 không mang.
_RE_MCP_CODEX = re.compile(r'^\[mcp_servers\.("[^"]+"|[^\].]+)(?:\.[^\]]+)?\]\s*$')


def _tach_codex(text: str) -> dict:
    """{tên máy chủ MCP: khối chữ của nó trong config.toml (kể cả bảng con .env, .http_headers)}."""
    khoi, cur = {}, None
    for dong in text.splitlines():
        m = _RE_MCP_CODEX.match(dong.strip())
        if m:
            cur = m.group(1).strip('"')
            khoi.setdefault(cur, []).append(dong)
            continue
        if dong.strip().startswith("["):
            cur = None
            continue
        if cur is not None:
            khoi[cur].append(dong)
    return {k: "\n".join(v).strip("\n") + "\n" for k, v in khoi.items()}


def _codex_cua_ung_dung(khoi: str) -> bool:
    """Máy chủ do ứng dụng ChatGPT/Codex tự cài (đường dẫn trong /Applications hoặc ./): máy mới tự có, không mang."""
    return bool(re.search(r'command\s*=\s*"(/Applications/|\./|[A-Za-z]:\\Program Files)', khoi))


def gom_mcp_may() -> dict:
    """Đọc kết nối MCP của Claude Code và Codex trên máy này. Chỉ ĐỌC."""
    nha = Path.home()
    ra = {"claude_user": {}, "claude_project": {}, "codex": {}, "may": str(nha)}
    try:
        d = json.loads((nha / ".claude.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        d = {}
    if isinstance(d, dict):
        if isinstance(d.get("mcpServers"), dict):
            ra["claude_user"] = d["mcpServers"]
        for duong, v in (d.get("projects") or {}).items():
            ms = v.get("mcpServers") if isinstance(v, dict) else None
            if isinstance(ms, dict) and ms and (_trong(duong, str(ROOT)) or _trong(duong, str(BRAINS_DIR))):
                ra["claude_project"][duong] = ms
    try:
        for ten, khoi in _tach_codex((nha / ".codex" / "config.toml").read_text(encoding="utf-8")).items():
            if not _codex_cua_ung_dung(khoi):
                ra["codex"][ten] = khoi
    except OSError:
        pass
    return ra


def _chay_duoc(cmd: str) -> bool:
    if not cmd:
        return True
    if os.sep in cmd or (os.altsep and os.altsep in cmd):
        return Path(os.path.expanduser(cmd)).exists()
    return shutil.which(cmd) is not None


def ap_mcp_may(nguon: Path, cap: list) -> dict:
    """Trộn kết nối MCP của máy cũ vào Claude Code / Codex của máy này: CHỈ THÊM cái chưa có, bản cũ của hai tệp được chép dự phòng.
    Trả {"them": [...], "thieu_chuong_trinh": [...]} để ghi nhật ký và hiện ở bước kiểm tra."""
    ra = {"them": [], "thieu_chuong_trinh": []}
    tep = nguon / "mcp-may" / "mcp.json"
    if not tep.is_file():
        return ra
    goi = json.loads(_thay(tep.read_text(encoding="utf-8"), cap, "json"))
    goi["codex"] = {t: _thay(k, cap, "toml") for t, k in (json.loads(tep.read_text(encoding="utf-8")).get("codex") or {}).items()}
    if _la_may_win():                           # Windows: máy chủ MCP chạy bằng npx/npm phải bọc cmd /c (yêu cầu của Claude Code trên Windows)
        for v in list((goi.get("claude_user") or {}).values()) + [x for ms in (goi.get("claude_project") or {}).values() for x in ms.values()]:
            if isinstance(v, dict) and str(v.get("command") or "").lower() in ("npx", "npm", "pnpm", "yarn", "uvx"):
                v["args"] = ["/c", v["command"]] + list(v.get("args") or [])
                v["command"] = "cmd"
    nha, gio = Path.home(), time.strftime("%Y%m%d-%H%M%S")

    def kiem(ten, cmd):
        if not _chay_duoc(str(cmd or "")):
            ra["thieu_chuong_trinh"].append(f"{ten} (thiếu chương trình {cmd})")
    # Claude Code
    cj = nha / ".claude.json"
    try:
        d = json.loads(cj.read_text(encoding="utf-8")) if cj.is_file() else {}
    except (OSError, ValueError):
        d = None             # tệp đang hỏng hoặc đang bị ghi dở: không đụng
    if isinstance(d, dict) and (goi.get("claude_user") or goi.get("claude_project")):
        doi = False
        hien = d.setdefault("mcpServers", {}) if isinstance(d.get("mcpServers", {}), dict) else {}
        for ten, v in (goi.get("claude_user") or {}).items():
            if ten not in hien:
                hien[ten] = v; doi = True; ra["them"].append("Claude: " + ten); kiem("Claude: " + ten, (v or {}).get("command"))
        for duong, ms in (goi.get("claude_project") or {}).items():
            pj = d.setdefault("projects", {}).setdefault(duong, {})
            if not isinstance(pj.get("mcpServers"), dict):
                pj["mcpServers"] = {}
            for ten, v in ms.items():
                if ten not in pj["mcpServers"]:
                    pj["mcpServers"][ten] = v; doi = True; ra["them"].append("Claude (%s): %s" % (Path(duong).name, ten))
        if doi:
            if cj.is_file():
                shutil.copy2(cj, cj.with_name(f".claude.json.truoc-chuyen-may-{gio}"))
            tam = cj.with_name(".claude.json.chuyen-may.tmp")
            tam.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                os.chmod(tam, 0o600)
            except OSError:
                pass
            os.replace(tam, cj)
    # Codex
    if goi.get("codex"):
        cf = nha / ".codex" / "config.toml"
        try:
            ht = cf.read_text(encoding="utf-8") if cf.is_file() else ""
            co = set(_tach_codex(ht))
            them = [(t, k) for t, k in goi["codex"].items() if t not in co]
            if them:
                if cf.is_file():
                    shutil.copy2(cf, cf.with_name(f"config.toml.truoc-chuyen-may-{gio}"))
                cf.parent.mkdir(parents=True, exist_ok=True)
                with open(cf, "a", encoding="utf-8") as f:
                    f.write(("\n" if ht and not ht.endswith("\n") else "") + "\n# --- thêm từ máy cũ khi chuyển máy (TISA BOT) ---\n" + "\n".join(k for _, k in them))
                for t, k in them:
                    ra["them"].append("Codex: " + t)
                    m = re.search(r'command\s*=\s*"([^"]+)"', k)
                    if m:
                        kiem("Codex: " + t, m.group(1))
                    for tep_can in re.findall(re.escape(str(nha)) + r"/[^\s'\"\\]+", k):     # chương trình tự viết nằm trong thư mục riêng (vd ~/.codex/mcp/...) không đi theo gói
                        if not Path(tep_can).exists():
                            ra["thieu_chuong_trinh"].append(f"Codex: {t} (thiếu {tep_can})")
                            break
        except OSError:
            pass
    return ra


# ---------------------------------------------------------------- nhận
def _dai(p: Path) -> Path:
    """Windows: đường dẫn dài hơn 260 ký tự (tên thư mục tiếng Việt lồng nhiều tầng) phải có tiền tố \\?\\ mới mở được."""
    if os.name == "nt":
        t = os.path.abspath(str(p))
        if len(t) > 240 and not t.startswith("\\\\?\\"):
            return Path("\\\\?\\" + t)
    return p


def _an_toan(ten: str) -> bool:
    """Tên trong gói không được thoát ra ngoài thư mục chờ."""
    if not ten or ten.startswith(("/", "\\")) or "\\" in ten or ":" in ten:
        return False
    parts = Path(ten).parts
    return bool(parts) and ".." not in parts


def nhan(file: Path, mat_khau: str, bao=None) -> dict:
    """Giải mã, kiểm tra và giải nén vào thư mục chờ. Chưa đụng gì vào dữ liệu đang chạy."""
    VIEC.mkdir(parents=True, exist_ok=True)
    can = file.stat().st_size * 3 + GIU_TRONG
    if _dia_trong(VIEC) < can:
        raise ValueError(f"Máy không đủ chỗ trống (cần khoảng {can / 1024 ** 3:.1f} GB).")
    zip_tam = VIEC / f".giai-{uuid.uuid4().hex}.zip"
    if bao:
        bao(5, "Đang kiểm tra mật khẩu và giải mã...")
    try:
        giai_ma(file, zip_tam, mat_khau)
        if bao:
            bao(40, "Đang giải nén...")
        shutil.rmtree(CHO, ignore_errors=True)
        CHO.mkdir(parents=True)
        with zipfile.ZipFile(zip_tam) as z:
            try:
                ke_khai = json.loads(z.read("tisa-chuyen-may.json").decode("utf-8"))
            except KeyError:
                raise ValueError("File thiếu phần kê khai, không phải gói chuyển máy hợp lệ.")
            if ke_khai.get("loai") != "tisa-chuyen-may":
                raise ValueError("File không phải gói chuyển máy của TISA BOT.")
            ds = [m for m in z.infolist() if not m.is_dir() and m.filename != "tisa-chuyen-may.json"]
            bo_qua = 0
            khong_ghi = []
            for i, m in enumerate(ds):
                if not _an_toan(m.filename) or m.filename.split("/")[0] not in ("goc", "bo-nao", "trang-thai", "doi-quan-home", "doi-quan-env", "mcp-may"):
                    if m.filename.split("/")[0] in ("goc", "bo-nao", "trang-thai", "doi-quan-home", "doi-quan-env", "mcp-may"):
                        khong_ghi.append(m.filename)           # tên tệp có ký tự không hợp lệ (vd dấu hai chấm): báo, không im lặng bỏ
                    continue
                dau_goi, _, rel_goi = m.filename.partition("/")
                if (dau_goi == "goc" and la_ma_nguon_goc(rel_goi)) or (dau_goi == "trang-thai" and la_ma_nguon_trang_thai(rel_goi)):
                    bo_qua += 1          # gói của bản cũ hơn có thể mang cả chương trình của máy cũ: không bao giờ đặt đè lên máy này
                    continue
                dich = CHO / m.filename
                try:
                    _dai(dich.parent).mkdir(parents=True, exist_ok=True)
                    with z.open(m) as a, open(_dai(dich), "wb") as b:
                        shutil.copyfileobj(a, b, 1024 * 1024)
                    mode = (m.external_attr >> 16) & 0o777
                    if mode & 0o111 and os.name != "nt":
                        os.chmod(dich, mode | 0o600)            # giữ quyền chạy của tập lệnh (zip không tự giữ khi giải nén)
                except OSError:
                    khong_ghi.append(m.filename)                # Windows: tên không hợp lệ hoặc đường dẫn quá dài; một tệp lỗi không làm hỏng cả gói
                    continue
                if bao and i % 100 == 0:
                    bao(40 + int(i * 55 / max(len(ds), 1)), f"Đã giải nén {i + 1}/{len(ds)} tệp")
        bo_nao = sorted(p.name for p in (CHO / "bo-nao").iterdir() if p.is_dir()) if (CHO / "bo-nao").is_dir() else []
        may_goi = ke_khai.get("may") or {}
        cung = (may_goi.get("nhan_dang") == nhan_dang_may()) if may_goi.get("nhan_dang") else \
            (may_goi.get("goc") == str(ROOT) and may_goi.get("nha") == str(Path.home()))
        ban_cu, ban_nay = str(ke_khai.get("ban_tisa") or ""), _ban()
        vc, vn = _ver(ban_cu), _ver(ban_nay)
        so_sanh = "khong-ro" if not vc or not vn else ("may-nay-cu-hon" if vn < vc else "bang" if vn == vc else "may-nay-moi-hon")
        tom = {"ke_khai": ke_khai, "bo_nao": bo_nao, "so_tep": ke_khai.get("so_tep"), "dung_luong": ke_khai.get("dung_luong"),
               "cung_may": bool(cung), "ten_may_goi": may_goi.get("ten_may") or "", "bo_qua_ma_nguon": bo_qua,
               "khong_ghi_duoc": len(khong_ghi), "mau_khong_ghi": khong_ghi[:8], "ban_may_cu": ban_cu, "ten_ban_may_cu": str(ke_khai.get("ten_ban_tisa") or ""), "ban_may_nay": ban_nay, "ten_ban_may_nay": _ten_ban(), "so_sanh_ban": so_sanh}
        (VIEC / "cho-ap-dung-tom-tat.json").write_text(json.dumps(tom, ensure_ascii=False), encoding="utf-8")
        return tom
    except Exception:
        shutil.rmtree(CHO, ignore_errors=True)
        raise
    finally:
        try:
            zip_tam.unlink()
        except OSError:
            pass


def hen_ap_dung(khoi_dong_lai: bool = True, dong_y_quay_lai: bool = False) -> None:
    """Đánh dấu chờ áp dụng rồi khởi động lại: lần chạy mới đổi dữ liệu trước khi mở CSDL.
    Từ dòng lệnh (khoi_dong_lai=False) chỉ đánh dấu: tiến trình dòng lệnh không phải máy chủ, người dùng tự khởi động lại."""
    if not CHO.is_dir():
        raise ValueError("Chưa có dữ liệu nhận về để áp dụng.")
    tom = json.loads((VIEC / "cho-ap-dung-tom-tat.json").read_text(encoding="utf-8"))
    if tom.get("so_sanh_ban") == "may-nay-cu-hon":
        raise ValueError(f"Máy này đang chạy TISA BOT bản {tom.get('ban_may_nay')}, thấp hơn máy cũ (bản {tom.get('ban_may_cu')}). "
                         "Hãy cập nhật TISA BOT trên máy này lên bản mới nhất (menu Hệ thống, Cập nhật), rồi tải file lên lại. "
                         "Dữ liệu của bản mới không nên đặt vào chương trình bản cũ.")
    if tom.get("cung_may") and not dong_y_quay_lai:
        raise ValueError("Gói này được tạo từ CHÍNH máy này, áp dụng sẽ đưa dữ liệu quay về lúc "
                         f"{(tom.get('ke_khai') or {}).get('luc')} và mất mọi thay đổi sau đó. Nếu vẫn muốn, hãy tick ô xác nhận.")
    DANH_DAU.write_text(json.dumps({"luc": time.time(), "ke_khai": tom.get("ke_khai"), "khong_ghi": tom.get("khong_ghi_duoc") or 0,
                                    "mau_khong_ghi": tom.get("mau_khong_ghi") or []}, ensure_ascii=False), encoding="utf-8")
    if not khoi_dong_lai:
        return
    try:
        import tisa_khoi_dong_lai
        tisa_khoi_dong_lai.hen_khoi_dong_lai("chuyển máy: áp dụng dữ liệu máy cũ")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Đã nhận dữ liệu nhưng chưa khởi động lại được ({e}). Hãy tắt rồi mở lại TISA BOT.")


# ---------------------------------------------------------------- áp dụng (đầu lần khởi động mới)
def _cap_doi(ke_khai: dict) -> list:
    """Các cặp (đường dẫn máy cũ, đường dẫn máy mới) THÔ, dài trước ngắn sau để không thay nhầm phần đầu.
    Dạng viết vào từng loại tệp (JSON phải thoát dấu gạch ngược, TOML dùng gạch xuôi) do `_thay` quyết."""
    cu = (ke_khai or {}).get("may") or {}
    cap = [(cu.get("bo_nao"), str(BRAINS_DIR)), (cu.get("doi_quan_home"), str(DQ_HOME)),
           (cu.get("trang_thai"), str(STATE_DIR)), (cu.get("goc"), str(ROOT)), (cu.get("nha"), str(Path.home()))]
    cap = [(a, b) for a, b in cap if a and b and a != b]
    return sorted(cap, key=lambda x: -len(x[0]))


_RE_O_DIA = re.compile(r"^[A-Za-z]:[\\/]")
# Một đoạn đường dẫn: cho phép dấu cách GIỮA chữ (tên thư mục như "Brain Default") nhưng không nuốt đường dẫn kế tiếp sau dấu cách.
_DOAN = r'(?:[^\\/"\'\s]|\s(?=[^\s\\/"\']))*'


def _la_win(p: str) -> bool:
    return bool(_RE_O_DIA.match(p or "")) or "\\" in (p or "")


def _la_may_win() -> bool:
    return sys.platform == "win32"


def _thay(chu: str, cap: list, kieu: str) -> str:
    """Đổi tiền tố đường dẫn của máy cũ sang máy mới trong một đoạn chữ, rồi đổi dấu phân cách của PHẦN ĐUÔI theo máy mới.
    Đủ 4 hướng: Mac->Win, Win->Mac, Mac->Mac, Win->Win. kieu: "json" (thoát dấu gạch ngược), "toml" (đích luôn gạch xuôi), "tho" (văn bản thường).
    V3.11: bản cũ chèn đường dẫn Windows thẳng vào JSON làm hỏng settings.json, và Win->Mac để lại dấu gạch ngược trong đường dẫn Mac."""
    for a, b in cap:
        a_win, b_win = _la_win(a), _la_win(b)
        if kieu == "json":
            a_t, b_t = json.dumps(a)[1:-1], json.dumps(b)[1:-1]
            sep_dich = "\\\\" if b_win else "/"
        elif kieu == "toml":
            a_t, b_t, sep_dich = a, b.replace("\\", "/"), "/"
        else:
            a_t, b_t, sep_dich = a, b, ("\\" if b_win else "/")
        nguon = []
        if a_win:
            nguon.append((a_t, "\\\\" if kieu == "json" else "\\"))
            nguon.append((a.replace("\\", "/"), "/"))       # ứng dụng node/Claude hay ghi đường dẫn Windows bằng gạch xuôi
        else:
            nguon.append((a_t, "/"))
        for t, sep in nguon:
            if t not in chu:
                continue
            chu = chu.replace(t, b_t)
            if sep != sep_dich:
                chu = re.sub(re.escape(b_t) + "((?:" + re.escape(sep) + _DOAN + ")+)", lambda m, sep=sep: b_t + m.group(1).replace(sep, sep_dich), chu)
    return chu


def _sua_duong_dan(goc: Path, cap: list) -> int:
    n = 0
    if not cap:
        return 0
    for dp, dn, fn in os.walk(goc):
        dn[:] = [d for d in dn if d not in BO_THU_MUC]
        for f in fn:
            p = Path(dp) / f
            try:
                if p.suffix.lower() in DUOI_CHU or (f.startswith(".") and p.suffix == ""):
                    n += _sua_tep(p, cap)
                elif _la_sqlite(p):
                    n += _sua_sqlite(p, cap)
            except (OSError, UnicodeDecodeError, sqlite3.Error):
                continue
    return n


def _sua_tep(p: Path, cap: list) -> int:
    try:
        if not p.is_file() or p.stat().st_size > 5_000_000:
            return 0
        s = p.read_text(encoding="utf-8")
        suf = p.suffix.lower()
        m = _thay(s, cap, "json" if suf in (".json", ".jsonl") else "toml" if suf == ".toml" else "tho")
        if m != s:
            p.write_text(m, encoding="utf-8")
            return 1
    except (OSError, UnicodeDecodeError):
        pass
    return 0


def _sua_sqlite(p: Path, cap: list) -> int:
    n = 0
    con = sqlite3.connect(str(p))
    try:
        mau = []
        for a, _ in cap:
            for m in (a, json.dumps(a)[1:-1], a.replace("\\", "/")):
                if m and m not in mau:
                    mau.append(m)
        bang = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
        for b in bang:
            try:
                cot = [r[1] for r in con.execute(f'pragma table_info("{b}")') if (r[2] or "").upper() in ("TEXT", "", "VARCHAR", "JSON")]
            except sqlite3.Error:
                continue
            for c in cot:
                try:
                    dk = " or ".join(f'instr("{c}", ?) > 0' for _ in mau)
                    hang = con.execute(f'select rowid, "{c}" from "{b}" where {dk}', mau).fetchall()
                    for rid, v in hang:
                        if not isinstance(v, str):
                            continue
                        nv = _thay(v, cap, "json" if v[:1] in ("{", "[") else "tho")
                        if nv != v:
                            con.execute(f'update "{b}" set "{c}" = ? where rowid = ?', (nv, rid))
                            n += 1
                except sqlite3.Error:
                    continue
        con.commit()
    finally:
        con.close()
    return 1 if n else 0


def _dat_vao(nguon: Path, dich: Path, du_phong: Path) -> None:
    """Đưa mọi tệp dưới `nguon` vào `dich`; tệp cùng tên đang có thì dời sang `du_phong` (giữ cây thư mục)."""
    if not nguon.is_dir():
        return
    for dp, dn, fn in os.walk(nguon):
        rel = Path(dp).relative_to(nguon)
        for f in fn:
            a, b = _dai(Path(dp) / f), _dai(dich / rel / f)
            b.parent.mkdir(parents=True, exist_ok=True)
            if b.exists() or b.is_symlink():
                c = _dai(du_phong / rel / f)
                c.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(b), str(c))
            if _la_sqlite(a):
                for duoi in ("-wal", "-shm"):
                    cu = Path(str(b) + duoi)
                    if cu.exists():
                        c = du_phong / rel / (f + duoi)
                        c.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(cu), str(c))
            shutil.move(str(a), str(b))


DANH_DAU_KHOI_PHUC = VIEC / "cho-khoi-phuc.json"


def du_phong_khoi_phuc_duoc():
    """Thư mục `_truoc-chuyen-may-…` gần nhất còn tệp để trả về, hoặc None."""
    try:
        for d in sorted(ROOT.glob("_truoc-chuyen-may-*"), reverse=True):
            if any(f.is_file() for f in d.rglob("*")):
                return d
    except OSError:
        pass
    return None


def hen_khoi_phuc() -> None:
    """Hẹn trả dữ liệu về bản trước lần chuyển máy gần nhất rồi khởi động lại (đổi dữ liệu ngay đầu lần chạy mới)."""
    d = du_phong_khoi_phuc_duoc()
    if not d:
        raise ValueError("Không còn bản trước khi chuyển máy để khôi phục.")
    VIEC.mkdir(parents=True, exist_ok=True)
    DANH_DAU_KHOI_PHUC.write_text(json.dumps({"luc": time.time(), "tu": str(d)}, ensure_ascii=False), encoding="utf-8")
    try:
        import tisa_khoi_dong_lai
        tisa_khoi_dong_lai.hen_khoi_dong_lai("chuyển máy: khôi phục bản trước")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Đã hẹn khôi phục nhưng chưa khởi động lại được ({e}). Hãy tắt rồi mở lại TISA BOT.")


def _khoi_phuc(nguon: Path) -> int:
    """Trả mọi tệp trong `nguon` (một thư mục `_truoc-chuyen-may-…`) về chỗ cũ; bản đang có cất vào `_ban-goi-da-ap-dung-<giờ>`."""
    cat = ROOT / f"_ban-goi-da-ap-dung-{time.strftime('%Y%m%d-%H%M%S')}"
    n = 0
    dich = {"goc": ROOT, "trang-thai": STATE_DIR, "bo-nao": BRAINS_DIR, "doi-quan-home": DQ_HOME}
    for ten, goc in dich.items():
        for dp, _dn, fn in os.walk(nguon / ten):
            for f in fn:
                a = Path(dp) / f
                rel = a.relative_to(nguon / ten)
                d = goc / rel
                if d.exists() or d.is_symlink():
                    h = cat / ten / rel
                    h.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(d), str(h))
                if f.endswith(DUOI_SQLITE):     # -wal/-shm của bản đang chạy không được đứng cạnh CSDL cũ trả về
                    for duoi in ("-wal", "-shm"):
                        c = Path(str(d) + duoi)
                        if (c.exists() or c.is_symlink()) and not Path(str(a) + duoi).exists():
                            h = cat / ten / (str(rel) + duoi)
                            h.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(c), str(h))
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(a), str(d))
                n += 1
    env = nguon / "doi-quan-env" / ".env"
    if env.is_file():
        DQ_ENV.parent.mkdir(parents=True, exist_ok=True)
        if DQ_ENV.exists():
            (cat / "doi-quan-env").mkdir(parents=True, exist_ok=True)
            shutil.move(str(DQ_ENV), str(cat / "doi-quan-env" / ".env"))
        shutil.move(str(env), str(DQ_ENV))
        n += 1
    return n


def ap_dung_khi_khoi_dong() -> None:
    """Gọi ở dòng đầu main.py: áp dụng gói đang chờ (nếu có), rồi LUÔN kiểm lại chế độ cách ly của máy mới."""
    try:
        _ap_dung_goi()
    finally:
        try:
            ap_cach_ly()
        except Exception as e:  # noqa: BLE001 - lỗi cách ly chỉ ghi nhật ký, không chặn máy chủ
            try:
                with open(VIEC / "chuyen-may.log", "a", encoding="utf-8") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} LỖI cách ly: {type(e).__name__}: {e}\n")
            except OSError:
                pass


def _ap_dung_goi() -> None:
    """Có dấu chờ áp dụng thì đổi dữ liệu, xong xoá dấu. Lỗi thì ghi nhật ký, giữ máy chạy."""
    nk = VIEC / "chuyen-may.log"
    if DANH_DAU_KHOI_PHUC.is_file():
        try:
            tu = Path(json.loads(DANH_DAU_KHOI_PHUC.read_text(encoding="utf-8")).get("tu") or "")
            DANH_DAU_KHOI_PHUC.unlink()
            if tu.is_dir() and tu.parent == ROOT:
                n = _khoi_phuc(tu)
                for t in ("da-ap-dung.json", "cho-ap-dung-tom-tat.json", "che-do-thu.json"):
                    try:
                        (VIEC / t).unlink()
                    except OSError:
                        pass
                with open(nk, "a", encoding="utf-8") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} đã KHÔI PHỤC {n} tệp từ {tu.name}\n")
        except Exception as e:  # noqa: BLE001
            try:
                with open(nk, "a", encoding="utf-8") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} LỖI khôi phục: {type(e).__name__}: {e}\n")
            except OSError:
                pass
        return
    if not DANH_DAU.is_file() or not CHO.is_dir():
        return
    try:
        dau = json.loads(DANH_DAU.read_text(encoding="utf-8"))
        DANH_DAU.unlink()                      # chỉ thử một lần, lỗi giữa chừng không lặp lại vô tận
        ke_khai = dau.get("ke_khai") or {}
        du_phong = ROOT / f"_truoc-chuyen-may-{time.strftime('%Y%m%d-%H%M%S')}"
        _dat_vao(CHO / "goc", ROOT, du_phong / "goc")
        _dat_vao(CHO / "trang-thai", STATE_DIR, du_phong / "trang-thai")
        _dat_vao(CHO / "bo-nao", BRAINS_DIR, du_phong / "bo-nao")
        _dat_vao(CHO / "doi-quan-home", DQ_HOME, du_phong / "doi-quan-home")
        env_moi = CHO / "doi-quan-env" / ".env"
        if env_moi.is_file():
            DQ_ENV.parent.mkdir(parents=True, exist_ok=True)
            if DQ_ENV.exists():
                (du_phong / "doi-quan-env").mkdir(parents=True, exist_ok=True)
                shutil.move(str(DQ_ENV), str(du_phong / "doi-quan-env" / ".env"))
            shutil.move(str(env_moi), str(DQ_ENV))
        cap = _cap_doi(ke_khai)
        n = 0
        for g in {STATE_DIR, BRAINS_DIR, DQ_HOME, SERVER}:
            n += _sua_duong_dan(g, cap)
        for p in (ROOT / ".env", DQ_ENV):
            n += _sua_tep(p, cap)
        try:
            mcp_ra = ap_mcp_may(CHO, cap)
        except Exception as e:  # noqa: BLE001 - MCP ngoài lỗi thì phần còn lại vẫn áp dụng
            mcp_ra = {"them": [], "thieu_chuong_trinh": [], "loi": f"{type(e).__name__}: {e}"[:160]}
        try:
            lenh_ra = sua_lenh_mcp_tisa()
        except Exception as e:  # noqa: BLE001
            lenh_ra = {"da_sua": [], "thieu": [f"không kiểm tra được: {type(e).__name__}"]}
        shutil.rmtree(CHO, ignore_errors=True)
        kenh_tat = _tam_tat_kenh()
        _luu_che_do_thu({"giai_doan": "thu", "luc": time.time(), "kenh_tam_tat": kenh_tat, "ban_may_cu": ke_khai.get("ban_tisa"),
                         "ten_may_cu": (ke_khai.get("may") or {}).get("ten_may") or "", "mcp_them": mcp_ra.get("them"),
                         "mcp_thieu": mcp_ra.get("thieu_chuong_trinh"), "mcp_loi": mcp_ra.get("loi", ""),
                         "khong_ghi": dau.get("khong_ghi") or 0, "mau_khong_ghi": dau.get("mau_khong_ghi") or [], "mcp_tisa_sua": lenh_ra.get("da_sua"), "mcp_tisa_thieu": lenh_ra.get("thieu"),
                         "khac_he_dieu_hanh": (ke_khai.get("may") or {}).get("he_dieu_hanh") not in (None, sys.platform)})
        with open(nk, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} đã áp dụng dữ liệu máy cũ ({ke_khai.get('luc')}), "
                    f"sửa đường dẫn ở {n} tệp, bản cũ của máy này ở {du_phong}\n")
        (VIEC / "da-ap-dung.json").write_text(json.dumps({"luc": time.time(), "du_phong": str(du_phong),
                                                          "tu_may": ke_khai.get("may"), "ban": ke_khai.get("ban_tisa")},
                                                         ensure_ascii=False), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        try:
            VIEC.mkdir(parents=True, exist_ok=True)
            with open(nk, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} LỖI áp dụng: {type(e).__name__}: {e}\n")
        except OSError:
            pass


# ---------------------------------------------------------------- MCP của chính TISA BOT sau khi đổi máy (V3.11)
_RE_PY = re.compile(r"[\\/]\.venv[\\/](?:bin|Scripts)[\\/]python(?:3(?:\.\d+)?)?(?:\.exe)?$", re.I)


def _doc_mcp_tisa():
    p = STATE_DIR / "mcp_servers.json"
    try:
        return p, json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return p, None


def _ghi_mcp_tisa(p: Path, d: dict) -> None:
    tam = p.with_suffix(".json.tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tam, p)


def sua_lenh_mcp_tisa() -> dict:
    """Kết nối MCP kiểu stdio của TISA BOT (mcp_servers.json) chạy bằng Python của môi trường cài đặt: .venv/bin/python trên Mac, .venv\\Scripts\\python.exe
    trên Windows. Đổi hệ điều hành thì đường dẫn đó SAI dù tiền tố đã được đổi (chủ báo thiếu MCP sau khi chuyển Mac sang Windows). Đặt lại đúng cho máy này,
    rồi báo kết nối nào vẫn thiếu chương trình (Node/npx, uvx...). Trả {"da_sua": [...], "thieu": [...]}."""
    ra = {"da_sua": [], "thieu": []}
    p, d = _doc_mcp_tisa()
    if not isinstance(d, dict) or not isinstance(d.get("connections"), list):
        return ra
    doi = False
    py = ROOT / ".venv" / ("Scripts/python.exe" if _la_may_win() else "bin/python")
    for c in d["connections"]:
        if not isinstance(c, dict) or c.get("transport") != "stdio" or not isinstance(c.get("command"), str):
            continue
        cmd = c["command"]
        if _RE_PY.search(cmd) and str(py) != cmd and py.exists():
            c["command"] = str(py)
            doi = True
            ra["da_sua"].append(str(c.get("label") or c.get("id")))
        elif not _chay_duoc(c["command"]):
            ra["thieu"].append(f"{c.get('label') or c.get('id')} (thiếu chương trình {c['command']})")
    if doi:
        _ghi_mcp_tisa(p, d)
    return ra


# ---------------------------------------------------------------- CÁCH LY máy mới (V3.11)
# Chủ dặn 18/11/2026: máy mới KHÔNG được tự đồng bộ hay chạy cùng máy cũ; chạy thử riêng, kiểm tra ổn hết rồi mới chuyển thật.
# Gói mang theo mọi thứ nên máy mới khởi động là có thể tự: nối đường hầm tên miền, nhận tin Telegram/Zalo, chạy việc định kỳ và nhắc hẹn (lịch của máy cũ),
# chạy việc Kanban đang xếp hàng, để Auto của cộng sự tự chạy, đẩy GitHub, nối Zalo cùng một tài khoản, nối cùng bảng giao việc Cloudflare. Mọi thứ đó TẠM DỪNG
# trong suốt chế độ thử (mỗi lần máy chủ khởi động đều kiểm lại), và chỉ bật lại khi chủ bấm chuyển chính thức.
CACH_LY_GD = ("thu", "ten-mien")
TIEN_TO_DQ = "#TISA-CACH-LY# "
# Tên khoá có hai dạng (tệp .env của bản cũ dùng tiền tố cũ, bản mới dùng TISA_); viết tách ra để bước đổi tên khi dựng không biến mất một dạng.
DQ_KHOA_CAN_TAT = ("BOARD_URL", "BOARD_TOKEN") + tuple(tt + hau for tt in ("JAV" + "IS_", "TISA_") for hau in ("URL", "HOOK_ID", "HOOK_TOKEN"))
BIEN_TAM_DUNG = ("TISA_RESONANCE_TICK_PAUSED", "TISA_PULSE_TICK_PAUSED", "TISA_AUTO_BACKGROUND_PAUSED", "TISA_AUTO_LEARNING_PAUSED")


def dang_cach_ly() -> bool:
    d = doc_che_do_thu()
    return bool(d) and d.get("giai_doan") in CACH_LY_GD


def _tam_tat_dq() -> bool:
    """Chú thích các dòng nối bảng giao việc đám mây trong tệp .env của Đội Quân AI (giữ nguyên giá trị, chỉ thêm tiền tố). True nếu có đổi."""
    try:
        if not DQ_ENV.is_file():
            return False
        dong = DQ_ENV.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError:
        return False
    doi = False
    for i, d in enumerate(dong):
        if d.split("=", 1)[0].strip() in DQ_KHOA_CAN_TAT and "=" in d and not d.startswith(TIEN_TO_DQ):
            dong[i] = TIEN_TO_DQ + d
            doi = True
    if doi:
        DQ_ENV.write_text("".join(dong), encoding="utf-8")
    return doi


def _bat_lai_dq() -> bool:
    try:
        if not DQ_ENV.is_file():
            return False
        dong = DQ_ENV.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError:
        return False
    doi = False
    for i, d in enumerate(dong):
        if d.startswith(TIEN_TO_DQ):
            dong[i] = d[len(TIEN_TO_DQ):]
            doi = True
    if doi:
        DQ_ENV.write_text("".join(dong), encoding="utf-8")
    return doi


def _doi_trang_thai_mcp(ids, bat: bool, loc_zalo: bool = False) -> list:
    """Bật/tắt các kết nối MCP của TISA BOT. loc_zalo: chọn mọi kết nối Zalo đang bật (cùng một tài khoản Zalo đăng nhập ở hai máy sẽ đá nhau). Trả danh sách id đã đổi."""
    p, d = _doc_mcp_tisa()
    if not isinstance(d, dict) or not isinstance(d.get("connections"), list):
        return []
    ra = []
    for c in d["connections"]:
        if not isinstance(c, dict):
            continue
        if loc_zalo:
            chon = c.get("enabled") is True and "zalo" in json.dumps(c, ensure_ascii=False).lower()
        else:
            chon = c.get("id") in ids
        if chon and bool(c.get("enabled")) != bat:
            c["enabled"] = bat
            ra.append(c.get("id"))
    if ra:
        _ghi_mcp_tisa(p, d)
    return ra


def ap_cach_ly() -> dict:
    """Gọi MỖI lần máy chủ khởi động (ap_dung_khi_khoi_dong), trước mọi vòng nền. Không ở chế độ thử thì không làm gì."""
    d = doc_che_do_thu()
    if not d or d.get("giai_doan") not in CACH_LY_GD:
        return {}
    os.environ["TISA_CACH_LY"] = "1"        # main.py: vòng lập lịch và Kanban đứng yên khi cờ này bật
    for k in BIEN_TAM_DUNG:
        os.environ[k] = "1"
    st = _doc_cai_dat()
    tat = list(d.get("kenh_tam_tat") or [])
    doi = False
    for k in KENH_NHAN_TIN + ("backup",):
        v = st.get(k)
        if isinstance(v, dict) and v.get("enabled") is True:
            v["enabled"] = False; doi = True
            if k not in tat:
                tat.append(k)
    rt = st.get("remote_tunnel")
    if isinstance(rt, dict) and rt.get("enabled") is True and str(rt.get("mode") or "token") == "token":
        rt["enabled"] = False; doi = True
        if "remote_tunnel" not in tat:
            tat.append("remote_tunnel")
    if not st.get("schedules_off_here"):
        st["schedules_off_here"] = True; doi = True
        d.setdefault("lich_truoc", False)
    if doi:
        _ghi_cai_dat(st)
    if _tam_tat_dq() or _dq_da_tat_san():
        d["dq_tam_tat"] = True
    mcp_tat = _doi_trang_thai_mcp(None, False, loc_zalo=True)
    if mcp_tat:
        d["mcp_tam_tat"] = sorted(set((d.get("mcp_tam_tat") or []) + mcp_tat))
    d["kenh_tam_tat"] = tat
    d["cach_ly"] = True
    _luu_che_do_thu(d)
    return d


# ---------------------------------------------------------------- chế độ thử trên máy mới
def _doc_cai_dat() -> dict:
    try:
        d = json.loads((STATE_DIR / "settings.json").read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _ghi_cai_dat(st: dict) -> None:
    p = STATE_DIR / "settings.json"
    tam = p.with_suffix(".json.tmp")
    tam.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(tam, 0o600)
    except OSError:
        pass
    os.replace(tam, p)


def _tam_tat_kenh() -> list:
    """Tắt các kênh nhận tin đang bật (Telegram, Zalo bot, ...) trên máy MỚI để không trả lời trùng với máy cũ. Trả danh sách đã tắt."""
    st = _doc_cai_dat()
    tat = []
    for k in KENH_NHAN_TIN:
        v = st.get(k)
        if isinstance(v, dict) and v.get("enabled") is True:
            v["enabled"] = False
            tat.append(k)
    # V3.11: đường hầm Cloudflare theo TOKEN của máy cũ. settings.json mang theo token này, máy mới khởi động là tự nối vào ĐÚNG đường hầm đó,
    # thế là hai máy cùng trả lời một tên miền và chủ thấy lúc máy cũ lúc máy mới (18/11/2026). Tắt ở máy mới; đường hầm riêng của máy mới
    # (cloudflared cài bằng lệnh Cloudflare đưa, hoặc bật lại ở Cài đặt, Truy cập từ xa sau khi tắt ở máy cũ) do chủ tự quyết ở bước 2.
    rt = st.get("remote_tunnel")
    if isinstance(rt, dict) and rt.get("enabled") is True and str(rt.get("mode") or "token") == "token":
        rt["enabled"] = False
        tat.append("remote_tunnel")
    if tat:
        _ghi_cai_dat(st)
    return tat


def doc_che_do_thu():
    try:
        return json.loads(CHE_DO_THU.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _luu_che_do_thu(d: dict) -> None:
    VIEC.mkdir(parents=True, exist_ok=True)
    CHE_DO_THU.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def sang_ten_mien() -> dict:
    """Chủ đã thử xong, mở bước hướng dẫn trỏ tên miền. Chưa bật lại kênh."""
    d = doc_che_do_thu()
    if not d:
        raise ValueError("Máy này không ở chế độ thử.")
    d["giai_doan"] = "ten-mien"
    d["luc_thu_xong"] = time.time()
    _luu_che_do_thu(d)
    return d


def chinh_thuc(xac_nhan: bool = False) -> dict:
    """Kết thúc cách ly: bật lại những gì đã tạm dừng (kênh nhận tin, lịch, bảng giao việc đám mây, Zalo, sao lưu GitHub) rồi khởi động lại.
    KHÔNG bật đường hầm tên miền (chủ tự bật ở Cài đặt, Truy cập từ xa sau khi tắt ở máy cũ). Phải có xác nhận: nếu máy cũ còn chạy thì hai máy sẽ cùng
    nhận tin, cùng chạy lịch, cùng đăng nhập Zalo."""
    d = doc_che_do_thu()
    if not d:
        raise ValueError("Máy này không ở chế độ thử.")
    if not xac_nhan:
        raise ValueError("Cần xác nhận đã DỪNG máy cũ (hoặc đã tắt kênh nhận tin, việc tự chạy và Zalo ở máy cũ) trước khi chuyển chính thức.")
    st = _doc_cai_dat()
    bat = []
    for k in d.get("kenh_tam_tat") or []:
        if k == "remote_tunnel":
            continue       # đường hầm KHÔNG tự bật lại: chủ bật ở Cài đặt, Truy cập từ xa sau khi đã tắt ở máy cũ (hai máy cùng một token là trùng tên miền)
        v = st.get(k)
        if isinstance(v, dict):
            v["enabled"] = True
            bat.append(k)
    if d.get("lich_lai") is not False and d.get("lich_truoc") is False:
        st["schedules_off_here"] = False
        bat.append("lich")
    if bat:
        _ghi_cai_dat(st)
    if d.get("dq_tam_tat") and _bat_lai_dq():
        bat.append("bang_giao_viec")
    mcp_bat = _doi_trang_thai_mcp(d.get("mcp_tam_tat") or [], True)
    if mcp_bat:
        bat.append("zalo_mcp")
    d.update({"giai_doan": "xong", "luc_chinh_thuc": time.time(), "kenh_da_bat": bat, "cach_ly": False})
    _luu_che_do_thu(d)
    try:
        import tisa_khoi_dong_lai
        tisa_khoi_dong_lai.hen_khoi_dong_lai("chuyển máy: bật lại các kênh, chính thức")
    except Exception as e:  # noqa: BLE001
        d["can_khoi_dong_lai"] = str(e)[:100]
    return d


def dia_chi_local() -> str:
    import socket
    try:
        so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        so.connect(("10.255.255.255", 1))
        ip = so.getsockname()[0]
        so.close()
        return ip
    except OSError:
        return ""


def kiem_tra_may_moi() -> list:
    """Soát nhanh máy mới sau khi áp dụng: [{ten, ok (True/False/None = chỉ báo), chi_tiet}]."""
    ra = []

    def them(ten, ok, ct):
        ra.append({"ten": ten, "ok": ok, "chi_tiet": ct})
    da = {}
    try:
        da = json.loads((VIEC / "da-ap-dung.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    ban_cu, ban_nay = str(da.get("ban") or ""), _ban()
    if ban_cu and ban_nay:
        vc, vn = _ver(ban_cu), _ver(ban_nay)
        ok = bool(vc and vn and vn >= vc)
        them("Phiên bản TISA BOT", ok, f"Máy cũ bản {ban_cu}, máy này bản {ban_nay}." + ("" if ok else " Máy này thấp hơn: hãy cập nhật TISA BOT lên bản mới nhất."))
    else:
        them("Phiên bản TISA BOT", None, f"Máy này đang chạy bản {ban_nay or 'không rõ'}.")
    try:
        nao = [p for p in BRAINS_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")] if BRAINS_DIR.is_dir() else []
        so_md = sum(1 for p in nao for _ in p.rglob("*.md")) if nao else 0
        them("Bộ não", bool(nao and so_md), f"{len(nao)} bộ não, {so_md} trang." if nao else "Chưa thấy bộ não nào.")
    except OSError as e:
        them("Bộ não", False, str(e)[:100])
    st = _doc_cai_dat()
    co_khoa = (STATE_DIR / ".secret_key").exists()
    co_ma_hoa = "enc:" in json.dumps(st, ensure_ascii=False)
    if not st:
        them("Cài đặt và khoá mã hoá", False, "Không đọc được cài đặt của máy cũ.")
    elif co_ma_hoa and not co_khoa:
        them("Cài đặt và khoá mã hoá", False, "Có khoá API đã mã hoá nhưng thiếu khoá giải mã: khoá API sẽ không dùng được. Đóng gói lại từ máy cũ.")
    else:
        them("Cài đặt và khoá mã hoá", True, "Đã có cài đặt và khoá mã hoá của máy cũ." if co_khoa else "Đã có cài đặt của máy cũ (máy cũ chưa lưu khoá API nào nên chưa có khoá mã hoá).")
    try:
        mcp = json.loads((STATE_DIR / "mcp_servers.json").read_text(encoding="utf-8"))
        n = len(mcp.get("servers", mcp)) if isinstance(mcp, dict) else len(mcp)
        them("Kết nối MCP", n > 0, f"{n} kết nối MCP đã chuyển sang." if n else "Chưa có kết nối MCP nào.")
    except (OSError, ValueError):
        them("Kết nối MCP", None, "Máy cũ không có kết nối MCP, hoặc chưa đọc được tệp.")
    if DQ_HOME.is_dir():
        ct = "Có dữ liệu Đội Quân AI."
        ok = True
        try:
            import urllib.request
            e = {}
            for line in DQ_ENV.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    e[k.strip()] = v.strip()
            if e.get("BOARD_URL") and e.get("BOARD_TOKEN"):
                rq = urllib.request.Request(e["BOARD_URL"].rstrip("/") + "/api/db/settings/kit", headers={"Authorization": "Bearer " + e["BOARD_TOKEN"]})
                with urllib.request.urlopen(rq, timeout=6) as r:
                    ct = "Bảng giao việc Đội Quân AI trả lời bình thường." if r.status == 200 else f"Bảng giao việc báo mã {r.status}."
                    ok = r.status == 200
        except Exception:  # noqa: BLE001
            ok, ct = None, "Có dữ liệu Đội Quân AI, nhưng Bảng giao việc chưa trả lời (có thể đang khởi động, thử lại sau ít phút)."
        them("Đội Quân AI", ok, ct)
    else:
        them("Đội Quân AI", None, "Máy cũ không dùng Đội Quân AI.")
    d = doc_che_do_thu() or {}
    kenh = [k for k in (d.get("kenh_tam_tat") or []) if k != "remote_tunnel"]
    them("Kênh nhận tin (Telegram, Zalo...)", True, ("Đang tạm tắt trên máy này để không trả lời trùng máy cũ: " + ", ".join(kenh) + ".") if kenh else "Không có kênh nhắn tin nào đang bật.")
    rt = st.get("remote_tunnel") if isinstance(st.get("remote_tunnel"), dict) else {}
    if rt.get("enabled") and str(rt.get("mode") or "token") == "token":
        them("Đường hầm Cloudflare (tên miền)", False, "Máy này đang NỐI VÀO đường hầm Cloudflare theo token, có thể là đường hầm của máy cũ: hai máy cùng trả lời một tên miền, anh sẽ lúc thấy máy cũ lúc thấy máy này. "
             "Vào Hệ thống, Cài đặt, Truy cập từ xa và tắt đường hầm trên máy này (hoặc tắt ở máy cũ nếu muốn chuyển tên miền sang máy này).")
    elif "remote_tunnel" in (d.get("kenh_tam_tat") or []):
        them("Đường hầm Cloudflare (tên miền)", True, "Đã TẮT trên máy này, tên miền vẫn trỏ về máy cũ. Chuyển tên miền sang máy này ở bước 2.")
    if dang_cach_ly():
        tam = []
        if d.get("lich_truoc") is False or st.get("schedules_off_here"):
            tam.append("việc định kỳ, nhắc hẹn, loop")
        tam += ["việc Kanban tự chạy", "Auto của cộng sự", "tự học nền"]
        if d.get("dq_tam_tat"):
            tam.append("nối bảng giao việc Đội Quân AI trên Cloudflare")
        if d.get("mcp_tam_tat"):
            tam.append("Zalo (tránh đá tài khoản máy cũ)")
        if "backup" in (d.get("kenh_tam_tat") or []):
            tam.append("sao lưu GitHub")
        them("CÁCH LY khỏi máy cũ", True, "Máy này đang chạy ĐỘC LẬP, đã tạm dừng: " + ", ".join(tam) + ". Dữ liệu anh làm ở máy này không chảy sang máy cũ và ngược lại. Chuyển chính thức ở bước 3 mới bật lại.")
    if d.get("mcp_tisa_sua"):
        them("MCP của TISA BOT: đã đặt lại chương trình Python cho máy này", True, ", ".join(d["mcp_tisa_sua"]) + ".")
    if d.get("mcp_tisa_thieu"):
        them("MCP của TISA BOT cần cài chương trình", False, "; ".join(d["mcp_tisa_thieu"]) + ". Cài Node.js (npx) hoặc uv (uvx) trên máy này rồi bấm kiểm tra lại.")
    if d.get("khong_ghi"):
        them("Tệp không chép được", False, f"{d['khong_ghi']} tệp không chép được sang máy này (tên có ký tự Windows không cho, hoặc đường dẫn quá dài). Ví dụ: " + "; ".join(d.get("mau_khong_ghi") or []) + ". Đổi tên ngắn hơn ở máy cũ rồi đóng gói lại nếu cần các tệp đó.")
    if d.get("khac_he_dieu_hanh"):
        them("Khác hệ điều hành với máy cũ", None, "Đường dẫn đã đổi sang kiểu của máy này. Kết nối cần chương trình riêng của máy cũ (app cài sẵn, môi trường Python riêng) phải cài lại.")
    if d.get("mcp_them"):
        them("MCP thêm từ máy cũ (Claude Code, Codex)", True, "Đã thêm: " + ", ".join(d["mcp_them"]) + ". Bản cũ của hai tệp cấu hình được giữ cạnh nó (tên có chữ truoc-chuyen-may).")
    if d.get("mcp_thieu"):
        them("MCP cần cài lại chương trình", False, "Các kết nối này chạy bằng chương trình riêng chưa có trên máy này, cần cài lại: " + "; ".join(d["mcp_thieu"]) + ".")
    if d.get("mcp_loi"):
        them("MCP của Claude Code, Codex", None, "Chưa chép được: " + str(d["mcp_loi"]))
    m = st.get("model") if isinstance(st.get("model"), dict) else {}
    oa = m.get("openai_oauth") if isinstance(m.get("openai_oauth"), dict) else {}
    them("Đăng nhập gói Claude, ChatGPT", None, "Đã có đăng nhập ChatGPT." if (oa.get("access_token") or oa.get("refresh_token")) else "Máy này chưa đăng nhập gói Claude hoặc ChatGPT. Bình thường: vào Cài đặt, Mô hình, đăng nhập 1 lần.")
    them("Chỗ trống ổ đĩa", _dia_trong(STATE_DIR) > 2 * 1024 ** 3, f"Còn trống khoảng {_dia_trong(STATE_DIR) / 1024 ** 3:.1f} GB.")
    return ra


# ---------------------------------------------------------------- việc nền + đường dẫn web
def _viec_moi(loai: str) -> dict:
    v = {"id": uuid.uuid4().hex[:12], "loai": loai, "trang_thai": "dang", "phan_tram": 0, "chu": "", "loi": "", "ket_qua": None}
    with _khoa:
        _viec.clear()          # một việc một lúc là đủ cho một máy
        _viec[v["id"]] = v
    return v


def _chay_nen(v: dict, ham):
    def bao(pt, chu):
        v["phan_tram"], v["chu"] = max(0, min(99, pt)), chu

    def chay():
        try:
            v["ket_qua"] = ham(bao)
            v["trang_thai"], v["phan_tram"] = "xong", 100
        except Exception as e:  # noqa: BLE001
            v["trang_thai"], v["loi"] = "loi", str(e) or type(e).__name__
    threading.Thread(target=chay, daemon=True, name="tisa-chuyen-may").start()


def _host_cua(req) -> str:
    try:
        h = (req.headers.get("x-forwarded-host") or req.headers.get("host") or "").split(",")[0].strip().lower()
    except Exception:  # noqa: BLE001
        return ""
    if h.startswith("["):
        return h[1:].split("]")[0]
    return h.rsplit(":", 1)[0] if h.count(":") == 1 else h


def la_dia_chi_noi_bo(host: str) -> bool:
    """localhost, 127.x, ::1, 10.x, 192.168.x, 172.16-31.x, tên *.local hoặc tên không có dấu chấm: đang mở thẳng vào MÁY NÀY, không qua tên miền công khai."""
    h = (host or "").strip().lower()
    if not h or h in ("localhost", "::1") or h.startswith("127.") or h.startswith("10.") or h.startswith("192.168.") or h.endswith((".local", ".localhost", ".lan")):
        return True
    m = re.match(r"^172\.(\d+)\.", h)
    if m and 16 <= int(m.group(1)) <= 31:
        return True
    return "." not in h


def truy_cap(req) -> dict:
    """Trang này đang được mở bằng đường nào. qua_ten_mien: đường công khai (tên miền hoặc IP công cộng), có thể là máy gốc đang giữ tên miền."""
    h = _host_cua(req)
    rt = _doc_cai_dat().get("remote_tunnel")
    return {"host": h, "qua_ten_mien": not la_dia_chi_noi_bo(h), "duong_ham_dang_bat": bool(isinstance(rt, dict) and rt.get("enabled") is True),
            "ten_may": platform.node()}


def chan_qua_ten_mien(req, d) -> str:
    """Rỗng nếu cho phép. Nhận / áp dụng / khôi phục qua đường công khai mà chưa xác nhận máy: dừng, vì có thể đang thao tác trên MÁY GỐC (V3.17)."""
    t = truy_cap(req)
    if not t["qua_ten_mien"] or (d or {}).get("xac_nhan_may") is True:
        return ""
    return (f"Anh đang mở trang này qua địa chỉ {t['host'] or '(không rõ)'}, không phải địa chỉ local. Nếu tên miền này đang trỏ về MÁY CŨ thì thao tác này sẽ chạy trên MÁY CŨ "
            f"và thay dữ liệu máy cũ. Máy đang trả lời tên là \"{t['ten_may']}\". Hãy mở TISA BOT trên chính máy mới bằng http://localhost:cổng rồi làm lại; "
            "chỉ khi chắc chắn máy này đúng là máy cần nhận thì tick ô xác nhận máy.")


def _file_goi() -> Path:
    return VIEC / f"TISA-BOT-chuyen-may-{time.strftime('%Y%m%d-%H%M')}.tisapack"


def gan(app) -> None:
    from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

    trang = ROOT / "dashboard" / "tisa-chuyen-may.html"

    @app.get("/tisa-chuyen-may/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang chuyển máy", status_code=500)

    @app.get("/tisa-chuyen-may/api/tinh-trang")
    async def _tinh_trang(req: Request):
        import asyncio
        tep = await asyncio.to_thread(danh_sach)
        uoc = await asyncio.to_thread(uoc_tinh, tep)
        tong = uoc["tong_tat_ca"]
        bo_nao = sorted({t.split("/")[1] for _, t in tep if t.startswith("bo-nao/") and t.count("/") >= 2})
        da = None
        try:
            da = json.loads((VIEC / "da-ap-dung.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        goi = sorted((p for p in VIEC.glob("*.tisapack")), key=lambda p: p.stat().st_mtime, reverse=True) if VIEC.is_dir() else []
        cho_tom = None
        try:
            if CHO.is_dir():
                cho_tom = json.loads((VIEC / "cho-ap-dung-tom-tat.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        return {"ok": True, "cho_ap_dung": cho_tom, "so_tep": len(tep), "dung_luong": tong, "bo_nao": bo_nao, "trong": _dia_trong(VIEC.parent),
                "nen_tang": uoc["nen_tang"], "kho_nang": uoc["kho_nang"], "tong_kho_nang": uoc["tong_kho_nang"], "giu_trong": GIU_TRONG,
                "co_mcp": (STATE_DIR / "mcp_servers.json").exists(), "co_doi_quan": DQ_HOME.is_dir(),
                "ban": _ban(), "he_dieu_hanh": sys.platform, "da_ap_dung": da,
                "co_the_khoi_phuc": bool(du_phong_khoi_phuc_duoc()), "ten_may": platform.node(), "ten_ban": _ten_ban(),
                "che_do_thu": doc_che_do_thu(), "dia_chi_local": dia_chi_local(), "truy_cap": truy_cap(req),
                "goi_san": [{"ten": p.name, "kich_thuoc": p.stat().st_size} for p in goi[:3]],
                "viec": next(iter(_viec.values()), None)}

    @app.post("/tisa-chuyen-may/api/dong-goi")
    async def _dong_goi(req: Request):
        d = await req.json()
        mk = str(d.get("mat_khau") or "")
        if len(mk) < 8:
            return JSONResponse({"ok": False, "error": "Mật khẩu cần ít nhất 8 ký tự."}, status_code=400)
        for p in VIEC.glob("*.tisapack") if VIEC.is_dir() else []:
            try:
                p.unlink()        # chỉ giữ gói mới nhất, gói cũ chứa khoá cũ không nên nằm lại
            except OSError:
                pass
        ra = _file_goi()
        chon = [str(x) for x in (d.get("kho_nang") or []) if str(x) in KHO_NANG] if isinstance(d.get("kho_nang"), list) else []
        v = _viec_moi("dong-goi")
        _chay_nen(v, lambda bao: dong_goi(mk, ra, bao, chon))
        return {"ok": True, "viec": v["id"]}

    @app.get("/tisa-chuyen-may/api/viec")
    async def _xem_viec():
        return {"ok": True, "viec": next(iter(_viec.values()), None)}

    @app.get("/tisa-chuyen-may/api/tai/{ten}")
    async def _tai(ten: str):
        p = VIEC / ten
        if not re.fullmatch(r"TISA-BOT-chuyen-may-[0-9-]+\.tisapack", ten) or not p.is_file():
            return JSONResponse({"ok": False, "error": "Không có file này."}, status_code=404)
        return FileResponse(str(p), media_type="application/octet-stream", filename=ten)

    @app.post("/tisa-chuyen-may/api/xoa-goi")
    async def _xoa_goi():
        for p in VIEC.glob("*.tisapack") if VIEC.is_dir() else []:
            try:
                p.unlink()
            except OSError:
                pass
        return {"ok": True}

    # Tải lên từng khúc (Cloudflare Tunnel cắt yêu cầu quá ~100MB).
    @app.post("/tisa-chuyen-may/api/nhan/bat-dau")
    async def _nhan_bat_dau(req: Request):
        d = await req.json()
        loi = chan_qua_ten_mien(req, d)
        if loi:
            return JSONResponse({"ok": False, "error": loi, "can_xac_nhan_may": True}, status_code=409)
        size = int(d.get("kich_thuoc") or 0)
        if size <= 0:
            return JSONResponse({"ok": False, "error": "File rỗng."}, status_code=400)
        if _dia_trong(STATE_DIR) < size * 4 + GIU_TRONG:
            return JSONResponse({"ok": False, "error": "Máy không đủ chỗ trống để nhận file này."}, status_code=400)
        VIEC.mkdir(parents=True, exist_ok=True)
        for p in VIEC.glob("nhan-*.phan"):
            try:
                p.unlink()
            except OSError:
                pass
        ma = uuid.uuid4().hex[:16]
        (VIEC / f"nhan-{ma}.phan").write_bytes(b"")
        return {"ok": True, "ma": ma, "khuc": 8 * 1024 * 1024}

    @app.post("/tisa-chuyen-may/api/nhan/khuc/{ma}")
    async def _nhan_khuc(ma: str, req: Request):
        if not re.fullmatch(r"[0-9a-f]{16}", ma):
            return JSONResponse({"ok": False, "error": "Mã không hợp lệ."}, status_code=400)
        p = VIEC / f"nhan-{ma}.phan"
        if not p.is_file():
            return JSONResponse({"ok": False, "error": "Phiên tải lên đã hết, hãy chọn lại file."}, status_code=404)
        vi_tri = int(req.query_params.get("tu") or 0)
        da = p.stat().st_size
        if vi_tri != da:
            return {"ok": False, "da_co": da}
        body = await req.body()
        with open(p, "ab") as f:
            f.write(body)
        return {"ok": True, "da_co": da + len(body)}

    @app.post("/tisa-chuyen-may/api/nhan/xong/{ma}")
    async def _nhan_xong(ma: str, req: Request):
        if not re.fullmatch(r"[0-9a-f]{16}", ma):
            return JSONResponse({"ok": False, "error": "Mã không hợp lệ."}, status_code=400)
        d = await req.json()
        mk = str(d.get("mat_khau") or "")
        p = VIEC / f"nhan-{ma}.phan"
        if not p.is_file():
            return JSONResponse({"ok": False, "error": "Chưa có file tải lên."}, status_code=404)
        v = _viec_moi("nhan")

        def lam(bao):
            kq = nhan(p, mk, bao)      # sai mật khẩu thì giữ file đã tải lên: chỉ cần nhập lại mật khẩu
            try:
                p.unlink()
            except OSError:
                pass
            return kq
        _chay_nen(v, lam)
        return {"ok": True, "viec": v["id"]}

    @app.post("/tisa-chuyen-may/api/ap-dung")
    async def _ap_dung(req: Request):
        try:
            d = await req.json()
        except Exception:  # noqa: BLE001
            d = {}
        loi = chan_qua_ten_mien(req, d)
        if loi:
            return JSONResponse({"ok": False, "error": loi, "can_xac_nhan_may": True}, status_code=409)
        try:
            hen_ap_dung(dong_y_quay_lai=bool((d or {}).get("dong_y_quay_lai")))
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        return {"ok": True}

    @app.post("/tisa-chuyen-may/api/kiem-tra-may-moi")
    async def _kiem_tra():
        import asyncio
        return {"ok": True, "ket_qua": await asyncio.to_thread(kiem_tra_may_moi)}

    @app.post("/tisa-chuyen-may/api/sang-ten-mien")
    async def _sang_tm():
        try:
            return {"ok": True, "che_do_thu": sang_ten_mien()}
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)

    @app.get("/tisa-chuyen-may/api/che-do-thu")
    async def _che_do_thu():
        return {"ok": True, "che_do_thu": doc_che_do_thu()}

    @app.post("/tisa-chuyen-may/api/lui-ve-buoc-thu")
    async def _lui():
        d = doc_che_do_thu()
        if not d or d.get("giai_doan") == "xong":
            return JSONResponse({"ok": False, "error": "Máy này không ở chế độ thử."}, status_code=400)
        d["giai_doan"] = "thu"
        _luu_che_do_thu(d)
        return {"ok": True, "che_do_thu": d}

    @app.post("/tisa-chuyen-may/api/chinh-thuc")
    async def _chinh_thuc(req: Request):
        try:
            try:
                b = await req.json()
            except Exception:  # noqa: BLE001
                b = {}
            return {"ok": True, "che_do_thu": chinh_thuc(bool((b or {}).get("xac_nhan")))}
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)

    @app.post("/tisa-chuyen-may/api/khoi-phuc")
    async def _khoi_phuc_api(req: Request):
        try:
            d = await req.json()
        except Exception:  # noqa: BLE001
            d = {}
        loi = chan_qua_ten_mien(req, d)
        if loi:
            return JSONResponse({"ok": False, "error": loi, "can_xac_nhan_may": True}, status_code=409)
        try:
            hen_khoi_phuc()
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        return {"ok": True}

    @app.post("/tisa-chuyen-may/api/huy-nhan")
    async def _huy_nhan():
        shutil.rmtree(CHO, ignore_errors=True)
        for p in (DANH_DAU, VIEC / "cho-ap-dung-tom-tat.json"):
            try:
                p.unlink()
            except OSError:
                pass
        return {"ok": True}


# ---------------------------------------------------------------- dòng lệnh (VPS)
def _cli(argv) -> int:
    import getpass
    if len(argv) < 2 or argv[0] not in ("dong-goi", "nhan"):
        print(__doc__.split("Dùng được từ dòng lệnh")[1] if "Dùng được từ dòng lệnh" in __doc__ else "")
        return 2
    mk = os.getenv("TISA_CHUYEN_MAY_MAT_KHAU") or getpass.getpass("Mật khẩu của gói: ")
    bao = lambda pt, chu: print(f"\r{pt:3d}% {chu:60.60s}", end="", flush=True)  # noqa: E731
    try:
        if argv[0] == "dong-goi":
            chon = []
            for a in argv[2:]:
                if a == "--tat-ca-kho":
                    chon = list(KHO_NANG)
                elif a.startswith("--kho="):
                    chon = [x for x in a[6:].split(",") if x in KHO_NANG]
            kq = dong_goi(mk, Path(argv[1]).resolve(), bao, chon)
            print(f"\nXong: {kq['file']} ({kq['kich_thuoc'] / 1024 ** 2:.0f} MB, {kq['so_bo_nao']} bộ não, {kq['so_tep']} tệp)")
            if kq.get("kho_nang_bo_qua"):
                print("Chưa mang (kho nặng): " + ", ".join(f"{NHAN_KHO[k][0]} {v['dung_luong'] / 1024 ** 3:.1f} GB" for k, v in kq["kho_nang_bo_qua"].items()) + ". Chép riêng nếu cần (--kho=" + ",".join(KHO_NANG) + " để mang theo).")
        else:
            kq = nhan(Path(argv[1]).resolve(), mk, bao)
            print(f"\nĐã nhận dữ liệu từ máy cũ ({kq['ke_khai'].get('luc')}), bộ não: {', '.join(kq['bo_nao'])}")
            print(f"Phiên bản: máy cũ {kq.get('ban_may_cu') or '?'}, máy này {kq.get('ban_may_nay') or '?'}.")
            if kq.get("bo_qua_ma_nguon"):
                print(f"(Gói của bản cũ có kèm chương trình máy cũ: đã bỏ qua {kq['bo_qua_ma_nguon']} tệp, giữ nguyên chương trình của máy này.)")
            hen_ap_dung(khoi_dong_lai=False)
            print("Bước cuối: khởi động lại TISA BOT (VPS: sudo systemctl restart <tên dịch vụ TISA BOT>, hoặc tắt rồi mở lại),")
            print("dữ liệu máy cũ sẽ được áp dụng ngay đầu lần chạy mới.")
            print("Máy này sẽ CHẠY THỬ: các kênh nhận tin tạm tắt, máy cũ vẫn chạy. Mở trang Chuyển máy chủ để kiểm tra và làm bước trỏ tên miền.")
    except ValueError as e:
        print(f"\nLỖI: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
