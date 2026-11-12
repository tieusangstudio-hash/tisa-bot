"""tisa_oauth_cimd.py - chọn ứng dụng OAuth (client) cho máy chủ MCP tự thêm, đúng chuẩn MCP (V2.78, chủ báo 11/11/2026).

Sự cố: nối HeyGen MCP (https://mcp.heygen.com/mcp/v1/) bị chặn ở trang đăng nhập với "Invalid redirect_uri: not
registered for this client", màn đồng ý hiện tên "HeyGen MCP Default". Nguyên nhân: đăng ký tự động (DCR) của HeyGen trả về
một client DÙNG CHUNG (client_id an1xhCM552m7m1AuY7hLlwzM) và chép lại redirect_uri của mình trong câu trả lời, nhưng không
thật sự đăng ký địa chỉ đó. TISA BOT tin câu trả lời và lưu client đó cho kết nối.

Thứ tự chọn client theo chuẩn MCP (bản 2025-11):
  (a) máy chủ đăng nhập khai `client_id_metadata_document_supported`: dùng Client ID Metadata Document. client_id chính là
      địa chỉ công khai https://<tên-miền>/oauth/client-metadata.json, tài liệu ở đó khai tên "TISA BOT" và đúng địa chỉ
      quay về. Không cần đăng ký, máy chủ đăng nhập tự đọc tài liệu.
  (b) không có (a): Dynamic Client Registration (đoạn sẵn có trong oauth_mcp.py), kết quả lưu theo từng máy chủ đăng nhập.
  (c) chỉ khi (a) và (b) đều không được: client_id chủ tự nhập trong kết nối.
Client lưu theo (máy chủ đăng nhập, địa chỉ quay về) trong STATE_DIR/.oauth_clients.json. Máy chủ báo client hỏng
(invalid_client, redirect_uri chưa đăng ký) thì bỏ client đã lưu và đăng ký lại.

(a) chỉ dùng được khi TISA BOT có tên miền https công khai: máy chủ đăng nhập phải tự tải được tài liệu metadata.
Mở bằng localhost / 127.0.0.1 thì đi (b).
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
from pathlib import Path

DUONG_TAI_LIEU = "/oauth/client-metadata.json"
DUONG_QUAY_VE = "/connect/oauth/callback"
TEN_UNG_DUNG = "TISA BOT"


def _tep_cache() -> Path:
    try:
        import config
        return Path(config.STATE_DIR) / ".oauth_clients.json"
    except Exception:  # noqa: BLE001
        return Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent) / ".oauth_clients.json"


def _doc() -> dict:
    try:
        return json.loads(_tep_cache().read_text(encoding="utf-8")) or {}
    except (OSError, ValueError):
        return {}


def _ghi(d: dict) -> None:
    p = _tep_cache()
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, p)
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def khoa_may_chu(md: dict, authorize_endpoint: str = "") -> str:
    """Khoá nhận diện máy chủ đăng nhập: issuer, thiếu thì gốc của trang xin quyền."""
    iss = str((md or {}).get("issuer") or "").strip().rstrip("/")
    if iss:
        return iss
    p = urllib.parse.urlparse(authorize_endpoint or "")
    return f"{p.scheme}://{p.netloc}" if p.netloc else ""


def _goc(redirect_uri: str) -> str:
    p = urllib.parse.urlparse(redirect_uri or "")
    return f"{p.scheme}://{p.netloc}" if p.netloc else ""


def dung_duoc_cimd(redirect_uri: str) -> bool:
    """Máy chủ đăng nhập chỉ tải được tài liệu metadata qua https từ một tên miền công khai."""
    p = urllib.parse.urlparse(redirect_uri or "")
    host = (p.hostname or "").lower()
    if p.scheme != "https" or not host:
        return False
    return not (host == "localhost" or host.endswith(".localhost") or host.startswith("127.") or host == "::1"
                or host.endswith(".local"))


def client_id_cimd(redirect_uri: str) -> str:
    return _goc(redirect_uri) + DUONG_TAI_LIEU


def tai_lieu(goc: str) -> dict:
    """Client ID Metadata Document của TISA BOT ở địa chỉ gốc `goc` (vd https://tisabot.hocvientisa.com)."""
    goc = goc.rstrip("/")
    return {
        "client_id": goc + DUONG_TAI_LIEU,
        "client_name": TEN_UNG_DUNG,
        "client_uri": goc + "/",
        "logo_uri": goc + "/brand-logo",
        "redirect_uris": [goc + DUONG_QUAY_VE],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }


def _khoa(may_chu: str, redirect_uri: str) -> str:
    return f"{may_chu}|{redirect_uri}"


def chon_client(conn_id: str, md: dict, redirect_uri: str, ent: dict, authorize_endpoint: str = "") -> tuple:
    """(client_id, nguồn) trước bước đăng ký tự động. Nguồn: "cimd", "da-luu" hoặc "" (để oauth_mcp chạy DCR)."""
    may_chu = khoa_may_chu(md, authorize_endpoint)
    c = _doc().get(_khoa(may_chu, redirect_uri)) or {}
    if md.get("client_id_metadata_document_supported") and dung_duoc_cimd(redirect_uri) and c.get("nguon") != "cimd-hong":
        cid = client_id_cimd(redirect_uri)
        luu_client(may_chu, redirect_uri, cid, "cimd")
        return cid, "cimd"
    if c.get("client_id") and c.get("nguon") not in ("cimd", "cimd-hong"):
        return c["client_id"], "da-luu"
    # Bản trước lưu client theo từng kết nối: giữ dùng tiếp nếu đúng máy chủ đăng nhập đó (không phá kết nối đang chạy),
    # trừ client dùng chung đã biết là hỏng.
    cu = str((ent or {}).get("client_id") or "")
    if cu and (ent or {}).get("token_endpoint") == md.get("token_endpoint") and not cu.startswith(("http://", "https://")):
        luu_client(may_chu, redirect_uri, cu, "dcr")
        return cu, "da-luu"
    return "", ""


def luu_client(may_chu: str, redirect_uri: str, client_id: str, nguon: str) -> None:
    if not (may_chu and client_id):
        return
    d = _doc()
    d[_khoa(may_chu, redirect_uri)] = {"client_id": client_id, "nguon": nguon, "luc": int(time.time())}
    _ghi(d)


def bo_client(may_chu: str, redirect_uri: str) -> None:
    """Máy chủ đăng nhập từ chối client đã lưu. Client từ DCR: quên để lần sau đăng ký lại. Client Metadata Document:
    đánh dấu hỏng cho máy chủ này để lần sau đi DCR, không lặp lại cùng một lỗi."""
    d = _doc()
    k = _khoa(may_chu, redirect_uri)
    cu = d.get(k) or {}
    if cu.get("nguon") == "cimd":
        d[k] = {"client_id": "", "nguon": "cimd-hong", "luc": int(time.time())}
    elif k in d:
        d.pop(k)
    else:
        return
    _ghi(d)


def la_loi_client(error: str, mo_ta: str = "") -> bool:
    """Lỗi cho thấy client đã lưu không còn dùng được: bỏ đi và đăng ký lại."""
    e, m = str(error or "").lower(), str(mo_ta or "").lower()
    if e in ("invalid_client", "unauthorized_client"):
        return True
    return e in ("invalid_request", "invalid_redirect_uri") and ("redirect" in m or "client" in m)


def gan(app) -> None:
    """Phục vụ tài liệu metadata CÔNG KHAI: máy chủ đăng nhập (HeyGen...) tải nó không có phiên đăng nhập TISA BOT."""
    from starlette.responses import JSONResponse

    @app.middleware("http")
    async def _tisa_oauth_cimd_mw(request, call_next):
        if request.url.path == DUONG_TAI_LIEU and request.method in ("GET", "HEAD"):
            import web_security
            goc = web_security.external_base(request.url.scheme, request.url.netloc,
                                             request.headers.get("x-forwarded-proto", ""),
                                             request.headers.get("x-forwarded-host", ""))
            return JSONResponse(tai_lieu(goc), headers={"cache-control": "public, max-age=3600",
                                                        "access-control-allow-origin": "*"})
        return await call_next(request)
