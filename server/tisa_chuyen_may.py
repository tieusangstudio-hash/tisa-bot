"""tisa_chuyen_may.py - Chuyển TISA BOT sang máy khác hoặc VPS bằng MỘT file (V2.76, chủ chốt 10/11/2026).

Chủ dặn: "chuyển qua phải đi kèm toàn bộ hệ thống MCP với API, bộ não và các thiết lập để không mất thời gian setup lại".

Gói gồm mọi thứ TISA BOT tự sinh ra trên máy cũ, tức mọi tệp KHÔNG thuộc mã nguồn (git không theo dõi):
- mọi bộ não (BRAINS_DIR), kể cả skill, cộng sự, quy trình, trí nhớ, tệp đính kèm;
- settings.json kèm `.secret_key` (khoá API, token kênh, MCP đều mã hoá bằng khoá này, thiếu nó là mất hết);
- mcp_servers.json, .oauth_mcp.json, .hub_token, kết nối kênh, chatbot, lịch sử chat, việc định kỳ, webhook, mọi CSDL;
- plugin, gói Store, ảnh đại diện, connector-home (phiên đăng nhập Zalo...), tệp .env của TISA BOT;
- dữ liệu Đội Quân AI (DOI_QUAN_HOME) và tệp .env của nó (DOI_QUAN_ENV).
Không mang: mã nguồn (máy mới cài bản mới), .venv, node_modules, bộ nhớ đệm, nhật ký, pid, phiên đăng nhập web cũ, đường dẫn
chương trình riêng của máy cũ, và đăng nhập gói Claude / ChatGPT của máy cũ (đăng nhập lại 1 lần trên máy mới).

File chứa mọi khoá nên luôn KHOÁ bằng mật khẩu chủ đặt: scrypt -> AES-256-GCM từng khúc 4MB, khúc cuối có cờ riêng nên
cắt bớt đuôi file là bị phát hiện. Sai mật khẩu hay file hỏng thì dừng trước khi đụng vào máy mới.

Áp dụng trên máy mới đi qua lần khởi động lại: dữ liệu đã giải nén nằm chờ trong thư mục `chuyen-may/cho-ap-dung`, máy chủ
khởi động lại, và NGAY ĐẦU lần chạy mới (trước khi mở bất kỳ CSDL nào, xem `ap_dung_khi_khoi_dong`) mới đổi dữ liệu:
bản đang có của máy mới chuyển sang `_truoc-chuyen-may-<giờ>` (không xoá), rồi đặt dữ liệu cũ vào chỗ và sửa đường dẫn
máy cũ thành đường dẫn máy mới trong tệp cấu hình và CSDL.

Dùng được từ dòng lệnh cho VPS (file lớn, chép bằng scp):
    python server/tisa_chuyen_may.py dong-goi <file-ra>          (hỏi mật khẩu)
    python server/tisa_chuyen_may.py nhan <file.tisapack>         (hỏi mật khẩu, rồi khởi động lại TISA BOT)
"""
from __future__ import annotations

import io
import json
import os
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


def _duyet(goc: Path, tien_to: str, theo_doi, bo_cap_dau_gach=False, la_nao=False):
    """(đường dẫn thật, tên trong gói) của mọi tệp nên mang theo dưới `goc`."""
    if not goc.is_dir():
        return
    bo_tm = BO_THU_MUC_NAO if la_nao else BO_THU_MUC
    for dp, dn, fn in os.walk(goc):
        rel_dp = Path(dp).relative_to(goc)
        if bo_cap_dau_gach and rel_dp == Path("."):
            dn[:] = [d for d in dn if not d.startswith("_")]
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
            ten = "trang-thai/" + Path(rp).relative_to(tt).as_posix()
        out.append((p, ten)); da.add(rp)
    if not _trong(tt, str(ROOT.resolve())):
        for p, ten in _duyet(STATE_DIR, "trang-thai", None):
            if str(p.resolve()) not in da:
                out.append((p, ten))
    for p, ten in _duyet(BRAINS_DIR, "bo-nao", None, la_nao=True):
        out.append((p, ten))
    for p, ten in _duyet(DQ_HOME, "doi-quan-home", None):
        out.append((p, ten))
    if DQ_ENV.is_file():
        out.append((DQ_ENV, "doi-quan-env/.env"))
    return out


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
def _ban() -> str:
    try:
        return (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def dong_goi(mat_khau: str, ra: Path, bao=None) -> dict:
    """Đóng gói và mã hoá ra `ra`. `bao(phan_tram, chu)` báo tiến độ. Trả tóm tắt."""
    if len(mat_khau or "") < 8:
        raise ValueError("Mật khẩu cần ít nhất 8 ký tự.")
    VIEC.mkdir(parents=True, exist_ok=True)
    tep = danh_sach()
    tong = sum((p.stat().st_size for p, _ in tep if p.exists()), 0)
    if _dia_trong(ra.parent) < tong + GIU_TRONG:
        raise ValueError(f"Máy không đủ chỗ trống để đóng gói (cần khoảng {tong / 1024 ** 3 + 2:.1f} GB).")
    ke_khai = {"loai": "tisa-chuyen-may", "phien_ban_goi": PHIEN_BAN, "ban_tisa": _ban(), "luc": time.strftime("%Y-%m-%d %H:%M"),
               "may": {"goc": str(ROOT), "nha": str(Path.home()), "bo_nao": str(BRAINS_DIR), "trang_thai": str(STATE_DIR),
                       "doi_quan_home": str(DQ_HOME), "he_dieu_hanh": sys.platform},
               "so_tep": len(tep), "dung_luong": tong}
    da, n_bo_nao = 0, set()
    tam = ra.with_suffix(ra.suffix + ".dang-tao")
    with open(tam, "wb") as fout:
        w = _GhiMaHoa(fout, mat_khau)
        with zipfile.ZipFile(w, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as z:
            z.writestr("tisa-chuyen-may.json", json.dumps(ke_khai, ensure_ascii=False, indent=1))
            for i, (p, ten) in enumerate(tep):
                try:
                    if _la_sqlite(p):
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
    return {"so_tep": len(tep), "dung_luong": tong, "so_bo_nao": len(n_bo_nao), "file": str(ra), "kich_thuoc": ra.stat().st_size}


# ---------------------------------------------------------------- nhận
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
            for i, m in enumerate(ds):
                if not _an_toan(m.filename) or m.filename.split("/")[0] not in ("goc", "bo-nao", "trang-thai", "doi-quan-home", "doi-quan-env"):
                    continue
                dich = CHO / m.filename
                dich.parent.mkdir(parents=True, exist_ok=True)
                with z.open(m) as a, open(dich, "wb") as b:
                    shutil.copyfileobj(a, b, 1024 * 1024)
                if bao and i % 100 == 0:
                    bao(40 + int(i * 55 / max(len(ds), 1)), f"Đã giải nén {i + 1}/{len(ds)} tệp")
        bo_nao = sorted(p.name for p in (CHO / "bo-nao").iterdir() if p.is_dir()) if (CHO / "bo-nao").is_dir() else []
        tom = {"ke_khai": ke_khai, "bo_nao": bo_nao, "so_tep": ke_khai.get("so_tep"), "dung_luong": ke_khai.get("dung_luong")}
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


def hen_ap_dung(khoi_dong_lai: bool = True) -> None:
    """Đánh dấu chờ áp dụng rồi khởi động lại: lần chạy mới đổi dữ liệu trước khi mở CSDL.
    Từ dòng lệnh (khoi_dong_lai=False) chỉ đánh dấu: tiến trình dòng lệnh không phải máy chủ, người dùng tự khởi động lại."""
    if not CHO.is_dir():
        raise ValueError("Chưa có dữ liệu nhận về để áp dụng.")
    tom = json.loads((VIEC / "cho-ap-dung-tom-tat.json").read_text(encoding="utf-8"))
    DANH_DAU.write_text(json.dumps({"luc": time.time(), "ke_khai": tom.get("ke_khai")}, ensure_ascii=False), encoding="utf-8")
    if not khoi_dong_lai:
        return
    try:
        import tisa_khoi_dong_lai
        tisa_khoi_dong_lai.hen_khoi_dong_lai("chuyển máy: áp dụng dữ liệu máy cũ")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Đã nhận dữ liệu nhưng chưa khởi động lại được ({e}). Hãy tắt rồi mở lại TISA BOT.")


# ---------------------------------------------------------------- áp dụng (đầu lần khởi động mới)
def _cap_doi(ke_khai: dict) -> list:
    """Các cặp (đường dẫn máy cũ, đường dẫn máy mới), dài trước ngắn sau để không thay nhầm phần đầu."""
    cu = (ke_khai or {}).get("may") or {}
    cap = [(cu.get("bo_nao"), str(BRAINS_DIR)), (cu.get("doi_quan_home"), str(DQ_HOME)),
           (cu.get("trang_thai"), str(STATE_DIR)), (cu.get("goc"), str(ROOT)), (cu.get("nha"), str(Path.home()))]
    cap = [(a, b) for a, b in cap if a and b and a != b]
    them = []
    for a, b in cap:   # dạng đã thoát trong JSON của đường dẫn Windows
        if "\\" in a or "\\" in b:
            them.append((a.replace("\\", "\\\\"), b.replace("\\", "\\\\")))
    return sorted(cap + them, key=lambda x: -len(x[0]))


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
        m = s
        for a, b in cap:
            m = m.replace(a, b)
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
        bang = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
        for b in bang:
            try:
                cot = [r[1] for r in con.execute(f'pragma table_info("{b}")') if (r[2] or "").upper() in ("TEXT", "", "VARCHAR", "JSON")]
            except sqlite3.Error:
                continue
            for c in cot:
                for a, moi in cap:
                    try:
                        cur = con.execute(f'update "{b}" set "{c}" = replace("{c}", ?, ?) where instr("{c}", ?) > 0', (a, moi, a))
                        n += cur.rowcount or 0
                    except sqlite3.Error:
                        break
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
            a, b = Path(dp) / f, dich / rel / f
            b.parent.mkdir(parents=True, exist_ok=True)
            if b.exists() or b.is_symlink():
                c = du_phong / rel / f
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


def ap_dung_khi_khoi_dong() -> None:
    """Gọi ở dòng đầu main.py. Có dấu chờ áp dụng thì đổi dữ liệu, xong xoá dấu. Lỗi thì ghi nhật ký, giữ máy chạy."""
    if not DANH_DAU.is_file() or not CHO.is_dir():
        return
    nk = VIEC / "chuyen-may.log"
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
        shutil.rmtree(CHO, ignore_errors=True)
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
    async def _tinh_trang():
        import asyncio
        tep = await asyncio.to_thread(danh_sach)
        tong = sum((p.stat().st_size for p, _ in tep if p.exists()), 0)
        bo_nao = sorted({t.split("/")[1] for _, t in tep if t.startswith("bo-nao/") and t.count("/") >= 2})
        da = None
        try:
            da = json.loads((VIEC / "da-ap-dung.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        goi = sorted((p for p in VIEC.glob("*.tisapack")), key=lambda p: p.stat().st_mtime, reverse=True) if VIEC.is_dir() else []
        return {"ok": True, "so_tep": len(tep), "dung_luong": tong, "bo_nao": bo_nao, "trong": _dia_trong(VIEC.parent),
                "co_mcp": (STATE_DIR / "mcp_servers.json").exists(), "co_doi_quan": DQ_HOME.is_dir(),
                "ban": _ban(), "he_dieu_hanh": sys.platform, "da_ap_dung": da,
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
        v = _viec_moi("dong-goi")
        _chay_nen(v, lambda bao: dong_goi(mk, ra, bao))
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
    async def _ap_dung():
        try:
            hen_ap_dung()
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
            kq = dong_goi(mk, Path(argv[1]).resolve(), bao)
            print(f"\nXong: {kq['file']} ({kq['kich_thuoc'] / 1024 ** 2:.0f} MB, {kq['so_bo_nao']} bộ não, {kq['so_tep']} tệp)")
        else:
            kq = nhan(Path(argv[1]).resolve(), mk, bao)
            print(f"\nĐã nhận dữ liệu từ máy cũ ({kq['ke_khai'].get('luc')}), bộ não: {', '.join(kq['bo_nao'])}")
            hen_ap_dung(khoi_dong_lai=False)
            print("Bước cuối: khởi động lại TISA BOT (VPS: sudo systemctl restart <tên dịch vụ TISA BOT>, hoặc tắt rồi mở lại),")
            print("dữ liệu máy cũ sẽ được áp dụng ngay đầu lần chạy mới.")
    except ValueError as e:
        print(f"\nLỖI: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
