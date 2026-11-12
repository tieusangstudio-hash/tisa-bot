"""tisa_quang_cao_tu_van.py - mọi nút "Hỏi trợ lý" của trang Quảng Cáo gửi thẳng cho cộng sự phụ trách quảng cáo (V2.78).

Câu hỏi đi như một tin chat riêng của chủ gửi cộng sự đó trên Bảng giao việc (đúng đường khung Chat nội bộ dùng). Cộng sự trả lời trong
phiên chat riêng của mình, có bộ nhớ và kỹ năng của mình; chữ trả lời hiện dần ngay trong trang. Chọn người giống nút giao việc
(tisa_quang_cao_giao_viec.ung_vien). Chỉ TƯ VẤN bằng lời: câu hỏi luôn kèm dặn không đổi gì trong tài khoản quảng cáo.
"""
from __future__ import annotations

import re
import time

import tisa_quang_cao_giao_viec as G

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

LUAT = ("\n\n(Đây là câu hỏi TƯ VẤN từ trang Quảng Cáo của TISA BOT. Trả lời bằng lời, ngắn gọn, từng bước, tiếng Việt dễ hiểu, dựa trên số liệu anh gửi kèm. "
        "KHÔNG bật, tắt, đổi ngân sách, tạo hay sửa quảng cáo trong lượt này; muốn làm thì đề xuất để anh bấm trong trang hoặc giao việc.)")


def gui(cau_hoi: str, nen: str = "", cong_su_id: str = "", vai: str = "quang-cao", luat: str = LUAT) -> dict:
    cau_hoi = str(cau_hoi or "").strip()
    if len(cau_hoi) < 3:
        raise ValueError("Câu hỏi trống.")
    ds = G.ung_vien(nen, vai)
    if not ds:
        raise ValueError("Chưa thấy cộng sự nào phụ trách %s trong đội hình. Vào Cài đặt đội thêm một người." % G.VAI.get(vai, G.VAI["quang-cao"])["ten"])
    cs = next((x for x in ds if x["id"] == cong_su_id), ds[0])
    iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + ".000Z"
    d = {"dm": cs["id"], "jobId": "", "part": 0, "to": cs["id"], "from": "chu", "kind": "chat", "status": "moi", "created": iso, "nguon": "quang-cao",
         "text": (cau_hoi[:7500] + luat)}
    r = G._bang("POST", "/api/db/messages", d)
    if not r or not r.get("id"):
        raise ValueError("Bảng chưa nhận câu hỏi.")
    return {"ok": True, "tin": r["id"], "cong_su": cs, "ung_vien": ds[:5]}


def doc(tin: str) -> dict:
    tin = re.sub(r"[^\w-]", "", tin or "")
    r = G._bang("GET", "/api/db/messages")
    docs = r.get("docs") or []
    goc = next((x for x in docs if x.get("id") == tin), None)
    if not goc:
        raise ValueError("Không thấy câu hỏi này trên bảng.")
    tl = sorted((x for x in docs if x.get("replyTo") == tin and x.get("kind") == "tra-loi"), key=lambda x: str(x.get("created") or ""))
    text = "\n\n".join(str(x.get("text") or "") for x in tl).strip()
    xong = goc.get("status") == "da-tra-loi"
    return {"ok": True, "text": text, "xong": xong, "dang": goc.get("status") in ("dang-xu-ly",) or bool(text) and not xong, "tu": (tl[-1].get("from") if tl else goc.get("to"))}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400, chua_co_bang=False):
        return JSONResponse({"ok": False, "error": msg, "chua_co_bang": chua_co_bang}, status_code=ma)

    @app.post("/tisa-quang-cao/api/tu-van")
    async def _gui(request: Request):
        import asyncio
        d = await request.json()
        try:
            return await asyncio.to_thread(gui, d.get("cau_hoi"), str(d.get("nen") or ""), str(d.get("cong_su") or ""))
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/tu-van/{tin}")
    async def _doc(tin: str):
        import asyncio
        try:
            return await asyncio.to_thread(doc, tin)
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))
