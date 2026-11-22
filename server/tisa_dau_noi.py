"""tisa_dau_noi.py - Cộng sự "Đạt Đấu Nối": người làm riêng mọi việc nối công cụ (MCP, API, OAuth) cho TISA BOT (chủ yêu cầu 19/11/2026).

Chủ: "phần hỗ trợ nối giao cho một cộng sự kỹ thuật có skill và kinh nghiệm đấu nối MCP, API; nghiên cứu cách làm trước rồi triển khai, làm liên tục,
khó thì tự tìm giải pháp; có chỗ chọn mô hình và mức nỗ lực ở phần cài đặt; không dùng đại một ô chat không có kinh nghiệm."

Cách làm:
- Hồ sơ cộng sự là một tệp agent thường (suite/agents/tisa-dau-noi.md, cài vào brain/agents cùng các cộng sự khác). Các nút "Nhờ TISA BOT kết nối giúp"
  mở một cuộc chat kênh `agent:tisa-dau-noi` (TISA BOT tự nạp lời nhắc, kỹ năng, mô hình và mức suy luận của cộng sự này vào từng lượt).
- Mô hình và mức nỗ lực nằm ngay trong phần đầu (frontmatter) của tệp đó: `model_provider`, `model`, `reasoning`. Module này chỉ đọc/ghi đúng 3 khoá ấy,
  không đụng phần còn lại; thiếu tệp thì tự chép từ gói cài.
- Không ghi khoá API, token hay dữ liệu cá nhân ở đây.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import threading
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

SLUG = "tisa-dau-noi"
TEN = "Đạt Đấu Nối"
MUC_NO_LUC = ("off", "low", "medium", "high", "xhigh", "ultra")
MAC_DINH = {"model_provider": "anthropic-cli", "model": "claude-opus-5-5", "reasoning": "high"}
KHOA = ("model_provider", "model", "reasoning")
_RE_GT = re.compile(r"^[A-Za-z0-9._:/@+-]{1,120}$")
_khoa = threading.RLock()
ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------- tìm tệp
def _main():
    for ten in ("main", "__main__"):
        m = sys.modules.get(ten)
        if m is not None and hasattr(m, "_agents_dir"):
            return m
    return None


def thu_muc_agents() -> Path:
    """Thư mục agents của brain đang dùng (cùng cách máy chủ chính tìm)."""
    m = _main()
    if m is not None:
        try:
            return Path(m._agents_dir("brain"))
        except Exception:  # noqa: BLE001
            pass
    env = os.environ.get("TISA_AGENTS_DIR")
    if env:
        return Path(env)
    return Path.home() / "Desktop" / "agents"


def tep_agent() -> Path:
    return thu_muc_agents() / (SLUG + ".md")


def bao_dam() -> bool:
    """Có tệp cộng sự trong brain. Thiếu thì chép từ gói cài. Trả True nếu có tệp sau khi gọi."""
    t = tep_agent()
    if t.exists():
        return True
    nguon = ROOT / "suite" / "agents" / (SLUG + ".md")
    try:
        if not nguon.exists():
            return False
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(nguon, t)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------- frontmatter
def _cat(text: str):
    """Tách (khối đầu, phần thân). Khối đầu là các dòng giữa hai `---`; không có thì ([], toàn văn)."""
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, text


def _gia_tri(dong: str) -> str:
    v = dong.split(":", 1)[1].strip() if ":" in dong else ""
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def doc_cai_dat() -> dict:
    out = {"model_provider": "", "model": "", "reasoning": ""}
    try:
        text = tep_agent().read_text(encoding="utf-8")
    except OSError:
        return out
    dau, _ = _cat(text)
    for d in dau or []:
        for k in KHOA:
            if d.startswith(k + ":"):
                out[k] = _gia_tri(d)
    return out


def hop_le(model_provider: str, model: str, reasoning: str):
    """(lỗi, giá trị đã chuẩn). Rỗng cả provider lẫn model nghĩa là 'theo mặc định của TISA BOT' (xoá hai khoá)."""
    mp, md, rs = str(model_provider or "").strip(), str(model or "").strip(), str(reasoning or "").strip()
    if bool(mp) != bool(md):
        return "Chọn đủ cả nhà cung cấp và mô hình, hoặc để trống cả hai.", None
    if mp and not (_RE_GT.match(mp) and _RE_GT.match(md)):
        return "Tên nhà cung cấp hoặc mô hình có ký tự không hợp lệ.", None
    if rs and rs not in MUC_NO_LUC:
        return "Mức nỗ lực không hợp lệ.", None
    return "", {"model_provider": mp, "model": md, "reasoning": rs}


def luu_cai_dat(model_provider: str, model: str, reasoning: str) -> dict:
    loi, v = hop_le(model_provider, model, reasoning)
    if loi:
        return {"ok": False, "loi": loi}
    with _khoa:
        if not bao_dam():
            return {"ok": False, "loi": "Chưa có hồ sơ cộng sự Đạt Đấu Nối trong bộ não. Khởi động lại TISA BOT rồi thử lại."}
        t = tep_agent()
        try:
            text = t.read_text(encoding="utf-8")
        except OSError as e:
            return {"ok": False, "loi": "Không đọc được hồ sơ cộng sự: %s" % e}
        dau, than = _cat(text)
        if dau is None:
            return {"ok": False, "loi": "Hồ sơ cộng sự không có phần đầu hợp lệ."}
        moi = [d for d in dau if not any(d.startswith(k + ":") for k in KHOA)]
        # chèn trước dòng `updated:` nếu có để giữ thứ tự dễ đọc, không thì cuối khối
        pos = next((i for i, d in enumerate(moi) if d.startswith("updated:")), len(moi))
        them = []
        if v["model_provider"]:
            them.append('model: "%s"' % v["model"])
            them.append('model_provider: "%s"' % v["model_provider"])
        if v["reasoning"]:
            them.append('reasoning: "%s"' % v["reasoning"])
        moi[pos:pos] = them
        out = "---\n" + "\n".join(moi) + "\n---\n" + than
        tam = t.with_suffix(".md.tmp")
        try:
            tam.write_text(out, encoding="utf-8")
            os.replace(tam, t)
        except OSError as e:
            return {"ok": False, "loi": "Không ghi được hồ sơ cộng sự: %s" % e}
    return {"ok": True, **doc_cai_dat()}


# ---------------------------------------------------------------- trình duyệt khi đấu nối
# Anh chọn MỘT lần (hộp Cài đặt của Đạt Đấu Nối, hoặc lần đầu bấm Nhờ TISA BOT kết nối giúp): ① trình duyệt riêng chạy ngầm (làm ngay trong khung,
# anh đăng nhập trong khung), hoặc ② Chrome ngoài với MỘT hồ sơ Chrome đã đăng nhập đúng tài khoản cần nối (Google, Meta, Cloudflare...), để nối đúng tài khoản.
TEP_TD = ROOT / "server" / "trinh-duyet" / "dau-noi.json"


def doc_trinh_duyet() -> dict:
    """{"loai": "" | "rieng" | "chrome", "ho_so": thư mục hồ sơ Chrome, "ten": chữ hiển thị}. Rỗng = chưa chọn (lần đầu sẽ hỏi)."""
    try:
        d = json.loads(TEP_TD.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"loai": "", "ho_so": "", "ten": ""}
    loai = d.get("loai") if d.get("loai") in ("rieng", "chrome") else ""
    ho_so = str(d.get("ho_so") or "") if loai == "chrome" else ""
    if loai == "chrome" and not ho_so:
        loai = ""
    ten = ""
    if ho_so:
        try:
            import tisa_chong_chen as CC
            h = CC.tim_ho_so(ho_so, None)
            if not h:
                return {"loai": "", "ho_so": "", "ten": ""}        # hồ sơ Chrome đã bị xoá: coi như chưa chọn
            ten = "%s%s" % (h.get("ten") or h.get("thu_muc"), (" (" + h["email"] + ")") if h.get("email") else "")
        except Exception:  # noqa: BLE001
            pass
    return {"loai": loai, "ho_so": ho_so, "ten": ten}


def luu_trinh_duyet(loai, ho_so="") -> dict:
    loai = str(loai or "").strip()
    if loai not in ("", "rieng", "chrome"):
        return {"ok": False, "loi": "Kiểu trình duyệt không hợp lệ."}
    ho_so = str(ho_so or "").strip()
    if loai == "chrome":
        try:
            import tisa_chong_chen as CC
            h = CC.tim_ho_so(ho_so, None)
        except Exception:  # noqa: BLE001
            h = None
        if not h:
            return {"ok": False, "loi": "Không thấy hồ sơ Chrome đó trên máy. Mở lại hộp chọn để chọn hồ sơ khác."}
        ho_so = h["thu_muc"]
    else:
        ho_so = ""
    with _khoa:
        TEP_TD.parent.mkdir(parents=True, exist_ok=True)
        tmp = TEP_TD.with_suffix(".tmp")
        tmp.write_text(json.dumps({"loai": loai, "ho_so": ho_so}, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, TEP_TD)
    return {"ok": True, "trinh_duyet": doc_trinh_duyet()}


def trang_thai() -> dict:
    co = bao_dam()
    cd = doc_cai_dat() if co else {"model_provider": "", "model": "", "reasoning": ""}
    return {"ok": True, "co_ho_so": co, "slug": SLUG, "ten": TEN, "channel": "agent:" + SLUG, "cai_dat": cd, "mac_dinh": MAC_DINH,
            "muc_no_luc": list(MUC_NO_LUC), "trinh_duyet": doc_trinh_duyet()}


# ---------------------------------------------------------------- đường web
def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.get("/tisa-dau-noi/cai-dat")
    async def _lay():
        return JSONResponse(trang_thai())

    @app.post("/tisa-dau-noi/cai-dat")
    async def _dat(request: Request):
        try:
            b = await request.json()
        except Exception:  # noqa: BLE001
            b = {}
        if not isinstance(b, dict):
            b = {}
        td = b.get("trinh_duyet")
        if not any(k in b for k in KHOA) and not isinstance(td, dict):      # thân rỗng hoặc không phải JSON: không được lặng lẽ xoá cài đặt
            return JSONResponse({"ok": False, "loi": "Thiếu dữ liệu cài đặt."}, status_code=400)
        r = {"ok": True}
        if any(k in b for k in KHOA):
            r = luu_cai_dat(b.get("model_provider"), b.get("model"), b.get("reasoning"))
            if not r.get("ok"):
                return JSONResponse(r, status_code=400)
        if isinstance(td, dict):
            r2 = luu_trinh_duyet(td.get("loai"), td.get("ho_so"))
            if not r2.get("ok"):
                return JSONResponse(r2, status_code=400)
            r = {**r, **r2}
        return JSONResponse(r, status_code=200)

    @app.on_event("startup")
    async def _bat_dau():
        try:
            bao_dam()
        except Exception:  # noqa: BLE001
            pass
