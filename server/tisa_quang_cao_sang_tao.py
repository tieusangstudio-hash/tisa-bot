"""tisa_quang_cao_sang_tao.py - ảnh và video quảng cáo do ĐÚNG cộng sự làm, trên nền bộ não của doanh nghiệp (V2.78).

Hai đường, đều đi qua Bảng giao việc của Đội Quân AI:
  1. CHỈ ĐẠO HÌNH: trước khi vẽ ảnh, trang nhắn cộng sự thiết kế hình ảnh (tự chọn theo chức danh). Người này đọc bộ não, hiểu sản phẩm, rồi
     viết lời chỉ đạo cho TỪNG ảnh (cảnh, ánh sáng, chỗ đặt logo, nhân vật, sản phẩm, chữ tiếng Việt). Trang dùng lời chỉ đạo đó để tạo ảnh.
     Cộng sự chưa trả lời kịp hoặc chưa có Bảng thì trang tự dùng lời tả có sẵn kèm kiến thức đọc từ bộ não, không bị kẹt.
  2. GIAO VIỆC: nút "Giao cộng sự làm" tạo một việc thật trên Bảng cho cộng sự thiết kế (làm ảnh) hoặc cộng sự dựng video (làm video),
     kèm kịch bản, ảnh tham chiếu, độ dài, dặn đọc bộ não trước. Tiến độ hiện ngay trong trang; file kết quả cộng sự lưu trong thư mục
     của việc được trang nhận về.
Việc nào cũng chỉ SOẠN: không đăng, không bật quảng cáo, không chi tiền.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import time
from pathlib import Path

import tisa_quang_cao as Q
import tisa_quang_cao_ai as A
import tisa_quang_cao_giao_viec as G
import tisa_quang_cao_thiet_lap as T
import tisa_quang_cao_tu_van as TV

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

TEP_DA_NHAP = Q.KHO / "sang-tao-da-nhap.json"
ANH = (".png", ".jpg", ".jpeg", ".webp")
VIDEO = (".mp4", ".mov", ".webm", ".m4v")
MAX_ANH_BYTE = 25 * 1024 * 1024
MAX_VIDEO_BYTE = 600 * 1024 * 1024
CHO_TOI_DA = 240

LUAT_HINH = ("\n\n(Đây là việc từ trang Quảng Cáo của TISA BOT. TRƯỚC HẾT đọc bộ não của doanh nghiệp (00-DOC-TRUOC, 01-ho-so, 02-kien-thuc) để hiểu ĐÚNG sản phẩm, "
             "khách hàng, màu sắc, giọng thương hiệu và quy tắc. Chỉ trả lời bằng MỘT khối JSON đúng khuôn, không giải thích thêm, không tạo ảnh, không đăng gì, không chạm vào tài khoản quảng cáo.)")


def doi_hinh() -> dict:
    """Cộng sự sẽ nhận việc ảnh và video (để trang hiện tên trước khi anh bấm)."""
    out = {"bang": True, "thiet_ke": None, "video": None, "quang_cao": None}
    try:
        for k, vai in (("thiet_ke", "thiet-ke"), ("video", "video"), ("quang_cao", "quang-cao")):
            ds = G.ung_vien("", vai)
            out[k] = ds[0] if ds else None
    except G.ChuaCoBang:
        out["bang"] = False
    except ValueError:
        pass
    return out


# ---------------------------------------------------------------- chỉ đạo hình ảnh
def _tom_tat_tham_chieu(d: dict) -> list:
    dong = []
    for khoa, nhan, mo, t in A.tham_chieu_theo_vai(d):
        dong.append("- %s: %s (mở xem tại %s)" % (nhan, t["ten"], t["duong_dan"]))
    return dong


def soan_chi_dao(d: dict) -> tuple:
    """(lời nhắn gửi cộng sự thiết kế, số ảnh cần chỉ đạo)."""
    tang = next((t for t in A.TANG if t["id"] == int(d.get("tang") or 3)), A.TANG[2])
    nen = A._cat(d.get("nen"), 12)
    muc = [m for m in (d.get("muc") or []) if isinstance(m, dict)][:12]
    if not muc:
        raise ValueError("Chưa có ảnh nào cần chỉ đạo.")
    sp = A._cat(d.get("san_pham"), 900)
    bn = A._bo_nao_cho(d, sp, 2600)
    dong = ["CHỈ ĐẠO HÌNH ẢNH CHO QUẢNG CÁO %s" % (Q.NEN.get(nen) or "").upper(),
            "Tầng phễu %d: %s (%s). Mục tiêu: %s" % (tang["id"], tang["ten"], tang["khach"], tang["muc_tieu"]),
            "Sản phẩm, dịch vụ anh nhập: " + sp]
    for nhan, k in (("Khách hàng mục tiêu", "khach"), ("Điểm khác biệt", "khac_biet"), ("Phong cách hình", "phong_cach")):
        if A._cat(d.get(k), 300):
            dong.append("%s: %s" % (nhan, A._cat(d.get(k), 300)))
    if A._cat(d.get("tieu_de"), 200):
        dong.append("Tiêu đề bài: " + A._cat(d.get("tieu_de"), 200))
    if A._cat(d.get("noi_dung"), 700):
        dong.append("Nội dung bài (để hình ăn khớp): " + A._cat(d.get("noi_dung"), 700).replace("\n", " "))
    if bn["text"]:
        dong += ["", "KIẾN THỨC TRÍCH TỪ BỘ NÃO (kiểm lại trong bộ não nếu cần):", bn["text"][:2600]]
    elif bn["thieu"]:
        dong.append("Lưu ý: hồ sơ bộ não còn trống ở: %s. Thiếu gì thì ghi [cần anh bổ sung], đừng bịa." % ", ".join(bn["thieu"][:5]))
    ref = _tom_tat_tham_chieu(d)
    if ref:
        dong += ["", "ẢNH THAM CHIẾU anh đã tải lên (hệ thống sẽ gửi các ảnh này cho AI vẽ, bạn chỉ cần dặn cách dùng):"] + ref + [
            "Quy tắc: nhân vật phải giống hệt ảnh nhân vật; logo đặt nguyên vẹn ở một góc, không méo; sản phẩm giống hệt ảnh sản phẩm."]
    dong += ["", "CẦN %d ẢNH:" % len(muc)]
    for i, m in enumerate(muc, 1):
        dong.append("%d. Ý chính: %s | Chữ nên in trên ảnh: %s | Mô tả sơ bộ: %s" % (i, A._cat(m.get("y"), 300) or "(theo bài)", A._cat(m.get("chu"), 90) or "(không)", A._cat(m.get("mo_ta"), 450) or "(chưa có)"))
    dong += ["", ("Chèn chữ lên ảnh: CÓ, chữ tiếng Việt có dấu đúng chính tả." if d.get("chen_chu") else "Chèn chữ lên ảnh: KHÔNG, ảnh sạch."),
             "Trả về đúng khuôn: {\"anh\": [{\"prompt\": \"lời chỉ đạo chi tiết bằng tiếng Anh cho AI vẽ: chủ thể, bối cảnh, ánh sáng, bố cục, màu thương hiệu, chỗ để chữ, cách dùng nhân vật/logo/sản phẩm tham chiếu\", \"chu\": \"câu tiếng Việt in trên ảnh nếu có, không thì để trống\"}]} "
             "(đúng %d phần tử, đúng thứ tự)." % len(muc)]
    return "\n".join(dong)[:6200], len(muc)


async def chi_dao_hinh(d: dict) -> dict:
    """Nhờ cộng sự thiết kế viết lời chỉ đạo cho từng ảnh. Không được thì trả ok False kèm lý do để trang dùng đường dự phòng."""
    try:
        msg, n = soan_chi_dao(d)
        r = await asyncio.to_thread(TV.gui, msg, "", str(d.get("cong_su") or ""), "thiet-ke", LUAT_HINH)
    except G.ChuaCoBang as e:
        return {"ok": False, "chua_co_bang": True, "error": str(e)}
    cs, tin = r["cong_su"], r["tin"]
    han = time.time() + CHO_TOI_DA
    text = ""
    while time.time() < han:
        await asyncio.sleep(3)
        try:
            x = await asyncio.to_thread(TV.doc, tin)
        except (G.ChuaCoBang, ValueError):
            continue
        text = x.get("text") or ""
        if x.get("xong") and text:
            break
    if not text:
        return {"ok": False, "cong_su": cs, "error": "%s chưa trả lời kịp. Trang dùng lời tả có sẵn để tạo ảnh." % cs["ten"]}
    try:
        j = A._json_tu_chu(text)
        ds = [{"prompt": A._cat(x.get("prompt"), 1800), "chu": A._cat(x.get("chu"), 80)} for x in (j.get("anh") or []) if isinstance(x, dict)]
    except (ValueError, TypeError):
        ds = []
    ds = [x for x in ds if x["prompt"]]
    if len(ds) < n:
        return {"ok": False, "cong_su": cs, "error": "%s trả lời chưa đủ %d ảnh. Trang dùng lời tả có sẵn để tạo ảnh." % (cs["ten"], n)}
    return {"ok": True, "cong_su": cs, "anh": ds[:n]}


# ---------------------------------------------------------------- giao việc thật
def _chep_vao_bo_nao(t: dict, nhan: str) -> str:
    """Chép ảnh tham chiếu vào thư mục attachments của bộ não để cộng sự mở được; trả đường dẫn tương đối."""
    import image_gen
    vault = image_gen._resolve_vault(None)
    adir = image_gen._attachments_dir(vault)
    cp = adir / ("qc-%s-%s%s" % (nhan, t["id"], Path(t["duong_dan"]).suffix))
    shutil.copyfile(t["duong_dan"], cp)
    return os.path.relpath(cp, vault).replace(os.sep, "/")


def _brief(d: dict, vai: str, folder: str, cs: dict) -> str:
    nen = A._cat(d.get("nen"), 12)
    tang = next((t for t in A.TANG if t["id"] == int(d.get("tang") or 3)), A.TANG[2])
    sp = A._cat(d.get("san_pham"), 900)
    pa = d.get("pa") if isinstance(d.get("pa"), dict) else {}
    L = ["Giao cho %s: làm %s cho quảng cáo %s, theo phiếu từ trang Quảng Cáo của TISA BOT." % (cs["ten"], "ẢNH" if vai == "thiet-ke" else "VIDEO", Q.NEN.get(nen, nen)),
         "", "BƯỚC 1 (bắt buộc): ĐỌC BỘ NÃO trước khi làm: 00-DOC-TRUOC, muc-luc, 01-ho-so (sản phẩm, khách hàng, thương hiệu), 02-kien-thuc. Làm ĐÚNG sản phẩm, giá, giọng và quy tắc ở đó. Thiếu thông tin thì ghi rõ chỗ thiếu, đừng bịa.",
         "", "TẦNG PHỄU %d: %s (%s). Mục tiêu: %s" % (tang["id"], tang["ten"], tang["khach"], tang["muc_tieu"]), "SẢN PHẨM, DỊCH VỤ: " + sp]
    for nhan, k in (("Khách hàng mục tiêu", "khach"), ("Điểm khác biệt", "khac_biet"), ("Phong cách hình", "phong_cach")):
        if A._cat(d.get(k), 300):
            L.append("%s: %s" % (nhan, A._cat(d.get(k), 300)))
    if A._cat(pa.get("tieu_de"), 200):
        L.append("Tiêu đề bài: " + A._cat(pa.get("tieu_de"), 200))
    if A._cat(pa.get("noi_dung"), 700):
        L.append("Nội dung bài: " + A._cat(pa.get("noi_dung"), 700).replace("\n", " "))
    refs = []
    for khoa, nhan, mo, t in A.tham_chieu_theo_vai(d):
        try:
            refs.append("- %s: %s (trong bộ não)" % (nhan, _chep_vao_bo_nao(t, khoa)))
        except OSError:
            refs.append("- %s: %s" % (nhan, t["duong_dan"]))
    if refs:
        L += ["", "ẢNH THAM CHIẾU (mở xem, dựng đúng theo): nhân vật giống hệt, logo đặt nguyên vẹn, sản phẩm giống hệt:"] + refs
    if vai == "thiet-ke":
        mm = [m for m in (d.get("muc") or []) if isinstance(m, dict)][:12]
        L += ["", "CẦN %d ẢNH (tỉ lệ %s):" % (len(mm), "dọc 9:16" if d.get("ty_le") == "portrait" else "vuông 1:1")]
        for i, m in enumerate(mm, 1):
            L.append("%d. Ý chính: %s | Chữ in trên ảnh: %s | Mô tả: %s" % (i, A._cat(m.get("y"), 200) or "(theo bài)", A._cat(m.get("chu"), 90) or "(không)", A._cat(m.get("mo_ta"), 350) or "(chưa có)"))
        L += ["", "Dùng công cụ tạo ảnh của TISA BOT (tạo ảnh bằng ChatGPT) nếu có. Chữ tiếng Việt trên ảnh phải đúng dấu, kiểm lại từng ảnh. Đưa 2 phương án nếu được."]
    else:
        cc = [c for c in (d.get("muc") or []) if isinstance(c, dict)][:12]
        do_dai = A.so_giay(d.get("do_dai"))
        L += ["", "VIDEO DỌC 9:16, dài khoảng %d giây, %d cảnh. Cảnh đầu là hook 3 giây, cảnh cuối kêu gọi hành động (%s)." % (do_dai, len(cc), A._cat(pa.get("cta"), 40) or tang["cta"]), "KỊCH BẢN:"]
        for i, c in enumerate(cc, 1):
            L.append("Cảnh %d (%ss): hình: %s | lời: %s | chữ trên màn hình: %s" % (i, A._cat(c.get("giay"), 6) or "4", A._cat(c.get("mo_ta"), 300), A._cat(c.get("loi"), 300), A._cat(c.get("chu"), 90)))
        L += ["", "Dựng bằng công cụ video đã nối (video AI hoặc ffmpeg trên máy). Có phụ đề tiếng Việt đúng dấu. Chưa có công cụ nào thì nói rõ và đề xuất cách, đừng làm giả."]
    L += ["", "LƯU KẾT QUẢ (file %s) vào đúng thư mục của việc này: %s" % ("ảnh .png/.jpg" if vai == "thiet-ke" else "video .mp4", folder),
          "Trang Quảng Cáo sẽ tự nhận file trong thư mục đó. Không đăng, không bật quảng cáo, không chi tiền; chỉ soạn để anh duyệt."]
    return "\n".join(L)


def giao_sang_tao(d: dict) -> dict:
    vai = "video" if d.get("vai") == "video" else "thiet-ke"
    ds = G.ung_vien("", vai)
    if not ds:
        raise ValueError("Chưa thấy cộng sự nào phụ trách %s trong đội hình. Vào Cài đặt đội thêm một người, hoặc tải %s có sẵn lên." % (G.VAI[vai]["ten"], "ảnh" if vai == "thiet-ke" else "video"))
    cs = next((x for x in ds if x["id"] == str(d.get("cong_su") or "")), ds[0])
    kit = G._bang("GET", "/api/db/settings/kit")
    vp = (kit.get("brain") or {}).get("office") or "05 - Van Phong AI"
    hom = time.localtime()
    ngay, gio = time.strftime("%Y-%m-%d", hom), time.strftime("%H:%M", hom)
    ten_pa = A._cat((d.get("pa") or {}).get("tieu_de"), 40) or ("quang cao " + ("anh" if vai == "thiet-ke" else "video"))
    tieu = "Giao cho %s: %s quảng cáo %s" % (cs["ten"], "Làm ảnh" if vai == "thiet-ke" else "Làm video", ten_pa)
    folder = "%s/03 - Ket qua/%s/%s/%s/%s %s/" % (vp, ngay[:4], ngay[:7], ngay, gio.replace(":", ""), G._slug(tieu))
    de_bai = _brief(d, vai, folder, cs)
    if len(de_bai) > G.GIOI_HAN_DE_BAI:
        de_bai = de_bai[:G.GIOI_HAN_DE_BAI - 60] + "\n...(phiếu đầy đủ ở trường phieu_qc)"
    vid = G._id_viec()
    iso = time.strftime("%Y-%m-%dT%H:%M:%S", hom) + ".000Z"
    doc = {"title": tieu[:160], "task": de_bai, "date": ngay, "time": gio, "created": iso, "updated": iso, "status": "hang-doi", "mode": "claude", "demo": False, "folder": folder,
           "plan": [], "summary": "", "insights": [], "synced": False, "brain": "cho-nap", "settings": {}, "files": [], "nguon": "quang-cao", "phieu_qc": _brief(d, vai, folder, cs)[:20000], "nen_qc": A._cat(d.get("nen"), 12)}
    G._bang("PUT", "/api/db/results/" + vid, doc)
    return {"ok": True, "viec": vid, "cong_su": cs, "tieu_de": doc["title"], "vai": vai}


def _da_nhap() -> dict:
    try:
        x = json.loads(TEP_DA_NHAP.read_text(encoding="utf-8"))
        return x if isinstance(x, dict) else {}
    except (OSError, ValueError):
        return {}


def nhan_ket_qua(vid: str) -> list:
    """Quét thư mục kết quả của việc, nhận ảnh/video mới về kho tải lên của trang. Trả danh sách tệp công khai (mới và cũ của việc này)."""
    vid = re.sub(r"[^\w-]", "", vid or "")
    job = G._bang("GET", "/api/v1/job/" + vid)
    kit = G._bang("GET", "/api/db/settings/kit")
    goc = Path(str((kit.get("brain") or {}).get("abs") or (kit.get("brain") or {}).get("path") or ""))
    rel = str((job or {}).get("folder") or "").strip().strip("/")
    if not rel or not goc.is_dir():
        return []
    thu_muc = (goc / rel).resolve()
    try:
        thu_muc.relative_to(goc.resolve())
    except ValueError:
        return []
    if not thu_muc.is_dir():
        return []
    import tisa_quang_cao_ai as AI
    da = _da_nhap()
    ra = []
    for p in sorted(thu_muc.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in ANH + VIDEO:
            continue
        loai = "video" if p.suffix.lower() in VIDEO else "anh"
        try:
            kt = p.stat().st_size
        except OSError:
            continue
        if kt > (MAX_VIDEO_BYTE if loai == "video" else MAX_ANH_BYTE) or kt < 1000:
            continue
        khoa = "%s|%d|%d" % (p, kt, int(p.stat().st_mtime))
        tid = da.get(khoa)
        t = T.tim_tep(tid) if tid else None
        if not t:
            pub = AI._luu_tep_tu_file(p, loai, p.name)
            da[khoa] = pub["id"]
            Q._ghi(TEP_DA_NHAP, da)
            ra.append(pub)
        else:
            ra.append(T.tep_cong_khai(t))
    return ra


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def loi(msg, ma=400, chua_co_bang=False):
        return JSONResponse({"ok": False, "error": msg, "chua_co_bang": chua_co_bang}, status_code=ma)

    @app.get("/tisa-quang-cao/api/ai/doi-hinh")
    async def _dh():
        return {"ok": True, **(await asyncio.to_thread(doi_hinh))}

    @app.post("/tisa-quang-cao/api/ai/chi-dao")
    async def _cd(request: Request):
        try:
            return await chi_dao_hinh(await request.json())
        except ValueError as e:
            return loi(str(e))

    @app.post("/tisa-quang-cao/api/giao-sang-tao")
    async def _gs(request: Request):
        try:
            return await asyncio.to_thread(giao_sang_tao, await request.json())
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/giao-sang-tao/{vid}")
    async def _xs(vid: str):
        try:
            x = await asyncio.to_thread(G.xem_viec, vid)
            try:
                x["tep"] = await asyncio.to_thread(nhan_ket_qua, vid)
            except Exception:  # noqa: BLE001
                x["tep"] = []
            return x
        except G.ChuaCoBang as e:
            return loi(str(e), 200, True)
        except ValueError as e:
            return loi(str(e))
