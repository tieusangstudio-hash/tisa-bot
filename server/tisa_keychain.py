"""tisa_keychain.py - Cất và lấy bí mật (khóa API, refresh token, mật khẩu) bằng macOS Keychain. Không ghi tệp, không in ra, không đi qua argv.

  luu(dich_vu, gia_tri)   ghi (hoặc cập nhật) mục generic-password: dich_vu + tài khoản = tên người dùng máy. Giá trị đi vào lệnh `security -i` qua STDIN
                          dạng hex (-X), nên không nằm trong danh sách tiến trình (ps) và không cần xử lý dấu nháy.
  doc(dich_vu)            trả chuỗi hoặc None. Chỉ gọi trong mã, KHÔNG bao giờ trả kết quả này cho AI.
  co(dich_vu)             có mục hay không (không lấy giá trị).
  xoa(dich_vu)            xóa mục (chỉ dùng trong kiểm thử và khi anh yêu cầu).

Tên mục của TISA BOT đều bắt đầu bằng "tisa-bot-": tisa-bot-mo-khoa (mật khẩu máy), tisa-bot-drive (JSON khóa Google Drive), tisa-bot-<dịch vụ>.
macOS: Keychain. Windows và Linux (từ V3.34): tệp STATE_DIR/tisa-kho-khoa.json, từng giá trị mã hóa bằng Fernet qua secrets_store (khóa máy .secret_key), quyền 600. Đặt TISA_KHOA_TEP=1 để buộc dùng tệp ngay cả trên Mac (kiểm thử).
"""
from __future__ import annotations

import binascii
import getpass
import json
import os
import re
import subprocess
import sys

SECURITY = "/usr/bin/security"
_TEN_HOP_LE = re.compile(r"^[a-zA-Z0-9._-]{3,80}$")


def _tk(tai_khoan: str = "") -> str:
    return tai_khoan or getpass.getuser()


def _hop_le(dich_vu: str) -> bool:
    return bool(_TEN_HOP_LE.match(str(dich_vu or "")))


def _dung_tep() -> bool:
    """Máy không có Keychain (Windows, Linux) hoặc được buộc dùng tệp mã hóa."""
    return sys.platform != "darwin" or os.environ.get("TISA_KHOA_TEP") == "1"


def _duong_tep():
    from pathlib import Path
    try:
        import config as _c
        return Path(_c.STATE_DIR) / "tisa-kho-khoa.json"
    except Exception:  # noqa: BLE001
        return Path(os.environ.get("TISA_STATE_DIR") or Path(__file__).resolve().parent) / "tisa-kho-khoa.json"


def _tep_doc() -> dict:
    try:
        d = json.loads(_duong_tep().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _tep_ghi(d: dict) -> bool:
    p = _duong_tep()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tam = p.with_suffix(".tmp")
        tam.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        try:
            os.chmod(tam, 0o600)
        except OSError:
            pass
        os.replace(tam, p)
        return True
    except OSError:
        return False


def _tep_khoa(dich_vu: str, tai_khoan: str) -> str:
    return "%s|%s" % (dich_vu, _tk(tai_khoan))


def _tep_luu(dich_vu: str, gia_tri: str, tai_khoan: str) -> bool:
    try:
        import secrets_store
        ma = secrets_store.encrypt(str(gia_tri))
    except Exception:  # noqa: BLE001
        return False
    if not ma or ma.startswith("plain:"):    # thiếu thư viện mã hóa: không cất bí mật dạng chữ thường
        return False
    d = _tep_doc()
    d[_tep_khoa(dich_vu, tai_khoan)] = ma
    return _tep_ghi(d)


def _tep_lay(dich_vu: str, tai_khoan: str):
    ma = _tep_doc().get(_tep_khoa(dich_vu, tai_khoan))
    if not ma:
        return None
    try:
        import secrets_store
        v = secrets_store.decrypt(ma)
    except Exception:  # noqa: BLE001
        return None
    return v or None


def luu(dich_vu: str, gia_tri: str, tai_khoan: str = "") -> bool:
    if not _hop_le(dich_vu) or not gia_tri:
        return False
    if _dung_tep():
        return _tep_luu(dich_vu, gia_tri, tai_khoan)
    hexs = binascii.hexlify(str(gia_tri).encode("utf-8")).decode("ascii")
    lenh = "add-generic-password -U -s %s -a %s -X %s\n" % (dich_vu, _tk(tai_khoan), hexs)
    try:
        r = subprocess.run([SECURITY, "-i"], input=lenh, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and "error" not in (r.stderr or "").lower() and co(dich_vu, tai_khoan)


def doc(dich_vu: str, tai_khoan: str = "") -> str | None:
    if not _hop_le(dich_vu):
        return None
    if _dung_tep():
        return _tep_lay(dich_vu, tai_khoan)
    try:
        r = subprocess.run([SECURITY, "find-generic-password", "-s", dich_vu, "-a", _tk(tai_khoan), "-w"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    v = (r.stdout or "").rstrip("\n")
    if v and re.fullmatch(r"[0-9a-fA-F]+", v) and len(v) % 2 == 0 and not re.fullmatch(r"[0-9]+", v):
        # `security -w` in dạng hex khi dữ liệu có ký tự không in được (xuống dòng, tiếng Việt...): giải ngược nếu ra UTF-8 hợp lệ.
        try:
            g = binascii.unhexlify(v).decode("utf-8")
            if any(ord(c) < 32 or ord(c) > 126 for c in g):
                return g
        except (binascii.Error, UnicodeDecodeError):
            pass
    return v or None


def co(dich_vu: str, tai_khoan: str = "") -> bool:
    if not _hop_le(dich_vu):
        return False
    if _dung_tep():
        return _tep_khoa(dich_vu, tai_khoan) in _tep_doc()
    try:
        r = subprocess.run([SECURITY, "find-generic-password", "-s", dich_vu, "-a", _tk(tai_khoan)], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def xoa(dich_vu: str, tai_khoan: str = "") -> bool:
    if not _hop_le(dich_vu):
        return False
    if _dung_tep():
        d = _tep_doc()
        if d.pop(_tep_khoa(dich_vu, tai_khoan), None) is None:
            return False
        return _tep_ghi(d)
    try:
        r = subprocess.run([SECURITY, "delete-generic-password", "-s", dich_vu, "-a", _tk(tai_khoan)], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
