"""tisa_quang_cao_bang.py - bảng chỉ số chi tiết của trang Quảng Cáo (V2.78), theo cách xem của Trình quản lý quảng cáo Meta.

Mỗi dòng là một chiến dịch hoặc một nhóm quảng cáo, cả kỳ đã chọn (không chia ngày), gồm 19 chỉ số:
  phân phối, tên nhóm, ngân sách, số tiền đã chi, người tiếp cận, lượt hiển thị, tần suất, lượt chia sẻ, bình luận,
  lượt bắt đầu trò chuyện qua tin nhắn, chi phí mỗi lượt trò chuyện, kết quả, chi phí mỗi kết quả, CPM, CTR (tất cả),
  lượt phát 25%, 50%, 75%, 100% video; thêm lượt bấm, CPC, doanh thu, ROAS.
Chỉ số nền tảng nào không có thì để 0 và trang hiện dấu gạch. Số tổng tính lại từ số thô, CÙNG MỘT công thức cho mọi nền tảng.
Chỉ đọc, giống phần còn lại của trang.
"""
from __future__ import annotations

import datetime as _dt
import json
import urllib.parse

import tisa_quang_cao as Q

_CONG = ("chi_phi", "tiep_can", "hien_thi", "bam", "chia_se", "binh_luan", "tin_nhan", "ket_qua", "doanh_thu", "v25", "v50", "v75", "v100")


def dong(nen, tk, cd_id, cd, nhom_id="", nhom="", tien_te="VND", **kw) -> dict:
    r = {"nen": nen, "tk_ten": tk, "cd_id": str(cd_id), "cd": cd or str(cd_id), "nhom_id": str(nhom_id or ""), "nhom": nhom or "", "tien_te": tien_te,
         "trang_thai": "", "ngan_sach": 0.0, "tan_suat": 0.0}
    for k in _CONG:
        r[k] = 0.0
    for k, v in kw.items():
        r[k] = Q._so(v) if k not in ("trang_thai",) else v
    return r


def chi_so(r: dict) -> dict:
    """CTR, CPM, CPC, giá mỗi kết quả, giá mỗi lượt trò chuyện, ROAS, tần suất: tính lại từ số thô."""
    cp, ht, bam, kq, tn = r["chi_phi"], r["hien_thi"], r["bam"], r["ket_qua"], r["tin_nhan"]
    r["ctr"] = (bam / ht * 100) if ht else 0.0
    r["cpm"] = (cp / ht * 1000) if ht else 0.0
    r["cpc"] = (cp / bam) if bam else 0.0
    r["cpa"] = (cp / kq) if kq else 0.0
    r["cp_tin_nhan"] = (cp / tn) if tn else 0.0
    r["roas"] = (r["doanh_thu"] / cp) if cp and r["doanh_thu"] else 0.0
    if r["tiep_can"] and ht and not r["tan_suat"]:
        r["tan_suat"] = ht / r["tiep_can"]
    return r


def tong(ds: list) -> dict:
    t = dong("", "", "", "Tổng cộng")
    for r in ds:
        for k in _CONG:
            t[k] += r[k]
    # Người tiếp cận không cộng được giữa các dòng (một người có thể thấy nhiều nhóm): tổng chỉ để tham khảo, nên bỏ trống nếu có nhiều dòng.
    if len(ds) > 1:
        t["tiep_can"] = 0.0
    return chi_so(t)


# ---------------------------------------------------------------- Facebook
def _tong_hd(ds) -> float:
    return sum(Q._so(a.get("value")) for a in (ds or []) if isinstance(a, dict))


def _bang_fb(tk, bm, tu, den, cap):
    ma, ver, token = tk["ma_tk"], tk.get("phien_ban") or Q.FB_PHIEN_BAN, bm.get("token", "")
    goc = "%s/%s/%s" % (Q.FB_GOC, ver, ma)
    nhom = cap == "nhom"
    info = Q._http("GET", goc + "?" + urllib.parse.urlencode({"fields": "name,currency", "access_token": token}))
    if (m := Q._loi_fb(info)):
        raise Q.LoiNenTang(m)
    tien_te, ten_tk = info.get("currency") or "VND", info.get("name") or ""
    truong = ("campaign_id,campaign_name,spend,impressions,reach,frequency,clicks,actions,action_values,"
              "video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions") + (",adset_id,adset_name" if nhom else "")
    url = goc + "/insights?" + urllib.parse.urlencode({"level": "adset" if nhom else "campaign", "limit": 500, "access_token": token, "fields": truong,
                                                       "time_range": json.dumps({"since": tu, "until": den})})
    rows = []
    for _ in range(40):
        j = Q._http("GET", url)
        if (m := Q._loi_fb(j)):
            raise Q.LoiNenTang(m)
        for r in j.get("data") or []:
            mua = Q._fb_lay(r.get("actions"), Q._FB_MUA)
            tn = Q._fb_lay(r.get("actions"), Q._FB_TIN)
            kq = mua or Q._fb_lay(r.get("actions"), Q._FB_KHACH) or tn
            x = dong("facebook", ten_tk, r.get("campaign_id"), r.get("campaign_name"), r.get("adset_id"), r.get("adset_name") if nhom else "", tien_te,
                     chi_phi=r.get("spend"), hien_thi=r.get("impressions"), tiep_can=r.get("reach"), tan_suat=r.get("frequency"), bam=r.get("clicks"),
                     chia_se=Q._fb_lay(r.get("actions"), ("post",)), binh_luan=Q._fb_lay(r.get("actions"), ("comment",)), tin_nhan=tn, ket_qua=kq,
                     doanh_thu=Q._fb_lay(r.get("action_values"), Q._FB_MUA), v25=_tong_hd(r.get("video_p25_watched_actions")), v50=_tong_hd(r.get("video_p50_watched_actions")),
                     v75=_tong_hd(r.get("video_p75_watched_actions")), v100=_tong_hd(r.get("video_p100_watched_actions")))
            rows.append(x)
        url = ((j.get("paging") or {}).get("next")) or ""
        if not url:
            break
    ent = {}
    j = Q._http("GET", goc + ("/adsets" if nhom else "/campaigns") + "?" + urllib.parse.urlencode({
        "fields": ("id,name,campaign_id,effective_status,daily_budget,lifetime_budget" if nhom else "id,name,effective_status,daily_budget,lifetime_budget"), "limit": 500, "access_token": token}))
    for e in j.get("data") or []:
        ent[str(e.get("id"))] = {"trang_thai": str(e.get("effective_status") or "").upper(), "ngan_sach": Q._so(e.get("daily_budget")) or Q._so(e.get("lifetime_budget"))}
    for r in rows:
        e = ent.get(r["nhom_id"] if nhom else r["cd_id"]) or {}
        r["trang_thai"], r["ngan_sach"] = e.get("trang_thai", ""), e.get("ngan_sach", 0.0)
    return rows


# ---------------------------------------------------------------- TikTok
def _bang_tiktok(tk, bm, tu, den, cap):
    ma, h = tk["ma_tk"], {"Access-Token": bm.get("token", "")}
    base = Q.TT_GOC + "/open_api/v1.3"
    nhom = cap == "nhom"
    # Thử bộ số đầy đủ trước, nền tảng báo sai tên số thì lùi dần (tên số khác nhau theo loại tài khoản).
    tap = [["campaign_name", "adgroup_name", "spend", "impressions", "reach", "frequency", "clicks", "conversion", "shares", "comments", "video_views_p25", "video_views_p50", "video_views_p75", "video_views_p100", "total_purchase_value"],
           ["campaign_name", "adgroup_name", "spend", "impressions", "reach", "frequency", "clicks", "conversion", "shares", "comments", "video_views_p25", "video_views_p50", "video_views_p75", "video_views_p100"],
           ["campaign_name", "adgroup_name", "spend", "impressions", "reach", "clicks", "conversion"], ["campaign_name", "adgroup_name", "spend", "impressions", "clicks", "conversion"]]
    rows, loi_cuoi = [], None
    for so_do in tap:
        rows, trang, loi_cuoi = [], 1, None
        so_do = [m for m in so_do if nhom or m != "adgroup_name"]
        while trang <= 40:
            q = {"advertiser_id": ma, "report_type": "BASIC", "data_level": "AUCTION_ADGROUP" if nhom else "AUCTION_CAMPAIGN",
                 "dimensions": json.dumps(["adgroup_id"] if nhom else ["campaign_id"]), "metrics": json.dumps(so_do), "start_date": tu, "end_date": den, "page": trang, "page_size": 1000}
            j = Q._http("GET", base + "/report/integrated/get/?" + urllib.parse.urlencode(q), headers=h)
            if j.get("code") not in (None, 0):
                loi_cuoi = j
                break
            d = j.get("data") or {}
            for r in d.get("list") or []:
                dm, m = r.get("dimensions") or {}, r.get("metrics") or {}
                rows.append(dong("tiktok", "", m.get("campaign_id") or dm.get("campaign_id") or "", m.get("campaign_name"), dm.get("adgroup_id", ""), m.get("adgroup_name") if nhom else "", "VND",
                                 chi_phi=m.get("spend"), hien_thi=m.get("impressions"), tiep_can=m.get("reach"), tan_suat=m.get("frequency"), bam=m.get("clicks"), ket_qua=m.get("conversion"),
                                 chia_se=m.get("shares"), binh_luan=m.get("comments"), doanh_thu=m.get("total_purchase_value"), v25=m.get("video_views_p25"), v50=m.get("video_views_p50"),
                                 v75=m.get("video_views_p75"), v100=m.get("video_views_p100")))
            if trang >= int((d.get("page_info") or {}).get("total_page") or 1):
                break
            trang += 1
        if loi_cuoi is None:
            break
        if loi_cuoi.get("code") in (40100, 40101, 40102, 40104, 40105, 40001):
            break
    if loi_cuoi is not None:
        raise Q.LoiNenTang(Q._loi_tt(loi_cuoi) or "TikTok báo lỗi.")
    info = Q._http("GET", base + "/advertiser/info/?" + urllib.parse.urlencode({"advertiser_ids": json.dumps([ma]), "fields": json.dumps(["name", "currency"])}), headers=h)
    ds = ((info.get("data") or {}).get("list") or [{}]) if info.get("code") in (None, 0) else [{}]
    tien_te, ten_tk = ds[0].get("currency") or "VND", ds[0].get("name") or ""
    ent = {}
    j = Q._http("GET", base + ("/adgroup/get/" if nhom else "/campaign/get/") + "?" + urllib.parse.urlencode({
        "advertiser_id": ma, "page_size": 1000, "fields": json.dumps(["adgroup_id", "adgroup_name", "campaign_id", "operation_status", "budget"] if nhom else ["campaign_id", "campaign_name", "operation_status", "budget"])}), headers=h)
    if j.get("code") in (None, 0):
        for e in (j.get("data") or {}).get("list") or []:
            ent[str(e.get("adgroup_id") if nhom else e.get("campaign_id"))] = {"trang_thai": "ACTIVE" if e.get("operation_status") == "ENABLE" else str(e.get("operation_status") or "").upper(),
                                                                                "ngan_sach": Q._so(e.get("budget")), "cd_id": str(e.get("campaign_id") or ""), "cd": e.get("campaign_name") or ""}
    for r in rows:
        e = ent.get(r["nhom_id"] if nhom else r["cd_id"]) or {}
        r["trang_thai"], r["ngan_sach"], r["tien_te"], r["tk_ten"] = e.get("trang_thai", ""), e.get("ngan_sach", 0.0), tien_te, ten_tk
        if nhom and e.get("cd") and (not r["cd"] or r["cd"] == r["cd_id"]):
            r["cd"], r["cd_id"] = e["cd"], e.get("cd_id", r["cd_id"])
    return rows


# ---------------------------------------------------------------- Google Ads
def _bang_google(tk, bm, tu, den, cap):
    cid, ver = tk["ma_tk"], tk.get("phien_ban") or Q.GG_PHIEN_BAN
    h = {"Authorization": "Bearer " + Q._gg_token(bm), "developer-token": bm.get("developer_token", "")}
    if bm.get("login_customer_id"):
        h["login-customer-id"] = bm["login_customer_id"]
    url = "%s/%s/customers/%s/googleAds:search" % (Q.GG_GOC, ver, cid)
    nhom = cap == "nhom"

    def hoi(gaql):
        ra, tok = [], ""
        for _ in range(60):
            body = {"query": gaql, "pageSize": 10000}
            if tok:
                body["pageToken"] = tok
            j = Q._http("POST", url, headers=h, data=body)
            if (m := Q._loi_gg(j)):
                raise Q.LoiNenTang(m)
            ra += j.get("results") or []
            tok = j.get("nextPageToken") or ""
            if not tok:
                break
        return ra

    kh = hoi("SELECT customer.currency_code, customer.descriptive_name FROM customer LIMIT 1")
    c0 = (kh[0].get("customer") if kh else {}) or {}
    tien_te, ten_tk = c0.get("currencyCode") or "VND", c0.get("descriptiveName") or ""
    q = ("SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros, " + ("ad_group.id, ad_group.name, ad_group.status, " if nhom else "") +
         "metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.conversions_value, metrics.video_views, "
         "metrics.video_quartile_p25_rate, metrics.video_quartile_p50_rate, metrics.video_quartile_p75_rate, metrics.video_quartile_p100_rate "
         "FROM " + ("ad_group" if nhom else "campaign") + " WHERE segments.date BETWEEN '%s' AND '%s' AND campaign.status != 'REMOVED'" % (tu, den))
    rows = []
    for r in hoi(q):
        c, m, g = r.get("campaign") or {}, r.get("metrics") or {}, r.get("adGroup") or {}
        xem = Q._so(m.get("videoViews"))
        x = dong("google", ten_tk, c.get("id"), c.get("name"), g.get("id", ""), g.get("name", "") if nhom else "", tien_te,
                 chi_phi=Q._so(m.get("costMicros")) / 1e6, hien_thi=m.get("impressions"), bam=m.get("clicks"), ket_qua=m.get("conversions"), doanh_thu=m.get("conversionsValue"),
                 v25=xem * Q._so(m.get("videoQuartileP25Rate")), v50=xem * Q._so(m.get("videoQuartileP50Rate")), v75=xem * Q._so(m.get("videoQuartileP75Rate")), v100=xem * Q._so(m.get("videoQuartileP100Rate")),
                 ngan_sach=Q._so((r.get("campaignBudget") or {}).get("amountMicros")) / 1e6)
        x["trang_thai"] = str((g.get("status") if nhom and g.get("status") else c.get("status")) or "").upper()
        rows.append(x)
    return rows


_LAY = {"facebook": _bang_fb, "tiktok": _bang_tiktok, "google": _bang_google}


def lay_bang(tk: dict, tu: str, den: str, cap: str, lam_moi: bool = False) -> list:
    khoa = "%s|bang|%s|%s|%s" % (tk["id"], cap, tu, den)
    with Q._khoa:
        c = Q._nho.get(khoa)
        if c and not lam_moi and Q.time.time() - c[0] < Q.NHO_GIAY:
            return c[1]
    rows = _LAY[tk["nen"]](tk, Q._bi_mat(tk), tu, den, cap)
    for r in rows:
        r["tk_ten"] = tk.get("ten") or r["tk_ten"] or tk["ma_tk"]
        r["tk_id"] = tk["id"]
    with Q._khoa:
        Q._nho[khoa] = (Q.time.time(), rows)
    return rows


# ---------------------------------------------------------------- số mẫu
def bang_mau(a: _dt.date, b: _dt.date, cap: str, nen: str = "") -> list:
    """Dựng bảng mẫu từ số mẫu theo ngày, chia mỗi chiến dịch thành 1 đến 3 nhóm quảng cáo."""
    out = []
    for n, d in Q.so_mau(a.isoformat(), b.isoformat()).items():
        if nen and n != nen:
            continue
        theo = {}
        for r in d["dong"]:
            c = theo.setdefault(r["cd_id"], {"cd": r["cd"], "chi_phi": 0.0, "hien_thi": 0.0, "bam": 0.0, "ket_qua": 0.0, "doanh_thu": 0.0})
            for k in ("chi_phi", "hien_thi", "bam", "ket_qua", "doanh_thu"):
                c[k] += r[k]
        for cid, c in theo.items():
            st = (d["chien_dich"].get(cid) or {})
            so_nhom = (1 + int(Q._hat(cid, "n") * 3)) if cap == "nhom" else 1
            ten_nhom = ["Đối tượng quan tâm", "Đối tượng tương tự", "Khách đã tương tác"]
            trong = [0.5 + Q._hat(cid, j) for j in range(so_nhom)]
            tt = sum(trong)
            for j in range(so_nhom):
                f = trong[j] / tt
                ht = c["hien_thi"] * f
                tan = 1.15 + Q._hat(cid, j, "tan") * 1.6
                bam = c["bam"] * f
                kq = round(c["ket_qua"] * f)
                tn = round(kq * 0.9) if n == "facebook" and c["doanh_thu"] == 0 else round(kq * 0.15)
                v = ht * 0.32 if (n != "google") else ht * 0.2
                x = dong(n, "Dữ liệu mẫu", cid, c["cd"], "%s-%d" % (cid, j) if cap == "nhom" else "", ("%s %d" % (ten_nhom[j % 3], j + 1)) if cap == "nhom" else "", "VND",
                         chi_phi=c["chi_phi"] * f, hien_thi=ht, tiep_can=ht / tan, tan_suat=tan, bam=bam, chia_se=bam * (0.006 + Q._hat(cid, j, "s") * 0.01), binh_luan=bam * (0.012 + Q._hat(cid, j, "b") * 0.02),
                         tin_nhan=tn if n != "google" else 0, ket_qua=kq, doanh_thu=c["doanh_thu"] * f, v25=v, v50=v * 0.62, v75=v * 0.4, v100=v * 0.21,
                         ngan_sach=(st.get("ngan_sach_ngay") or 0) * f)
                x["trang_thai"] = st.get("trang_thai") or "ACTIVE"
                x["tk_ten"] = "Dữ liệu mẫu"
                out.append(x)
    return out


def hoan_tat(rows: list) -> list:
    for r in rows:
        chi_so(r)
    rows.sort(key=lambda r: -r["chi_phi"])
    return rows
