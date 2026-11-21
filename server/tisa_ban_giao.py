"""tisa_ban_giao.py - Phiếu bàn giao giữa các cộng sự + chuỗi nối đuôi (V3.39, chủ yêu cầu 21/11/2026).

Vấn đề: cộng sự 1 lên ý tưởng xong (vd lên kế hoạch coaching và đặc tả web) nhưng việc làm tiếp thuộc cộng sự khác (Quản Trị WEB có mã
nguồn, biết đưa web lên Cloudflare). Trước đây anh phải chép tay, mà chép cả ô chat thì người nhận ngợp, chép một đoạn thì thiếu bối cảnh.

Cách làm:
  1. Nút "Bàn giao" dưới câu trả lời của cộng sự. Bấm vào, chính bộ não đọc cuộc chat rồi soạn một PHIẾU BÀN GIAO ngắn: mục tiêu, các việc
     (anh tích chọn việc nào giao đi), đã chốt, tệp đầu vào, câu còn treo, tiêu chí xong; kèm gợi ý cộng sự nhận theo chức danh.
  2. Anh sửa phiếu rồi bấm Giao. Phiếu lưu thành tệp trong bộ não (ban-giao/<ngày>/<mã>-<tên>.md) và tạo MỘT việc Kanban gắn mã cộng sự nhận,
     đúng đường của nút Giao việc ở trang Cộng sự (POST /agents/<slug>/jobs). Người nhận đọc phiếu, không đọc cả ô chat.
  3. Chuỗi nối đuôi: anh khai trước bạn thứ ba, thứ tư. Khi một bước XONG, máy soạn sẵn phiếu cho bước kế từ kết quả vừa có và chờ anh duyệt
     (mặc định), hoặc tự giao tiếp nếu anh bật "tự chạy tiếp". Bước lỗi, bị chặn, bị hủy thì chuỗi dừng và báo anh.
  Việc đối ngoại (đăng bài, gửi tin, chạy quảng cáo, đưa web lên mạng, thanh toán) luôn ghi trong phiếu là phải xin anh duyệt, kể cả chạy tự động.

Một lượt AI chỉ chữ, không công cụ (cùng đường với trang Quảng Cáo: tisa_quang_cao_ai._ASK). Không dùng ký tự em dash.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import threading
import time
import unicodedata
import uuid
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

THU_MUC_PHIEU = "ban-giao"
CHU_KY_VONG_S = 25
TOI_DA_BUOC_CHUOI = 5
TOI_DA_LICH_SU = 14000      # ký tự cuộc chat đưa cho AI
TOI_DA_TIN_CHON = 7000      # ký tự của câu trả lời được chọn
TOI_DA_KET_QUA = 7000       # ký tự kết quả của bước trước đưa cho AI soạn phiếu tiếp
LUAT_DOI_NGOAI = ("Việc ra ngoài (đăng bài, gửi tin cho khách, chạy hay bật quảng cáo, đưa web lên mạng, thanh toán, xóa dữ liệu) "
                  "phải xin anh duyệt trước khi làm. Việc không nằm trong danh sách ở trên là của bạn khác, không làm.")
_khoa = threading.RLock()


# ---------------------------------------------------------------- tiện ích thuần
def _ascii(s: str, mx: int = 40) -> str:
    x = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D").encode("ascii", "ignore").decode().lower()
    x = re.sub(r"[^a-z0-9]+", "-", x).strip("-")
    return (x[:mx].strip("-")) or "phieu"


def _chuoi(v, mx: int) -> str:
    return re.sub(r"[ \t]+", " ", str(v or "")).strip()[:mx]


def _ds_chuoi(v, so: int, mx: int) -> list:
    if isinstance(v, str):
        v = [x for x in re.split(r"\r?\n", v)]
    out = []
    for x in (v or []):
        t = _chuoi(re.sub(r"^\s*(?:[-*\u2022]|\d+[.)])\s*", "", str(x or "")), mx)
        if t:
            out.append(t)
    return out[:so]


def chuan_phieu(d) -> dict:
    """Làm sạch một phiếu (từ AI hay từ giao diện): đúng kiểu, đúng cỡ."""
    d = d if isinstance(d, dict) else {}
    viec = []
    for x in (d.get("viec") or []):
        if isinstance(x, str):
            x = {"text": x, "giao": True}
        if not isinstance(x, dict):
            continue
        t = _chuoi(x.get("text"), 420)
        if t:
            viec.append({"text": t, "giao": x.get("giao") is not False})
    return {
        "tieu_de": _chuoi(d.get("tieu_de"), 140),
        "muc_tieu": _chuoi(d.get("muc_tieu"), 700),
        "viec": viec[:14],
        "da_chot": _ds_chuoi(d.get("da_chot"), 10, 320),
        "dau_vao": _ds_chuoi(d.get("dau_vao"), 12, 320),
        "con_treo": _ds_chuoi(d.get("con_treo"), 10, 320),
        "xong_khi": _chuoi(d.get("xong_khi"), 320),
    }


def tach_json(raw: str):
    """Lấy khối JSON đầu tiên trong câu trả lời của AI (có thể kèm rào ``` hay lời dẫn). Không được thì None."""
    s = str(raw or "")
    s = re.sub(r"```(?:json)?", "", s)
    a, b = s.find("{"), s.rfind("}")
    if a < 0 or b <= a:
        return None
    try:
        d = json.loads(s[a:b + 1])
        return d if isinstance(d, dict) else None
    except ValueError:
        return None


def viec_duoc_giao(phieu: dict) -> list:
    return [x["text"] for x in (phieu.get("viec") or []) if x.get("giao")]


def dung_markdown(rec: dict, phieu: dict) -> str:
    """Nội dung tệp phiếu bàn giao (đọc được bằng mắt và bằng AI)."""
    p = chuan_phieu(phieu)
    dong = ["---", "type: ban-giao", "id: %s" % rec.get("id", ""), "title: %s" % (p["tieu_de"] or "Phiếu bàn giao"),
            "tu: %s" % rec.get("tu_ten", ""), "den: %s" % rec.get("den_ten", ""), "created: %s" % time.strftime("%Y-%m-%d %H:%M"),
            "---", "", "# %s" % (p["tieu_de"] or "Phiếu bàn giao"), "",
            "Từ **%s** cho **%s**." % (rec.get("tu_ten", ""), rec.get("den_ten", "")), ""]
    dong += ["## Mục tiêu", p["muc_tieu"] or "(chưa ghi)", "", "## Việc giao đi (chỉ làm các việc này)"]
    giao = viec_duoc_giao(p)
    dong += ["%d. %s" % (i + 1, t) for i, t in enumerate(giao)] or ["(không có)"]
    khong = [x["text"] for x in p["viec"] if not x.get("giao")]
    if khong:
        dong += ["", "## Việc KHÔNG giao (người bàn giao giữ lại, đừng làm)"] + ["- " + t for t in khong]
    for ten, ds in (("Đã chốt / ràng buộc", p["da_chot"]), ("Tệp đầu vào", p["dau_vao"]), ("Còn treo (hỏi anh, không tự đoán)", p["con_treo"])):
        if ds:
            dong += ["", "## " + ten] + ["- " + t for t in ds]
    dong += ["", "## Xong khi", p["xong_khi"] or "(chưa ghi, hỏi lại anh)", "", "## Luật", LUAT_DOI_NGOAI]
    chuoi = rec.get("chuoi") or []
    if chuoi:
        dong += ["", "## Chuỗi nối đuôi", "Sau khi xong, kết quả được chuyển tiếp cho: " + " , ".join(
            str(x.get("ten") or x.get("slug") or x) if isinstance(x, dict) else str(x) for x in chuoi) +
            ". Ghi rõ kết quả và đường dẫn các tệp tạo ra ở câu trả lời cuối để bàn giao tiếp."]
    return "\n".join(dong) + "\n"


def dung_loi_giao(rec: dict, phieu: dict, tep: str) -> str:
    """Lời giao việc đưa cho cộng sự nhận (đủ ý để làm ngay, kèm đường dẫn phiếu đầy đủ)."""
    p = chuan_phieu(phieu)
    giao = viec_duoc_giao(p)
    dong = ["BÀN GIAO VIỆC TỪ %s CHO %s" % (rec.get("tu_ten", ""), rec.get("den_ten", ""))]
    if tep:
        dong.append("Phiếu đầy đủ (đọc trước khi làm): %s" % tep)
    dong += ["", "MỤC TIÊU: " + (p["muc_tieu"] or p["tieu_de"] or "(xem phiếu)"), "", "VIỆC CẦN LÀM (chỉ làm các việc này):"]
    dong += ["%d. %s" % (i + 1, t) for i, t in enumerate(giao)]
    for ten, ds in (("ĐÃ CHỐT / RÀNG BUỘC", p["da_chot"]), ("TỆP ĐẦU VÀO", p["dau_vao"]), ("CÒN TREO (hỏi anh, không tự đoán)", p["con_treo"])):
        if ds:
            dong += ["", ten + ":"] + ["- " + t for t in ds]
    if p["xong_khi"]:
        dong += ["", "XONG KHI: " + p["xong_khi"]]
    chuoi = rec.get("chuoi") or []
    if chuoi:
        ten_tiep = str((chuoi[0].get("ten") if isinstance(chuoi[0], dict) else chuoi[0]) or "")
        dong += ["", "SAU KHI XONG kết quả được chuyển tiếp cho %s. Ở câu trả lời cuối, ghi rõ đã làm gì, kết quả ra sao và đường dẫn các tệp tạo ra." % ten_tiep]
    dong += ["", "LUẬT: " + LUAT_DOI_NGOAI]
    return "\n".join(dong)


# ---------------------------------------------------------------- kho trạng thái
def _thu_muc() -> Path:
    try:
        import config as _cfg
        d = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        d = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tep_kho() -> Path:
    return _thu_muc() / "ban-giao.json"


def _doc() -> dict:
    try:
        d = json.loads(_tep_kho().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _ghi(d: dict) -> None:
    ks = list(d)
    if len(ks) > 400:
        for k in ks[:len(ks) - 400]:
            d.pop(k, None)
    t = _tep_kho().with_suffix(".tmp")
    t.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    os.replace(t, _tep_kho())


def _luu(rec: dict) -> None:
    with _khoa:
        d = _doc()
        d[rec["id"]] = rec
        _ghi(d)


def _lay(pid: str):
    with _khoa:
        return _doc().get(str(pid))


# ---------------------------------------------------------------- nối với máy chủ chính
def _m():
    for ten in ("main", "__main__"):
        m = sys.modules.get(ten)
        if m is not None and hasattr(m, "_agents_dir") and hasattr(m, "tasks_feature"):
            return m
    return None


def _brain(b: str = "") -> str:
    return str(b or "brain")


def danh_sach_cong_su(m, brain: str, tru: str = "") -> list:
    out = []
    for a in m.agents_index(brain, kem_prompt=False):
        if tru and a.get("slug") == tru:
            continue
        out.append({"slug": a["slug"], "name": a.get("name") or a["slug"], "role": str(a.get("role") or "")[:160],
                    "skills": [str(s) for s in (a.get("skills") or [])][:8]})
    return out


def nguon_cua_phien(m, sid: str):
    """(slug, tên) của cộng sự đang chat ở phiên này; chat thường thì ('', 'TISA BOT')."""
    ss = m.get_store()
    s = ss.get_session(sid) or {}
    kenh = str(s.get("channel") or "")
    if kenh.startswith("agent:"):
        slug = kenh[len("agent:"):]
        ten = slug
        try:
            p = m._agent_md_path(m._brain_key(_brain(s.get("brain"))), slug)
            if p:
                meta, _b = m._read_md(p)
                ten = str((meta or {}).get("name") or slug)
        except Exception:  # noqa: BLE001
            pass
        return slug, ten
    return "", "TISA BOT"


def _sach(t: str) -> str:
    s = str(t or "")
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
    return s.strip()


def lich_su_de_soan(tin: list, mid: str = "") -> str:
    """Cuộc chat rút gọn đưa cho AI: câu được chọn đầy đủ, phần còn lại lấy từ cuối ngược lên tới hết hạn mức."""
    tin = [t for t in tin if t.get("role") in ("user", "assistant") and _sach(t.get("content"))]
    chon = None
    if mid:
        chon = next((t for t in tin if str(t.get("id")) == str(mid)), None)
    if chon is None and tin:
        chon = next((t for t in reversed(tin) if t.get("role") == "assistant"), tin[-1])
    dong, tong = [], 0
    for t in reversed(tin):
        if t is chon:
            continue
        x = _sach(t.get("content"))[:1800]
        d = "%s: %s" % ("ANH" if t.get("role") == "user" else "CỘNG SỰ", x)
        if tong + len(d) > TOI_DA_LICH_SU:
            break
        dong.append(d)
        tong += len(d)
    dong.reverse()
    cau = _sach(chon.get("content"))[:TOI_DA_TIN_CHON] if chon else ""
    return "CUỘC CHAT (cũ tới mới):\n" + "\n\n".join(dong) + "\n\nCÂU TRẢ LỜI CẦN BÀN GIAO (đầy đủ):\n" + cau


_HE_THONG = (
    "Bạn là người soạn PHIẾU BÀN GIAO giữa các cộng sự AI của anh (Học Viện TISA). Một cộng sự vừa làm xong phần của mình và anh muốn "
    "giao phần việc tiếp theo cho cộng sự khác. Người nhận KHÔNG đọc được cuộc chat, chỉ đọc phiếu này, nên phiếu phải tự đứng được. "
    "Trả về DUY NHẤT một khối JSON (không giải thích, không rào ```), các khóa: "
    '"tieu_de" (tên phiếu, tối đa 12 từ), "muc_tieu" (1 đến 2 câu: kết quả cuối cùng cần có), '
    '"viec" (danh sách {"text": một hành động cụ thể người nhận làm được ngay, "giao": true nếu thuộc chuyên môn người nhận, false nếu là việc '
    'của người bàn giao), "da_chot" (điều đã quyết định hay ràng buộc người nhận phải tuân theo), "dau_vao" (đường dẫn tệp hay tài liệu cần đọc, lấy đúng từ cuộc chat), '
    '"con_treo" (điều chưa chắc, mỗi mục bắt đầu bằng [CẦN XÁC NHẬN]), "xong_khi" (tiêu chí nhìn là biết xong), '
    '"goi_y_den" (danh sách slug cộng sự nên nhận, chọn CHỈ từ danh sách cho sẵn, hợp chuyên môn nhất đứng đầu; có thể rỗng), '
    '"chuoi_goi_y" (slug các cộng sự nên làm tiếp SAU người nhận, theo thứ tự; thường rỗng). '
    "Quy tắc: tiếng Việt có dấu; chỉ dùng thông tin có trong cuộc chat, không bịa tên tệp, số liệu hay quyết định; mỗi việc tối đa 25 từ; "
    "tách việc theo từng chuyên môn (việc lập trình, đưa web lên mạng, thiết kế, viết nội dung, quảng cáo...) để anh chọn việc nào giao đi; "
    "việc nào cần anh quyết hay cần đăng, gửi, thanh toán thì ghi vào con_treo hoặc đánh dấu rõ là cần anh duyệt; không dùng dấu gạch dài."
)


def _bang_cong_su(ds: list) -> str:
    return "\n".join("- slug=%s | tên=%s | chức danh=%s | kỹ năng=%s" % (x["slug"], x["name"], x["role"] or "?", ", ".join(x["skills"]) or "?") for x in ds)


async def _hoi_ai(he_thong: str, cau_hoi: str, cho: int = 150) -> str:
    import tisa_quang_cao_ai as AI
    ask = getattr(AI, "_ASK", None)
    if ask is None:
        raise RuntimeError("AI chưa sẵn sàng")
    return await asyncio.wait_for(ask(he_thong, cau_hoi), cho)


def phieu_du_phong(tin: list, mid: str, tieu_de: str = "") -> dict:
    """AI chưa soạn được thì lập phiếu thô từ chính câu trả lời, để anh vẫn sửa tay và giao được."""
    cau = ""
    if mid:
        cau = next((_sach(t.get("content")) for t in tin if str(t.get("id")) == str(mid)), "")
    if not cau:
        cau = next((_sach(t.get("content")) for t in reversed(tin) if t.get("role") == "assistant"), "")
    return chuan_phieu({"tieu_de": tieu_de or "Bàn giao việc", "muc_tieu": "",
                        "viec": [{"text": cau[:400], "giao": True}], "xong_khi": ""})


def ap_goi_y(phieu: dict, d: dict, slugs: set) -> dict:
    gy = [s for s in (d.get("goi_y_den") or []) if isinstance(s, str) and s in slugs]
    ch = [s for s in (d.get("chuoi_goi_y") or []) if isinstance(s, str) and s in slugs and s not in gy[:1]]
    return {"phieu": phieu, "goi_y_den": gy[:3], "chuoi_goi_y": ch[:TOI_DA_BUOC_CHUOI]}


async def soan(m, sid: str, mid: str = "", brain: str = "brain") -> dict:
    ss = m.get_store()
    s = ss.get_session(sid)
    if not s:
        return {"ok": False, "loi": "Không thấy cuộc chat này."}
    tin = [t for t in ss.get_messages(sid) if t.get("role") in ("user", "assistant")]
    if not tin:
        return {"ok": False, "loi": "Cuộc chat chưa có nội dung để bàn giao."}
    tu_slug, tu_ten = nguon_cua_phien(m, sid)
    ds = danh_sach_cong_su(m, brain, tru=tu_slug)
    slugs = {x["slug"] for x in ds}
    tieu_de = str(s.get("title") or "").strip()
    ai_loi = ""
    try:
        raw = await _hoi_ai(_HE_THONG, "NGƯỜI BÀN GIAO: %s\n\nDANH SÁCH CỘNG SỰ CÓ THỂ NHẬN:\n%s\n\n%s\n\nHãy soạn phiếu bàn giao (JSON)." % (
            tu_ten, _bang_cong_su(ds), lich_su_de_soan(tin, mid)))
        d = tach_json(raw)
        if not d:
            raise ValueError("AI không trả JSON hợp lệ")
        phieu = chuan_phieu(d)
        if not phieu["viec"]:
            raise ValueError("phiếu không có việc nào")
        if not phieu["tieu_de"]:
            phieu["tieu_de"] = tieu_de or "Bàn giao việc"
        kq = ap_goi_y(phieu, d, slugs)
    except Exception as e:  # noqa: BLE001
        ai_loi = "%s: %s" % (type(e).__name__, str(e)[:120])
        print("[tisa_ban_giao] AI chưa soạn được phiếu: " + ai_loi, file=sys.stderr)
        kq = {"phieu": phieu_du_phong(tin, mid, tieu_de), "goi_y_den": [], "chuoi_goi_y": []}
    kq.update({"ok": True, "tu": {"slug": tu_slug, "name": tu_ten}, "ds": ds, "ai_loi": ai_loi})
    return kq


# ---------------------------------------------------------------- giao việc thật
def _ghi_tep(m, brain: str, rec: dict, phieu: dict) -> str:
    """Lưu phiếu thành tệp trong bộ não, trả đường dẫn tuyệt đối ('' nếu không ghi được)."""
    try:
        root = Path(m._brain_root(brain))
        thu_muc = root / THU_MUC_PHIEU / time.strftime("%Y-%m-%d")
        thu_muc.mkdir(parents=True, exist_ok=True)
        p = thu_muc / ("%s-%s.md" % (rec["id"], _ascii(phieu.get("tieu_de") or "ban-giao")))
        p.write_text(dung_markdown(rec, phieu), encoding="utf-8")
        return str(p)
    except OSError as e:
        print("[tisa_ban_giao] không ghi được tệp phiếu: %s" % e, file=sys.stderr)
        return ""


def _tao_viec(m, brain: str, den: str, tieu_de: str, loi_giao: str, xong_khi: str, nonce: str) -> tuple:
    """Một việc Kanban gắn mã cộng sự nhận (đúng đường nút Giao việc ở trang Cộng sự). Trả (task_id, session_id, tên)."""
    root = m._brain_key(brain)
    path = m._agent_md_path(root, den)
    if not path:
        raise ValueError("Không tìm thấy cộng sự nhận việc")
    key = m._agent_jobs_key(root, den, register=True)
    meta, _b = m._read_md(path)
    ten = str((meta or {}).get("name") or den)
    ss = m.get_store()
    sid = m.agent_jobs.report_session(key, den, m._brain_keys(brain), ss, m._resonance_store())
    if not sid:
        sid = ss.create_session(brain=brain, channel="agent:%s" % den, title=ten[:120])
    noi_dung = m.agent_jobs.brief(loi_giao, xong_khi, "task", None)
    tid = m.tasks_feature.enqueue(brain, m.agent_jobs.assign_title(ten, tieu_de), noi_dung, chat_id="web:%s" % sid,
                                  idempotency_key=m.agent_jobs.assign_key(key, den, nonce, "task", ""), dedupe_title=False)
    return tid, sid, ten


def _ten_cong_su(m, brain: str, slug: str) -> str:
    try:
        p = m._agent_md_path(m._brain_key(brain), slug)
        if p:
            meta, _b = m._read_md(p)
            return str((meta or {}).get("name") or slug)
    except Exception:  # noqa: BLE001
        pass
    return slug


def giao_sync(m, body: dict) -> dict:
    """Chạy trong thread: ghi tệp + tạo việc + lưu bản ghi chuỗi."""
    brain = _brain(body.get("brain"))
    den = str(body.get("den") or "").strip()
    phieu = chuan_phieu(body.get("phieu"))
    if not den:
        return {"ok": False, "loi": "Chưa chọn cộng sự nhận việc."}
    if not viec_duoc_giao(phieu):
        return {"ok": False, "loi": "Chưa tích việc nào để giao."}
    sid_nguon = str(body.get("sid") or "").strip()
    tu_slug, tu_ten = nguon_cua_phien(m, sid_nguon) if sid_nguon else (str(body.get("tu") or ""), "TISA BOT")
    if body.get("tu_ten"):
        tu_ten = _chuoi(body.get("tu_ten"), 80)
    if tu_slug and tu_slug == den:
        return {"ok": False, "loi": "Hãy chọn cộng sự khác để nhận việc."}
    chuoi = []
    for x in (body.get("chuoi") or []):
        sl = str(x.get("slug") if isinstance(x, dict) else x or "").strip()
        if sl and sl != den and not any(c["slug"] == sl for c in chuoi):
            chuoi.append({"slug": sl, "ten": _ten_cong_su(m, brain, sl)})
    chuoi = chuoi[:TOI_DA_BUOC_CHUOI]
    pid = uuid.uuid4().hex[:10]
    rec = {"id": pid, "tao_luc": time.time(), "tu": tu_slug, "tu_ten": tu_ten, "den": den, "den_ten": _ten_cong_su(m, brain, den),
           "sid_nguon": sid_nguon, "tieu_de": phieu["tieu_de"] or "Bàn giao việc", "chuoi": chuoi, "tu_chay": bool(body.get("tu_chay")),
           "cha": str(body.get("cha") or ""), "trang_thai": "dang_lam", "brain": brain}
    tep = _ghi_tep(m, brain, rec, phieu)
    rec["tep"] = tep
    loi_giao = dung_loi_giao(rec, phieu, tep)
    try:
        tid, sid_nhan, ten_nhan = _tao_viec(m, brain, den, rec["tieu_de"], loi_giao, phieu["xong_khi"], pid)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "loi": "Chưa giao được: %s" % (str(e)[:160] or type(e).__name__)}
    rec.update({"task_id": tid, "sid_nhan": sid_nhan, "den_ten": ten_nhan, "so_viec": len(viec_duoc_giao(phieu)), "phieu": phieu})
    _luu(rec)
    # Bản ghi cha (bước trước của chuỗi) đã bàn giao xong: gỡ bản nháp chờ duyệt.
    if rec["cha"]:
        cha = _lay(rec["cha"])
        if cha and cha.get("trang_thai") == "cho_duyet_tiep":
            cha["trang_thai"] = "da_ban_giao_tiep"
            cha.pop("ban_nhap", None)
            _luu(cha)
    return {"ok": True, "id": pid, "task_id": tid, "tep": tep, "den_ten": ten_nhan, "so_viec": rec["so_viec"], "session_nhan": sid_nhan}


async def bao_chat(m, sid: str, text: str, tieu_de: str = "") -> None:
    if not sid:
        return
    try:
        await asyncio.wait_for(m.push_to_chat(sid, text, viec={"kind": "task", "status": "giao", "title": tieu_de[:160]}), 8)
    except Exception as e:  # noqa: BLE001
        print("[tisa_ban_giao] không báo được vào chat: %s: %s" % (type(e).__name__, str(e)[:100]), file=sys.stderr)


# ---------------------------------------------------------------- chuỗi nối đuôi
_HE_THONG_TIEP = _HE_THONG.replace(
    "Một cộng sự vừa làm xong phần của mình và anh muốn giao phần việc tiếp theo cho cộng sự khác.",
    "Một cộng sự vừa XONG một bước trong chuỗi việc nối đuôi; phần việc tiếp theo thuộc cộng sự kế tiếp. Dựa vào KẾT QUẢ THẬT của bước vừa xong.")


async def soan_buoc_tiep(m, rec: dict, ket_qua: str) -> dict:
    """Phiếu cho bước kế của chuỗi, soạn từ phiếu trước + kết quả thật của bước vừa xong."""
    brain = _brain(rec.get("brain"))
    nxt = (rec.get("chuoi") or [{}])[0]
    ds = danh_sach_cong_su(m, brain)
    slugs = {x["slug"] for x in ds}
    ten_nhan = nxt.get("ten") or nxt.get("slug") or "?"
    cau = ("NGƯỜI BÀN GIAO: %s (vừa xong bước của mình)\nNGƯỜI NHẬN TIẾP THEO: %s (slug=%s)\n\nDANH SÁCH CỘNG SỰ:\n%s\n\n"
           "PHIẾU CỦA BƯỚC VỪA XONG:\n%s\n\nKẾT QUẢ BƯỚC VỪA XONG (câu trả lời cuối):\n%s\n\nHãy soạn phiếu bàn giao cho %s (JSON). "
           "Chỉ giữ những việc thuộc chuyên môn của người nhận tiếp theo, dùng đúng đường dẫn tệp có trong kết quả."
           % (rec.get("den_ten", ""), ten_nhan, nxt.get("slug"), _bang_cong_su(ds), dung_markdown(rec, rec.get("phieu") or {})[:5000],
              str(ket_qua or "")[:TOI_DA_KET_QUA] or "(không có nội dung)", ten_nhan))
    try:
        d = tach_json(await _hoi_ai(_HE_THONG_TIEP, cau))
        if not d:
            raise ValueError("AI không trả JSON hợp lệ")
        phieu = chuan_phieu(d)
        if not phieu["viec"]:
            raise ValueError("phiếu không có việc nào")
        if not phieu["tieu_de"]:
            phieu["tieu_de"] = "Tiếp theo: " + (rec.get("tieu_de") or "")
        return {"phieu": phieu, "ai_loi": ""}
    except Exception as e:  # noqa: BLE001
        print("[tisa_ban_giao] AI chưa soạn được phiếu bước tiếp: %s: %s" % (type(e).__name__, str(e)[:100]), file=sys.stderr)
        return {"phieu": chuan_phieu({"tieu_de": "Tiếp theo: " + (rec.get("tieu_de") or ""), "muc_tieu": rec.get("phieu", {}).get("muc_tieu", ""),
                                      "viec": [{"text": "Làm tiếp phần việc thuộc chuyên môn của bạn dựa trên kết quả bước trước: " + str(ket_qua or "")[:300], "giao": True}],
                                      "dau_vao": [rec.get("tep") or ""] if rec.get("tep") else []}), "ai_loi": "AI chưa soạn được, phiếu thô"}


def _ket_qua_viec(m, tk: dict, rec: dict) -> str:
    kq = str(tk.get("result") or "").strip()
    if kq:
        return kq
    try:
        ss = m.get_store()
        tin = [t for t in ss.get_messages(rec.get("sid_nhan")) if t.get("role") == "assistant"]
        return _sach(tin[-1].get("content")) if tin else ""
    except Exception:  # noqa: BLE001
        return ""


async def xu_ly_mot(m, rec: dict) -> bool:
    """Kiểm một bước đang chạy. Trả True nếu bản ghi đổi."""
    tk = await asyncio.to_thread(m.tasks_feature.store.get_task, rec.get("task_id"))
    if not tk:
        return False
    st = str(tk.get("status") or "")
    if st in ("done",):
        pass
    elif st in ("cancelled", "archived", "blocked"):
        if st == "blocked":
            return False        # chờ anh trả lời / cấp quyền: chưa phải lỗi, chuỗi vẫn chờ
        rec["trang_thai"] = "dung"
        _luu(rec)
        if rec.get("chuoi"):
            await bao_chat(m, rec.get("sid_nhan"), "Việc của %s đã bị hủy nên chuỗi bàn giao dừng ở đây, chưa chuyển cho %s." % (
                rec.get("den_ten", ""), (rec["chuoi"][0].get("ten") or "bước sau")), rec.get("tieu_de", ""))
        return True
    else:
        return False
    # đã xong
    rec["trang_thai"] = "xong"
    rec["xong_luc"] = time.time()
    chuoi = rec.get("chuoi") or []
    if not chuoi:
        _luu(rec)
        return True
    ket_qua = _ket_qua_viec(m, tk, rec)
    rec["ket_qua"] = ket_qua[:TOI_DA_KET_QUA]
    nxt = chuoi[0]
    if not rec.get("tu_chay"):
        _luu(rec)       # lưu trước: soạn bằng AI có thể lâu
    nhap = await soan_buoc_tiep(m, rec, ket_qua)
    if rec.get("tu_chay"):
        r = await asyncio.to_thread(giao_sync, m, {
            "brain": rec.get("brain"), "den": nxt["slug"], "phieu": nhap["phieu"], "chuoi": chuoi[1:], "tu_chay": True,
            "cha": rec["id"], "sid": "", "tu": rec.get("den"), "tu_ten": rec.get("den_ten")})
        if r.get("ok"):
            rec["trang_thai"] = "da_ban_giao_tiep"
            _luu(rec)
            await bao_chat(m, rec.get("sid_nhan"), "%s đã xong. Em đã tự chuyển tiếp cho %s (%d việc)." % (rec.get("den_ten", ""), r.get("den_ten", ""), r.get("so_viec", 0)), rec.get("tieu_de", ""))
            return True
    rec["trang_thai"] = "cho_duyet_tiep"
    rec["ban_nhap"] = {"phieu": nhap["phieu"], "den": nxt["slug"], "den_ten": nxt.get("ten") or nxt["slug"], "chuoi": chuoi[1:], "ai_loi": nhap.get("ai_loi", "")}
    _luu(rec)
    await bao_chat(m, rec.get("sid_nhan"), "%s đã xong việc được bàn giao. Em soạn sẵn phiếu chuyển tiếp cho %s, anh mở nút \"Phiếu bàn giao chờ anh\" để xem và giao." % (
        rec.get("den_ten", ""), nxt.get("ten") or nxt["slug"]), rec.get("tieu_de", ""))
    return True


async def vong_kiem_tra() -> None:
    await asyncio.sleep(40)
    while True:
        try:
            m = _m()
            if m is not None:
                with _khoa:
                    cho = [dict(r) for r in _doc().values() if r.get("trang_thai") == "dang_lam" and r.get("task_id")]
                for rec in cho:
                    try:
                        await xu_ly_mot(m, rec)
                    except Exception as e:  # noqa: BLE001
                        print("[tisa_ban_giao] kiểm bước lỗi: %s: %s" % (type(e).__name__, str(e)[:120]), file=sys.stderr)
        except Exception as e:  # noqa: BLE001
            print("[tisa_ban_giao] vòng kiểm lỗi: %s: %s" % (type(e).__name__, str(e)[:120]), file=sys.stderr)
        await asyncio.sleep(CHU_KY_VONG_S)


# ---------------------------------------------------------------- đường dẫn HTTP
def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "loi": msg}, status_code=ma)

    async def _json(request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return d if isinstance(d, dict) else {}

    @app.get("/tisa-ban-giao/cong-su")
    async def _cong_su(sid: str = "", brain: str = "brain"):
        m = _m()
        if m is None:
            return loi("Máy chủ chưa sẵn sàng.", 503)
        tu_slug, tu_ten = nguon_cua_phien(m, sid) if sid else ("", "TISA BOT")
        return {"ok": True, "tu": {"slug": tu_slug, "name": tu_ten}, "ds": danh_sach_cong_su(m, _brain(brain), tru=tu_slug)}

    @app.post("/tisa-ban-giao/soan")
    async def _soan(request: Request):
        m = _m()
        if m is None:
            return loi("Máy chủ chưa sẵn sàng.", 503)
        d = await _json(request)
        sid = str(d.get("sid") or "").strip()
        if not sid:
            return loi("Thiếu mã cuộc chat.")
        try:
            return JSONResponse(await soan(m, sid, str(d.get("mid") or ""), _brain(d.get("brain"))))
        except Exception as e:  # noqa: BLE001
            return loi("Chưa soạn được phiếu: %s" % (str(e)[:140] or type(e).__name__), 500)

    @app.post("/tisa-ban-giao/giao")
    async def _giao(request: Request):
        m = _m()
        if m is None:
            return loi("Máy chủ chưa sẵn sàng.", 503)
        d = await _json(request)
        r = await asyncio.to_thread(giao_sync, m, d)
        if not r.get("ok"):
            return JSONResponse(r, status_code=400)
        if d.get("sid"):
            tieu = (_lay(r["id"]) or {}).get("tieu_de", "")
            await bao_chat(m, str(d.get("sid")), "Đã bàn giao cho %s: %d việc.%s Phiếu: %s" % (
                r.get("den_ten", ""), r.get("so_viec", 0), " Xong sẽ báo anh và chuyển tiếp theo chuỗi." if d.get("chuoi") else "", r.get("tep") or "(chưa lưu được tệp)"), tieu)
        return JSONResponse(r)

    @app.get("/tisa-ban-giao/cho-duyet")
    async def _cho_duyet():
        with _khoa:
            out = []
            for r in _doc().values():
                if r.get("trang_thai") == "cho_duyet_tiep" and r.get("ban_nhap"):
                    out.append({"id": r["id"], "tu_ten": r.get("den_ten", ""), "tieu_de": r.get("tieu_de", ""), "ban_nhap": r["ban_nhap"],
                                "tu_chay": bool(r.get("tu_chay")), "brain": r.get("brain"), "sid_nhan": r.get("sid_nhan")})
        return {"ok": True, "ds": out}

    @app.post("/tisa-ban-giao/bo-qua")
    async def _bo_qua(request: Request):
        d = await _json(request)
        r = _lay(str(d.get("id") or ""))
        if not r:
            return loi("Không thấy phiếu.", 404)
        r["trang_thai"] = "dung"
        r.pop("ban_nhap", None)
        _luu(r)
        return {"ok": True}

    @app.get("/tisa-ban-giao/danh-sach")
    async def _ds(sid: str = ""):
        with _khoa:
            rs = sorted(_doc().values(), key=lambda r: -float(r.get("tao_luc") or 0))
        out = [{"id": r["id"], "tu_ten": r.get("tu_ten"), "den_ten": r.get("den_ten"), "tieu_de": r.get("tieu_de"), "trang_thai": r.get("trang_thai"),
                "so_viec": r.get("so_viec"), "chuoi": [c.get("ten") for c in (r.get("chuoi") or [])], "tep": r.get("tep")}
               for r in rs if not sid or r.get("sid_nguon") == sid]
        return {"ok": True, "ds": out[:30]}

    @app.on_event("startup")
    async def _bat_vong():
        if os.environ.get("TISA_BO_QUA_BAN_GIAO") == "1":
            return
        asyncio.get_running_loop().create_task(vong_kiem_tra())
