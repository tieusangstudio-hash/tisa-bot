"""tisa_browser_ngoai.py - Dùng CHÍNH trình duyệt anh đang mở TISA BOT (Chrome, Edge, Brave của anh, đã đăng nhập sẵn mọi tài khoản).

Từ Chrome 144, anh tự bật một công tắc trong chrome://inspect/#remote-debugging ("Allow remote debugging for this browser instance").
Khi bật, Chrome ghi tệp DevToolsActivePort trong thư mục dữ liệu của nó (dòng 1: cổng, dòng 2: /devtools/browser/<mã>) và nghe ở 127.0.0.1.
Đã thử với Chrome 157 (17/11/2026):
  - KHÔNG có HTTP /json/list, /json/version (trả 404). Chỉ có MỘT đường websocket cấp trình duyệt.
  - Mỗi lần nối, Chrome hiện hộp hỏi anh có cho phép không; chưa bấm thì lần nối đứng chờ.
Nên ở đây giữ MỘT kết nối lâu dài (anh chỉ bấm Cho phép một lần cho tới khi đóng Chrome hoặc khởi động lại TISA BOT),
và nói chuyện với từng tab bằng Target.attachToTarget flatten (sessionId) thay cho websocket từng trang.

TISA BOT không bao giờ mở, đóng hay tắt tiến trình Chrome của anh; "Đóng" chỉ là ngắt kết nối. Mọi rào chắn (mật khẩu, OTP, thanh toán,
ngân hàng, mức duyệt) vẫn nằm ở tisa_browser.thuc_hien như với trình duyệt riêng.
"""
from __future__ import annotations

import asyncio
import json
import os
import socket
import sys
import time
from pathlib import Path

TEN = {"chrome": "Google Chrome", "edge": "Microsoft Edge", "brave": "Brave", "chromium": "Chromium"}
CHO_CHO_PHEP = 120          # giây chờ anh bấm Cho phép trên Chrome


def thu_muc(trinh: str) -> Path:
    h = Path.home()
    if sys.platform == "darwin":
        a = h / "Library" / "Application Support"
        m = {"chrome": a / "Google" / "Chrome", "edge": a / "Microsoft Edge", "brave": a / "BraveSoftware" / "Brave-Browser", "chromium": a / "Chromium"}
    elif os.name == "nt":
        la = Path(os.environ.get("LOCALAPPDATA") or (h / "AppData" / "Local"))
        m = {"chrome": la / "Google" / "Chrome" / "User Data", "edge": la / "Microsoft" / "Edge" / "User Data",
             "brave": la / "BraveSoftware" / "Brave-Browser" / "User Data", "chromium": la / "Chromium" / "User Data"}
    else:
        a = h / ".config"
        m = {"chrome": a / "google-chrome", "edge": a / "microsoft-edge", "brave": a / "BraveSoftware" / "Brave-Browser", "chromium": a / "chromium"}
    return m.get(trinh) or m["chrome"]


def co_tren_may(trinh: str) -> bool:
    return (thu_muc(trinh) / "Local State").is_file()


def doc_cong(trinh: str):
    """(cổng, đường ws) nếu anh đã bật công tắc và Chrome đang nghe; ngược lại None."""
    f = thu_muc(trinh) / "DevToolsActivePort"
    try:
        dong = f.read_text(encoding="utf-8").split()
        cong, duong = int(dong[0]), dong[1]
    except (OSError, ValueError, IndexError):
        return None
    try:
        with socket.create_connection(("127.0.0.1", cong), timeout=0.6):
            return cong, duong
    except OSError:
        return None       # tệp cũ còn sót, Chrome đã tắt hoặc anh đã tắt công tắc


class KetNoi:
    """Một kết nối lâu dài tới trình duyệt của anh."""

    def __init__(self, trinh: str):
        self.trinh = trinh
        self.ws = None
        self.id = 0
        self.cho: dict = {}
        self.trang: dict = {}          # targetId -> targetInfo (cập nhật theo sự kiện, đọc không cần chờ)
        self.dang_noi = False
        self.loi = ""
        self.luc_noi = 0.0
        self._khoa = None
        self._nghe_tv = None
        self.su_kien: dict = {}        # (V3.43) sessionId -> hàm nhận sự kiện của tab (khung trình duyệt cạnh ô chat)

    @property
    def song(self) -> bool:
        return self.ws is not None

    async def noi(self, cho: float = CHO_CHO_PHEP) -> bool:
        if self.ws is not None:
            return True
        if self._khoa is None:
            self._khoa = asyncio.Lock()
        async with self._khoa:
            if self.ws is not None:
                return True
            c = await asyncio.to_thread(doc_cong, self.trinh)
            if not c:
                self.loi = "CHUA_BAT"
                return False
            import websockets
            self.dang_noi, self.loi = True, ""
            try:
                self.ws = await websockets.connect("ws://127.0.0.1:%d%s" % c, max_size=60 * 2 ** 20, ping_interval=None, open_timeout=cho)
            except asyncio.TimeoutError:
                self.loi = "CHUA_CHO_PHEP"
                return False
            except Exception as e:  # noqa: BLE001
                self.loi = "LOI: %s" % str(e)[:160]
                return False
            finally:
                self.dang_noi = False
            self.luc_noi = time.time()
            self._nghe_tv = asyncio.create_task(self._nghe())
            try:
                await self.gui("Target.setDiscoverTargets", {"discover": True}, timeout=10)
                r = await self.gui("Target.getTargets", timeout=10)
                self.trang = {t["targetId"]: t for t in r.get("targetInfos", [])}
            except Exception as e:  # noqa: BLE001
                self.loi = "LOI: %s" % str(e)[:160]
            return self.ws is not None

    async def _nghe(self):
        try:
            async for m in self.ws:
                d = json.loads(m)
                if "id" in d:
                    f = self.cho.pop(d.get("id"), None)
                    if f and not f.done():
                        f.set_result(d)
                    continue
                me, p = d.get("method", ""), d.get("params") or {}
                if d.get("sessionId") and d["sessionId"] in self.su_kien:
                    try:
                        self.su_kien[d["sessionId"]](me, p)
                    except Exception:  # noqa: BLE001
                        pass
                    continue
                if me == "Target.detachedFromTarget" and p.get("sessionId") in self.su_kien:
                    try:
                        self.su_kien.pop(p["sessionId"])("__dong__", {})
                    except Exception:  # noqa: BLE001
                        pass
                if me in ("Target.targetCreated", "Target.targetInfoChanged"):
                    t = p.get("targetInfo") or {}
                    if t.get("targetId"):
                        self.trang[t["targetId"]] = t
                elif me == "Target.targetDestroyed":
                    self.trang.pop(p.get("targetId"), None)
        except Exception:  # noqa: BLE001
            pass
        self.ws = None
        self.trang = {}
        self.loi = self.loi or "MAT_KET_NOI"
        for f in self.cho.values():
            if not f.done():
                f.set_exception(RuntimeError("mất kết nối với trình duyệt của anh"))
        self.cho.clear()

    async def gui(self, method: str, params: dict | None = None, session: str = "", timeout: float = 20.0):
        if self.ws is None:
            raise RuntimeError("chưa nối được trình duyệt của anh")
        self.id += 1
        i = self.id
        f = asyncio.get_running_loop().create_future()
        self.cho[i] = f
        goi = {"id": i, "method": method, "params": params or {}}
        if session:
            goi["sessionId"] = session
        await self.ws.send(json.dumps(goi))
        try:
            d = await asyncio.wait_for(f, timeout)
        except asyncio.TimeoutError:
            self.cho.pop(i, None)
            raise RuntimeError("trình duyệt không trả lời (%s)" % method)
        if "error" in d:
            raise RuntimeError(str(d["error"].get("message") or d["error"])[:200])
        return d.get("result") or {}

    async def ngat(self):
        try:
            if self.ws is not None:
                await self.ws.close()
        except Exception:  # noqa: BLE001
            pass
        self.ws = None
        self.trang = {}
        self.loi = ""

    def ds_trang(self) -> list:
        """Giống /json/list của trình duyệt riêng: chỉ trang thường, không lấy trang nội bộ của Chrome."""
        out = []
        for t in self.trang.values():
            u = str(t.get("url", ""))
            if t.get("type") != "page" or u.startswith(("devtools://", "chrome-extension://", "chrome://", "edge://", "brave://", "chrome-untrusted://")):
                continue
            out.append({"id": t["targetId"], "type": "page", "url": u, "title": t.get("title", ""), "webSocketDebuggerUrl": "ngoai:%s:%s" % (self.trinh, t["targetId"])})
        return out


_KN: dict = {}


def ket_noi(trinh: str) -> KetNoi:
    trinh = trinh if trinh in TEN else "chrome"
    if trinh not in _KN:
        _KN[trinh] = KetNoi(trinh)
    return _KN[trinh]


def trang_thai(trinh: str) -> dict:
    k = ket_noi(trinh)
    if k.song:
        tt = "da_noi"
    elif k.dang_noi:
        tt = "cho_cho_phep"
    elif doc_cong(trinh):
        tt = "da_bat"          # công tắc đã bật, chưa nối (hoặc anh bấm Không cho phép)
    else:
        tt = "chua_bat"
    return {"trinh": trinh, "ten_trinh": TEN.get(trinh, trinh), "tinh_trang": tt, "co_tren_may": co_tren_may(trinh), "loi": k.loi, "so_tab": len(k.ds_trang())}


class PhienNgoai:
    """Cùng cách dùng với tisa_browser._Phien (gui, js), nhưng đi qua kết nối chung. url dạng ngoai:<trinh>:<targetId> (targetId rỗng = cấp trình duyệt)."""

    def __init__(self, url: str):
        _, self.trinh, self.tid = (url.split(":", 2) + ["", ""])[:3]
        self.k = ket_noi(self.trinh)
        self.ss = ""

    async def __aenter__(self):
        if not await self.k.noi():
            raise RuntimeError(loi_de_hieu(self.k))
        if self.tid:
            r = await self.k.gui("Target.attachToTarget", {"targetId": self.tid, "flatten": True}, timeout=15)
            self.ss = r.get("sessionId", "")
            try:       # V3.20: trang tin là đang được xem dù anh đã mở tab khác lên hoặc cửa sổ khác che (không đổi tab anh đang xem)
                await self.k.gui("Emulation.setFocusEmulationEnabled", {"enabled": True}, self.ss, 3)
            except Exception:  # noqa: BLE001
                pass
        return self

    async def __aexit__(self, *a):
        if self.ss:
            try:
                await self.k.gui("Target.detachFromTarget", {"sessionId": self.ss}, timeout=5)
            except Exception:  # noqa: BLE001
                pass

    async def gui(self, method: str, params: dict | None = None, timeout: float = 20.0):
        try:
            return await self.k.gui(method, params, self.ss, timeout)
        except RuntimeError as e:
            if "không trả lời" in str(e) and method.startswith("Runtime.") and self.ss:      # hộp thoại alert chặn trang: đóng rồi báo
                try:
                    await self.k.gui("Page.handleJavaScriptDialog", {"accept": True}, self.ss, 2)
                except Exception:  # noqa: BLE001
                    pass
            raise

    async def _gui_nhanh(self, method, params):
        try:
            await self.k.gui(method, params, self.ss, 2)
        except Exception:  # noqa: BLE001
            pass

    async def js(self, bieu_thuc: str, tham_chieu: bool = False, timeout: float = 20.0):
        r = await self.gui("Runtime.evaluate", {"expression": bieu_thuc, "returnByValue": not tham_chieu, "awaitPromise": True, "userGesture": True}, timeout)
        if r.get("exceptionDetails"):
            raise RuntimeError("lỗi trang: " + str((r["exceptionDetails"].get("exception") or {}).get("description") or r["exceptionDetails"].get("text"))[:200])
        return r["result"] if tham_chieu else (r.get("result") or {}).get("value")


def loi_de_hieu(k: KetNoi) -> str:
    ten = TEN.get(k.trinh, k.trinh)
    if k.loi == "CHUA_BAT":
        return ("CHUA_BAT_CHROME: %s của anh chưa bật cho AI điều khiển. Nhờ anh mở trang chrome://inspect/#remote-debugging trong %s, "
                "bật ô \"Allow remote debugging for this browser instance\", rồi bấm Nối ở bảng Điều khiển của AI." % (ten, ten))
    if k.loi == "CHUA_CHO_PHEP":
        return "CHUA_CHO_PHEP: %s đang hỏi anh có cho TISA BOT điều khiển không. Nhờ anh bấm \"Allow/Cho phép\" trên cửa sổ %s rồi gọi lại." % (ten, ten)
    return "KHONG_NOI_DUOC: không nối được %s của anh (%s). Nhờ anh mở lại bảng Điều khiển của AI để nối lại." % (ten, k.loi or "lỗi lạ")
