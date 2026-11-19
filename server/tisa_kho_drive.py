"""tisa_kho_drive.py - Kho tư liệu nối với Google Drive (V3.34, chủ yêu cầu 19/11/2026).

Hai việc, một thư mục Drive cho mỗi việc:
  1. THƯ MỤC LÀM VIỆC: tư liệu trong thư mục Drive này được chép về Kho tư liệu trên máy (đội AI đọc thẳng trên máy). Chạy khi bấm
     "Đồng bộ ngay" hoặc tự động theo chu kỳ. Chỉ chép về, KHÔNG xóa gì trên Drive hay trên máy.
  2. THƯ MỤC NHẬN KẾT QUẢ: kết quả đội AI làm xong (thư mục `03 - Ket qua` của văn phòng AI trong bộ não) được tải lên thư mục Drive này,
     giữ cấu trúc ngày/việc. Chạy khi bấm "Tải kết quả lên ngay" hoặc tự động khi có kết quả mới.

Dùng API Drive qua tisa_drive.py (OAuth, khóa cất trong Keychain trên Mac, tệp mã hóa trên Windows/Linux; không bao giờ qua bảng hay AI).
Chia việc: máy chủ TISA BOT (routes /tisa-kho-drive/api/*) lo phần tương tác (nối, duyệt thư mục, chọn, bật tắt, yêu cầu chạy);
cầu nối Đội Quân AI (suite/bridge/bang.py) gọi tick() mỗi vài giây: nó biết đường dẫn kho và văn phòng thật, và là nơi duy nhất chạy việc nặng.
Cấu hình và sổ ở STATE_DIR/kho-drive/ (cau-hinh.json, trang-thai.json, so-ve.json, so-len.json). Không ghi khóa vào các tệp này.
"""
from __future__ import annotations

import http.client
import json
import os
import re
import shutil
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import tisa_drive as D

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "kho-drive"
TEP_CH = DIR / "cau-hinh.json"
TEP_TT = DIR / "trang-thai.json"
TEP_VE = DIR / "so-ve.json"
TEP_LEN = DIR / "so-len.json"

NGAN_MAY = "12 - Thu muc lien ket tren may"     # cùng tên ngăn "Thư mục liên kết trên máy" của kho (bang.py KHO_DIRS['may'])
THU_MUC_KET_QUA = "03 - Ket qua"
MB = 1024 * 1024
XUAT = {  # tệp Google (không có dung lượng) xuất ra định dạng mở được ở mọi máy
    "application/vnd.google-apps.document": ("application/pdf", ".pdf"),
    "application/vnd.google-apps.presentation": ("application/pdf", ".pdf"),
    "application/vnd.google-apps.spreadsheet": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
    "application/vnd.google-apps.drawing": ("application/pdf", ".pdf"),
}
MAC_DINH = {"lam_viec": None, "ket_qua": None, "tu_ve": False, "ve_moi_phut": 15, "tu_len": False, "gioi_han_mb": 500, "yeu_cau": {}}
_lock = threading.Lock()
_chay = {"viec": None, "t": 0.0}
_TOI_DA_LEN_MOI_LUOT = 15
_ONE_ID = re.compile(r"^[A-Za-z0-9_-]{20,}$")


# ---------------------------------------------------------------- tệp nhỏ
def _doc(p: Path, md):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, type(md)) else md
    except (OSError, ValueError):
        return md


def _ghi(p: Path, d) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, p)


def cau_hinh() -> dict:
    d = dict(MAC_DINH)
    d.update(_doc(TEP_CH, {}))
    d["yeu_cau"] = dict(d.get("yeu_cau") or {})
    return d


def luu_cau_hinh(**kw) -> dict:
    with _lock:
        d = cau_hinh()
        d.update(kw)
        _ghi(TEP_CH, d)
    return d


def _ten_an_toan(t: str, mac_dinh: str = "tep") -> str:
    t = unicodedata.normalize("NFC", str(t or ""))
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", t).strip(" .")
    return (t or mac_dinh)[:120]


def _khong_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


# ---------------------------------------------------------------- nối Drive
def co_client() -> bool:
    return bool(D._kc().co(D.DICH_VU_CLIENT))


def luu_client(client_id: str, client_secret: str) -> tuple[bool, str]:
    client_id, client_secret = str(client_id or "").strip(), str(client_secret or "").strip()
    if not re.fullmatch(r"[0-9]+-[A-Za-z0-9_]+\.apps\.googleusercontent\.com", client_id):
        return False, "Client ID có dạng 123456-abc.apps.googleusercontent.com. Chép lại từ trang Google Cloud (Credentials)."
    if len(client_secret) < 10 or re.search(r"\s", client_secret):
        return False, "Client secret chưa đúng (thường bắt đầu bằng GOCSPX-). Chép lại, không có dấu cách."
    ok = D._kc().luu(D.DICH_VU_CLIENT, json.dumps({"client_id": client_id, "client_secret": client_secret}))
    return (True, "Đã cất khóa Google trên máy này.") if ok else (False, "Chưa cất được khóa trên máy này (kho khóa của máy không ghi được).")


def da_ket_noi() -> bool:
    return D.da_dang_nhap()


def dang_nhap() -> dict:
    return D.dang_nhap_bat_dau()


def dang_nhap_xem() -> str:
    return D.dang_nhap_trang_thai()


def ngat_ket_noi() -> bool:
    ok = D._kc().xoa(D.DICH_VU)
    luu_cau_hinh(email="")
    return ok


def tai_khoan() -> str:
    c = cau_hinh()
    if c.get("email") and time.time() - float(c.get("email_luc") or 0) < 3600:
        return c["email"]
    try:
        u = D.Drive()._json("GET", D.API + "/about", params={"fields": "user(emailAddress,displayName)"}).get("user") or {}
        e = u.get("emailAddress") or u.get("displayName") or ""
        luu_cau_hinh(email=e, email_luc=time.time())
        return e
    except Exception:  # noqa: BLE001
        return c.get("email") or ""


# ---------------------------------------------------------------- duyệt và chọn thư mục
def _muc_thu_muc(f: dict) -> dict:
    return {"id": f["id"], "ten": f.get("name") or f["id"]}


def liet_ke_thu_muc(cha: str = "") -> dict:
    """Thư mục con của một thư mục Drive. Gốc: Drive của tôi, Được chia sẻ với tôi, các ổ dùng chung."""
    d = D.Drive()
    cha = str(cha or "").strip()
    if not cha:
        muc = [{"id": "root", "ten": "Drive của tôi"}, {"id": "sharedWithMe", "ten": "Được chia sẻ với tôi"}]
        try:
            for x in (d._json("GET", D.API + "/drives", params={"pageSize": 50, "fields": "drives(id,name)"}).get("drives") or []):
                muc.append({"id": x["id"], "ten": x.get("name") or x["id"], "o_chung": True})
        except D.LoiDrive:
            pass
        return {"cha": "", "ten": "Google Drive", "muc": muc}
    if cha == "sharedWithMe":
        ds = d._json("GET", D.API + "/files", params={"q": "sharedWithMe = true and mimeType = '%s' and trashed = false" % D.FOLDER, "pageSize": 200,
                                                      "fields": "files(id,name)", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true", "orderBy": "name"}).get("files") or []
        return {"cha": cha, "ten": "Được chia sẻ với tôi", "muc": [_muc_thu_muc(x) for x in ds]}
    cha = re.sub(r"[^A-Za-z0-9_-]", "", cha)
    ten = "Drive của tôi" if cha == "root" else (d.thong_tin(cha).get("name") or cha)
    ds = d.liet_ke(cha, "mimeType = '%s'" % D.FOLDER, 500)
    return {"cha": cha, "ten": ten, "muc": [_muc_thu_muc(x) for x in ds]}


def phan_giai(lien_ket: str) -> dict:
    """Từ link hoặc mã thư mục Drive (dán vào) ra {id, ten}. Báo lỗi rõ nếu không phải thư mục."""
    t = str(lien_ket or "").strip()
    m = re.search(r"/folders/([A-Za-z0-9_-]{10,})", t) or re.search(r"[?&]id=([A-Za-z0-9_-]{10,})", t)
    ma = m.group(1) if m else (t if _ONE_ID.match(t) else "")
    if not ma:
        raise D.LoiDrive("LOI: Không đọc được mã thư mục từ link đã dán. Mở thư mục trên Drive, chép địa chỉ trên thanh địa chỉ (có dạng drive.google.com/drive/folders/...).")
    f = D.Drive().thong_tin(ma)
    if f.get("mimeType") != D.FOLDER:
        raise D.LoiDrive("LOI: Link này là một tệp, không phải thư mục.")
    return {"id": f["id"], "ten": f.get("name") or f["id"]}


def duong_ten(ma: str, toi_da: int = 6) -> str:
    """Đường dẫn chữ 'Drive > A > B' của một thư mục (đi ngược lên tối đa vài cấp)."""
    d = D.Drive()
    ten = []
    cur = ma
    for _ in range(toi_da):
        try:
            f = d._json("GET", D.API + "/files/" + urllib.parse.quote(cur), params={"fields": "id,name,parents", "supportsAllDrives": "true"})
        except D.LoiDrive:
            break
        ten.append(f.get("name") or cur)
        ps = f.get("parents") or []
        if not ps:
            break
        cur = ps[0]
    return " › ".join(["Drive"] + list(reversed(ten)))


def tao_thu_muc(cha: str, ten: str) -> dict:
    ten = str(ten or "").strip()
    if not ten or len(ten) > 100:
        raise D.LoiDrive("LOI: Tên thư mục trống hoặc quá dài.")
    cha = re.sub(r"[^A-Za-z0-9_-]", "", str(cha or "")) or "root"
    f = D.Drive().tao_thu_muc(ten, cha)
    return _muc_thu_muc(f)


def chon(vai_tro: str, ma: str, ten: str = "") -> dict:
    if vai_tro not in ("lam_viec", "ket_qua"):
        raise D.LoiDrive("LOI: vai trò phải là lam_viec hoặc ket_qua")
    ma = re.sub(r"[^A-Za-z0-9_-]", "", str(ma or ""))
    if not ma:
        raise D.LoiDrive("LOI: chưa chọn thư mục")
    f = D.Drive().thong_tin(ma) if ma != "root" else {"id": "root", "name": "Drive của tôi", "mimeType": D.FOLDER}
    if f.get("mimeType") != D.FOLDER:
        raise D.LoiDrive("LOI: Đây không phải thư mục.")
    muc = {"id": f["id"], "ten": f.get("name") or ma, "duong": duong_ten(f["id"]) if ma != "root" else "Drive của tôi"}
    luu_cau_hinh(**{vai_tro: muc})
    return muc


def yeu_cau(viec: str) -> None:
    """Bấm 'Đồng bộ ngay' / 'Tải kết quả lên ngay': ghi dấu giờ, cầu nối thấy thì chạy."""
    if viec not in ("ve", "len"):
        raise D.LoiDrive("LOI: việc phải là ve hoặc len")
    c = cau_hinh()
    yc = dict(c.get("yeu_cau") or {})
    yc[viec] = time.time()
    luu_cau_hinh(yeu_cau=yc)


# ---------------------------------------------------------------- trạng thái cho giao diện
def trang_thai() -> dict:
    c = cau_hinh()
    tt = _doc(TEP_TT, {})
    co_c, da = co_client(), da_ket_noi()
    buoc = "da_ket_noi" if da else ("chua_dang_nhap" if co_c else "chua_client")
    return {"ok": True, "buoc": buoc, "email": c.get("email") or "", "lam_viec": c.get("lam_viec"), "ket_qua": c.get("ket_qua"),
            "tu_ve": bool(c.get("tu_ve")), "ve_moi_phut": int(c.get("ve_moi_phut") or 15), "tu_len": bool(c.get("tu_len")),
            "gioi_han_mb": int(c.get("gioi_han_mb") or 500), "ve": tt.get("ve") or {}, "len": tt.get("len") or {},
            "dang_chay": tt.get("dang_chay") or "", "cau_noi_luc": tt.get("cau_noi_luc") or 0,
            "cau_noi_song": time.time() - float(tt.get("cau_noi_luc") or 0) < 90, "kho_may": tt.get("kho_may") or "",
            "cho_ve": float(c["yeu_cau"].get("ve") or 0) > float((tt.get("ve") or {}).get("yeu_cau_da") or 0),
            "cho_len": float(c["yeu_cau"].get("len") or 0) > float((tt.get("len") or {}).get("yeu_cau_da") or 0)}


def cai_dat(tu_ve=None, tu_len=None, ve_moi_phut=None, gioi_han_mb=None) -> dict:
    kw = {}
    if tu_ve is not None:
        kw["tu_ve"] = bool(tu_ve)
    if tu_len is not None:
        kw["tu_len"] = bool(tu_len)
    if ve_moi_phut is not None:
        kw["ve_moi_phut"] = max(5, min(1440, int(ve_moi_phut)))
    if gioi_han_mb is not None:
        kw["gioi_han_mb"] = max(10, min(20000, int(gioi_han_mb)))
    luu_cau_hinh(**kw)
    return trang_thai()


def _ghi_tt(**kw) -> None:
    with _lock:
        tt = _doc(TEP_TT, {})
        tt.update(kw)
        _ghi(TEP_TT, tt)


# ---------------------------------------------------------------- chép về
def _tai_tep(d: D.Drive, ma: str, dich: Path, xuat_mime: str = "", tong: int = 0) -> int:
    """Tải một tệp Drive về `dich` (qua .part, nối tiếp khi đứt). `tong` là dung lượng Drive báo (0 = không biết, tệp xuất của Google).
    Chỉ coi là xong khi đủ dung lượng: đứt giữa chừng mà thiếu thì nối tiếp, không bao giờ để tệp cụt thành tệp thật."""
    dich.parent.mkdir(parents=True, exist_ok=True)
    part = dich.with_name(dich.name + ".part")
    if part.exists():
        part.unlink()
    if xuat_mime:
        url = D.API + "/files/%s/export?%s" % (urllib.parse.quote(ma), urllib.parse.urlencode({"mimeType": xuat_mime}))
    else:
        url = D.API + "/files/%s?alt=media&supportsAllDrives=true" % urllib.parse.quote(ma)
    da = 0
    loi = None
    for lan in range(6):
        h = {"Authorization": "Bearer " + d.token()}
        if da:
            h["Range"] = "bytes=%d-" % da
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
                if da and r.status != 206:
                    da = 0
                    part.unlink(missing_ok=True)
                cl = r.headers.get("Content-Length")
                co_hieu_luc = int(cl) if cl and cl.isdigit() else None
                moi_nhan = 0
                with open(part, "ab" if da else "wb") as f:
                    while True:
                        buf = r.read(1024 * 1024)
                        if not buf:
                            break
                        f.write(buf)
                        da += len(buf)
                        moi_nhan += len(buf)
            if (tong and da < tong) or (co_hieu_luc is not None and moi_nhan < co_hieu_luc):
                loi = ConnectionError("đứt giữa chừng")
                time.sleep(0.2 * (lan + 1))
                continue
            os.replace(part, dich)
            return da
        except urllib.error.HTTPError as e:
            if e.code == 401:
                d._tok = ""
            elif e.code in (403, 404):
                raise D.LoiDrive("LOI: Drive không cho tải tệp này (%d)." % e.code)
            elif e.code == 416 and tong and da >= tong:
                os.replace(part, dich)
                return da
            loi = e
        except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError) as e:
            loi = e
        time.sleep(0.5 * (2 ** min(lan, 4)))
    part.unlink(missing_ok=True)
    raise D.LoiDrive("LOI: Tải tệp từ Drive không được sau nhiều lần thử (%s)." % type(loi).__name__)


def dong_bo_ve(kho_root: Path, log=print) -> dict:
    """Chép tệp mới hoặc đã đổi trong thư mục Drive làm việc về kho. Không xóa gì."""
    c = cau_hinh()
    lam = c.get("lam_viec")
    if not lam:
        raise D.LoiDrive("LOI: Chưa chọn thư mục Drive làm việc.")
    gh = int(c.get("gioi_han_mb") or 500) * MB
    d = D.Drive()
    dich_goc = Path(kho_root) / NGAN_MAY / ("Google Drive - " + _ten_an_toan(lam.get("ten"), "thu muc"))
    so = _doc(TEP_VE, {})
    kq = {"so_moi": 0, "so_tong": 0, "bo_qua_lon": [], "loi": [], "dung_luong": 0}
    hang = [(lam["id"], Path())]
    dung = 0
    while hang:
        ma_cha, rel = hang.pop()
        for f in d.liet_ke(ma_cha):
            ten = _ten_an_toan(f.get("name"))
            if f.get("mimeType") == D.FOLDER:
                hang.append((f["id"], rel / ten))
                continue
            kq["so_tong"] += 1
            mime = f.get("mimeType") or ""
            xuat = XUAT.get(mime)
            if mime.startswith("application/vnd.google-apps.") and not xuat:
                continue       # biểu mẫu, bản đồ, lối tắt...: không có nội dung tải được
            if xuat and not ten.lower().endswith(xuat[1]):
                ten += xuat[1]
            chu_ky = f.get("md5Checksum") or f.get("modifiedTime") or ""
            cu = so.get(f["id"]) or {}
            dich = dich_goc / rel / ten
            if cu.get("chu_ky") == chu_ky and (dich_goc / cu.get("rel", "")).is_file():
                continue
            kich_thuoc = int(f.get("size") or 0)
            if kich_thuoc > gh:
                kq["bo_qua_lon"].append({"ten": ten, "dung_luong": kich_thuoc})
                continue
            # trùng tên khác tệp: thêm đuôi mã để không đè
            if dich.exists() and cu.get("rel") != str(dich.relative_to(dich_goc)):
                dich = dich.with_name("%s (%s)%s" % (dich.stem, f["id"][:6], dich.suffix))
            try:
                n = _tai_tep(d, f["id"], dich, xuat[0] if xuat else "", 0 if xuat else kich_thuoc)
            except D.LoiDrive as e:
                kq["loi"].append("%s: %s" % (ten, str(e)[:100]))
                continue
            so[f["id"]] = {"ten": ten, "chu_ky": chu_ky, "rel": str(dich.relative_to(dich_goc)), "luc": time.time()}
            kq["so_moi"] += 1
            dung += n
            if kq["so_moi"] % 20 == 0:
                _ghi(TEP_VE, so)
    kq["dung_luong"] = dung
    _ghi(TEP_VE, so)
    if kq["so_moi"]:
        log("Drive: đã chép %d tệp mới về %s" % (kq["so_moi"], dich_goc))
    return kq


# ---------------------------------------------------------------- tải kết quả lên
def _tep_dang_on_dinh(p: Path, chua_doi: float = 60.0) -> bool:
    try:
        return p.is_file() and p.stat().st_size > 0 and time.time() - p.stat().st_mtime >= chua_doi
    except OSError:
        return False


def _duong_tren_drive(rel: Path) -> list[str]:
    """Bỏ hai cấp năm/tháng đầu cho gọn: 2026/2026-11/2026-11-19/1030 viec/tep -> 2026-11-19/1030 viec/tep."""
    p = list(rel.parts)
    if len(p) >= 4 and re.fullmatch(r"\d{4}", p[0]) and re.fullmatch(r"\d{4}-\d{2}", p[1]):
        p = p[2:]
    return [_ten_an_toan(x) for x in p]


def tai_ket_qua_len(office: Path, log=print, chua_doi: float = 60.0) -> dict:
    """Tải tệp kết quả mới trong `03 - Ket qua` của văn phòng AI lên thư mục Drive nhận kết quả."""
    c = cau_hinh()
    kqf = c.get("ket_qua")
    if not kqf:
        raise D.LoiDrive("LOI: Chưa chọn thư mục Drive nhận kết quả.")
    goc = Path(office) / THU_MUC_KET_QUA
    kq = {"so_moi": 0, "loi": [], "gan_nhat": [], "cho_on_dinh": 0}
    if not goc.is_dir():
        return kq
    d = D.Drive()
    so = _doc(TEP_LEN, {})
    cache = {"": kqf["id"]}
    dem = 0
    for p in sorted(goc.rglob("*"), key=lambda x: x.stat().st_mtime if x.exists() else 0):
        try:
            rel = p.relative_to(goc)
        except ValueError:
            continue
        if any(x.startswith(".") for x in rel.parts) or p.name.endswith((".tmp", ".part")) or not p.is_file() or p.is_symlink():
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        khoa = str(rel)
        cu = so.get(khoa) or {}
        if cu.get("size") == st.st_size and cu.get("mtime") == int(st.st_mtime):
            continue
        if cu.get("thu_lai_luc", 0) > time.time():
            continue
        if not _tep_dang_on_dinh(p, chua_doi):
            kq["cho_on_dinh"] += 1
            continue
        if dem >= _TOI_DA_LEN_MOI_LUOT:
            break
        dem += 1
        try:
            cha = kqf["id"]
            duong = _duong_tren_drive(rel)
            for i, thanh in enumerate(duong[:-1]):
                k = "/".join(duong[:i + 1])
                if k not in cache:
                    cache[k] = d.tao_thu_muc(thanh, cha)["id"]
                cha = cache[k]
            r = d.tai_len(str(p), cha, duong[-1])
            so[khoa] = {"size": st.st_size, "mtime": int(st.st_mtime), "id": r.get("id"), "luc": time.time()}
            kq["so_moi"] += 1
            kq["gan_nhat"].append({"ten": duong[-1], "link": r.get("link", "")})
        except D.LoiDrive as e:
            so[khoa] = dict(cu, thu_lai_luc=time.time() + 1800, loi=str(e)[:100])
            kq["loi"].append("%s: %s" % (p.name, str(e)[:100]))
    _ghi(TEP_LEN, so)
    if kq["so_moi"]:
        log("Drive: đã tải %d tệp kết quả lên Drive (%s)" % (kq["so_moi"], kqf.get("ten")))
    return kq


# ---------------------------------------------------------------- nhịp của cầu nối
def _chay_nen(viec: str, ham, tt_key: str, yeu_cau_luc: float) -> None:
    def lam():
        t0 = time.time()
        _ghi_tt(dang_chay=viec)
        try:
            kq = ham()
            kq["loi_chung"] = ""
        except D.LoiDrive as e:
            kq = {"loi_chung": str(e)[:200]}
        except Exception as e:  # noqa: BLE001
            kq = {"loi_chung": "LOI: %s" % type(e).__name__}
        kq.update(luc=time.time(), mat=round(time.time() - t0, 1), yeu_cau_da=yeu_cau_luc)
        _ghi_tt(**{tt_key: kq, "dang_chay": ""})
        _chay["viec"] = None
    _chay["viec"], _chay["t"] = viec, time.time()
    threading.Thread(target=lam, daemon=True, name="tisa-kho-drive-" + viec).start()


_VT = {"t": 0.0, "kho": None, "office": None}


def _duong(kho_root, office):
    """Đường dẫn kho và văn phòng AI. Cầu nối đưa hàm (hỏi bảng, hơi tốn) nên chỉ hỏi lại sau 60 giây."""
    now = time.time()
    if now - _VT["t"] >= 60 or (_VT["kho"] is None and _VT["office"] is None):
        try:
            _VT["kho"] = kho_root() if callable(kho_root) else kho_root
        except Exception:  # noqa: BLE001
            _VT["kho"] = None
        try:
            _VT["office"] = office() if callable(office) else office
        except Exception:  # noqa: BLE001
            _VT["office"] = None
        _VT["t"] = now
    return _VT["kho"], _VT["office"]


def tick(kho_root, office, log=print) -> None:
    """Cầu nối gọi mỗi vài giây. Nhẹ: chỉ xem lịch, việc nặng chạy ở luồng nền, mỗi lần một việc.
    `kho_root` và `office` là đường dẫn hoặc hàm trả đường dẫn."""
    if _chay["viec"] and time.time() - _chay["t"] < 3 * 3600:
        return
    kho, vp = _duong(kho_root, office)
    _ghi_tt(cau_noi_luc=time.time(), kho_may=str(kho or ""))
    if not da_ket_noi():
        return
    c = cau_hinh()
    tt = _doc(TEP_TT, {})
    yc = c.get("yeu_cau") or {}
    now = time.time()
    ve, ln = tt.get("ve") or {}, tt.get("len") or {}
    if kho and c.get("lam_viec"):
        bam = float(yc.get("ve") or 0) > float(ve.get("yeu_cau_da") or 0)
        den_gio = c.get("tu_ve") and now - float(ve.get("luc") or 0) >= int(c.get("ve_moi_phut") or 15) * 60
        if bam or den_gio:
            _chay_nen("ve", lambda: dong_bo_ve(Path(kho), log), "ve", float(yc.get("ve") or 0) if bam else float(ve.get("yeu_cau_da") or 0))
            return
    if vp and c.get("ket_qua"):
        bam = float(yc.get("len") or 0) > float(ln.get("yeu_cau_da") or 0)
        den_gio = c.get("tu_len") and now - float(ln.get("luc") or 0) >= 120
        if bam or den_gio:
            _chay_nen("len", lambda: tai_ket_qua_len(Path(vp), log, 0.0 if bam else 60.0), "len", float(yc.get("len") or 0) if bam else float(ln.get("yeu_cau_da") or 0))


# ---------------------------------------------------------------- đường API cho giao diện
def gan(app) -> None:
    from fastapi import Request
    from fastapi.responses import JSONResponse
    globals()["Request"] = Request      # FastAPI đọc kiểu của tham số từ chuỗi chú thích, phải có ở phạm vi mô-đun

    def loi(e, ma=400):
        return JSONResponse({"ok": False, "error": str(e).replace("LOI: ", "")[:300]}, status_code=ma)

    async def body(request: Request) -> dict:
        try:
            b = await request.json()
            return b if isinstance(b, dict) else {}
        except Exception:  # noqa: BLE001
            return {}

    @app.get("/tisa-kho-drive/api/trang-thai")
    async def _tt():
        t = trang_thai()
        if t["buoc"] == "da_ket_noi" and not t["email"]:
            import asyncio
            t["email"] = await asyncio.to_thread(tai_khoan)
        return t

    @app.post("/tisa-kho-drive/api/client")
    async def _client(request: Request):
        b = await body(request)
        ok, tb = luu_client(b.get("client_id"), b.get("client_secret"))
        return {"ok": ok, "thong_bao": tb} if ok else JSONResponse({"ok": False, "error": tb}, status_code=400)

    @app.post("/tisa-kho-drive/api/dang-nhap")
    async def _dn():
        try:
            return {"ok": True, **dang_nhap()}
        except D.LoiDrive as e:
            return loi(e)

    @app.get("/tisa-kho-drive/api/dang-nhap-xem")
    async def _dnx():
        return {"ok": True, "ket_qua": dang_nhap_xem(), "buoc": trang_thai()["buoc"]}

    @app.post("/tisa-kho-drive/api/ngat")
    async def _ngat():
        return {"ok": True, "da_ngat": ngat_ket_noi()}

    @app.get("/tisa-kho-drive/api/thu-muc")
    async def _tm(cha: str = ""):
        try:
            return {"ok": True, **liet_ke_thu_muc(cha)}
        except D.LoiDrive as e:
            return loi(e)

    @app.post("/tisa-kho-drive/api/phan-giai")
    async def _pg(request: Request):
        try:
            return {"ok": True, **phan_giai((await body(request)).get("lien_ket"))}
        except D.LoiDrive as e:
            return loi(e)

    @app.post("/tisa-kho-drive/api/tao-thu-muc")
    async def _tao(request: Request):
        b = await body(request)
        try:
            return {"ok": True, **tao_thu_muc(b.get("cha"), b.get("ten"))}
        except D.LoiDrive as e:
            return loi(e)

    @app.post("/tisa-kho-drive/api/chon")
    async def _chon(request: Request):
        b = await body(request)
        try:
            return {"ok": True, "thu_muc": chon(b.get("vai_tro"), b.get("id"), b.get("ten"))}
        except D.LoiDrive as e:
            return loi(e)

    @app.post("/tisa-kho-drive/api/cai-dat")
    async def _cd(request: Request):
        b = await body(request)
        try:
            return {"ok": True, **cai_dat(b.get("tu_ve"), b.get("tu_len"), b.get("ve_moi_phut"), b.get("gioi_han_mb"))}
        except (ValueError, TypeError):
            return loi("Giá trị cài đặt không hợp lệ")

    @app.post("/tisa-kho-drive/api/chay")
    async def _chay_api(request: Request):
        b = await body(request)
        try:
            yeu_cau(str(b.get("viec") or ""))
            return {"ok": True, **trang_thai()}
        except D.LoiDrive as e:
            return loi(e)
