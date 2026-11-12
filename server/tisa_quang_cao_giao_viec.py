"""tisa_quang_cao_giao_viec.py - nút "Nhờ trợ lý tạo" của trang Quảng Cáo tự GIAO VIỆC cho cộng sự phụ trách quảng cáo (V2.78).

Thay vì chép lời nhờ sang khung chat, trang tạo một việc trên Bảng giao việc của Đội Quân AI, đúng cách khung "Giao việc" làm:
tiêu đề và đề bài bắt đầu bằng "Giao cho <tên cộng sự>:", Tâm Tổng Quản nhận và giao đúng người đó làm chính, tiến độ hiện ở
Giao dự án và ở ngay trang Quảng Cáo.

Chọn cộng sự: đọc đội hình thật trên bảng (kể cả cộng sự anh tự tạo hoặc đổi tên), chấm điểm theo phòng, chức danh, việc phụ trách
có liên quan quảng cáo, cộng điểm nếu nhắc đúng nền tảng (Facebook, TikTok, Google). Anh đổi người được ngay trước khi giao.

Việc luôn mang luật của phiếu: tạo ở trạng thái TẠM DỪNG, chờ anh duyệt. Trang không bật quảng cáo thay anh.
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

import tisa_quang_cao as Q

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

PHONG_QC = "quang-cao"
TU_QC = ("quang cao", "ads", "chien dich", "ngan sach", "facebook ads", "tiktok ads", "google ads", "meta ads", "dung chien dich", "toi uu")
# Vai trò cộng sự: phòng ưu tiên + từ khoá ở chức danh (nặng) và việc phụ trách (nhẹ). Quảng cáo là vai mặc định.
VAI = {
    "quang-cao": {"phong": "quang-cao", "tu": TU_QC, "ten": "quảng cáo"},
    "thiet-ke": {"phong": "sang-tao", "tu": ("thiet ke", "hinh anh", "banner", "carousel", "thumbnail", "logo", "design", "anh bai dang", "tao anh"), "ten": "thiết kế hình ảnh"},
    "video": {"phong": "sang-tao", "tu": ("video", "dung video", "b-roll", "shot list", "phu de", "quay dung"), "ten": "dựng video"},
}
TU_NEN = {"facebook": ("facebook", "meta", "fb"), "tiktok": ("tiktok",), "google": ("google", "youtube")}
GIOI_HAN_DE_BAI = 4800


def _kd(s) -> str:
    x = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D").encode("ascii", "ignore").decode().lower()
    return " " + re.sub(r"\s+", " ", x) + " "


def _env() -> dict:
    p = Path(os.getenv("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
    out = {}
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    except OSError:
        pass
    return out


class ChuaCoBang(ValueError):
    """Chưa có Bảng giao việc Đội Quân AI chạy cùng TISA BOT."""


def _bang(method: str, path: str, body=None):
    c = _env()
    if not (c.get("BOARD_URL") and c.get("BOARD_TOKEN")):
        raise ChuaCoBang("Chưa thấy Bảng giao việc Đội Quân AI trên máy này (thiếu cấu hình bảng).")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(c["BOARD_URL"].rstrip("/") + path, data=data, method=method, headers={
        "Authorization": "Bearer " + c["BOARD_TOKEN"], "Content-Type": "application/json", "User-Agent": "tisa-quang-cao/1"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        raise ValueError("Bảng giao việc báo lỗi %s." % e.code)
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ChuaCoBang("Không nối được Bảng giao việc. Kiểm tra TISA BOT đã chạy đủ chưa rồi thử lại.")


def ung_vien(nen: str = "", vai: str = "quang-cao") -> list:
    """Các cộng sự có thể phụ trách một vai (mặc định quảng cáo), điểm cao nhất đứng đầu: [{id, ten, chuc_danh, phong, diem, ly_do}]."""
    cfg = VAI.get(vai) or VAI["quang-cao"]
    tu_vai, phong_vai = cfg["tu"], cfg["phong"]
    import tisa_team_sync
    kit = _bang("GET", "/api/db/settings/kit")
    kit.pop("id", None)
    roster = tisa_team_sync.board_roster(kit)
    ra = []
    for ma, a in roster.items():
        if a.get("off") or ma == "chu":
            continue
        chuc, viec = _kd(a.get("title")), _kd(" ".join(a.get("jobs") or []) + " " + str(a.get("output") or ""))
        ten = _kd(a.get("name"))
        diem, ly = 0, []
        if a.get("room") == phong_vai:
            diem += 5 if vai == "quang-cao" else 1
            ly.append("thuộc phòng đúng chuyên môn")
        n_chuc = sum(1 for k in tu_vai if k in chuc)
        n_viec = sum(1 for k in tu_vai if k in viec)
        if n_chuc:
            diem += 3 * n_chuc
            ly.append("chức danh đúng vai %s" % cfg["ten"])
        if n_viec:
            diem += min(n_viec, 4)
            ly.append("việc phụ trách có %s" % cfg["ten"])
        van = chuc + viec + ten
        if vai == "quang-cao" and nen and any(k in van for k in TU_NEN.get(nen, ())):
            diem += 3
            ly.append("nhắc đúng nền tảng %s" % Q.NEN[nen])
        elif vai == "quang-cao" and nen and any(k in van for n2, ks in TU_NEN.items() if n2 != nen for k in ks):
            diem -= 6            # chuyên nền tảng khác thì nhường cho người đúng nền tảng
        if diem > 0:
            ra.append({"id": ma, "ten": a.get("name") or ma, "chuc_danh": a.get("title") or "", "phong": a.get("room_name") or "", "diem": diem, "ly_do": ", ".join(ly)})
    ra.sort(key=lambda x: -x["diem"])
    return ra


def _id_viec() -> str:
    n, s = int(time.time() * 1000), ""
    while n:
        s = "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36] + s
        n //= 36
    return "job-" + s


def _slug(t: str, mx: int = 34) -> str:
    x = unicodedata.normalize("NFD", str(t)).replace("đ", "d").replace("Đ", "D").encode("ascii", "ignore").decode()
    x = re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9 ]+", " ", x)).strip()
    out = ""
    for w in x.split(" "):
        nx = (out + " " + w).strip()
        if len(nx) > mx:
            break
        out = nx
    out = out or "Viec"
    return out[:1].upper() + out[1:].lower()


def giao_viec(nen: str, ten_chien_dich: str, loi_nhac: str, cong_su_id: str = "") -> dict:
    ds = ung_vien(nen)
    if not ds:
        raise ValueError("Chưa thấy cộng sự nào phụ trách quảng cáo trong đội hình. Vào Cài đặt đội thêm một cộng sự quảng cáo, hoặc dán lời nhờ vào chat.")
    cs = next((x for x in ds if x["id"] == cong_su_id), ds[0])
    kit = _bang("GET", "/api/db/settings/kit")
    kbr = kit.get("brain") or {}
    vp = kbr.get("office") or "05 - Van Phong AI"
    hom = time.localtime()
    ngay, gio = time.strftime("%Y-%m-%d", hom), time.strftime("%H:%M", hom)
    tieu = "Giao cho %s: Tạo chiến dịch %s (tạm dừng)" % (cs["ten"], ten_chien_dich)
    dau = "Giao cho %s: Tạo chiến dịch quảng cáo theo phiếu từ trang Quảng Cáo, ở trạng thái TẠM DỪNG, chờ anh duyệt rồi mới bật.\n\n" % cs["ten"]
    de_bai = dau + loi_nhac
    if len(de_bai) > GIOI_HAN_DE_BAI:
        de_bai = dau + "Phiếu đầy đủ nằm ở trường phieu_qc của việc này (đọc bằng lệnh lay JOB). Tóm tắt: " + loi_nhac[:GIOI_HAN_DE_BAI - len(dau) - 120] + "..."
    vid = _id_viec()
    iso = time.strftime("%Y-%m-%dT%H:%M:%S", hom) + ".000Z"
    doc = {"title": tieu[:160], "task": de_bai, "date": ngay, "time": gio, "created": iso, "updated": iso, "status": "hang-doi", "mode": "claude", "demo": False,
           "folder": "%s/03 - Ket qua/%s/%s/%s/%s %s/" % (vp, ngay[:4], ngay[:7], ngay, gio.replace(":", ""), _slug(tieu)), "plan": [], "summary": "", "insights": [], "synced": False,
           "brain": "cho-nap", "settings": {}, "files": [], "nguon": "quang-cao", "phieu_qc": loi_nhac[:20000], "nen_qc": nen}
    _bang("PUT", "/api/db/results/" + vid, doc)
    return {"ok": True, "viec": vid, "cong_su": cs, "ung_vien": ds[:5], "tieu_de": doc["title"]}


def xem_viec(vid: str) -> dict:
    vid = re.sub(r"[^\w-]", "", vid or "")
    d = _bang("GET", "/api/v1/job/" + vid)
    if not d or d.get("error"):
        raise ValueError("Không thấy việc này trên bảng.")
    ten = {}
    try:
        import tisa_team_sync
        kit = _bang("GET", "/api/db/settings/kit")
        kit.pop("id", None)
        ten = {ma: a.get("name") or ma for ma, a in tisa_team_sync.board_roster(kit).items()}
        ten.setdefault("chu", "Anh")
    except Exception:  # noqa: BLE001
        pass
    plan = [{"n": p.get("n"), "agent": p.get("agent"), "ten": ten.get(p.get("agent")) or p.get("agent"), "viec": p.get("viec"), "state": p.get("state"), "pct": p.get("pct"), "out": str(p.get("out") or "")[:600],
             "log": [x.get("text") for x in (p.get("log") or [])][-3:]} for p in (d.get("plan") or [])]
    st = d.get("status") or ""
    return {"ok": True, "status": st, "title": d.get("title"), "summary": str(d.get("summary") or "")[:1500], "plan": plan,
            "links": [{"title": x.get("title"), "url": x.get("url"), "kind": x.get("kind")} for x in (d.get("links") or [])][:10],
            "xong": st in ("xong", "cho-duyet", "dung") or (bool(plan) and all(p["state"] in ("done", "duyet", "given", "owner", "err") for p in plan)),
            "cap_nhat": d.get("updated")}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400, chua_co_bang=False):
        return JSONResponse({"ok": False, "error": msg, "chua_co_bang": chua_co_bang}, status_code=ma)

    @app.get("/tisa-quang-cao/api/cong-su")
    async def _cs(request: Request):
        import asyncio
        try:
            return {"ok": True, "ung_vien": await asyncio.to_thread(ung_vien, request.query_params.get("nen", ""))}
        except ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/giao-viec")
    async def _gv(request: Request):
        import asyncio
        import tisa_quang_cao_thiet_lap as T
        d = await request.json()
        try:
            p = T.luu_phieu(d.get("phieu") or {})
            return await asyncio.to_thread(lambda: dict(giao_viec(p["nen"], p["ten"], T.loi_nhac(p), str(d.get("cong_su") or "")), phieu_id=p["id"]))
        except ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/giao-viec/{vid}")
    async def _xem(vid: str):
        import asyncio
        try:
            return await asyncio.to_thread(xem_viec, vid)
        except ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))
