"""tisa_quang_cao_ai.py - phần "Tạo bài quảng cáo bằng AI" và "bài đã đăng" của trang Quảng Cáo (V2.78).

Làm được gì:
  - TANG: 5 tầng phễu marketing (Nhận biết, Quan tâm, Cân nhắc, Chuyển đổi, Giữ chân và giới thiệu), mỗi tầng có mục tiêu,
    công thức viết, nút kêu gọi gợi ý. Chọn tầng nào thì AI viết đúng tầng đó.
  - viet_noi_dung: nhờ bộ não AI của TISA BOT (một lượt chỉ chữ, không công cụ, không MCP) viết 1 đến 3 phương án quảng cáo:
    chữ, nhiều tấm ảnh (carousel) hoặc kịch bản video theo từng cảnh. Có sửa lại theo yêu cầu.
  - tao_anh: tạo ảnh quảng cáo bằng gói ChatGPT đang đăng nhập trong TISA BOT (image_gen.py), sửa ảnh theo yêu cầu.
  - dung_video: dựng video ngắn từ các ảnh cảnh (chuyển động nhẹ, phụ đề) bằng ffmpeg trên máy, không cần khoá API.
  - ho_so: danh sách Fanpage / kênh / website đã nhập, lần sau chỉ chọn.
  - phan_tich_link: nhận link bài đã đăng (Facebook, TikTok, YouTube), báo loại bài và mã bài để chạy đúng bài đó.
Mọi thứ ở đây chỉ SOẠN. Không đăng, không bật quảng cáo, không tiêu tiền quảng cáo.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.parse
from pathlib import Path

import tisa_quang_cao as Q
import tisa_quang_cao_thiet_lap as T

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

TEP_HO_SO = Q.KHO / "ho-so.json"
_khoa = threading.RLock()
_ASK = None           # async def ask(he_thong: str, cau_hoi: str) -> str, do main.py gắn vào (một lượt chỉ chữ, không công cụ)


def wire(*, ask) -> None:
    global _ASK
    _ASK = ask


# ---------------------------------------------------------------- 5 tầng phễu
TANG = [
    {"id": 1, "ten": "Nhận biết", "ngan": "Người lạ chưa biết anh", "khach": "Khách lạnh",
     "muc_tieu": "Làm họ dừng lại, nhớ tên và thấy mình có vấn đề cần giải quyết. Chưa bán.",
     "viet": "Mở đầu thật mạnh trong 3 giây đầu. Kể chuyện, nêu một nỗi đau quen thuộc hoặc một điều bất ngờ. Không nêu giá, không ép mua.",
     "cong_thuc": "Hook, Story, Offer nhẹ; hoặc PAS (Vấn đề, Khuấy sâu, Giải pháp)", "cta": "Xem thêm", "loai_goi_y": "video",
     "muc_tieu_qc": ["nhan_dien", "xem_video"]},
    {"id": 2, "ten": "Quan tâm", "ngan": "Họ biết vấn đề, đang tìm hiểu", "khach": "Khách nguội",
     "muc_tieu": "Cho họ thấy anh hiểu vấn đề và biết cách giải. Tạo lý do để theo dõi, bấm xem.",
     "viet": "Cho giá trị thật: một mẹo, một kiến thức, một cách làm nhanh. Gợi mở giải pháp của anh ở cuối, không chốt.",
     "cong_thuc": "AIDA (Chú ý, Quan tâm, Mong muốn, Hành động); mẹo 3 bước", "cta": "Xem thêm", "loai_goi_y": "anh_nhieu",
     "muc_tieu_qc": ["tuong_tac", "truy_cap", "xem_video"]},
    {"id": 3, "ten": "Cân nhắc", "ngan": "Đang so sánh với chỗ khác", "khach": "Khách ấm",
     "muc_tieu": "Giúp họ tin và dễ quyết định: chứng minh anh đáng chọn, trả lời nỗi lo.",
     "viet": "Bằng chứng, khách nói gì, trước và sau, câu hỏi thường gặp, so sánh công bằng. Mỗi ý có thật, không thổi phồng.",
     "cong_thuc": "FAB (Tính năng, Lợi thế, Lợi ích); BAB (Trước, Sau, Cầu nối); lời khách hàng", "cta": "Gửi tin nhắn", "loai_goi_y": "anh_nhieu",
     "muc_tieu_qc": ["tin_nhan", "khach"]},
    {"id": 4, "ten": "Chuyển đổi", "ngan": "Sẵn sàng mua, cần một cú hích", "khach": "Khách nóng",
     "muc_tieu": "Chốt: một lời đề nghị rõ ràng, dễ làm theo ngay, có lý do hành động bây giờ.",
     "viet": "Nêu rõ cái họ nhận được, vì sao nên làm hôm nay, cách làm trong một bước. Chỉ nêu giá, ưu đãi, hạn chót nếu anh đã cung cấp.",
     "cong_thuc": "4U (Gấp, Độc đáo, Hữu ích, Cụ thể); đề nghị cộng bảo chứng", "cta": "Mua ngay", "loai_goi_y": "anh_1",
     "muc_tieu_qc": ["ban_hang", "khach", "tin_nhan"]},
    {"id": 5, "ten": "Giữ chân và giới thiệu", "ngan": "Khách đã mua", "khach": "Khách cũ",
     "muc_tieu": "Cảm ơn, giúp họ dùng tốt hơn, bán thêm hoặc nhờ giới thiệu bạn bè.",
     "viet": "Giọng thân thiết. Hướng dẫn dùng, mẹo hay, quà tri ân, lời mời giới thiệu. Không dùng giọng bán hàng cứng.",
     "cong_thuc": "Cảm ơn, Giá trị thêm, Lời mời; chương trình giới thiệu", "cta": "Liên hệ chúng tôi", "loai_goi_y": "anh_1",
     "muc_tieu_qc": ["ban_hang", "tuong_tac"]},
]
GIONG = ["Thân thiện, gần gũi", "Chuyên gia, đáng tin", "Sôi nổi, trẻ trung", "Sang trọng, tinh tế", "Hài hước, duyên dáng", "Ấm áp, chân thành"]
PHONG_CACH_ANH = ["Chân thực như chụp thật", "Tối giản, nền sạch", "Màu sắc nổi bật, bắt mắt", "Cao cấp, ánh sáng đẹp", "Minh hoạ hiện đại", "Đời thường, như người dùng tự chụp"]

# Giới hạn chữ nên theo từng nền tảng (để quảng cáo không bị cắt)
GIOI_HAN = {
    "facebook": "Nội dung chính: 2 dòng đầu thật cuốn vì người xem chỉ thấy khoảng 125 ký tự trước khi bấm Xem thêm. Tiêu đề tối đa 40 ký tự.",
    "tiktok": "Lời dẫn tối đa khoảng 100 ký tự, giọng nói chuyện như người thật, mở đầu bằng một câu gây tò mò. Video dọc 9:16.",
    "google": "Tìm kiếm: mỗi tiêu đề tối đa 30 ký tự, mỗi mô tả tối đa 90 ký tự, ghi 8 đến 15 tiêu đề và 3 đến 4 mô tả khác nhau để Google tự ghép.",
}

_HE_THONG = (
    "Bạn là chuyên gia viết quảng cáo (copywriter) và đạo diễn sáng tạo tiếng Việt cho doanh nghiệp nhỏ. Bạn viết đúng tầng phễu marketing "
    "được yêu cầu, bằng tiếng Việt tự nhiên, dễ hiểu, câu ngắn, không sáo rỗng.\n"
    "LUẬT BẮT BUỘC:\n"
    "- Chỉ dùng thông tin người dùng cung cấp. KHÔNG bịa giá, ưu đãi, số liệu, giải thưởng, giấy tờ, cam kết. Chỗ nào thiếu thì viết đặt chỗ trong ngoặc vuông, ví dụ [giá], để người dùng điền.\n"
    "- Không dùng từ tuyệt đối khó chứng minh (số 1, tốt nhất, duy nhất, cam kết 100%). Không hứa lợi nhuận, không nói về sức khoẻ hay tài chính cá nhân kiểu hứa hẹn.\n"
    "- Không nói về đặc điểm cá nhân của người xem (kiểu \"bạn đang bị...\", \"bạn nợ nần...\"). Nói về tình huống, không gán cho người đọc.\n"
    "- Mỗi phương án dùng một góc khác nhau, không viết lại cùng một ý.\n"
    "- Chỉ trả về MỘT khối JSON hợp lệ, không giải thích, không dùng ký hiệu markdown."
)


def tang_cong_khai() -> dict:
    return {"tang": TANG, "giong": GIONG, "phong_cach_anh": PHONG_CACH_ANH, "gioi_han": GIOI_HAN}


def _cat(s, n):
    return str(s or "").strip()[:n]


def _bo_nao_cho(d: dict, sp: str, toi_da: int = 6000) -> dict:
    """Đọc bộ não theo sản phẩm anh nhập (và tên trang đang quảng cáo). Lỗi đọc thì coi như bộ não trống, không chặn việc viết."""
    try:
        import tisa_quang_cao_bo_nao as B
        hs = d.get("ho_so") if isinstance(d.get("ho_so"), dict) else {}
        return B.doc_bo_nao("%s %s %s" % (sp, hs.get("ten") or "", d.get("khac_biet") or ""), toi_da)
    except Exception:  # noqa: BLE001
        return {"text": "", "da_doc": [], "thieu": [], "co": False}


def _json_tu_chu(raw: str):
    """Lấy khối JSON đầu tiên trong câu trả lời (model đôi khi bọc trong ```json)."""
    t = str(raw or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I)
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j <= i:
        raise ValueError("AI không trả về dữ liệu đọc được. Thử bấm tạo lại.")
    return json.loads(t[i:j + 1])


def _giay_canh(v) -> str:
    """"5", "5s", "0-5" (khoảng giây), "3-8" đều ra số giây của cảnh."""
    t = str(v or "").lower().replace(",", ".")
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", t)
    if m:
        n = max(float(m.group(2)) - float(m.group(1)), 2.0)
    else:
        m = re.search(r"(\d+(?:\.\d+)?)", t)
        n = float(m.group(1)) if m else 4.0
    return str(int(round(max(2.0, min(20.0, n)))))


def _lam_sach_pa(p: dict, kieu: str, so_tam: int) -> dict:
    ds = lambda v, n, m: [_cat(x, n) for x in (v or []) if _cat(x, n)][:m] if isinstance(v, list) else []
    out = {"ten": _cat(p.get("ten"), 80), "cong_thuc": _cat(p.get("cong_thuc"), 60), "tieu_de": _cat(p.get("tieu_de"), 200), "noi_dung": _cat(p.get("noi_dung"), 2500),
           "cta": _cat(p.get("cta"), 40), "hashtag": ds(p.get("hashtag"), 40, 8), "tieu_de_phu": ds(p.get("tieu_de_phu"), 60, 15), "mo_ta_ngan": ds(p.get("mo_ta_ngan"), 120, 4),
           "mo_ta_anh": _cat(p.get("mo_ta_anh"), 900), "chu_tren_anh": _cat(p.get("chu_tren_anh"), 80), "slides": [], "canh": []}
    for s in (p.get("slides") or [])[:max(so_tam, 1)]:
        if isinstance(s, dict):
            out["slides"].append({"tieu_de": _cat(s.get("tieu_de"), 80), "mo_ta": _cat(s.get("mo_ta"), 300), "mo_ta_anh": _cat(s.get("mo_ta_anh"), 700), "chu_tren_anh": _cat(s.get("chu_tren_anh"), 70)})
    for i, c in enumerate((p.get("canh") or [])[:12], 1):
        gs = _giay_canh(c.get("giay") if isinstance(c, dict) else "")
        if isinstance(c, dict):
            out["canh"].append({"stt": i, "giay": gs, "hinh": _cat(c.get("hinh"), 400), "loi": _cat(c.get("loi"), 400), "chu": _cat(c.get("chu"), 90), "mo_ta_anh": _cat(c.get("mo_ta_anh"), 700)})
    return out


def so_giay(v, mac_dinh: int = 30) -> int:
    """Độ dài video anh chọn hoặc tự nhập, ép trong 5 đến 180 giây."""
    try:
        n = int(float(str(v).replace(",", ".")))
    except (TypeError, ValueError):
        n = mac_dinh
    return max(5, min(180, n))


def so_canh(do_dai: int) -> int:
    """Khoảng 5 đến 6 giây mỗi cảnh, tối thiểu 3 và tối đa 12 cảnh."""
    return max(3, min(12, round(do_dai / 6)))


def _khung_json(kieu: str, so_tam: int, do_dai: int) -> str:
    chung = '"ten": "tên ngắn của góc viết", "cong_thuc": "công thức đã dùng", "tieu_de": "tiêu đề", "noi_dung": "nội dung chính hoàn chỉnh, xuống dòng bằng \\n", "cta": "nút kêu gọi", "hashtag": ["..."]'
    if kieu == "anh_1":
        return '{"phuong_an": [{' + chung + ', "mo_ta_anh": "mô tả chi tiết bức ảnh quảng cáo cần tạo: chủ thể, bối cảnh, ánh sáng, bố cục, cảm xúc", "chu_tren_anh": "câu rất ngắn in trên ảnh, tối đa 8 từ"}]}'
    if kieu == "anh_nhieu":
        return ('{"phuong_an": [{' + chung + ', "slides": [{"tieu_de": "tiêu đề tấm", "mo_ta": "chữ mô tả tấm", "mo_ta_anh": "mô tả chi tiết ảnh của tấm này", "chu_tren_anh": "chữ ngắn in trên ảnh"}]'
                + ' (đúng %d tấm, tấm đầu gây chú ý, tấm cuối kêu gọi hành động)}]}' % so_tam)
    if kieu == "video":
        return ('{"phuong_an": [{' + chung + ', "canh": [{"giay": "số giây của cảnh này, chỉ viết số, ví dụ 5", "hinh": "cảnh quay, góc máy, hành động", "loi": "lời thoại hoặc lời dẫn", "chu": "chữ hiện trên màn hình", "mo_ta_anh": "mô tả ảnh minh hoạ của cảnh (dọc 9:16)"}]'
                + ' (video đúng khoảng %d giây, chia %d cảnh, cộng số giây các cảnh gần bằng %d, cảnh đầu là hook 3 giây, cảnh cuối kêu gọi hành động)}]}' % (do_dai, so_canh(do_dai), do_dai))
    return '{"phuong_an": [{' + chung + ', "tieu_de_phu": ["tiêu đề phụ (dùng cho Google)"], "mo_ta_ngan": ["mô tả ngắn (dùng cho Google)"]}]}'


async def viet_noi_dung(d: dict) -> dict:
    if _ASK is None:
        raise ValueError("Chưa nối được bộ não AI của TISA BOT. Đăng nhập Claude hoặc ChatGPT trong TISA BOT rồi thử lại.")
    nen = _cat(d.get("nen"), 12)
    if nen not in Q.NEN:
        raise ValueError("Chọn nền tảng.")
    tang = next((t for t in TANG if t["id"] == int(d.get("tang") or 3)), TANG[2])
    kieu = _cat(d.get("kieu"), 12)
    if kieu not in ("chu", "anh_1", "anh_nhieu", "video"):
        kieu = "chu"
    so_tam = max(2, min(10, int(d.get("so_tam") or 3)))
    do_dai = so_giay(d.get("do_dai"))
    so_pa = max(1, min(3, int(d.get("so_phuong_an") or 2)))
    sp = _cat(d.get("san_pham"), 1500)
    if len(sp) < 8:
        raise ValueError("Anh mô tả sản phẩm hoặc dịch vụ trước (ít nhất một câu) để AI viết đúng.")
    dong = ["TẦNG PHỄU: %d. %s (%s)" % (tang["id"], tang["ten"], tang["khach"]), "Mục tiêu của tầng: " + tang["muc_tieu"], "Cách viết: " + tang["viet"], "Công thức nên dùng: " + tang["cong_thuc"],
            "Nền tảng: %s. %s" % (Q.NEN[nen], GIOI_HAN[nen]), "Nút kêu gọi gợi ý: " + (_cat(d.get("cta"), 40) or tang["cta"]), "", "SẢN PHẨM, DỊCH VỤ: " + sp]
    for nhan, k in (("Giá, ưu đãi (chỉ dùng nếu có ghi ở đây)", "gia"), ("Điểm khác biệt", "khac_biet"), ("Khách hàng mục tiêu", "khach"), ("Giọng văn", "giong")):
        if _cat(d.get(k), 500):
            dong.append("%s: %s" % (nhan, _cat(d.get(k), 500)))
    bn = _bo_nao_cho(d, sp)
    if bn["text"]:
        dong += ["", "KIẾN THỨC CỦA DOANH NGHIỆP LẤY TỪ BỘ NÃO (đây là sự thật về sản phẩm, giọng thương hiệu và quy tắc. Viết ĐÚNG theo đây, không trái, không bịa thêm ngoài đây và phần anh nhập):", bn["text"]]
    hs = d.get("ho_so") if isinstance(d.get("ho_so"), dict) else {}
    if hs.get("ten"):
        dong.append("Thương hiệu, trang: %s%s" % (_cat(hs.get("ten"), 80), (". Giọng thương hiệu: " + _cat(hs.get("giong_van"), 300)) if hs.get("giong_van") else ""))
    dong += ["", "YÊU CẦU: viết %d phương án khác nhau, loại quảng cáo: %s." % (so_pa, {"chu": "chỉ chữ", "anh_1": "ảnh 1 tấm", "anh_nhieu": "ảnh nhiều tấm (%d tấm)" % so_tam, "video": "video %d giây" % do_dai}[kieu]),
             "Trả về JSON đúng khuôn sau (giữ đúng tên khoá):", _khung_json(kieu, so_tam, do_dai)]
    cu = d.get("noi_dung_cu") if isinstance(d.get("noi_dung_cu"), dict) else None
    sua = _cat(d.get("yeu_cau_sua"), 600)
    if cu and sua:
        dong = dong[:-3] + ["", "BẢN HIỆN TẠI (JSON): " + json.dumps(cu, ensure_ascii=False)[:5000], "YÊU CẦU SỬA CỦA NGƯỜI DÙNG: " + sua,
                            "Hãy viết lại ĐÚNG MỘT phương án theo yêu cầu sửa, giữ những phần người dùng không nhắc tới. Trả về JSON khuôn sau:", _khung_json(kieu, so_tam, do_dai)]
        so_pa = 1
    try:
        raw = await asyncio.wait_for(_ASK(_HE_THONG, "\n".join(dong)), 170)
    except asyncio.TimeoutError:
        raise ValueError("AI trả lời quá lâu. Thử lại, hoặc rút ngắn mô tả.")
    except Exception as e:  # noqa: BLE001
        raise ValueError("Bộ não AI chưa trả lời được (%s). Kiểm tra TISA BOT đã đăng nhập Claude hoặc ChatGPT chưa." % str(e)[:120])
    try:
        j = _json_tu_chu(raw)
    except ValueError as e:
        raise ValueError(str(e))
    ds = [_lam_sach_pa(p, kieu, so_tam) for p in (j.get("phuong_an") or []) if isinstance(p, dict)][:so_pa]
    if not ds or not any(p["noi_dung"] or p["slides"] or p["canh"] for p in ds):
        raise ValueError("AI chưa viết được nội dung. Thử bấm tạo lại.")
    for p in ds:
        p["cta"] = p["cta"] or tang["cta"]
    return {"ok": True, "phuong_an": ds, "tang": tang["id"], "kieu": kieu, "bo_nao": {"da_doc": bn["da_doc"], "thieu": bn["thieu"], "co": bn["co"]}}


# ---------------------------------------------------------------- ảnh và video
def _luu_tep_tu_file(nguon: Path, loai: str, ten: str) -> dict:
    ext = nguon.suffix.lower() or (".png" if loai == "anh" else ".mp4")
    tid = "tl-" + hashlib.sha1(("%s%s" % (ten, time.time())).encode()).hexdigest()[:10]
    T.THU_MUC_TAI.mkdir(parents=True, exist_ok=True)
    dich = T.THU_MUC_TAI / (tid + ext)
    shutil.copyfile(nguon, dich)
    try:
        os.chmod(dich, 0o600)
    except OSError:
        pass
    t = {"id": tid, "loai": loai, "ten": ten, "kich_thuoc": dich.stat().st_size, "duong_dan": str(dich), "luc": int(time.time())}
    with T._khoa:
        ds = T._doc_tai()
        ds.append(t)
        Q._ghi(T.TEP_TAI, ds[-300:])
    return T.tep_cong_khai(t)


class LoiAnh(ValueError):
    """Tạo ảnh không được; giao_viec=True khi có thể nhờ cộng sự thiết kế làm thay."""
    def __init__(self, msg: str, giao_viec: bool = False):
        super().__init__(msg)
        self.giao_viec = giao_viec


# Ảnh tham chiếu anh tải lên, theo vai: AI NHÌN THẤY ảnh thật rồi dựng theo, không đoán từ lời tả.
VAI_THAM_CHIEU = [
    ("nhan_vat", "NHÂN VẬT", "Người trong ảnh quảng cáo phải GIỐNG HỆT người ở ảnh này: giữ khuôn mặt, kiểu tóc, màu da, dáng người. Không đổi thành người khác."),
    ("logo", "LOGO", "Đặt đúng logo này vào một góc ảnh (nhỏ gọn, không che chủ thể), giữ NGUYÊN hình dạng, màu sắc và chữ của logo, không vẽ lại, không méo, không thêm logo nào khác."),
    ("san_pham", "SẢN PHẨM", "Sản phẩm trong ảnh quảng cáo phải GIỐNG HỆT sản phẩm ở ảnh này: giữ đúng hình dáng, màu sắc, bao bì, chữ in trên sản phẩm. Không bịa thêm chi tiết."),
]
MAX_THAM_CHIEU = 4


def tham_chieu_theo_vai(d: dict) -> list:
    """[(vai, nhãn, mô tả, tệp)] theo thứ tự nhân vật, logo, sản phẩm. Tệp không còn thì bỏ qua."""
    tc = d.get("tham_chieu") if isinstance(d.get("tham_chieu"), dict) else {}
    ra = []
    for khoa, nhan, mo_ta in VAI_THAM_CHIEU:
        for tid in (tc.get(khoa) or [])[:MAX_THAM_CHIEU]:
            t = T.tim_tep(_cat(tid, 20))
            if t and t["loai"] == "anh":
                ra.append((khoa, nhan, mo_ta, t))
    return ra


def _lenh_anh(d: dict, tang: dict, refs: list = (), co_anh_sua: bool = False, bo_nao: str = "") -> str:
    mo_ta = _cat(d.get("mo_ta_anh"), 1000)
    chu = _cat(d.get("chu_tren_anh"), 80)
    chi_dao = _cat(d.get("chi_dao"), 1800)
    if chi_dao:
        p = ["Tạo MỘT ảnh quảng cáo chất lượng cao cho mạng xã hội, tầng phễu \"%s\" (%s)." % (tang["ten"], tang["khach"]),
             "CHỈ ĐẠO HÌNH ẢNH TỪ NHÀ THIẾT KẾ CỦA DOANH NGHIỆP (làm đúng theo): " + chi_dao]
    else:
        p = ["Tạo MỘT ảnh quảng cáo chất lượng cao cho mạng xã hội, đúng tầng phễu \"%s\" (%s)." % (tang["ten"], tang["khach"]), "Nội dung ảnh: " + mo_ta]
    if _cat(d.get("san_pham"), 400):
        p.append("Sản phẩm, dịch vụ: " + _cat(d.get("san_pham"), 400))
    if bo_nao and not chi_dao:
        p.append("Thông tin ĐÚNG về doanh nghiệp và sản phẩm (lấy từ bộ não, chỉ để hiểu đúng, KHÔNG in thành chữ lên ảnh): " + bo_nao[:900].replace("\n", " "))
    if _cat(d.get("phong_cach"), 80):
        p.append("Phong cách: " + _cat(d.get("phong_cach"), 80))
    if refs:
        n0 = 2 if co_anh_sua else 1
        p.append("Có kèm các ảnh tham chiếu thật, hãy NHÌN và dựng theo:")
        for k, (khoa, nhan, mo, t) in enumerate(refs):
            p.append("- Ảnh số %d là %s. %s" % (n0 + k, nhan, mo))
    if d.get("chen_chu") and chu:
        p.append("Chèn đúng câu chữ này lên ảnh, bằng tiếng Việt có dấu đúng chính tả, chữ lớn, rõ, dễ đọc, đặt ở vùng trống: \"%s\". Không thêm chữ nào khác." % chu)
    else:
        p.append("Không chèn chữ lên ảnh." + ("" if any(r[0] == "logo" for r in refs) else " Không logo, không hình mờ."))
    p.append("Bố cục có chỗ trống cho chữ quảng cáo, ánh sáng đẹp, không méo mặt hay tay, không dùng logo thương hiệu khác ngoài logo được cung cấp.")
    return "\n".join(p)


async def tao_anh(d: dict) -> dict:
    import image_gen
    tang = next((t for t in TANG if t["id"] == int(d.get("tang") or 3)), TANG[2])
    if not _cat(d.get("mo_ta_anh"), 10) and not _cat(d.get("yeu_cau_sua"), 10) and not _cat(d.get("chi_dao"), 10):
        raise ValueError("Thiếu mô tả ảnh.")
    ty_le = d.get("ty_le") if d.get("ty_le") in ("square", "portrait", "landscape") else "square"
    chat = d.get("chat_luong") if d.get("chat_luong") in ("low", "medium", "high") else "medium"
    refs = tham_chieu_theo_vai(d)
    mau = T.tim_tep(_cat(d.get("anh_mau"), 20)) if d.get("anh_mau") else None
    if len(refs) + (1 if mau else 0) > image_gen.MAX_REF_IMAGES:
        raise ValueError("Mỗi lượt tạo ảnh nhận tối đa %d ảnh (kể cả ảnh đang sửa). Anh bớt ảnh tham chiếu giúp em." % image_gen.MAX_REF_IMAGES)
    bn = _bo_nao_cho(d, _cat(d.get("san_pham"), 600), 900) if not _cat(d.get("chi_dao"), 10) else {"text": ""}
    prompt = _lenh_anh(d, tang, refs, bool(mau), bn["text"])
    vault = image_gen._resolve_vault(None)
    adir = image_gen._attachments_dir(vault)
    anh_gui = []

    def chep(t: dict, nhan: str) -> str:
        # image_gen chỉ đọc ảnh nằm trong bộ não: chép vào thư mục attachments, dùng xong để lại như mọi ảnh AI.
        cp = adir / ("qc-%s-%s%s" % (nhan, t["id"], Path(t["duong_dan"]).suffix))
        shutil.copyfile(t["duong_dan"], cp)
        return os.path.relpath(cp, vault).replace(os.sep, "/")

    if mau:
        anh_gui.append(chep(mau, "mau"))
        prompt = "SỬA ẢNH ĐÃ CÓ (ảnh số 1) theo yêu cầu, giữ nguyên chủ thể và bố cục nếu không được nhắc tới.\nYêu cầu sửa: " + _cat(d.get("yeu_cau_sua"), 600) + "\n\n" + prompt
    for khoa, nhan, mo, t in refs:
        anh_gui.append(chep(t, khoa))
    res = await image_gen.generate_chatgpt(prompt, ty_le, chat, vault_root=None, images=anh_gui)
    if not res.get("ok"):
        loi = str(res.get("error") or "Tạo ảnh chưa được.")
        chua_noi = "ChatGPT" in loi and ("OAuth" in loi or "account" in loi or "tài khoản" in loi or "Chưa kết nối" in loi)
        if chua_noi:
            loi = "Chưa tạo được ảnh vì TISA BOT chưa đăng nhập ChatGPT. Vào Cài đặt, Mô hình, đăng nhập ChatGPT rồi bấm tạo lại. Hoặc bấm Giao cộng sự thiết kế làm ảnh này, hoặc tải ảnh có sẵn lên."
        raise LoiAnh(loi, giao_viec=True)
    t = await asyncio.to_thread(_luu_tep_tu_file, Path(res["abs_path"]), "anh", "AI-" + Path(res["abs_path"]).name)
    return {"ok": True, "tep": t, "so_anh_tham_chieu": len(refs)}


def trang_thai_ai() -> dict:
    anh = False
    try:
        import image_gen
        import openai_oauth
        anh = bool(openai_oauth.status().get("connected")) and bool(image_gen._image_account_order())
    except Exception:  # noqa: BLE001
        pass
    bn = _bo_nao_cho({}, "", 3000)
    return {"chu": _ASK is not None, "anh": anh, "video": bool(shutil.which("ffmpeg") and shutil.which("ffprobe")),
            "bo_nao": {"co": bn["co"], "thieu": bn["thieu"]}}


_FONTS = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf", "C:\\Windows\\Fonts\\arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]


def _phu_de(img_path: Path, chu: str, ra: Path, rong: int, cao: int) -> None:
    """Cắt ảnh cho vừa khung dọc, kẻ dải tối ở chân và in phụ đề tiếng Việt có dấu."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(img_path).convert("RGB")
    tl = max(rong / im.width, cao / im.height)
    im = im.resize((int(im.width * tl) + 1, int(im.height * tl) + 1))
    x0, y0 = (im.width - rong) // 2, (im.height - cao) // 2
    im = im.crop((x0, y0, x0 + rong, y0 + cao))
    if chu.strip():
        dr = ImageDraw.Draw(im, "RGBA")
        font = None
        for f in _FONTS:
            if os.path.isfile(f):
                try:
                    font = ImageFont.truetype(f, int(rong * 0.058))
                    break
                except OSError:
                    continue
        if font is None:
            font = ImageFont.load_default()
        dong, hien = [], ""
        for tu in chu.split():
            thu = (hien + " " + tu).strip()
            if dr.textlength(thu, font=font) > rong * 0.84 and hien:
                dong.append(hien)
                hien = tu
            else:
                hien = thu
        if hien:
            dong.append(hien)
        dong = dong[:4]
        lh = int(rong * 0.07)
        top = cao - int(cao * 0.12) - lh * len(dong)
        dr.rectangle((0, top - int(lh * 0.6), rong, cao), fill=(0, 0, 0, 150))
        for i, l in enumerate(dong):
            w = dr.textlength(l, font=font)
            dr.text(((rong - w) / 2, top + i * lh), l, font=font, fill=(255, 255, 255, 255))
    im.save(ra, "PNG")


def _dung_video_dong_bo(canh: list, ten: str) -> dict:
    ff = shutil.which("ffmpeg")
    if not ff:
        raise ValueError("Máy chủ TISA BOT chưa cài ffmpeg nên chưa dựng được video từ ảnh.")
    rong, cao, fps = 1080, 1920, 30
    with tempfile.TemporaryDirectory(prefix="qc-video-") as td:
        td = Path(td)
        doan = []
        for i, c in enumerate(canh):
            t = T.tim_tep(c["tep_id"])
            if not t or t["loai"] != "anh":
                raise ValueError("Cảnh %d chưa có ảnh." % (i + 1))
            khung = td / ("k%02d.png" % i)
            _phu_de(Path(t["duong_dan"]), c.get("chu") or "", khung, rong, cao)
            giay = max(2.0, min(20.0, float(c.get("giay") or 3)))
            n = int(giay * fps)
            out = td / ("c%02d.mp4" % i)
            vf = "zoompan=z='min(zoom+0.0007,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d,format=yuv420p" % (n, rong, cao, fps)
            r = subprocess.run([ff, "-nostdin", "-v", "error", "-y", "-loop", "1", "-i", str(khung), "-t", "%.2f" % giay, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", str(out)],
                               capture_output=True, text=True, timeout=180, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if r.returncode != 0 or not out.is_file():
                raise ValueError("ffmpeg dựng cảnh %d chưa được: %s" % (i + 1, (r.stderr or "")[-160:]))
            doan.append(out)
        ds = td / "ds.txt"
        ds.write_text("".join("file '%s'\n" % p.as_posix() for p in doan), encoding="utf-8")
        ra = td / "video.mp4"
        r = subprocess.run([ff, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(ds), "-c", "copy", "-movflags", "+faststart", str(ra)],
                           capture_output=True, text=True, timeout=180, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode != 0 or not ra.is_file():
            raise ValueError("ffmpeg ghép video chưa được: " + (r.stderr or "")[-160:])
        return {"ok": True, "tep": _luu_tep_tu_file(ra, "video", ten or "video-quang-cao.mp4")}


async def dung_video(d: dict) -> dict:
    canh = []
    for c in (d.get("canh") or [])[:12]:
        if isinstance(c, dict) and c.get("tep_id"):
            canh.append({"tep_id": _cat(c.get("tep_id"), 20), "chu": _cat(c.get("chu"), 160), "giay": c.get("giay") or 3})
    if len(canh) < 2:
        raise ValueError("Cần ít nhất 2 cảnh có ảnh để dựng video.")
    return await asyncio.to_thread(_dung_video_dong_bo, canh, _cat(d.get("ten"), 80) + ".mp4" if d.get("ten") else "video-quang-cao.mp4")


# ---------------------------------------------------------------- báo cáo bằng chữ
_HE_THONG_BC = ("Bạn là trợ lý phân tích quảng cáo cho chủ doanh nghiệp nhỏ, không rành kỹ thuật. Viết báo cáo tiếng Việt ngắn gọn, dễ hiểu từ SỐ LIỆU được cung cấp. "
                "Chỉ dùng đúng các số trong dữ liệu, không bịa, không suy đoán số khác. Viết văn bản thuần, viết hoa đúng chính tả tiếng Việt (đầu câu, tên riêng), dùng gạch đầu dòng, không bảng, không ký hiệu markdown. "
                "Bố cục: 1) Tổng quan kỳ này (chi phí, kết quả, giá mỗi kết quả, doanh thu nếu có, so với kỳ trước). 2) Điểm tốt. 3) Cần chú ý. 4) Việc nên làm ngay (tối đa 3 việc, cụ thể). "
                "Mọi việc bật, tắt, đổi ngân sách chỉ là GỢI Ý để chủ quyết định.")


async def bao_cao(d: dict) -> dict:
    if _ASK is None:
        raise ValueError("Chưa nối được bộ não AI của TISA BOT. Đăng nhập Claude hoặc ChatGPT trong TISA BOT rồi thử lại.")
    kieu = d.get("kieu") if d.get("kieu") in ("hom-qua", "7-ngay", "30-ngay", "thang-nay", "thang-truoc") else "7-ngay"
    nen = d.get("nen") if d.get("nen") in Q.NEN else ""
    r = await asyncio.to_thread(Q.tong_quan, kieu, "", "", nen, bool(d.get("mau")), False, "chien-dich")
    if r.get("che_do") == "mau":
        raise ValueError("Đang là dữ liệu mẫu. Nối tài khoản thật rồi mới soạn báo cáo được.")
    t, c = r["tong"], r["doi"]
    so = lambda v: round(v, 2) if isinstance(v, float) else v
    dg = {"ky": "%s đến %s" % (r["tu"], r["den"]), "tien_te": r["tien_te"], "tong": {k: so(v) for k, v in t.items()}, "so_voi_ky_truoc_phan_tram": c,
          "theo_nen_tang": {Q.NEN[k]: {x: so(y) for x, y in v.items() if x in ("chi_phi", "ket_qua", "cpa", "doanh_thu", "roas", "ctr")} for k, v in r["theo_nen"].items()},
          "chien_dich_chi_nhieu_nhat": [{"ten": x["cd"], "nen": Q.NEN[x["nen"]], "chi_phi": so(x["chi_phi"]), "ket_qua": so(x["ket_qua"]), "cpa": so(x["cpa"]), "roas": so(x["roas"]), "trang_thai": x["trang_thai"]} for x in r["chien_dich"][:6]],
          "goi_y_he_thong": [{"muc": g["muc"], "tieu_de": g["tieu_de"], "chi_tiet": g["chi_tiet"]} for g in r["goi_y"][:6]], "muc_tieu_cua_chu": r["muc_tieu"]}
    try:
        raw = await asyncio.wait_for(_ASK(_HE_THONG_BC, "DỮ LIỆU (JSON):\n" + json.dumps(dg, ensure_ascii=False) + "\n\nHãy viết báo cáo."), 120)
    except asyncio.TimeoutError:
        raise ValueError("AI trả lời quá lâu. Thử lại.")
    except Exception as e:  # noqa: BLE001
        raise ValueError("Bộ não AI chưa trả lời được (%s)." % str(e)[:120])
    return {"ok": True, "bao_cao": str(raw or "").strip()[:6000], "ky": dg["ky"]}


# ---------------------------------------------------------------- hồ sơ Fanpage, kênh, website
def doc_ho_so() -> list:
    try:
        d = json.loads(TEP_HO_SO.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except (OSError, ValueError):
        return []


def luu_ho_so(d: dict) -> dict:
    nen = _cat(d.get("nen"), 12)
    if nen not in Q.NEN:
        raise ValueError("Chọn nền tảng.")
    ten = _cat(d.get("ten"), 100)
    if not ten:
        raise ValueError("Nhập tên Fanpage hoặc kênh.")
    h = {"id": _cat(d.get("id"), 20) or "hs-" + hashlib.sha1(("%s%s%s" % (nen, ten, time.time())).encode()).hexdigest()[:8], "nen": nen, "ten": ten, "link": _cat(d.get("link"), 300),
         "giong_van": _cat(d.get("giong_van"), 300), "san_pham": _cat(d.get("san_pham"), 1500), "ngay": time.strftime("%Y-%m-%d")}
    with _khoa:
        ds = [x for x in doc_ho_so() if x.get("id") != h["id"]]
        ds.insert(0, h)
        Q._ghi(TEP_HO_SO, ds[:60])
    return h


def xoa_ho_so(hid: str) -> bool:
    with _khoa:
        ds = doc_ho_so()
        moi = [x for x in ds if x.get("id") != hid]
        Q._ghi(TEP_HO_SO, moi)
    return len(moi) < len(ds)


# ---------------------------------------------------------------- link bài đã đăng
def phan_tich_link(nen: str, url: str) -> dict:
    """Nhận một link, báo bài của nền tảng nào, loại gì, mã bài. Link rút gọn thì báo để trợ lý mở ra lấy mã."""
    u = str(url or "").strip()
    if not u:
        return {"ok": False, "error": "Chưa có link."}
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    try:
        p = urllib.parse.urlparse(u)
    except ValueError:
        return {"ok": False, "error": "Link không đúng dạng."}
    host = (p.hostname or "").lower().removeprefix("www.").removeprefix("m.").removeprefix("web.")
    path, q = p.path or "", urllib.parse.parse_qs(p.query)
    ra = {"ok": True, "chuan": u, "nen_link": "", "loai": "", "ma_bai": "", "trang": "", "ghi_chu": "", "rut_gon": False}
    if host in ("facebook.com", "fb.com", "fb.watch", "l.facebook.com") or host.endswith(".facebook.com"):
        ra["nen_link"] = "facebook"
        m = re.search(r"/(?:posts|videos|reel|reels|photos?)/([\w.-]+)", path)
        if "permalink.php" in path or "story.php" in path:
            ra["loai"], ra["ma_bai"], ra["trang"] = "bai_viet", (q.get("story_fbid") or [""])[0], (q.get("id") or [""])[0]
        elif "/share/" in path or host == "fb.watch":
            ra["loai"], ra["rut_gon"] = "rut_gon", True
            ra["ghi_chu"] = "Đây là link chia sẻ rút gọn. Không sao: trợ lý sẽ mở link để lấy mã bài thật."
        elif m:
            ra["loai"] = "video" if re.search(r"/(videos|reel|reels)/", path) else ("anh" if "/photo" in path else "bai_viet")
            ra["ma_bai"], ra["trang"] = m.group(1), path.strip("/").split("/")[0]
        elif path.startswith("/watch"):
            ra["loai"], ra["ma_bai"] = "video", (q.get("v") or [""])[0]
        elif "/photo" in path:
            ra["loai"], ra["ma_bai"] = "anh", (q.get("fbid") or [""])[0]
        else:
            ra["loai"] = "khong_ro"
            ra["ghi_chu"] = "Link này chưa giống một bài viết cụ thể (có thể là link trang). Hãy mở bài cần chạy rồi chép link của đúng bài đó."
    elif host.endswith("tiktok.com"):
        ra["nen_link"] = "tiktok"
        m = re.search(r"/@([^/]+)/video/(\d+)", path)
        if m:
            ra["loai"], ra["trang"], ra["ma_bai"] = "video", "@" + m.group(1), m.group(2)
        elif host in ("vm.tiktok.com", "vt.tiktok.com") or re.match(r"^/[\w]{6,}/?$", path):
            ra["loai"], ra["rut_gon"] = "rut_gon", True
            ra["ghi_chu"] = "Link rút gọn của TikTok. Trợ lý sẽ mở ra để lấy mã video."
        else:
            ra["loai"] = "khong_ro"
            ra["ghi_chu"] = "Link này chưa giống một video cụ thể. Mở đúng video rồi bấm Chia sẻ > Sao chép liên kết."
    elif host in ("youtube.com", "youtu.be", "music.youtube.com") or host.endswith(".youtube.com"):
        ra["nen_link"] = "google"
        vid = (q.get("v") or [""])[0] if "watch" in path else (path.strip("/").split("/")[-1] if host == "youtu.be" or "/shorts/" in path else "")
        ra["loai"] = "shorts" if "/shorts/" in path else ("video" if vid else "khong_ro")
        ra["ma_bai"] = vid
        if not vid:
            ra["ghi_chu"] = "Link này chưa giống một video cụ thể."
    else:
        return {"ok": False, "error": "Link này không phải của Facebook, TikTok hay YouTube."}
    if nen in Q.NEN and ra["nen_link"] and ra["nen_link"] != nen:
        ten_l = Q.NEN[ra["nen_link"]]
        return {"ok": False, "error": "Đây là link của %s, nhưng anh đang chọn %s. Đổi nền tảng ở bước 1 hoặc dùng link đúng nền tảng." % (ten_l, Q.NEN[nen])}
    if ra["loai"] != "khong_ro" and not ra["ma_bai"] and not ra["rut_gon"]:
        ra["ghi_chu"] = ra["ghi_chu"] or "Chưa đọc được mã bài từ link. Kiểm tra link có đủ không."
    ra["mo_ta"] = {"bai_viet": "Bài viết", "video": "Video", "anh": "Ảnh", "shorts": "YouTube Shorts", "rut_gon": "Link rút gọn", "khong_ro": "Chưa rõ"}.get(ra["loai"], "Bài")
    ra["ok"] = ra["loai"] != "khong_ro" or True
    ra["can_than"] = ra["loai"] == "khong_ro"
    return ra


# ---------------------------------------------------------------- đường dẫn
def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=ma)

    @app.get("/tisa-quang-cao/api/ai/tang")
    async def _tang():
        return {"ok": True, **tang_cong_khai(), "trang_thai": await asyncio.to_thread(trang_thai_ai)}

    @app.post("/tisa-quang-cao/api/ai/viet")
    async def _viet(request: Request):
        try:
            return await viet_noi_dung(await request.json())
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/ai/anh")
    async def _anh(request: Request):
        try:
            return await tao_anh(await request.json())
        except LoiAnh as e:
            return JSONResponse({"ok": False, "error": str(e), "giao_viec": e.giao_viec}, status_code=400)
        except ValueError as e:
            return loi(str(e))
        except Exception as e:  # noqa: BLE001
            return loi("Tạo ảnh chưa được: %s" % str(e)[:160], 500)

    @app.post("/tisa-quang-cao/api/ai/video")
    async def _video(request: Request):
        try:
            return await dung_video(await request.json())
        except ValueError as e:
            return loi(str(e))
        except subprocess.TimeoutExpired:
            return loi("Dựng video quá lâu, thử ít cảnh hơn.")

    @app.post("/tisa-quang-cao/api/ai/bao-cao")
    async def _bc(request: Request):
        try:
            return await bao_cao(await request.json())
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/ho-so")
    async def _ds_hs():
        return {"ok": True, "ho_so": doc_ho_so()}

    @app.post("/tisa-quang-cao/api/ho-so")
    async def _luu_hs(request: Request):
        try:
            return {"ok": True, "ho_so": luu_ho_so(await request.json())}
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/ho-so/{hid}/xoa")
    async def _xoa_hs(hid: str):
        return {"ok": xoa_ho_so(hid)}

    @app.get("/tisa-quang-cao/api/phan-tich-link")
    async def _link(request: Request):
        q = request.query_params
        return phan_tich_link(q.get("nen", ""), q.get("url", ""))
