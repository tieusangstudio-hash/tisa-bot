"""Xếp hàng đúng LÚC LÀM MỚI token Claude - chống hai lượt chat đá nhau văng đăng nhập.

Bệnh (chủ repo báo 02/09, hai vợ chồng dùng chung một tisa)
------------------------------------------------------------
TISA BOT chạy NHIỀU tiến trình `claude` song song (xem `_ACTIVE_PROCS` ở claude_cli, và
`_ACTIVE` ở claude_sdk_engine) mà không có gì xếp hàng chúng lại. Cả đám dùng chung ĐÚNG MỘT
file `~/.claude/.credentials.json`.

Refresh token OAuth là loại DÙNG MỘT LẦN: máy chủ tiêu nó rồi trả về một cặp mới. Nên khi
access token hết hạn đúng lúc hai người đang cùng chat:

  - lượt A làm mới trước  -> tiêu mất refresh token cũ, ghi cặp mới xuống file, chạy tiếp;
  - lượt B vẫn cầm refresh token CŨ (đọc từ trước) -> máy chủ trả
    "refresh token was already used. Please log out and sign in again".

Ai thua thì lượt đó hỏng, còn FILE VẪN LÀNH nên người kia không thấy gì. Đúng cái hình
"vợ bị văng, chồng dùng bình thường".

Vì sao vệ sĩ credentials (claude_cli.giu_credentials) không cứu được: nó lo file HỎNG hoặc
MẤT. Ở đây file lành tuyệt đối - chỉ có một cái token bị tiêu trước. Và nó quét 5 phút một
lần, quá chậm so với một cuộc đua tính bằng mili giây.

Cách chặn
---------
Chỉ xếp hàng trong ĐÚNG cửa sổ hẹp lúc token sắp/đã hết hạn (đọc `expiresAt` ngay trong file,
không đụng tới chính token - cùng cách connect_health đang làm). Ngoài cửa sổ đó thì hàm này
trả về ngay, không tốn gì. Trong cửa sổ: người đầu tiên đi luôn, người tới sau chờ tới khi
`expiresAt` nhích lên rồi mới chạy, tức là đã cầm token mới.

KHÔNG dùng khoá giữ suốt lượt: một lượt chat có thể chạy vài phút, giữ khoá cả lượt là biến
hai người thành xếp hàng nối đuôi. Ở đây chỉ giữ một MỐC THỜI GIAN tự hết hạn, nên không có
đường nào kẹt vĩnh viễn: kẹt xấu nhất là mọi lượt chờ thêm vài giây rồi vẫn chạy.

macOS cất token trong Keychain, không có file. Trước 28/11/2026 `han_token()` vì thế trả 0 và
trên Mac KHÔNG xếp hàng gì cả - đúng ca chủ báo "tắt mở máy là văng kết nối Claude Code": máy
tắt qua đêm thì access token hết hạn, bật lên là cả loạt tiến trình `claude` (lượt chat, việc
nền, mở sẵn, giọng nói) cùng làm mới một lúc, đứa thua cầm refresh token đã bị tiêu. Nay đọc
`expiresAt` trong Keychain (chỉ đọc, qua lệnh `security` y như connect_health), có nhớ đệm để
không gọi `security` mỗi lượt khi token còn xa hạn.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

# Coi là "sắp hết hạn" khi hạn còn dưới ngần này. Rộng hơn thời gian một lượt khởi động
# `claude` để cuộc đua bị bắt TRƯỚC khi nó xảy ra, chứ không phải sau.
CHUAN_BI_S = 120.0
# Người tới sau chờ tối đa ngần này rồi vẫn chạy. Thà chịu rủi ro đua còn hơn treo lượt chat.
CHO_TOI_DA_S = 30.0
# Mốc "đang có người đi trước" tự hết hạn sau ngần này, kể cả khi lượt đó chết giữa chừng.
GIU_TOI_DA_S = 25.0
NHIP_S = 0.4

_KHOA_BIEN = threading.Lock()
_MOC_DI_TRUOC = 0.0


def duong_cred() -> Path:
    home = os.environ.get("HOME") or os.path.expanduser("~")
    return Path(home) / ".claude" / ".credentials.json"


_KC_DICH_VU = "Claude Code-credentials"
_KC_NHO = {"het": 0.0, "oa": None}       # nhớ đệm đọc Keychain: hết hạn lúc nào, phần claudeAiOauth đọc được
_KC_KHOA = threading.Lock()


def _oa_keychain() -> dict | None:
    """macOS: phần `claudeAiOauth` Claude Code cất trong Keychain. None = không có / không đọc được.

    Chỉ đọc. Nhớ đệm: token còn xa hạn thì nhớ tới lúc gần vào cửa sổ (tối đa 60 giây), gần hạn thì
    chỉ nhớ 1 giây để vòng chờ trong `xep_hang` thấy ngay cặp mới. Không đọc được thì nhớ 30 giây
    (máy không cho đọc thì gọi lại liên tục cũng vô ích).
    """
    if sys.platform != "darwin":
        return None
    now = time.time()
    with _KC_KHOA:
        if now < _KC_NHO["het"]:
            return _KC_NHO["oa"]
    oa = None
    try:
        r = subprocess.run(["security", "find-generic-password", "-s", _KC_DICH_VU, "-w"],
                           capture_output=True, text=True, timeout=3)
        if r.returncode == 0:
            oa = (json.loads(r.stdout.strip() or "{}") or {}).get("claudeAiOauth") or None
    except Exception:  # noqa: BLE001 - đọc không được thì như chưa có, giữ hành vi cũ
        oa = None
    if isinstance(oa, dict):
        try:
            exp = float(oa.get("expiresAt") or 0) / 1000.0
        except (TypeError, ValueError):
            exp = 0.0
        con = exp - now - CHUAN_BI_S
        giu = min(60.0, con - 5.0) if con > 6.0 else 1.0
    else:
        oa, giu = None, 30.0
    with _KC_KHOA:
        _KC_NHO["oa"], _KC_NHO["het"] = oa, now + giu
    return oa


def _oa() -> dict | None:
    """Phần claudeAiOauth: file ~/.claude/.credentials.json (Windows, Linux), rơi về Keychain trên macOS."""
    try:
        oa = (json.loads(duong_cred().read_text(encoding="utf-8")) or {}).get("claudeAiOauth")
        if isinstance(oa, dict):
            return oa
    except FileNotFoundError:
        pass
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return _oa_keychain()


def han_token() -> float:
    """Hạn của access token, tính bằng epoch GIÂY. 0.0 = không đọc được / chưa đăng nhập.

    Chỉ đọc MỖI trường `expiresAt`, không đụng tới accessToken/refreshToken và không gửi
    chúng đi đâu - đúng ranh giới mà connect_health đã đặt sẵn.
    """
    oa = _oa() or {}
    try:
        exp = float(oa.get("expiresAt") or 0)
    except (TypeError, ValueError):
        return 0.0
    # Ghi bằng mili giây (13 chữ số). Chia cho 1000 để về giây.
    return exp / 1000.0 if exp > 0 else 0.0


def la_loi_tranh_lam_moi(text: str) -> bool:
    """Câu lỗi này có phải DẤU VẾT CUỘC ĐUA không - phân biệt với mất đăng nhập THẬT.

    Mốc nhận dạng là "already used": nó nói refresh token bị TIÊU TRƯỚC bởi một lượt khác,
    tức phiên đăng nhập vẫn còn nguyên. Cố ý KHÔNG nhận theo "could not be refreshed" trơn:
    câu đó cũng là câu của phiên hết hạn THẬT (vụ Claude 27/07), mà bắt nhầm ca đó thành
    "chạy lại là được" là giấu mất một lỗi người dùng buộc phải xử lý.
    """
    return "already used" in (text or "").lower() or la_loi_tho_tranh_lam_moi(text)


_DUA_TOKEN_THO = "failed to refresh oauth token: another claude code process is refreshing"


def la_loi_tho_tranh_lam_moi(text: str) -> bool:
    """Câu này có phải CHÍNH thông báo lỗi thô của Claude Code bản mới về cuộc đua làm mới token không (pilot Resonance
    lần 4, 08/10/2026): toàn bộ kết quả MỞ ĐẦU bằng "Failed to refresh OAuth token: another Claude Code process is
    refreshing". Neo ở đầu chứ không tìm chuỗi con: một câu trả lời đang GIẢI THÍCH hay trích lỗi đó, hay câu thường có
    chữ OAuth/refresh, không bị nhận (review sửa pilot 4, P2-1). Siết khuôn không phải bằng chứng hoàn hảo về nguồn văn
    bản; tín hiệu chính vẫn là is_error có cấu trúc của CLI."""
    return (text or "").lstrip().lower().startswith(_DUA_TOKEN_THO)


def con_dang_nhap() -> bool:
    """Còn token không (file, hoặc Keychain trên macOS) - để phân biệt "đua nhau" với "mất đăng nhập thật"."""
    oa = _oa() or {}
    return bool(oa.get("accessToken") or oa.get("refreshToken"))


async def xep_hang() -> str:
    """Gọi ngay trước khi khởi chạy một tiến trình `claude`.

    Trả nhãn để test và log đọc được: "" (ngoài cửa sổ, không làm gì) | "di-truoc" |
    "cho" (đã có token mới, hoặc người đi trước hết lượt giữ) | "het-gio".
    """
    global _MOC_DI_TRUOC
    # Trên macOS đọc Keychain là một lệnh `security` (thường vài chục ms, có nhớ đệm): chạy ở luồng phụ
    # để không chặn vòng sự kiện.
    han = await asyncio.to_thread(han_token)
    if han <= 0:
        return ""                                   # không đọc được hạn -> giữ nguyên hành vi cũ
    if han - time.time() > CHUAN_BI_S:
        return ""                                   # đường nhanh: token còn tốt, không tốn gì
    with _KHOA_BIEN:
        di_truoc = (time.time() - _MOC_DI_TRUOC) >= GIU_TOI_DA_S
        if di_truoc:
            _MOC_DI_TRUOC = time.time()
    if di_truoc:
        return "di-truoc"
    het = time.time() + CHO_TOI_DA_S
    while time.time() < het:
        await asyncio.sleep(NHIP_S)
        if await asyncio.to_thread(han_token) > han:
            return "cho"                            # người đi trước đã ghi cặp mới -> đi thôi
        with _KHOA_BIEN:
            if (time.time() - _MOC_DI_TRUOC) >= GIU_TOI_DA_S:
                return "cho"                        # lượt đi trước chết giữa chừng, không chờ nữa
    return "het-gio"
