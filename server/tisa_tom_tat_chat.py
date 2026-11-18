"""tisa_tom_tat_chat.py - Tự tóm tắt nội dung cuộc hội thoại thành TÊN ngắn cho ô chat (chủ yêu cầu 18/11/2026).

Trước đây tên ô chat là mấy chữ đầu của tin nhắn đầu tiên, nên danh sách có hàng chục ô cùng tên kiểu "Dùng skill dq-ho-tro-ket-noi: KẾT NỐI TỰ ĐỘNG..."
hay "Alo em ơi...", nhìn không biết đã trao đổi gì. Module này nhờ bộ não AI đọc cuộc trò chuyện rồi đặt MỘT tên ngắn (tối đa 7 từ) nói rõ nội dung.

  - Sau mỗi lượt trả lời, nếu tên ô chat còn là tên máy đặt (chữ đầu của tin nhắn đầu) hoặc tên AI đặt lần trước thì tóm tắt lại ở các mốc 2, 8, 24 tin nhắn
    (đầu cuộc chỉ biết sơ, càng nói nhiều tên càng đúng chủ đề). Tên anh/chị tự đặt (khác hai loại trên) thì KHÔNG BAO GIỜ bị đè.
  - Một lần sau khi cập nhật: tóm tắt lại tối đa 20 ô chat gần nhất đang mang tên máy đặt. Làm lại tay: POST /tisa-tom-tat-chat/lam-lai {"so": 20} hoặc {"sid": "..."}.
  - AI chưa sẵn sàng (chưa đăng nhập, hết lượt) thì giữ tên cũ, lần sau thử lại. Không bao giờ làm hỏng việc trả lời.
Một lượt AI chỉ chữ, không công cụ (cùng đường với trang Quảng Cáo: tisa_quang_cao_ai._ASK).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

MOC = (2, 8, 24)                  # số tin nhắn để tóm tắt (lần 1, 2, 3)
TOI_DA_KY_TU = 56
_khoa = threading.RLock()
_dang_lam: set = set()


def _thu_muc() -> Path:
    try:
        import config as _cfg
        d = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        d = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tep() -> Path:
    return _thu_muc() / "chat-tieu-de-ai.json"


def _doc() -> dict:
    try:
        d = json.loads(_tep().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _ghi(d: dict) -> None:
    if len(d) > 5000:
        for k in list(d)[:len(d) - 5000]:
            d.pop(k, None)
    t = _tep().with_suffix(".tmp")
    t.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    os.replace(t, _tep())


# ---------------------------------------------------------------- làm sạch nội dung
def _sach(text: str) -> str:
    s = str(text or "")
    try:
        import chat_recall
        s = chat_recall.strip_block(s)
    except Exception:  # noqa: BLE001
        pass
    try:
        import channel_context
        s = channel_context.strip_control_blocks(s)
    except Exception:  # noqa: BLE001
        pass
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"[#*_>`|]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def dung_de_tom_tat(tin_nhan: list) -> str:
    """Đoạn hội thoại rút gọn (≤ ~2200 ký tự) đưa cho AI: hai tin đầu của người dùng, câu cuối của người dùng và câu trả lời cuối."""
    u = [(_sach(m.get("content")), m) for m in tin_nhan if m.get("role") == "user"]
    a = [_sach(m.get("content")) for m in tin_nhan if m.get("role") == "assistant"]
    u = [x for x, _ in u if x]
    a = [x for x in a if x]
    dong = []
    for i, x in enumerate(u[:2]):
        dong.append("NGƯỜI DÙNG%s: %s" % (" (đầu tiên)" if i == 0 else "", x[:650]))
    if len(u) > 3:
        dong.append("... (còn %d lượt trao đổi giữa chừng)" % (len(u) - 3))
    if len(u) > 2:
        dong.append("NGƯỜI DÙNG (gần nhất): %s" % u[-1][:450])
    if a:
        dong.append("AI TRẢ LỜI (gần nhất): %s" % a[-1][:500])
    return "\n".join(dong)[:2300]


_HE_THONG = ("Bạn đặt TÊN cho một cuộc hội thoại để chủ doanh nghiệp nhìn danh sách là biết cuộc đó nói về việc gì. "
             "Quy tắc: tiếng Việt có dấu; TỐI ĐA 7 từ và dưới 50 ký tự; nêu đúng chủ đề hoặc việc cụ thể (làm gì, về cái gì, tên riêng nếu có); "
             "bắt đầu bằng động từ hoặc danh từ chính; bỏ lời chào, lời dặn, tên skill, tên công cụ nội bộ (ví dụ 'Dùng skill dq-...'); "
             "không dấu ngoặc kép, không chấm cuối, không viết 'Hội thoại về', 'Cuộc trò chuyện'. Chỉ dùng thông tin đã cho, không bịa. "
             "Ví dụ tên tốt: 'Nối Canva vào TISA BOT', 'Lên kịch bản video bán nhà Gò Vấp', 'Sửa lỗi mở khóa máy Mac', 'Báo cáo quảng cáo Facebook tuần này'. "
             "Trả CHỈ tên, một dòng, không giải thích.")


def lam_sach_ten(raw: str) -> str:
    s = str(raw or "").strip().splitlines()[0] if str(raw or "").strip() else ""
    s = re.sub(r"^(tên|tiêu đề|title)\s*[:\-]\s*", "", s, flags=re.I)
    s = s.strip().strip("\"'“”‘’`*#_ ").rstrip(".:;,!?… ").strip()
    s = re.sub(r"\s+", " ", s)
    if not s or "{" in s or "}" in s or len(s) < 4:
        return ""
    if len(s) > TOI_DA_KY_TU:
        s = s[:TOI_DA_KY_TU].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"
    return s[:1].upper() + s[1:]


# ---------------------------------------------------------------- tên máy đặt hay anh tự đặt
def _chuan(x: str) -> str:
    return re.sub(r"[\W_]+", " ", str(x or "").lower()).strip()


def _la_ten_may(store, sess: dict, tin_nhan: list, st: dict | None) -> bool:
    """True nếu tên hiện tại do máy đặt (trống, bằng chữ đầu tin nhắn đầu, hoặc đúng tên AI đặt lần trước). Tên anh tự đặt thì False."""
    ten = str((sess or {}).get("title") or "").strip()
    if not ten:
        return True
    if st and st.get("ai") and ten == st["ai"]:
        return True
    dau = next((m for m in tin_nhan if m.get("role") == "user"), None)
    if not dau:
        return False
    try:
        import sessions
        mau = sessions.title_from_message(str(dau.get("content") or ""))
    except Exception:  # noqa: BLE001
        mau = ""
    if mau and ten == mau:
        return True
    if not ten.endswith("…"):
        return False
    goc = _chuan(ten.rstrip("….").strip())    # tên bị cắt "…" của cách đặt cũ: là phần đầu của tin nhắn đầu (so sánh bỏ dấu câu, khoảng trắng, hoa thường)
    return len(goc) >= 8 and goc in _chuan(str(dau.get("content") or ""))


async def _hoi_ai(noi_dung: str) -> str:
    import tisa_quang_cao_ai as AI
    ask = getattr(AI, "_ASK", None)
    if ask is None:
        return ""
    raw = await asyncio.wait_for(ask(_HE_THONG, "CUỘC HỘI THOẠI:\n" + noi_dung + "\n\nHãy đặt tên."), 60)
    return lam_sach_ten(raw)


def _can_tom_tat(n: int, giai_doan: int) -> bool:
    can = sum(1 for m in MOC if n >= m)
    return can > giai_doan


async def tom_tat_mot(store, sid: str, ep: bool = False) -> dict:
    """Tóm tắt một ô chat nếu tới mốc (hoặc ep=True). Trả {"ok", "ten"|"ly_do"}."""
    if sid in _dang_lam:
        return {"ok": False, "ly_do": "đang làm"}
    _dang_lam.add(sid)
    try:
        sess = await asyncio.to_thread(store.get_session, sid)
        if not sess:
            return {"ok": False, "ly_do": "không thấy ô chat"}
        tin = await asyncio.to_thread(store.get_messages, sid)
        tin = [m for m in tin if m.get("role") in ("user", "assistant")]
        with _khoa:
            st = _doc().get(sid) or {}
        if not _la_ten_may(store, sess, tin, st):
            return {"ok": False, "ly_do": "tên do anh tự đặt, giữ nguyên"}
        if len(tin) < 2:
            return {"ok": False, "ly_do": "chưa đủ nội dung"}
        gd = int(st.get("gd") or 0)
        if not ep and not _can_tom_tat(len(tin), gd):
            return {"ok": False, "ly_do": "chưa tới mốc tóm tắt"}
        nd = dung_de_tom_tat(tin)
        if not nd.strip():
            return {"ok": False, "ly_do": "không có chữ để tóm tắt"}
        try:
            ten = await _hoi_ai(nd)
        except Exception as e:  # noqa: BLE001 - AI chưa sẵn sàng: giữ tên cũ, lần sau thử lại
            print("[tisa_tom_tat_chat] AI chưa tóm tắt được: %s: %s" % (type(e).__name__, str(e)[:100]), file=sys.stderr)
            return {"ok": False, "ly_do": "AI chưa sẵn sàng"}
        if not ten:
            return {"ok": False, "ly_do": "AI không trả tên hợp lệ"}
        # đọc lại ngay trước khi ghi: lúc chờ AI anh có thể vừa tự đổi tên
        sess2 = await asyncio.to_thread(store.get_session, sid)
        if not _la_ten_may(store, sess2, tin, st):
            return {"ok": False, "ly_do": "anh vừa tự đổi tên, giữ nguyên"}
        await asyncio.to_thread(store.rename, sid, ten)
        with _khoa:
            d = _doc()
            d[sid] = {"ai": ten, "gd": sum(1 for m in MOC if len(tin) >= m), "n": len(tin), "luc": int(time.time())}
            _ghi(d)
        return {"ok": True, "ten": ten}
    except Exception as e:  # noqa: BLE001
        print("[tisa_tom_tat_chat] lỗi: %s: %s" % (type(e).__name__, str(e)[:120]), file=sys.stderr)
        return {"ok": False, "ly_do": type(e).__name__}
    finally:
        _dang_lam.discard(sid)


def _store():
    try:
        import sessions
        if hasattr(sessions, "get_store"):
            return sessions.get_store()
    except Exception:  # noqa: BLE001
        pass
    for ten in ("main", "__main__"):
        m = sys.modules.get(ten)
        if m is not None and hasattr(m, "get_store"):
            try:
                return m.get_store()
            except Exception:  # noqa: BLE001
                return None
    return None


def sau_luot(sid: str) -> None:
    """Gọi sau khi lượt trả lời đã lưu (trong luồng async của máy chủ). Chạy nền, không chặn, không bao giờ ném lỗi."""
    try:
        st = _store()
        if st is None or not sid:
            return
        asyncio.get_running_loop().create_task(_sau_luot(st, str(sid)))
    except Exception:  # noqa: BLE001
        pass


async def _sau_luot(store, sid: str) -> None:
    await asyncio.sleep(1.0)
    await tom_tat_mot(store, sid)


async def lam_lai_gan_day(store, so: int = 20, nghi: float = 2.0) -> dict:
    """Tóm tắt tối đa `so` ô chat gần nhất đang mang tên máy đặt (không đụng tên anh tự đặt)."""
    ds = await asyncio.to_thread(store.list_sessions, 80)
    xong, bo = 0, 0
    for s in ds:
        if xong >= so:
            break
        sid = str(s.get("id") or "")
        if not sid:
            continue
        kq = await tom_tat_mot(store, sid, ep=True)
        if kq.get("ok"):
            xong += 1
            await asyncio.sleep(nghi)
        else:
            bo += 1
            if kq.get("ly_do") == "AI chưa sẵn sàng":
                break
    return {"ok": True, "da_dat_ten": xong, "bo_qua": bo}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.post("/tisa-tom-tat-chat/lam-lai")
    async def _lam_lai(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        st = _store()
        if st is None:
            return JSONResponse({"ok": False, "ly_do": "chưa sẵn sàng"})
        sid = str((d or {}).get("sid") or "")
        if sid:
            return JSONResponse(await tom_tat_mot(st, sid, ep=True))
        return JSONResponse(await lam_lai_gan_day(st, max(1, min(int((d or {}).get("so") or 20), 60))))

    @app.on_event("startup")
    async def _lam_lai_mot_lan():
        """Một lần sau khi cập nhật: đặt lại tên cho các ô chat gần nhất còn mang tên máy đặt. Có dấu hiệu đã làm nên không lặp lại."""
        dau = _thu_muc() / "chat-tieu-de-ai-lan-dau.json"
        if dau.exists() or os.environ.get("TISA_BO_QUA_TOM_TAT_CHAT") == "1":
            return

        async def chay():
            await asyncio.sleep(90)
            st = _store()
            if st is None:
                return
            kq = await lam_lai_gan_day(st, 20)
            if kq.get("da_dat_ten", 0) > 0:        # AI chưa sẵn sàng (0 ô được đặt) thì lần khởi động sau thử lại
                try:
                    dau.write_text(json.dumps({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), **kq}), encoding="utf-8")
                except OSError:
                    pass
        asyncio.get_running_loop().create_task(chay())
