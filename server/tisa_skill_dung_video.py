"""tisa_skill_dung_video.py - Đưa bản dựng video NHANH (Bộ TISA V3.49) vào skill tisa-edit-video-studio đã cài trong bộ não.

Vì sao có file này: skill nằm trong bộ não (brains/..., không lên GitHub) nên bấm "Cập nhật" không tự đổi được render.mjs của nó.
Mỗi lần máy chủ khởi động, hàm ap_dung() tìm skill đã cài và thay render.mjs CŨ bằng bản mới (kèm sao lưu), rồi sửa đúng 2 dòng hướng dẫn cho AI.
Bản mới (server/skill-ban-va/tisa-edit-video-studio/render.mjs): dựng nhiều cảnh cùng lúc, nhớ cảnh đã dựng, kiểm ảnh thiếu trước khi dựng, khoá chống dựng trùng.

An toàn:
- Chỉ đụng file đúng hình dạng render.mjs gốc của skill này (có dòng "usage: node render.mjs" và gọi renderMedia) và CHƯA có chữ "V3.49".
- Sao lưu bản cũ thành render.mjs.truoc-V3.49 (không đè nếu đã có). Ghi qua file tạm rồi đổi tên.
- Bản sửa tay của người dùng (khác hình dạng gốc) vẫn được thay vì skill gốc luôn là bản này; nhưng bản cũ nằm trong .truoc-V3.49 để lấy lại.
- Chạy lặp lại không đổi gì thêm. Mọi lỗi chỉ ghi log, không làm hỏng việc khởi động.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOI = ROOT / "server" / "skill-ban-va" / "tisa-edit-video-studio" / "render.mjs"
DAU = "V3.49"
MOC_MOI = "V3.52"      # bản có chốt chống treo, hàng đợi chung, headless-shell (RENDER_REV xem render.mjs)
TEN_SKILL = "tisa-edit-video-studio"

_DONG_SKILL_CU = ("5. **Render** `node remotion/render.mjs S5|S4 <propsDir> <outDir> sid…` + kiểm tra bằng `sheet.sh` (contact sheet) – nhìn từng khung trước khi gửi.")
_DONG_SKILL_MOI = ("5. **Render** `node remotion/render.mjs S5|S4 <propsDir> <outDir> sid…` (MỘT lệnh cho tất cả cảnh; tự chạy song song, tự bỏ qua cảnh chưa đổi, tự báo thiếu ảnh trước khi dựng, "
                   "không đặt `CONC`, không mở 2 tiến trình) + kiểm tra bằng `sheet.sh` (contact sheet) – nhìn từng khung trước khi gửi.")
_DONG_WF_CU_DAU = "`node ../remotion/render.mjs S5 $TISA_WORK/props $TISA_WORK/rend hook c1 c2 …`"
_KHOI_WF_MOI = """
**Cách dựng nhanh (bản V3.49, đã đo trên máy 12 nhân: nhanh gấp ~3 lần so với cách cũ):**
- Chạy ĐÚNG MỘT lệnh với TẤT CẢ các cảnh cần dựng, để `render.mjs` tự chia cảnh chạy cùng lúc. KHÔNG mở hai tiến trình dựng song song, KHÔNG đặt `CONC` cao (đã đo: 1 cảnh dù 2 hay 10 luồng đều ~12 khung/giây; nhiều cảnh cùng lúc mới nhanh).
- `render.mjs` tự nhớ cảnh nào đã dựng (file `.hash` cạnh mp4). Sửa 1 cảnh rồi chạy lại cùng lệnh: chỉ cảnh đổi được dựng lại, cảnh còn lại báo "bỏ qua". Muốn ép dựng lại hết: `FORCE=1`.
- Trước khi mở Chrome nó kiểm mọi ảnh/video trong props (và ảnh ghi cứng trong mã như `s3/info2..7.png` của mẫu carousel). Thiếu tệp thì dừng ngay, báo tên tệp thiếu: bổ sung vào `remotion/public/` rồi chạy lại. Đừng thử dựng khi chưa có ảnh.
- Có khoá chống dựng trùng và ghi file nguyên vẹn (`.part.mp4` rồi mới đổi tên): lỡ chạy hai lần cũng không hỏng file."""


_DONG_CHO_CU = "- Có khoá chống dựng trùng và ghi file nguyên vẹn (`.part.mp4` rồi mới đổi tên): lỡ chạy hai lần cũng không hỏng file."
_DONG_CHO_MOI = (_DONG_CHO_CU + "\n- Chờ dựng xong: KHÔNG dùng `tail -n0 -F <log>` (chỉ báo dòng MỚI; dựng xong trước khi bắt đầu chờ thì chờ mãi, chat đứng im, "
                 "tin của người dùng không ai đọc). Dùng `until grep -q 'Xong sau' <log>; do sleep 3; done` (đọc cả file), hoặc xem `.mp4` và `.hash` của từng cảnh trong thư mục kết quả (V3.53).")


_DONG_TRINH_DUYET_MOI = ("- Trình duyệt dựng: `render.mjs` tự dùng chrome-headless-shell của Remotion (nhanh hơn Chrome thường ~1,6 lần, không chiếm Chrome của người dùng; tự tải 1 lần). "
                         "KHÔNG đặt `CHROME=/Applications/Google Chrome.app/...` khi chạy: Chrome thường bị bỏ qua (V3.55).")


def _thu_muc_skill(brains_dir) -> list:
    """Mọi thư mục skill đã cài: <brain>/skills/<skill> và <brain>/.claude/skills/<skill> (bỏ trùng theo đường dẫn thật)."""
    out, thay = [], set()
    try:
        brains = [d for d in Path(brains_dir).iterdir() if d.is_dir() and not d.name.startswith(".")]
    except OSError:
        return out
    for b in brains:
        for rel in (("skills", TEN_SKILL), (".claude", "skills", TEN_SKILL)):
            d = b.joinpath(*rel)
            try:
                r = d.resolve()
                if d.is_dir() and r not in thay and (d / "remotion").is_dir():
                    thay.add(r)
                    out.append(d)
            except OSError:
                continue
    return out


def _ghi(p: Path, text: str) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def _rev(text: str) -> int:
    """Số bản của render.mjs: dòng `// RENDER_REV: n`. Không có dòng này = 0 (bản gốc của skill hoặc bản V3.49 đầu tiên)."""
    m = re.search(r"RENDER_REV:\s*(\d+)", text or "")
    return int(m.group(1)) if m else 0


def _la_render_goc(text: str, rev_moi: int = 1) -> bool:
    """Đúng hình dạng render.mjs của skill này và CŨ hơn bản đang phát (so theo RENDER_REV): gồm bản gốc, bản V3.49, bản chưa có hàng đợi chung."""
    return "usage: node render.mjs" in text and "renderMedia" in text and _rev(text) < rev_moi


def va_mot_skill(d: Path, moi_text: str) -> list:
    """Trả danh sách việc đã làm (rỗng nếu không có gì đổi)."""
    lam = []
    f = d / "remotion" / "render.mjs"
    try:
        cu = f.read_text(encoding="utf-8")
    except OSError:
        cu = None
    if cu is not None and _la_render_goc(cu, _rev(moi_text)):
        sao = f.with_name("render.mjs.truoc-V3.52" if DAU in cu else "render.mjs.truoc-V3.49")   # bản V3.49 cũ giữ riêng, không đè bản gốc
        if not sao.exists():
            shutil.copy2(f, sao)
        _ghi(f, moi_text)
        lam.append("render.mjs")
    # hai dòng hướng dẫn cho AI: chỉ sửa khi còn đúng câu gốc
    sk = d / "SKILL.md"
    try:
        t = sk.read_text(encoding="utf-8")
        if _DONG_SKILL_CU in t and DAU not in t:
            _ghi(sk, t.replace(_DONG_SKILL_CU, _DONG_SKILL_MOI))
            lam.append("SKILL.md")
    except OSError:
        pass
    wf = d / "reference" / "workflow.md"
    try:
        lines = wf.read_text(encoding="utf-8").split("\n")
        if DAU not in "\n".join(lines):
            for i, ln in enumerate(lines):
                if ln.startswith(_DONG_WF_CU_DAU):
                    cat = ln.split(" Máy 2 CPU")[0]
                    lines[i] = cat + _KHOI_WF_MOI
                    _ghi(wf, "\n".join(lines))
                    lam.append("workflow.md")
                    break
    except OSError:
        pass
    # V3.53: dặn AI không chờ bằng `tail -F` (đã gây kẹt cả chat). Chỉ thêm khi còn đúng câu cũ và chưa có dặn này.
    try:
        t = wf.read_text(encoding="utf-8")
        if _DONG_CHO_CU in t and "V3.53" not in t:
            _ghi(wf, t.replace(_DONG_CHO_CU, _DONG_CHO_MOI, 1))
            lam.append("workflow.md (chờ dựng)")
    except OSError:
        pass
    # V3.55: dặn AI không đặt CHROME=Chrome thường. Chèn ngay sau dặn "Chờ dựng xong" (V3.53).
    try:
        t = wf.read_text(encoding="utf-8")
        if "V3.53" in t and "V3.55" not in t:
            ls = t.split("\n")
            for i, ln in enumerate(ls):
                if ln.startswith("- Chờ dựng xong:"):
                    ls.insert(i + 1, _DONG_TRINH_DUYET_MOI)
                    _ghi(wf, "\n".join(ls))
                    lam.append("workflow.md (trình duyệt)")
                    break
    except OSError:
        pass
    return lam


def ap_dung(brains_dir) -> dict:
    kq = {"da_va": [], "loi": ""}
    try:
        moi_text = MOI.read_text(encoding="utf-8")
        if DAU not in moi_text or MOC_MOI not in moi_text:
            kq["loi"] = "bản mới thiếu dấu V3.49/V3.52"
            return kq
        for d in _thu_muc_skill(brains_dir):
            try:
                lam = va_mot_skill(d, moi_text)
            except Exception as e:  # noqa: BLE001
                print(f"[skill dựng video] không vá được {d}: {type(e).__name__}: {e}", file=sys.stderr)
                continue
            if lam:
                kq["da_va"].append({"skill": str(d), "file": lam})
                print(f"[skill dựng video] đã đưa bản dựng nhanh (có chốt chống treo V3.52) vào {d}: {', '.join(lam)}", file=sys.stderr)
    except Exception as e:  # noqa: BLE001
        kq["loi"] = f"{type(e).__name__}: {e}"
        print(f"[skill dựng video] bỏ qua: {kq['loi']}", file=sys.stderr)
    return kq
