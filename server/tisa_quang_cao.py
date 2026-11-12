"""tisa_quang_cao.py - trang Quảng Cáo của TISA BOT (V2.78): quản lý tài khoản quảng cáo Facebook, TikTok, Google Ads,
bảng số liệu gộp một chỗ, kiểm tra kết nối, gợi ý tối ưu và phiếu thiết lập quảng cáo.

Thiết kế (rút từ cách các bảng điều khiển quảng cáo và máy chủ MCP quảng cáo đang làm):
  - MỘT công thức cho mọi nền tảng: CTR = bấm / hiển thị, CPC = chi phí / bấm, CPA = chi phí / kết quả, ROAS = doanh thu / chi phí.
    Số trên trang là số TISA BOT tự tính lại từ số thô của từng nền tảng, nên đặt cạnh nhau so sánh được.
  - Hàng trên cùng chỉ có 4 số quan trọng: chi phí, kết quả, CPA (đặt cạnh mục tiêu), doanh thu / ROAS; kèm % so với kỳ trước.
  - CHỈ ĐỌC. Trang không tạo, sửa, bật quảng cáo hay tiêu tiền. Việc tạo chiến dịch đi qua trợ lý (skill + MCP), luôn ở trạng
    thái tạm dừng và chờ chủ duyệt, giống rào chặn của tisa_quyen_qc.py.
  - Hai đường nối: API trực tiếp (token của chủ, mã hoá bằng secrets_store) và MCP (Kết nối trong TISA BOT).
  - Chưa nối tài khoản nào thì có chế độ dữ liệu mẫu (ghi rõ "Dữ liệu mẫu") để xem trước giao diện.

Đường dẫn: /tisa-quang-cao/ (trang) và /tisa-quang-cao/api/... (dữ liệu). Mọi đường dẫn nằm sau đăng nhập TISA BOT.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:   # phải đứng ở đầu tệp: FastAPI đọc chú thích kiểu theo tên toàn cục
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

ROOT = Path(__file__).resolve().parent.parent
try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
KHO = STATE_DIR / "quang-cao"
TEP_TK = KHO / "tai-khoan.json"

# Địa chỉ gốc có thể đổi bằng biến môi trường (dùng để thử bằng máy chủ giả, không gọi nền tảng thật).
FB_GOC = os.getenv("TISA_QC_FB_GOC", "https://graph.facebook.com")
TT_GOC = os.getenv("TISA_QC_TT_GOC", "https://business-api.tiktok.com")
GG_GOC = os.getenv("TISA_QC_GG_GOC", "https://googleads.googleapis.com")
GG_TOKEN = os.getenv("TISA_QC_GG_TOKEN", "https://oauth2.googleapis.com/token")
FB_PHIEN_BAN = "v25.0"
GG_PHIEN_BAN = "v23"

NEN = {"facebook": "Facebook / Meta", "tiktok": "TikTok", "google": "Google Ads"}
# Ô nhập cho từng nền tảng: (khoá, nhãn, là bí mật, gợi ý)
TRUONG = {
    "facebook": [("ma_tk", "Mã tài khoản quảng cáo", False, "Dạng act_1234567890 hoặc chỉ dãy số"),
                 ("token", "Mã truy cập (access token)", True, "Quyền ads_read. Nên dùng mã của System User, dùng lâu dài")],
    "tiktok": [("ma_tk", "Mã nhà quảng cáo (Advertiser ID)", False, "Dãy số trong TikTok Ads Manager"),
               ("token", "Mã truy cập (Access Token)", True, "Lấy từ app trên TikTok for Business")],
    "google": [("ma_tk", "Mã khách hàng (Customer ID)", False, "10 số, có hoặc không có dấu gạch"),
               ("developer_token", "Developer token", True, "Lấy ở Google Ads, mục API Center"),
               ("client_id", "OAuth client ID", True, "Tạo trong Google Cloud, loại ứng dụng máy tính"),
               ("client_secret", "OAuth client secret", True, ""),
               ("refresh_token", "Refresh token", True, "Mã làm mới đăng nhập của tài khoản có quyền"),
               ("login_customer_id", "Mã tài khoản quản lý (MCC), nếu có", False, "Bỏ trống nếu truy cập trực tiếp")],
}
KHOA_BI_MAT = {k for ds in TRUONG.values() for k, _, bm, _ in ds if bm}

_khoa = threading.RLock()
_nho: dict = {}          # khoá -> (giờ, dữ liệu): bộ nhớ đệm số liệu thật
NHO_GIAY = 600


# ---------------------------------------------------------------- kho tài khoản
def _doc_tk() -> dict:
    try:
        d = json.loads(TEP_TK.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            d.setdefault("tai_khoan", [])
            d.setdefault("chung", {})
            return d
    except (OSError, ValueError):
        pass
    return {"tai_khoan": [], "chung": {}}


def _ghi(tep: Path, d) -> None:
    KHO.mkdir(parents=True, exist_ok=True)
    tam = tep.with_suffix(".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, tep)
    try:
        os.chmod(tep, 0o600)
    except OSError:
        pass


def _ma_hoa(v: str) -> str:
    try:
        import secrets_store
        return secrets_store.encrypt(v)
    except Exception:  # noqa: BLE001
        return "plain:" + v


def _giai_ma(v: str) -> str:
    try:
        import secrets_store
        return secrets_store.decrypt(v)
    except Exception:  # noqa: BLE001
        return v[6:] if str(v).startswith("plain:") else str(v)


def _bi_mat(tk: dict) -> dict:
    return {k: _giai_ma(v) for k, v in (tk.get("bi_mat") or {}).items()}


def _cong_khai(tk: dict) -> dict:
    """Bản trả ra trình duyệt: không bao giờ kèm giá trị bí mật, chỉ cho biết đã nhập hay chưa."""
    return {"id": tk["id"], "nen": tk["nen"], "ten": tk.get("ten") or "", "ma_tk": tk.get("ma_tk") or "",
            "da_nhap": sorted((tk.get("bi_mat") or {}).keys()), "tien_te": tk.get("tien_te") or "",
            "phien_ban": tk.get("phien_ban") or "", "ngay_tao": tk.get("ngay_tao") or "", "cho_ghi": bool(tk.get("cho_ghi")),
            "kiem_tra": tk.get("kiem_tra") or None}


def danh_sach() -> list:
    return [_cong_khai(t) for t in _doc_tk()["tai_khoan"]]


def them_tai_khoan(d: dict) -> dict:
    nen = str(d.get("nen") or "")
    if nen not in NEN:
        raise ValueError("Chọn nền tảng: Facebook, TikTok hoặc Google Ads.")
    ma_tk = re.sub(r"\s", "", str(d.get("ma_tk") or ""))
    if not ma_tk:
        raise ValueError("Cần nhập mã tài khoản quảng cáo.")
    if nen == "facebook":
        ma_tk = "act_" + re.sub(r"\D", "", ma_tk) if not ma_tk.startswith("act_") else ma_tk
    if nen == "google":
        ma_tk = re.sub(r"\D", "", ma_tk)
        if len(ma_tk) != 10:
            raise ValueError("Mã khách hàng Google Ads gồm đúng 10 số.")
    bi_mat = {}
    for k, nhan, bm, _ in TRUONG[nen]:
        v = str(d.get(k) or "").strip()
        if bm and not v and k not in ("login_customer_id",):
            raise ValueError("Cần nhập: %s." % nhan)
        if bm and v:
            bi_mat[k] = _ma_hoa(v)
    if nen == "google" and d.get("login_customer_id"):
        bi_mat["login_customer_id"] = _ma_hoa(re.sub(r"\D", "", str(d["login_customer_id"])))
    tk = {"id": "tk-" + hashlib.sha1((nen + ma_tk + str(time.time())).encode()).hexdigest()[:8], "nen": nen,
          "ten": str(d.get("ten") or "").strip()[:80] or (NEN[nen] + " " + ma_tk), "ma_tk": ma_tk, "bi_mat": bi_mat,
          "phien_ban": str(d.get("phien_ban") or "").strip()[:12], "ngay_tao": _dt.date.today().isoformat()}
    with _khoa:
        doc = _doc_tk()
        if any(t["nen"] == nen and t["ma_tk"] == ma_tk for t in doc["tai_khoan"]):
            raise ValueError("Tài khoản này đã có trong danh sách.")
        doc["tai_khoan"].append(tk)
        _ghi(TEP_TK, doc)
    return _cong_khai(tk)


def xoa_tai_khoan(tid: str) -> bool:
    with _khoa:
        doc = _doc_tk()
        n = len(doc["tai_khoan"])
        doc["tai_khoan"] = [t for t in doc["tai_khoan"] if t["id"] != tid]
        _ghi(TEP_TK, doc)
        for k in [k for k in _nho if k.startswith(tid + "|")]:
            _nho.pop(k, None)
    return len(doc["tai_khoan"]) < n


def cai_chung(d: dict | None = None) -> dict:
    """Mục tiêu dùng cho gợi ý: CPA mong muốn, ROAS mong muốn, ngân sách ngày tối đa (đơn vị tiền của tài khoản)."""
    with _khoa:
        doc = _doc_tk()
        if d is not None:
            for k in ("muc_tieu_cpa", "muc_tieu_roas", "ngan_sach_ngay_toi_da"):
                if k in d:
                    try:
                        doc["chung"][k] = max(0.0, float(d[k] or 0))
                    except (TypeError, ValueError):
                        raise ValueError("Mục tiêu phải là số.")
            _ghi(TEP_TK, doc)
        return {"muc_tieu_cpa": doc["chung"].get("muc_tieu_cpa", 0), "muc_tieu_roas": doc["chung"].get("muc_tieu_roas", 0),
                "ngan_sach_ngay_toi_da": doc["chung"].get("ngan_sach_ngay_toi_da", 0)}


# ---------------------------------------------------------------- gọi HTTP
class LoiNenTang(Exception):
    """Lỗi từ nền tảng, đã dịch ra tiếng Việt cho người không rành kỹ thuật."""


def _http(method: str, url: str, headers: dict | None = None, data=None, hinh: str = "json", thu: int = 40):
    h = {"User-Agent": "tisa-bot-quang-cao/1", "Accept": "application/json"}
    h.update(headers or {})
    body = None
    if data is not None:
        if hinh == "form":
            body = urllib.parse.urlencode(data).encode()
            h["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=thu) as r:
            raw = r.read().decode("utf-8", "replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            j = json.loads(raw)
        except ValueError:
            j = {"raw": raw[:300]}
        j["_http"] = e.code
        return j
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise LoiNenTang("Không kết nối được tới nền tảng quảng cáo (mạng chập chờn hoặc bị chặn): %s" % str(e)[:120])
    except ValueError:
        raise LoiNenTang("Nền tảng trả về dữ liệu không đọc được.")


def _loi_fb(j: dict) -> str | None:
    e = j.get("error")
    if not isinstance(e, dict):
        return None
    ma, msg = e.get("code"), str(e.get("message") or "")
    if ma in (190, 102) or e.get("type") == "OAuthException" and "token" in msg.lower():
        return "Mã truy cập Facebook hết hạn hoặc sai. Tạo mã mới (nên dùng System User) rồi nhập lại."
    if ma in (10, 200, 294) or "permission" in msg.lower():
        return "Mã truy cập chưa có quyền đọc quảng cáo (cần ads_read) hoặc chưa được gán tài khoản này."
    if ma in (4, 17, 32, 613):
        return "Facebook đang giới hạn số lần gọi. Chờ vài phút rồi bấm Làm mới."
    return "Facebook báo lỗi: " + msg[:200]


def _loi_tt(j: dict) -> str | None:
    c = j.get("code")
    if c in (None, 0):
        return None
    msg = str(j.get("message") or "")
    if c in (40100, 40101, 40102, 40104, 40105):
        return "Mã truy cập TikTok hết hạn hoặc sai. Lấy mã mới rồi nhập lại."
    if c in (40001, 40002) or "permission" in msg.lower():
        return "TikTok báo thiếu quyền hoặc sai mã nhà quảng cáo: " + msg[:160]
    if c == 40100 or "rate" in msg.lower():
        return "TikTok đang giới hạn số lần gọi. Chờ vài phút rồi bấm Làm mới."
    return "TikTok báo lỗi %s: %s" % (c, msg[:200])


def _loi_gg(j: dict) -> str | None:
    e = j.get("error")
    if not isinstance(e, dict):
        return None
    msg = str(e.get("message") or "")
    if e.get("code") == 401 or "UNAUTHENTICATED" in str(e.get("status")):
        return "Đăng nhập Google Ads hết hạn hoặc sai. Kiểm tra lại client ID, secret và refresh token."
    if e.get("code") == 403:
        return "Google Ads từ chối: kiểm tra developer token, quyền của tài khoản và mã tài khoản quản lý (MCC). " + msg[:160]
    if e.get("code") == 404 or "version" in msg.lower() or "deprecated" in msg.lower():
        return "Phiên bản API Google Ads có thể đã hết hạn. Thử đổi ô Phiên bản (ví dụ v24). " + msg[:140]
    return "Google Ads báo lỗi: " + msg[:200]


# ---------------------------------------------------------------- chuẩn hoá một dòng số liệu
def _so(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def dong(ngay, cd_id, cd_ten, chi_phi=0, hien_thi=0, bam=0, ket_qua=0, doanh_thu=0) -> dict:
    return {"ngay": ngay, "cd_id": str(cd_id), "cd": cd_ten or str(cd_id), "chi_phi": _so(chi_phi), "hien_thi": _so(hien_thi),
            "bam": _so(bam), "ket_qua": _so(ket_qua), "doanh_thu": _so(doanh_thu)}


# Loại hành động Facebook tính là "kết quả", theo thứ tự ưu tiên: mua hàng, khách để lại thông tin, tin nhắn.
_FB_MUA = ("omni_purchase", "purchase", "offsite_conversion.fb_pixel_purchase", "onsite_web_purchase")
_FB_KHACH = ("lead", "onsite_conversion.lead_grouped", "offsite_conversion.fb_pixel_lead", "onsite_web_lead")
_FB_TIN = ("onsite_conversion.messaging_conversation_started_7d", "onsite_conversion.total_messaging_connection")


def _fb_lay(ds, loai) -> float:
    kq = {a.get("action_type"): _so(a.get("value")) for a in (ds or []) if isinstance(a, dict)}
    for t in loai:
        if t in kq:
            return kq[t]
    return 0.0


def _tk_fb(tk: dict, bm: dict, tu: str, den: str) -> dict:
    ma = tk["ma_tk"]
    ver = tk.get("phien_ban") or FB_PHIEN_BAN
    token = bm.get("token", "")
    goc = "%s/%s/%s" % (FB_GOC, ver, ma)
    info = _http("GET", goc + "?" + urllib.parse.urlencode({"fields": "name,currency,account_status", "access_token": token}))
    if (m := _loi_fb(info)):
        raise LoiNenTang(m)
    rows = []
    url = goc + "/insights?" + urllib.parse.urlencode({
        "level": "campaign", "time_increment": 1, "limit": 500, "access_token": token,
        "fields": "campaign_id,campaign_name,spend,impressions,clicks,actions,action_values",
        "time_range": json.dumps({"since": tu, "until": den})})
    for _ in range(40):
        j = _http("GET", url)
        if (m := _loi_fb(j)):
            raise LoiNenTang(m)
        for r in j.get("data") or []:
            mua = _fb_lay(r.get("actions"), _FB_MUA)
            kq = mua or _fb_lay(r.get("actions"), _FB_KHACH) or _fb_lay(r.get("actions"), _FB_TIN)
            rows.append(dong(r.get("date_start"), r.get("campaign_id"), r.get("campaign_name"), r.get("spend"),
                             r.get("impressions"), r.get("clicks"), kq, _fb_lay(r.get("action_values"), _FB_MUA)))
        url = ((j.get("paging") or {}).get("next")) or ""
        if not url:
            break
    cd = {}
    j = _http("GET", goc + "/campaigns?" + urllib.parse.urlencode({
        "fields": "id,name,status,effective_status,daily_budget,objective", "limit": 200, "access_token": token}))
    for c in j.get("data") or []:
        cd[str(c.get("id"))] = {"trang_thai": str(c.get("effective_status") or c.get("status") or "").upper(),
                                "ngan_sach_ngay": _so(c.get("daily_budget")), "muc_tieu": c.get("objective") or ""}
    return {"tien_te": info.get("currency") or "VND", "ten": info.get("name") or "", "dong": rows, "chien_dich": cd}


def _tk_tiktok(tk: dict, bm: dict, tu: str, den: str) -> dict:
    ma = tk["ma_tk"]
    h = {"Access-Token": bm.get("token", "")}
    base = TT_GOC + "/open_api/v1.3"
    rows, loi_cuoi = [], None
    # Thử bộ số đầy đủ trước; nền tảng báo sai tên số thì lùi về bộ cơ bản (TikTok đổi tên số theo từng loại tài khoản).
    for so_do in (["spend", "impressions", "clicks", "conversion", "total_purchase_value", "campaign_name"],
                  ["spend", "impressions", "clicks", "conversion", "campaign_name"]):
        rows, trang, loi_cuoi = [], 1, None
        while trang <= 40:
            q = {"advertiser_id": ma, "report_type": "BASIC", "data_level": "AUCTION_CAMPAIGN",
                 "dimensions": json.dumps(["campaign_id", "stat_time_day"]), "metrics": json.dumps(so_do),
                 "start_date": tu, "end_date": den, "page": trang, "page_size": 1000}
            j = _http("GET", base + "/report/integrated/get/?" + urllib.parse.urlencode(q), headers=h)
            if j.get("code") not in (None, 0):
                loi_cuoi = j
                break
            d = j.get("data") or {}
            for r in d.get("list") or []:
                dm, m = r.get("dimensions") or {}, r.get("metrics") or {}
                rows.append(dong(str(dm.get("stat_time_day") or "")[:10], dm.get("campaign_id"), m.get("campaign_name"), m.get("spend"),
                                 m.get("impressions"), m.get("clicks"), m.get("conversion"), m.get("total_purchase_value")))
            if trang >= int((d.get("page_info") or {}).get("total_page") or 1):
                break
            trang += 1
        if loi_cuoi is None:
            break
        if loi_cuoi.get("code") in (40100, 40101, 40102, 40104, 40105, 40001):
            break           # lỗi đăng nhập hoặc quyền: thử lại bộ số khác cũng vô ích
    if loi_cuoi is not None:
        raise LoiNenTang(_loi_tt(loi_cuoi) or "TikTok báo lỗi.")
    cd = {}
    j = _http("GET", base + "/campaign/get/?" + urllib.parse.urlencode({
        "advertiser_id": ma, "page_size": 1000, "fields": json.dumps(["campaign_id", "campaign_name", "operation_status", "budget", "objective_type"])}), headers=h)
    if j.get("code") in (None, 0):
        for c in (j.get("data") or {}).get("list") or []:
            cd[str(c.get("campaign_id"))] = {"trang_thai": "ACTIVE" if c.get("operation_status") == "ENABLE" else str(c.get("operation_status") or "").upper(),
                                              "ngan_sach_ngay": _so(c.get("budget")), "muc_tieu": c.get("objective_type") or ""}
    info = _http("GET", base + "/advertiser/info/?" + urllib.parse.urlencode({"advertiser_ids": json.dumps([ma]), "fields": json.dumps(["name", "currency"])}), headers=h)
    ds = ((info.get("data") or {}).get("list") or [{}]) if info.get("code") in (None, 0) else [{}]
    return {"tien_te": ds[0].get("currency") or "VND", "ten": ds[0].get("name") or "", "dong": rows, "chien_dich": cd}


def _gg_token(bm: dict) -> str:
    j = _http("POST", GG_TOKEN, data={"client_id": bm.get("client_id", ""), "client_secret": bm.get("client_secret", ""),
                                       "refresh_token": bm.get("refresh_token", ""), "grant_type": "refresh_token"}, hinh="form")
    if not j.get("access_token"):
        raise LoiNenTang("Đăng nhập Google Ads không được: kiểm tra client ID, secret và refresh token. (%s)" % str(j.get("error_description") or j.get("error") or "")[:120])
    return j["access_token"]


def _tk_google(tk: dict, bm: dict, tu: str, den: str) -> dict:
    cid = tk["ma_tk"]
    ver = tk.get("phien_ban") or GG_PHIEN_BAN
    h = {"Authorization": "Bearer " + _gg_token(bm), "developer-token": bm.get("developer_token", "")}
    if bm.get("login_customer_id"):
        h["login-customer-id"] = bm["login_customer_id"]
    url = "%s/%s/customers/%s/googleAds:search" % (GG_GOC, ver, cid)

    def hoi(gaql):
        ra, tok = [], ""
        for _ in range(60):
            body = {"query": gaql, "pageSize": 10000}
            if tok:
                body["pageToken"] = tok
            j = _http("POST", url, headers=h, data=body)
            if (m := _loi_gg(j)):
                raise LoiNenTang(m)
            ra += j.get("results") or []
            tok = j.get("nextPageToken") or ""
            if not tok:
                break
        return ra

    kh = hoi("SELECT customer.currency_code, customer.descriptive_name FROM customer LIMIT 1")
    c0 = (kh[0].get("customer") if kh else {}) or {}
    rows, cd = [], {}
    q = ("SELECT segments.date, campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, metrics.cost_micros, "
         "metrics.impressions, metrics.clicks, metrics.conversions, metrics.conversions_value FROM campaign "
         "WHERE segments.date BETWEEN '%s' AND '%s' AND campaign.status != 'REMOVED'" % (tu, den))
    for r in hoi(q):
        c, m, s = r.get("campaign") or {}, r.get("metrics") or {}, r.get("segments") or {}
        rows.append(dong(s.get("date"), c.get("id"), c.get("name"), _so(m.get("costMicros")) / 1e6, m.get("impressions"), m.get("clicks"),
                         m.get("conversions"), m.get("conversionsValue")))
        cd[str(c.get("id"))] = {"trang_thai": str(c.get("status") or "").upper(),
                                "ngan_sach_ngay": _so((r.get("campaignBudget") or {}).get("amountMicros")) / 1e6, "muc_tieu": ""}
    return {"tien_te": c0.get("currencyCode") or "VND", "ten": c0.get("descriptiveName") or "", "dong": rows, "chien_dich": cd}


_LAY = {"facebook": _tk_fb, "tiktok": _tk_tiktok, "google": _tk_google}


def lay_so_that(tk: dict, tu: str, den: str, lam_moi: bool = False) -> dict:
    khoa = "%s|%s|%s" % (tk["id"], tu, den)
    with _khoa:
        c = _nho.get(khoa)
        if c and not lam_moi and time.time() - c[0] < NHO_GIAY:
            return c[1]
    kq = _LAY[tk["nen"]](tk, _bi_mat(tk), tu, den)
    with _khoa:
        _nho[khoa] = (time.time(), kq)
    return kq


def kiem_tra(tid: str) -> dict:
    """Kiểm tra kết nối bằng một lần đọc nhẹ (2 ngày gần nhất). Kết quả ghi lại để trang hiện đèn xanh / đỏ."""
    with _khoa:
        doc = _doc_tk()
        tk = next((t for t in doc["tai_khoan"] if t["id"] == tid), None)
    if not tk:
        return {"ok": False, "thong_bao": "Không thấy tài khoản này."}
    hom_nay = _dt.date.today()
    t0 = time.time()
    try:
        r = _LAY[tk["nen"]](tk, _bi_mat(tk), (hom_nay - _dt.timedelta(days=2)).isoformat(), hom_nay.isoformat())
        kq = {"ok": True, "thong_bao": "Nối được. Tài khoản: %s, tiền tệ %s, %d chiến dịch." % (r.get("ten") or tk["ma_tk"], r["tien_te"], len(r["chien_dich"]) or len({x["cd_id"] for x in r["dong"]})),
              "tien_te": r["tien_te"], "ten": r.get("ten") or ""}
    except LoiNenTang as e:
        kq = {"ok": False, "thong_bao": str(e)}
    except Exception as e:  # noqa: BLE001
        kq = {"ok": False, "thong_bao": "Lỗi không rõ khi kiểm tra: %s" % str(e)[:160]}
    kq["luc"] = int(time.time())
    kq["mat_ms"] = int((time.time() - t0) * 1000)
    with _khoa:
        doc = _doc_tk()
        for t in doc["tai_khoan"]:
            if t["id"] == tid:
                t["kiem_tra"] = kq
                if kq.get("ok"):
                    t["tien_te"] = kq.get("tien_te") or t.get("tien_te") or ""
                    if kq.get("ten") and (t.get("ten") or "").startswith(NEN[t["nen"]]):
                        t["ten"] = kq["ten"]
        _ghi(TEP_TK, doc)
    return kq


# ---------------------------------------------------------------- số liệu mẫu (xem trước giao diện)
_CD_MAU = [("facebook", "Sản phẩm A - Nhận tin nhắn", 520_000, 0.016, 0.012, 0), ("facebook", "Sản phẩm A - Khách để lại số", 380_000, 0.013, 0.008, 0),
           ("facebook", "Khóa học B - Bán hàng", 450_000, 0.021, 0.004, 1_000_000), ("tiktok", "Video giới thiệu sản phẩm", 300_000, 0.011, 0.004, 0),
           ("tiktok", "Video mẹo hữu ích", 260_000, 0.018, 0.006, 0), ("google", "Từ khoá: sản phẩm chính", 340_000, 0.045, 0.010, 0),
           ("google", "Từ khoá thương hiệu", 120_000, 0.090, 0.020, 0)]


def _hat(*a) -> float:
    h = hashlib.md5("|".join(str(x) for x in a).encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF


def so_mau(tu: str, den: str) -> dict:
    d0, d1 = _dt.date.fromisoformat(tu), _dt.date.fromisoformat(den)
    out = {}
    for i, (nen, ten, chi, tl_bam, tl_kq, gia_tri) in enumerate(_CD_MAU):
        rows = []
        d = d0
        while d <= d1:
            he_so = 0.75 + _hat(i, d.isoformat(), "a") * 0.55
            if i == 4 and d >= d1 - _dt.timedelta(days=2):
                he_so *= 2.3          # một chiến dịch tăng chi đột ngột để thấy cảnh báo
            cp = chi * he_so
            ht = cp / (9_000 + i * 1_500) * 1000 * (0.9 + _hat(i, d.isoformat(), "b") * 0.2)
            bam = ht * tl_bam
            kq = bam * tl_kq * (0.6 if i == 1 and d.day % 3 == 0 else 1) * (0.2 if i == 4 else 1)
            dt = kq * gia_tri if gia_tri else 0
            rows.append(dong(d.isoformat(), "mau-%d" % i, ten, cp, ht, bam, round(kq), dt))
            d += _dt.timedelta(days=1)
        out.setdefault(nen, {"tien_te": "VND", "ten": "Dữ liệu mẫu", "dong": [], "chien_dich": {}})
        out[nen]["dong"] += rows
        out[nen]["chien_dich"]["mau-%d" % i] = {"trang_thai": "PAUSED" if i == 5 else "ACTIVE", "ngan_sach_ngay": chi, "muc_tieu": ""}
    return out


# ---------------------------------------------------------------- tính toán chung
def _chi_so(a: dict) -> dict:
    cp, ht, bam, kq, dt = a["chi_phi"], a["hien_thi"], a["bam"], a["ket_qua"], a["doanh_thu"]
    a["ctr"] = (bam / ht * 100) if ht else 0.0
    a["cpc"] = (cp / bam) if bam else 0.0
    a["cpm"] = (cp / ht * 1000) if ht else 0.0
    a["cpa"] = (cp / kq) if kq else 0.0
    a["roas"] = (dt / cp) if cp and dt else 0.0
    return a


def _cong(ds: list) -> dict:
    t = {"chi_phi": 0.0, "hien_thi": 0.0, "bam": 0.0, "ket_qua": 0.0, "doanh_thu": 0.0}
    for r in ds:
        for k in t:
            t[k] += r[k]
    return _chi_so(t)


def khoang(kieu: str, tu: str = "", den: str = "") -> tuple:
    h = _dt.date.today()
    if kieu == "hom-nay":
        a, b = h, h
    elif kieu == "hom-qua":
        a = b = h - _dt.timedelta(days=1)
    elif kieu == "7-ngay":
        a, b = h - _dt.timedelta(days=6), h
    elif kieu == "30-ngay":
        a, b = h - _dt.timedelta(days=29), h
    elif kieu == "thang-nay":
        a, b = h.replace(day=1), h
    elif kieu == "thang-truoc":
        b = h.replace(day=1) - _dt.timedelta(days=1)
        a = b.replace(day=1)
    elif kieu == "tuy-chon":
        try:
            a, b = _dt.date.fromisoformat(tu), _dt.date.fromisoformat(den)
        except ValueError:
            raise ValueError("Ngày không đúng dạng năm-tháng-ngày.")
        if a > b:
            a, b = b, a
        if (b - a).days > 366:
            raise ValueError("Chọn tối đa 1 năm mỗi lần xem.")
    else:
        a, b = h - _dt.timedelta(days=6), h
    return a, b


def _gom(du_lieu: dict, tk_nen: dict, a: _dt.date, b: _dt.date) -> dict:
    """du_lieu: {id_nguồn: {nen, ten, tien_te, dong, chien_dich}} -> các bảng tổng hợp."""
    tat_ca = []
    cd_map = {}
    for nid, d in du_lieu.items():
        for r in d["dong"]:
            if not (a.isoformat() <= str(r["ngay"]) <= b.isoformat()):
                continue
            x = dict(r, nen=d["nen"], nguon=nid, tien_te=d["tien_te"], tk_ten=d["ten"])
            tat_ca.append(x)
            k = (nid, r["cd_id"])
            c = cd_map.setdefault(k, {"nen": d["nen"], "nguon": nid, "tk_ten": d["ten"], "cd_id": r["cd_id"], "cd": r["cd"], "tien_te": d["tien_te"],
                                      "chi_phi": 0.0, "hien_thi": 0.0, "bam": 0.0, "ket_qua": 0.0, "doanh_thu": 0.0, "ngay": {}})
            for kk in ("chi_phi", "hien_thi", "bam", "ket_qua", "doanh_thu"):
                c[kk] += r[kk]
            c["ngay"][r["ngay"]] = c["ngay"].get(r["ngay"], 0) + r["chi_phi"]
    # Tiền tệ chính = tiền tệ có chi phí lớn nhất. Số tổng chỉ cộng cùng tiền tệ, tránh cộng VND với USD.
    theo_tt = {}
    for r in tat_ca:
        theo_tt[r["tien_te"]] = theo_tt.get(r["tien_te"], 0) + r["chi_phi"]
    chinh = max(theo_tt, key=theo_tt.get) if theo_tt else "VND"
    cung = [r for r in tat_ca if r["tien_te"] == chinh]
    ngay_ds, nd = [], a
    while nd <= b:
        ngay_ds.append(nd.isoformat())
        nd += _dt.timedelta(days=1)
    chuoi = []
    for n in ngay_ds:
        t = _cong([r for r in cung if r["ngay"] == n])
        t["ngay"] = n
        chuoi.append(t)
    theo_nen = {}
    for nen in NEN:
        ds = [r for r in cung if r["nen"] == nen]
        if ds:
            theo_nen[nen] = _cong(ds)
    chien_dich = []
    for (nid, cid), c in cd_map.items():
        _chi_so(c)
        st = (du_lieu[nid].get("chien_dich") or {}).get(cid) or {}
        c["trang_thai"] = st.get("trang_thai") or ""
        c["ngan_sach_ngay"] = st.get("ngan_sach_ngay") or 0
        c["ngay_chi"] = [c["ngay"].get(n, 0) for n in ngay_ds]
        c.pop("ngay", None)
        chien_dich.append(c)
    chien_dich.sort(key=lambda c: -c["chi_phi"])
    return {"tien_te": chinh, "tien_te_khac": sorted(k for k in theo_tt if k != chinh), "tong": _cong(cung), "chuoi": chuoi,
            "theo_nen": theo_nen, "chien_dich": chien_dich, "ngay_ds": ngay_ds}


def _so_sanh(hien: dict, truoc: dict) -> dict:
    out = {}
    for k in ("chi_phi", "ket_qua", "cpa", "doanh_thu", "roas", "ctr", "hien_thi", "bam"):
        a, b = hien.get(k, 0), truoc.get(k, 0)
        out[k] = round((a - b) / b * 100, 1) if b else None
    return out


# ---------------------------------------------------------------- gợi ý tối ưu (luật rõ ràng, không đoán mò)
def goi_y(gom: dict, muc_tieu: dict) -> list:
    ra = []
    tt = gom["tien_te"]
    tong = gom["tong"]
    cpa_mt = _so(muc_tieu.get("muc_tieu_cpa"))
    roas_mt = _so(muc_tieu.get("muc_tieu_roas"))
    # Chưa đặt mục tiêu thì lấy mức trung bình toàn tài khoản làm chuẩn so sánh.
    cpa_chuan = cpa_mt or tong.get("cpa") or 0
    nguong_tieu = max(cpa_chuan * 3, 0) if cpa_chuan else 300_000 if tt == "VND" else 15

    def tien(v):
        return ("{:,.0f}".format(v).replace(",", ".") + " đ") if tt == "VND" else "{:,.2f} {}".format(v, tt)

    for c in gom["chien_dich"]:
        if c["chi_phi"] <= 0 or c["trang_thai"] in ("PAUSED", "DISABLE", "REMOVED", "ARCHIVED", "CAMPAIGN_PAUSED"):
            continue
        ten = "%s (%s)" % (c["cd"], NEN[c["nen"]])
        if c["ket_qua"] == 0 and c["chi_phi"] >= nguong_tieu:
            ra.append({"muc": "nghiem_trong", "nen": c["nen"], "cd": c["cd"], "tieu_de": "Tốn tiền mà chưa có kết quả",
                       "chi_tiet": "%s đã chi %s nhưng chưa có kết quả nào trong kỳ này." % (ten, tien(c["chi_phi"])),
                       "hanh_dong": "Tạm dừng hoặc đổi nội dung, đối tượng. Hỏi trợ lý để kiểm tra điểm kẹt (bài, đối tượng, trang đích)."})
            continue
        if cpa_chuan and c["ket_qua"] >= 3 and c["cpa"] > cpa_chuan * 1.3:
            ra.append({"muc": "canh_bao", "nen": c["nen"], "cd": c["cd"], "tieu_de": "Giá mỗi kết quả cao hơn mục tiêu",
                       "chi_tiet": "%s: %s mỗi kết quả, cao hơn %s (%s). Cao hơn %d%%." % (ten, tien(c["cpa"]), "mục tiêu" if cpa_mt else "mức trung bình", tien(cpa_chuan), round((c["cpa"] / cpa_chuan - 1) * 100)),
                       "hanh_dong": "Giảm ngân sách 20 đến 30% hoặc thay mẫu quảng cáo yếu nhất."})
        elif cpa_chuan and c["ket_qua"] >= 5 and 0 < c["cpa"] < cpa_chuan * 0.7:
            ra.append({"muc": "tot", "nen": c["nen"], "cd": c["cd"], "tieu_de": "Đang làm tốt, có thể tăng ngân sách",
                       "chi_tiet": "%s: %s mỗi kết quả, thấp hơn %s (%s), đã có %d kết quả." % (ten, tien(c["cpa"]), "mục tiêu" if cpa_mt else "mức trung bình", tien(cpa_chuan), c["ket_qua"]),
                       "hanh_dong": "Tăng ngân sách ngày khoảng 20% rồi theo dõi 2 ngày, không tăng quá nhanh."})
        if roas_mt and c["doanh_thu"] > 0 and c["roas"] < roas_mt * 0.8 and c["chi_phi"] >= nguong_tieu:
            ra.append({"muc": "canh_bao", "nen": c["nen"], "cd": c["cd"], "tieu_de": "ROAS thấp hơn mục tiêu",
                       "chi_tiet": "%s: ROAS %.2f, mục tiêu %.2f." % (ten, c["roas"], roas_mt), "hanh_dong": "Xem lại giá bán, đối tượng, hoặc dừng chạy phần kém."})
        if c["hien_thi"] >= 5000 and c["ctr"] < 0.8:
            ra.append({"muc": "canh_bao", "nen": c["nen"], "cd": c["cd"], "tieu_de": "Ít người bấm vào quảng cáo",
                       "chi_tiet": "%s: tỉ lệ bấm (CTR) chỉ %.2f%% sau %s lượt hiển thị." % (ten, c["ctr"], "{:,.0f}".format(c["hien_thi"]).replace(",", ".")),
                       "hanh_dong": "Đổi hình hoặc tiêu đề mở đầu; thử một mẫu mới chạy song song."})
        ng = c.get("ngay_chi") or []
        if len(ng) >= 4 and ng[-1] > 0:
            tb = sum(ng[:-1]) / max(1, len(ng) - 1)
            if tb > 0 and ng[-1] > tb * 2:
                ra.append({"muc": "canh_bao", "nen": c["nen"], "cd": c["cd"], "tieu_de": "Chi phí ngày gần nhất tăng đột biến",
                           "chi_tiet": "%s: ngày gần nhất chi %s, gấp %.1f lần mức trung bình các ngày trước (%s)." % (ten, tien(ng[-1]), ng[-1] / tb, tien(tb)),
                           "hanh_dong": "Kiểm tra có ai vừa đổi ngân sách hoặc bật thêm nhóm quảng cáo không."})
    tran = _so(muc_tieu.get("ngan_sach_ngay_toi_da"))
    if tran and gom["chuoi"]:
        ng_cuoi = gom["chuoi"][-1]["chi_phi"]
        if ng_cuoi > tran:
            ra.append({"muc": "nghiem_trong", "nen": "", "cd": "", "tieu_de": "Chi phí ngày vượt mức anh đặt",
                       "chi_tiet": "Ngày %s đã chi %s, vượt mức tối đa %s." % (gom["chuoi"][-1]["ngay"], tien(ng_cuoi), tien(tran)), "hanh_dong": "Giảm ngân sách các chiến dịch tốn nhiều nhất."})
    thu_tu = {"nghiem_trong": 0, "canh_bao": 1, "tot": 2}
    ra.sort(key=lambda x: thu_tu[x["muc"]])
    return ra[:30]


# ---------------------------------------------------------------- tổng hợp cho trang
def tong_quan(kieu: str, tu: str = "", den: str = "", nen: str = "", mau: bool = False, lam_moi: bool = False, cap: str = "nhom") -> dict:
    a, b = khoang(kieu, tu, den)
    so_ngay = (b - a).days + 1
    pa, pb = a - _dt.timedelta(days=so_ngay), a - _dt.timedelta(days=1)
    doc = _doc_tk()
    cac = [t for t in doc["tai_khoan"] if not nen or t["nen"] == nen]
    du_lieu, du_lieu_truoc, loi = {}, {}, []
    if mau or not doc["tai_khoan"]:
        che_do = "mau"
        for n, d in so_mau(pa.isoformat(), b.isoformat()).items():
            if nen and n != nen:
                continue
            d = dict(d, nen=n)
            du_lieu["mau-" + n] = d
    else:
        che_do = "that"
        for t in cac:
            try:
                d = lay_so_that(t, pa.isoformat(), b.isoformat(), lam_moi)
                du_lieu[t["id"]] = dict(d, nen=t["nen"], ten=t.get("ten") or d.get("ten") or t["ma_tk"])
            except LoiNenTang as e:
                loi.append({"tk": t.get("ten") or t["ma_tk"], "nen": t["nen"], "thong_bao": str(e)})
            except Exception as e:  # noqa: BLE001
                loi.append({"tk": t.get("ten") or t["ma_tk"], "nen": t["nen"], "thong_bao": "Lỗi không rõ: %s" % str(e)[:160]})
    g = _gom(du_lieu, {}, a, b)
    g0 = _gom(du_lieu, {}, pa, pb)
    mt = cai_chung()
    # Bảng chi tiết 19 chỉ số (tisa_quang_cao_bang.py): theo nhóm quảng cáo hoặc theo chiến dịch, cả kỳ.
    import tisa_quang_cao_bang as B
    cap = "chien-dich" if cap == "chien-dich" else "nhom"
    bang = []
    if che_do == "mau":
        bang = B.bang_mau(a, b, cap, nen)
    else:
        da = {(x["tk"], x["thong_bao"]) for x in loi}
        for t in cac:
            try:
                bang += B.lay_bang(t, a.isoformat(), b.isoformat(), cap, lam_moi)
            except LoiNenTang as e:
                if (t.get("ten") or t["ma_tk"], str(e)) not in da:
                    loi.append({"tk": t.get("ten") or t["ma_tk"], "nen": t["nen"], "thong_bao": str(e)})
            except Exception as e:  # noqa: BLE001
                loi.append({"tk": t.get("ten") or t["ma_tk"], "nen": t["nen"], "thong_bao": "Lỗi không rõ khi lấy bảng chi tiết: %s" % str(e)[:160]})
    bang = B.hoan_tat([r for r in bang if r["tien_te"] == g["tien_te"] or not g["theo_nen"]])
    return {"ok": True, "che_do": che_do, "tu": a.isoformat(), "den": b.isoformat(), "so_ngay": so_ngay, "tien_te": g["tien_te"], "tien_te_khac": g["tien_te_khac"],
            "tong": g["tong"], "truoc": g0["tong"], "doi": _so_sanh(g["tong"], g0["tong"]), "chuoi": g["chuoi"], "theo_nen": g["theo_nen"],
            "chien_dich": g["chien_dich"], "goi_y": goi_y(g, mt), "muc_tieu": mt, "loi": loi, "co_tai_khoan": bool(doc["tai_khoan"]),
            "bang": bang, "bang_tong": B.tong(bang), "cap": cap, "luc": int(time.time())}


# ---------------------------------------------------------------- dự kiến cho phiếu thiết lập (phiếu nằm ở tisa_quang_cao_thiet_lap.py)
def du_kien(nen: str, ngan_sach: float, tu_ngay_so: int = 30) -> dict:
    """Dự kiến số kết quả và chi phí tháng từ số thực 30 ngày của chính các tài khoản đã nối (hoặc số mẫu)."""
    d = tong_quan("30-ngay", nen=nen if nen in NEN else "")
    cac = [c for c in d["chien_dich"] if c["ket_qua"] > 0]
    cpa = (sum(c["chi_phi"] for c in cac) / sum(c["ket_qua"] for c in cac)) if cac else 0
    out = {"che_do": d["che_do"], "tien_te": d["tien_te"], "cpa_tham_chieu": round(cpa), "ket_qua_ngay": round(ngan_sach / cpa, 1) if cpa else 0,
           "chi_phi_thang": round(ngan_sach * 30), "ket_qua_thang": round(ngan_sach * 30 / cpa) if cpa else 0}
    out["ghi_chu"] = ("Dựa trên giá mỗi kết quả trung bình 30 ngày qua của %s." % (NEN[nen] if nen in NEN else "các nền tảng")) if cpa else "Chưa đủ dữ liệu 30 ngày để dự kiến."
    return out


# ---------------------------------------------------------------- đường dẫn
def gan(app) -> None:
    from fastapi.responses import HTMLResponse, JSONResponse, Response

    trang = ROOT / "dashboard" / "tisa-quang-cao.html"

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=ma)

    @app.get("/tisa-quang-cao/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang Quảng Cáo", status_code=500)

    @app.get("/tisa-quang-cao/api/tong-quan")
    async def _tong_quan(request: Request):
        import asyncio
        q = request.query_params
        try:
            return await asyncio.to_thread(tong_quan, q.get("kieu", "7-ngay"), q.get("tu", ""), q.get("den", ""), q.get("nen", ""),
                                           q.get("mau") == "1", q.get("lam_moi") == "1", q.get("cap", "nhom"))
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/tai-khoan")
    async def _ds():
        return {"ok": True, "tai_khoan": danh_sach(), "truong": {n: [{"khoa": k, "nhan": nh, "bi_mat": bm, "goi_y": gy} for k, nh, bm, gy in ds] for n, ds in TRUONG.items()},
                "nen": NEN, "chung": cai_chung(), "mac_dinh": {"facebook": FB_PHIEN_BAN, "google": GG_PHIEN_BAN}}

    @app.post("/tisa-quang-cao/api/tai-khoan")
    async def _them(request: Request):
        try:
            tk = them_tai_khoan(await request.json())
        except ValueError as e:
            return loi(str(e))
        return {"ok": True, "tai_khoan": tk}

    @app.post("/tisa-quang-cao/api/tai-khoan/{tid}/kiem-tra")
    async def _kt(tid: str):
        import asyncio
        return await asyncio.to_thread(kiem_tra, tid)

    @app.post("/tisa-quang-cao/api/tai-khoan/{tid}/xoa")
    async def _xoa(tid: str):
        return {"ok": xoa_tai_khoan(tid)}

    @app.post("/tisa-quang-cao/api/muc-tieu")
    async def _mt(request: Request):
        try:
            return {"ok": True, "chung": cai_chung(await request.json())}
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/du-kien")
    async def _du_kien(request: Request):
        import asyncio
        q = request.query_params
        try:
            ns = float(q.get("ngan_sach") or 0)
        except ValueError:
            return loi("Ngân sách phải là số.")
        return {"ok": True, **(await asyncio.to_thread(du_kien, q.get("nen", ""), ns))}

    @app.get("/tisa-quang-cao/api/xuat.csv")
    async def _csv(request: Request):
        import asyncio
        q = request.query_params
        d = await asyncio.to_thread(tong_quan, q.get("kieu", "7-ngay"), q.get("tu", ""), q.get("den", ""), q.get("nen", ""), q.get("mau") == "1", False, q.get("cap", "nhom"))
        cot = [("nen", "Nền tảng"), ("tk_ten", "Tài khoản"), ("cd", "Chiến dịch"), ("nhom", "Tên nhóm quảng cáo"), ("trang_thai", "Phân phối"), ("ngan_sach", "Ngân sách"), ("chi_phi", "Số tiền đã chi tiêu"),
               ("tiep_can", "Người tiếp cận"), ("hien_thi", "Lượt hiển thị"), ("tan_suat", "Tần suất"), ("chia_se", "Lượt chia sẻ bài viết"), ("binh_luan", "Bình luận về bài viết"),
               ("tin_nhan", "Lượt bắt đầu cuộc trò chuyện qua tin nhắn"), ("cp_tin_nhan", "Chi phí trên mỗi lượt bắt đầu cuộc trò chuyện"), ("ket_qua", "Kết quả"), ("cpa", "Chi phí trên mỗi kết quả"),
               ("cpm", "CPM"), ("ctr", "CTR (tất cả)"), ("v25", "Lượt phát 25% video"), ("v50", "Lượt phát 50% video"), ("v75", "Lượt phát 75% video"), ("v100", "Lượt phát 100% video"),
               ("bam", "Lượt bấm"), ("cpc", "CPC"), ("doanh_thu", "Doanh thu"), ("roas", "ROAS")]
        ra = ["\ufeff" + ",".join('"%s"' % n for _, n in cot)]
        for r in d["bang"]:
            gt = [NEN.get(r["nen"], r["nen"]) if k == "nen" else (round(r[k], 2) if isinstance(r.get(k), float) else r.get(k, "")) for k, _ in cot]
            ra.append(",".join('"%s"' % str(v).replace('"', '""') for v in gt))
        return Response("\n".join(ra), media_type="text/csv; charset=utf-8",
                        headers={"content-disposition": 'attachment; filename="quang-cao-%s-%s.csv"' % (d["tu"], d["den"])})

    try:
        import tisa_quang_cao_tu_van
        tisa_quang_cao_tu_van.gan(app)
    except Exception as e:  # noqa: BLE001
        print(f"[tisa_quang_cao_tu_van] không bật được: {type(e).__name__}: {e}")
    try:
        import tisa_quang_cao_sang_tao
        tisa_quang_cao_sang_tao.gan(app)
    except Exception as e:  # noqa: BLE001
        print(f"[tisa_quang_cao_sang_tao] không bật được: {type(e).__name__}: {e}")
    try:
        import tisa_quang_cao_giao_viec
        tisa_quang_cao_giao_viec.gan(app)
    except Exception as e:  # noqa: BLE001
        print(f"[tisa_quang_cao_giao_viec] không bật được: {type(e).__name__}: {e}")
    try:
        import tisa_quang_cao_thao_tac
        tisa_quang_cao_thao_tac.gan(app)
    except Exception as e:  # noqa: BLE001 - phần thao tác hỏng không được làm hỏng phần số liệu
        print(f"[tisa_quang_cao_thao_tac] không bật được: {type(e).__name__}: {e}")
    try:
        import tisa_quang_cao_thiet_lap
        tisa_quang_cao_thiet_lap.gan(app)
    except Exception as e:  # noqa: BLE001 - phần thiết lập hỏng không được làm hỏng phần số liệu
        print(f"[tisa_quang_cao_thiet_lap] không bật được: {type(e).__name__}: {e}")
