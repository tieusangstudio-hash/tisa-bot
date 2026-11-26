"""Chat với cộng sự: phần THUẦN (không I/O) của trang Cộng sự.

Ba việc:
1. `persona_cua_phien`: đọc cột `channel` của một phiên ra ("agent"|"workflow", slug). main.py
   dùng nó ở bộ điều phối lượt để rẽ nhánh: phiên trợ lý đổi system prompt, phiên quy trình
   chạy `execute_workflow` thay vì hỏi bộ não chính.
2. Quy trình chạy như một lượt chat: `chay()` tiêu thụ luồng sự kiện của execute_workflow,
   đẩy khung WebSocket cho khung chat (status) và cột phải (wf_event), rồi trả về kết quả
   để main.py dựng tin trả lời bằng `tin_xong` / `tin_loi` / `tin_cho_duyet`. Tách khỏi
   main.py để test được bằng một generator giả, không cần engine.

3. `quyet_dinh_luot`: tin vừa gửi là MỘT LẦN CHẠY, hay là câu nói VỀ CHÍNH quy trình
   ("cập nhật lại workflow...", "đánh giá lại quy trình 7 bước", "gộp bớt bước")? Tin loại sau
   phải đi bộ não chính để đọc/sửa file quy trình, không được nhồi vào `{{input}}`.

Luật quan trọng: một lần chạy KHÔNG BAO GIỜ kết thúc mà không có tin trong chat. Luồng đứt
(engine chết không kịp phát `error`) vẫn thành `trang_thai="error"` với câu lỗi rõ.

Ghi chú: KHÔNG dùng ký tự em dash.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

import tisa_core
import localefmt

TRAN_KET_QUA_TRUOC = 8000
_LOAI = ("agent", "workflow")


def persona_cua_phien(row: Optional[dict]) -> Optional[Tuple[str, str]]:
    ch = str((row or {}).get("channel") or "")
    # TISA Core (0.185.0) is not a persona: its chat is a normal TISA BOT turn plus a role block.
    if tisa_core.is_core_channel(ch):
        return None
    for loai in _LOAI:
        tien_to = loai + ":"
        if ch.startswith(tien_to) and len(ch) > len(tien_to):
            return loai, ch[len(tien_to):]
    return None


def ghep_dau_vao(user_message: str, ket_qua_truoc: str) -> str:
    """Tin sau trong cùng hội thoại vẫn hiểu được "sửa đoạn 2": nối kết quả lần trước vào."""
    u = str(user_message or "")
    k = str(ket_qua_truoc or "")
    if not k:
        return u
    return f"{u}\n\n# Kết quả lần trước\n{k[:TRAN_KET_QUA_TRUOC]}"


def tin_xong(so_lan: int, so_buoc: int, giay: int, ket_qua: str) -> str:
    than = str(ket_qua or "").strip() or localefmt.chu("(quy trình xong nhưng không có nội dung)",
                                                       "(the workflow finished but returned nothing)")
    return localefmt.chu(f"Lần chạy #{int(so_lan)} · {int(so_buoc)} bước · {int(giay)} giây\n\n{than}",
                         f"Run #{int(so_lan)} · {int(so_buoc)} steps · {int(giay)} seconds\n\n{than}")


def tin_loi(i: Optional[int], agent: str, loi: str) -> str:
    loi = str(loi or "").strip() or localefmt.chu("không rõ lý do", "reason unknown")
    if i is None:
        return localefmt.chu(f"Quy trình dừng vì lỗi: {loi}", f"The workflow stopped on an error: {loi}")
    ten = f" ({agent})" if agent else ""
    return localefmt.chu(f"Quy trình dừng ở bước {int(i) + 1}{ten}: {loi}",
                         f"The workflow stopped at step {int(i) + 1}{ten}: {loi}")


def tin_cho_duyet(node: str, prompt: str) -> str:
    p = str(prompt or "").strip()
    dau = localefmt.chu(f"Quy trình đang chờ duyệt bước \"{node}\"",
                        f"The workflow is waiting for approval of step \"{node}\"")
    return (dau + (f": {p}" if p else "")
            + localefmt.chu(". Bấm Duyệt ở cột phải để chạy tiếp.",
                            ". Press Approve in the right column to continue."))


# ============================================================
# Chạy TIẾP từ bước lỗi (V3.57)
# ============================================================
# Trước V3.57 một bước lỗi là cả lần chạy dừng, và tin "chạy tiếp bước 2" bị coi là một lần chạy MỚI: quy trình
# chạy lại từ bước 1 (làm lại đúng cái vừa lỗi, tốn thêm hàng phút, nhất là trên máy Windows mở tiến trình chậm).
# Giờ tin ngắn kiểu "chạy tiếp" / "tiếp tục" / "chạy từ bước 2" sau một lần chạy LỖI thì nạp lại kết quả các bước đã
# xong và chạy từ đúng bước hỏng (hoặc bước anh chỉ định). Hai hàm dưới đây là phần THUẦN để test không cần engine.
_LENH_TIEP = re.compile(
    r"\b(?:chay tiep|lam tiep|tiep tuc|chay lai|lam lai|thu lai|continue|resume|retry)\b"
    r"|\b(?:chay|lam|bat dau|tiep tuc|tu)\s+(?:tu\s+)?buoc\s*(\d{1,2})\b")
_SO_BUOC = re.compile(r"\bbuoc\s*(\d{1,2})\b")
# Từ đệm không mang việc mới. Tin còn lại QUÁ 1 từ lạ nghĩa là có đề bài ("tiếp tục viết bài về cà phê"): không phải lệnh.
_TU_DEM = frozenset((
    "anh", "em", "nhe", "nha", "di", "giup", "ok", "oke", "da", "vang", "thi", "cho", "hay", "nao", "buoc",
    "tu", "bay", "gio", "voi", "luon", "nua", "roi", "o", "la", "cai", "lan", "nay", "do", "ngay", "qua",
    "toi", "minh", "please", "pls", "again", "from", "step", "the", "it"))


def la_lenh_chay_tiep(user_message: str) -> Tuple[bool, Optional[int]]:
    """(đây là lệnh "chạy tiếp"?, số bước anh chỉ định hoặc None). Tin dài hoặc có đề bài thì KHÔNG phải lệnh."""
    d = _khong_dau(user_message).strip()
    d = re.sub(r"[^\w\s]", " ", d)
    if not d.strip() or len(d) > 60:
        return False, None
    m = _LENH_TIEP.search(d)
    if not m or re.search(r"\b(?:bo|bo qua|khong|dung|ngung|huy|thoi)\b", d):
        return False, None          # "bỏ bước 1", "đừng chạy"...: ý ngược lại, để đường cũ lo
    con = _SO_BUOC.sub(" ", _LENH_TIEP.sub(" ", d))
    con = [w for w in con.split() if w not in _TU_DEM and not w.isdigit()]
    if len(con) > 1:
        return False, None
    so = _SO_BUOC.search(d)
    n = int(so.group(1)) if so else (int(m.group(1)) if m.group(1) else None)
    return True, (n if n and n > 0 else None)


def diem_chay_tiep(run: Optional[dict], so_buoc_quy_trinh: int, so_yeu_cau: Optional[int] = None) -> Optional[dict]:
    """Điểm chạy tiếp của một lần chạy LỖI: {"start", "prev", "input", "xong"} hoặc None (không chạy tiếp được).

    `run`: bản ghi đầy đủ của lần chạy gần nhất trong phiên (workflow_runs.lay). Chỉ lần chạy `error` mới chạy tiếp được:
    `done` thì không có gì để tiếp, `waiting` có nút Duyệt riêng. Mặc định chạy tiếp từ bước đầu tiên CHƯA có kết quả.
    `so_yeu_cau` là số bước theo cách người dùng đếm (từ 1); bước trước nó mà có kết quả thì làm `{{prev}}`."""
    if not run:
        return None
    if str(run.get("status") or "") != "error":
        # V3.58: sau khi SỬA riêng một bước, tin báo dặn "chạy tiếp từ bước N": lần chạy đã xong cũng chạy tiếp được, nhưng CHỈ khi
        # chủ nói rõ số bước (từ bước 2 trở đi), để "tiếp tục" trần sau một lần chạy xong không bị hiểu nhầm.
        if not (str(run.get("status") or "") == "done" and so_yeu_cau and int(so_yeu_cau) >= 2):
            return None
    buoc = list(run.get("steps") or [])

    def _kq(i: int) -> str:
        b = buoc[i] if 0 <= i < len(buoc) else {}
        return "" if (b or {}).get("error") else str((b or {}).get("output") or "")

    xong = 0
    while xong < len(buoc) and _kq(xong).strip():
        xong += 1
    start = (int(so_yeu_cau) - 1) if so_yeu_cau else xong
    if start < 0 or start >= int(so_buoc_quy_trinh or 0):
        return None
    if so_yeu_cau is None and xong == 0:
        return None          # bước 1 lỗi và không có gì để giữ: chạy lại từ đầu là đúng, để đường chạy thường lo
    return {"start": start, "prev": _kq(start - 1) if start > 0 else "", "input": str(run.get("input") or ""),
            "xong": min(xong, start),
            "outs": [_kq(i) for i in range(start)],
            "agents": [str((buoc[i] if i < len(buoc) else {}).get("agent") or "") for i in range(start)]}


def tin_chay_tiep(start: int, tong: int, xong: int) -> str:
    giu = (localefmt.chu(f", giữ kết quả {int(xong)} bước đã xong", f", keeping the result of {int(xong)} finished step(s)")
           if xong else "")
    return localefmt.chu(f"Chạy tiếp từ bước {int(start) + 1}/{int(tong)}{giu}.",
                         f"Continuing from step {int(start) + 1}/{int(tong)}{giu}.")


def tin_thu_lai(i: int, lan: int, tong: int, giay: int) -> str:
    return localefmt.chu(
        f"Bước {int(i) + 1} gặp lỗi tạm thời, tự thử lại sau {int(giay)} giây (lần {int(lan)}/{int(tong)})...",
        f"Step {int(i) + 1} hit a temporary error, retrying in {int(giay)} seconds (attempt {int(lan)}/{int(tong)})...")


def _s(x) -> str:
    x = float(x)
    return ("%.1fs" % x) if x < 10 else ("%ds" % round(x))


def dong_thoi_gian(tms: list) -> str:
    """Một dòng nói thời gian từng bước đã tốn vào đâu (V3.59). Rỗng khi không có số đo hoặc đặt TISA_WORKFLOW_HIEN_THOI_GIAN=0.
    "tới chữ đầu" = từ lúc gọi tới khi bước có chữ/lệnh đầu tiên (gồm mở Claude, nối công cụ, nạp ngữ cảnh, model nghĩ); "mở Claude"
    và "công cụ" là phần ước lượng bên trong nó (có khi không có số, ví dụ bước không nối hub)."""
    import os
    if not tms or str(os.environ.get("TISA_WORKFLOW_HIEN_THOI_GIAN", "1")).strip() == "0":
        return ""
    phan = []
    for t in tms:
        try:
            ten = str(t.get("agent") or "").strip()
            chi = []
            if t.get("chu_dau_s") is not None:
                con = []
                if t.get("mo_claude_s") is not None:
                    con.append("mở Claude " + _s(t["mo_claude_s"]))
                if t.get("hub_s"):
                    con.append("công cụ " + _s(t["hub_s"]))
                chi.append("tới chữ đầu " + _s(t["chu_dau_s"]) + (" [" + ", ".join(con) + "]" if con else ""))
            if t.get("lam_s") is not None:
                chi.append("làm " + _s(t["lam_s"]))
            if t.get("kiem_chung_s"):
                chi.append("kiểm chứng " + _s(t["kiem_chung_s"]))
            if t.get("thu_lai"):
                chi.append("thử lại %d lần" % int(t["thu_lai"]))
            phan.append("B%d%s %s: %s" % (int(t.get("i") or 0) + 1, " (" + ten + ")" if ten else "", _s(t.get("tong_s") or 0), ", ".join(chi)))
        except Exception:  # noqa: BLE001 - số đo hỏng không được làm hỏng tin kết quả
            continue
    return ("⏱ Thời gian " + " · ".join(phan)) if phan else ""


NHIP_GIAY = 10.0      # 26/11/2026: cứ bấy nhiêu giây báo một dòng tiến độ trong lúc một bước đang chạy


def _nhan_cong_cu(ten: str) -> str:
    try:
        import tisa_tinh_hinh as TH
        return TH._nhan_dep(TH._ten_cong_cu(ten))
    except Exception:  # noqa: BLE001
        return str(ten or "")[:40]


def _phut_giay(s: float) -> str:
    s = int(max(0, s))
    return localefmt.chu("%d phút %02d giây" % (s // 60, s % 60), "%dm %02ds" % (s // 60, s % 60)) if s >= 60 else localefmt.chu("%d giây" % s, "%ds" % s)


def dong_nhip(i: int, tong: int, agent: str, giay: float, cong_cu: str = "", so_cong_cu: int = 0) -> str:
    """Dòng tiến độ của bước đang chạy (hàm thuần): "Bước 2/4: Biên tập viên đang làm · 1 phút 20 giây · vừa dùng: Ghi file (3 lần dùng công cụ)"."""
    dau = localefmt.chu("Bước %d/%d: %s đang làm" % (i + 1, tong, agent or "trợ lý"), "Step %d/%d: %s is working" % (i + 1, tong, agent or "assistant"))
    duoi = " · " + _phut_giay(giay)
    if cong_cu:
        duoi += localefmt.chu(" · vừa dùng: %s" % cong_cu, " · last tool: %s" % cong_cu)
    if so_cong_cu > 1:
        duoi += localefmt.chu(" (%d lần dùng công cụ)" % so_cong_cu, " (%d tool calls)" % so_cong_cu)
    elif not cong_cu and giay >= 30:
        duoi += localefmt.chu(" · đang suy nghĩ, chưa dùng công cụ", " · thinking, no tool yet")
    return dau + duoi


async def chay(events, emit: Callable[[dict], Awaitable[None]]) -> Dict[str, Any]:
    """Tiêu thụ luồng sự kiện của một lần chạy. `emit(frame)` gửi khung về trình duyệt.

    Khung phát ra:
    - `status` mỗi khi một bước bắt đầu (chip "đang làm" của khung chat);
    - `wf_event` cho MỌI sự kiện trừ `step_text` (cột phải vẽ tiến độ; step_text quá dày và
      cột phải không hiện chữ từng bước).
    Không phát `stream`: main.py gửi cả tin trả lời một lần sau khi có kết quả, để bong bóng
    sống và bản lưu giống hệt nhau.
    """
    kq: Dict[str, Any] = {"trang_thai": "error", "ket_qua": "", "so_buoc": 0, "loi": None,
                          "wait": None, "run_id": "", "timing": []}
    agent_cua_buoc: Dict[int, str] = {}
    buoc_dang_chay: Optional[int] = None
    da_ket = False
    tt = {"i": None, "luc": 0.0, "cong_cu": "", "so": 0}    # bước đang chạy, lúc bắt đầu, công cụ vừa dùng, số lần dùng

    async def _nhip():
        import asyncio as _aio
        import time as _t
        while True:
            await _aio.sleep(NHIP_GIAY)
            if tt["i"] is None:
                continue
            try:
                await emit({"type": "status", "content": dong_nhip(int(tt["i"]), kq["so_buoc"] or int(tt["i"]) + 1,
                                                                  agent_cua_buoc.get(int(tt["i"]), ""), _t.time() - tt["luc"],
                                                                  tt["cong_cu"], tt["so"])})
            except Exception:  # noqa: BLE001 - dòng tiến độ hỏng không được làm hỏng lần chạy
                pass
    import asyncio as _asyncio
    import time as _time
    _vong = _asyncio.ensure_future(_nhip())
    try:
        async for ev in events:
            t = ev.get("type")
            if t == "step_start":
                tt.update(i=int(ev.get("i") or 0), luc=_time.time(), cong_cu="", so=0)
            elif t == "step_tool":
                tt["cong_cu"] = _nhan_cong_cu(str(ev.get("tool") or ""))
                tt["so"] += 1
            elif t in ("step_done", "step_error", "done", "error", "wait_user"):
                tt["i"] = None
            if t == "start":
                kq["so_buoc"] = int(ev.get("steps") or 0)
                kq["run_id"] = str(ev.get("run_id") or "")
            elif t == "step_start":
                i = int(ev.get("i") or 0)
                buoc_dang_chay = i
                agent_cua_buoc[i] = str(ev.get("agent") or "")
                tong = kq["so_buoc"] or (i + 1)
                await emit({"type": "status", "content": localefmt.chu(
                    f"Bước {i + 1}/{tong}: {agent_cua_buoc[i]} đang làm...",
                    f"Step {i + 1}/{tong}: {agent_cua_buoc[i]} is working...")})
            elif t == "step_timing":
                if isinstance(ev.get("timing"), dict):
                    kq["timing"].append(ev["timing"])
            elif t == "step_auto_retry":
                await emit({"type": "status", "content": tin_thu_lai(
                    int(ev.get("i") or 0), int(ev.get("attempt") or 1), int(ev.get("of") or 1), int(ev.get("wait") or 0))})
            elif t == "done":
                kq["trang_thai"] = "done"
                kq["ket_qua"] = str(ev.get("result") or "")
                da_ket = True
            elif t == "error":
                # Lỗi của MỘT BƯỚC mang sẵn `i` và `agent` (main.py gắn khi bước hỏng): tin
                # theo nó trước. Chỉ rơi về "bước đang chạy" khi lỗi không thuộc bước nào
                # (không tìm thấy workflow, luồng đứt) - lúc đó `i` vắng mặt.
                i_loi = ev.get("i")
                i_loi = buoc_dang_chay if i_loi is None else int(i_loi)
                kq["trang_thai"] = "error"
                kq["loi"] = {"i": i_loi,
                             "agent": str(ev.get("agent") or agent_cua_buoc.get(
                                 i_loi if i_loi is not None else -1, "")),
                             "content": str(ev.get("content") or "")}
                da_ket = True
            elif t == "wait_user":
                kq["trang_thai"] = "waiting"
                kq["wait"] = dict(ev)
                da_ket = True
            if t != "step_text":
                await emit({"type": "wf_event", "event": dict(ev)})
    finally:
        _vong.cancel()
        aclose = getattr(events, "aclose", None)
        if aclose:
            try:
                await aclose()
            except Exception:
                pass
    if not da_ket:
        kq["trang_thai"] = "error"
        kq["loi"] = {"i": buoc_dang_chay, "agent": agent_cua_buoc.get(buoc_dang_chay if buoc_dang_chay is not None else -1, ""),
                     "content": localefmt.chu("luồng chạy không kết thúc (engine dừng mà không báo)",
                                              "the run never finished (the engine stopped without saying so)")}
    return kq


# ============================================================
# Tin NÓI VỀ chính quy trình, khác tin YÊU CẦU một lần chạy
# ============================================================
# Chuyện thật 16/09: ở phiên workflow:<slug>, mọi tin đều thành `{{input}}` của một lần chạy.
# Chủ dự án gõ "tôi muốn cập nhật lại workflow là có xuất bài viết ngay cả khi chưa đạt" và
# "tự đánh giá lại quy trình với 7 bước hiện tại, giảm số bước xuống" - hai câu nói VỀ quy
# trình - nên quy trình đem chúng đi viết bài: 7 bước, 640 giây, đốt hạn mức gói, trả ra một
# bản kiểm duyệt article.md chẳng liên quan gì tới câu hỏi.
#
# Chi phí của hai kiểu nhận nhầm KHÔNG bằng nhau, và đó là lý do chọn đoán thay vì hỏi lại:
#   - nhận nhầm tin nói-về-quy-trình thành lần chạy = 10 phút engine + hạn mức + kết quả rác;
#   - nhận nhầm một đề bài thành tin nói-về-quy-trình = một lượt chat rẻ, và câu trả lời có
#     kèm đúng một dòng chỉ cách ép chạy.
# Nên hàng rào này cố ý nghiêng về phía RẺ, và luôn nói ra là nó đã không chạy.

# Ép chạy: tiền tố ở đầu tin. Bấm nút "Chạy" ở cột phải gửi cờ `wf_run` nên không cần tiền tố.
TIEN_TO_CHAY = ("chay:", "run:")


def _khong_dau(s: str) -> str:
    """Bỏ dấu tiếng Việt + về chữ thường, để mẫu nhận dạng viết một lần là đủ.

    Người dùng gõ "quy trinh", "cap nhat" (không dấu) khá thường, nhất là trên điện thoại;
    khai hai bộ mẫu có dấu và không dấu thì thêm mẫu mới là chắc chắn lệch một bên."""
    x = unicodedata.normalize("NFD", str(s or ""))
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return x.replace("đ", "d").replace("Đ", "D").lower()


# ĐỘNG TỪ sửa/đánh giá. Cố ý KHÔNG có "chạy", "viết", "làm": đó là động từ của một đề bài.
_DONG_TU = (
    r"(?:danh gia|xem lai|ra soat|soat lai|kiem lai|cap nhat|sua|chinh|doi|viet lai|"
    r"thiet ke lai|toi uu|cai tien|hoan thien|rut gon|gian luoc|don gian hoa|gop|tach|"
    r"tom tat|giai thich|liet ke|bo|xoa|them|giam|bot|tang|"
    r"update|edit|change|evaluate|review|simplify|reduce|merge|summari[sz]e|explain|"
    r"optimi[sz]e)"
)
# DANH TỪ phải TỰ TRỎ vào quy trình đang mở. "quy trinh" trần KHÔNG tính: "viết bài tóm tắt
# quy trình làm nước mắm" là một đề bài, và nhận nhầm nó là câu hỏi về workflow thì người dùng
# mất một lần chạy họ thật sự muốn.
_DANH_TU = (
    r"(?:workflow|pipeline|steps|"
    r"quy trinh (?:nay|hien tai|tren|o day|dang mo|cua minh|cua toi)|"
    r"lai quy trinh|chinh quy trinh|so buoc|\d+ buoc|cac buoc (?:nay|hien tai)|buoc nao)"
)
# Hai chiều: động từ trước danh từ ("cập nhật lại workflow") và danh từ trước động từ
# ("quy trình này gộp bớt được không"). Khoảng cách tối đa 40 ký tự và KHÔNG vượt dấu kết câu:
# hai mệnh đề rời nhau trong cùng một tin thì không nói gì về nhau.
_KHONG_HET_CAU = r"[^.!?\n]{0,40}"
# Mẫu thứ ba: động từ DÍNH LIỀN "bước" ("bỏ bước kiểm chứng", "thêm bước QC ảnh", "gộp bước
# 2 và 3"). Đây là câu sửa cấu trúc quy trình rõ nhất mà hai mẫu trên không bắt được, vì danh
# từ ở đây là tên một bước cụ thể chứ không tự trỏ vào quy trình. Đòi DÍNH LIỀN nên "liệt kê
# các bước làm bánh" hay "viết bài theo từng bước" không lọt vào.
_MAU_SUA_BUOC = re.compile(r"\b(?:bo|xoa|them|gop|tach|doi|bot|giam|chen)\s+(?:mot\s+|1\s+)?buoc\b")
# Mẫu thứ tư: động từ SỬA dính liền "quy trình"/"workflow" mà sau đó KHÔNG phải một cụm định
# danh ("cập nhật quy trình:", "sửa quy trình đi", "rút gọn quy trình còn 4 bước").
# Vì sao phải xét cái đi sau: "viết bài tóm tắt quy trình làm nước mắm" cũng là động từ dính
# liền danh từ, nhưng "quy trình LÀM NƯỚC MẮM" là một quy trình KHÁC - đó là đề bài, nhận nhầm
# nó là người dùng mất đúng lần chạy họ muốn. Và động từ ở đây cố ý chỉ gồm nhóm SỬA/ĐÁNH GIÁ,
# không có "tóm tắt"/"giải thích"/"liệt kê": ba động từ đó là việc của một bài viết.
_DONG_TU_SUA = (
    r"(?:cap nhat|sua(?: lai)?|chinh(?: lai)?|doi|thiet ke lai|toi uu(?: lai)?|cai tien|"
    r"hoan thien|rut gon|gian luoc|don gian hoa|gop|tach|danh gia(?: lai)?|xem lai|"
    r"ra soat|soat lai|kiem lai|"
    r"update|edit|change|simplify|reduce|refactor|redesign|optimi[sz]e)"
)
_SAU_DANH_TU = (
    r"(?:$|[,.:;!?)\n]|\s+(?:nay|hien tai|tren|do|di|lai|voi|thanh|con|xuong|len|sao|"
    r"giup|cho|nhu|the|duoc|nhe)\b)"
)
_MAU_SUA_QUY_TRINH = re.compile(
    _DONG_TU_SUA + r"\s+(?:cai\s+|chinh\s+)?(?:quy trinh|workflow)" + _SAU_DANH_TU)
_MAU_VE_QUY_TRINH = (
    re.compile(_DONG_TU + r"\b" + _KHONG_HET_CAU + r"\b" + _DANH_TU),
    re.compile(_DANH_TU + r"\b" + _KHONG_HET_CAU + r"\b" + _DONG_TU),
    _MAU_SUA_BUOC,
    _MAU_SUA_QUY_TRINH,
)


def tach_lenh_chay(user_message: str) -> Tuple[bool, str]:
    """(ép chạy?, tin đã bỏ tiền tố). Tiền tố "chạy:" là đường thoát khi hàng rào đoán sai."""
    msg = str(user_message or "")
    dau = _khong_dau(msg.lstrip())
    for tt in TIEN_TO_CHAY:
        if dau.startswith(tt):
            return True, msg.lstrip()[len(tt):].lstrip()
    return False, msg


def la_tin_ve_quy_trinh(user_message: str) -> bool:
    """Tin này đang nói VỀ chính quy trình (sửa, đánh giá, tóm tắt nó) chứ không phải đề bài?"""
    dau = _khong_dau(user_message)
    if not dau.strip():
        return False
    return any(m.search(dau) for m in _MAU_VE_QUY_TRINH)


def quyet_dinh_luot(user_message: str, ep_chay: bool = False) -> Tuple[str, str]:
    """Rẽ nhánh một tin ở phiên workflow:<slug>. Trả ("chay"|"tra_loi", tin đã dọn tiền tố).

    Hàm THUẦN và module-level để test gọi thẳng: đây là chỗ quyết định một tin có đốt 10 phút
    engine hay không, mà quyết định không kiểm được thì không tin được.
    """
    tien_to, msg = tach_lenh_chay(user_message)
    if ep_chay or tien_to:
        return "chay", msg
    return ("tra_loi" if la_tin_ve_quy_trinh(msg) else "chay"), msg


def tin_khong_chay(ten: str = "") -> str:
    """Dòng nói THẲNG là lần chạy đã không khởi động, và cách ép chạy nếu đoán sai."""
    cua = f' "{ten}"' if str(ten or "").strip() else ""
    return localefmt.chu(
        "Tin này đang nói về chính quy trình" + cua + " nên được trả lời thay vì chạy. "
        "Muốn chạy thật với đúng câu này thì bấm nút Chạy ở cột phải, hoặc gửi lại với "
        "\"chạy:\" ở đầu tin.",
        "This message is about the workflow" + cua + " itself, so I answered instead of running it. "
        "To really run it with this exact message, press Run in the right column, or send it again "
        "starting with \"chạy:\".")


def khoi_quy_trinh_dang_mo(ten: str, slug: str, duong_dan: str, so_buoc: int,
                           buoc: Optional[list] = None) -> str:
    """Khối ngữ cảnh cho bộ não chính: người dùng đang đứng ở khung chat của quy trình nào.

    Cùng lối với khối "[FILE ĐANG MỞ...]" của trình sửa (xem CLAUDE.md): nói rõ file nào là
    đầu vào của lượt này, để câu "cập nhật lại workflow" không phải đoán xem workflow nào.
    Liệt kê luôn tên các bước - hỏi "gộp bớt bước được không" mà phải đi đọc file mới biết có
    những bước gì thì lượt trả lời nào cũng tốn thêm một vòng đọc file.
    """
    dong = [f"[QUY TRÌNH ĐANG MỞ trong trang Cộng sự: {ten} (slug: {slug}, {int(so_buoc)} bước)",
            f"File quy trình: {duong_dan}"]
    for i, b in enumerate(buoc or []):
        t = str((b or {}).get("task") or "").strip().replace("\n", " ")
        dong.append(f"  B{i + 1}. {(b or {}).get('agent') or '?'}: {t[:120]}")
    dong.append("Người dùng đang nói VỀ quy trình này, không phải đặt một đề bài cho nó. Đọc "
                "file trên trước khi trả lời; được yêu cầu sửa/gộp/thêm/bớt bước thì ghi thẳng "
                "vào chính file đó rồi nói đã đổi những gì. KHÔNG tự chạy quy trình.]")
    return "\n".join(dong)


# ============================================================
# Lịch chạy quy trình (26/11/2026, chủ yêu cầu): "chạy mỗi ngày lúc 6h sáng", "tắt lịch"
# ============================================================
NGAY_LICH = {"moi_ngay": "*", "t2_t6": "1-5", "t7_cn": "6,0"}
TEN_NGAY_LICH = {"moi_ngay": ("mỗi ngày", "every day"), "t2_t6": ("thứ 2 đến thứ 6", "Monday to Friday"),
                 "t7_cn": ("thứ 7 và chủ nhật", "weekends")}


def cron_lich(gio: int, phut: int, ngay: str) -> str:
    """Biểu thức cron 5 trường cho giờ:phút và kiểu ngày (moi_ngay | t2_t6 | t7_cn)."""
    gio, phut = int(gio), int(phut)
    if not (0 <= gio <= 23 and 0 <= phut <= 59):
        raise ValueError(localefmt.chu("Giờ không hợp lệ", "Invalid time"))
    return "%d %d * * %s" % (phut, gio, NGAY_LICH.get(ngay, "*"))


_LICH_TU = re.compile(r"\b(?:moi ngay|hang ngay|moi sang|moi toi|moi trua|moi chieu|lich chay|lich|hen gio|dat gio|tu dong chay|"
                      r"ngay thuong|ngay lam viec|cuoi tuan|thu 2 den thu 6|t2 den t6|t2 t6)\b")
_LICH_TAT = re.compile(r"\b(?:tat|bo|huy|xoa|ngung|dung)\s+(?:het\s+)?(?:lich|hen gio|chay tu dong|lich chay)\b")
_LICH_GIO = re.compile(r"\b(\d{1,2})\s*(?:h|g|gio|:)\s*(\d{1,2})?\b")


def doc_lenh_lich(user_message: str) -> Optional[Dict[str, Any]]:
    """Tin này là lệnh đặt / tắt lịch chạy quy trình? {"tat": True} | {"gio", "phut", "ngay"} | None. Hàm thuần.
    Chỉ nhận tin NGẮN có từ chỉ lịch (mỗi ngày, hằng ngày, hẹn giờ, lịch...) và có giờ, để không nuốt nhầm một đề bài."""
    d = re.sub(r"[^a-z0-9: ]+", " ", _khong_dau(user_message)).strip()
    d = re.sub(r"\s+", " ", d)
    if not d or len(d) > 140:
        return None
    if _LICH_TAT.search(d):
        return {"tat": True}
    if not _LICH_TU.search(d):
        return None
    m = _LICH_GIO.search(d)
    if not m:
        return None
    gio, phut = int(m.group(1)), int(m.group(2) or 0)
    if re.search(r"\b(?:chieu|toi|pm)\b", d) and gio < 12:
        gio += 12
    if not (0 <= gio <= 23 and 0 <= phut <= 59):
        return None
    ngay = "moi_ngay"
    if re.search(r"\b(?:ngay thuong|ngay lam viec|thu 2 den thu 6|t2 den t6|t2 t6)\b", d):
        ngay = "t2_t6"
    elif re.search(r"\b(?:cuoi tuan|thu 7 va chu nhat|t7 va cn)\b", d):
        ngay = "t7_cn"
    return {"gio": gio, "phut": phut, "ngay": ngay}


def tin_lich(ten: str, gio: int, phut: int, ngay: str, lan_toi: str = "") -> str:
    vi, en = TEN_NGAY_LICH.get(ngay, TEN_NGAY_LICH["moi_ngay"])
    return localefmt.chu(
        "Đã đặt lịch: quy trình \"%s\" tự chạy lúc %02d:%02d %s%s. Kết quả gửi vào ô chat này (và báo chuông nếu dừng giữa chừng). "
        "Nhắn \"tắt lịch\" để bỏ, hoặc sửa ở mục Lịch chạy bên phải." % (ten, gio, phut, vi, (" (lần tới: %s)" % lan_toi) if lan_toi else ""),
        "Scheduled: workflow \"%s\" runs at %02d:%02d %s%s. Results come to this chat (and the bell if it stops). "
        "Send \"tắt lịch\" to remove it, or edit it under Schedule on the right." % (ten, gio, phut, en, (" (next: %s)" % lan_toi) if lan_toi else ""))

