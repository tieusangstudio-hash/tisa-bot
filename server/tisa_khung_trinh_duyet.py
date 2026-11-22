"""Khung trình duyệt cạnh ô chat (V3.43, chủ yêu cầu 22/11/2026).

Anh mở một khung bên phải ô chat, thấy TRỰC TIẾP trình duyệt mà AI đang dùng (cùng hồ sơ, cùng tab) và tự bấm, gõ, đăng nhập
ngay trong khung, ở bất kỳ máy nào đang mở TISA BOT (kể cả qua tên miền). Giao việc ở ô chat bên trái, AI làm trong đúng tab đó.

Cách chạy: một WebSocket /trinh-duyet/khung/ws. Máy chủ nối DevTools vào tab, bật Page.startScreencast và gửi từng khung hình
(JPEG, base64) lên trình duyệt của anh; cú bấm, cuộn, phím, chữ anh gõ đi ngược lại thành Input.dispatchMouseEvent / insertText.
Không ghi lại phím hay chữ anh gõ ở đâu cả (mật khẩu đi thẳng vào trang).

Hai loại trình duyệt của tisa_browser đều dùng được:
  - trình duyệt riêng của TISA (cổng DevTools riêng): nối thẳng WebSocket của tab;
  - Chrome anh đang dùng (tisa_browser_ngoai, một kết nối chung): Target.attachToTarget rồi nghe sự kiện theo sessionId.
"""
from __future__ import annotations

import asyncio
import base64
import json
import re
import time
import urllib.parse

import tisa_browser as B

try:
    from fastapi import Request
except ImportError:  # pragma: no cover
    Request = None

try:      # PHẢI ở cấp mô-đun: có `from __future__ import annotations` thì FastAPI đọc kiểu `ws: WebSocket` theo tên trong mô-đun;
    from fastapi import WebSocket      # để trong gan() là FastAPI coi ws là tham số query, bắt tay WebSocket bị trả 403.
except ImportError:  # pragma: no cover
    WebSocket = None

CHAT_LUONG = 60          # JPEG
TOI_DA_CANH = 1600       # px khung hình gửi lên, giữ băng thông vừa phải khi xem qua mạng
_CHU_CO = {}             # mã tab -> khung đang đặt cỡ cho tab đó: mở khung ở 2 cửa sổ cùng lúc thì chỉ một khung đặt cỡ, không giành nhau (trang co giãn liên tục, nháy)
KHONG_KHUNG_THI_CHUP = 1.4   # giây không có khung screencast (cửa sổ bị che, tab nền) thì tự chụp bù


# ------------------------------------------------------------------ hai kiểu kết nối tới MỘT tab
class _KetRieng:
    """Trình duyệt riêng của TISA: một WebSocket thẳng tới tab, có nhận sự kiện."""

    def __init__(self, ws_url: str, nghe):
        self.url, self.nghe = ws_url, nghe
        self.ws, self.id, self.cho, self.tv = None, 0, {}, None

    async def mo(self):
        import websockets
        self.ws = await websockets.connect(self.url, max_size=60 * 2 ** 20, ping_interval=None, open_timeout=8)
        self.tv = asyncio.create_task(self._nghe())

    async def _nghe(self):
        try:
            async for m in self.ws:
                d = json.loads(m)
                if "id" in d:
                    f = self.cho.pop(d["id"], None)
                    if f and not f.done():
                        f.set_result(d)
                elif d.get("method"):
                    self.nghe(d["method"], d.get("params") or {})
        except Exception:  # noqa: BLE001
            pass
        for f in self.cho.values():
            if not f.done():
                f.set_exception(RuntimeError("mất kết nối tab"))
        self.cho.clear()
        self.nghe("__dong__", {})

    async def gui(self, method: str, params: dict | None = None, timeout: float = 10.0):
        if self.ws is None:
            raise RuntimeError("chưa nối tab")
        self.id += 1
        i = self.id
        f = asyncio.get_running_loop().create_future()
        self.cho[i] = f
        await self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        try:
            d = await asyncio.wait_for(f, timeout)
        except asyncio.TimeoutError:
            self.cho.pop(i, None)
            raise RuntimeError("tab không trả lời (%s)" % method)
        if "error" in d:
            raise RuntimeError(str(d["error"].get("message") or d["error"])[:200])
        return d.get("result") or {}

    async def dong(self):
        # Hủy ngay mọi lệnh đang chờ: hủy vòng nghe thì phần dọn ở cuối _nghe không chạy, lệnh chờ tab cũ (chụp màn hình) sẽ treo
        # tới hết hạn và làm khung đứng hình khi anh đổi tab.
        for f in self.cho.values():
            if not f.done():
                f.set_exception(RuntimeError("đã ngắt tab"))
        self.cho.clear()
        try:
            if self.tv:
                self.tv.cancel()
            if self.ws:
                await self.ws.close()
        except Exception:  # noqa: BLE001
            pass
        self.ws = None


class _KetNgoai:
    """Chrome anh đang dùng: đi qua kết nối chung của tisa_browser_ngoai, gắn vào tab bằng phiên flatten."""

    def __init__(self, trinh: str, tid: str, nghe):
        import tisa_browser_ngoai as N
        self.k = N.ket_noi(trinh)
        self.tid, self.nghe, self.ss = tid, nghe, ""

    async def mo(self):
        import tisa_browser_ngoai as N
        if not await self.k.noi():
            raise RuntimeError(N.loi_de_hieu(self.k))
        r = await self.k.gui("Target.attachToTarget", {"targetId": self.tid, "flatten": True}, timeout=15)
        self.ss = r.get("sessionId", "")
        self.chet = False
        self.k.su_kien[self.ss] = self._nhan

    def _nhan(self, me, p):
        if me == "__dong__":
            self.chet = True
        self.nghe(me, p)

    async def gui(self, method: str, params: dict | None = None, timeout: float = 10.0):
        return await self.k.gui(method, params, self.ss, timeout)

    async def dong(self):
        if self.ss:
            self.k.su_kien.pop(self.ss, None)
            try:
                await self.k.gui("Target.detachFromTarget", {"sessionId": self.ss}, timeout=5)
            except Exception:  # noqa: BLE001
                pass
        self.ss = ""


# ------------------------------------------------------------------ chữ anh gõ ở ô địa chỉ
def chuan_dia_chi(s: str) -> str:
    """Ô địa chỉ: có http thì giữ; trông như tên miền thì thêm https://; còn lại là tìm trên Google. Chặn javascript:, file:, chrome:."""
    s = (s or "").strip()
    if not s:
        return ""
    if re.match(r"^https?://", s, re.I):
        return s
    if re.match(r"^(javascript|file|data|chrome|devtools|about|view-source):", s, re.I):
        return "about:blank" if s.lower() == "about:blank" else ""
    if " " not in s and re.match(r"^(localhost(:\d+)?|[\w-]+(\.[\w-]+)+)(:\d+)?([/?#].*)?$", s):
        return "https://" + s
    return "https://www.google.com/search?q=" + urllib.parse.quote(s)


_LENH = {"a": "selectAll", "z": "undo", "x": "cut", "c": "copy"}
_MA_PHIM = {"Enter": 13, "Backspace": 8, "Tab": 9, "Escape": 27, "Delete": 46, "ArrowLeft": 37, "ArrowUp": 38, "ArrowRight": 39, "ArrowDown": 40,
            "Home": 36, "End": 35, "PageUp": 33, "PageDown": 34, " ": 32}


def lenh_phim(kieu: str, key: str, code: str, ma: int, mods: int) -> list:
    """Đổi một phím đặc biệt (Enter, xóa, mũi tên, phím tắt ⌘/Ctrl) thành các lệnh Input.dispatchKeyEvent. Chữ thường KHÔNG qua đây (đi insertText)."""
    ma = int(ma or _MA_PHIM.get(key, 0))
    goc = {"key": key, "code": code or "", "windowsVirtualKeyCode": ma, "nativeVirtualKeyCode": ma, "modifiers": int(mods or 0)}
    if kieu == "up":
        return [dict(goc, type="keyUp")]
    if key == "Enter" and not (mods & (2 | 4)):
        return [dict(goc, type="keyDown", text="\r", unmodifiedText="\r")]
    if (mods & (2 | 4)) and len(key) == 1:          # ⌘A, ⌘Z, ⌘X trên Mac không tự chạy qua phím giả: phải kèm lệnh soạn thảo
        lenh = _LENH.get(key.lower())
        if key.lower() == "z" and mods & 8:
            lenh = "redo"
        return [dict(goc, type="rawKeyDown", **({"commands": [lenh]} if lenh else {}))]
    return [dict(goc, type="rawKeyDown")]


# ------------------------------------------------------------------ (V3.44) tab Chrome đang ở trước trên máy chủ
def _chat_dung_may(chat: str) -> bool:
    try:
        import tisa_desktop as TD
        return TD.chat_vua_dung_may(chat, 90)
    except Exception:  # noqa: BLE001
        return False


def khop_tieu_de(tieu_de_cua_so: str, trang: list) -> str:
    """Cửa sổ Chrome có tiêu đề "<tiêu đề tab đang xem> - Google Chrome - <hồ sơ>". Trả mã tab khớp dài nhất, hoặc ""."""
    def gon(v):          # "(5) Chợ Fujifilm | Facebook": số thông báo trong ngoặc đổi liên tục, bỏ đi khi so
        return re.sub(r"^\(\d+\+?\)\s*", "", str(v or "").strip())
    t = gon(tieu_de_cua_so)
    tot, dai = "", 0
    for x in trang:
        tt = gon(x.get("title"))
        if len(tt) > dai and (t == tt or t.startswith(tt + " - ") or t.startswith(tt + " – ")):
            tot, dai = x["id"], len(tt)
    return tot


def tab_truoc_chrome(hs: str) -> str:
    """Mã tab đang hiện ở cửa sổ Chrome nằm TRƯỚC nhất trên màn hình máy chủ (cửa sổ bot vừa bấm, gõ)."""
    try:
        import tisa_browser_ngoai as N
        import tisa_chuot_rieng as CR
    except Exception:  # noqa: BLE001
        return ""
    trinh = B._ngoai(hs) or "chrome"
    ten = N.TEN.get(trinh, "Google Chrome")
    trang = B._trang_dang_co(hs)
    if not trang:
        return ""
    for w in CR.liet_ke_cua_so():
        if w.get("ung_dung") == ten and w.get("lop") == 0 and w.get("w", 0) > 200 and w.get("h", 0) > 200:
            tid = khop_tieu_de(w.get("tieu_de") or "", trang)
            if tid:
                return tid
            if w.get("tieu_de"):
                break          # cửa sổ Chrome trước nhất có tiêu đề nhưng không khớp tab nào: đừng đoán cửa sổ sau
    return ""


# ------------------------------------------------------------------ một phiên xem của một khung
class Khung:
    def __init__(self, gui_len, hs: str, chat: str = ""):
        self.gui_len = gui_len          # async fn(dict) gửi lên khung của anh
        self.hs = hs
        self.chat = chat                # mã phiên ô chat: khung chỉ thấy và điều khiển tab của ô chat này
        self.ket = None
        self.tab = ""
        self.w, self.h, self.dpr = 0, 0, 1.0
        self.vua = True                  # Vừa khung: trang dàn theo đúng bề rộng khung
        self.khung_moi = None            # (data, meta) mới nhất chưa gửi
        self.co_khung = asyncio.Event()
        self.luc_khung = 0.0
        self.luc_bam = 0.0
        self.dong_roi = False
        self.dang_chup = None
        self.cho_ai = False             # khung tự mở để xem AI làm: không tự mở tab, không gắn trình duyệt
        self.luc_chon = 0.0
        self.da_dua_len = False
        self.thong_tin = {}

    # ---- sự kiện từ tab
    def _su_kien(self, me: str, p: dict):
        if me == "Page.screencastFrame":
            m = p.get("metadata") or {}
            self.khung_moi = (p.get("data", ""), {"w": m.get("deviceWidth"), "h": m.get("deviceHeight"), "top": m.get("offsetTop", 0)})
            self.luc_khung = time.time()
            self.co_khung.set()
            if self.ket:
                asyncio.ensure_future(self._an(self.ket.gui("Page.screencastFrameAck", {"sessionId": p.get("sessionId")}, 3)))
        elif me in ("Page.frameNavigated", "Page.loadEventFired", "Page.navigatedWithinDocument"):
            if me != "Page.frameNavigated" or not (p.get("frame") or {}).get("parentId"):
                asyncio.ensure_future(self._an(self.bao_trang()))
        elif me == "Page.javascriptDialogOpening":
            asyncio.ensure_future(self._an(self.gui_len({"t": "hop", "kieu": p.get("type"), "chu": str(p.get("message") or "")[:300]})))
        elif me == "__dong__":
            if self.ket is not None and (getattr(self.ket, "ws", 1) is None or getattr(self.ket, "chet", False)) and not self.dong_roi:      # tab bị đóng / Chrome tắt (không phải mình tự ngắt)
                asyncio.ensure_future(self._an(self._noi_lai()))

    async def _noi_lai(self):
        await self.gui_len({"t": "bao", "chu": "Tab vừa đóng, đang nối lại..."})
        await asyncio.sleep(1.0)
        self.ket = None
        try:
            await self.chon_tab("")
        except Exception as e:  # noqa: BLE001
            await self.gui_len({"t": "loi", "chu": str(e)[:200]})

    @staticmethod
    async def _an(co):
        try:
            await co
        except Exception:  # noqa: BLE001
            pass

    # ---- chọn tab
    async def chon_tab(self, tid: str = ""):
        B._HS.set(self.hs)
        B._CHAT.set(self.chat)
        ds = B.tab_cua_chat(await asyncio.to_thread(B._trang_dang_co, self.hs), self.chat)
        if not tid:
            tid = B._lay_tab(self.chat)
        t = next((x for x in ds if x["id"] == tid), None)
        if not t and not tid and ds and (self.chat or not B._ngoai(self.hs)):
            t = ds[-1]
        if not t and self.cho_ai:
            raise RuntimeError("Đang chờ TISA BOT mở trang web cho việc này.")
        if not t:
            # Ô chat này chưa có tab (hoặc Chrome của anh: không lấy tab anh đang dùng): mở một tab riêng cho ô chat.
            tid = await B._tab_moi("https://www.google.com/")
            await asyncio.sleep(0.5)
            ds = await asyncio.to_thread(B._trang_dang_co, self.hs)
            t = next((x for x in ds if x["id"] == tid), None)
        if not t:
            raise RuntimeError("Chưa mở được tab cho ô chat này.")
        if self.ket:
            await self._tat_ket()
        nghe = self._su_kien
        ws = str(t.get("webSocketDebuggerUrl") or "")
        if ws.startswith("ngoai:"):
            _, trinh, _ = (ws.split(":", 2) + ["", ""])[:3]
            self.ket = _KetNgoai(trinh, t["id"], nghe)
        else:
            if not ws:
                raise RuntimeError("Tab này đang được một công cụ khác giữ, chưa xem được.")
            self.ket = _KetRieng(ws, nghe)
        await self.ket.mo()
        self.tab = t["id"]
        B._dat_tab(t["id"], self.chat)          # AI của ô chat này làm tiếp đúng tab anh đang xem trong khung
        cac = [("Page.enable", {}), ("Emulation.setFocusEmulationEnabled", {"enabled": True})]
        if isinstance(self.ket, _KetRieng):
            cac.append(("Page.bringToFront", {}))      # trình duyệt riêng của TISA: tab nằm sau thì Chrome không vẽ, đưa lên trước để khung có hình
        for me, pr in cac:
            try:
                await self.ket.gui(me, pr, 5)
            except Exception:  # noqa: BLE001
                pass
        self.luc_chon, self.da_dua_len = time.time(), False
        await self.ap_kich_thuoc()
        await self.bao_trang()

    async def _tat_ket(self):
        la_chu = _CHU_CO.get(self.tab) is self
        if la_chu:
            _CHU_CO.pop(self.tab, None)
        k, self.ket = self.ket, None
        if not k:
            return
        for me in ("Page.stopScreencast", "Emulation.clearDeviceMetricsOverride", "Emulation.setFocusEmulationEnabled"):
            if me == "Emulation.clearDeviceMetricsOverride" and not la_chu:
                continue          # khung khác đang đặt cỡ tab này: không xóa cỡ của nó
            try:
                await k.gui(me, {"enabled": False} if me.endswith("Enabled") else {}, 2)
            except Exception:  # noqa: BLE001
                pass
        await k.dong()

    async def ap_kich_thuoc(self):
        if not self.ket:
            return
        k = self.ket
        chu = _CHU_CO.get(self.tab)
        if chu is not None and chu is not self and not chu.dong_roi and chu.ket is not None:
            dat_co = False          # một khung khác đang đặt cỡ cho tab này: chỉ xem, thu phóng theo hình
        else:
            dat_co = True
            _CHU_CO[self.tab] = self
        try:
            if not dat_co:
                pass
            elif self.vua and self.w >= 240 and self.h >= 200 and not isinstance(k, _KetNgoai):     # Chrome của anh: không đổi cỡ tab trong cửa sổ thật của anh
                await k.gui("Emulation.setDeviceMetricsOverride", {"width": int(self.w), "height": int(self.h), "deviceScaleFactor": 0, "mobile": False}, 5)
            else:
                await k.gui("Emulation.clearDeviceMetricsOverride", {}, 5)
        except Exception:  # noqa: BLE001
            pass
        ti = max(1.0, min(self.dpr or 1.0, 1.5))
        mw = int(min(TOI_DA_CANH, max(320, (self.w or 1000) * ti)))
        mh = int(min(TOI_DA_CANH, max(240, (self.h or 800) * ti)))
        try:
            await k.gui("Page.stopScreencast", {}, 3)
        except Exception:  # noqa: BLE001
            pass
        try:
            await k.gui("Page.startScreencast", {"format": "jpeg", "quality": CHAT_LUONG, "maxWidth": mw, "maxHeight": mh, "everyNthFrame": 1}, 5)
        except Exception:  # noqa: BLE001
            pass
        self.luc_khung = 0.0
        asyncio.ensure_future(self._an(self.chup_bu()))

    async def chup_bu(self):
        """Cửa sổ Chrome bị che/thu nhỏ hoặc tab nằm sau thì Chrome không vẽ khung screencast: chụp thẳng một tấm."""
        if not self.ket:
            return
        k = self.ket
        r = await k.gui("Page.captureScreenshot", {"format": "jpeg", "quality": CHAT_LUONG}, 5)
        lm = await k.gui("Page.getLayoutMetrics", {}, 4)
        v = lm.get("cssLayoutViewport") or lm.get("layoutViewport") or {}
        if r.get("data") and k is self.ket:
            self.khung_moi = (r["data"], {"w": v.get("clientWidth"), "h": v.get("clientHeight"), "top": 0})
            self.luc_khung = time.time()
            self.co_khung.set()

    async def bao_trang(self):
        if not self.ket:
            return
        tt = {"t": "trang", "tab": self.tab, "url": "", "tieu_de": "", "lui": False, "toi": False}
        try:
            r = await self.ket.gui("Page.getNavigationHistory", {}, 4)
            ds, i = r.get("entries") or [], int(r.get("currentIndex") or 0)
            if ds:
                tt.update(url=ds[i].get("url", ""), tieu_de=ds[i].get("title", ""), lui=i > 0, toi=i < len(ds) - 1)
        except Exception:  # noqa: BLE001
            pass
        ds = B.tab_cua_chat(await asyncio.to_thread(B._trang_dang_co, self.hs), self.chat)
        tt["tabs"] = [{"id": t["id"], "tieu_de": (t.get("title") or t.get("url") or "")[:60], "url": t.get("url", "")} for t in ds][:12]
        self.thong_tin = tt
        await self.gui_len(tt)

    # ---- vòng gửi khung hình + chụp bù
    async def vong_gui(self):
        while not self.dong_roi:
            try:
                await asyncio.wait_for(self.co_khung.wait(), 0.6)
            except asyncio.TimeoutError:
                pass
            self.co_khung.clear()
            if self.khung_moi:
                d, m = self.khung_moi
                self.khung_moi = None
                await self.gui_len({"t": "hinh", "d": d, "m": m})
            elif self.ket and time.time() - self.luc_khung > KHONG_KHUNG_THI_CHUP and (time.time() - self.luc_bam < 30 or time.time() - self.luc_khung > 4) \
                    and not (self.dang_chup and not self.dang_chup.done()):
                self.dang_chup = asyncio.ensure_future(self._an(self.chup_bu()))      # chạy riêng: chụp chậm không được chặn vòng gửi hình

    async def vong_tab(self):
        """Mỗi 2,5 giây: danh sách tab, và nếu AI đã chuyển sang tab khác thì khung đi theo."""
        while not self.dong_roi:
            await asyncio.sleep(2.5)
            try:
                B._HS.set(self.hs)
                # (V3.44) AI của ô chat đang điều khiển CHUỘT, BÀN PHÍM máy chủ trong Chrome của anh (không qua công cụ trình duyệt):
                # khung đi theo đúng tab Chrome đang ở trước trên máy chủ, anh ngồi máy khác vẫn thấy bot làm ở trang nào.
                if B._ngoai(self.hs) and _chat_dung_may(self.chat):
                    tid = await asyncio.to_thread(tab_truoc_chrome, self.hs)
                    if tid and tid != self.tab:
                        B._dat_tab(tid, self.chat)
                        await self.chon_tab(tid)
                        await self.gui_len({"t": "san_sang", "ten": B._ten_hs(self.hs), "hoso": self.hs, "ngoai": True})
                        continue
                ai_tab = B._lay_tab(self.chat)
                if (B.DIR / "debug-khung").exists():
                    # Chẩn đoán khi khung không đi theo AI (22/11/2026): tạo tệp trinh-duyet/debug-khung để bật, xóa tệp để tắt, không cần khởi động lại.
                    try:
                        ds_that = await asyncio.to_thread(B._trang_dang_co, self.hs)
                        cua = set((B._tab_chat.get(self.chat) or {}).get("tabs") or [])
                        print("[khung-debug] chat=%s hs=%s cong_mo=%s ai_tab=%s dang_xem=%s | tab_that=%s | tab_o_chat=%s | ai_tab_con=%s" % (
                            (self.chat or "-")[:8], self.hs, B._cong_mo(), (ai_tab or "-")[:8], (self.tab or "-")[:8],
                            [t["id"][:8] for t in ds_that], sorted(x[:8] for x in cua), any(t["id"] == ai_tab for t in ds_that)), flush=True)
                    except Exception as e_dbg:  # noqa: BLE001
                        print("[khung-debug] loi: %s: %s" % (type(e_dbg).__name__, str(e_dbg)[:120]), flush=True)
                if ai_tab and ai_tab != self.tab and B._cong_mo() and any(t["id"] == ai_tab for t in B.tab_cua_chat(await asyncio.to_thread(B._trang_dang_co, self.hs), self.chat)):
                    await self.chon_tab(ai_tab)
                    await self.gui_len({"t": "san_sang", "ten": B._ten_hs(self.hs), "hoso": self.hs, "ngoai": bool(B._ngoai(self.hs))})
                elif self.ket:
                    await self.bao_trang()
                    # Chrome của anh: tab AI làm nằm sau thì Chrome không vẽ. Chờ 3 giây không có hình thì lật tab đó lên (anh đang muốn xem bot làm).
                    if isinstance(self.ket, _KetNgoai) and not self.da_dua_len and self.luc_khung < self.luc_chon and time.time() - self.luc_chon > 3:
                        self.da_dua_len = True
                        await self.ket.gui("Page.bringToFront", {}, 4)
            except Exception:  # noqa: BLE001
                pass

    # ---- lệnh từ khung của anh
    async def lenh(self, d: dict):
        t = d.get("t")
        k = self.ket
        if t == "kt":
            self.w, self.h = int(d.get("w") or 0), int(d.get("h") or 0)
            self.dpr = float(d.get("dpr") or 1)
            await self.ap_kich_thuoc()
            return
        if t == "vua":
            self.vua = bool(d.get("on"))
            await self.ap_kich_thuoc()
            return
        if t == "tab":
            await self.chon_tab(str(d.get("id") or ""))
            return
        if t == "tab_moi":
            if self.cho_ai and not self.ket and not B.hs_cua_chat(self.chat):
                # Chưa có gì để xem mà anh tự mở tab: dùng trình duyệt chạy ngầm của khung cho ô chat này (không mở tab trong Chrome của anh).
                self.hs, self.cho_ai = B.ho_so_khung() or self.hs, False
                B._HS.set(self.hs)
                if not B._cong_mo():
                    await B.mo_trinh_duyet("", self.hs)
                if self.chat:
                    B.gan_hs_chat(self.chat, self.hs)
            B._HS.set(self.hs)
            B._CHAT.set(self.chat)
            tid = await B._tab_moi(chuan_dia_chi(str(d.get("url") or "")) or "https://www.google.com/")
            await asyncio.sleep(0.4)
            await self.chon_tab(tid)
            return
        if t == "dong_tab":
            B._HS.set(self.hs)
            tid = str(d.get("id") or self.tab)
            if self.chat and B.chu_cua_tab(tid) not in ("", self.chat):
                return
            async with B._Phien(await B._ws_url_trinh_duyet()) as b:
                await b.gui("Target.closeTarget", {"targetId": tid})
            if tid == self.tab:
                B._dat_tab("", self.chat)
                await asyncio.sleep(0.3)
                await self.chon_tab("")
            return
        if not k:
            return
        self.luc_bam = time.time()
        if t == "chuot":
            await k.gui("Input.dispatchMouseEvent", {"type": d.get("kieu", "mouseMoved"), "x": float(d.get("x") or 0), "y": float(d.get("y") or 0),
                                                     "button": d.get("nut", "none"), "buttons": int(d.get("nuts") or 0), "clickCount": int(d.get("lan") or 0),
                                                     "modifiers": int(d.get("mods") or 0)}, 5)
        elif t == "cuon":
            await k.gui("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": float(d.get("x") or 0), "y": float(d.get("y") or 0),
                                                     "deltaX": float(d.get("dx") or 0), "deltaY": float(d.get("dy") or 0), "modifiers": int(d.get("mods") or 0)}, 5)
        elif t == "chu":
            s = str(d.get("s") or "")[:5000]
            if s:
                await k.gui("Input.insertText", {"text": s}, 5)
        elif t == "phim":
            for ev in lenh_phim(str(d.get("kieu") or "down"), str(d.get("key") or ""), str(d.get("code") or ""), int(d.get("ma") or 0), int(d.get("mods") or 0)):
                await k.gui("Input.dispatchKeyEvent", ev, 5)
        elif t == "chep":
            r = await k.gui("Runtime.evaluate", {"expression": "String(getSelection ? getSelection() : '')", "returnByValue": True}, 4)
            await self.gui_len({"t": "chep", "s": str(((r.get("result") or {}).get("value")) or "")[:20000]})
        elif t == "di":
            u = chuan_dia_chi(str(d.get("url") or ""))
            if u:
                await k.gui("Page.navigate", {"url": u}, 10)
        elif t in ("lui", "toi"):
            r = await k.gui("Page.getNavigationHistory", {}, 4)
            ds, i = r.get("entries") or [], int(r.get("currentIndex") or 0)
            j = i - 1 if t == "lui" else i + 1
            if 0 <= j < len(ds):
                await k.gui("Page.navigateToHistoryEntry", {"entryId": ds[j]["id"]}, 6)
        elif t == "tai":
            await k.gui("Page.reload", {}, 6)
        elif t == "hop":
            await k.gui("Page.handleJavaScriptDialog", {"accept": bool(d.get("ok")), **({"promptText": str(d.get("chu"))} if d.get("chu") is not None else {})}, 4)

    async def dong(self):
        self.dong_roi = True
        self.co_khung.set()
        await self._tat_ket()


# ------------------------------------------------------------------ route
def gan(app) -> None:
    @app.websocket("/trinh-duyet/khung/ws")
    async def khung_ws(ws: WebSocket):
        try:
            import config as cfgmod
            if cfgmod.gate_active() and not cfgmod.valid_session(ws.cookies.get("tisa_session", "")):
                await ws.close(code=1008)
                return
        except ImportError:
            pass
        await ws.accept()
        khoa_gui = asyncio.Lock()

        async def gui_len(obj):
            async with khoa_gui:
                await ws.send_text(json.dumps(obj, ensure_ascii=False))

        chat = re.sub(r"[^\w:.-]", "", str(ws.query_params.get("chat") or ""))[:80]
        cho = ws.query_params.get("cho") == "1"
        B._CHAT.set(chat)
        # Chọn trình duyệt cho khung (V3.43, chủ chốt 22/11):
        #  - ô chat đã gắn trình duyệt (anh từng mở khung ở đây) -> trình duyệt đó;
        #  - AI của ô chat đang làm trên một tab (vd Đạt Đấu Nối cài MCP/API trong Chrome có sẵn đăng nhập của anh) -> XEM đúng các tab AI mở
        #    cho ô chat này, không gắn, không đụng tab khác của anh;
        #  - khung tự mở để chờ AI (cho=1) -> chờ, chưa mở gì;
        #  - còn lại (anh bấm nút Trình duyệt) -> trình duyệt CHẠY NGẦM riêng, không lẫn với tab Chrome anh đang mở.
        ban = B.hs_cua_chat(chat) if chat else ""
        hs_ai = B.hs_dang_dung()
        if ban:
            hs, gan_khung = ban, False
        elif chat and (B._lay_tab(chat) or cho):
            hs, gan_khung = hs_ai, False
        else:
            hs, gan_khung = (B.ho_so_khung() or hs_ai), True
        B._HS.set(hs)
        if not B._cong_mo():
            if not gan_khung and not ban:
                await gui_len({"t": "cho", "chu": "Đang chờ TISA BOT mở trang web. Khung hiện ngay khi bot bắt đầu làm."})
            else:
                await gui_len({"t": "bao", "chu": "Đang mở trình duyệt..."})
                kq = await B.mo_trinh_duyet("", hs)
                if not kq.get("ok"):
                    await gui_len({"t": "loi", "chu": kq.get("loi") or "Không mở được trình duyệt."})
                    await ws.close()
                    return
        if chat and gan_khung:
            B.gan_hs_chat(chat, hs)          # từ giờ AI của ô chat này làm trong trình duyệt của khung
        kh = Khung(gui_len, hs, chat)
        kh.cho_ai = not gan_khung and not ban
        try:
            d = json.loads(await asyncio.wait_for(ws.receive_text(), 10))
            if d.get("t") == "kt":
                kh.w, kh.h, kh.dpr = int(d.get("w") or 0), int(d.get("h") or 0), float(d.get("dpr") or 1)
                kh.vua = d.get("vua") is not False
        except Exception:  # noqa: BLE001
            pass
        try:
            if kh.cho_ai and not (B._cong_mo() and B._lay_tab(chat) and any(t["id"] == B._lay_tab(chat) for t in await asyncio.to_thread(B._trang_dang_co, hs))):
                await gui_len({"t": "cho", "chu": "Đang chờ TISA BOT mở trang web. Khung hiện ngay khi bot bắt đầu làm."})
            else:
                await kh.chon_tab("")
        except Exception as e:  # noqa: BLE001
            try:          # khung đã đóng giữa chừng thì thôi (trước đây gửi tiếp làm lỗi "after sending websocket.close" trong nhật ký)
                await gui_len({"t": "loi", "chu": str(e)[:300]})
                await ws.close()
            except Exception:  # noqa: BLE001
                pass
            return
        await gui_len({"t": "san_sang", "ten": B._ten_hs(hs), "hoso": hs, "ngoai": bool(B._ngoai(hs))})
        cac_vong = [asyncio.create_task(kh.vong_gui()), asyncio.create_task(kh.vong_tab())]
        try:
            while True:
                m = await ws.receive_text()
                try:
                    d = json.loads(m)
                except ValueError:
                    continue
                try:
                    await kh.lenh(d)
                except Exception as e:  # noqa: BLE001
                    if d.get("t") not in ("chuot", "cuon"):
                        await gui_len({"t": "bao", "chu": str(e)[:200]})
                    if "mất kết nối" in str(e) or "không trả lời" in str(e):
                        try:
                            await kh.chon_tab("")
                        except Exception:  # noqa: BLE001
                            pass
        except Exception:  # noqa: BLE001 - anh đóng khung / mất mạng
            pass
        finally:
            for v in cac_vong:
                v.cancel()
            await kh.dong()

    @app.get("/trinh-duyet/khung/chat")
    async def khung_chat(chat: str = ""):
        """Trang hỏi: AI của ô chat này có đang dùng trình duyệt không (để tự mở khung cho anh xem)."""
        from fastapi.responses import JSONResponse
        c = re.sub(r"[^\w:.-]", "", chat)[:80]
        B.danh_dau_xem(c)          # trang đang mở đúng ô chat này: AI làm trên web thì mặc định vào khung bên phải
        hs = B.hs_cua_chat(c) if c else ""
        x = next((y for y in B._doc_hs()["ds"] if y["id"] == hs), {}) if hs else {}
        try:
            import tisa_chong_chen as CC
            g = CC.doc_da_chon()
        except Exception:  # noqa: BLE001
            g = None
        try:
            import tisa_desktop as TD
            may = TD.chat_vua_dung_may(c)
        except Exception:  # noqa: BLE001
            may = False
        try:
            import tisa_browser_ngoai as N
            hoi = N.dang_hoi()
        except Exception:  # noqa: BLE001
            hoi = None
        return JSONResponse({"moi": B.chat_vua_dung(c), "co_tab": bool(B._lay_tab(c)) if c else False,
                             "loai": "chrome" if x.get("loai") == "ngoai" else ("rieng" if x.get("khung") else ""),
                             "ho_so": (g or {}).get("thu_muc", "") if x.get("loai") == "ngoai" else "",
                             "may": may, "go_loi": hoi})

    # ---------------------------------------------------------------- (V3.44) anh ngồi máy khác vẫn thấy và làm được trên máy chủ
    @app.post("/trinh-duyet/khung/go-loi")
    async def khung_go_loi(request: Request):
        """Anh bấm Cho phép / Huỷ cho hộp "Cho phép gỡ lỗi từ xa?" của Chrome trên máy chủ, từ khung Trình duyệt ở bất kỳ máy nào."""
        from fastapi.responses import JSONResponse
        import tisa_browser_ngoai as N
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        h = N.dang_hoi()
        if not h:
            return JSONResponse({"ok": False, "tin": "Chrome không còn hỏi nữa (đã có người bấm, hoặc lần nối đã hết giờ)."})
        kq = await N.ket_noi(h["trinh"]).tra_loi_hop(bool((d or {}).get("cho_phep")))
        return JSONResponse({"ok": kq == "ok", "tin": {"ok": "Đã bấm trên máy chủ.", "khong_co": "Không thấy hộp trên máy chủ nữa."}.get(kq, "Chưa bấm được (%s)." % kq)})

    @app.post("/trinh-duyet/khung/do-ban-phim")
    async def khung_do_ban_phim(request: Request):
        """(V3.44) Số đo bàn phím từ điện thoại (dò lỗi ô nhập cách bàn phím). Chỉ số đo màn hình, giữ 60 dòng gần nhất."""
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        if isinstance(d, dict):
            d = {str(k)[:20]: (v if isinstance(v, (int, float, bool)) or v is None else str(v)[:200]) for k, v in list(d.items())[:20]}
            d["luc"] = time.strftime("%Y-%m-%d %H:%M:%S")
            f = B.DIR / "do-ban-phim.jsonl"
            try:
                f.parent.mkdir(parents=True, exist_ok=True)
                cu = f.read_text(encoding="utf-8").splitlines()[-59:] if f.exists() else []
                f.write_text("\n".join(cu + [json.dumps(d, ensure_ascii=False)]) + "\n", encoding="utf-8")
            except OSError:
                pass
        return JSONResponse({"ok": True})

    @app.get("/trinh-duyet/khung/khoa")
    async def khung_khoa():
        """Máy chủ có đang ở màn hình khóa không, và đã có mật khẩu mở khóa trong Keychain chưa (không bao giờ trả mật khẩu)."""
        from fastapi.responses import JSONResponse
        import tisa_desktop as TD
        p = TD.nen()
        if p is None or getattr(p, "ten", "") != "macOS":
            return JSONResponse({"ho_tro": False, "khoa": False})
        import tisa_mo_khoa as MK
        khoa = await asyncio.to_thread(MK._dang_khoa, p)
        return JSONResponse({"ho_tro": True, "khoa": bool(khoa), "san_sang": await asyncio.to_thread(MK.dang_bat)})

    @app.post("/trinh-duyet/khung/mo-khoa")
    async def khung_mo_khoa():
        """(V3.44, chủ yêu cầu 22/11) Anh ngồi máy khác bấm "Mở khóa máy" trong khung: TISA BOT gõ mật khẩu lấy từ Keychain vào màn hình khóa của máy chủ.
        Chính anh bấm trên dashboard đã đăng nhập = anh duyệt; vẫn đi qua mọi chốt của tisa_mo_khoa (kiểm mật khẩu trước khi gõ, tối đa 3 lần, nhật ký)."""
        from fastapi.responses import JSONResponse
        import tisa_desktop as TD
        import tisa_mo_khoa as MK
        p = TD.nen()
        if p is None:
            return JSONResponse({"ok": False, "ma": "KHONG_HO_TRO", "tin": "Máy chủ chưa hỗ trợ điều khiển máy tính."})
        loop = asyncio.get_running_loop()
        try:
            import tisa_bao_anh as BA
            bao = (lambda t: BA.bao(t, loop))
        except Exception:  # noqa: BLE001
            bao = None
        turn = {"kenh": "dashboard", "la_chu": True, "chat_type": "private"}
        kq = await asyncio.to_thread(MK._mo_khoa_nen, p, {}, "toan_quyen", turn, None, bao)
        ma = str(kq).split(":", 1)[0].strip()
        tin = {"DA_MO_KHOA": "Đã mở khóa máy chủ.", "KHONG_CAN": "Máy chủ không ở màn hình khóa.",
               "TAT": "Chưa có mật khẩu mở khóa. Anh nhập mật khẩu máy một lần bên dưới (được kiểm đúng rồi cất vào Keychain của máy chủ).",
               "CHUA_CAI_MAT_KHAU": "Chưa có mật khẩu mở khóa. Anh nhập mật khẩu máy một lần bên dưới.",
               "SAI_MAT_KHAU_LUU": "Mật khẩu đang lưu không khớp mật khẩu máy (có thể anh vừa đổi). Anh nhập lại bên dưới.",
               "DA_DUNG_THU": "Đã thử 3 lần không được nên tạm dừng 30 phút. Vào Điều khiển của AI → Máy tính → Mở khóa máy bấm \"Cho thử lại\".",
               "CAN_NGUOI_DUNG": "Máy chủ đang hiện hộp xác minh (Touch ID, mã khóa): cần người ở máy chủ.",
               "DANG_CHAY": "Đang mở khóa, chờ chút."}.get(ma, str(kq).split("\n", 1)[0][:220])
        return JSONResponse({"ok": ma in ("DA_MO_KHOA", "KHONG_CAN"), "ma": ma, "tin": tin, "can_mat_khau": ma in ("TAT", "CHUA_CAI_MAT_KHAU", "SAI_MAT_KHAU_LUU")})

    @app.get("/trinh-duyet/khung/man-hinh")
    async def khung_man_hinh(canh: int = 1400):
        """Ảnh màn hình máy chủ (JPEG) cho khung xem khi AI của ô chat đang điều khiển máy tính."""
        from fastapi.responses import JSONResponse, Response
        try:
            import tisa_desktop as TD
            if TD.muc_hien_tai() == "tat":
                return JSONResponse({"loi": "Anh đang tắt điều khiển máy tính."}, status_code=403)
        except Exception:  # noqa: BLE001
            pass
        f = B.DIR / "khung-man-hinh.jpg"

        def chup():
            try:
                import tisa_chup_nhanh as QN
                f.parent.mkdir(parents=True, exist_ok=True)
                r = QN.chup(f, max(480, min(int(canh or 1400), 2000)), None, 0.62)
                if r:
                    return f.read_bytes(), r
            except Exception:  # noqa: BLE001
                pass
            return None, None
        b, r = await asyncio.to_thread(chup)
        if not b:
            return JSONResponse({"loi": "Không chụp được màn hình máy chủ (thiếu quyền Ghi màn hình?)."}, status_code=503)
        return Response(b, media_type="image/jpeg", headers={"Cache-Control": "no-store", "X-Goc": "%dx%d" % (r[0], r[1])})

    @app.post("/trinh-duyet/khung/may")
    async def khung_may(request: Request):
        """Anh bấm / gõ trên màn hình máy chủ qua khung (anh đang ngồi máy khác). Toạ độ theo tỉ lệ ảnh (0..1)."""
        from fastapi.responses import JSONResponse
        import tisa_desktop as TD
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        d = d or {}
        p = TD.nen()
        if p is None:
            return JSONResponse({"ok": False, "tin": "Máy chủ chưa hỗ trợ điều khiển máy tính."})
        if TD.muc_hien_tai() == "tat":
            return JSONResponse({"ok": False, "tin": "Anh đang tắt điều khiển máy tính (mức Không cho)."})
        t = str(d.get("t") or "")

        def lam():
            w, h = p.kich_thuoc()
            if t in ("bam", "bam_doi", "bam_phai"):
                x = max(0, min(w - 1, int(float(d.get("rx") or 0) * w)))
                y = max(0, min(h - 1, int(float(d.get("ry") or 0) * h)))
                p.bam(x, y, "right" if t == "bam_phai" else "left", 2 if t == "bam_doi" else 1)
                return "Đã bấm tại (%d,%d)" % (x, y)
            if t == "cuon":
                p.cuon(int(d.get("dy") or 0), int(float(d.get("rx") or 0.5) * w), int(float(d.get("ry") or 0.5) * h))
                return "Đã cuộn"
            if t == "phim":
                mods, phim = TD._tach_phim(str(d.get("key") or ""))
                if not phim:
                    return "Thiếu phím"
                p.nhan_phim(mods, phim)
                return "Đã nhấn %s" % d.get("key")
            if t == "chu":
                s = str(d.get("s") or "")[:4000]
                khoa = False
                if s and getattr(p, "ten", "") == "macOS":
                    try:
                        import tisa_mo_khoa as MK
                        khoa = bool(MK._dang_khoa(p))
                    except Exception:  # noqa: BLE001
                        khoa = False
                if s and khoa:
                    # Màn hình khóa macOS chỉ nhận PHÍM THẬT (mã phím, nguồn phần cứng); chữ gửi kiểu "dán"/unicode bị bỏ qua (chủ báo 22/11).
                    try:
                        p.danh_thuc_man_hinh()
                    except Exception:  # noqa: BLE001
                        pass
                    try:
                        import tisa_mo_khoa as MK2
                        MK2._bam_vao_o_mat_khau(p)       # ô mật khẩu phải được bấm vào trước, không thì phím bị bỏ
                    except Exception:  # noqa: BLE001
                        pass
                    p.go(s, "phim", 0.05)
                    return "Đã gõ %d ký tự vào màn hình khóa" % len(s)        # không ghi nội dung (có thể là mật khẩu)
                if s:
                    (p.dan_chu if any(ord(c) > 127 for c in s) else (lambda x: p.go(x, "chu")))(s)
                return "Đã gõ %d ký tự" % len(s)
            return "Lệnh lạ"
        try:
            tin = await asyncio.to_thread(lam)
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "tin": "%s: %s" % (type(e).__name__, str(e)[:160])})
        TD._nk("tu_xa_" + t, "ok", "Anh thao tác trên màn hình máy chủ từ khung Trình duyệt: %s" % tin)
        return JSONResponse({"ok": True, "tin": tin})

    @app.post("/trinh-duyet/khung/chon")
    async def khung_chon(request: Request):
        """Anh chọn trình duyệt cho ô chat ngay trong khung: trình duyệt riêng chạy ngầm, hoặc MỘT hồ sơ Chrome đã đăng nhập sẵn của anh.
        Chỉ đổi ô chat này; trình duyệt mặc định của các ô chat khác giữ nguyên."""
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        d = d or {}
        c = re.sub(r"[^\w:.-]", "", str(d.get("chat") or ""))[:80]
        if not c:
            return JSONResponse({"ok": False, "loi": "Chưa mở ô chat nào."})
        if str(d.get("loai") or "") == "rieng":
            hs = B.ho_so_khung()
            if not hs:
                return JSONResponse({"ok": False, "loi": "Không tạo được trình duyệt riêng."})
            B.gan_hs_chat(c, hs)
            return JSONResponse({"ok": True, "tin": "Ô chat này dùng trình duyệt riêng chạy ngầm của TISA BOT."})
        import tisa_chong_chen as CC
        r = await asyncio.to_thread(CC.dat_da_chon, str(d.get("ho_so") or ""))
        if not r.get("ok"):
            return JSONResponse(r)
        x = B.tao_ho_so_ngoai("chrome")
        if not x.get("ok"):
            return JSONResponse(x)
        B.gan_hs_chat(c, x["id"])
        h = r["ho_so"]
        return JSONResponse({"ok": True, "tin": "Ô chat này dùng Chrome hồ sơ %s%s (đã đăng nhập sẵn)." % (h.get("ten") or h.get("thu_muc"), (" - " + h["email"]) if h.get("email") else "")})

    @app.get("/trinh-duyet/khung/co")
    async def khung_co():
        from fastapi.responses import JSONResponse
        return JSONResponse({"ok": True, "ban": 1})
