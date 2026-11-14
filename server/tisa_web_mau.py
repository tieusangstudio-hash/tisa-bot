"""Web mẫu có sẵn trong Quản lý web: Web CRM và Lead Page + Sale Page (gói tisa.web-crm-lead của Học Viện TISA).

Chủ yêu cầu 09/11/2026: hai web này có sẵn trong TISA BOT, nhân bản được thêm 3, 4, 5 trang, và nối sẵn với TISA BOT để
chatbot ghi khách vào CRM, hoặc lấy số điện thoại trong CRM rồi kết bạn Zalo, nhắn chăm sóc.

- Gói `tisa.web-crm-lead` (suite/goi/tisa-web-crm-lead.zip) được cài MỘT LẦN qua trình cài gói của TISA BOT lúc khởi động
  (kiểm tra zip, ghi sổ, cài skill vào bộ não). Gói mang công cụ chatbot và Zalo: crm_push_lead, crm_zalo_sync, crm_connect...
  Người dùng gỡ gói thì không cài lại.
- Một "bộ web" = thư mục có crm/ (Node.js) và lead/ (trang tĩnh). Bộ đầu tiên ở ~/Documents/TISA-CRM, cổng 3000 và 4173.
  Chạy bằng scripts/demo-local.mjs của chính bộ mã (chỉ nghe 127.0.0.1).
- Trang Lead/Sale còn được TISA BOT phát ở /tisa-web/trang/<slug>/ (công khai, đi được qua Truy cập từ xa). Form trên đó gửi
  về /tisa-web/crm-form/<bộ> (công khai, chỉ nhận ghi, giới hạn tần suất), TISA BOT chuyển vào CRM trên máy. CRM không lộ ra ngoài.
- Nhân bản trang: chép thư mục lead/ thành lead-2, lead-3..., cùng đổ khách vào CRM của bộ. Nhân bản bộ: chép cả bộ sang thư mục
  mới, cổng mới, dữ liệu trống (không chép node_modules, .local).
Không bao giờ xoá thư mục của người dùng: "gỡ" chỉ bỏ khỏi danh sách.
"""
import asyncio
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import unicodedata
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response

import config as cfgmod

ROOT = Path(__file__).resolve().parent.parent
KHO = Path(cfgmod.STATE_DIR) / "tisa_web"
TEP = KHO / "mau.json"
GOI_ID = "tisa.web-crm-lead"
GOI_ZIP = ROOT / "suite" / "goi" / "tisa-web-crm-lead.zip"
GOC_MAC_DINH = Path(os.getenv("TISA_WEB_MAU_GOC") or (Path.home() / "Documents" / "TISA-CRM")).expanduser()
NODE_TOI_THIEU = (22, 13)
_KHOA = threading.Lock()
_CHAY = {}          # bộ -> Popen của lần "chạy" đang khởi động
_TAN_SUAT = {}
_BO_QUA_FILE = {"_headers", ".DS_Store"}


# ---------------------------------------------------------------- tiện ích

def _bay_gio():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _khong_dau(s):
    s = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:50] or "trang"


def _doc():
    try:
        d = json.loads(TEP.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            d.setdefault("bo", [])
            d.setdefault("trang", [])
            return d
    except (OSError, ValueError):
        pass
    return {"bo": [], "trang": []}


def _ghi(d):
    KHO.mkdir(parents=True, exist_ok=True)
    tam = TEP.with_suffix(".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, TEP)


def _mac_dinh(d):
    """Bộ đầu tiên và trang Lead của nó luôn có trong danh sách (hai web mặc định)."""
    if not any(b.get("id") == "bo1" for b in d["bo"]):
        d["bo"].insert(0, {"id": "bo1", "ten": "Web CRM", "thu_muc": str(GOC_MAC_DINH), "cong_crm": 3000, "cong_lead": 4173,
                           "mac_dinh": True, "tao": _bay_gio()})
    if not any(t.get("id") == "lead-bo1" for t in d["trang"]):
        d["trang"].insert(0, {"id": "lead-bo1", "bo": "bo1", "ten": "Lead Page & Sale Page", "thu_muc_con": "lead",
                              "slug": "lead-page", "mac_dinh": True, "tao": _bay_gio()})
    return d


def _tim(ds, i):
    return next((x for x in ds if x.get("id") == i), None)


def _goc(bo):
    return Path(str(bo.get("thu_muc") or GOC_MAC_DINH)).expanduser()


def _cong_mo(cong, host="127.0.0.1"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.6)
    try:
        return s.connect_ex((host, int(cong))) == 0
    except OSError:
        return False
    finally:
        s.close()


def _cong_trong(da_dung):
    """Cặp cổng (CRM, Lead) chưa ai dùng, sau 3000/4173."""
    for i in range(1, 60):
        c, l = 3000 + i, 4173 + i
        if c in da_dung or l in da_dung:
            continue
        if not _cong_mo(c) and not _cong_mo(l):
            return c, l
    raise ValueError("Không còn cổng trống để chạy thêm bộ web")


_NODE = {"luc": 0.0, "kq": None}


def _node():
    """(đường dẫn node, phiên bản, đủ dùng) - nhớ 60 giây."""
    if _NODE["kq"] and time.time() - _NODE["luc"] < 60:
        return _NODE["kq"]
    ung = [shutil.which("node")]
    if os.name == "nt":
        ung += [os.path.expandvars(r"%ProgramFiles%\nodejs\node.exe"), os.path.expandvars(r"%LOCALAPPDATA%\Programs\nodejs\node.exe")]
    else:
        ung += ["/opt/homebrew/bin/node", "/usr/local/bin/node", "/usr/bin/node"]
        nvm = Path.home() / ".nvm" / "versions" / "node"
        if nvm.is_dir():
            ung += [str(p / "bin" / "node") for p in sorted(nvm.iterdir(), reverse=True)]
    kq = ("", "", False)
    for p in ung:
        if not p or not Path(p).is_file():
            continue
        try:
            v = subprocess.run([p, "-v"], capture_output=True, text=True, timeout=8,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            continue
        m = re.match(r"v(\d+)\.(\d+)", v)
        du = bool(m) and (int(m.group(1)), int(m.group(2))) >= NODE_TOI_THIEU
        kq = (p, v, du)
        if du:
            break
    _NODE.update(luc=time.time(), kq=kq)
    return kq


def _moi_truong(node):
    env = dict(os.environ)
    thu_muc = str(Path(node).parent)
    env["PATH"] = thu_muc + os.pathsep + env.get("PATH", "")
    return env


def _goi_da_cai():
    try:
        import packs
        for p in packs.installed():
            if p.get("id") == GOI_ID:
                return p
    except Exception:  # noqa: BLE001
        pass
    return None


def _thu_muc_goi():
    try:
        import packs
        d = packs.PACKS_DIR / GOI_ID
        return d if d.is_dir() else None
    except Exception:  # noqa: BLE001
        return None


def _ban_goi_kem():
    try:
        with zipfile.ZipFile(GOI_ZIP) as z:
            m = re.search(r"^version:\s*\"?([\d.]+)", z.read("tisa-pack.yaml").decode("utf-8"), re.M)
            return m.group(1) if m else ""
    except (OSError, KeyError, zipfile.BadZipFile):
        return ""


def _ver(v):
    return tuple(int(x) for x in re.findall(r"\d+", str(v or ""))[:3]) or (0,)


def cai_goi(bat_buoc=False):
    """Cài gói kèm theo qua trình cài của TISA BOT. Trả dict kết quả. Chỉ tự cài một lần, hoặc nâng bản khi gói đang cài cũ hơn."""
    if not GOI_ZIP.is_file():
        return {"ok": False, "error": "Thiếu tệp gói web mẫu trong bộ cài"}
    co = _goi_da_cai()
    moi = _ban_goi_kem()
    da = KHO / "goi-mau.json"
    try:
        ghi_nho = json.loads(da.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        ghi_nho = {}
    if co and _ver(co.get("version")) >= _ver(moi):
        return {"ok": True, "da_co": True, "version": co.get("version")}
    if not co and ghi_nho.get("da_cai") and not bat_buoc:
        return {"ok": False, "error": "Gói đã được gỡ. Bấm Cài lại nếu muốn dùng."}
    import pack_install
    du_lieu = GOI_ZIP.read_bytes()
    soi = pack_install.soi(du_lieu, GOI_ZIP.name)
    if not soi.get("ok"):
        return {"ok": False, "error": soi.get("error") or "Gói không hợp lệ"}
    brain = ""
    try:
        m = sys.modules.get("main")
        brain = str(m._brain_root("brain")) if m and hasattr(m, "_brain_root") else ""
    except Exception:  # noqa: BLE001
        brain = ""
    kq = pack_install.cai(soi["staging_id"], soi["sha256"], enable=True,
                          nguon={"kind": "tisa-bot", "url": "suite/goi/" + GOI_ZIP.name}, brain_root=brain)
    if kq.get("ok"):
        KHO.mkdir(parents=True, exist_ok=True)
        da.write_text(json.dumps({"da_cai": moi, "luc": _bay_gio()}), encoding="utf-8")
        try:
            import mcp_hub
            mcp_hub.invalidate_cache()
        except Exception:  # noqa: BLE001
            pass
    return kq if kq.get("ok") else {"ok": False, "error": kq.get("error") or "Không cài được gói"}


def _site_url(bo):
    try:
        b = json.loads((_goc(bo) / "crm" / "template" / "business.json").read_text(encoding="utf-8"))
        return str(b.get("siteUrl") or "").rstrip("/")
    except (OSError, ValueError):
        return ""


def _da_noi_bot(bo):
    """CRM của bộ này có đang là CRM mà TISA BOT nối (khoá lưu ở ~/.config/tisa-crm)."""
    th = Path(os.getenv("TISA_CRM_CONFIG_DIR") or (Path.home() / ".config" / "tisa-crm"))
    url = "http://localhost:%s" % bo.get("cong_crm")
    kq = {}
    for ten, khoa in (("crm.env", "tro_ly"), ("chatbot.env", "chatbot")):
        try:
            s = (th / ten).read_text(encoding="utf-8")
        except OSError:
            kq[khoa] = False
            continue
        m = re.search(r"^\s*(?:CRM_URL|TISA_CRM_URL|URL)\s*=\s*\"?([^\"\n]+)", s, re.M)
        u = (m.group(1).strip().rstrip("/") if m else "")
        kq[khoa] = bool(u) and (u.replace("127.0.0.1", "localhost") == url or u == _site_url(bo))
    return kq


def _cua_minh(bo):
    """CRM đang nghe ở cổng có đúng là của bộ này (demo.pid còn sống), hay một ứng dụng khác chiếm cổng."""
    f = _goc(bo) / "crm" / ".local" / "demo.pid"
    try:
        pid = int(f.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return False
    try:
        if os.name == "nt":
            r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid], capture_output=True, text=True, timeout=8,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return str(pid) in r.stdout
        os.kill(pid, 0)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def _trang_thai_bo(bo):
    g = _goc(bo)
    crm = g / "crm"
    p = _CHAY.get(bo["id"])
    dang_khoi = bool(p and p.poll() is None)
    log = ""
    if p and p.poll() not in (None, 0):
        for ten in ("tisa-chay.log", "demo.log"):
            try:
                log = (crm / ".local" / ten).read_text(encoding="utf-8", errors="replace")[-900:].strip()
            except OSError:
                continue
            if log:
                break
    minh = _cua_minh(bo)
    return {"da_giai_nen": (crm / "package.json").is_file(), "da_cai_thu_vien": (crm / "node_modules").is_dir(),
            "crm_chay": minh and _cong_mo(bo["cong_crm"]), "lead_chay": minh and _cong_mo(bo["cong_lead"]),
            "dang_khoi_dong": dang_khoi, "loi": log, "noi_bot": _da_noi_bot(bo), "goc": str(g), "crm_public": str(bo.get("crm_public") or "")}


# ---------------------------------------------------------------- việc trên đĩa

def va_crm_da_cai():
    """CRM học viên đã giải nén từ trước vẫn nhận các bản vá giao diện mới (suite/goi/va/). Chỉ sửa khi gặp đúng đoạn mã cũ,
    nên chạy lại nhiều lần không sao; học viên đã tự sửa tệp đó thì bỏ qua, không ghi đè."""
    try:
        sys.path.insert(0, str(ROOT / "suite" / "goi" / "va"))
        import crm_bang_khach
    except Exception:  # noqa: BLE001
        return 0
    n = 0
    for bo in _mac_dinh(_doc())["bo"]:
        for ten, ds in crm_bang_khach.VA:
            f = _goc(bo) / "crm" / ten
            try:
                s = f.read_text(encoding="utf-8")
            except OSError:
                continue
            if all(s.count(cu) == 1 for cu, _ in ds):
                try:
                    f.write_text(crm_bang_khach.ap(ten, s), encoding="utf-8")
                    n += 1
                except (SystemExit, OSError):
                    pass
    return n


def _giai_nen_zip(nguon, dich):
    dich.mkdir(parents=True, exist_ok=True)
    goc = dich.resolve()
    with zipfile.ZipFile(nguon) as z:
        for info in z.infolist():
            if (goc / info.filename).resolve() != goc and goc not in (goc / info.filename).resolve().parents:
                raise ValueError("đường dẫn lạ trong gói: %s" % info.filename)
        z.extractall(goc)


def _nguon_zip(ten):
    """assets/<ten> trong gói đã cài; không có thì đọc thẳng từ tệp gói kèm theo."""
    d = _thu_muc_goi()
    if d and (d / "assets" / ten).is_file():
        return d / "assets" / ten
    tam = KHO / "tam" / ten
    tam.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(GOI_ZIP) as z:
        tam.write_bytes(z.read("assets/" + ten))
    return tam


def _giai_nen_bo(bo):
    g = _goc(bo)
    for con in ("crm", "lead"):
        if (g / con).exists() and any((g / con).iterdir()):
            raise ValueError("Thư mục %s đã có dữ liệu, không ghi đè" % (g / con))
    _giai_nen_zip(_nguon_zip("crm-source.zip"), g / "crm")
    _giai_nen_zip(_nguon_zip("lead-source.zip"), g / "lead")
    va_crm_da_cai()
    if bo.get("cong_crm") != 3000 or bo.get("cong_lead") != 4173:
        _doi_cong(g, bo["cong_crm"], bo["cong_lead"])


def _doi_cong(g, crm, lead, thu_muc_lead=("lead",)):
    """Sửa địa chỉ trong bản chép cho khớp cổng mới."""
    f = g / "crm" / "template" / "business.json"
    try:
        b = json.loads(f.read_text(encoding="utf-8"))
        b["siteUrl"] = "http://localhost:%d" % crm
        cu = [o for o in (b.get("leadOrigins") or []) if not re.match(r"^http://(localhost|127\.0\.0\.1):\d+$", o)]
        b["leadOrigins"] = ["http://localhost:%d" % lead, "http://127.0.0.1:%d" % lead] + cu
        f.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError):
        pass
    for con in thu_muc_lead:
        c = g / con / "lead-config.js"
        try:
            s = c.read_text(encoding="utf-8")
            c.write_text(re.sub(r"http://(localhost|127\.0\.0\.1):\d+/api/consultation-leads",
                                "http://localhost:%d/api/consultation-leads" % crm, s), encoding="utf-8")
        except OSError:
            pass


def _bo_qua_khi_chep(thu_muc, ten):
    return [x for x in ten if x in ("node_modules", ".local", ".wrangler", "dist", ".git") or x.endswith(".sqlite")]


# ---------------------------------------------------------------- phát trang Lead qua TISA BOT

_ATTR_GOC = re.compile(r'((?:href|src|action)=")/(?!/)')


def _phat_tep(trang, duong, bo):
    goc_lead = (_goc(bo) / trang.get("thu_muc_con", "lead")).resolve()
    duong = duong.lstrip("/")
    f = (goc_lead / duong).resolve()
    if f != goc_lead and goc_lead not in f.parents:
        return Response(status_code=403)
    if any(p.startswith(".") for p in Path(duong).parts) or f.name in _BO_QUA_FILE:
        return Response(status_code=404)
    if f.is_dir():
        f = f / "index.html"
    if not f.is_file():
        return Response("Không có trang này", status_code=404, media_type="text/plain; charset=utf-8")
    tien_to = "/tisa-web/trang/%s/" % trang["slug"]
    dau = {"x-content-type-options": "nosniff", "referrer-policy": "strict-origin-when-cross-origin", "cache-control": "no-cache"}
    if f.name == "lead-config.js":
        s = f.read_text(encoding="utf-8")
        s = re.sub(r'crmEndpoint:\s*"[^"]*"', 'crmEndpoint: "/tisa-web/crm-form/%s"' % bo["id"], s)
        s = re.sub(r'thankYouPage:\s*"/?([^"]*)"', lambda m: 'thankYouPage: "%s%s"' % (tien_to, m.group(1)), s)
        return Response(s, media_type="application/javascript; charset=utf-8", headers=dau)
    if f.suffix.lower() in (".html", ".htm"):
        s = f.read_text(encoding="utf-8")
        s = _ATTR_GOC.sub(lambda m: m.group(1) + tien_to, s)
        s = s.replace('"/cam-on/"', '"%scam-on/"' % tien_to)
        return Response(s, media_type="text/html; charset=utf-8", headers=dict(dau, **{"x-frame-options": "SAMEORIGIN"}))
    return FileResponse(str(f), headers=dau)


def _qua_tai(khoa, gioi_han, giay):
    now = time.time()
    with _KHOA:
        q = [t for t in _TAN_SUAT.get(khoa, []) if now - t < giay]
        if len(q) >= gioi_han:
            _TAN_SUAT[khoa] = q
            return True
        q.append(now)
        _TAN_SUAT[khoa] = q
        if len(_TAN_SUAT) > 5000:
            _TAN_SUAT.clear()
        return False


# ---------------------------------------------------------------- chatbot -> CRM -> Zalo, chạy nền

# Chủ yêu cầu 09/11/2026: mọi hệ thống trả lời tự động có nhận data thì tự đẩy vào CRM, rồi CRM lấy data để kết bạn, nhắn chăm sóc.
# - Mỗi phút: tin khách mới trong kho hội thoại (mọi kênh chatbot) có số điện thoại hoặc email -> /api/chatbot-leads của CRM đang
#   nối (khoá chatbot ở ~/.config/tisa-crm/chatbot.env), kèm hội thoại gốc, kênh, mức tiềm năng tự chấm. CRM tự gộp theo số.
# - Khách Fanpage (chưa có trên Zalo) để lại số -> thêm vào hàng chờ kết bạn Zalo của CRM (bảng khách đăng ký tư vấn).
# - Mỗi 10 phút: gọi lượt crm_zalo_sync của gói. Lượt đó chỉ kết bạn, nhắn khi chủ đã duyệt mẫu và bật trong cài đặt Zalo của gói.
TEP_DB = KHO / "dong-bo-crm.json"
_SDT = re.compile(r"(?<![\d+])(?:\+?84|0)(?:[\s.\-]?\d){9}(?!\d)")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_NONG = re.compile(r"chuyển khoản|chuyen khoan|đặt cọc|dat coc|\bcọc\b|thanh toán|chốt|lấy luôn|mua luôn|đăng ký luôn|đk luôn|stk|số tài khoản", re.I)
_AM = re.compile(r"giá|bao nhiêu|học phí|lịch|khi nào|ở đâu|địa chỉ|tư vấn|ưu đãi|khuyến mãi|còn chỗ|bảo hành", re.I)


def _db_doc():
    try:
        d = json.loads(TEP_DB.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            return d
    except (OSError, ValueError):
        pass
    return {"day_khach": True, "hang_zalo": True, "zalo_tu_chay": True, "moc": None, "da_day": {}, "nhat_ky": [], "so_day": 0}


def _db_ghi(d):
    d["nhat_ky"] = (d.get("nhat_ky") or [])[-40:]
    if len(d.get("da_day") or {}) > 20000:
        d["da_day"] = dict(list(d["da_day"].items())[-10000:])
    KHO.mkdir(parents=True, exist_ok=True)
    tam = TEP_DB.with_suffix(".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, TEP_DB)


def _cau_hinh_crm():
    th = Path(os.getenv("TISA_CRM_CONFIG_DIR") or (Path.home() / ".config" / "tisa-crm"))
    try:
        kv = dict(l.strip().split("=", 1) for l in (th / "chatbot.env").read_text(encoding="utf-8").splitlines() if "=" in l)
    except OSError:
        return "", ""
    return kv.get("CRM_URL", "").rstrip("/"), kv.get("CRM_CHATBOT_KEY", "").strip()


def _chuan_sdt(raw):
    d = re.sub(r"\D", "", raw or "")
    if d.startswith("84") and len(d) == 11:
        d = "0" + d[2:]
    return d if re.fullmatch(r"0[35789]\d{8}", d) else ""


def _kenh(acc):
    a = str(acc or "").lower()
    if a.startswith(("messenger", "facebook", "fb")):
        return "facebook"
    if a.startswith("zalo"):
        return "zalo"
    return "khac"


def _cham_diem(khach_noi):
    m = _NONG.search(khach_noi)
    if m:
        return 4, "Khách nhắc \"%s\" trong hội thoại (TISA BOT tự chấm)." % m.group(0)
    m = _AM.search(khach_noi)
    if m:
        return 3, "Khách hỏi về \"%s\" và để lại liên hệ (TISA BOT tự chấm)." % m.group(0)
    return 2, "Khách để lại liên hệ, chưa hỏi giá hay lịch (TISA BOT tự chấm)."


def _ts(t):
    try:
        return datetime.fromtimestamp(float(t)).strftime("%d/%m/%Y %H:%M")
    except (TypeError, ValueError, OSError):
        return ""


def _quet_hoi_thoai(d, tu_luc=None):
    """Đọc kho hội thoại (chỉ đọc). Trả (danh sách khách cần đẩy, mốc mới)."""
    import sqlite3
    db = ROOT / "server" / "customer_conversations.sqlite3"
    if not db.is_file():
        return [], d.get("moc")
    c = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=5)
    try:
        if d.get("moc") is None and tu_luc is None:
            r = c.execute("select max(id) from messages").fetchone()
            return [], (r[0] or 0)
        if tu_luc is not None:
            rows = c.execute("select id, conversation_id, text from messages where sender_type='customer' and created_at>=? order by id",
                             (tu_luc,)).fetchall()
        else:
            rows = c.execute("select id, conversation_id, text from messages where sender_type='customer' and id>? order by id limit 3000",
                             (d["moc"],)).fetchall()
        moc = max([r[0] for r in rows], default=d.get("moc") or 0)
        tim = {}
        for _, cid, txt in rows:
            txt = txt or ""
            for m in _SDT.finditer(txt):
                p = _chuan_sdt(m.group(0))
                if p:
                    tim.setdefault(cid, {})["phone"] = p
            m = _EMAIL.search(txt)
            if m:
                tim.setdefault(cid, {})["email"] = m.group(0)[:254]
        ra = []
        for cid, lien in tim.items():
            khoa = "%s:%s" % (cid, lien.get("phone") or lien.get("email"))
            if khoa in (d.get("da_day") or {}):
                continue
            cv = c.execute("select channel_account_id, external_chat_id, title, customer_id, bot_id from conversations where id=?", (cid,)).fetchone()
            if not cv:
                continue
            ten = ""
            if cv[3]:
                kh = c.execute("select name from customers where id=?", (cv[3],)).fetchone()
                ten = (kh[0] if kh else "") or ""
            ten = (ten or cv[2] or "Khách %s" % _kenh(cv[0])).strip()[:200]
            tin = c.execute("select sender_type, text, created_at, message_type from messages where conversation_id=? order by created_at, id",
                            (cid,)).fetchall()
            tr = [{"from": "Khách" if st == "customer" else "Page",
                   "text": ((t or "").replace("[TACH_TIN]", "\n").strip() or "[%s]" % (mt or "Đính kèm"))[:4000], "time": _ts(ts)}
                  for st, t, ts, mt in tin]
            while tr and len(json.dumps(tr, ensure_ascii=False).encode()) > 50000:
                tr.pop(0)
            khach_noi = " ".join((t or "") for st, t, _, _ in tin if st == "customer")[-6000:]
            diem, ly_do = _cham_diem(khach_noi)
            cuoi = [x["text"] for x in tr if x["from"] == "Khách"][-3:]
            ra.append({"khoa": khoa, "kenh": _kenh(cv[0]), "external_id": str(cv[1])[:200], "name": ten, "bot": cv[4],
                       "phone": lien.get("phone", ""), "email": lien.get("email", ""), "transcript": tr,
                       "summary": ("Khách để lại liên hệ qua chatbot (%s). Khách nói gần nhất: %s" % (_kenh(cv[0]), " | ".join(cuoi)))[:7900],
                       "potential": diem, "potential_reason": ly_do})
        return ra, moc
    finally:
        c.close()


async def _day_mot(cli, url, key, k, hang_zalo):
    body = {"channel": k["kenh"], "external_id": k["external_id"], "name": k["name"], "summary": k["summary"],
            "transcript": k["transcript"], "potential": k["potential"], "potential_reason": k["potential_reason"]}
    if k["phone"]:
        body["phone"] = k["phone"]
    if k["email"]:
        body["email"] = k["email"]
    r = await cli.post(url + "/api/chatbot-leads", json=body,
                       headers={"authorization": "Bearer " + key, "user-agent": "TISA-BOT/1.0"})
    if r.status_code >= 300:
        raise ValueError("CRM trả HTTP %s" % r.status_code)
    # Khách Fanpage có số: vào hàng chờ kết bạn Zalo (bảng khách đăng ký tư vấn của CRM). Khách Zalo đã là liên hệ Zalo rồi.
    if hang_zalo and k["kenh"] == "facebook" and k["phone"]:
        try:
            await cli.post(url + "/api/consultation-leads", json={
                "requestId": "tisa-bot-" + secrets.token_hex(10), "name": k["name"][:120], "phone": k["phone"],
                "email": k["email"], "course": "Khách từ chatbot Fanpage", "wants": k["summary"][:500], "consent": True, "website": ""},
                headers={"origin": url, "cf-connecting-ip": "chatbot-" + k["phone"], "user-agent": "TISA-BOT/1.0"})
        except Exception:  # noqa: BLE001
            pass


async def dong_bo_mot_luot(tu_luc=None):
    """Một lượt đẩy khách chatbot vào CRM. Trả tóm tắt."""
    url, key = _cau_hinh_crm()
    with _KHOA:
        d = _db_doc()
    if not url or not key:
        return {"ok": False, "error": "Chưa nối CRM với TISA BOT (bấm Nối TISA BOT ở Web CRM)."}
    if not d.get("day_khach") and tu_luc is None:
        return {"ok": True, "tat": True}
    ds, moc = await asyncio.to_thread(_quet_hoi_thoai, d, tu_luc)
    import httpx
    da, loi = 0, ""
    async with httpx.AsyncClient(timeout=20) as cli:
        for k in ds:
            try:
                await _day_mot(cli, url, key, k, d.get("hang_zalo", True))
            except Exception as e:  # noqa: BLE001
                loi = "%s" % e
                break
            da += 1
            d.setdefault("da_day", {})[k["khoa"]] = _bay_gio()
            d.setdefault("nhat_ky", []).append({"luc": _bay_gio(), "ten": k["name"][:60], "kenh": k["kenh"],
                                                 "lien_he": (k["phone"][:4] + "…" + k["phone"][-3:]) if k["phone"] else "email",
                                                 "diem": k["potential"]})
    with _KHOA:
        moi = _db_doc()
        moi["da_day"] = {**(moi.get("da_day") or {}), **(d.get("da_day") or {})}
        moi["nhat_ky"] = d.get("nhat_ky") or []
        moi["so_day"] = int(moi.get("so_day") or 0) + da
        if not loi and tu_luc is None:
            moi["moc"] = moc
        moi["lan_cuoi"] = _bay_gio()
        moi["loi"] = loi
        _db_ghi(moi)
    return {"ok": not loi, "da_day": da, "tim_thay": len(ds), "error": loi}


def _zalo_bat():
    try:
        cfg = json.loads((Path(cfgmod.STATE_DIR) / "plugin-data" / "crm-zalo" / "config.json").read_text(encoding="utf-8"))
        return {k: bool(cfg.get(k)) for k in ("moi_ket_ban", "them_tu_inbox", "tao_don")}
    except (OSError, ValueError):
        return {"moi_ket_ban": False, "them_tu_inbox": False, "tao_don": False}


async def zalo_mot_luot():
    bat = _zalo_bat()
    if not (bat["moi_ket_ban"] or bat["them_tu_inbox"]):
        return {"ok": True, "tat": True}
    import plugins_host
    _, route = await asyncio.to_thread(plugins_host.plugin_tools, "full", None, scope_vault=False)
    r = route.get("crm_zalo_sync")
    if not r:
        return {"ok": False, "error": "Gói web mẫu đang tắt hoặc thiếu công cụ Zalo"}
    kq = await r["call"]({})
    with _KHOA:
        d = _db_doc()
        d["zalo_lan_cuoi"] = _bay_gio()
        d["zalo_ket_qua"] = str(kq)[:400]
        _db_ghi(d)
    return {"ok": True, "ket_qua": str(kq)[:400]}


# ---------------------------------------------------------------- gắn vào app

def gan(app):

    @app.on_event("startup")
    async def _tu_cai_goi():
        async def lam():
            await asyncio.sleep(15)
            try:
                await asyncio.to_thread(va_crm_da_cai)
                kq = await asyncio.to_thread(cai_goi)
                if not kq.get("ok") and not kq.get("da_co"):
                    print("[tisa_web_mau] chưa cài gói web mẫu: %s" % kq.get("error"), file=sys.stderr)
            except Exception as e:  # noqa: BLE001
                print("[tisa_web_mau] cài gói lỗi: %s: %s" % (type(e).__name__, e), file=sys.stderr)
        asyncio.create_task(lam())

        async def nen():
            await asyncio.sleep(45)
            dem = 0
            while True:
                try:
                    if _goi_da_cai():
                        await dong_bo_mot_luot()
                        if dem % 10 == 0 and _db_doc().get("zalo_tu_chay", True):
                            await zalo_mot_luot()
                except Exception as e:  # noqa: BLE001
                    print("[tisa_web_mau] đồng bộ CRM lỗi: %s: %s" % (type(e).__name__, e), file=sys.stderr)
                dem += 1
                await asyncio.sleep(60)
        asyncio.create_task(nen())

        async def tu_noi():
            await asyncio.sleep(75)
            while True:
                try:
                    await _tu_noi_crm_mot_luot()
                except Exception as e:  # noqa: BLE001
                    print("[tisa_web_mau] tự nối CRM lỗi: %s: %s" % (type(e).__name__, e), file=sys.stderr)
                await asyncio.sleep(90)
        asyncio.create_task(tu_noi())

    class _GiaYeuCau:
        """Gọi lại chính các nút Chạy / Nối từ bên trong máy chủ (không có người bấm)."""
        def __init__(self, du_lieu):
            self._d = du_lieu

        async def json(self):
            return self._d

    _TU_NOI = {"chay": 0, "noi": 0}

    async def _tu_noi_crm_mot_luot():
        """Web CRM mặc định tự chạy và tự nối với TISA BOT (Hỏi nhanh, Đội Quân AI, chatbot ghi khách).
        Chỉ làm khi gói web mẫu đã cài, Node đủ bản, và chủ chưa bấm Tắt. Mỗi bước thử tối đa 3 lần mỗi lần mở máy."""
        if _db_doc().get("crm_tu_noi") is False or not _goi_da_cai():
            return
        bo = _tim(_mac_dinh(_doc())["bo"], "bo1")
        if not bo:
            return
        tt = await asyncio.to_thread(_trang_thai_bo, bo)
        if not tt["crm_chay"]:
            if tt["dang_khoi_dong"] or _TU_NOI["chay"] >= 3 or not _node()[2]:
                return
            _TU_NOI["chay"] += 1
            kq = await _api_chay(_GiaYeuCau({"bo": bo["id"], "_he_thong": True}))
            if isinstance(kq, JSONResponse):
                print("[tisa_web_mau] tự chạy Web CRM chưa được: %s" % kq.body.decode("utf-8", "ignore")[:200], file=sys.stderr)
            return
        nb = tt.get("noi_bot") or {}
        if nb.get("tro_ly") and nb.get("chatbot"):
            return
        if _TU_NOI["noi"] >= 3:
            return
        _TU_NOI["noi"] += 1
        kq = await _api_noi(_GiaYeuCau({"bo": bo["id"], "_he_thong": True}))
        if isinstance(kq, JSONResponse):
            print("[tisa_web_mau] tự nối Web CRM chưa được: %s" % kq.body.decode("utf-8", "ignore")[:200], file=sys.stderr)
        elif not kq.get("ok"):
            print("[tisa_web_mau] tự nối Web CRM chưa đủ: %s" % json.dumps(kq, ensure_ascii=False)[:300], file=sys.stderr)

    @app.get("/tisa-web/api/mau/dong-bo")
    async def _api_db():
        d = _db_doc()
        url, key = _cau_hinh_crm()
        return {"ok": True, "noi": bool(url and key), "crm_url": url, "day_khach": d.get("day_khach", True), "hang_zalo": d.get("hang_zalo", True),
                "zalo_tu_chay": d.get("zalo_tu_chay", True), "zalo": _zalo_bat(), "so_day": d.get("so_day", 0),
                "lan_cuoi": d.get("lan_cuoi"), "loi": d.get("loi", ""), "nhat_ky": list(reversed(d.get("nhat_ky") or []))[:15],
                "zalo_lan_cuoi": d.get("zalo_lan_cuoi"), "zalo_ket_qua": d.get("zalo_ket_qua", "")}

    @app.post("/tisa-web/api/mau/dong-bo")
    async def _api_db_luu(request: Request):
        b = await _than(request)
        with _KHOA:
            d = _db_doc()
            for k in ("day_khach", "hang_zalo", "zalo_tu_chay"):
                if isinstance(b.get(k), bool):
                    d[k] = b[k]
            _db_ghi(d)
        kq = {}
        if b.get("quet_ngay"):
            ngay = max(1, min(90, int(b.get("quet_ngay") or 0)))
            kq = await dong_bo_mot_luot(tu_luc=time.time() - ngay * 86400)
        elif b.get("chay_ngay"):
            kq = await dong_bo_mot_luot()
        return {"ok": True, **({"ket_qua": kq} if kq else {})}

    def _cong_khai(request):
        try:
            import remote_tunnel
            st = remote_tunnel.MANAGER.status()
            if st.get("enabled") and st.get("url"):
                return st["url"].rstrip("/")
        except Exception:  # noqa: BLE001
            pass
        host = (request.headers.get("host") or "").split(":")[0]
        if host and host not in ("127.0.0.1", "localhost", "::1"):
            return "https://" + host
        return ""

    @app.get("/tisa-web/api/mau")
    async def _api_mau(request: Request):
        with _KHOA:
            d = _mac_dinh(_doc())
            _ghi(d)
        node, ban_node, du = await asyncio.to_thread(_node)
        goi = _goi_da_cai()
        bo = []
        for b in d["bo"]:
            x = dict(b)
            x.update(await asyncio.to_thread(_trang_thai_bo, b))
            bo.append(x)
        return {"ok": True, "node": {"co": bool(node), "ban": ban_node, "du": du},
                "goi": {"co": bool(goi), "ban": (goi or {}).get("version") or "", "bat": bool((goi or {}).get("enabled", True))},
                "bo": bo, "trang": d["trang"], "cong_khai": _cong_khai(request), "goc_tisa": str(request.base_url).rstrip("/")}

    @app.post("/tisa-web/api/mau/cai-goi")
    async def _api_cai_goi():
        kq = await asyncio.to_thread(cai_goi, True)
        return kq if kq.get("ok") else JSONResponse(kq, status_code=400)

    async def _than(request):
        try:
            b = await request.json()
            return b if isinstance(b, dict) else {}
        except ValueError:
            return {}

    @app.post("/tisa-web/api/mau/giai-nen")
    async def _api_giai_nen(request: Request):
        b = await _than(request)
        bo = _tim(_mac_dinh(_doc())["bo"], b.get("bo"))
        if not bo:
            return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
        try:
            await asyncio.to_thread(_giai_nen_bo, bo)
        except (ValueError, OSError, KeyError, zipfile.BadZipFile) as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        return {"ok": True, "goc": str(_goc(bo))}

    @app.post("/tisa-web/api/mau/chay")
    async def _api_chay(request: Request):
        b = await _than(request)
        bo = _tim(_mac_dinh(_doc())["bo"], b.get("bo"))
        if not bo:
            return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
        if bo.get("id") == "bo1" and not b.get("_he_thong") and _db_doc().get("crm_tu_noi") is False:
            dd = _db_doc()
            dd["crm_tu_noi"] = True        # chủ bấm Chạy: bật lại chế độ tự chạy, tự nối
            _db_ghi(dd)
        node, ban_node, du = _node()
        if not du:
            return JSONResponse({"ok": False, "can_node": True,
                                 "error": "Cần Node.js 22.13 trở lên (máy đang có %s). Tải bản LTS ở nodejs.org rồi bấm lại." % (ban_node or "chưa cài")}, status_code=400)
        crm = _goc(bo) / "crm"
        if not (crm / "package.json").is_file():
            try:
                await asyncio.to_thread(_giai_nen_bo, bo)
            except (ValueError, OSError, KeyError, zipfile.BadZipFile) as e:
                return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        p = _CHAY.get(bo["id"])
        if p and p.poll() is None:
            return {"ok": True, "dang_khoi_dong": True}
        doi = ""
        if not _cua_minh(bo) and (_cong_mo(bo["cong_crm"]) or _cong_mo(bo["cong_lead"])):
            # Cổng đang bị ứng dụng khác dùng: chuyển bộ này sang cặp cổng trống, sửa địa chỉ trong mã cho khớp.
            with _KHOA:
                d = _mac_dinh(_doc())
                try:
                    c, l = _cong_trong({x.get("cong_crm") for x in d["bo"]} | {x.get("cong_lead") for x in d["bo"]})
                except ValueError as e:
                    return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
                x = _tim(d["bo"], bo["id"])
                doi = "Cổng %s đang bị ứng dụng khác dùng, đã chuyển sang cổng %s." % (bo["cong_crm"], c)
                x["cong_crm"], x["cong_lead"] = c, l
                _ghi(d)
                bo = dict(x)
            g = _goc(bo)
            cac_lead = [q.name for q in g.iterdir() if q.is_dir() and re.match(r"^lead(-\d+)?$", q.name)]
            await asyncio.to_thread(_doi_cong, g, bo["cong_crm"], bo["cong_lead"], cac_lead)
        env = _moi_truong(node)
        env.update(PORT=str(bo["cong_crm"]), LEAD_PORT=str(bo["cong_lead"]))
        (crm / ".local").mkdir(parents=True, exist_ok=True)
        nhat_ky = open(crm / ".local" / "tisa-chay.log", "w", encoding="utf-8")
        _CHAY[bo["id"]] = subprocess.Popen(
            [node, "scripts/demo-local.mjs", "--background", "--lead=" + str(_goc(bo) / "lead")], cwd=str(crm), env=env,
            stdout=nhat_ky, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        nhat_ky.close()
        return {"ok": True, "dang_khoi_dong": True, "doi_cong": doi}

    @app.post("/tisa-web/api/mau/tat")
    async def _api_tat(request: Request):
        b = await _than(request)
        bo = _tim(_mac_dinh(_doc())["bo"], b.get("bo"))
        if not bo:
            return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
        node, _, _ = _node()
        crm = _goc(bo) / "crm"
        if not node or not crm.is_dir():
            return JSONResponse({"ok": False, "error": "Bộ web này chưa chạy"}, status_code=400)
        if bo.get("id") == "bo1" and not b.get("_he_thong"):
            dd = _db_doc()
            dd["crm_tu_noi"] = False       # chủ chủ động tắt: máy không tự bật lại
            _db_ghi(dd)
        r = await asyncio.to_thread(subprocess.run, [node, "scripts/demo-local.mjs", "--stop"], cwd=str(crm), env=_moi_truong(node),
                                    capture_output=True, text=True, timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return {"ok": True, "thong_bao": (r.stdout or "").strip()[-200:]}

    @app.post("/tisa-web/api/mau/noi")
    async def _api_noi(request: Request):
        """Nối CRM của bộ này với TISA BOT: tạo khoá trợ lý và khoá chatbot (lưu kín ở ~/.config/tisa-crm, không in ra),
        thêm kết nối tisa-crm cho Hỏi nhanh và Đội Quân AI, và cho plugin Data chatbot biết địa chỉ CRM."""
        b = await _than(request)
        bo = _tim(_mac_dinh(_doc())["bo"], b.get("bo"))
        if not bo:
            return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
        if not _goi_da_cai():
            return JSONResponse({"ok": False, "error": "Chưa cài gói web mẫu. Bấm Cài gói trước."}, status_code=400)
        if not (_cua_minh(bo) and _cong_mo(bo["cong_crm"])):
            return JSONResponse({"ok": False, "error": "Bấm Chạy cho Web CRM trước, rồi nối."}, status_code=400)
        node, _, du = _node()
        crm = _goc(bo) / "crm"
        try:
            token = (crm / ".local" / "bootstrap-token").read_text(encoding="utf-8").strip()
        except OSError:
            return JSONResponse({"ok": False, "error": "Thiếu khoá khởi tạo của CRM. Tắt rồi Chạy lại Web CRM."}, status_code=400)
        url = "http://localhost:%s" % bo["cong_crm"]
        env = _moi_truong(node)
        env["BOOTSTRAP_TOKEN"] = token
        for co in ("--agent-key", "--chatbot-key"):
            r = await asyncio.to_thread(subprocess.run, [node, "scripts/sites-bootstrap.mjs", url, co], cwd=str(crm), env=env,
                                        capture_output=True, text=True, timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if r.returncode != 0:
                loi = (r.stderr or r.stdout or "").strip().splitlines()
                return JSONResponse({"ok": False, "error": "Chưa tạo được khoá: %s" % (loi[-1][:200] if loi else "lỗi không rõ")}, status_code=400)
        ket = {"tro_ly": False, "chatbot": False}
        try:
            import mcp_hub
            import mcp_store
            th = Path(os.getenv("TISA_CRM_CONFIG_DIR") or (Path.home() / ".config" / "tisa-crm"))
            kv = dict(l.strip().split("=", 1) for l in (th / "crm.env").read_text(encoding="utf-8").splitlines() if "=" in l)
            for c in [c for c in mcp_store.list_connections() if c.get("connector") == "tisa-crm"]:
                mcp_store.delete_connection(c["id"])
            cid, loi = mcp_store.add_connection("tisa-crm", {"label": "CRM (%s)" % bo.get("ten", ""), "perm": "full",
                                                             "fields": {"crm_url": kv.get("CRM_URL", url), "api_key": kv.get("CRM_AGENT_KEY", "")}})
            if loi:
                raise ValueError(loi)
            mcp_hub.invalidate_cache()
            kq = await mcp_hub.validate_connection(cid)
            ket["tro_ly"] = bool(kq.get("ok"))
            ket["loi_tro_ly"] = "" if kq.get("ok") else str(kq.get("error") or "")[:200]
        except Exception as e:  # noqa: BLE001
            ket["loi_tro_ly"] = "%s: %s" % (type(e).__name__, str(e)[:200])
        try:
            f = Path(cfgmod.STATE_DIR) / "plugin-data" / "crm-chatbot-leads" / "connection.json"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps({"crm_url": url}, ensure_ascii=False), encoding="utf-8")
            try:
                f.chmod(0o600)
            except OSError:
                pass
            ket["chatbot"] = True
        except OSError as e:
            ket["loi_chatbot"] = str(e)[:200]
        return {"ok": ket["tro_ly"] and ket["chatbot"], **ket}

    @app.post("/tisa-web/api/mau/crm-public")
    async def _api_crm_public(request: Request):
        """Địa chỉ công khai của CRM (đã trỏ về cổng CRM, ví dụ qua Cloudflare Tunnel) để mở và chạy demo trên mạng. Để trống = dùng localhost."""
        b = await _than(request)
        u = str(b.get("url") or "").strip().rstrip("/")
        if u and not re.match(r"^https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,200}$", u):
            return JSONResponse({"ok": False, "error": "Địa chỉ không hợp lệ. Dạng đúng: https://crm.ten-mien-cua-ban.com"}, status_code=400)
        with _KHOA:
            d = _mac_dinh(_doc())
            x = _tim(d["bo"], b.get("bo"))
            if not x:
                return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
            if u:
                x["crm_public"] = u
            else:
                x.pop("crm_public", None)
            _ghi(d)
        return {"ok": True, "crm_public": u}

    @app.post("/tisa-web/api/mau/nhan-ban")
    async def _api_nhan_ban(request: Request):
        b = await _than(request)
        ten = re.sub(r"[\x00-\x1f<>]", "", str(b.get("ten") or "")).strip()[:60]
        with _KHOA:
            d = _mac_dinh(_doc())
        if b.get("loai") == "trang":
            t0 = _tim(d["trang"], b.get("id"))
            bo = _tim(d["bo"], (t0 or {}).get("bo"))
            if not t0 or not bo:
                return JSONResponse({"ok": False, "error": "Không thấy trang"}, status_code=404)
            g = _goc(bo)
            nguon = g / t0.get("thu_muc_con", "lead")
            if not (nguon / "index.html").is_file():
                return JSONResponse({"ok": False, "error": "Trang gốc chưa có trên máy. Bấm Chạy ở Web CRM trước để lấy mã về."}, status_code=400)
            n = 2
            while (g / ("lead-%d" % n)).exists():
                n += 1
            con = "lead-%d" % n
            ten = ten or "Lead Page %d" % n
            await asyncio.to_thread(shutil.copytree, nguon, g / con, ignore=_bo_qua_khi_chep)
            slug, dung = _khong_dau(ten), {x.get("slug") for x in d["trang"]}
            while slug in dung:
                slug += "-" + secrets.token_hex(2)
            moi = {"id": "lead-" + secrets.token_hex(4), "bo": bo["id"], "ten": ten, "thu_muc_con": con, "slug": slug,
                   "tu": t0["id"], "tao": _bay_gio()}
            with _KHOA:
                d = _mac_dinh(_doc())
                d["trang"].append(moi)
                _ghi(d)
            return {"ok": True, "trang": moi}
        if b.get("loai") == "bo":
            bo0 = _tim(d["bo"], b.get("id"))
            if not bo0:
                return JSONResponse({"ok": False, "error": "Không thấy bộ web"}, status_code=404)
            g0 = _goc(bo0)
            n = 2
            while Path(str(GOC_MAC_DINH) + "-%d" % n).exists():
                n += 1
            g = Path(str(GOC_MAC_DINH) + "-%d" % n)
            try:
                c, l = _cong_trong({x.get("cong_crm") for x in d["bo"]} | {x.get("cong_lead") for x in d["bo"]})
            except ValueError as e:
                return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
            ten = ten or "Web CRM %d" % n
            bo = {"id": "bo" + secrets.token_hex(3), "ten": ten, "thu_muc": str(g), "cong_crm": c, "cong_lead": l,
                  "tu": bo0["id"], "tao": _bay_gio()}
            if (g0 / "crm" / "package.json").is_file():
                await asyncio.to_thread(shutil.copytree, g0, g, ignore=_bo_qua_khi_chep)
                cac_lead = [p.name for p in g.iterdir() if p.is_dir() and re.match(r"^lead(-\d+)?$", p.name)]
                await asyncio.to_thread(_doi_cong, g, c, l, cac_lead)
            else:
                try:
                    await asyncio.to_thread(_giai_nen_bo, bo)
                except (ValueError, OSError, KeyError, zipfile.BadZipFile) as e:
                    return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
            slug, dung = _khong_dau(ten + " lead"), {x.get("slug") for x in d["trang"]}
            while slug in dung:
                slug += "-" + secrets.token_hex(2)
            trang = {"id": "lead-" + secrets.token_hex(4), "bo": bo["id"], "ten": "Lead Page & Sale Page (%s)" % ten,
                     "thu_muc_con": "lead", "slug": slug, "tao": _bay_gio()}
            with _KHOA:
                d = _mac_dinh(_doc())
                d["bo"].append(bo)
                d["trang"].append(trang)
                _ghi(d)
            return {"ok": True, "bo": bo, "trang": trang}
        return JSONResponse({"ok": False, "error": "Thiếu loại nhân bản"}, status_code=400)

    @app.post("/tisa-web/api/mau/doi-ten")
    async def _api_doi_ten(request: Request):
        b = await _than(request)
        ten = re.sub(r"[\x00-\x1f<>]", "", str(b.get("ten") or "")).strip()[:60]
        if not ten:
            return JSONResponse({"ok": False, "error": "Tên không được trống"}, status_code=400)
        with _KHOA:
            d = _mac_dinh(_doc())
            x = _tim(d["bo" if b.get("loai") == "bo" else "trang"], b.get("id"))
            if not x:
                return JSONResponse({"ok": False, "error": "Không thấy"}, status_code=404)
            x["ten"] = ten
            _ghi(d)
        return {"ok": True}

    @app.post("/tisa-web/api/mau/go")
    async def _api_go(request: Request):
        """Bỏ khỏi danh sách. Thư mục trên máy giữ nguyên. Hai web mặc định không gỡ được."""
        b = await _than(request)
        with _KHOA:
            d = _mac_dinh(_doc())
            ds = d["bo" if b.get("loai") == "bo" else "trang"]
            x = _tim(ds, b.get("id"))
            if not x:
                return JSONResponse({"ok": False, "error": "Không thấy"}, status_code=404)
            if x.get("mac_dinh"):
                return JSONResponse({"ok": False, "error": "Web mặc định không gỡ được"}, status_code=400)
            if b.get("loai") == "bo" and _cong_mo(x.get("cong_crm")):
                return JSONResponse({"ok": False, "error": "Tắt bộ web này trước khi gỡ"}, status_code=400)
            ds.remove(x)
            if b.get("loai") == "bo":
                d["trang"] = [t for t in d["trang"] if t.get("bo") != x["id"]]
            _ghi(d)
        return {"ok": True, "thu_muc_giu": str(_goc(x)) if b.get("loai") == "bo" else ""}

    # ---------- công khai: trang Lead/Sale và form gửi về CRM ----------

    @app.get("/tisa-web/trang/{slug}")
    async def _trang_khong_gach(slug: str):
        return RedirectResponse("/tisa-web/trang/%s/" % slug, status_code=301)

    @app.get("/tisa-web/trang/{slug}/{duong:path}")
    async def _trang(slug: str, duong: str = ""):
        d = _mac_dinh(_doc())
        t = next((x for x in d["trang"] if x.get("slug") == slug), None)
        bo = _tim(d["bo"], (t or {}).get("bo"))
        if not t or not bo:
            return Response("Không có trang này", status_code=404, media_type="text/plain; charset=utf-8")
        f = (_goc(bo) / t.get("thu_muc_con", "lead") / duong.lstrip("/"))
        if duong and not duong.endswith("/") and f.is_dir():
            return RedirectResponse("/tisa-web/trang/%s/%s/" % (slug, duong.strip("/")), status_code=301)
        return await asyncio.to_thread(_phat_tep, t, duong, bo)

    @app.post("/tisa-web/crm-form/{bo_id}")
    async def _form(bo_id: str, request: Request):
        bo = _tim(_mac_dinh(_doc())["bo"], bo_id)
        if not bo:
            return JSONResponse({"error": "Không tìm thấy nơi nhận"}, status_code=404)
        ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
        if _qua_tai("ip:" + ip, 8, 60) or _qua_tai("bo:" + bo_id, 300, 3600):
            return JSONResponse({"error": "Gửi quá nhiều lần, vui lòng thử lại sau ít phút."}, status_code=429)
        than = await request.body()
        if len(than) > 16_000:
            return JSONResponse({"error": "Thông tin quá dài"}, status_code=413)
        if not (_cong_mo(bo["cong_crm"]) and _cua_minh(bo)):
            return JSONResponse({"error": "Hệ thống đang bảo trì, vui lòng thử lại sau hoặc gọi trực tiếp cho chúng tôi."}, status_code=503)
        import httpx
        site = _site_url(bo) or "http://localhost:%s" % bo["cong_crm"]
        try:
            async with httpx.AsyncClient(timeout=20) as cli:
                r = await cli.post("http://127.0.0.1:%s/api/consultation-leads" % bo["cong_crm"], content=than,
                                   headers={"content-type": "application/json", "origin": site, "cf-connecting-ip": ip,
                                            "user-agent": "TISA-BOT/1.0"})
        except httpx.HTTPError:
            return JSONResponse({"error": "Chưa gửi được, vui lòng thử lại."}, status_code=502)
        try:
            return JSONResponse(r.json(), status_code=r.status_code)
        except ValueError:
            return JSONResponse({"error": "Chưa gửi được, vui lòng thử lại."}, status_code=502)
