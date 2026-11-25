"""tisa_quy_trinh_sua.py - Sửa RIÊNG MỘT bước của quy trình (chủ yêu cầu 23/11/2026).

Chuyện thật 23/11: ở trang Cộng sự, tab Quy trình ("Nghiên cứu nỗi đau đến đăng đa kênh", 5 bước), chủ nhắn "sửa lại phần thiết kế, tạo lại 10 ảnh
khác, không cần làm lại từ bước 1". Trước đây MỌI tin ở phiên quy trình đều thành một lần chạy mới từ bước 1 (workflow_chat.quyet_dinh_luot chỉ phân
biệt "nói về quy trình" và "đề bài"), nên cả 5 bước chạy lại: tốn thời gian, tốn token, mà câu góp ý còn bị nhồi vào {{input}} của bước nghiên cứu.

Nay có nhánh thứ ba: tin là GÓP Ý SỬA kết quả lần chạy trước (có động từ sửa/tạo lại/chỉnh và trỏ được tới một bước) thì chỉ chạy lại ĐÚNG bước đó,
một lượt của đúng cộng sự phụ trách, kèm kết quả lần trước và lời góp ý. Không trỏ được bước nào thì hỏi lại một câu (rẻ), không chạy gì.

Hàng rào nghiêng về phía RẺ, như workflow_chat: nhận nhầm một đề bài thành góp ý chỉ tốn một lượt chat và có dòng chỉ cách ép chạy cả quy trình
("chạy:" ở đầu tin, hoặc nút Chạy ở cột phải). Nhận nhầm góp ý thành lần chạy mới là 5 bước phí.

Phần nhận diện THUẦN (không I/O) để test thẳng: tools/test_quy_trinh_sua.py. Không dùng ký tự em dash.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional

TRAN_KQ_TRUOC = 8000
TRAN_KQ_BUOC_TRUOC = 5000


def _khong_dau(s: str) -> str:
    x = unicodedata.normalize("NFD", str(s or ""))
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return x.replace("đ", "d").replace("Đ", "D").lower()


# Động từ/cụm của một lời GÓP Ý SỬA (không có "chạy", "viết", "làm" trần: đó là động từ của một đề bài).
_SUA = re.compile(
    r"\b(?:chinh sua|sua lai|sua|chinh lai|chinh|doi|thay doi|thay|tao lai|lam lai|ve lai|viet lai|thiet ke lai|"
    r"bo cuc khac|chi can sua|chi can chinh|chi sua|chi chinh|khong can lam lai|dung chay lai|khong chay lai|giu nguyen)\b")
# "không cần làm lại từ bước 1", "đừng chạy lại cả quy trình": nhắc tới bước nhưng là để LOẠI nó ra.
_LOAI_RA = re.compile(r"\b(?:khong can|dung|khong|chu khong|khoi)\b[^.!?\n]{0,25}?\b(?:tu\s+)?(?:buoc|b)\s*\d+\b")
_TU_BUOC = re.compile(r"\btu\s+(?:buoc|b)\s*\d+\b")
_BUOC_SO = re.compile(r"\b(?:buoc|b)\s*0?(\d{1,2})\b")
# Từ chung chung, không dùng để nhận ra một bước.
_CHUNG = frozenset("""
cho anh em lai nhe di the nay de khong va cua duoc voi la bao tao sua chinh phan buoc agent can chi thoi hieu k nhu nhung mot cac
nhieu it hay sao bi qua rat chan khac moi cu cung da dang se thi ma neu thay doi lam viec ket qua bai bo hon dung roi nua lan
""".split())


def _tu(s: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9]+", _khong_dau(s)) if len(t) >= 3 and t not in _CHUNG]


def _ten_buoc(run_buoc: Optional[dict], meta_buoc: Optional[dict]) -> str:
    ten = str((run_buoc or {}).get("agent") or "").strip()
    return ten or str((meta_buoc or {}).get("agent") or "").strip()


def tim_buoc(msg: str, steps: List[dict], run_steps: Optional[List[dict]] = None) -> Optional[int]:
    """Chỉ số bước (từ 0) mà tin trỏ tới, hoặc None khi không chắc. Ưu tiên 'bước N' nói rõ, rồi tên cộng sự/nội dung bước."""
    n = len(steps)
    if not n:
        return None
    d = _khong_dau(msg)
    d = _LOAI_RA.sub(" ", d)
    d = _TU_BUOC.sub(" ", d)
    ms = [int(m) for m in _BUOC_SO.findall(d) if 1 <= int(m) <= n]
    if len(set(ms)) == 1:
        return ms[0] - 1
    if len(set(ms)) > 1:
        return None
    tu_tin = set(_tu(d))
    if not tu_tin:
        return None
    diem: List[int] = []
    for i in range(n):
        rb = (run_steps or [])[i] if run_steps and i < len(run_steps) else None
        ten = set(_tu(_ten_buoc(rb, steps[i])))
        viec = set(_tu(str(steps[i].get("task") or "")[:200]))
        diem.append(2 * len(tu_tin & ten) + len(tu_tin & viec - ten))
    cao = max(diem)
    if cao < 2 or diem.count(cao) != 1:
        return None
    return diem.index(cao)


def nhan_dien(msg: str, steps: List[dict], run_truoc: Optional[dict]) -> Optional[Dict[str, Any]]:
    """None = không phải góp ý sửa (chạy bình thường). {"kieu":"buoc","i":k,"run_id":...} = chỉ sửa bước k.
    {"kieu":"hoi","ds":[tên các bước]} = là góp ý sửa nhưng chưa rõ bước nào: hỏi lại, không chạy gì."""
    if not run_truoc or not steps:
        return None
    rs = run_truoc.get("steps") or []
    if not any(str((b or {}).get("output") or "").strip() for b in rs):
        return None          # lần trước chưa có kết quả nào để sửa: đây là đề bài mới
    d = _khong_dau(msg)
    if not _SUA.search(d):
        return None
    i = tim_buoc(msg, steps, rs)
    if i is not None:
        return {"kieu": "buoc", "i": i, "run_id": str(run_truoc.get("id") or "")}
    # Sửa nhưng không trỏ được bước: chỉ hỏi lại khi lời lẽ nói rõ là KHÔNG muốn chạy lại cả quy trình hoặc nhắc tới bước/kết quả cũ.
    if re.search(r"\b(?:khong can lam lai|dung chay lai|khong chay lai|chi can|chi sua|chi chinh|tu buoc|ket qua (?:vua|truoc)|ban (?:vua|truoc))\b", d):
        ds = []
        for k, b in enumerate(steps):
            rb = rs[k] if k < len(rs) else None
            ds.append(_ten_buoc(rb, b) or ("Bước %d" % (k + 1)))
        return {"kieu": "hoi", "ds": ds}
    return None


# Dấu hiệu một lời GÓP Ý về kết quả (không cần động từ sửa): "đẹp hơn", "ngắn lại", "chán quá", "sai rồi", "thiếu", "bị ảo"...
_GOP_Y = re.compile(r"\b(?:dep hon|ngan hon|dai qua|ngan lai|dai hon|chan|sai|thieu|thua|ao|chua (?:ok|on|dep|duoc|dung)|khong (?:dep|on|duoc|dung|hop)|"
                    r"qua (?:dai|ngan|nhieu|it|cu|chung chung)|nhieu hon|it hon|khac di|khac hon|them|bot|bo)\b")


def can_hoi_ai(msg: str, steps: List[dict], run_truoc: Optional[dict]) -> bool:
    """Có lần chạy trước để sửa, mà tin không rõ ràng là đề bài mới hay góp ý: tin ngắn, hoặc có dấu hiệu góp ý, hoặc có từ sửa mà chưa rõ bước."""
    if not run_truoc or not steps:
        return False
    if not any(str((b or {}).get("output") or "").strip() for b in (run_truoc.get("steps") or [])):
        return False
    d = _khong_dau(msg)
    return len(msg.strip()) < 70 or bool(_GOP_Y.search(d)) or bool(_SUA.search(d))


def _he_thong_phan_loai() -> str:
    return ("Em là bộ phân loại tin nhắn trong khung chat của MỘT QUY TRÌNH nhiều bước. Quy trình vừa chạy xong một lần và có kết quả từng bước. "
            "Chủ vừa nhắn thêm. Em quyết định: tin này là GÓP Ý/YÊU CẦU CHỈNH kết quả vừa làm (\"sua\"), hay là GIAO MỘT VIỆC MỚI độc lập (\"moi\").\n"
            "Là \"sua\" khi chủ nhận xét, chê, đòi đổi, bổ sung, làm lại MỘT PHẦN của kết quả vừa có (kể cả ngắn như \"ảnh đẹp hơn\", \"dài quá\", "
            "\"đổi bố cục khác\"), hoặc chỉ nói tên người/bước để trả lời câu hỏi chọn bước.\n"
            "Là \"moi\" khi chủ đưa một đề bài/chủ đề/việc mới, không nhằm vào kết quả vừa có (kể cả khi ngắn như \"viết bài về giá khóa học\").\n"
            "Nếu \"sua\": chọn \"buoc\" = số thứ tự bước (bắt đầu từ 1) làm ra phần bị góp ý (góp ý về ảnh thì bước thiết kế ảnh; về lời văn thì bước viết content...). "
            "Không chắc thì chọn bước phù hợp nhất, đừng bỏ trống.\n"
            "CHỈ trả đúng một dòng JSON: {\"y\":\"sua\"|\"moi\",\"buoc\":số hoặc null,\"lydo\":\"ngắn\"}")


def _cau_phan_loai(msg: str, steps: List[dict], run_truoc: dict) -> str:
    rs = run_truoc.get("steps") or []
    dong = ["CÁC BƯỚC CỦA QUY TRÌNH VÀ KẾT QUẢ LẦN TRƯỚC:"]
    for k, b in enumerate(steps):
        rb = rs[k] if k < len(rs) else None
        ten = _ten_buoc(rb, b) or ("Bước %d" % (k + 1))
        kq = " ".join(str((rb or {}).get("output") or "").split())[:160]
        dong.append("%d. %s | kết quả: %s" % (k + 1, ten, kq or "(trống)"))
    dong += ["", "TIN CỦA CHỦ:", msg.strip()[:1500], "", "Trả JSON một dòng như hướng dẫn."]
    return "\n".join(dong)


def doc_phan_loai(raw: str, steps: List[dict], run_truoc: dict) -> Optional[Dict[str, Any]]:
    """Đọc JSON AI trả. {"kieu":"buoc",...} khi sửa một bước hợp lệ; {"kieu":"moi"} khi là việc mới; None khi đọc không ra."""
    import json
    m = re.search(r"\{.*?\}", str(raw or ""), re.S)
    if not m:
        return None
    try:
        j = json.loads(m.group(0))
    except ValueError:
        return None
    y = str(j.get("y") or "").lower()
    if y == "moi":
        return {"kieu": "moi"}
    if y == "sua":
        try:
            b = int(j.get("buoc"))
        except (TypeError, ValueError):
            return None
        if 1 <= b <= len(steps):
            return {"kieu": "buoc", "i": b - 1, "run_id": str(run_truoc.get("id") or "")}
    return None


# ------------------------------------------------------------------ "Gửi/cho xem kết quả" KHÔNG phải góp ý sửa (24/11/2026)
# Chuyện thật 24/11: chạy xong, chủ nhắn "sao anh không thấy content", "gửi anh xem content", "gửi qua đây", "gửi đây". Cả bốn tin bị coi là GÓP Ý SỬA
# nên bốn lượt liền đều trả "Em hiểu anh muốn... Em làm thử MỘT mẫu nhé?", không lượt nào đưa nội dung. Yêu cầu xem/nhận lại thứ ĐÃ CÓ thì trả
# thẳng bản lưu của lần chạy trước, không cần hỏi lại, không tốn một lượt AI.
_OBJ_XEM = r"(?:content|noi dung|bai viet|bai dang|bai|ket qua|prompt|ban nhap|anh|hinh|link|file|video|kich ban|caption)"
_XEM_1 = re.compile(r"\b(?:gui|cho|dua|dan|hien|show|paste|in ra|chep|doc)\b.{0,30}?\b(?:xem|o day|qua day|tai day|day|trong chat|khung chat|nguyen van|day du|toan bo)\b")
_XEM_2 = re.compile(r"\b(?:khong|chua|k|ko)\s+(?:thay|xem duoc|doc duoc)\b.{0,30}?\b" + _OBJ_XEM + r"\b|\b" + _OBJ_XEM + r"\b.{0,20}?\b(?:khong|chua|k|ko)\s+(?:thay|xem duoc|doc duoc)\b")
_XEM_3 = re.compile(r"\b(?:xem|doc)\b.{0,15}?\b(?:lai\s+)?" + _OBJ_XEM + r"\b")
TRAN_XEM_BUOC = 9000
TRAN_XEM_TONG = 20000


def la_xem(msg: str) -> bool:
    """Tin này là đòi XEM/NHẬN LẠI kết quả đã có ("gửi qua đây", "sao anh không thấy content") chứ không phải góp ý sửa. Thuần chữ, không I/O."""
    d = re.sub(r"[^a-z0-9]+", " ", _khong_dau(msg)).strip()
    if not d or len(d) > 90:
        return False
    # "không thấy" là KHÔNG NHÌN THẤY, không phải động từ "thay" (đổi) của một góp ý sửa.
    if _SUA.search(re.sub(r"\b(?:khong|chua|k|ko)\s+thay\b", " ", d)):
        return False
    return bool(_XEM_1.search(d) or _XEM_2.search(d) or _XEM_3.search(d))


def tra_ket_qua(run: dict, steps: List[dict], i: Optional[int] = None) -> str:
    """Nguyên văn kết quả đã lưu của lần chạy trước: một bước (i) hoặc tất cả. Không dùng AI."""
    rs = (run or {}).get("steps") or []
    chon = [i] if i is not None and 0 <= i < len(steps) else list(range(len(steps)))
    khoi, tong, cat_luu = [], 0, False
    for k in chon:
        rb = rs[k] if k < len(rs) else None
        out = str((rb or {}).get("output") or "").strip()
        if not out:
            continue
        ten = _ten_buoc(rb, steps[k]) or ("Bước %d" % (k + 1))
        if len(out) > TRAN_XEM_BUOC:
            out = out[:TRAN_XEM_BUOC].rstrip() + "\n\n(…còn tiếp, em cắt bớt cho vừa khung chat)"
        elif len(out) == 4000:
            cat_luu = True            # bản lưu cũ cắt cứng ở 4000 chữ: nói thật là phần cuối có thể thiếu
        if tong + len(out) > TRAN_XEM_TONG and khoi:
            khoi.append("(Còn các bước sau, anh nói số bước nào em gửi tiếp.)")
            break
        tong += len(out)
        khoi.append("**Bước %d · %s**\n\n%s" % (k + 1, ten, out))
    if not khoi:
        return "Em chưa có kết quả nào của lần chạy trước để gửi. Anh bấm Chạy quy trình, xong em gửi ngay."
    dau = "Dạ, em gửi nguyên văn kết quả ngay tại đây:" if len(khoi) else ""
    cuoi = []
    if cat_luu:
        cuoi.append("Lưu ý: bản lưu của lần chạy này cắt ở 4.000 chữ nên phần cuối có thể thiếu. Từ lần chạy sau em lưu đủ.")
    if i is not None and len(steps) > 1:
        cuoi.append("Anh muốn xem bước khác thì nói số bước. Muốn sửa thì nói rõ đổi gì.")
    return dau + "\n\n" + "\n\n".join(khoi) + ("\n\n" + "\n".join(cuoi) if cuoi else "")


async def quyet_dinh(msg: str, steps: List[dict], run_truoc: Optional[dict], ask=None, cho_mau: Optional[dict] = None, cho: int = 45) -> Optional[Dict[str, Any]]:
    """Cửa chính: None = chạy bình thường (việc mới); {"kieu":"buoc"...} = chỉ sửa một bước; {"kieu":"hoi"...} = hỏi lại (chỉ khi AI không trả lời được).
    Rõ ràng thì quyết ngay không tốn AI; mơ hồ thì nhờ một lượt AI chỉ chữ đọc hiểu như người, để chủ không phải nhắn đúng cụm từ nào."""
    import asyncio
    d0 = _khong_dau(msg).strip()
    truc_tiep = bool(_LAM_LUON.search(d0)) or not _MUON_MAU.search(d0)   # V3.58: mặc định LÀM LUÔN, chỉ làm mẫu khi chủ đòi
    pha = str((cho_mau or {}).get("pha") or "mau")
    co_kq = bool(run_truoc) and any(str((b or {}).get("output") or "").strip() for b in ((run_truoc or {}).get("steps") or []))
    if co_kq and la_xem(msg):
        # (24/11) đòi xem/nhận lại kết quả đã có: trả bản lưu, không hỏi lại. Bước nào thì lấy theo lời chủ ("content" -> bước viết content), không rõ thì gửi hết.
        return {"kieu": "xem", "i": tim_buoc(msg, steps, (run_truoc or {}).get("steps")), "run_id": str((run_truoc or {}).get("id") or "")}
    if cho_mau and not _MUON_MAU.search(d0) and not _HUY.search(d0):
        # V3.58: còn một lần chờ duyệt dang dở từ kiểu cũ (hoặc chủ vừa nhắn thêm): KHÔNG hỏi lại nữa, làm trọn bước luôn.
        i_cho = int(cho_mau.get("i") or 0)
        j = tim_buoc(msg, steps, (run_truoc or {}).get("steps"))
        rid = str((run_truoc or {}).get("id") or "")
        if len(d0) <= 70 and _DONG_Y.search(d0) and not _SUA.search(d0):
            return {"kieu": "ap_dung", "i": i_cho, "run_id": rid}
        if len(d0) < 160 and (j == i_cho or (j is None and (_SUA.search(d0) or _GOP_Y.search(d0) or len(d0) <= 60))):
            return {"kieu": "buoc", "i": i_cho, "run_id": rid, "truc_tiep": True, "them": True}
    if cho_mau:       # đang chờ chủ xác nhận cách em hiểu (pha "hieu") hoặc chờ chủ xem mẫu (pha "mau"): tin này duyệt, hủy, hay góp ý thêm?
        if len(d0) <= 70 and _DONG_Y.search(d0) and not _SUA.search(d0):
            if pha == "mau" and _MUON_MAU.search(d0) and not _LAM_HET.search(d0):    # V3.58: "làm thử mẫu khác" là xin MẪU nữa, không phải ok
                return {"kieu": "mau", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or ""), "them": True}
            if pha == "hieu" and not _LAM_HET.search(d0):
                return {"kieu": "mau", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or "")}
            return {"kieu": "ap_dung", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or "")}
        if len(d0) <= 45 and _HUY.search(d0):
            return {"kieu": "huy", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or "")}
        n_gop = len(cho_mau.get("gop_y") or [])
        if pha == "hieu" and not _HUY.search(d0) and ((len(d0) <= 60 and not _SUA.search(d0) and not _GOP_Y.search(d0)) or n_gop >= 2):
            # (24/11) em đã hỏi rồi: câu trả lời ngắn (không phải góp ý mới hay lệnh hủy), hoặc đã qua 2 vòng hỏi, thì ĐI LÀM MẪU luôn, kèm câu đó vào
            # góp ý. Trước đây mọi câu không phải "ok" đều thành góp ý mới và em hỏi lại mãi. Câu trỏ sang một bước KHÁC thì để đường thường lo.
            j = tim_buoc(msg, steps, (run_truoc or {}).get("steps"))
            if j is None or j == int(cho_mau.get("i") or 0):
                return {"kieu": "mau", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or ""), "them": True}
    kq = nhan_dien(msg, steps, run_truoc)
    if kq and kq.get("kieu") == "buoc":
        if truc_tiep:
            kq["truc_tiep"] = True
        return _chuyen_pha(kq, cho_mau)
    if not can_hoi_ai(msg, steps, run_truoc):
        if cho_mau and len(d0) < 160:      # đang chờ mà chủ nhắn thêm yêu cầu ngắn: coi là góp ý tiếp cho đúng bước đó
            return _chuyen_pha({"kieu": "buoc", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or ""), "them": True, "truc_tiep": truc_tiep}, cho_mau)
        return None
    if ask is not None:
        try:
            raw = await asyncio.wait_for(ask(_he_thong_phan_loai(), _cau_phan_loai(msg, steps, run_truoc)), cho)
            r = doc_phan_loai(raw, steps, run_truoc)
            if r is not None:
                if r["kieu"] == "moi":
                    return None
                if truc_tiep:
                    r["truc_tiep"] = True
                return _chuyen_pha(r, cho_mau)
        except Exception:  # noqa: BLE001 - AI không sẵn sàng thì dùng kết luận sơ bộ
            pass
    if kq is None and cho_mau and len(d0) < 160:    # đang chờ mà AI không trả lời được: tin ngắn là góp ý tiếp cho đúng bước đó
        return _chuyen_pha({"kieu": "buoc", "i": int(cho_mau.get("i") or 0), "run_id": str((run_truoc or {}).get("id") or ""), "them": True, "truc_tiep": truc_tiep}, cho_mau)
    return kq


def cau_hoi_buoc(ds: List[str], ten_qt: str = "") -> str:
    dong = ["%d. %s" % (k + 1, t) for k, t in enumerate(ds)]
    cua = ' "%s"' % ten_qt if ten_qt else ""
    return ("Em chưa chạy lại quy trình" + cua + " vì tin này giống góp ý sửa kết quả vừa làm. Phần nào cần sửa ạ?\n\n"
            + "\n".join(dong)
            + "\n\nAnh nói tên bước hoặc nói rõ phần cần sửa, em chỉ chạy lại đúng bước đó. Nếu anh đang giao việc mới thì cứ nhắn việc đó rõ hơn một chút, em sẽ chạy cả quy trình.")


def soan_lenh(ten_qt: str, i: int, tong: int, task_goc: str, out_truoc: str, prev_truoc: str, gop_y: str) -> str:
    dong = ["[SỬA RIÊNG MỘT BƯỚC] Em đang làm lại CHỈ bước %d/%d của quy trình \"%s\". Các bước khác đã xong, KHÔNG làm lại và không đụng tới."
            % (i + 1, tong, ten_qt), "", "NHIỆM VỤ GỐC CỦA BƯỚC NÀY:", task_goc.strip() or "(không có)"]
    if prev_truoc.strip():
        dong += ["", "ĐẦU VÀO TỪ BƯỚC TRƯỚC (giữ nguyên, dùng làm nền):", prev_truoc.strip()[:TRAN_KQ_BUOC_TRUOC]]
    dong += ["", "KẾT QUẢ CỦA BƯỚC NÀY LẦN TRƯỚC:", (out_truoc.strip() or "(trống)")[:TRAN_KQ_TRUOC],
             "", "GÓP Ý CỦA CHỦ (làm đúng như vậy):", gop_y.strip(),
             "", "Chỉ sửa đúng phần chủ nêu, giữ nguyên phần còn lại. Trả về KẾT QUẢ ĐÃ SỬA của bước này (đầy đủ, dùng được ngay), "
                 "không giải thích dài.",
             "KHÔNG hỏi lại, KHÔNG xin duyệt, LÀM LUÔN. Nếu góp ý chưa nói rõ đổi gì (ví dụ chỉ nói \"sửa bước này\"), tự rà kết quả lần trước, "
             "sửa lỗi hoặc thiếu sót rõ nhất theo nhiệm vụ gốc, rồi nói một dòng đã đổi gì."]
    return "\n".join(dong)


def tin_xong(i: int, tong: int, agent: str, giay: int, ket_qua: str, con_lai: List[str]) -> str:
    than = str(ket_qua or "").strip() or "(bước sửa xong nhưng không có nội dung)"
    cuoi = ""
    if i + 1 < tong:
        cuoi = ("\n\nCác bước sau (%s) em chưa chạy lại. Anh muốn chạy tiếp thì nói \"chạy tiếp từ bước %d\" hoặc gửi \"chạy:\" kèm việc cần làm."
                % (", ".join(con_lai[:3]) + ("..." if len(con_lai) > 3 else ""), i + 2))
    return ("Đã sửa riêng bước %d/%d (%s) trong %d giây, không chạy lại các bước khác.\n\n%s%s\n\nKhi anh ưng ý, nhắn \"lưu lại quy trình\" để lần sau em làm đúng như vậy ngay từ đầu."
            % (i + 1, tong, agent, int(giay), than, cuoi))


async def sua_mot_buoc(deps: Dict[str, Any], run_truoc: dict, steps: List[dict], ten_qt: str, i: int, gop_y: str, emit) -> Dict[str, Any]:
    """Chạy đúng bước i bằng cộng sự của bước đó. `deps`: mk, agent_sysprompt, step_run, reasoning_kw, step_tools, loi_het_luot (hàm của main.py).
    Trả {"ok":bool,"text":str,"out":str,"agent":str}."""
    import time
    step = steps[i]
    rs = run_truoc.get("steps") or []
    agent_slug = str(step.get("agent") or "")
    agent_name, sysprompt, model, prov = deps["agent_sysprompt"](agent_slug, "workflow")
    rb = rs[i] if i < len(rs) else {}
    out_truoc = str((rb or {}).get("output") or "")
    task_goc = str((rb or {}).get("task") or step.get("task") or "")
    prev_truoc = str((rs[i - 1] or {}).get("output") or "") if i > 0 and i - 1 < len(rs) else ""
    prompt = soan_lenh(ten_qt, i, len(steps), task_goc, out_truoc, prev_truoc, gop_y)
    await emit({"type": "status", "content": "Chỉ sửa bước %d/%d: %s đang làm..." % (i + 1, len(steps), agent_name)})
    await emit({"type": "wf_event", "event": {"type": "step_start", "i": i, "agent": agent_name, "agent_slug": agent_slug, "task": "Sửa riêng bước này theo góp ý"}})
    t0 = time.time()
    out, loi_engine = "", ""
    async for ev in deps["step_run"](lambda: deps["mk"](sysprompt, model, prov, deps["step_tools"](step), **deps["reasoning_kw"](deps["agent_sysprompt"], agent_slug)), prompt):
        t = ev.get("type")
        if t == "final":
            out = ev.get("content") or out
        elif t == "error":
            loi_engine = ev.get("content") or loi_engine
    loi = deps["loi_het_luot"](out, loi_engine, prov, agent_name) or loi_engine
    giay = time.time() - t0
    if loi:
        await emit({"type": "wf_event", "event": {"type": "step_error", "i": i, "content": str(loi)}})
        return {"ok": False, "out": "", "agent": agent_name,
                "text": "Sửa bước %d (%s) không xong: %s\n\nKết quả cũ của bước vẫn còn nguyên." % (i + 1, agent_name, str(loi).strip()[:400])}
    await emit({"type": "wf_event", "event": {"type": "step_done", "i": i, "agent": agent_name, "output": out, "verified": None}})
    con_lai = []
    for k in range(i + 1, len(steps)):
        con_lai.append(str((rs[k] if k < len(rs) else {}).get("agent") or steps[k].get("agent") or "Bước %d" % (k + 1)))
    return {"ok": True, "out": out, "agent": agent_name, "text": tin_xong(i, len(steps), agent_name, giay, out, con_lai)}

# ------------------------------------------------------------------ Ghi nhớ bài học (chủ yêu cầu 23/11/2026)
# Chủ chỉnh quy trình qua các lần sửa riêng một bước; khi ưng ý nói "lưu lại quy trình, lần sau áp dụng theo" thì các góp ý được chắt thành
# BÀI HỌC NGẮN theo từng bước, lưu ở <thư mục quy trình>/.hoc/<slug>.json và tự nối vào nhiệm vụ của đúng bước ở MỌI lần chạy sau.
import json as _json
import os as _os
import time as _time
from pathlib import Path as _Path

TOI_DA_BAI_HOC_BUOC = 6
TOI_DA_CHU_BUOC = 1500
_LUU = re.compile(r"\b(?:luu lai|luu cai nay|ghi nho|nho lai|nho nhung|nho giup|cap nhat (?:cho )?lan sau|luu quy trinh|luu workflow)\b")
_LAN_SAU = re.compile(r"\b(?:lan sau|lan toi|sau nay|lan nua|ap dung|lam theo|nho|quy trinh|workflow)\b")


def la_lenh_luu(msg: str) -> bool:
    """Tin này là LỆNH LƯU bài học ("lưu lại quy trình lần sau áp dụng theo", "ghi nhớ những chỉnh sửa này")? Chỉ tin ngắn, có từ lưu/nhớ VÀ có ý lần sau/quy trình."""
    d = _khong_dau(msg)
    if len(d.strip()) > 260 or len(d.strip()) < 6:
        return False
    return bool(_LUU.search(d)) and bool(_LAN_SAU.search(d))


def _tep_hoc(thu_muc_qt, slug: str) -> "_Path":
    d = _Path(thu_muc_qt) / ".hoc"
    d.mkdir(parents=True, exist_ok=True)
    return d / (str(slug) + ".json")


def doc_hoc(thu_muc_qt, slug: str) -> Dict[str, Any]:
    try:
        d = _json.loads(_tep_hoc(thu_muc_qt, slug).read_text(encoding="utf-8"))
        if isinstance(d, dict):
            d.setdefault("nhap", []); d.setdefault("bai_hoc", {})
            return d
    except (OSError, ValueError):
        pass
    return {"nhap": [], "bai_hoc": {}}


def ghi_hoc(thu_muc_qt, slug: str, d: Dict[str, Any]) -> None:
    p = _tep_hoc(thu_muc_qt, slug)
    tam = p.with_suffix(".tmp")
    tam.write_text(_json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    _os.replace(str(tam), str(p))


def ghi_nhap(thu_muc_qt, slug: str, sid: str, i: int, agent: str, gop_y: str) -> None:
    """Ghi một góp ý vừa dùng để sửa bước i. Chưa phải bài học: chờ chủ nói "lưu lại"."""
    d = doc_hoc(thu_muc_qt, slug)
    d["nhap"].append({"sid": str(sid), "i": int(i), "agent": str(agent), "gop_y": str(gop_y).strip()[:800], "luc": int(_time.time())})
    d["nhap"] = d["nhap"][-40:]
    ghi_hoc(thu_muc_qt, slug, d)


def bai_hoc_buoc(thu_muc_qt, slug: str, i: int) -> str:
    """Khối chữ nối vào nhiệm vụ của bước i ở mỗi lần chạy. Rỗng khi chưa có bài học nào. Không bao giờ làm hỏng lần chạy."""
    try:
        ls = doc_hoc(thu_muc_qt, slug)["bai_hoc"].get(str(int(i) + 1)) or []
    except Exception:  # noqa: BLE001
        return ""
    ls = [str(x).strip() for x in ls if str(x).strip()][:TOI_DA_BAI_HOC_BUOC]
    if not ls:
        return ""
    return ("\n\nLƯU Ý CHỦ ĐÃ CHỈNH Ở CÁC LẦN CHẠY TRƯỚC (BẮT BUỘC ÁP DỤNG, ưu tiên hơn mặc định):\n"
            + "\n".join("- " + x for x in ls))[:TOI_DA_CHU_BUOC]


def _he_thong_chat_loc() -> str:
    return ("Em gộp các GÓP Ý CHỈNH SỬA của chủ thành BÀI HỌC NGẮN cho lần chạy sau của một quy trình nhiều bước. "
            "Mỗi bài học là MỘT câu mệnh lệnh cụ thể, dùng lại được cho lần chạy khác (không nhắc chuyện riêng của một lần chạy: tên khách, ngày, số liệu cụ thể). "
            "Gom theo số thứ tự bước (bắt đầu từ 1). Có BÀI HỌC ĐANG LƯU thì gộp chung với góp ý mới, bỏ trùng; hai ý mâu thuẫn thì theo góp ý MỚI. "
            "Mỗi bước tối đa %d bài học, mỗi bài tối đa 200 ký tự. Chỉ trả đúng một dòng JSON: {\"buoc\":{\"1\":[\"...\"],\"3\":[\"...\"]}}" % TOI_DA_BAI_HOC_BUOC)


def _doc_chat_loc(raw: str, so_buoc: int) -> Optional[Dict[str, List[str]]]:
    m = re.search(r"\{.*\}", str(raw or ""), re.S)
    if not m:
        return None
    try:
        j = _json.loads(m.group(0)).get("buoc")
    except (ValueError, AttributeError):
        return None
    if not isinstance(j, dict):
        return None
    ra: Dict[str, List[str]] = {}
    for k, v in j.items():
        try:
            n = int(k)
        except (TypeError, ValueError):
            continue
        if 1 <= n <= so_buoc and isinstance(v, list):
            ls = [" ".join(str(x).split())[:200] for x in v if str(x).strip()][:TOI_DA_BAI_HOC_BUOC]
            if ls:
                ra[str(n)] = ls
    return ra or None


def tin_luu_xong(ten_qt: str, bai_hoc: Dict[str, List[str]], steps: List[dict], rs: List[dict]) -> str:
    dong = ["Đã lưu bài học cho quy trình \"%s\". Từ lần chạy sau, em tự áp dụng đúng những điều anh đã chỉnh:" % ten_qt, ""]
    for n in sorted(bai_hoc, key=lambda x: int(x)):
        k = int(n) - 1
        ten = (str((rs[k] if k < len(rs) else {}).get("agent") or "") or str(steps[k].get("agent") or "")) if k < len(steps) else ""
        dong.append("Bước %s%s:" % (n, " (%s)" % ten if ten else ""))
        dong += ["- " + x for x in bai_hoc[n]]
        dong.append("")
    dong.append("Anh chỉnh thêm lần nào ưng ý, cứ nhắn \"lưu lại\" để em cập nhật tiếp. Bài học nằm ở thư mục quy trình, tệp .hoc, anh xóa tệp đó là quên hết.")
    return "\n".join(dong)


async def luu(thu_muc_qt, slug: str, sid: str, ten_qt: str, steps: List[dict], run_truoc: Optional[dict], ask=None, cho: int = 90) -> str:
    """Chốt các góp ý của cuộc chat này thành bài học theo bước và lưu. Trả tin báo cho chủ."""
    import asyncio
    d = doc_hoc(thu_muc_qt, slug)
    moi = [x for x in d["nhap"] if x.get("sid") == str(sid)]
    if not moi:
        return ("Em chưa thấy chỗ nào anh chỉnh sửa trong cuộc chat này để lưu cho lần sau. "
                "Anh góp ý sửa một bước trước, ưng ý rồi nhắn \"lưu lại\" nhé.")
    rs = (run_truoc or {}).get("steps") or []
    bai: Optional[Dict[str, List[str]]] = None
    if ask is not None:
        dong = ["CÁC BƯỚC:"] + ["%d. %s" % (k + 1, str((rs[k] if k < len(rs) else {}).get("agent") or b.get("agent") or "")) for k, b in enumerate(steps)]
        dong += ["", "BÀI HỌC ĐANG LƯU (JSON):", _json.dumps(d["bai_hoc"], ensure_ascii=False), "", "GÓP Ý MỚI CỦA CHỦ:"]
        dong += ["- Bước %d: %s" % (int(x.get("i") or 0) + 1, str(x.get("gop_y") or "")) for x in moi]
        try:
            raw = await asyncio.wait_for(ask(_he_thong_chat_loc(), "\n".join(dong)), cho)
            bai = _doc_chat_loc(raw, len(steps))
        except Exception:  # noqa: BLE001
            bai = None
    if bai is None:   # AI chưa sẵn sàng: lưu thẳng góp ý, mỗi bước giữ vài ý gần nhất, không mất công chủ chỉnh
        bai = {}
        for x in moi:
            n = str(int(x.get("i") or 0) + 1)
            bai.setdefault(n, []).append(" ".join(str(x.get("gop_y") or "").split())[:200])
        for n in list(bai):
            cu = d["bai_hoc"].get(n) or []
            bai[n] = (cu + bai[n])[-TOI_DA_BAI_HOC_BUOC:]
    d["bai_hoc"].update(bai)
    d["nhap"] = [x for x in d["nhap"] if x.get("sid") != str(sid)]
    d["luu_luc"] = int(_time.time())
    ghi_hoc(thu_muc_qt, slug, d)
    return tin_luu_xong(ten_qt, {n: d["bai_hoc"][n] for n in sorted(bai, key=int)}, steps, rs)

# ------------------------------------------------------------------ Hiểu lại và làm MẪU trước khi làm cả bước (chủ yêu cầu 23/11/2026)
# Trước: góp ý xong là chạy lại nguyên bước, chủ không biết AI hiểu đúng chưa, làm xong mới thấy sai thì mất thêm một lượt chờ.
# Nay: (1) nói lại em hiểu gì; (2) làm thử ĐÚNG MỘT mẫu; (3) chủ nói ok / làm hết thì mới làm trọn bước; chưa ưng thì góp ý thêm, làm mẫu lại.
# Muốn bỏ qua mẫu: "làm luôn", "khỏi làm thử".
_DONG_Y = re.compile(r"\b(?:ok|oke|okay|lam thu|thu di|duoc roi|dung roi|dung y|chuan|on roi|ung|duyet|dong y|lam di|lam het|lam toan bo|lam tat ca|ap dung|tiep tuc|"
                     r"chay di|cu the|lam theo mau|nhu vay|nhu mau|chot)\b")
_LAM_HET = re.compile(r"\b(?:lam het|lam toan bo|lam tat ca|lam luon|ap dung|chay het)\b")
_HUY = re.compile(r"\b(?:thoi|huy|bo qua|khong lam nua|dung lai|dung lam|khoi|cancel)\b")
_LAM_LUON = re.compile(r"\b(?:lam luon|khoi lam thu|khong can lam thu|dung lam thu|lam ngay|lam het luon|chay luon)\b")
# (V3.58, chủ báo 25/11) Mặc định "sửa bước N" là LÀM LUÔN. Trước đây mọi góp ý đều đi ba vòng: em nói "em hiểu anh muốn..." rồi chờ ok, làm thử một mẫu
# rồi chờ ok làm hết, rồi mới làm thật: chủ nhắn "sửa bước 4" mà bị hỏi tới hỏi lui. Giờ chỉ làm thử mẫu khi chủ TỰ đòi ("làm thử", "cho xem mẫu trước").
_MUON_MAU = re.compile(r"\b(?:lam thu|cho xem mau|xem mau truoc|xem thu|lam mau|thu mot (?:cai|mau|ban|anh|bai))\b")


def _chuyen_pha(r: Dict[str, Any], cho_mau: Optional[dict]) -> Dict[str, Any]:
    """Đang ở pha xem MẪU mà chủ góp ý thêm cho đúng bước đó: làm mẫu mới luôn (chủ đã xác nhận hướng rồi). Pha "hieu" thì em nói lại cách hiểu."""
    if cho_mau and str(cho_mau.get("pha") or "mau") == "mau" and r.get("kieu") == "buoc" and not r.get("truc_tiep") \
            and int(r.get("i", -1)) == int(cho_mau.get("i") or 0):
        r = dict(r)
        r["kieu"] = "mau"
        r["them"] = True
    return r


def _he_thong_hieu(agent: str) -> str:
    return ("Em là %s, cộng sự phụ trách MỘT bước của quy trình. Chủ vừa góp ý về kết quả bước em làm. Em CHƯA LÀM GÌ, chỉ trò chuyện để chốt cách hiểu. "
            "Trả lời ngắn gọn, tiếng Việt, xưng em gọi anh, đúng ba phần:\n"
            "1) \"Em hiểu anh muốn:\" rồi 2 đến 4 gạch đầu dòng: sẽ đổi gì, giữ nguyên gì.\n"
            "2) CHỈ khi THẬT SỰ thiếu thông tin quan trọng mới hỏi, tối đa 2 câu ngắn, kèm gợi ý lựa chọn nếu được. Không thiếu thì bỏ phần này.\n"
            "3) Kết đúng bằng: \"Em làm thử MỘT mẫu theo hướng này nhé? Anh nói ok, hoặc bổ sung thêm.\"\n"
            "KHÔNG dùng công cụ, KHÔNG tạo ảnh hay nội dung kết quả, KHÔNG dài dòng." % (agent or "cộng sự"))


async def hieu(ask, ten_qt: str, steps: List[dict], run_truoc: dict, i: int, gop_y: List[str], cho: int = 70) -> str:
    """Trả lời NGAY (một lượt chỉ chữ, không công cụ): em hiểu gì + câu hỏi nếu cần. AI chưa sẵn sàng thì dùng mẫu câu từ chính lời chủ."""
    import asyncio
    rs = run_truoc.get("steps") or []
    rb = rs[i] if i < len(rs) else {}
    agent = _ten_buoc(rb, steps[i]) or ("Bước %d" % (i + 1))
    if ask is not None:
        cau = ["QUY TRÌNH: %s | BƯỚC %d/%d: %s" % (ten_qt, i + 1, len(steps), agent),
               "NHIỆM VỤ GỐC CỦA BƯỚC: " + " ".join(str((rb or {}).get("task") or steps[i].get("task") or "").split())[:400],
               "KẾT QUẢ LẦN TRƯỚC (tóm tắt): " + (" ".join(str((rb or {}).get("output") or "").split())[:500] or "(trống)"),
               "", "GÓP Ý CỦA CHỦ (theo thứ tự, ý sau thắng ý trước):"] + ["%d) %s" % (k + 1, x.strip()) for k, x in enumerate(gop_y)]
        try:
            txt = str(await asyncio.wait_for(ask(_he_thong_hieu(agent), "\n".join(cau)), cho) or "").strip()
            if txt:
                return txt
        except Exception:  # noqa: BLE001
            pass
    cuoi = " ".join(gop_y[-1].split())[:400]
    return ("Em hiểu anh muốn sửa bước %d (%s) theo góp ý:\n- \"%s\"\n\nEm làm thử MỘT mẫu theo hướng này nhé? Anh nói ok, hoặc bổ sung thêm." % (i + 1, agent, cuoi))


def doc_cho(thu_muc_qt, slug: str, sid: str) -> Optional[dict]:
    try:
        c = (doc_hoc(thu_muc_qt, slug).get("cho") or {}).get(str(sid))
        return c if isinstance(c, dict) and c.get("gop_y") else None
    except Exception:  # noqa: BLE001
        return None


def dat_cho(thu_muc_qt, slug: str, sid: str, i: int, gop_y: List[str], mau: str, pha: str = "mau") -> None:
    d = doc_hoc(thu_muc_qt, slug)
    cho = d.setdefault("cho", {})
    cho[str(sid)] = {"pha": pha, "i": int(i), "gop_y": [str(x).strip()[:800] for x in gop_y][-8:], "mau": str(mau)[:6000], "luc": int(_time.time())}
    for k in sorted(cho, key=lambda x: cho[x].get("luc", 0))[:-10]:
        cho.pop(k, None)
    ghi_hoc(thu_muc_qt, slug, d)


def xoa_cho(thu_muc_qt, slug: str, sid: str) -> None:
    d = doc_hoc(thu_muc_qt, slug)
    if (d.get("cho") or {}).pop(str(sid), None) is not None:
        ghi_hoc(thu_muc_qt, slug, d)


def soan_lenh_mau(ten_qt: str, i: int, tong: int, task_goc: str, out_truoc: str, prev_truoc: str, gop_y: List[str]) -> str:
    dong = ["[LÀM THỬ MỘT MẪU] Em chỉ làm MẪU cho bước %d/%d của quy trình \"%s\", CHƯA làm cả bước. Các bước khác không đụng tới." % (i + 1, tong, ten_qt), "",
            "NHIỆM VỤ GỐC CỦA BƯỚC NÀY:", task_goc.strip() or "(không có)"]
    if prev_truoc.strip():
        dong += ["", "ĐẦU VÀO TỪ BƯỚC TRƯỚC (giữ nguyên):", prev_truoc.strip()[:TRAN_KQ_BUOC_TRUOC]]
    dong += ["", "KẾT QUẢ LẦN TRƯỚC CỦA BƯỚC NÀY:", (out_truoc.strip() or "(trống)")[:TRAN_KQ_TRUOC], "", "GÓP Ý CỦA CHỦ (theo thứ tự, ý sau thắng ý trước nếu mâu thuẫn):"]
    dong += ["%d) %s" % (k + 1, x.strip()) for k, x in enumerate(gop_y)]
    dong += ["", "Trả lời đúng hai phần, theo đúng thứ tự:",
             "EM HIỂU: 2 đến 4 gạch đầu dòng ngắn, nói rõ em sẽ đổi gì so với lần trước, giữ nguyên gì (để chủ xác nhận em hiểu đúng).",
             "MẪU: làm ĐÚNG MỘT mẫu đại diện theo góp ý. Nếu bước này tạo nhiều mục (nhiều ảnh, nhiều bài, nhiều biến thể) thì chỉ làm MỘT mục thật hoàn chỉnh "
             "(ảnh thì tạo thật một ảnh và nêu đường dẫn/hiển thị được). Nếu bước chỉ ra một khối nội dung thì viết bản rút gọn của phần dễ thấy sự khác biệt nhất. "
             "KHÔNG làm cả bộ."]
    return "\n".join(dong)


def tin_mau(i: int, tong: int, agent: str, giay: int, ket_qua: str, lan: int) -> str:
    than = str(ket_qua or "").strip() or "(chưa có nội dung)"
    return ("Em chưa làm cả bước, mới làm thử một mẫu cho bước %d/%d (%s), mất %d giây%s.\n\n%s\n\n"
            "Anh xem mẫu: ưng thì nói \"ok, làm hết\" em làm trọn bước theo đúng hướng này. Chưa ưng thì anh nói chỗ cần sửa, em làm lại mẫu."
            % (i + 1, tong, agent, int(giay), (" (lần chỉnh thứ %d)" % lan) if lan > 1 else "", than))


async def lam_mau(deps: Dict[str, Any], run_truoc: dict, steps: List[dict], ten_qt: str, i: int, gop_y: List[str], emit) -> Dict[str, Any]:
    """Một lượt của cộng sự bước i: nói em hiểu gì + làm MỘT mẫu. Không ghi đè kết quả bước."""
    import time
    step = steps[i]
    rs = run_truoc.get("steps") or []
    agent_slug = str(step.get("agent") or "")
    agent_name, sysprompt, model, prov = deps["agent_sysprompt"](agent_slug, "workflow")
    rb = rs[i] if i < len(rs) else {}
    prompt = soan_lenh_mau(ten_qt, i, len(steps), str((rb or {}).get("task") or step.get("task") or ""), str((rb or {}).get("output") or ""),
                           str((rs[i - 1] or {}).get("output") or "") if i > 0 and i - 1 < len(rs) else "", gop_y)
    await emit({"type": "status", "content": "Em đang hiểu lại góp ý và làm thử MỘT mẫu cho bước %d/%d: %s..." % (i + 1, len(steps), agent_name)})
    t0 = time.time()
    out, loi_engine = "", ""
    async for ev in deps["step_run"](lambda: deps["mk"](sysprompt, model, prov, deps["step_tools"](step), **deps["reasoning_kw"](deps["agent_sysprompt"], agent_slug)), prompt):
        t = ev.get("type")
        if t == "final":
            out = ev.get("content") or out
        elif t == "error":
            loi_engine = ev.get("content") or loi_engine
    loi = deps["loi_het_luot"](out, loi_engine, prov, agent_name) or loi_engine
    if loi:
        return {"ok": False, "out": "", "agent": agent_name, "text": "Làm thử mẫu cho bước %d (%s) không xong: %s\n\nChưa đổi gì, kết quả cũ vẫn còn." % (i + 1, agent_name, str(loi).strip()[:400])}
    return {"ok": True, "out": out, "agent": agent_name, "text": tin_mau(i, len(steps), agent_name, time.time() - t0, out, len(gop_y))}


def gop_y_ap_dung(gop_y: List[str], mau: str) -> str:
    dong = ["Các góp ý của chủ (ý sau thắng ý trước nếu mâu thuẫn):"] + ["%d) %s" % (k + 1, x.strip()) for k, x in enumerate(gop_y)]
    if str(mau).strip():
        dong += ["", "MẪU CHỦ ĐÃ XEM VÀ ĐỒNG Ý (làm đúng hướng này cho TOÀN BỘ bước, làm đủ số lượng như nhiệm vụ gốc):", str(mau).strip()[:3000]]
    return "\n".join(dong)

