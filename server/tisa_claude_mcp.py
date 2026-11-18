"""tisa_claude_mcp.py - Nối MCP của CLAUDE CODE vào TISA BOT, mặc định, kèm thẻ báo "đã kết nối" ở trang Kết nối (chủ yêu cầu 18/11/2026).

Chủ: "anh đã kết nối cổng MCP quảng cáo Facebook bên Claude Code rồi; muốn TISA BOT tự dùng MCP đó để báo cáo, xem số liệu, lên chiến dịch, tắt bật cam. Kết nối qua
API và MCP trên TISA BOT thì phức tạp quá. Mặc định luôn: máy đang dùng Claude Code gắn vào TISA BOT thì tự dùng được MCP luôn, và hiện ra để biết đã nối thành công."

Cách hoạt động (không cấu hình gì thêm):
- Engine Claude của TISA BOT chạy bằng Claude Code (claude-agent-sdk). Khi cài đặt `mcp.strict` = False (mặc định), nó nạp luôn MCP mà Claude Code của máy đang có: MCP tự
  thêm (`claude mcp add`, ~/.claude.json, .mcp.json) và các kết nối đồng bộ từ tài khoản claude.ai (Meta Ads, Google Drive, Canva...). Module này:
  1. ép `mcp.strict` về False MỘT LẦN khi chưa từng làm (nếu ai đó đã bật chặn thì chỉ gỡ lần đầu; anh bật lại sau đó thì giữ);
  2. định kỳ chạy `claude mcp list` (có kiểm sức khoẻ, hơi lâu) ở luồng nền rồi cất kết quả, để trang Kết nối hiện ngay;
  3. nhận ra kết nối Meta Ads (Facebook Ads) để báo riêng, và dặn AI dùng nó (xem tisa_cong_cu_ai.KHOI).
Giới hạn nói thẳng: chỉ engine CLAUDE dùng được (ChatGPT/Codex có kho MCP riêng). Kết nối cần đăng nhập lại (Needs authentication) thì báo để anh vào Claude Code đăng nhập.
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

TUOI_TOI_DA = 600           # giây: quá hạn này thì quét lại nền
_khoa = threading.RLock()
_dang_quet = {"v": False}
_RE_QC = re.compile(r"meta\s*ads|facebook\s*ads|mcp\.facebook\.com/ads", re.I)


def _thu_muc() -> Path:
    try:
        import config as _cfg
        d = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        d = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tep_cache() -> Path:
    return _thu_muc() / "claude-mcp-cache.json"


def _tep_dau() -> Path:
    return _thu_muc() / "claude-mcp-mac-dinh.json"


# ---------------------------------------------------------------- phân loại
def phan_loai(s: dict) -> dict:
    """Từ một dòng của `claude mcp list` -> thẻ gọn để hiển thị."""
    ten = str(s.get("name") or "")
    kieu = "claude.ai" if ten.lower().startswith("claude.ai ") else "may"
    ten_ngan = ten[len("claude.ai "):].strip() if kieu == "claude.ai" else ten
    tt = str(s.get("status") or "")
    low = tt.lower()
    if s.get("connected"):
        trang_thai = "ok"
    elif "authentication" in low or "needs auth" in low:
        trang_thai = "can_dang_nhap"
    else:
        trang_thai = "loi"
    chi_tiet = "" if trang_thai == "ok" else re.sub(r"^[^\w]+", "", tt)[:160]
    return {"ten": ten_ngan, "nguon": kieu, "trang_thai": trang_thai, "chi_tiet": chi_tiet, "dia_chi": str(s.get("url") or "")[:120],
            "quang_cao": bool(_RE_QC.search(ten) or _RE_QC.search(str(s.get("url") or "")))}


def tom_tat(ds: list) -> dict:
    ok = [x for x in ds if x["trang_thai"] == "ok"]
    qc = [x for x in ds if x["quang_cao"]]
    return {"tong": len(ds), "ket_noi_tot": len(ok), "can_dang_nhap": [x["ten"] for x in ds if x["trang_thai"] == "can_dang_nhap"],
            "loi": [x["ten"] for x in ds if x["trang_thai"] == "loi"],
            "meta_ads": ({"co": True, "ok": any(x["trang_thai"] == "ok" for x in qc), "ten": qc[0]["ten"], "trang_thai": qc[0]["trang_thai"]} if qc else {"co": False, "ok": False})}


# ---------------------------------------------------------------- quét
def _doc_cache() -> dict:
    try:
        return json.loads(_tep_cache().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _engine_hien_tai() -> str:
    try:
        import config as _cfg
        st = _cfg.read_settings()
        return str(((st.get("model") or {}).get("main") or {}).get("provider") or "")
    except Exception:  # noqa: BLE001
        return ""


def quet_thuc() -> dict:
    """Chạy `claude mcp list` (chặn tới 60 giây, kèm kiểm sức khoẻ từng kết nối). Gọi trong luồng nền, không gọi trên vòng sự kiện."""
    try:
        import claude_cli
        cli = claude_cli.find_claude_cli()
        ds = [phan_loai(s) for s in claude_cli.mcp_native_list()] if cli else []
    except Exception as e:  # noqa: BLE001
        return {"co_claude": False, "loi": "%s: %s" % (type(e).__name__, str(e)[:100]), "may_chu": [], "luc": time.time(), "tom_tat": tom_tat([])}
    kq = {"co_claude": bool(cli), "may_chu": ds, "luc": time.time(), "tom_tat": tom_tat(ds)}
    try:
        _tep_cache().write_text(json.dumps(kq, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return kq


def quet_nen(ep: bool = False) -> bool:
    """Bắt đầu quét ở luồng nền nếu chưa quét hoặc dữ liệu quá cũ. True nếu đã bắt đầu."""
    with _khoa:
        if _dang_quet["v"]:
            return False
        c = _doc_cache()
        if not ep and c and time.time() - float(c.get("luc") or 0) < TUOI_TOI_DA:
            return False
        _dang_quet["v"] = True

    def chay():
        try:
            quet_thuc()
        finally:
            with _khoa:
                _dang_quet["v"] = False
    threading.Thread(target=chay, name="tisa-claude-mcp", daemon=True).start()
    return True


def trang_thai(quet: bool = False) -> dict:
    c = _doc_cache()
    bat = quet_nen(ep=quet)
    with _khoa:
        dang = _dang_quet["v"]
    ep = _engine_hien_tai()
    return {"ok": True, "co_du_lieu": bool(c), "dang_quet": bool(dang or bat), "tuoi_giay": int(time.time() - float(c.get("luc") or time.time())) if c else None,
            "co_claude": bool(c.get("co_claude")) if c else None, "may_chu": c.get("may_chu") or [], "tom_tat": c.get("tom_tat") or tom_tat([]),
            "engine": ep, "engine_la_claude": ep in ("", "anthropic-cli"), "loi": c.get("loi", "")}


# ---------------------------------------------------------------- mặc định bật
def bat_mac_dinh() -> dict:
    """Đặt `mcp.strict` = False một lần (không chặn MCP sẵn có của Claude Code). Có dấu thì không làm lại: anh bật chặn sau đó thì giữ."""
    dau = _tep_dau()
    if dau.exists():
        return {"lam": False}
    try:
        import config as _cfg
        st = _cfg.read_settings()
        mcp = st.setdefault("mcp", {})
        da_doi = bool(mcp.get("strict"))
        if da_doi:
            mcp["strict"] = False
            _cfg.write_settings(st)
        dau.write_text(json.dumps({"luc": time.time(), "da_doi_strict": da_doi}), encoding="utf-8")
        return {"lam": True, "da_doi_strict": da_doi}
    except Exception as e:  # noqa: BLE001
        return {"lam": False, "loi": "%s: %s" % (type(e).__name__, str(e)[:80])}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.get("/tisa-claude-mcp/trang-thai")
    async def _tt(request: Request):
        quet = str(request.query_params.get("quet") or "") in ("1", "true")
        return JSONResponse(trang_thai(quet))

    @app.post("/tisa-claude-mcp/quet")
    async def _quet():
        return JSONResponse(trang_thai(True))

    @app.on_event("startup")
    async def _bat_dau():
        if os.environ.get("TISA_BO_QUA_CLAUDE_MCP") == "1":
            return
        try:
            bat_mac_dinh()
        except Exception:  # noqa: BLE001
            pass

        async def vong():
            await asyncio.sleep(20)
            while True:
                try:
                    quet_nen()
                except Exception:  # noqa: BLE001
                    pass
                await asyncio.sleep(TUOI_TOI_DA)
        asyncio.get_event_loop().create_task(vong())
