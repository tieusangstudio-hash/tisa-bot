"""tisa_quang_cao_so_mcp.py - nút "Lấy số thật qua MCP" của trang Quảng Cáo (V2.78).

Anh nối MCP quảng cáo (ví dụ Meta Ads) mà chưa nhập mã API thì bảng số liệu vẫn trống. Nút này nhờ CỘNG SỰ phụ trách quảng cáo
(đúng đường nút "Hỏi trợ lý" đang dùng) đọc số liệu qua công cụ MCP đã nối rồi trả về MỘT khối JSON theo mẫu cố định.
Trang đọc khối đó, kiểm tra từng con số, cất lại và hiện lên bảng như số thật (ghi rõ "lấy qua MCP lúc ...").

An toàn:
  - CHỈ ĐỌC: lệnh gửi cho cộng sự luôn dặn không bật, tắt, đổi, tạo hay xoá gì trong tài khoản quảng cáo.
  - Không bịa số: không đọc được thì cộng sự phải trả {"loi": "..."}; trang báo lại nguyên văn, không điền số giả.
  - Mỗi lần bấm là một lượt chat với cộng sự (tốn một lượt Claude), nên trang không tự bấm, chỉ chạy khi anh bấm.
Số cất ở STATE_DIR/quang-cao/so-mcp.json, mỗi nền tảng một bản (bản mới nhất).
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import threading
import time

import tisa_quang_cao as Q
import tisa_quang_cao_bang as B
import tisa_quang_cao_tu_van as TV

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

TEP = Q.KHO / "so-mcp.json"
_khoa = threading.Lock()
MAX_NGAY, MAX_NHOM = 400, 400

TEN_CONG_CU = {"facebook": "Meta Ads (Facebook)", "tiktok": "TikTok Ads", "google": "Google Ads"}

MAU = """{
  "tai_khoan": "tên tài khoản quảng cáo",
  "tien_te": "VND",
  "tu": "YYYY-MM-DD",
  "den": "YYYY-MM-DD",
  "ngay": [ {"ngay": "YYYY-MM-DD", "chi_phi": 0, "hien_thi": 0, "bam": 0, "ket_qua": 0, "doanh_thu": 0} ],
  "nhom": [ {"cd_id": "", "cd": "tên chiến dịch", "nhom_id": "", "nhom": "tên nhóm quảng cáo", "trang_thai": "ACTIVE hoặc PAUSED",
             "ngan_sach_ngay": 0, "chi_phi": 0, "tiep_can": 0, "hien_thi": 0, "bam": 0, "chia_se": 0, "binh_luan": 0,
             "tin_nhan": 0, "ket_qua": 0, "doanh_thu": 0, "v25": 0, "v50": 0, "v75": 0, "v100": 0} ]
}"""


def _lenh(nen: str, tu: str, den: str, ten_tk: str) -> str:
    cc = TEN_CONG_CU.get(nen, nen)
    kq = {"facebook": "kết quả = mua hàng, nếu không có thì khách để lại thông tin, nếu không có thì lượt bắt đầu trò chuyện qua tin nhắn",
          "tiktok": "kết quả = chuyển đổi chính của chiến dịch", "google": "kết quả = chuyển đổi; chi phí đổi từ micro về đơn vị tiền tệ thật"}.get(nen, "kết quả = mục tiêu chính của chiến dịch")
    tk = ("Tài khoản quảng cáo: %s. " % ten_tk) if ten_tk else "Nếu có nhiều tài khoản thì lấy tài khoản đang chạy nhiều nhất. "
    return ("NHIỆM VỤ LẤY SỐ LIỆU (CHỈ ĐỌC) cho trang Quảng Cáo của TISA BOT.\n"
            "Dùng công cụ MCP %s đã nối để đọc số liệu quảng cáo từ ngày %s đến ngày %s (cả hai ngày đều tính). %s\n"
            "Cần: (1) tổng theo TỪNG NGÀY trong kỳ; (2) từng NHÓM QUẢNG CÁO (kèm tên chiến dịch) cộng dồn cả kỳ.\n"
            "Quy tắc:\n"
            "- CHỈ ĐỌC. Tuyệt đối không bật, tắt, đổi ngân sách, tạo, sửa hay xoá bất cứ thứ gì trong tài khoản.\n"
            "- Không bịa, không ước chừng. Số nào công cụ không trả về thì để 0. %s.\n"
            "- Số là số thuần (ví dụ 1250000), không dấu chấm phẩy ngăn cách, không ký hiệu tiền. chi_phi theo đơn vị tiền tệ của tài khoản.\n"
            "- Ngày dạng YYYY-MM-DD. trang_thai: ACTIVE hoặc PAUSED (hoặc để trống nếu không rõ).\n"
            "- Nếu công cụ báo chưa đăng nhập, hết hạn hay lỗi quyền thì KHÔNG đoán: trả đúng {\"loi\": \"mô tả ngắn lỗi, cách khắc phục\"}.\n"
            "Trả lời bằng MỘT khối ```json duy nhất theo mẫu dưới đây (thêm bớt dòng cho đủ số liệu), sau khối đó chỉ được viết tối đa 2 câu ghi chú.\n"
            "%s") % (cc, tu, den, tk, kq, MAU)


LUAT_IM = "\n\n(Lượt này chỉ lấy số liệu để trang Quảng Cáo hiển thị. Không làm gì ngoài việc đọc.)"


# ---------------------------------------------------------------- kho
def _doc_kho() -> dict:
    try:
        d = json.loads(TEP.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def lay(nen: str) -> dict | None:
    return _doc_kho().get(nen)


def luu(nen: str, d: dict) -> None:
    with _khoa:
        kho = _doc_kho()
        kho[nen] = d
        Q._ghi(TEP, kho)


def xoa(nen: str) -> bool:
    with _khoa:
        kho = _doc_kho()
        if nen in kho:
            kho.pop(nen)
            Q._ghi(TEP, kho)
            return True
    return False


# ---------------------------------------------------------------- đọc và kiểm tra khối JSON
class LoiSo(ValueError):
    pass


def _khoi_json(text: str):
    m = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text or "", flags=re.S)
    cands = m[::-1] if m else []
    if not cands:
        a, b = (text or "").find("{"), (text or "").rfind("}")
        if a >= 0 and b > a:
            cands = [text[a:b + 1]]
    for c in cands:
        try:
            d = json.loads(c)
            if isinstance(d, dict):
                return d
        except ValueError:
            continue
    return None


def _ngay_hop_le(s) -> str:
    try:
        return _dt.date.fromisoformat(str(s)[:10]).isoformat()
    except ValueError:
        return ""


def phan_tich(text: str, nen: str, tu: str, den: str) -> dict:
    """Từ lời cộng sự thành bản số đã kiểm tra. Ném LoiSo với câu báo lỗi tiếng Việt nếu không dùng được."""
    d = _khoi_json(text)
    if d is None:
        t = re.sub(r"\s+", " ", str(text or "")).strip()
        raise LoiSo("Cộng sự chưa trả số theo mẫu." + ((" Cộng sự nói: " + t[:260]) if t else ""))
    if d.get("loi"):
        raise LoiSo("Cộng sự không đọc được số qua MCP: %s" % str(d["loi"])[:300])
    ngay_ds, nhom_ds = d.get("ngay") or [], d.get("nhom") or []
    if not isinstance(ngay_ds, list) or not isinstance(nhom_ds, list) or not (ngay_ds or nhom_ds):
        raise LoiSo("Khối số không có dòng nào (cả theo ngày lẫn theo nhóm quảng cáo). Có thể kỳ này chưa chạy quảng cáo, hoặc công cụ chưa trả số.")
    ngay = []
    for r in ngay_ds[:MAX_NGAY]:
        if not isinstance(r, dict):
            continue
        n = _ngay_hop_le(r.get("ngay"))
        if not n:
            continue
        ngay.append({"ngay": n, **{k: max(0.0, Q._so(r.get(k))) for k in ("chi_phi", "hien_thi", "bam", "ket_qua", "doanh_thu")}})
    nhom = []
    for r in nhom_ds[:MAX_NHOM]:
        if not isinstance(r, dict):
            continue
        x = {"cd_id": str(r.get("cd_id") or r.get("cd") or "")[:60], "cd": str(r.get("cd") or r.get("cd_id") or "Chiến dịch")[:160],
             "nhom_id": str(r.get("nhom_id") or "")[:60], "nhom": str(r.get("nhom") or "")[:160],
             "trang_thai": str(r.get("trang_thai") or "")[:20].upper(), "ngan_sach_ngay": max(0.0, Q._so(r.get("ngan_sach_ngay")))}
        for k in ("chi_phi", "tiep_can", "hien_thi", "bam", "chia_se", "binh_luan", "tin_nhan", "ket_qua", "doanh_thu", "v25", "v50", "v75", "v100"):
            x[k] = max(0.0, Q._so(r.get(k)))
        nhom.append(x)
    if not ngay and not nhom:
        raise LoiSo("Các dòng số cộng sự trả về đều sai định dạng (thiếu ngày hoặc không phải số).")
    # Chi phí hai bảng phải gần khớp nhau: lệch quá xa nghĩa là cộng sự điền sai, không cất để khỏi hiện số sai.
    ct_ngay, ct_nhom = sum(r["chi_phi"] for r in ngay), sum(r["chi_phi"] for r in nhom)
    canh = ""
    if ngay and nhom and ct_ngay > 0 and abs(ct_ngay - ct_nhom) / ct_ngay > 0.25:
        canh = "Chi phí cộng theo ngày (%s) và theo nhóm (%s) lệch nhau trên 25%%, nên số này cần kiểm tra lại." % (round(ct_ngay), round(ct_nhom))
    tt = str(d.get("tien_te") or "VND").upper()[:5]
    return {"nen": nen, "ten": str(d.get("tai_khoan") or TEN_CONG_CU.get(nen, nen))[:120], "tien_te": tt,
            "tu": _ngay_hop_le(d.get("tu")) or tu, "den": _ngay_hop_le(d.get("den")) or den, "ngay": ngay, "nhom": nhom,
            "luc": int(time.time()), "canh_bao": canh}


# ---------------------------------------------------------------- đưa vào mô hình dữ liệu của trang
def thanh_nguon(nen: str) -> dict | None:
    """Dạng {nen, ten, tien_te, dong, chien_dich, mcp} như một nguồn API, để _gom dùng chung công thức."""
    s = lay(nen)
    if not s:
        return None
    dong = [Q.dong(r["ngay"], "mcp-tong", "Tất cả chiến dịch", r["chi_phi"], r["hien_thi"], r["bam"], r["ket_qua"], r["doanh_thu"]) for r in s.get("ngay") or []]
    return {"nen": nen, "ten": s["ten"], "tien_te": s["tien_te"], "dong": dong, "chien_dich": {}, "mcp": True, "luc": s["luc"], "tu": s["tu"], "den": s["den"],
            "canh_bao": s.get("canh_bao") or ""}


def chien_dich(nen: str, ngay_ds: list) -> list:
    """Danh sách chiến dịch (cộng các nhóm cùng chiến dịch) cho tab Chiến dịch."""
    s = lay(nen)
    if not s:
        return []
    cd = {}
    for r in s.get("nhom") or []:
        k = r["cd_id"] or r["cd"]
        c = cd.setdefault(k, {"nen": nen, "nguon": "mcp-" + nen, "tk_ten": s["ten"], "cd_id": k, "cd": r["cd"], "tien_te": s["tien_te"], "chi_phi": 0.0,
                              "hien_thi": 0.0, "bam": 0.0, "ket_qua": 0.0, "doanh_thu": 0.0, "trang_thai": "", "ngan_sach_ngay": 0.0})
        for kk in ("chi_phi", "hien_thi", "bam", "ket_qua", "doanh_thu"):
            c[kk] += r[kk]
        c["ngan_sach_ngay"] += r["ngan_sach_ngay"]
        c["trang_thai"] = "ACTIVE" if "ACTIVE" in (c["trang_thai"], r["trang_thai"]) else (c["trang_thai"] or r["trang_thai"])
    out = []
    for c in cd.values():
        Q._chi_so(c)
        c["ngay_chi"] = [0] * len(ngay_ds)
        out.append(c)
    return out


def bang(nen: str, cap: str) -> list:
    """Dòng cho bảng 19 chỉ số (theo nhóm quảng cáo, hoặc cộng theo chiến dịch)."""
    s = lay(nen)
    if not s:
        return []
    rows = []
    for r in s.get("nhom") or []:
        x = B.dong(nen, s["ten"], r["cd_id"] or r["cd"], r["cd"], r["nhom_id"], r["nhom"], s["tien_te"], trang_thai=r["trang_thai"], ngan_sach=r["ngan_sach_ngay"],
                   chi_phi=r["chi_phi"], tiep_can=r["tiep_can"], hien_thi=r["hien_thi"], bam=r["bam"], chia_se=r["chia_se"], binh_luan=r["binh_luan"],
                   tin_nhan=r["tin_nhan"], ket_qua=r["ket_qua"], doanh_thu=r["doanh_thu"], v25=r["v25"], v50=r["v50"], v75=r["v75"], v100=r["v100"])
        rows.append(x)
    if cap == "chien-dich":
        gop = {}
        for x in rows:
            g = gop.get(x["cd_id"])
            if not g:
                g = gop[x["cd_id"]] = dict(x, nhom_id="", nhom="", ngan_sach=0.0, tiep_can=0.0, tan_suat=0.0)
                for k in B._CONG:
                    g[k] = 0.0
            for k in B._CONG:
                g[k] += x[k]
            g["ngan_sach"] += x["ngan_sach"]
            if x["trang_thai"] == "ACTIVE":
                g["trang_thai"] = "ACTIVE"
        rows = list(gop.values())
    return [B.chi_so(x) for x in rows]


def tom_tat() -> dict:
    """Cho trang biết nền tảng nào đã có số lấy qua MCP, kỳ nào, lúc nào."""
    return {n: {"luc": v["luc"], "tu": v["tu"], "den": v["den"], "ten": v["ten"], "canh_bao": v.get("canh_bao") or ""} for n, v in _doc_kho().items()}


# ---------------------------------------------------------------- gửi lệnh và nhận kết quả
def bat_dau(nen: str, kieu: str, tu: str, den: str, ten_tk: str = "", cong_su: str = "") -> dict:
    if nen not in Q.NEN:
        raise ValueError("Chưa biết nền tảng này.")
    a, b = Q.khoang(kieu, tu, den)
    r = TV.gui(_lenh(nen, a.isoformat(), b.isoformat(), ten_tk[:120]), nen, cong_su, "quang-cao", LUAT_IM)
    return {"ok": True, "tin": r["tin"], "cong_su": r["cong_su"], "tu": a.isoformat(), "den": b.isoformat(), "nen": nen}


def ket_qua(tin: str, nen: str, tu: str, den: str) -> dict:
    d = TV.doc(tin)
    if not d.get("xong"):
        return {"ok": True, "xong": False, "dang": bool(d.get("dang")), "tu": d.get("tu") or ""}
    try:
        s = phan_tich(d.get("text") or "", nen, tu, den)
    except LoiSo as e:
        return {"ok": False, "xong": True, "error": str(e)}
    luu(nen, s)
    return {"ok": True, "xong": True, "so_ngay": len(s["ngay"]), "so_nhom": len(s["nhom"]), "canh_bao": s["canh_bao"], "tu": s["tu"], "den": s["den"]}


def gan(app) -> None:
    from fastapi.responses import JSONResponse
    import tisa_quang_cao_giao_viec as G

    def loi(msg, ma=400, chua_co_bang=False):
        return JSONResponse({"ok": False, "error": msg, "chua_co_bang": chua_co_bang}, status_code=ma)

    @app.post("/tisa-quang-cao/api/so-mcp/bat-dau")
    async def _bd(request: Request):
        import asyncio
        d = await request.json()
        try:
            return await asyncio.to_thread(bat_dau, str(d.get("nen") or ""), str(d.get("kieu") or "7-ngay"), str(d.get("tu") or ""), str(d.get("den") or ""),
                                           str(d.get("tai_khoan") or ""), str(d.get("cong_su") or ""))
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/so-mcp/ket-qua/{tin}")
    async def _kq(tin: str, request: Request):
        import asyncio
        q = request.query_params
        try:
            return await asyncio.to_thread(ket_qua, tin, q.get("nen", ""), q.get("tu", ""), q.get("den", ""))
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/so-mcp")
    async def _tt():
        return {"ok": True, "so": tom_tat()}

    @app.post("/tisa-quang-cao/api/so-mcp/{nen}/xoa")
    async def _xoa(nen: str):
        return {"ok": True, "da_xoa": xoa(nen)}
