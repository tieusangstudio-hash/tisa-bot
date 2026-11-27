"""tisa_tieu_de.py - TIÊU ĐỀ NGẮN CHO TRANG KẾT QUẢ CỦA ĐỘI QUÂN AI (V2.91).

Việc giao bằng giọng nói có tiêu đề là nguyên văn lời nói ("Alo anh muốn em lên mạng nghiên cứu các vấn đề của học viên về mong muốn xây dựng kênh t...")
nên trang Kết quả dài, khó biết đó là việc gì. Module này nhờ AI tóm tắt mỗi việc thành MỘT tiêu đề ngắn (tối đa khoảng 8 từ) và MỘT dòng mô tả,
lưu lại trên máy để mỗi việc chỉ tóm tắt một lần. AI lỗi hay chưa đăng nhập thì dùng bản rút gọn bằng luật (bỏ lời chào, lời dặn thừa, cắt gọn).

POST /tisa-doi-quan/tieu-de  {items: [{id, title, summary, tiep?: {ten, chuoi, buoc}}]}  ->  {ok, tieu_de: {id: {t, m, c, ai}}}

V2.95: việc làm nối tiếp (có "tiep") thì "t" chỉ nói PHẦN MỚI so với việc trước, "c" là tên chuỗi 3-4 từ (giữ nguyên nếu đã có),
trang Kết quả ghép thành "c · Bước N: t" và hiện chip "Tiếp từ …".
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import threading
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

_khoa = threading.RLock()
_TOI_DA_MOI_LAN = 20

_THUA = ("alo", "a lô", "ê", "này", "nè", "dạ", "vâng", "ừ", "ok", "okay", "rồi", "bây giờ", "giờ", "vậy", "thế", "thì", "mà", "em ơi", "ơi",
         "anh muốn em", "anh muốn", "anh cần em", "anh cần", "anh nhờ em", "anh nhờ", "anh bảo em", "anh bảo", "anh dặn em", "mình muốn em", "mình muốn",
         "tôi muốn", "bạn hãy", "em hãy", "các em hãy", "hãy", "làm ơn", "giúp cho anh", "giúp anh", "giúp em", "giúp", "giùm", "cho anh", "đó là", "những cái", "cái",
         "em", "anh", "mình", "nha", "nhé")
_GIUA = (" giúp cho anh", " giúp anh", " giùm anh", " cho anh", " đó là những cái", " đó là", " những cái", " nha", " nhé")


def _thu_muc() -> Path:
    try:
        import config as _cfg
        base = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        base = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    d = base / "doi-quan"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _file() -> Path:
    return _thu_muc() / "tieu-de-ngan.json"


def _doc() -> dict:
    try:
        d = json.loads(_file().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _ghi(d: dict) -> None:
    f = _file()
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, f)


def _bam(title: str, summary: str, tiep: str = "") -> str:
    return hashlib.sha1((str(title) + "\n" + str(summary) + "\n" + str(tiep)).encode("utf-8")).hexdigest()[:12]


def rut_gon(text: str, toi_da: int = 56) -> str:
    """Bản rút gọn bằng luật: bỏ lời mở đầu thừa, viết hoa chữ đầu, cắt ở ranh giới từ."""
    goc = str(text or "")
    con = re.sub(r"https?://\S+|\(\d+ link\)", "", goc)
    # Link nằm giữa câu thì thay bằng tên trang ("làm quảng cáo cho abc.vn"); câu chỉ có link thì xử lý ở dưới.
    s = re.sub(r"https?://(?:www\.)?([^/\s?#]+)\S*", r"\1", goc) if len(re.sub(r"[\W_]", "", con)) >= 4 else con
    s = re.sub(r"\(\d+ link\)", "", s)
    s = re.sub(r"\s+", " ", s).strip().rstrip(".…:;,")
    s = re.sub(r"^[\W_]+", "", s)
    for _ in range(12):
        low = s.lower()
        hit = ""
        for w in sorted(_THUA, key=len, reverse=True):
            if low.startswith(w) and (len(low) == len(w) or not low[len(w)].isalnum()):
                hit = w
                break
        if not hit:
            break
        s = re.sub(r"^[\s,.!?:;]+", "", s[len(hit):])
    for g in _GIUA:
        s = re.sub(re.escape(g) + r"(?=[\s,.!?]|$)", "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    if len(re.sub(r"[\W_]", "", s)) < 4:
        # Việc chỉ là một đường link (chủ 27/11/2026: tiêu đề hiện nguyên "https://z4z.poha.vn/?utm_source=..."): gọi theo tên trang.
        lk = re.search(r"https?://([^/\s?#]+)", str(text or ""))
        s = ("Việc với trang " + re.sub(r"^www\.", "", lk.group(1))) if lk else (s or re.sub(r"\s+", " ", str(text or "")).strip())
    s = s[:1].upper() + s[1:]
    if len(s) > toi_da:
        s = s[:toi_da].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"
    return s


def _he_thong() -> str:
    return ("Bạn đặt tiêu đề cho danh sách việc của một đội AI, để chủ doanh nghiệp nhìn qua là biết việc đó là việc gì. Với MỖI việc, viết: "
            '"t" = tiêu đề ngắn tối đa 8 từ, dưới 55 ký tự, bắt đầu bằng động từ, nói rõ làm gì và về cái gì; '
            '"m" = một câu mô tả dưới 95 ký tự, nói việc ra kết quả gì hoặc đang ở đâu. '
            "Bỏ hết lời chào và lời dặn thừa (Alo, anh muốn em, em ơi, giúp anh, làm ơn...). Không bao giờ chép đường link vào \"t\"; việc chỉ có một đường link thì đặt tên theo trang đó (ví dụ Việc với trang z4z.poha.vn). Giữ tên riêng, con số quan trọng. Chỉ dùng thông tin đã cho, không bịa. Tiếng Việt, viết hoa đúng chính tả. "
            "Việc nào có trường \"tiep\" là việc làm NỐI TIẾP một việc trước: \"t\" chỉ nói PHẦN MỚI việc này làm (đừng lặp lại tên việc trước, đừng viết chữ Tiếp tục, nối tiếp, đang làm dở, bước), "
            "và thêm \"c\" = tên chuỗi 3 đến 4 từ gọi chung cả mạch việc (rút từ tên việc trước); nếu tiep.chuoi đã có thì chép NGUYÊN chữ đó vào \"c\". Việc không có \"tiep\" thì không cần \"c\". "
            'Trả CHỈ MỘT khối JSON hợp lệ dạng {"<id>": {"t": "...", "m": "...", "c": "..."}, ...}, không chữ nào ngoài JSON.')


async def _hoi_ai(ds: list) -> dict:
    import tisa_quang_cao_ai as AI
    ask = getattr(AI, "_ASK", None)
    if ask is None:
        return {}
    ndung = json.dumps([dict({"id": x["id"], "viec": x["title"][:400], "tom_tat_ket_qua": x["summary"][:300]}, **({"tiep": x["tiep"]} if x.get("tiep") else {})) for x in ds], ensure_ascii=False)
    raw = await asyncio.wait_for(ask(_he_thong(), "DANH SÁCH VIỆC (JSON):\n" + ndung + "\n\nHãy đặt tiêu đề."), 90)
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", str(raw or "").strip(), flags=re.I)
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j <= i:
        return {}
    d = json.loads(t[i:j + 1])
    return d if isinstance(d, dict) else {}


async def tieu_de(items: list) -> dict:
    ra, can = {}, []
    with _khoa:
        luu = _doc()
    for it in (items or [])[:60]:
        if not isinstance(it, dict) or not it.get("id"):
            continue
        i, title, summ = str(it["id"]), str(it.get("title") or ""), str(it.get("summary") or "")
        tp = it.get("tiep") if isinstance(it.get("tiep"), dict) else None
        tiep = {"ten": str(tp.get("ten") or "")[:140], "chuoi": str(tp.get("chuoi") or "")[:60], "buoc": int(tp.get("buoc") or 2)} if tp and tp.get("ten") else None
        h = _bam(title, summ, json.dumps(tiep, ensure_ascii=False) if tiep else "")
        e = luu.get(i)
        if isinstance(e, dict) and e.get("h") == h and e.get("t"):
            ra[i] = {"t": e["t"], "m": e.get("m") or "", "c": e.get("c") or "", "ai": bool(e.get("ai"))}
        else:
            ra[i] = {"t": rut_gon(title), "m": "", "c": (tiep["chuoi"] or rut_gon(tiep["ten"], 30)) if tiep else "", "ai": False}
            can.append({"id": i, "title": title, "summary": summ, "h": h, "tiep": tiep})
    can = can[:_TOI_DA_MOI_LAN]
    if can:
        try:
            kq = await _hoi_ai(can)
        except Exception as e:  # noqa: BLE001 - AI chưa sẵn sàng thì dùng bản rút gọn, lần sau thử lại
            print(f"[tisa_tieu_de] AI chưa tóm tắt được: {type(e).__name__}: {str(e)[:120]}")
            kq = {}
        moi = {}
        for x in can:
            v = kq.get(x["id"])
            if isinstance(v, dict) and str(v.get("t") or "").strip():
                t = re.sub(r"\s+", " ", str(v["t"])).strip()[:70]
                m = re.sub(r"\s+", " ", str(v.get("m") or "")).strip()[:120]
                c = ""
                if x.get("tiep"):
                    c = x["tiep"]["chuoi"] or re.sub(r"\s+", " ", str(v.get("c") or "")).strip()[:40] or rut_gon(x["tiep"]["ten"], 30)
                ra[x["id"]] = {"t": t, "m": m, "c": c, "ai": True}
                moi[x["id"]] = {"h": x["h"], "t": t, "m": m, "c": c, "ai": True}
        if moi:
            with _khoa:
                d = _doc()
                d.update(moi)
                if len(d) > 4000:   # giữ gọn: bỏ bớt phần cũ nhất
                    for k in list(d)[:len(d) - 4000]:
                        d.pop(k, None)
                _ghi(d)
    return ra


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.post("/tisa-doi-quan/tieu-de")
    async def _tieu_de(request: Request):
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Dữ liệu không đúng."}, status_code=400)
        return {"ok": True, "tieu_de": await tieu_de(body.get("items") if isinstance(body, dict) else [])}
