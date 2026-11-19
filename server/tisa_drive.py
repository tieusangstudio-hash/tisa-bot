"""tisa_drive.py - Google Drive bằng API thật (không bấm giao diện): liệt kê, đổi tên hàng loạt, tạo thư mục, tải lên file lớn (resumable, có tiếp tục), chia sẻ, lấy link, kiểm số file và dung lượng.

Khóa: JSON {client_id, client_secret, refresh_token} nằm trong macOS Keychain, mục `tisa-bot-drive` (tisa_keychain.py). Không có tệp khóa, không in khóa, không đưa cho AI.
  - Đăng nhập một lần: dang_nhap_bat_dau() mở cổng 127.0.0.1 chờ Google chuyển về; anh bấm Cho phép trên trang Google; mã đổi lấy refresh_token và cất thẳng vào Keychain.
    Cần client_id và client_secret của một OAuth client loại "Desktop app" (mục tisa-bot-drive-client trong Keychain; xem skill dq-ho-tro-ket-noi, phần Google Drive).
  - Quyền xin: https://www.googleapis.com/auth/drive (đọc, ghi, đổi tên, tải lên). Không xóa vĩnh viễn: công cụ này KHÔNG có thao tác xóa.

Tải lên: resumable, mỗi khúc 8 MiB (bội của 256 KiB); đứt giữa chừng thì hỏi Drive đã nhận tới đâu rồi gửi tiếp; địa chỉ phiên được nhớ theo (đường dẫn, dung lượng, giờ sửa)
nên chạy lại sau khi TISA BOT khởi động lại vẫn tiếp tục. Xong thì kiểm dung lượng (và md5) khớp với tệp gốc.
Đổi tên hàng loạt: mặc định CHỈ XEM TRƯỚC (danh sách tên cũ, tên mới); chạy thật ghi tệp hoàn tác dieu-khien-may/drive-hoan-tac-<giờ>.json (chỉ có id và tên, không có khóa).
Chỉ dùng thư viện chuẩn (urllib). Địa chỉ API đổi được bằng biến môi trường TISA_DRIVE_API / TISA_DRIVE_UPLOAD / TISA_DRIVE_TOKEN (kiểm thử dùng máy chủ giả).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "dieu-khien-may"
DICH_VU = "tisa-bot-drive"
DICH_VU_CLIENT = "tisa-bot-drive-client"
API = os.environ.get("TISA_DRIVE_API", "https://www.googleapis.com/drive/v3")
UPLOAD = os.environ.get("TISA_DRIVE_UPLOAD", "https://www.googleapis.com/upload/drive/v3")
TOKEN_URL = os.environ.get("TISA_DRIVE_TOKEN", "https://oauth2.googleapis.com/token")
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPE = "https://www.googleapis.com/auth/drive"
KHUC = 8 * 1024 * 1024           # 32 x 256 KiB
THU_LAI = 6
FOLDER = "application/vnd.google-apps.folder"
_lock = threading.Lock()


class LoiDrive(Exception):
    pass


def _kc():
    import tisa_keychain
    return tisa_keychain


# ---------------------------------------------------------------- khóa
def da_dang_nhap() -> bool:
    try:
        d = json.loads(_kc().doc(DICH_VU) or "{}")
        return bool(d.get("refresh_token") and d.get("client_id"))
    except ValueError:
        return False


def _khoa() -> dict:
    raw = _kc().doc(DICH_VU)
    if not raw:
        raise LoiDrive("CHUA_DANG_NHAP: Chưa nối Google Drive (Keychain chưa có mục %s). Làm theo kỹ năng dq-ho-tro-ket-noi, phần Google Drive." % DICH_VU)
    try:
        d = json.loads(raw)
    except ValueError:
        raise LoiDrive("LOI: Mục %s trong Keychain hỏng." % DICH_VU)
    if not all(d.get(k) for k in ("client_id", "client_secret", "refresh_token")):
        raise LoiDrive("CHUA_DANG_NHAP: Khóa Drive trong Keychain thiếu phần (client_id, client_secret, refresh_token).")
    return d


# ---------------------------------------------------------------- HTTP
def _http(method: str, url: str, headers: dict | None = None, data: bytes | None = None, timeout: int = 60):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read() or b""


class Drive:
    def __init__(self, khoa: dict | None = None):
        self._k = khoa
        self._tok = ""
        self._het = 0.0

    def token(self) -> str:
        if self._tok and time.time() < self._het - 60:
            return self._tok
        k = self._k or _khoa()
        body = urllib.parse.urlencode({"client_id": k["client_id"], "client_secret": k["client_secret"], "refresh_token": k["refresh_token"], "grant_type": "refresh_token"}).encode()
        st, _, raw = _http("POST", TOKEN_URL, {"Content-Type": "application/x-www-form-urlencoded"}, body, 30)
        try:
            d = json.loads(raw or b"{}")
        except ValueError:
            d = {}
        if st != 200 or not d.get("access_token"):
            raise LoiDrive("LOI_DANG_NHAP: Google từ chối làm mới quyền (%s). Có thể anh đã thu hồi quyền hoặc khóa hết hạn: đăng nhập Drive lại." % (d.get("error") or st))
        self._tok, self._het = d["access_token"], time.time() + int(d.get("expires_in") or 3600)
        return self._tok

    def _goi(self, method: str, url: str, *, params=None, body=None, headers=None, data=None, timeout: int = 60):
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        for lan in range(THU_LAI):
            h = {"Authorization": "Bearer " + self.token()}
            h.update(headers or {})
            payload = data
            if body is not None:
                payload = json.dumps(body).encode()
                h["Content-Type"] = "application/json; charset=UTF-8"
            try:
                st, rh, raw = _http(method, url, h, payload, timeout)
            except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
                st, rh, raw = 599, {}, b""
            if st == 401:
                self._tok = ""
                continue
            if st in (429, 500, 502, 503, 504, 599):
                time.sleep(min(0.05 * (2 ** lan), 8))
                continue
            return st, rh, raw
        raise LoiDrive("LOI: Drive không trả lời sau %d lần thử (%s %s)." % (THU_LAI, method, url.split("?")[0][-40:]))

    def _json(self, method, url, **kw):
        st, rh, raw = self._goi(method, url, **kw)
        try:
            d = json.loads(raw or b"{}")
        except ValueError:
            d = {}
        if st >= 400:
            e = (d.get("error") or {})
            raise LoiDrive("LOI: Drive trả %d: %s" % (st, (e.get("message") if isinstance(e, dict) else str(e)) or "không rõ"))
        return d

    # ---- đọc
    def liet_ke(self, cha: str = "root", truy_van: str = "", toi_da: int = 100000) -> list:
        q = "'%s' in parents and trashed = false" % cha.replace("'", "")
        if truy_van:
            q += " and (%s)" % truy_van
        out, tok = [], ""
        while True:
            p = {"q": q, "pageSize": 1000, "fields": "nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime,parents)", "supportsAllDrives": "true", "includeItemsFromAllDrives": "true", "orderBy": "name"}
            if tok:
                p["pageToken"] = tok
            d = self._json("GET", API + "/files", params=p)
            out += d.get("files") or []
            tok = d.get("nextPageToken") or ""
            if not tok or len(out) >= toi_da:
                return out[:toi_da]

    def thong_tin(self, ma: str) -> dict:
        return self._json("GET", API + "/files/" + urllib.parse.quote(ma), params={"fields": "id,name,mimeType,size,md5Checksum,webViewLink,webContentLink,parents", "supportsAllDrives": "true"})

    def dem(self, cha: str, de_quy: bool = True) -> dict:
        """{"so_tep", "so_thu_muc", "dung_luong"} dưới một thư mục."""
        n = t = b = 0
        hang = [cha]
        while hang:
            c = hang.pop()
            for f in self.liet_ke(c):
                if f.get("mimeType") == FOLDER:
                    t += 1
                    if de_quy:
                        hang.append(f["id"])
                else:
                    n += 1
                    b += int(f.get("size") or 0)
        return {"so_tep": n, "so_thu_muc": t, "dung_luong": b}

    # ---- thư mục
    def tao_thu_muc(self, ten: str, cha: str = "root", neu_co_thi_dung: bool = True) -> dict:
        if neu_co_thi_dung:
            for f in self.liet_ke(cha, "name = '%s' and mimeType = '%s'" % (ten.replace("\\", "\\\\").replace("'", "\\'"), FOLDER)):
                return f
        return self._json("POST", API + "/files", params={"fields": "id,name,mimeType,webViewLink", "supportsAllDrives": "true"}, body={"name": ten, "mimeType": FOLDER, "parents": [cha]})

    # ---- đổi tên hàng loạt
    @staticmethod
    def ke_hoach_doi_ten(ds: list, mau: str, thay: str, chi_tep: bool = True) -> list:
        rx = re.compile(mau)
        kq = []
        for f in ds:
            if chi_tep and f.get("mimeType") == FOLDER:
                continue
            moi = rx.sub(thay, f["name"])
            if moi != f["name"] and moi.strip():
                kq.append({"id": f["id"], "cu": f["name"], "moi": moi})
        return kq

    def doi_ten(self, ke_hoach: list, tep_hoan_tac: Path | None = None) -> dict:
        """Chạy kế hoạch; ghi tệp hoàn tác TRƯỚC khi đổi. Trả {"da_doi", "loi": [...]}."""
        if tep_hoan_tac is None:
            DIR.mkdir(parents=True, exist_ok=True)
            tep_hoan_tac = DIR / ("drive-hoan-tac-%s.json" % time.strftime("%Y%m%d-%H%M%S"))
        tep_hoan_tac.write_text(json.dumps([{"id": x["id"], "cu": x["cu"], "moi": x["moi"]} for x in ke_hoach], ensure_ascii=False), encoding="utf-8")
        da, loi = 0, []
        for x in ke_hoach:
            try:
                self._json("PATCH", API + "/files/" + urllib.parse.quote(x["id"]), params={"fields": "id,name", "supportsAllDrives": "true"}, body={"name": x["moi"]})
                da += 1
            except LoiDrive as e:
                loi.append({"id": x["id"], "ly_do": str(e)[:80]})
        return {"da_doi": da, "loi": loi, "tep_hoan_tac": str(tep_hoan_tac)}

    # ---- tải lên (resumable)
    @staticmethod
    def _dau_van_tay(tep: Path, cha: str, ten: str) -> str:
        s = tep.stat()
        return hashlib.sha1(("%s|%d|%d|%s|%s" % (tep.resolve(), s.st_size, int(s.st_mtime), cha, ten)).encode()).hexdigest()[:24]

    def _phien_tep(self) -> Path:
        return DIR / "drive-tai-len-dang-do.json"

    def _doc_phien(self) -> dict:
        try:
            return json.loads(self._phien_tep().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def _ghi_phien(self, d: dict) -> None:
        try:
            DIR.mkdir(parents=True, exist_ok=True)
            self._phien_tep().write_text(json.dumps(d), encoding="utf-8")
        except OSError:
            pass

    def tai_len(self, duong_dan: str, cha: str = "root", ten: str = "", khuc: int = KHUC, tien_do=None) -> dict:
        tep = Path(duong_dan).expanduser()
        if not tep.is_file():
            raise LoiDrive("LOI: không thấy tệp %s" % tep)
        tong = tep.stat().st_size
        ten = ten or tep.name
        # đã có tệp trùng tên và dung lượng ở thư mục đích thì không tải lại
        for f in self.liet_ke(cha, "name = '%s'" % ten.replace("\\", "\\\\").replace("'", "\\'")):
            if f.get("mimeType") != FOLDER and int(f.get("size") or -1) == tong:
                return {"id": f["id"], "ten": f["name"], "dung_luong": tong, "da_co": True, "link": self.thong_tin(f["id"]).get("webViewLink", "")}
        vt = self._dau_van_tay(tep, cha, ten)
        phien = self._doc_phien().get(vt, "")
        da_nhan = 0
        if phien:
            da_nhan = self._hoi_da_nhan(phien, tong)
            if da_nhan is None:
                phien, da_nhan = "", 0
        if not phien:
            st, rh, raw = self._goi("POST", UPLOAD + "/files?uploadType=resumable&supportsAllDrives=true&fields=id,name,size,md5Checksum,webViewLink",
                                    body={"name": ten, "parents": [cha]}, headers={"X-Upload-Content-Length": str(tong)})
            loc = {k.lower(): v for k, v in rh.items()}.get("location", "")
            if st >= 400 or not loc:
                raise LoiDrive("LOI: không mở được phiên tải lên (%d)." % st)
            phien = loc
            d = self._doc_phien()
            d[vt] = phien
            self._ghi_phien(d)
        loi_lien_tiep = 0
        with open(tep, "rb") as f:
            while True:
                f.seek(da_nhan)
                buf = f.read(khuc)
                cuoi = da_nhan + len(buf)
                if tong == 0:
                    cr = "bytes */0"
                else:
                    cr = "bytes %d-%d/%d" % (da_nhan, cuoi - 1, tong)
                try:
                    st, rh, raw = _http("PUT", phien, {"Content-Length": str(len(buf)), "Content-Range": cr, "Authorization": "Bearer " + self.token()}, buf, 120)
                except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
                    st, rh, raw = 599, {}, b""
                if st in (200, 201):
                    kq = json.loads(raw or b"{}")
                    d = self._doc_phien()
                    d.pop(vt, None)
                    self._ghi_phien(d)
                    return self._kiem_sau_tai(tep, kq, tong)
                if st == 308:
                    rng = {k.lower(): v for k, v in rh.items()}.get("range", "")
                    m = re.search(r"bytes=0-(\d+)", rng)
                    da_nhan = int(m.group(1)) + 1 if m else 0
                    loi_lien_tiep = 0
                    if tien_do:
                        tien_do(da_nhan, tong)
                    continue
                loi_lien_tiep += 1
                if st == 404:           # phiên không còn dùng được: bỏ, lần sau mở phiên mới
                    d = self._doc_phien()
                    d.pop(vt, None)
                    self._ghi_phien(d)
                    raise LoiDrive("LOI: phiên tải lên đã hết hạn (404). Chạy lại lệnh để tải lại từ đầu.")
                if loi_lien_tiep > THU_LAI:     # đứt mạng, Drive bận: GIỮ phiên, chạy lại lệnh sẽ tiếp tục đúng chỗ đã nhận
                    raise LoiDrive("LOI: tải lên đứt (mã %d) sau %d lần thử. Phiên được giữ: chạy lại đúng lệnh này để TIẾP TỤC từ chỗ Drive đã nhận." % (st, loi_lien_tiep))
                time.sleep(min(0.05 * (2 ** loi_lien_tiep), 8))
                hoi = self._hoi_da_nhan(phien, tong)
                if hoi is not None:
                    da_nhan = hoi

    def _hoi_da_nhan(self, phien: str, tong: int):
        """Drive đã nhận tới byte nào. None = phiên không còn dùng được."""
        try:
            st, rh, raw = _http("PUT", phien, {"Content-Length": "0", "Content-Range": "bytes */%d" % tong, "Authorization": "Bearer " + self.token()}, b"", 30)
        except (urllib.error.URLError, socket.timeout, ConnectionError, OSError):
            return 0
        if st in (200, 201):
            return tong
        if st == 308:
            m = re.search(r"bytes=0-(\d+)", {k.lower(): v for k, v in rh.items()}.get("range", ""))
            return int(m.group(1)) + 1 if m else 0
        if st == 404:
            return None
        return 0

    def _kiem_sau_tai(self, tep: Path, kq: dict, tong: int) -> dict:
        ma = kq.get("id", "")
        tt = self.thong_tin(ma) if ma else {}
        dl = int(tt.get("size") or kq.get("size") or 0)
        ok_dl = dl == tong
        md5 = tt.get("md5Checksum") or kq.get("md5Checksum") or ""
        ok_md5 = True
        if md5:
            h = hashlib.md5()
            with open(tep, "rb") as f:
                for c in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(c)
            ok_md5 = h.hexdigest() == md5
        return {"id": ma, "ten": tt.get("name") or kq.get("name", ""), "dung_luong": dl, "khop_dung_luong": ok_dl, "khop_md5": ok_md5, "link": tt.get("webViewLink") or kq.get("webViewLink", ""), "da_co": False}

    def tai_thu_muc(self, thu_muc: str, cha: str = "root", tien_do=None) -> dict:
        goc = Path(thu_muc).expanduser()
        if not goc.is_dir():
            raise LoiDrive("LOI: không thấy thư mục %s" % goc)
        ma_goc = self.tao_thu_muc(goc.name, cha)["id"]
        map_ = {goc: ma_goc}
        so_tep = bo_qua = tong_b = 0
        sai = []
        for dg, ds_thu, ds_tep in os.walk(goc):
            dg = Path(dg)
            for t in sorted(ds_thu):
                map_[dg / t] = self.tao_thu_muc(t, map_[dg])["id"]
            for t in sorted(ds_tep):
                if t.startswith("."):
                    continue
                try:
                    r = self.tai_len(str(dg / t), map_[dg])
                    so_tep += 0 if r.get("da_co") else 1
                    bo_qua += 1 if r.get("da_co") else 0
                    tong_b += (dg / t).stat().st_size
                    if r.get("khop_dung_luong") is False or r.get("khop_md5") is False:
                        sai.append(str(dg / t))
                except LoiDrive as e:
                    sai.append("%s: %s" % (dg / t, str(e)[:60]))
        kiem = self.kiem_thu_muc(goc, ma_goc)
        kiem.update({"da_tai": so_tep, "da_co_san": bo_qua, "tep_loi": sai, "id_thu_muc": ma_goc})
        return kiem

    def kiem_thu_muc(self, thu_muc: Path, ma: str) -> dict:
        n = b = 0
        for dg, _, ds_tep in os.walk(thu_muc):
            for t in ds_tep:
                if not t.startswith("."):
                    n += 1
                    b += (Path(dg) / t).stat().st_size
        tren = self.dem(ma)
        return {"may_so_tep": n, "may_dung_luong": b, "drive_so_tep": tren["so_tep"], "drive_dung_luong": tren["dung_luong"], "khop": n == tren["so_tep"] and b == tren["dung_luong"]}

    # ---- chia sẻ, link
    def chia_se(self, ma: str, vai_tro: str = "reader", loai: str = "anyone", email: str = "") -> dict:
        if vai_tro not in ("reader", "commenter", "writer"):
            raise LoiDrive("LOI: vai_tro chỉ nhận reader, commenter, writer.")
        body = {"role": vai_tro, "type": loai}
        if loai == "user":
            if not email:
                raise LoiDrive("LOI: thiếu email.")
            body["emailAddress"] = email
        self._json("POST", API + "/files/%s/permissions" % urllib.parse.quote(ma), params={"supportsAllDrives": "true", "sendNotificationEmail": "false"}, body=body)
        return self.lay_link(ma)

    def lay_link(self, ma: str) -> dict:
        t = self.thong_tin(ma)
        return {"id": ma, "ten": t.get("name"), "link": t.get("webViewLink", ""), "link_tai": t.get("webContentLink", "")}


# ---------------------------------------------------------------- đăng nhập một lần (loopback OAuth, khóa đi thẳng vào Keychain)
_dn = {"may_chu": None, "ket_qua": "", "thread": None, "tt": ""}


def dang_nhap_bat_dau(client_id: str = "", client_secret: str = "", chuyen_huong_cong: int = 0, tgian_cho: int = 300) -> dict:
    """Mở cổng 127.0.0.1 chờ Google chuyển về. Trả {"url": ...} để mở trong trình duyệt của anh (anh bấm Cho phép). Khi xong refresh_token vào Keychain."""
    kc = _kc()
    if not client_id:
        raw = kc.doc(DICH_VU_CLIENT)
        try:
            c = json.loads(raw or "{}")
        except ValueError:
            c = {}
        client_id, client_secret = c.get("client_id", ""), c.get("client_secret", "")
    if not client_id or not client_secret:
        raise LoiDrive("THIEU_CLIENT: Chưa có OAuth client (client_id, client_secret) của Google Drive trong Keychain mục %s. Xem dq-ho-tro-ket-noi." % DICH_VU_CLIENT)
    state = hashlib.sha1(os.urandom(16)).hexdigest()[:20]

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # noqa: D401
            pass

        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            ok = False
            if q.get("state", [""])[0] == state and q.get("code"):
                body = urllib.parse.urlencode({"code": q["code"][0], "client_id": client_id, "client_secret": client_secret,
                                               "redirect_uri": "http://127.0.0.1:%d" % self.server.server_port, "grant_type": "authorization_code"}).encode()
                st, _, raw = _http("POST", TOKEN_URL, {"Content-Type": "application/x-www-form-urlencoded"}, body, 30)
                try:
                    d = json.loads(raw or b"{}")
                except ValueError:
                    d = {}
                if st == 200 and d.get("refresh_token"):
                    ok = kc.luu(DICH_VU, json.dumps({"client_id": client_id, "client_secret": client_secret, "refresh_token": d["refresh_token"]}))
                _dn["ket_qua"] = "ok" if ok else "that_bai"
            else:
                _dn["ket_qua"] = "that_bai"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(("<h3>%s</h3>" % ("Xong. Anh quay lại TISA BOT." if ok else "Chưa nối được, quay lại TISA BOT xem lý do.")).encode())

    sv = HTTPServer(("127.0.0.1", chuyen_huong_cong), H)
    port = sv.server_port
    _dn.update({"may_chu": sv, "ket_qua": "cho"})

    def chay():
        sv.timeout = 1.0
        t0 = time.time()
        while _dn["ket_qua"] == "cho" and time.time() - t0 < tgian_cho:
            sv.handle_request()
        if _dn["ket_qua"] == "cho":
            _dn["ket_qua"] = "het_gio"
        sv.server_close()

    th = threading.Thread(target=chay, daemon=True, name="tisa-drive-dn")
    th.start()
    _dn["thread"] = th
    url = AUTH_URL + "?" + urllib.parse.urlencode({"client_id": client_id, "redirect_uri": "http://127.0.0.1:%d" % port, "response_type": "code", "scope": SCOPE,
                                                    "access_type": "offline", "prompt": "consent", "state": state})
    return {"url": url, "cong": port}


def dang_nhap_trang_thai() -> str:
    return _dn["ket_qua"] or "chua_bat_dau"


# ---------------------------------------------------------------- công cụ cho hub: tisa_drive_do
TEP_NK = DIR / "drive-nhat-ky.jsonl"
_OP_DOC = ("trang_thai", "liet_ke", "lay_link", "kiem", "dang_nhap_xem", "thu_muc_kho")
_OP_VIEC_NEN_DUOC = ("trang_thai", "liet_ke", "lay_link", "kiem", "tai_len", "tai_thu_muc", "tao_thu_muc", "thu_muc_kho", "dong_bo_kho")


def _nk(kenh: str, op: str, kq: str, tom_tat: str = "") -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        with open(TEP_NK, "a", encoding="utf-8") as f:
            f.write(json.dumps({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "kenh": kenh[:40], "op": op, "ket_qua": kq[:40], "tom_tat": tom_tat[:120]}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _duyet(a: dict, op: str, mo_ta: str):
    """None = được làm; chuỗi CAN_DUYET = chờ anh bấm Duyệt (trừ khi đang Toàn quyền)."""
    try:
        import tisa_desktop as D
        import tisa_browser as B
    except Exception:  # noqa: BLE001
        return "LOI: thiếu mô-đun duyệt."
    if D.muc_hien_tai() == "toan_quyen":
        return None
    nc = {"host": "Google Drive", "url": "", "tag": "", "ten": ("%s: %s" % (op, mo_ta))[:100], "tieu_de": "drive"}
    if B.dung_duyet(str(a.get("duyet_id") or ""), "drive_" + op, nc):
        return None
    k = B.xin_duyet("drive_" + op, nc, mo_ta)
    return "CAN_DUYET: %s. Anh phải bấm Duyệt trong TISA BOT. Nói rõ với anh rồi gọi lại đúng lệnh này với duyet_id=\"%s\" sau khi anh duyệt. Chưa duyệt thì KHÔNG làm." % (mo_ta, k)


def _tom(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False)[:1800]


def thuc_hien(a: dict, turn) -> str:
    op = str(a.get("op") or "trang_thai").lower()
    import tisa_mo_khoa as MK
    ok, kenh, ly = MK.kiem_kenh(turn)
    if not ok:
        viec_nen = isinstance(turn, dict) and str(turn.get("job") or "").startswith("kanban:") and not turn.get("bot_id") and not turn.get("agent")
        if viec_nen and op in _OP_VIEC_NEN_DUOC:
            kenh = "việc nền " + str(turn.get("job"))[:30]
        else:
            _nk(kenh, op, "từ chối", ly[:80])
            return "TU_CHOI: Thao tác Drive này chỉ làm khi chính anh nhắn từ dashboard TISA BOT hoặc Zalo của anh (việc nền do anh giao chỉ được tải lên, liệt kê, kiểm, lấy link). %s" % ly
    try:
        if op == "trang_thai":
            return _tom({"da_dang_nhap": da_dang_nhap(), "co_oauth_client": _kc().co(DICH_VU_CLIENT), "nhat_ky": TEP_NK.name})
        if op == "dang_nhap":
            k = _duyet(a, "dang_nhap", "Cho TISA BOT quyền đọc và ghi Google Drive của anh (OAuth, khóa cất trong Keychain)")
            if k:
                return k
            r = dang_nhap_bat_dau()
            _nk(kenh, op, "bắt đầu")
            return ("Mở địa chỉ này trong trình duyệt anh đã chọn (dùng tisa_browser_do op=hoi_mo rồi để anh bấm Cho phép; gặp Touch ID/mã khóa thì op=cho_nguoi_that): %s\n"
                    "Xong gọi tisa_drive_do op=dang_nhap_xem. Khóa tự vào Keychain, không hiện ra đây." % r["url"])
        if op == "dang_nhap_xem":
            return {"ok": "Đã nối Google Drive (khóa nằm trong Keychain).", "cho": "Đang chờ anh bấm Cho phép trên trang Google.", "that_bai": "Chưa nối được: Google không trả mã hoặc mã sai. Gọi op=dang_nhap làm lại.",
                    "het_gio": "Hết giờ chờ. Gọi op=dang_nhap làm lại.", "chua_bat_dau": "Chưa bắt đầu đăng nhập."}.get(dang_nhap_trang_thai(), dang_nhap_trang_thai())
        if op in ("thu_muc_kho", "dong_bo_kho"):
            import tisa_kho_drive as KD       # Kho tư liệu nối Drive (V3.34): thư mục chủ đã chọn trong trang Kho tư liệu
            if op == "thu_muc_kho":
                c = KD.cau_hinh()
                return _tom({"da_dang_nhap": da_dang_nhap(), "thu_muc_lam_viec": c.get("lam_viec"), "thu_muc_nhan_ket_qua": c.get("ket_qua"),
                             "tu_dong_chep_ve": bool(c.get("tu_ve")), "tu_dong_tai_len": bool(c.get("tu_len")),
                             "ghi_chu": "Tải kết quả lên thư mục nhận kết quả bằng tai_len/tai_thu_muc với cha=<id thư mục>. Tư liệu từ thư mục làm việc đã được chép về Kho tư liệu trên máy (ngăn 12), đọc ở đó."})
            if not da_dang_nhap():
                return "CHUA_DANG_NHAP: Chưa nối Google Drive. Chủ nối ở trang Kho tư liệu (nút Kết nối Drive) hoặc làm theo dq-ho-tro-ket-noi."
            viec = str(a.get("viec") or "ve").lower()
            KD.yeu_cau(viec)
            _nk(kenh, op, "ok", viec)
            return "Đã gửi lệnh đồng bộ (%s). Cầu nối Đội Quân AI chạy trong vài giây; xem kết quả ở trang Kho tư liệu." % ("chép từ Drive về kho" if viec == "ve" else "tải kết quả lên Drive")
        d = Drive()
        if op == "liet_ke":
            ds = d.liet_ke(str(a.get("thu_muc") or "root"), str(a.get("truy_van") or ""), int(a.get("toi_da") or 200))
            _nk(kenh, op, "ok", "%d mục" % len(ds))
            return _tom({"so_muc": len(ds), "muc": [{"id": f["id"], "ten": f["name"], "loai": "thu_muc" if f.get("mimeType") == FOLDER else "tep", "dung_luong": int(f.get("size") or 0)} for f in ds[:200]]})
        if op == "doi_ten":
            ds = d.liet_ke(str(a.get("thu_muc") or "root"))
            kh = d.ke_hoach_doi_ten(ds, str(a.get("mau") or ""), str(a.get("thay") or ""), not a.get("ca_thu_muc"))
            if not a.get("chay"):
                _nk(kenh, op, "xem trước", "%d tên sẽ đổi" % len(kh))
                return _tom({"che_do": "XEM TRƯỚC (chưa đổi gì)", "se_doi": len(kh), "tong_tep": len(ds), "mau_xem": kh[:15], "de_chay_that": "gọi lại với chay=true (cần anh duyệt)"})
            k = _duyet(a, "doi_ten", "Đổi tên %d tệp trong Drive (có tệp hoàn tác)" % len(kh))
            if k:
                return k
            r = d.doi_ten(kh)
            _nk(kenh, op, "ok" if not r["loi"] else "một phần", "đổi %d, lỗi %d" % (r["da_doi"], len(r["loi"])))
            sau = d.liet_ke(str(a.get("thu_muc") or "root"))
            r["kiem_sau"] = {"so_muc_truoc": len(ds), "so_muc_sau": len(sau), "con_khop_mau": sum(1 for f in sau if re.search(str(a.get("mau") or "$^"), f["name"]) and f["name"] != re.sub(str(a.get("mau") or ""), str(a.get("thay") or ""), f["name"]))}
            return _tom(r)
        if op == "tao_thu_muc":
            f = d.tao_thu_muc(str(a.get("ten") or ""), str(a.get("cha") or "root"))
            _nk(kenh, op, "ok")
            return _tom({"id": f["id"], "ten": f["name"], "link": f.get("webViewLink", "")})
        if op == "tai_len":
            r = d.tai_len(str(a.get("duong_dan") or ""), str(a.get("cha") or "root"), str(a.get("ten") or ""))
            _nk(kenh, op, "ok" if r.get("khop_dung_luong", True) else "lệch", "%d byte" % r.get("dung_luong", 0))
            return _tom(r)
        if op == "tai_thu_muc":
            r = d.tai_thu_muc(str(a.get("duong_dan") or ""), str(a.get("cha") or "root"))
            _nk(kenh, op, "khớp" if r.get("khop") else "lệch", "%d tệp, %d byte" % (r.get("may_so_tep", 0), r.get("may_dung_luong", 0)))
            return _tom(r)
        if op == "kiem":
            r = d.kiem_thu_muc(Path(str(a.get("duong_dan") or "")).expanduser(), str(a.get("thu_muc") or "")) if a.get("duong_dan") else d.dem(str(a.get("thu_muc") or "root"))
            return _tom(r)
        if op == "lay_link":
            return _tom(d.lay_link(str(a.get("ma") or "")))
        if op == "chia_se":
            loai = str(a.get("loai") or "anyone")
            k = _duyet(a, "chia_se", "Chia sẻ tệp Drive %s với %s (%s)" % (str(a.get("ma") or "")[:12], "BẤT KỲ AI CÓ LINK" if loai == "anyone" else str(a.get("email") or "một người"), a.get("vai_tro") or "reader"))
            if k:
                return k
            r = d.chia_se(str(a.get("ma") or ""), str(a.get("vai_tro") or "reader"), loai, str(a.get("email") or ""))
            _nk(kenh, op, "ok", loai)
            return _tom(r)
        return "LOI: op của tisa_drive_do: trang_thai, dang_nhap, dang_nhap_xem, liet_ke, doi_ten, tao_thu_muc, tai_len, tai_thu_muc, kiem, lay_link, chia_se, thu_muc_kho, dong_bo_kho."
    except LoiDrive as e:
        _nk(kenh, op, "lỗi", str(e)[:100])
        return str(e)
    except Exception as e:  # noqa: BLE001
        _nk(kenh, op, "lỗi", type(e).__name__)
        return "LOI: %s" % type(e).__name__


def dang_ky_hub(add, vault_root=None) -> None:
    import asyncio

    async def _lam(args):
        try:
            import turn_context
            turn = turn_context.current()
        except Exception:  # noqa: BLE001
            turn = None
        return await asyncio.to_thread(thuc_hien, args or {}, turn)

    add("tisa_drive_do",
        "Làm việc với Google Drive của anh BẰNG API (nhanh, không bấm giao diện): op=trang_thai; op=dang_nhap / dang_nhap_xem (nối Drive một lần, khóa cất vào Keychain); "
        "op=liet_ke thu_muc [truy_van]; op=doi_ten thu_muc mau=<regex> thay=<chuỗi> [chay=true] (mặc định chỉ XEM TRƯỚC, chạy thật cần anh duyệt, có tệp hoàn tác); "
        "op=tao_thu_muc ten [cha]; op=tai_len duong_dan [cha] [ten] (tệp lớn, resumable, tự tiếp tục, kiểm dung lượng + md5); op=tai_thu_muc duong_dan [cha]; "
        "op=kiem thu_muc [duong_dan] (đếm tệp và dung lượng); op=lay_link ma; op=chia_se ma [vai_tro] [loai=anyone|user] [email] (cần anh duyệt). KHÔNG có thao tác xóa. "
        "Khóa không bao giờ hiện ra. Làm theo kỹ năng dq-ho-tro-ket-noi (phần Google Drive).",
        {"op": {"type": "string"}, "thu_muc": {"type": "string"}, "cha": {"type": "string"}, "ten": {"type": "string"}, "mau": {"type": "string"}, "thay": {"type": "string"},
         "chay": {"type": "boolean"}, "duong_dan": {"type": "string"}, "ma": {"type": "string"}, "vai_tro": {"type": "string"}, "loai": {"type": "string"}, "email": {"type": "string"},
         "truy_van": {"type": "string"}, "toi_da": {"type": "integer"}, "ca_thu_muc": {"type": "boolean"}, "duyet_id": {"type": "string"}},
        ["op"], _lam, effect="write")
