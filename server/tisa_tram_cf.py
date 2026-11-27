"""tisa_tram_cf.py - dựng Trạm TISA lên Cloudflare của chính chủ bằng MỘT token API (bản thử Nhiều máy, 21/11/2026).

Người dùng chỉ dán token (tạo theo đường dẫn mẫu bên dưới). Mô-đun tự:
  1. tìm tài khoản Cloudflare,
  2. tạo cơ sở dữ liệu D1 `tram-tisa` (có rồi thì dùng lại),
  3. tạo kho R2 `tram-tisa-kho` (có rồi thì dùng lại; tài khoản chưa bật R2 thì báo cách bật),
  4. đưa mã Worker `tram-tisa` (tram/tram-tisa.js) lên kèm D1, R2 và khóa dựng Trạm (secret QUAN_TRI do máy sinh ngẫu nhiên),
  5. bật địa chỉ miễn phí https://tram-tisa.<tên-tài-khoản>.workers.dev,
  6. (tùy chọn) gắn một tên miền con riêng, ví dụ tisa.tenmien.com, vào Worker.
Token KHÔNG được lưu ở đâu: dùng xong là bỏ. Muốn cập nhật mã Trạm sau này thì dán token lần nữa.
Không đụng DNS đang có: tên miền con phải chưa được dùng (Cloudflare tự tạo bản ghi cho Worker).
"""
from __future__ import annotations

import json
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.cloudflare.com/client/v4"
TEN_WORKER = "tram-tisa"
TEN_D1 = "tram-tisa"
TEN_R2 = "tram-tisa-kho"
MA_WORKER = Path(__file__).resolve().parent.parent / "tram" / "tram-tisa.js"
NGAY_TUONG_THICH = "2025-01-01"

# Đường dẫn mở sẵn trang tạo token với đúng quyền cần (Cloudflare điền sẵn các quyền theo tham số permissionGroupKeys).
_QUYEN = [{"key": "workers_scripts", "type": "edit"}, {"key": "d1", "type": "edit"}, {"key": "workers_r2", "type": "edit"},
          {"key": "account_settings", "type": "read"}, {"key": "workers_routes", "type": "edit"}, {"key": "zone", "type": "read"},
          {"key": "dns", "type": "edit"}]
LINK_TAO_TOKEN = ("https://dash.cloudflare.com/profile/api-tokens?permissionGroupKeys="
                  + urllib.parse.quote(json.dumps(_QUYEN, separators=(",", ":"))) + "&name=" + urllib.parse.quote("TISA Tram"))
HUONG_DAN_TOKEN = ("Mở đường dẫn, Cloudflare điền sẵn quyền: Workers Scripts (sửa), D1 (sửa), Workers R2 Storage (sửa), Account Settings (đọc), "
                   "Workers Routes, Zone, DNS (để gắn tên miền riêng, có thể bỏ). Chọn tài khoản của anh ở mục Account Resources, "
                   "bấm Continue to summary rồi Create Token, chép token dán vào đây.")


class LoiCF(Exception):
    pass


class CF:
    def __init__(self, token: str, api: str = API):
        self.token = (token or "").strip()
        self.api = api.rstrip("/")
        if not re.fullmatch(r"[A-Za-z0-9_\-]{30,200}", self.token):
            raise LoiCF("Token Cloudflare không đúng dạng. Chép lại nguyên token (một dòng chữ dài) ở bước Create Token.")

    def goi(self, method: str, path: str, body=None, raw: bytes = None, content_type: str = None, cho_phep=()):
        h = {"Authorization": "Bearer " + self.token, "User-Agent": "tisa-bot"}
        data = None
        if raw is not None:
            data = raw
            h["Content-Type"] = content_type or "application/octet-stream"
        elif body is not None:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
        req = urllib.request.Request(self.api + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            try:
                d = json.loads(e.read().decode() or "{}")
            except ValueError:
                d = {"success": False, "errors": [{"code": e.code, "message": str(e)}]}
        except urllib.error.URLError as e:
            raise LoiCF(f"Không kết nối được Cloudflare: {e.reason}")
        if d.get("success") is False:
            loi = d.get("errors") or [{}]
            ma = {int(x.get("code") or 0) for x in loi}
            if ma & set(cho_phep):
                return d
            raise LoiCF(_dich_loi(loi))
        return d


def _dich_loi(loi: list) -> str:
    x = loi[0] if loi else {}
    ma, chu = int(x.get("code") or 0), str(x.get("message") or "")
    if ma in (10000, 9109, 6003, 6111) or "Authentication" in chu:
        return "Token sai hoặc thiếu quyền. Tạo lại token theo đường dẫn mẫu (đủ quyền Workers, D1, R2) rồi dán lại."
    if ma == 10042 or "enable R2" in chu:
        return ("Tài khoản Cloudflare chưa bật R2. Vào dash.cloudflare.com, mục R2 Object Storage, bấm bật (gói miễn phí 10 GB, Cloudflare có thể đòi thêm thẻ), "
                "rồi bấm Dựng Trạm lần nữa.")
    return f"Cloudflare báo lỗi {ma}: {chu[:200]}"


def tai_khoan(cf: CF) -> dict:
    d = cf.goi("GET", "/accounts?per_page=50")
    ds = d.get("result") or []
    if not ds:
        raise LoiCF("Token không thấy tài khoản Cloudflare nào. Ở bước tạo token, mục Account Resources hãy chọn tài khoản của anh.")
    return ds[0]


def ten_trong(cf: CF, acc: str) -> str:
    """Tên Worker cho Trạm MỚI (27/11/2026). Tài khoản Cloudflare đã có Trạm `tram-tisa` (ví dụ nhóm máy chạy bản khác của cùng chủ)
    thì dựng Trạm mới là `tram-tisa-2`, `tram-tisa-3`...: dựng đè lên sẽ thay mã và khóa của Trạm đang chạy, các máy đang nối vào đó mất kết nối,
    và hai nhóm máy dùng chung một cơ sở dữ liệu."""
    d = cf.goi("GET", f"/accounts/{acc}/workers/scripts")
    co = {str(x.get("id") or "") for x in (d.get("result") or [])}
    for i in range(1, 10):
        ten = TEN_WORKER if i == 1 else f"{TEN_WORKER}-{i}"
        if ten not in co:
            return ten
    raise LoiCF("Tài khoản Cloudflare đã có 9 Trạm TISA. Xóa bớt Worker tram-tisa-... không dùng rồi dựng lại.")


def _ten_phu(ten: str) -> tuple:
    """(tên D1, tên kho R2) đi theo tên Worker: tram-tisa giữ tên cũ, tram-tisa-2 dùng tram-tisa-2 và tram-tisa-2-kho."""
    return (TEN_D1, TEN_R2) if ten == TEN_WORKER else (ten, ten + "-kho")


def _d1(cf: CF, acc: str, ten_d1: str = TEN_D1) -> str:
    d = cf.goi("GET", f"/accounts/{acc}/d1/database?name={ten_d1}")
    for x in d.get("result") or []:
        if x.get("name") == ten_d1:
            return x["uuid"]
    d = cf.goi("POST", f"/accounts/{acc}/d1/database", {"name": ten_d1})
    return d["result"]["uuid"]


def _r2(cf: CF, acc: str, ten_r2: str = TEN_R2) -> None:
    cf.goi("POST", f"/accounts/{acc}/r2/buckets", {"name": ten_r2}, cho_phep=(10004,))   # 10004: đã có kho cùng tên


def _subdomain(cf: CF, acc: str) -> str:
    d = cf.goi("GET", f"/accounts/{acc}/workers/subdomain", cho_phep=(10007,))
    sd = ((d.get("result") or {}) if d.get("success") is not False else {}).get("subdomain")
    if sd:
        return sd
    ten = "tisa-" + secrets.token_hex(3)
    d = cf.goi("PUT", f"/accounts/{acc}/workers/subdomain", {"subdomain": ten})
    return (d.get("result") or {}).get("subdomain") or ten


def _multipart(phan: list) -> tuple:
    bd = "----tisa" + secrets.token_hex(8)
    out = b""
    for ten, ten_tep, kieu, du_lieu in phan:
        out += f"--{bd}\r\nContent-Disposition: form-data; name=\"{ten}\"".encode()
        if ten_tep:
            out += f"; filename=\"{ten_tep}\"".encode()
        out += f"\r\nContent-Type: {kieu}\r\n\r\n".encode() + du_lieu + b"\r\n"
    out += f"--{bd}--\r\n".encode()
    return out, f"multipart/form-data; boundary={bd}"


def dua_ma(cf: CF, acc: str, d1: str, quan_tri: str, ten: str = TEN_WORKER) -> None:
    ma = MA_WORKER.read_bytes()
    meta = {"main_module": "tram-tisa.js", "compatibility_date": NGAY_TUONG_THICH,
            "bindings": [{"type": "d1", "name": "DB", "id": d1},
                         {"type": "r2_bucket", "name": "KHO", "bucket_name": _ten_phu(ten)[1]},
                         {"type": "secret_text", "name": "QUAN_TRI", "text": quan_tri}]}
    body, ct = _multipart([("metadata", "", "application/json", json.dumps(meta).encode()),
                           ("tram-tisa.js", "tram-tisa.js", "application/javascript+module", ma)])
    cf.goi("PUT", f"/accounts/{acc}/workers/scripts/{ten}", raw=body, content_type=ct)
    cf.goi("POST", f"/accounts/{acc}/workers/scripts/{ten}/subdomain", {"enabled": True, "previews_enabled": False})


def gan_ten_mien(cf: CF, acc: str, ten_mien: str, ten: str = TEN_WORKER) -> str:
    h = (ten_mien or "").strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
    if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+){2,}", h):
        raise LoiCF("Tên miền riêng phải là một tên miền con, ví dụ tisa.tenmien.com.")
    goc = ".".join(h.split(".")[-2:])
    z = cf.goi("GET", f"/zones?name={goc}")
    zs = z.get("result") or []
    if not zs:
        raise LoiCF(f"Không thấy tên miền {goc} trong Cloudflare của anh (hoặc token chưa có quyền Zone).")
    d = cf.goi("GET", f"/zones/{zs[0]['id']}/dns_records?name={h}")
    if d.get("result"):
        raise LoiCF(f"{h} đang được dùng (đã có bản ghi DNS). Chọn một tên miền con khác chưa dùng, Trạm không ghi đè bản ghi đang chạy.")
    cf.goi("PUT", f"/accounts/{acc}/workers/domains", {"environment": "production", "hostname": h, "service": ten, "zone_id": zs[0]["id"]})
    return "https://" + h


def dung(token: str, ten_mien: str = "", quan_tri: str = "", bao=None, api: str = API, ten: str = "") -> dict:
    """Dựng (hoặc cập nhật) Trạm. Trả {tram, quan_tri, ten_mien}. `quan_tri` rỗng thì sinh mới (lần đầu)."""
    def b(pt, chu):
        if bao:
            bao(pt, chu)
    cf = CF(token, api)
    b(5, "Đang tìm tài khoản Cloudflare...")
    acc = tai_khoan(cf)["id"]
    # Trạm mới (chưa có khóa dựng) thì chọn tên chưa ai dùng; cập nhật Trạm cũ (có khóa) thì giữ tên đã truyền vào.
    ten = (ten or TEN_WORKER) if quan_tri else ten_trong(cf, acc)
    ten_d1, ten_r2 = _ten_phu(ten)
    b(20, "Đang tạo cơ sở dữ liệu D1...")
    d1 = _d1(cf, acc, ten_d1)
    b(40, "Đang tạo kho R2...")
    _r2(cf, acc, ten_r2)
    quan_tri = quan_tri or secrets.token_urlsafe(32)
    b(60, "Đang đưa Trạm lên Cloudflare" + ("" if ten == TEN_WORKER else f" (tên {ten}, vì tài khoản đã có Trạm khác)") + "...")
    dua_ma(cf, acc, d1, quan_tri, ten)
    b(80, "Đang bật địa chỉ workers.dev...")
    sd = _subdomain(cf, acc)
    tram = f"https://{ten}.{sd}.workers.dev"
    rieng = ""
    if ten_mien:
        b(90, "Đang gắn tên miền riêng...")
        rieng = gan_ten_mien(cf, acc, ten_mien, ten)
    b(100, "Xong")
    return {"tram": rieng or tram, "tram_workers_dev": tram, "quan_tri": quan_tri, "ten_mien": rieng, "ten_worker": ten}
