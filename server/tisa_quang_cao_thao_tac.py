"""tisa_quang_cao_thao_tac.py - bật, tắt và đổi ngân sách quảng cáo TỪ trang Quảng Cáo, luôn có xác nhận (V2.78).

Rào chặn (làm theo tinh thần công cụ ghi có xác nhận của chủ):
  - Mặc định MỌI tài khoản chỉ đọc. Chủ phải tự bật công tắc "Cho phép bật, tắt, đổi ngân sách" cho từng tài khoản.
  - Mỗi thao tác đi hai bước: CHUẨN BỊ (máy chủ đọc trạng thái thật từ nền tảng, lập đề xuất có mã, hiệu lực 15 phút, dùng một lần)
    rồi XÁC NHẬN (chủ gõ đúng câu "XÁC NHẬN QC <mã>"). Chưa gõ đúng thì không làm gì.
  - Chỉ có 3 việc: bật, tắt, đổi ngân sách ngày của một chiến dịch hoặc một nhóm quảng cáo. Không tạo, không xoá, không đổi nội dung,
    không chuyển ngân sách ngày sang trọn đời. Tạo chiến dịch mới đi qua trợ lý và luôn ở trạng thái tạm dừng.
  - Tăng ngân sách tối đa 50% mỗi lần (muốn tăng nhiều thì tăng từng bước). Có đặt "chi tối đa mỗi ngày" thì ngân sách mới không được vượt.
  - Làm xong đọc lại từ nền tảng để chắc, ghi nhật ký (thời gian, trước, sau, kết quả). Không ghi mã truy cập vào nhật ký.
  - Không tự thử lại khi lỗi. Mất mạng giữa chừng thì báo "cần đối chiếu", chủ xem lại trạng thái thật rồi mới làm tiếp.
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
import time
import urllib.parse

import tisa_quang_cao as Q

try:   # đứng ở đầu tệp: FastAPI đọc chú thích kiểu theo tên toàn cục
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

TEP_NHAT_KY = Q.KHO / "nhat-ky-thao-tac.json"
HIEU_LUC = 15 * 60
TANG_TOI_DA = 1.5
_khoa = threading.RLock()
_de_xuat: dict = {}
_KHONG_LE = {"VND", "JPY", "KRW", "CLP", "ISK", "PYG", "UGX", "VUV", "XAF", "XOF", "XPF", "RWF", "KMF", "GNF", "DJF", "BIF"}   # tiền không có đơn vị lẻ


def _tai_khoan(tid: str):
    return next((t for t in Q._doc_tk()["tai_khoan"] if t["id"] == tid), None)


def dat_cho_ghi(tid: str, bat: bool) -> dict:
    with Q._khoa:
        doc = Q._doc_tk()
        tk = next((t for t in doc["tai_khoan"] if t["id"] == tid), None)
        if not tk:
            raise ValueError("Không thấy tài khoản này.")
        tk["cho_ghi"] = bool(bat)
        Q._ghi(Q.TEP_TK, doc)
    _ghi_nk({"tk": tk.get("ten") or tk["ma_tk"], "nen": tk["nen"], "viec": "Bật quyền thao tác" if bat else "Tắt quyền thao tác", "ket_qua": "xong"})
    return {"ok": True, "cho_ghi": bool(bat)}


# ---------------------------------------------------------------- nhật ký
def doc_nk() -> list:
    try:
        d = json.loads(TEP_NHAT_KY.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except (OSError, ValueError):
        return []


def _ghi_nk(x: dict) -> None:
    x = dict(x, luc=time.strftime("%Y-%m-%d %H:%M:%S"))
    with _khoa:
        ds = doc_nk()
        ds.insert(0, x)
        Q._ghi(TEP_NHAT_KY, ds[:200])


# ---------------------------------------------------------------- đọc trạng thái thật và ghi
def _doc_fb(tk, bm, cap, oid):
    ver = tk.get("phien_ban") or Q.FB_PHIEN_BAN
    j = Q._http("GET", "%s/%s/%s?%s" % (Q.FB_GOC, ver, oid, urllib.parse.urlencode({"fields": "name,status,effective_status,daily_budget,lifetime_budget", "access_token": bm.get("token", "")})))
    if (m := Q._loi_fb(j)):
        raise Q.LoiNenTang(m)
    cu = Q._http("GET", "%s/%s/%s?%s" % (Q.FB_GOC, ver, tk["ma_tk"], urllib.parse.urlencode({"fields": "currency", "access_token": bm.get("token", "")})))
    return {"ten": j.get("name") or oid, "chay": str(j.get("status") or "").upper() == "ACTIVE", "trang_thai": str(j.get("effective_status") or j.get("status") or ""),
            "ngan_sach": Q._so(j.get("daily_budget")) / (1 if (cu.get("currency") or "VND") in _KHONG_LE else 100), "tron_doi": Q._so(j.get("lifetime_budget")) > 0, "tien_te": cu.get("currency") or "VND"}


def _ghi_fb(tk, bm, cap, oid, hd, gt, tien_te):
    ver = tk.get("phien_ban") or Q.FB_PHIEN_BAN
    du = {"access_token": bm.get("token", "")}
    if hd in ("bat", "tat"):
        du["status"] = "ACTIVE" if hd == "bat" else "PAUSED"
    else:
        du["daily_budget"] = str(int(round(gt * (1 if tien_te in _KHONG_LE else 100))))
    j = Q._http("POST", "%s/%s/%s" % (Q.FB_GOC, ver, oid), data=du, hinh="form")
    if (m := Q._loi_fb(j)):
        raise Q.LoiNenTang(m)
    if j.get("success") is False:
        raise Q.LoiNenTang("Facebook từ chối thay đổi này.")


def _doc_tt(tk, bm, cap, oid):
    h = {"Access-Token": bm.get("token", "")}
    base = Q.TT_GOC + "/open_api/v1.3"
    nhom = cap == "nhom"
    q = {"advertiser_id": tk["ma_tk"], "filtering": json.dumps({"adgroup_ids" if nhom else "campaign_ids": [oid]}),
         "fields": json.dumps(["adgroup_id", "adgroup_name", "operation_status", "budget", "budget_mode"] if nhom else ["campaign_id", "campaign_name", "operation_status", "budget", "budget_mode"])}
    j = Q._http("GET", base + ("/adgroup/get/" if nhom else "/campaign/get/") + "?" + urllib.parse.urlencode(q), headers=h)
    if j.get("code") not in (None, 0):
        raise Q.LoiNenTang(Q._loi_tt(j) or "TikTok báo lỗi.")
    ds = (j.get("data") or {}).get("list") or []
    if not ds:
        raise Q.LoiNenTang("Không thấy mục này trên TikTok (có thể đã xoá).")
    e = ds[0]
    return {"ten": e.get("adgroup_name" if nhom else "campaign_name") or oid, "chay": e.get("operation_status") == "ENABLE", "trang_thai": str(e.get("operation_status") or ""),
            "ngan_sach": Q._so(e.get("budget")), "tron_doi": str(e.get("budget_mode") or "").upper() == "BUDGET_MODE_TOTAL", "tien_te": "VND"}


def _ghi_tt(tk, bm, cap, oid, hd, gt, tien_te):
    h = {"Access-Token": bm.get("token", "")}
    base = Q.TT_GOC + "/open_api/v1.3"
    nhom = cap == "nhom"
    if hd in ("bat", "tat"):
        j = Q._http("POST", base + ("/adgroup/status/update/" if nhom else "/campaign/status/update/"), headers=h,
                    data={"advertiser_id": tk["ma_tk"], ("adgroup_ids" if nhom else "campaign_ids"): [oid], "operation_status": "ENABLE" if hd == "bat" else "DISABLE"})
    else:
        j = Q._http("POST", base + ("/adgroup/update/" if nhom else "/campaign/update/"), headers=h, data={"advertiser_id": tk["ma_tk"], ("adgroup_id" if nhom else "campaign_id"): oid, "budget": gt})
    if j.get("code") not in (None, 0):
        raise Q.LoiNenTang(Q._loi_tt(j) or "TikTok từ chối thay đổi này.")


def _gg(tk, bm):
    ver = tk.get("phien_ban") or Q.GG_PHIEN_BAN
    h = {"Authorization": "Bearer " + Q._gg_token(bm), "developer-token": bm.get("developer_token", "")}
    if bm.get("login_customer_id"):
        h["login-customer-id"] = bm["login_customer_id"]
    return "%s/%s/customers/%s" % (Q.GG_GOC, ver, tk["ma_tk"]), h


def _doc_gg(tk, bm, cap, oid):
    goc, h = _gg(tk, bm)
    nhom = cap == "nhom"
    q = ("SELECT ad_group.id, ad_group.name, ad_group.status, campaign.campaign_budget FROM ad_group WHERE ad_group.id = %s" % int(oid)) if nhom else \
        ("SELECT campaign.id, campaign.name, campaign.status, campaign.campaign_budget, campaign_budget.amount_micros FROM campaign WHERE campaign.id = %s" % int(oid))
    j = Q._http("POST", goc + "/googleAds:search", headers=h, data={"query": q})
    if (m := Q._loi_gg(j)):
        raise Q.LoiNenTang(m)
    r = (j.get("results") or [None])[0]
    if not r:
        raise Q.LoiNenTang("Không thấy mục này trên Google Ads.")
    c, g_ = r.get("campaign") or {}, r.get("adGroup") or {}
    tt = str((g_.get("status") if nhom else c.get("status")) or "")
    return {"ten": (g_.get("name") if nhom else c.get("name")) or oid, "chay": tt == "ENABLED", "trang_thai": tt, "ngan_sach": Q._so((r.get("campaignBudget") or {}).get("amountMicros")) / 1e6,
            "tron_doi": False, "tien_te": "VND", "budget_res": c.get("campaignBudget") or ""}


def _ghi_gg(tk, bm, cap, oid, hd, gt, tien_te, budget_res=""):
    goc, h = _gg(tk, bm)
    nhom = cap == "nhom"
    if hd in ("bat", "tat"):
        res = "customers/%s/%s/%s" % (tk["ma_tk"], "adGroups" if nhom else "campaigns", oid)
        j = Q._http("POST", goc + ("/adGroups:mutate" if nhom else "/campaigns:mutate"), headers=h,
                    data={"operations": [{"updateMask": "status", "update": {"resourceName": res, "status": "ENABLED" if hd == "bat" else "PAUSED"}}]})
    else:
        if not budget_res:
            raise Q.LoiNenTang("Không tìm thấy ngân sách của chiến dịch này để đổi.")
        j = Q._http("POST", goc + "/campaignBudgets:mutate", headers=h, data={"operations": [{"updateMask": "amount_micros", "update": {"resourceName": budget_res, "amountMicros": str(int(gt * 1e6))}}]})
    if (m := Q._loi_gg(j)):
        raise Q.LoiNenTang(m)


_DOC = {"facebook": _doc_fb, "tiktok": _doc_tt, "google": _doc_gg}
_GHI = {"facebook": _ghi_fb, "tiktok": _ghi_tt, "google": _ghi_gg}


def _tien(v, tt):
    return ("{:,.0f} đ".format(v).replace(",", ".")) if tt == "VND" else "{:,.2f} {}".format(v, tt)


# ---------------------------------------------------------------- hai bước: chuẩn bị rồi xác nhận
def chuan_bi(d: dict) -> dict:
    tk = _tai_khoan(str(d.get("tk_id") or ""))
    if not tk:
        raise ValueError("Không thấy tài khoản này.")
    if not tk.get("cho_ghi"):
        raise ValueError("Tài khoản này đang ở chế độ chỉ đọc. Vào tab Tài khoản và kết nối, bật \"Cho phép bật, tắt, đổi ngân sách\" trước.")
    cap = "nhom" if d.get("cap") == "nhom" else "chien-dich"
    oid = re.sub(r"[^\w-]", "", str(d.get("doi_tuong_id") or ""))
    hd = str(d.get("hanh_dong") or "")
    if not oid or hd not in ("bat", "tat", "ngan_sach"):
        raise ValueError("Thiếu thông tin thao tác.")
    bm = Q._bi_mat(tk)
    hien = _DOC[tk["nen"]](tk, bm, cap, oid)
    tt = hien["tien_te"]
    doi = "nhóm quảng cáo" if cap == "nhom" else "chiến dịch"
    moi_ns = None
    if hd == "bat":
        if hien["chay"]:
            raise ValueError("%s này đang chạy rồi, không cần bật." % doi.capitalize())
        tom = "BẬT %s \"%s\". Hiện đang tắt. Sau khi bật, quảng cáo bắt đầu hiển thị và TIÊU TIỀN THẬT theo ngân sách ngày %s." % (doi, hien["ten"], _tien(hien["ngan_sach"], tt) if hien["ngan_sach"] else "đã đặt")
    elif hd == "tat":
        if not hien["chay"] and "PAUSED" in hien["trang_thai"].upper() + "DISABLE":
            raise ValueError("%s này đang tắt rồi." % doi.capitalize())
        tom = "TẮT %s \"%s\". Hiện đang chạy (ngân sách ngày %s). Sau khi tắt, quảng cáo ngừng hiển thị, ngừng tiêu tiền." % (doi, hien["ten"], _tien(hien["ngan_sach"], tt) if hien["ngan_sach"] else "đã đặt")
    else:
        try:
            moi_ns = float(d.get("gia_tri"))
        except (TypeError, ValueError):
            raise ValueError("Ngân sách mới phải là một con số.")
        if moi_ns <= 0 or (tt in _KHONG_LE and moi_ns != int(moi_ns)):
            raise ValueError("Ngân sách mới phải là số dương%s." % (", tiền đồng không có số lẻ" if tt in _KHONG_LE else ""))
        if hien["tron_doi"]:
            raise ValueError("%s này dùng ngân sách trọn đời. Trang chỉ đổi ngân sách theo ngày, hãy đổi trực tiếp trên nền tảng." % doi.capitalize())
        if not hien["ngan_sach"]:
            raise ValueError("%s này không đặt ngân sách riêng ở cấp này (ngân sách nằm ở cấp khác). Hãy đổi ở cấp đã đặt ngân sách." % doi.capitalize())
        if moi_ns > hien["ngan_sach"] * TANG_TOI_DA:
            raise ValueError("Mỗi lần chỉ tăng tối đa 50%%: từ %s lên tối đa %s. Muốn tăng nhiều hơn thì tăng từng bước, cách nhau vài ngày." % (_tien(hien["ngan_sach"], tt), _tien(hien["ngan_sach"] * TANG_TOI_DA, tt)))
        tran = Q.cai_chung().get("ngan_sach_ngay_toi_da") or 0
        if tran and moi_ns > tran:
            raise ValueError("Ngân sách mới %s vượt mức \"chi tối đa mỗi ngày\" anh đã đặt (%s). Đổi mức đó ở tab Gợi ý tối ưu nếu muốn." % (_tien(moi_ns, tt), _tien(tran, tt)))
        if moi_ns == hien["ngan_sach"]:
            raise ValueError("Ngân sách mới trùng ngân sách hiện tại.")
        tom = "ĐỔI NGÂN SÁCH NGÀY của %s \"%s\" từ %s thành %s (%s %d%%). Tiền quảng cáo thật thay đổi theo." % (doi, hien["ten"], _tien(hien["ngan_sach"], tt), _tien(moi_ns, tt), "tăng" if moi_ns > hien["ngan_sach"] else "giảm", abs(round((moi_ns / hien["ngan_sach"] - 1) * 100)))
    ma = hashlib.sha1(("%s%s%s%s" % (tk["id"], oid, hd, time.time())).encode()).hexdigest()[:6].upper()
    with _khoa:
        for k in [k for k, v in _de_xuat.items() if v["het"] < time.time()]:
            _de_xuat.pop(k, None)
        _de_xuat[ma] = {"tk_id": tk["id"], "cap": cap, "oid": oid, "hd": hd, "gt": moi_ns, "tien_te": tt, "truoc": hien, "tom": tom, "het": time.time() + HIEU_LUC}
    return {"ok": True, "ma": ma, "tom_tat": tom, "cau_xac_nhan": "XÁC NHẬN QC " + ma, "het_sau_phut": HIEU_LUC // 60, "ten_tk": tk.get("ten") or tk["ma_tk"], "nen": tk["nen"]}


def xac_nhan(ma: str, cau: str) -> dict:
    ma = str(ma or "").strip().upper()
    with _khoa:
        dx = _de_xuat.get(ma)
    if not dx or dx["het"] < time.time():
        raise ValueError("Đề xuất đã hết hạn hoặc không có. Bấm lại để lập đề xuất mới.")
    chuan = re.sub(r"\s+", " ", "XÁC NHẬN QC " + ma)
    if re.sub(r"\s+", " ", str(cau or "").strip()).upper() != chuan.upper():
        raise ValueError("Câu xác nhận chưa đúng. Gõ chính xác: " + chuan)
    with _khoa:
        _de_xuat.pop(ma, None)         # dùng một lần
    tk = _tai_khoan(dx["tk_id"])
    if not tk or not tk.get("cho_ghi"):
        raise ValueError("Tài khoản không còn cho phép thao tác.")
    bm = Q._bi_mat(tk)
    nk = {"tk": tk.get("ten") or tk["ma_tk"], "nen": tk["nen"], "cap": dx["cap"], "doi_tuong": dx["truoc"]["ten"], "viec": dx["tom"][:160], "truoc": {"chay": dx["truoc"]["chay"], "ngan_sach": dx["truoc"]["ngan_sach"]}}
    # Đọc lại ngay trước khi ghi: dữ liệu đã đổi so với lúc lập đề xuất thì dừng, không ghi đè lên thay đổi của người khác.
    hien = _DOC[tk["nen"]](tk, bm, dx["cap"], dx["oid"])
    if hien["chay"] != dx["truoc"]["chay"] or abs(hien["ngan_sach"] - dx["truoc"]["ngan_sach"]) > 0.5:
        nk["ket_qua"] = "dừng: dữ liệu đã đổi"
        _ghi_nk(nk)
        raise ValueError("Trạng thái hoặc ngân sách trên nền tảng vừa đổi so với lúc anh xem. Chưa làm gì. Bấm lại để lập đề xuất mới.")
    try:
        if tk["nen"] == "google":
            _GHI["google"](tk, bm, dx["cap"], dx["oid"], dx["hd"], dx["gt"], dx["tien_te"], hien.get("budget_res", ""))
        else:
            _GHI[tk["nen"]](tk, bm, dx["cap"], dx["oid"], dx["hd"], dx["gt"], dx["tien_te"])
    except Q.LoiNenTang as e:
        nk["ket_qua"] = "lỗi: %s" % str(e)[:120]
        _ghi_nk(nk)
        raise ValueError("Nền tảng chưa nhận thay đổi: %s. Không tự thử lại; hãy kiểm tra trạng thái thật trên nền tảng rồi mới làm tiếp." % e)
    except Exception as e:  # noqa: BLE001
        nk["ket_qua"] = "cần đối chiếu"
        _ghi_nk(nk)
        raise ValueError("Chưa chắc nền tảng đã nhận thay đổi hay chưa (%s). Đừng bấm lại; mở trang quản lý của nền tảng xem trạng thái thật." % str(e)[:100])
    try:
        sau = _DOC[tk["nen"]](tk, bm, dx["cap"], dx["oid"])
    except Exception:  # noqa: BLE001
        sau = None
    dung = bool(sau) and ((dx["hd"] == "bat" and sau["chay"]) or (dx["hd"] == "tat" and not sau["chay"]) or (dx["hd"] == "ngan_sach" and abs(sau["ngan_sach"] - dx["gt"]) < 0.5))
    nk["sau"] = {"chay": sau["chay"], "ngan_sach": sau["ngan_sach"]} if sau else None
    nk["ket_qua"] = "xong, đã đọc lại khớp" if dung else "đã gửi, chưa đọc lại được hoặc chưa khớp: cần đối chiếu"
    _ghi_nk(nk)
    with Q._khoa:
        for k in [k for k in Q._nho if k.startswith(tk["id"] + "|")]:
            Q._nho.pop(k, None)             # số liệu cũ không còn đúng
    return {"ok": True, "khop": dung, "tom_tat": dx["tom"], "sau": nk["sau"], "thong_bao": ("Đã thực hiện và đọc lại khớp." if dung else "Đã gửi yêu cầu nhưng chưa đọc lại khớp. Mở trang quản lý của nền tảng kiểm tra trạng thái thật.")}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=ma)

    @app.post("/tisa-quang-cao/api/tai-khoan/{tid}/cho-ghi")
    async def _cho_ghi(tid: str, request: Request):
        d = await request.json()
        if d.get("bat") and not d.get("da_hieu"):
            return loi("Anh cần tick xác nhận đã hiểu trước khi bật.")
        try:
            return dat_cho_ghi(tid, bool(d.get("bat")))
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/thao-tac/chuan-bi")
    async def _cb(request: Request):
        import asyncio
        try:
            return await asyncio.to_thread(chuan_bi, await request.json())
        except ValueError as e:
            return loi(str(e))
        except Q.LoiNenTang as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/thao-tac/xac-nhan")
    async def _xn(request: Request):
        import asyncio
        d = await request.json()
        try:
            return await asyncio.to_thread(xac_nhan, d.get("ma"), d.get("cau"))
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/thao-tac/nhat-ky")
    async def _nk():
        return {"ok": True, "nhat_ky": doc_nk()[:60]}
