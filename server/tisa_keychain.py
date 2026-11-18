"""tisa_keychain.py - Cất và lấy bí mật (khóa API, refresh token, mật khẩu) bằng macOS Keychain. Không ghi tệp, không in ra, không đi qua argv.

  luu(dich_vu, gia_tri)   ghi (hoặc cập nhật) mục generic-password: dich_vu + tài khoản = tên người dùng máy. Giá trị đi vào lệnh `security -i` qua STDIN
                          dạng hex (-X), nên không nằm trong danh sách tiến trình (ps) và không cần xử lý dấu nháy.
  doc(dich_vu)            trả chuỗi hoặc None. Chỉ gọi trong mã, KHÔNG bao giờ trả kết quả này cho AI.
  co(dich_vu)             có mục hay không (không lấy giá trị).
  xoa(dich_vu)            xóa mục (chỉ dùng trong kiểm thử và khi anh yêu cầu).

Tên mục của TISA BOT đều bắt đầu bằng "tisa-bot-": tisa-bot-mo-khoa (mật khẩu máy), tisa-bot-drive (JSON khóa Google Drive), tisa-bot-<dịch vụ>.
Chỉ macOS. Windows: chưa làm (dùng Credential Manager sau).
"""
from __future__ import annotations

import binascii
import getpass
import re
import subprocess
import sys

SECURITY = "/usr/bin/security"
_TEN_HOP_LE = re.compile(r"^[a-zA-Z0-9._-]{3,80}$")


def _tk(tai_khoan: str = "") -> str:
    return tai_khoan or getpass.getuser()


def _hop_le(dich_vu: str) -> bool:
    return bool(_TEN_HOP_LE.match(str(dich_vu or "")))


def luu(dich_vu: str, gia_tri: str, tai_khoan: str = "") -> bool:
    if sys.platform != "darwin" or not _hop_le(dich_vu) or not gia_tri:
        return False
    hexs = binascii.hexlify(str(gia_tri).encode("utf-8")).decode("ascii")
    lenh = "add-generic-password -U -s %s -a %s -X %s\n" % (dich_vu, _tk(tai_khoan), hexs)
    try:
        r = subprocess.run([SECURITY, "-i"], input=lenh, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and "error" not in (r.stderr or "").lower() and co(dich_vu, tai_khoan)


def doc(dich_vu: str, tai_khoan: str = "") -> str | None:
    if sys.platform != "darwin" or not _hop_le(dich_vu):
        return None
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
    if sys.platform != "darwin" or not _hop_le(dich_vu):
        return False
    try:
        r = subprocess.run([SECURITY, "find-generic-password", "-s", dich_vu, "-a", _tk(tai_khoan)], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def xoa(dich_vu: str, tai_khoan: str = "") -> bool:
    if sys.platform != "darwin" or not _hop_le(dich_vu):
        return False
    try:
        r = subprocess.run([SECURITY, "delete-generic-password", "-s", dich_vu, "-a", _tk(tai_khoan)], capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
