"""tisa_quang_cao_kho.py - KHO SỐ LIỆU QUẢNG CÁO của TISA BOT (V2.90).

Trước đây mỗi lần đổi kỳ xem là phải quét lại, và số chỉ cất một bản (kỳ lấy gần nhất), nên bảng chiến dịch thiếu dòng. Nay:
  - Quét từ Meta bằng API (máy làm, không nhờ AI đọc hộ nên không bị cắt chữ, không sót dòng), lưu từng NGÀY, từng NHÓM quảng cáo
    vào một cơ sở dữ liệu trên máy (STATE_DIR/quang-cao/lich-su.sqlite3). Lưu xong là giữ mãi, quét tiếp chỉ bồi thêm.
  - Đổi kỳ xem (7 ngày, 30 ngày, tháng trước, chọn ngày...) chỉ ĐỌC kho, không gọi lại Meta. Kỳ nào kho chưa phủ hết thì trang báo
    số ngày thiếu và có nút quét bổ sung.
  - Danh mục chiến dịch và nhóm quảng cáo (tên, trạng thái, ngân sách) được quét đủ, kể cả cái đang bật mà chưa chi tiền.
  - Tự đồng bộ nền mỗi giờ (chỉ đọc 7 ngày gần nhất, vì Meta còn cập nhật số của vài ngày trước).

Nguồn mã truy cập (chỉ ĐỌC, quyền ads_read):
  1. Tài khoản Facebook anh đã nhập mã API ở tab Tài khoản và kết nối.
  2. Kết nối "Meta Ads (tự tạo app, chỉ đọc)" đã đăng nhập (mã nằm trong két của TISA BOT, không đưa ra trình duyệt).
Không ghi, không bật tắt, không sửa gì trong tài khoản quảng cáo.
"""
from __future__ import annotations

import asyncio
import datetime as _dt
import json
import os
import sqlite3
import threading
import time
import urllib.parse

import tisa_quang_cao as Q
import tisa_quang_cao_bang as B

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

DB = Q.KHO / "lich-su.sqlite3"
CAI_DAT = Q.KHO / "kho-cai-dat.json"
NGAY_NAP_LAN_DAU = 90      # lần quét đầu tiên lấy ngược bao nhiêu ngày
NGAY_BOI_LAI = 7           # mỗi lần đồng bộ nhanh quét lại bấy nhiêu ngày gần nhất (số của Meta còn đổi vài ngày sau)
MOI_DOT = 31               # mỗi đợt hỏi Meta tối đa bấy nhiêu ngày
GIO_TU_DONG = 3600
TIEN_KHONG_LE = {"VND", "JPY", "KRW", "CLP", "PYG", "UGX", "ISK"}   # tiền không có phần lẻ: ngân sách Meta trả đúng đơn vị

_khoa = threading.RLock()
_tien: dict = {}     # nen -> tiến độ quét đang chạy / vừa xong
_mo_ta_nhanh = threading.Lock()


# ---------------------------------------------------------------- cơ sở dữ liệu
SCHEMA = """
CREATE TABLE IF NOT EXISTS ngay_nhom (
  nen TEXT NOT NULL, tk TEXT NOT NULL, ngay TEXT NOT NULL, cd_id TEXT NOT NULL, nhom_id TEXT NOT NULL,
  cd TEXT, nhom TEXT,
  chi_phi REAL, tiep_can REAL, hien_thi REAL, bam REAL, chia_se REAL, binh_luan REAL, tin_nhan REAL, ket_qua REAL, doanh_thu REAL,
  v25 REAL, v50 REAL, v75 REAL, v100 REAL,
  PRIMARY KEY (nen, tk, ngay, nhom_id));
CREATE INDEX IF NOT EXISTS i_ngay ON ngay_nhom (nen, ngay);
CREATE TABLE IF NOT EXISTS doi_tuong (
  nen TEXT NOT NULL, tk TEXT NOT NULL, loai TEXT NOT NULL, id TEXT NOT NULL, cd_id TEXT, ten TEXT, trang_thai TEXT, ngan_sach REAL,
  PRIMARY KEY (nen, tk, loai, id));
CREATE TABLE IF NOT EXISTS tai_khoan (
  nen TEXT NOT NULL, tk TEXT NOT NULL, ten TEXT, tien_te TEXT, PRIMARY KEY (nen, tk));
CREATE TABLE IF NOT EXISTS quet (
  nen TEXT NOT NULL, tk TEXT NOT NULL, tu TEXT NOT NULL, den TEXT NOT NULL, luc INTEGER NOT NULL, so_dong INTEGER);
CREATE TABLE IF NOT EXISTS ngay_bai (
  nen TEXT NOT NULL, tk TEXT NOT NULL, ngay TEXT NOT NULL, cd_id TEXT NOT NULL, nhom_id TEXT NOT NULL, bai_id TEXT NOT NULL,
  bai TEXT,
  chi_phi REAL, tiep_can REAL, hien_thi REAL, bam REAL, chia_se REAL, binh_luan REAL, tin_nhan REAL, ket_qua REAL, doanh_thu REAL,
  v25 REAL, v50 REAL, v75 REAL, v100 REAL,
  PRIMARY KEY (nen, tk, ngay, bai_id));
CREATE INDEX IF NOT EXISTS i_bai_cd ON ngay_bai (nen, tk, cd_id, ngay);
CREATE TABLE IF NOT EXISTS quet_bai (
  nen TEXT NOT NULL, tk TEXT NOT NULL, cd_id TEXT NOT NULL, tu TEXT NOT NULL, den TEXT NOT NULL, luc INTEGER NOT NULL);
"""


def _noi() -> sqlite3.Connection:
    Q.KHO.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(DB), timeout=30)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    try:
        os.chmod(DB, 0o600)
    except OSError:
        pass
    return c


def _doc_cai_dat() -> dict:
    try:
        d = json.loads(CAI_DAT.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def chon_tai_khoan(nen: str, ds) -> None:
    with _khoa:
        d = _doc_cai_dat()
        d.setdefault(nen, {})["tai_khoan"] = sorted({str(x) for x in ds}) if ds is not None else None
        Q._ghi(CAI_DAT, d)


# ---------------------------------------------------------------- mã truy cập (chỉ đọc)
def _token_oauth() -> str:
    """Mã của kết nối Meta Ads (tự tạo app, chỉ đọc) nếu anh đã đăng nhập. Chạy trong luồng riêng nên tự dựng vòng lặp."""
    try:
        import mcp_client
        import mcp_store
        for c in mcp_store.resolved():
            if c.get("connector_id") != "meta-ads-graph":
                continue
            h = asyncio.run(mcp_client._oauth_headers(c))
            a = (h or {}).get("Authorization", "")
            if a.lower().startswith("bearer "):
                return a.split(" ", 1)[1].strip()
    except Exception:  # noqa: BLE001
        pass
    return ""


def _nguon_token(nen: str) -> list:
    """[{ma, ten, tien_te, token, kieu}] các tài khoản quảng cáo đọc được. Mã API anh nhập tay đi trước."""
    if nen != "facebook":
        return []
    ra, thay = [], set()
    for t in Q._doc_tk()["tai_khoan"]:
        if t["nen"] != "facebook":
            continue
        ma = str(t.get("ma_tk") or "")
        ma = ma if ma.startswith("act_") else "act_" + ma
        tok = Q._bi_mat(t).get("token", "")
        if ma and tok:
            ra.append({"ma": ma, "ten": t.get("ten") or ma, "tien_te": t.get("tien_te") or "", "token": tok, "kieu": "api", "trang_thai": 1})
            thay.add(ma)
    tok = _token_oauth()
    if tok:
        try:
            url = "%s/%s/me/adaccounts?%s" % (Q.FB_GOC, Q.FB_PHIEN_BAN, urllib.parse.urlencode(
                {"fields": "id,name,currency,account_status", "limit": 100, "access_token": tok}))
            for _ in range(10):
                j = Q._http("GET", url)
                if Q._loi_fb(j):
                    break
                for a in j.get("data") or []:
                    ma = str(a.get("id") or "")
                    if ma and ma not in thay:
                        ra.append({"ma": ma, "ten": a.get("name") or ma, "tien_te": a.get("currency") or "VND", "token": tok, "kieu": "oauth",
                                   "trang_thai": a.get("account_status")})
                        thay.add(ma)
                url = ((j.get("paging") or {}).get("next")) or ""
                if not url:
                    break
        except Q.LoiNenTang:
            pass
    return ra


def _chon(nen: str, ds: list) -> list:
    """Tài khoản được quét: anh đã tick thì theo đó, chưa tick thì lấy các tài khoản đang hoạt động."""
    cd = (_doc_cai_dat().get(nen) or {}).get("tai_khoan")
    if cd is not None:
        return [a for a in ds if a["ma"] in cd]
    return [a for a in ds if a["kieu"] == "api" or a.get("trang_thai") == 1]


# ---------------------------------------------------------------- gọi Meta
def _goi(url: str) -> dict:
    """GET có chờ và thử lại khi Meta giới hạn số lần gọi."""
    for lan in range(4):
        j = Q._http("GET", url, thu=60)
        e = j.get("error") if isinstance(j, dict) else None
        if isinstance(e, dict) and e.get("code") in (4, 17, 32, 613, 80000, 80003, 80004) and lan < 3:
            time.sleep(20 * (lan + 1))
            continue
        if (m := Q._loi_fb(j)):
            raise Q.LoiNenTang(m)
        return j
    return {}


def _trang(url: str, toi_da: int = 60):
    for _ in range(toi_da):
        j = _goi(url)
        for r in j.get("data") or []:
            yield r
        url = ((j.get("paging") or {}).get("next")) or ""
        if not url:
            return


def _hd(ds) -> float:
    return sum(Q._so(a.get("value")) for a in (ds or []) if isinstance(a, dict))


def _tu_insight(r: dict) -> dict:
    tn = Q._fb_lay(r.get("actions"), Q._FB_TIN)
    mua = Q._fb_lay(r.get("actions"), Q._FB_MUA)
    return {"chi_phi": Q._so(r.get("spend")), "tiep_can": Q._so(r.get("reach")), "hien_thi": Q._so(r.get("impressions")), "bam": Q._so(r.get("clicks")),
            "chia_se": Q._fb_lay(r.get("actions"), ("post",)), "binh_luan": Q._fb_lay(r.get("actions"), ("comment",)), "tin_nhan": tn,
            "ket_qua": mua or Q._fb_lay(r.get("actions"), Q._FB_KHACH) or tn, "doanh_thu": Q._fb_lay(r.get("action_values"), Q._FB_MUA),
            "v25": _hd(r.get("video_p25_watched_actions")), "v50": _hd(r.get("video_p50_watched_actions")),
            "v75": _hd(r.get("video_p75_watched_actions")), "v100": _hd(r.get("video_p100_watched_actions"))}


_COT = ("chi_phi", "tiep_can", "hien_thi", "bam", "chia_se", "binh_luan", "tin_nhan", "ket_qua", "doanh_thu", "v25", "v50", "v75", "v100")


def _quet_tk(c: sqlite3.Connection, a: dict, tu: str, den: str, tien) -> int:
    """Quét một tài khoản: số liệu từng ngày từng nhóm quảng cáo trong [tu, den] và danh mục chiến dịch, nhóm. Trả số dòng ngày đã lưu."""
    ma, tok = a["ma"], a["token"]
    goc = "%s/%s/%s" % (Q.FB_GOC, Q.FB_PHIEN_BAN, ma)
    info = _goi(goc + "?" + urllib.parse.urlencode({"fields": "name,currency", "access_token": tok}))
    ten, tt = info.get("name") or a["ten"], info.get("currency") or a.get("tien_te") or "VND"
    le = 1 if tt.upper() in TIEN_KHONG_LE else 100
    # danh mục (cả nhóm đang bật mà chưa chi tiền)
    dm = []
    for r in _trang(goc + "/campaigns?" + urllib.parse.urlencode({"fields": "id,name,effective_status,daily_budget,lifetime_budget", "limit": 500, "access_token": tok})):
        dm.append(("cd", str(r.get("id")), str(r.get("id")), r.get("name") or "", str(r.get("effective_status") or "").upper(),
                   (Q._so(r.get("daily_budget")) or Q._so(r.get("lifetime_budget"))) / le))
    for r in _trang(goc + "/adsets?" + urllib.parse.urlencode({"fields": "id,name,campaign_id,effective_status,daily_budget,lifetime_budget", "limit": 500, "access_token": tok})):
        dm.append(("nhom", str(r.get("id")), str(r.get("campaign_id") or ""), r.get("name") or "", str(r.get("effective_status") or "").upper(),
                   (Q._so(r.get("daily_budget")) or Q._so(r.get("lifetime_budget"))) / le))
    # số liệu từng ngày, từng nhóm: chia đợt để mỗi lần hỏi không quá lớn
    dong_luu, a0, b0 = [], _dt.date.fromisoformat(tu), _dt.date.fromisoformat(den)
    d0 = a0
    while d0 <= b0:
        d1 = min(b0, d0 + _dt.timedelta(days=MOI_DOT - 1))
        tien("%s: lấy số %s đến %s" % (ten, d0.isoformat(), d1.isoformat()))
        truong = ("campaign_id,campaign_name,adset_id,adset_name,spend,impressions,reach,clicks,actions,action_values,"
                  "video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions")
        url = goc + "/insights?" + urllib.parse.urlencode({"level": "adset", "time_increment": 1, "limit": 500, "access_token": tok, "fields": truong,
                                                           "time_range": json.dumps({"since": d0.isoformat(), "until": d1.isoformat()})})
        for r in _trang(url, 120):
            ngay = str(r.get("date_start") or "")[:10]
            if not ngay:
                continue
            x = _tu_insight(r)
            dong_luu.append((a["ma"], ngay, str(r.get("campaign_id") or ""), str(r.get("adset_id") or r.get("campaign_id") or ""),
                             r.get("campaign_name") or "", r.get("adset_name") or "", x))
        d0 = d1 + _dt.timedelta(days=1)
    with c:   # một giao dịch: hoặc lưu đủ hoặc không đổi gì
        c.execute("DELETE FROM ngay_nhom WHERE nen='facebook' AND tk=? AND ngay BETWEEN ? AND ?", (ma, tu, den))
        c.executemany("INSERT OR REPLACE INTO ngay_nhom VALUES ('facebook',?,?,?,?,?,?," + ",".join("?" * len(_COT)) + ")",
                      [(m, ng, cd, nh, cdt, nht) + tuple(x[k] for k in _COT) for m, ng, cd, nh, cdt, nht, x in dong_luu])
        c.execute("DELETE FROM doi_tuong WHERE nen='facebook' AND tk=?", (ma,))
        c.executemany("INSERT OR REPLACE INTO doi_tuong VALUES ('facebook',?,?,?,?,?,?,?)", [(ma,) + d for d in dm])
        c.execute("INSERT OR REPLACE INTO tai_khoan VALUES ('facebook',?,?,?)", (ma, ten, tt))
        c.execute("INSERT INTO quet VALUES ('facebook',?,?,?,?,?)", (ma, tu, den, int(time.time()), len(dong_luu)))
    return len(dong_luu)


def quet(nen: str, tu: str, den: str) -> dict:
    """Quét đồng bộ (chạy trong luồng nền). Ném LoiNenTang nếu không quét được tài khoản nào."""
    if nen != "facebook":
        raise Q.LoiNenTang("Kho số liệu mới quét được Facebook / Meta. TikTok và Google Ads vẫn xem trực tiếp qua mã API.")
    ds = _chon(nen, _nguon_token(nen))
    if not ds:
        raise Q.LoiNenTang("Chưa có mã truy cập để quét. Nối Facebook ở Quảng Cáo > tab Kết nối, hoặc đăng nhập kết nối Meta Ads (tự tạo app, chỉ đọc).")
    tong, loi = 0, []
    with _khoa:
        t = _tien[nen] = {"dang": True, "msg": "bắt đầu quét", "buoc": 0, "tong": len(ds), "loi": "", "bat_dau": int(time.time()), "xong": 0, "tu": tu, "den": den}

    def tien(m):
        t["msg"] = m

    c = _noi()
    try:
        for i, a in enumerate(ds):
            t["buoc"] = i + 1
            try:
                tong += _quet_tk(c, a, tu, den, tien)
            except Q.LoiNenTang as e:
                loi.append("%s: %s" % (a["ten"], e))
            except Exception as e:  # noqa: BLE001
                loi.append("%s: lỗi %s" % (a["ten"], str(e)[:120]))
    finally:
        c.close()
        t["dang"] = False
        t["xong"] = int(time.time())
        t["loi"] = " | ".join(loi)[:600]
        t["msg"] = "đã lưu %d dòng số liệu" % tong
    if loi and not tong:
        raise Q.LoiNenTang(t["loi"])
    return {"so_dong": tong, "loi": loi}


def bat_dau(nen: str, kieu: str, tu: str = "", den: str = "") -> dict:
    """Mở một luồng quét nền rồi trả ngay. kieu: nhanh (7 ngày gần nhất + bù khoảng trống), 90-ngay, tuy-chon."""
    h = _dt.date.today()
    with _khoa:
        if (_tien.get(nen) or {}).get("dang"):
            return {"ok": True, "dang": True, "ghi_chu": "Đang quét rồi, chờ xong nhé."}
    if kieu == "90-ngay":
        a, b = h - _dt.timedelta(days=NGAY_NAP_LAN_DAU - 1), h
    elif kieu == "tuy-chon":
        try:
            a, b = _dt.date.fromisoformat(tu), _dt.date.fromisoformat(den)
        except ValueError:
            raise ValueError("Ngày không đúng dạng năm-tháng-ngày.")
        if a > b:
            a, b = b, a
        if (b - a).days > 400:
            raise ValueError("Mỗi lần quét tối đa khoảng 13 tháng.")
    else:
        pc = phu(nen)
        den_cuoi = _dt.date.fromisoformat(pc["den"]) if pc.get("den") else None
        a = min(h - _dt.timedelta(days=NGAY_BOI_LAI - 1), (den_cuoi - _dt.timedelta(days=NGAY_BOI_LAI - 1)) if den_cuoi else h)
        if not den_cuoi:
            a = h - _dt.timedelta(days=NGAY_NAP_LAN_DAU - 1)
        b = h

    def chay():
        try:
            quet(nen, a.isoformat(), b.isoformat())
        except Exception as e:  # noqa: BLE001
            with _khoa:
                t = _tien.setdefault(nen, {})
                t.update({"dang": False, "loi": str(e)[:600], "xong": int(time.time()), "msg": "lỗi"})

    threading.Thread(target=chay, name="tisa-qc-kho", daemon=True).start()
    return {"ok": True, "dang": True, "tu": a.isoformat(), "den": b.isoformat()}


# ---------------------------------------------------------------- đọc kho
def phu(nen: str, a: str = "", b: str = "") -> dict:
    """Kho đã phủ những ngày nào: {tu, den, luc, thieu: [ngày chưa quét trong [a, b]], so_dong}. Ngày "đã quét" = nằm trong
    một lần quét của MỌI tài khoản đang chọn."""
    c = _noi()
    try:
        tk = [r["tk"] for r in c.execute("SELECT DISTINCT tk FROM quet WHERE nen=?", (nen,))]
        chon = (_doc_cai_dat().get(nen) or {}).get("tai_khoan")
        if chon is not None:
            tk = [x for x in tk if x in chon]
        if not tk:
            return {"co": False, "tu": "", "den": "", "luc": 0, "thieu": [], "so_dong": 0, "tai_khoan": []}
        da = None
        luc = 0
        for m in tk:
            s = set()
            for r in c.execute("SELECT tu, den, luc FROM quet WHERE nen=? AND tk=?", (nen, m)):
                d0, d1 = _dt.date.fromisoformat(r["tu"]), _dt.date.fromisoformat(r["den"])
                for i in range((d1 - d0).days + 1):
                    s.add((d0 + _dt.timedelta(days=i)).isoformat())
                luc = max(luc, r["luc"])
            da = s if da is None else (da & s)
        da = sorted(da or [])
        n = c.execute("SELECT COUNT(*) FROM ngay_nhom WHERE nen=?", (nen,)).fetchone()[0]
        thieu = []
        if a and b:
            d0, d1 = _dt.date.fromisoformat(a), _dt.date.fromisoformat(b)
            ss = set(da)
            thieu = [(d0 + _dt.timedelta(days=i)).isoformat() for i in range((d1 - d0).days + 1) if (d0 + _dt.timedelta(days=i)).isoformat() not in ss]
        return {"co": bool(da), "tu": da[0] if da else "", "den": da[-1] if da else "", "luc": luc, "thieu": thieu, "so_dong": n, "tai_khoan": tk}
    finally:
        c.close()


def co_so(nen: str) -> bool:
    try:
        return bool(phu(nen)["co"])
    except Exception:  # noqa: BLE001
        return False


def _dm(c, nen, loai, tk=None):
    q = "SELECT * FROM doi_tuong WHERE nen=? AND loai=?" + (" AND tk=?" if tk else "")
    return {(r["tk"], r["id"]): r for r in c.execute(q, (nen, loai) + ((tk,) if tk else ()))}


def nguon(nen: str, a: _dt.date, b: _dt.date) -> dict:
    """{id nguồn: {nen, ten, tien_te, dong, chien_dich, kho}}: mỗi tài khoản một nguồn, dòng theo ngày và chiến dịch (cho _gom).
    Chiến dịch đang bật mà chưa chi tiền trong kỳ vẫn có một dòng số 0, để bảng liệt kê đủ."""
    c = _noi()
    ra = {}
    try:
        pc = phu(nen)
        tk_ds = pc.get("tai_khoan") or []
        cd_dm = _dm(c, nen, "cd")
        for m in tk_ds:
            t = c.execute("SELECT * FROM tai_khoan WHERE nen=? AND tk=?", (nen, m)).fetchone()
            dong, co = [], set()
            for r in c.execute("SELECT ngay, cd_id, MAX(cd) AS cd, SUM(chi_phi) AS chi_phi, SUM(hien_thi) AS hien_thi, SUM(bam) AS bam, SUM(ket_qua) AS ket_qua, "
                               "SUM(doanh_thu) AS doanh_thu FROM ngay_nhom WHERE nen=? AND tk=? AND ngay BETWEEN ? AND ? GROUP BY ngay, cd_id",
                               (nen, m, a.isoformat(), b.isoformat())):
                dong.append(Q.dong(r["ngay"], r["cd_id"], r["cd"], r["chi_phi"], r["hien_thi"], r["bam"], r["ket_qua"], r["doanh_thu"]))
                co.add(r["cd_id"])
            chien = {}
            for (tk_, cid), e in cd_dm.items():
                if tk_ != m:
                    continue
                chien[cid] = {"trang_thai": e["trang_thai"], "ngan_sach_ngay": e["ngan_sach"] or 0}
                if cid not in co and e["trang_thai"] == "ACTIVE":
                    dong.append(Q.dong(b.isoformat(), cid, e["ten"]))
            ra["kho-%s-%s" % (nen, m)] = {"nen": nen, "ten": (t["ten"] if t else m), "tien_te": (t["tien_te"] if t else "VND"), "dong": dong, "chien_dich": chien,
                                          "kho": True, "mcp": False}
    finally:
        c.close()
    return ra


def bang(nen: str, a: _dt.date, b: _dt.date, cap: str) -> list:
    """Bảng 19 chỉ số: mỗi nhóm quảng cáo (hoặc chiến dịch) một dòng, cộng cả kỳ. Nhóm đang bật mà chưa có số vẫn hiện (số 0).
    Người tiếp cận cộng theo ngày nên lớn hơn số thật của Meta một chút (Meta đếm mỗi người một lần cả kỳ)."""
    c = _noi()
    out = []
    try:
        pc = phu(nen)
        nhom = cap != "chien-dich"
        dm_nhom, dm_cd = _dm(c, nen, "nhom"), _dm(c, nen, "cd")
        for m in pc.get("tai_khoan") or []:
            t = c.execute("SELECT * FROM tai_khoan WHERE nen=? AND tk=?", (nen, m)).fetchone()
            ten_tk, tien_te = (t["ten"] if t else m), (t["tien_te"] if t else "VND")
            khoa = "nhom_id" if nhom else "cd_id"
            tong = {}
            sql = ("SELECT cd_id, MAX(cd) AS cd, " + ("nhom_id, MAX(nhom) AS nhom, " if nhom else "") + ",".join("SUM(%s) AS %s" % (k, k) for k in _COT) +
                   " FROM ngay_nhom WHERE nen=? AND tk=? AND ngay BETWEEN ? AND ? GROUP BY " + ("nhom_id" if nhom else "cd_id"))
            for r in c.execute(sql, (nen, m, a.isoformat(), b.isoformat())):
                e = (dm_nhom.get((m, r["nhom_id"])) if nhom else dm_cd.get((m, r["cd_id"])))
                x = B.dong(nen, ten_tk, r["cd_id"], r["cd"], r["nhom_id"] if nhom else "", (r["nhom"] if nhom else ""), tien_te,
                           **{k: r[k] for k in _COT})
                x["trang_thai"], x["ngan_sach"], x["tk_id"] = (e["trang_thai"] if e else ""), ((e["ngan_sach"] or 0) if e else 0.0), m
                tong[r[khoa]] = x
            if nhom:
                for (tk_, nid), e in dm_nhom.items():
                    if tk_ != m or nid in tong or e["trang_thai"] != "ACTIVE":
                        continue
                    cd = dm_cd.get((m, e["cd_id"]))
                    x = B.dong(nen, ten_tk, e["cd_id"], (cd["ten"] if cd else e["cd_id"]), nid, e["ten"], tien_te)
                    x["trang_thai"], x["ngan_sach"], x["tk_id"] = e["trang_thai"], e["ngan_sach"] or 0.0, m
                    tong[nid] = x
            else:
                for (tk_, cid), e in dm_cd.items():
                    if tk_ != m or cid in tong or e["trang_thai"] != "ACTIVE":
                        continue
                    x = B.dong(nen, ten_tk, cid, e["ten"], "", "", tien_te)
                    x["trang_thai"], x["ngan_sach"], x["tk_id"] = e["trang_thai"], e["ngan_sach"] or 0.0, m
                    tong[cid] = x
            out += list(tong.values())
    finally:
        c.close()
    return out


_khoa_bai = threading.Lock()
NGAY_LAM_MOI_BAI = 2         # số của vài ngày gần nhất còn đổi: xem bài quảng cáo thì quét lại các ngày này nếu đã cũ
PHUT_BAI_CU = 15


def _quet_bai(c: sqlite3.Connection, a: dict, cd_id: str, tu: str, den: str) -> int:
    """Lấy số liệu từng ngày từng BÀI quảng cáo của một chiến dịch trong [tu, den] và lưu vào kho (chỉ đọc)."""
    ma, tok = a["ma"], a["token"]
    goc = "%s/%s/%s" % (Q.FB_GOC, Q.FB_PHIEN_BAN, ma)
    truong = ("campaign_id,adset_id,adset_name,ad_id,ad_name,spend,impressions,reach,clicks,actions,action_values,"
              "video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions")
    loc = json.dumps([{"field": "campaign.id", "operator": "EQUAL", "value": cd_id}])
    dong_luu, d0, b0 = [], _dt.date.fromisoformat(tu), _dt.date.fromisoformat(den)
    while d0 <= b0:
        d1 = min(b0, d0 + _dt.timedelta(days=MOI_DOT - 1))
        url = goc + "/insights?" + urllib.parse.urlencode({"level": "ad", "time_increment": 1, "limit": 500, "access_token": tok, "fields": truong, "filtering": loc,
                                                           "time_range": json.dumps({"since": d0.isoformat(), "until": d1.isoformat()})})
        for r in _trang(url, 120):
            ngay = str(r.get("date_start") or "")[:10]
            if ngay and r.get("ad_id"):
                dong_luu.append((ngay, str(r.get("adset_id") or ""), str(r["ad_id"]), r.get("ad_name") or "", _tu_insight(r)))
        d0 = d1 + _dt.timedelta(days=1)
    with c:
        c.execute("DELETE FROM ngay_bai WHERE nen='facebook' AND tk=? AND cd_id=? AND ngay BETWEEN ? AND ?", (ma, cd_id, tu, den))
        c.executemany("INSERT OR REPLACE INTO ngay_bai VALUES ('facebook',?,?,?,?,?,?," + ",".join("?" * len(_COT)) + ")",
                      [(ma, ng, cd_id, nh, bid, ten) + tuple(x[k] for k in _COT) for ng, nh, bid, ten, x in dong_luu])
        c.execute("INSERT INTO quet_bai VALUES ('facebook',?,?,?,?,?)", (ma, cd_id, tu, den, int(time.time())))
    return len(dong_luu)


def bai_qc(nen: str, tk: str, cd_id: str, a: _dt.date, b: _dt.date) -> dict:
    """Các BÀI quảng cáo của một chiến dịch trong kỳ [a, b]: mỗi bài một dòng 19 chỉ số, kèm ảnh nhỏ, nhóm chứa nó, trạng thái.
    Lần đầu xem một chiến dịch thì hỏi Meta rồi LƯU vào kho; lần sau đọc kho (chỉ quét thêm ngày còn thiếu và vài ngày gần nhất nếu đã cũ)."""
    if nen != "facebook":
        raise Q.LoiNenTang("Xem từng bài quảng cáo hiện mới có cho Facebook / Meta.")
    nguon_ = [x for x in _nguon_token(nen) if x["ma"] == tk]
    if not nguon_:
        raise Q.LoiNenTang("Chưa có mã truy cập cho tài khoản quảng cáo này nên chưa lấy được bài quảng cáo.")
    a_tk = nguon_[0]
    cd_id = str(cd_id)
    with _khoa_bai:
        c = _noi()
        try:
            da, luc = set(), 0
            for r in c.execute("SELECT tu, den, luc FROM quet_bai WHERE nen=? AND tk=? AND cd_id=?", (nen, tk, cd_id)):
                d0, d1 = _dt.date.fromisoformat(r["tu"]), _dt.date.fromisoformat(r["den"])
                for i in range((d1 - d0).days + 1):
                    da.add((d0 + _dt.timedelta(days=i)).isoformat())
                luc = max(luc, r["luc"])
            h = _dt.date.today()
            ngay_ky = [(a + _dt.timedelta(days=i)) for i in range((b - a).days + 1)]
            thieu = [d for d in ngay_ky if d.isoformat() not in da]
            if time.time() - luc > PHUT_BAI_CU * 60:
                thieu += [d for d in ngay_ky if d >= h - _dt.timedelta(days=NGAY_LAM_MOI_BAI) and d not in thieu]
            if thieu:
                _quet_bai(c, a_tk, cd_id, min(thieu).isoformat(), max(thieu).isoformat())
            ten_tk_row = c.execute("SELECT * FROM tai_khoan WHERE nen=? AND tk=?", (nen, tk)).fetchone()
            ten_tk, tien_te = (ten_tk_row["ten"] if ten_tk_row else a_tk["ten"]), (ten_tk_row["tien_te"] if ten_tk_row else (a_tk.get("tien_te") or "VND"))
            nhom_dm = {r["id"]: r["ten"] for r in c.execute("SELECT id, ten FROM doi_tuong WHERE nen=? AND tk=? AND loai='nhom'", (nen, tk))}
            cd_row = c.execute("SELECT ten FROM doi_tuong WHERE nen=? AND tk=? AND loai='cd' AND id=?", (nen, tk, cd_id)).fetchone()
            cd_ten = cd_row["ten"] if cd_row else cd_id
            tong = {}
            sql = ("SELECT bai_id, MAX(bai) AS bai, MAX(nhom_id) AS nhom_id, " + ",".join("SUM(%s) AS %s" % (k, k) for k in _COT) +
                   " FROM ngay_bai WHERE nen=? AND tk=? AND cd_id=? AND ngay BETWEEN ? AND ? GROUP BY bai_id")
            for r in c.execute(sql, (nen, tk, cd_id, a.isoformat(), b.isoformat())):
                x = B.dong(nen, ten_tk, cd_id, cd_ten, r["nhom_id"], nhom_dm.get(r["nhom_id"], ""), tien_te, **{k: r[k] for k in _COT})
                x.update({"bai_id": r["bai_id"], "bai": r["bai"] or r["bai_id"], "tk_id": tk, "trang_thai": "", "thumb": ""})
                tong[r["bai_id"]] = x
        finally:
            c.close()
    # Danh mục bài của chiến dịch (tên, trạng thái, ảnh nhỏ): gọi trực tiếp, nhẹ, và ảnh nhỏ của Meta có hạn nên không lưu.
    try:
        url = "%s/%s/%s/ads?%s" % (Q.FB_GOC, Q.FB_PHIEN_BAN, cd_id, urllib.parse.urlencode(
            {"fields": "id,name,adset_id,effective_status,creative{thumbnail_url}", "limit": 200, "access_token": a_tk["token"]}))
        for r in _trang(url, 20):
            bid = str(r.get("id"))
            tt = str(r.get("effective_status") or "").upper()
            thumb = ((r.get("creative") or {}).get("thumbnail_url")) or ""
            x = tong.get(bid)
            if x is None:
                if tt != "ACTIVE":
                    continue   # bài tắt mà không có số trong kỳ thì không cần liệt kê
                nhom_id = str(r.get("adset_id") or "")
                x = B.dong(nen, "", cd_id, "", nhom_id, "", "VND")
                x.update({"bai_id": bid, "bai": r.get("name") or bid, "tk_id": tk})
                tong[bid] = x
            x["trang_thai"], x["thumb"] = tt, thumb
            if r.get("name"):
                x["bai"] = r["name"]
            if r.get("adset_id"):
                x["nhom_id"] = str(r["adset_id"])
    except Q.LoiNenTang:
        pass
    ds = B.hoan_tat(list(tong.values()))
    return {"bai": ds, "tong": B.tong(ds), "luc": int(time.time())}


def tom_tat(a: str = "", b: str = "") -> dict:
    """Cho trang: từng nền tảng có kho hay chưa, kho phủ tới đâu, kỳ đang xem thiếu ngày nào, đang quét tới đâu, tài khoản nào được chọn."""
    ra = {}
    for nen in Q.NEN:
        if nen != "facebook":
            continue
        try:
            pc = phu(nen, a, b)
        except Exception as e:  # noqa: BLE001
            pc = {"co": False, "tu": "", "den": "", "luc": 0, "thieu": [], "so_dong": 0, "loi": str(e)[:100]}
        with _khoa:
            t = dict(_tien.get(nen) or {})
        ra[nen] = {"co": pc["co"], "tu": pc["tu"], "den": pc["den"], "luc": pc["luc"], "thieu": pc["thieu"][:60], "so_thieu": len(pc["thieu"]), "so_dong": pc["so_dong"],
                   "tien": t}
    return ra


def tai_khoan_co_the(nen: str) -> dict:
    ds = _nguon_token(nen)
    chon = {a["ma"] for a in _chon(nen, ds)}
    return {"co_ma": bool(ds), "tai_khoan": [{"ma": a["ma"], "ten": a["ten"], "tien_te": a["tien_te"], "trang_thai": a.get("trang_thai"), "chon": a["ma"] in chon,
                                              "kieu": a["kieu"]} for a in ds]}


# ---------------------------------------------------------------- tự đồng bộ nền
def _vong_tu_dong() -> None:
    time.sleep(90)
    while True:
        try:
            if os.getenv("TISA_QC_TU_DONG", "1") != "0" and _nguon_token("facebook"):
                bat_dau("facebook", "nhanh")
        except Exception as e:  # noqa: BLE001
            print(f"[tisa_quang_cao_kho] tự đồng bộ lỗi: {type(e).__name__}: {e}")
        time.sleep(GIO_TU_DONG)


_da_chay = False


def gan(app) -> None:
    global _da_chay
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=ma)

    @app.get("/tisa-quang-cao/api/kho")
    async def _tt(request: Request):
        q = request.query_params
        d = await asyncio.to_thread(tom_tat, q.get("tu", ""), q.get("den", ""))
        return {"ok": True, "kho": d}

    @app.get("/tisa-quang-cao/api/kho/tai-khoan")
    async def _tk(nen: str = "facebook"):
        return {"ok": True, **(await asyncio.to_thread(tai_khoan_co_the, nen))}

    @app.get("/tisa-quang-cao/api/bai")
    async def _bai(request: Request):
        q = request.query_params
        try:
            a, b = _dt.date.fromisoformat(q.get("tu", "")), _dt.date.fromisoformat(q.get("den", ""))
        except ValueError:
            return loi("Thiếu hoặc sai khoảng ngày.")
        try:
            d = await asyncio.to_thread(bai_qc, q.get("nen", "facebook"), q.get("tk", ""), q.get("cd", ""), a, b)
        except Q.LoiNenTang as e:
            return loi(str(e))
        except Exception as e:  # noqa: BLE001
            return loi("Không lấy được bài quảng cáo: %s" % str(e)[:160], 500)
        return {"ok": True, **d}

    @app.post("/tisa-quang-cao/api/kho/dong-bo")
    async def _db(request: Request):
        d = await request.json()
        try:
            return await asyncio.to_thread(bat_dau, str(d.get("nen") or "facebook"), str(d.get("kieu") or "nhanh"), str(d.get("tu") or ""), str(d.get("den") or ""))
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/kho/chon")
    async def _chon_api(request: Request):
        d = await request.json()
        chon_tai_khoan(str(d.get("nen") or "facebook"), d.get("tai_khoan") if isinstance(d.get("tai_khoan"), list) else None)
        return {"ok": True}

    if not _da_chay:
        _da_chay = True
        threading.Thread(target=_vong_tu_dong, name="tisa-qc-kho-tu-dong", daemon=True).start()
