"""Hồ sơ của anh (V3.03, chủ yêu cầu 17/11/2026).

Vấn đề: mở một ô chat mới hay gọi điện cho bot thì bot không biết anh là ai, tên gì, nói tiếng Anh, hỏi "chào bạn, bạn cần gì".
Nguyên nhân: bộ nhớ chung `user_profile.md` (mọi ô chat đều nạp, memory_control.profile_block) vốn trống vì không có chỗ nào để anh điền, và cuộc gọi
điện (voice_live) hoàn toàn không đọc hồ sơ này.

Trang /tisa-ho-so/ cho anh khai: tên, cách bot gọi anh, cách bot xưng, ngôn ngữ, nghề và lĩnh vực, công việc hằng ngày, nguyên tắc, kèm nút
"Tự động điền từ Bộ Não Thứ 2" (AI đọc kho tri thức của anh rồi điền sẵn, anh xem lại và bấm Lưu).

Lưu: tisa-ho-so.json (nguyên bản) + một khối có đánh dấu ở ĐẦU user_profile.md (các dòng bot tự ghi thêm bên dưới được giữ nguyên).
Cuộc gọi: voice_live.make_provider gọi khoi_cho_goi_dien() để thêm hồ sơ vào lời dặn của bot (mọi nhà cung cấp Live).
"""
from __future__ import annotations

import json
import os
import re
import threading
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

TEP = STATE_DIR / "tisa-ho-so.json"
DAU = "<!-- TISA_HO_SO_START -->"
CUOI = "<!-- TISA_HO_SO_END -->"
_khoa = threading.RLock()

# (khoá, độ dài tối đa). Tổng khối hồ sơ phải gọn vì bộ nhớ chung chỉ có 4.000 ký tự.
TRUONG = (("ten", 80), ("goi_chu", 60), ("xung_bot", 40), ("ngon_ngu", 40), ("nghe_nghiep", 380), ("cong_viec", 520),
          ("nguyen_tac", 760), ("tom_tat_bo_nao", 900), ("bo_nao", 300))
MAC_DINH = {"ten": "", "goi_chu": "", "xung_bot": "em", "ngon_ngu": "tiếng Việt", "nghe_nghiep": "", "cong_viec": "", "nguyen_tac": "",
            "tom_tat_bo_nao": "", "bo_nao": "", "bat_buoc_bo_nao": True}


def _cat(s, n):
    t = re.sub(r"[ \t]+\n", "\n", str(s or "").strip())
    if len(t) <= n:
        return t
    c = t[:n]
    if "\n" in c:                   # danh sách nhiều dòng: bỏ dòng cuối bị cắt dở, không để câu đứt giữa chừng
        c = c[:c.rfind("\n")]
    return c.strip()


def doc() -> dict:
    d = dict(MAC_DINH)
    try:
        j = json.loads(TEP.read_text(encoding="utf-8"))
        if isinstance(j, dict):
            for k, n in TRUONG:
                if k in j:
                    d[k] = _cat(j[k], n)
            if "bat_buoc_bo_nao" in j:
                d["bat_buoc_bo_nao"] = bool(j["bat_buoc_bo_nao"])
    except (OSError, ValueError):
        pass
    return d


def _dong(s: str) -> str:
    return re.sub(r"\s*\n\s*", " · ", str(s or "").strip())


def khoi_van_ban(d: dict) -> str:
    """Khối chữ đưa vào lời dặn của bot (mọi ô chat, cuộc gọi, cộng sự). Rỗng khi anh chưa khai gì."""
    ten, goi, xung = _cat(d.get("ten"), 80), _cat(d.get("goi_chu"), 60), _cat(d.get("xung_bot"), 40) or "em"
    ngon = _cat(d.get("ngon_ngu"), 40) or "tiếng Việt"
    co = any(_cat(d.get(k), 9999) for k in ("ten", "goi_chu", "nghe_nghiep", "cong_viec", "nguyen_tac", "tom_tat_bo_nao", "bo_nao"))
    if not co:
        return ""
    L = [DAU, "# HỒ SƠ CỦA CHỦ (do chủ tự cài, ưu tiên cao nhất, áp dụng cho MỌI ô chat và MỌI cuộc gọi)"]
    if ten or goi:
        L.append("- Chủ là: %s. %sBot xưng là \"%s\"; luôn xưng gọi đúng như vậy ở MỌI ô chat, MỌI cộng sự và MỌI cuộc gọi, kể cả câu đầu tiên. KHÔNG dùng \"bạn\", \"tôi\", \"mình\" với chủ."
                 % (ten or goi, ("Gọi chủ là \"%s\". " % goi) if goi else "", xung))
    L.append("- Ngôn ngữ: luôn nói %s với chủ, kể cả khi nghe chữ hay âm thanh giống tiếng nước ngoài. Chủ đã được giới thiệu ngay đây nên KHÔNG chào kiểu \"chào bạn, bạn cần gì\" hay \"tôi nghe đây\", không hỏi chủ là ai; "
             "chủ chỉ chào hay nói \"alo\" thì đáp ngắn%s rồi chờ chủ nói." % (ngon, (" \"Dạ %s, %s nghe ạ\"" % (goi, xung)) if goi else ""))
    for nhan, k, n in (("Nghề, lĩnh vực", "nghe_nghiep", 380), ("Công việc hằng ngày", "cong_viec", 520), ("Nguyên tắc bắt buộc", "nguyen_tac", 760),
                       ("Tóm tắt từ Bộ Não Thứ 2", "tom_tat_bo_nao", 900)):
        v = _dong(_cat(d.get(k), n))
        if v:
            L.append("- %s: %s" % (nhan, v))
    bn = _cat(d.get("bo_nao"), 300)
    if bn and d.get("bat_buoc_bo_nao", True):
        L.append("- Bộ Não Thứ 2 (kho tri thức của chủ) nằm ở: %s. Việc liên quan tới chủ, công việc, khách, sản phẩm, giá, lịch: ĐỌC index.md rồi trang liên quan ở đó TRƯỚC khi trả lời (công cụ đọc tệp), không đoán; chưa đọc được hoặc thiếu thì nói thật." % bn)
    L.append(CUOI)
    return "\n".join(L)


def _ghi_khoi_vao_profile(khoi: str) -> None:
    import memory_control as MC
    hien = MC.read_profile()
    sach = re.sub(re.escape(DAU) + r".*?" + re.escape(CUOI) + r"\s*", "", hien, flags=re.S).strip()
    MC.write_profile((khoi + ("\n\n" + sach if sach else "")).strip() if khoi else sach)


def luu(d: dict) -> dict:
    ra = {}
    for k, n in TRUONG:
        ra[k] = _cat((d or {}).get(k), n)
    ra["xung_bot"] = ra["xung_bot"] or "em"
    ra["ngon_ngu"] = ra["ngon_ngu"] or "tiếng Việt"
    ra["bat_buoc_bo_nao"] = bool((d or {}).get("bat_buoc_bo_nao", True))
    with _khoa:
        TEP.parent.mkdir(parents=True, exist_ok=True)
        t = TEP.with_name(TEP.name + ".tmp")
        t.write_text(json.dumps(ra, ensure_ascii=False, indent=1), encoding="utf-8")
        t.replace(TEP)
        khoi = khoi_van_ban(ra)
        _ghi_khoi_vao_profile(khoi)
    return {"ho_so": ra, "khoi": khoi, "so_ky_tu": len(khoi)}


def khoi_cho_goi_dien() -> str:
    """Hồ sơ cho lời dặn của bot gọi điện (voice_live.make_provider). Đọc thẳng tệp của anh, không phụ thuộc bộ nhớ chung."""
    try:
        return khoi_van_ban(doc())
    except Exception:  # noqa: BLE001
        return ""


def khoi_cong_su() -> str:
    """Hồ sơ của chủ cho lời dặn của CỘNG SỰ (chat riêng, nhóm, việc Kanban, quy trình). Trước V3.09 lời dặn cộng sự cố ý không nối hồ sơ nên
    mở chat với cộng sự là bot không biết chủ là ai. Đọc thẳng tệp của anh, rỗng khi anh chưa khai gì."""
    try:
        k = khoi_van_ban(doc())
        if not k:
            return ""
        return "\n\n# === HỒ SƠ CỦA CHỦ (áp dụng cho mọi cộng sự, ưu tiên cao nhất về xưng hô và ngôn ngữ) ===\n" + k + "\n"
    except Exception:  # noqa: BLE001
        return ""


_RE_NGON_NGU_ANH = re.compile(r"(?:Detect the user's spoken language|The user selected recognition language)[^\n]*?do not infer a language switch from noise\.", re.S)
_RE_XUNG_HO_CU = re.compile(r"XƯNG HÔ theo đúng cách người dùng đang xưng hô với bạn[^.]*\.")


def ap_cho_cuoc_goi(system: str) -> str:
    """Lời dặn cuộc gọi (mọi nhà cung cấp Live và đường gọi Cơ bản): QUY TẮC xưng hô, ngôn ngữ, câu chào, cách đọc đặt Ở ĐẦU (mô hình coi trọng phần đầu), bỏ
    câu tiếng Anh "reply in that language" và câu "xưng hô theo cách người dùng xưng" vì chúng cãi lại hồ sơ, rồi hồ sơ đầy đủ ở cuối như cũ.
    Chủ chưa khai hồ sơ thì chỉ thêm quy tắc tiếng Việt mặc định (đã khai ngôn ngữ khác thì theo ngôn ngữ đó)."""
    system = str(system or "")
    try:
        d = doc()
        ngon = _cat(d.get("ngon_ngu"), 40) or "tiếng Việt"
        goi, xung = _cat(d.get("goi_chu"), 60), _cat(d.get("xung_bot"), 40) or "em"
        viet = "việt" in ngon.lower()
        L = ["# QUY TẮC CỐ ĐỊNH CỦA CUỘC GỌI (cao hơn mọi chỉ dẫn bên dưới, không bao giờ bỏ)",
             "1. Luôn nói %s. Âm thanh nghe giống tiếng Anh hay có tiếng ồn thì vẫn đáp %s; chỉ đổi ngôn ngữ khi chủ nói TRỌN một câu có nghĩa bằng ngôn ngữ khác hoặc bảo đổi." % (ngon, ngon)]
        if goi:
            L.append("2. Xưng \"%s\", gọi chủ là \"%s\", từ câu đầu tiên đến hết cuộc gọi. TUYỆT ĐỐI không dùng \"bạn\", \"tôi\", \"mình\" với chủ." % (xung, goi))
            L.append("3. Chủ chào hay nói \"alo\": đáp ngắn \"Dạ %s, %s nghe ạ\". Không nói \"chào bạn\", \"bạn cần gì\", \"tôi nghe đây\", không hỏi chủ là ai." % (goi, xung))
        L.append("%s. Khi được đưa một đoạn chữ để đọc cho chủ nghe: đọc đúng nguyên văn %s, không dịch sang ngôn ngữ khác, không thêm lời dẫn bằng tiếng Anh." % ("4" if goi else "2", ngon))
        if viet:
            system = _RE_NGON_NGU_ANH.sub("", system)
        if goi:
            system = _RE_XUNG_HO_CU.sub("XƯNG HÔ cố định theo quy tắc ở đầu lời dặn.", system)
        khoi = khoi_van_ban(d)
        return "\n".join(L) + "\n\n" + system.strip() + (("\n\n" + khoi) if khoi else "")
    except Exception:  # noqa: BLE001 - lỗi gì thì cuộc gọi vẫn chạy với lời dặn gốc
        return system


def mo_dau_cuoc_goi() -> list:
    """Hai lượt hội thoại đưa vào ĐẦU lịch sử cuộc gọi (ChatGPT Live initialItems). Lời dặn (prompt) mô hình có thể bỏ qua, còn lịch sử thì nó coi như
    chuyện đã xảy ra: chủ vừa tự giới thiệu và bot đã nhận lời. Đo thật 18/11/2026: có hồ sơ trong prompt mà bot vẫn hỏi \"anh/chị, anh tên gì\"."""
    try:
        d = doc()
        ten, goi, xung = _cat(d.get("ten"), 80), _cat(d.get("goi_chu"), 60), _cat(d.get("xung_bot"), 40) or "em"
        ngon = _cat(d.get("ngon_ngu"), 40) or "tiếng Việt"
        if not (ten or goi):
            return []
        goi = goi or ten
        nghe = re.split(r"(?<=[.!?])\s", _dong(_cat(d.get("nghe_nghiep"), 400)), maxsplit=1)[0].strip()
        if len(nghe) > 150:
            nghe = nghe[:150].rsplit(" ", 1)[0].rstrip(",;:(·- ")
        if nghe and nghe[-1] not in ".!?":
            nghe += "."
        ai = "Mình là %s.%s Từ giờ bạn gọi mình là \"%s\", xưng \"%s\" và luôn nói %s nhé." % (ten or goi, (" " + nghe) if nghe else "", goi, xung, ngon)
        tra = "Dạ %s, %s nhớ rồi ạ. %s sẽ luôn gọi %s, xưng \"%s\" và nói %s." % (goi, xung, xung.capitalize(), goi, xung, ngon)
        return [{"role": "user", "text": ai}, {"role": "assistant", "text": tra}]
    except Exception:  # noqa: BLE001
        return []


def lam_moi_khoi() -> None:
    """Dựng lại khối hồ sơ trong user_profile.md theo chữ MỚI NHẤT (khối đã lưu từ bản cũ vẫn mang câu chữ cũ cho tới lần anh bấm Lưu)."""
    try:
        if not TEP.exists():
            return
        with _khoa:
            khoi = khoi_van_ban(doc())
            if khoi:
                _ghi_khoi_vao_profile(khoi)
    except Exception:  # noqa: BLE001
        pass


# ---------------------------------------------------------------- tìm Bộ Não Thứ 2
def _la_bo_nao(p: Path) -> bool:
    try:
        return p.is_dir() and any((p / x).exists() for x in ("CLAUDE.md", "index.md", "wiki", "00-DOC-TRUOC.md", "MEMORY.md", "memory"))
    except OSError:
        return False


def ung_vien() -> list:
    """Các thư mục có vẻ là bộ não của anh: [{duong_dan, ten, nguon}]."""
    ra, thay = [], set()

    def them(p, nguon):
        try:
            p = Path(p).expanduser().resolve()
        except OSError:
            return
        if str(p) in thay or not _la_bo_nao(p):
            return
        thay.add(str(p))
        ra.append({"duong_dan": str(p), "ten": p.name, "nguon": nguon})
    home = Path.home()
    for nen in (home / "Desktop", home / "Documents", home / "OneDrive" / "Desktop", home / "Downloads"):
        try:
            for x in sorted(nen.iterdir()) if nen.is_dir() else []:
                n = x.name.lower()
                if "bộ não" in n or "bo nao" in n or "second brain" in n or n.startswith("brain"):
                    them(x, "Máy anh")
        except OSError:
            continue
    try:
        import tisa_quang_cao_bo_nao as B
        v = B.vault_mac_dinh()
        if v:
            them(v, "Bộ não đang mở trong TISA BOT")
    except Exception:  # noqa: BLE001
        pass
    return ra


# ---------------------------------------------------------------- đọc bộ não và nhờ AI điền
_TU_KHOA_CHU = ("chủ", "hồ sơ", "nguyên tắc", "xưng", "giọng", "tisa", "doanh nghiệp", "thương hiệu", "làm việc", "mục tiêu", "khách hàng", "sản phẩm")


def _doc_tep(p: Path, n: int) -> str:
    try:
        if p.stat().st_size > 400_000:
            return ""
        t = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    t = re.sub(r"\A---.*?\n---\s*", "", t, count=1, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()[:n]


def thu_thap(v: Path, toi_da: int = 24000) -> tuple:
    """(văn bản gom được, [đường dẫn tương đối đã đọc]). Chỉ ĐỌC."""
    khuc, da, dung = [], [], 0

    def them(rel: str, n: int):
        nonlocal dung
        p = v / rel
        if not p.is_file() or dung >= toi_da:
            return
        t = _doc_tep(p, min(n, toi_da - dung))
        if t:
            khuc.append("### %s\n%s" % (rel, t))
            da.append(rel)
            dung += len(t) + len(rel) + 8
    for rel, n in (("CLAUDE.md", 7000), ("00-DOC-TRUOC.md", 3000), ("index.md", 3500), ("wiki/overview.md", 3500), ("MEMORY.md", 3000)):
        them(rel, n)
    # trang nói về chủ, doanh nghiệp, nguyên tắc: chọn theo tên tệp
    ung = []
    for sub in ("01-ho-so", "wiki/entities", "wiki/concepts", "wiki/ban-do", "memory", "wiki"):
        d = v / sub
        if not d.is_dir():
            continue
        try:
            for f in d.rglob("*.md"):
                if len(f.relative_to(v).parts) > 4:
                    continue
                ten = f.stem.lower()
                diem = sum(1 for k in _TU_KHOA_CHU if k in ten)
                if diem or sub == "01-ho-so":
                    ung.append((diem + (2 if sub == "01-ho-so" else 0), str(f.relative_to(v))))
        except OSError:
            continue
    for _, rel in sorted(set(ung), key=lambda x: -x[0])[:9]:
        if rel not in da:
            them(rel, 2400)
    return "\n\n".join(khuc), da


_HE_THONG = ("Bạn đọc kho tri thức (\"Bộ Não Thứ 2\") của một chủ doanh nghiệp rồi điền HỒ SƠ để các trợ lý AI biết anh ấy là ai. "
             "Chỉ dùng thông tin CÓ trong tài liệu, không bịa; thiếu thông tin nào thì để chuỗi rỗng. Viết tiếng Việt, ngắn gọn, đúng sự thật. "
             "TUYỆT ĐỐI không đưa vào hồ sơ: số tài khoản ngân hàng, mật khẩu, khóa API, token, số điện thoại hay địa chỉ nhà riêng. "
             "Trả về DUY NHẤT một JSON, không giải thích.")


def _khung_json() -> str:
    return json.dumps({
        "ten": "tên đầy đủ của chủ, ví dụ Nguyễn Văn An",
        "goi_chu": "cách trợ lý gọi chủ theo đúng tài liệu (ví dụ anh An, sếp An); không có thì để rỗng",
        "xung_bot": "cách trợ lý xưng (ví dụ em); không có thì để rỗng",
        "nghe_nghiep": "nghề, lĩnh vực, doanh nghiệp, thương hiệu của chủ: 1 đến 3 câu",
        "cong_viec": "công việc cơ bản hằng ngày và các mảng chủ đang làm: 2 đến 5 gạch đầu dòng ngắn",
        "nguyen_tac": "các nguyên tắc làm việc, giọng văn, điều cấm mà trợ lý PHẢI theo (lấy đúng từ tài liệu): 3 đến 8 gạch đầu dòng ngắn",
        "tom_tat_bo_nao": "tóm tắt những sự thật quan trọng nhất trợ lý cần nhớ (sản phẩm, giá, lịch, khu vực, quy trình) trong tối đa 700 ký tự",
    }, ensure_ascii=False, indent=1)


def _tu_chu(v: Path, da: list, text: str) -> dict:
    """Không có AI: nhặt vài thứ chắc chắn từ chữ (dòng \"Chủ sở hữu:\", ngôn ngữ mặc định)."""
    ra = {}
    m = re.search(r"Chủ sở hữu[:\s*]+\**\s*([^—\-–\n(]+?)\s*(?:[—\-–]\s*([^\n]+))?\n", text)
    if m:
        ra["ten"] = m.group(1).strip(" *:")[:80]
        if m.group(2):
            ra["nghe_nghiep"] = m.group(2).strip(" *")[:380]
    return ra


async def tu_dong(duong_dan: str = "") -> dict:
    import asyncio
    c = ung_vien()
    v = Path(duong_dan).expanduser() if duong_dan else (Path(c[0]["duong_dan"]) if c else None)
    if not v or not v.is_dir():
        return {"ok": False, "loi": "Chưa tìm thấy thư mục Bộ Não Thứ 2. Anh dán đường dẫn thư mục vào ô \"Bộ Não Thứ 2 nằm ở đâu\" rồi bấm lại."}
    try:
        text, da = await asyncio.to_thread(thu_thap, v)
    except PermissionError:
        return {"ok": False, "loi": "TISA BOT chưa được phép đọc thư mục này (hệ điều hành chặn). Cấp quyền truy cập thư mục cho TISA BOT, hoặc chép bộ não vào nơi khác rồi thử lại."}
    if not text.strip():
        return {"ok": False, "loi": "Thư mục này chưa có tệp .md nào đọc được (cần CLAUDE.md, index.md hoặc thư mục wiki)."}
    ask = None
    try:
        import tisa_quang_cao_ai as A
        ask = A._ASK
    except Exception:  # noqa: BLE001
        ask = None
    truong, nguon, ghi = {}, "chu", ""
    if ask is not None:
        try:
            raw = await asyncio.wait_for(ask(_HE_THONG, "TÀI LIỆU TRONG BỘ NÃO:\n\n" + text + "\n\nTrả về JSON đúng khuôn (giữ đúng tên khoá):\n" + _khung_json()), 170)
            import tisa_quang_cao_ai as A2
            j = A2._json_tu_chu(raw)
            if isinstance(j, dict):
                truong = {k: _cat(j.get(k), n) for k, n in TRUONG if k in j and isinstance(j.get(k), str)}
                if isinstance(j.get("nguyen_tac"), list):
                    truong["nguyen_tac"] = _cat("\n".join("- " + str(x).lstrip("-• ") for x in j["nguyen_tac"]), 760)
                if isinstance(j.get("cong_viec"), list):
                    truong["cong_viec"] = _cat("\n".join("- " + str(x).lstrip("-• ") for x in j["cong_viec"]), 520)
                nguon = "ai"
        except Exception as e:  # noqa: BLE001
            ghi = "AI chưa trả lời được (%s) nên em chỉ điền được phần nhặt từ chữ." % str(e)[:100]
    if not truong:
        truong = _tu_chu(v, da, text)
        ghi = ghi or "Chưa nối được bộ não AI (đăng nhập Claude hoặc ChatGPT trong TISA BOT) nên chỉ điền được phần nhặt từ chữ."
    truong["bo_nao"] = str(v)
    return {"ok": True, "truong": truong, "da_doc": da, "nguon": nguon, "ghi_chu": ghi}


# ---------------------------------------------------------------- đường dẫn
def gan(app) -> None:
    from fastapi.responses import HTMLResponse, JSONResponse
    lam_moi_khoi()
    trang = Path(__file__).resolve().parent.parent / "dashboard" / "tisa-ho-so.html"

    @app.get("/tisa-ho-so/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang Hồ sơ", status_code=500)

    @app.get("/tisa-ho-so/api/ho-so")
    async def _doc():
        import asyncio
        d = doc()
        return JSONResponse({"ok": True, "ho_so": d, "khoi": khoi_van_ban(d), "ung_vien": await asyncio.to_thread(ung_vien)})

    @app.post("/tisa-ho-so/api/ho-so")
    async def _luu(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        try:
            return JSONResponse({"ok": True, **luu(d if isinstance(d, dict) else {})})
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Chưa lưu được: %s" % str(e)[:160]}, status_code=500)

    @app.post("/tisa-ho-so/api/tu-dong")
    async def _tu_dong(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        r = await tu_dong(str((d or {}).get("duong_dan") or ""))
        return JSONResponse(r if r.get("ok") else {**r, "error": r.get("loi")})
