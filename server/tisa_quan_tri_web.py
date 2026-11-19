"""tisa_quan_tri_web.py - Cộng sự "Quản Trị WEB" (tisa-quan-tri-web), V3.34.

Việc ở đây nhỏ: bảo đảm hồ sơ cộng sự có trong bộ não (chép từ gói cài nếu thiếu) và cho giao diện biết cộng sự có sẵn để mở cuộc chat riêng
(kênh agent:tisa-quan-tri-web). Mọi nút hỗ trợ ở trang Quản lý web được giao cho cộng sự này qua tisa-quan-tri-web.js.
Cùng cách làm với Đạt Đấu Nối (tisa_dau_noi.py), dùng lại hàm tìm thư mục agents của Đạt."""
import shutil
from pathlib import Path

SLUG = "tisa-quan-tri-web"
TEN = "Quản Trị WEB"
ROOT = Path(__file__).resolve().parent.parent


def _agents() -> Path:
    import tisa_dau_noi as DN
    return DN.thu_muc_agents()


def bao_dam() -> bool:
    t = _agents() / (SLUG + ".md")
    if t.exists():
        return True
    nguon = ROOT / "suite" / "agents" / (SLUG + ".md")
    try:
        if not nguon.exists():
            return False
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(nguon, t)
        # kỹ năng chính của cộng sự cũng phải có trong bộ não
        ks = ROOT / "suite" / "skills" / "dq-quan-tri-web"
        dich = t.parent.parent / "skills" / "dq-quan-tri-web"
        if ks.is_dir() and not dich.exists():
            shutil.copytree(ks, dich)
        return True
    except OSError:
        return False


def trang_thai() -> dict:
    return {"ok": True, "co_ho_so": bao_dam(), "slug": SLUG, "ten": TEN, "channel": "agent:" + SLUG}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.get("/tisa-quan-tri-web/trang-thai")
    async def _tt():
        return JSONResponse(trang_thai())

    @app.on_event("startup")
    async def _bat_dau():
        try:
            bao_dam()
        except Exception:  # noqa: BLE001
            pass
