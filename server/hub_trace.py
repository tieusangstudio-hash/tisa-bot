"""Short in-memory trace of the MCP hub's startup requests (0.72.1).

When Claude Code starts it connects to the TISA BOT hub (`/hub/mcp`) and asks `initialize` and
`tools/list` before it takes any work. If that startup times out, the question that decides
where to look is whether Claude ever reached the hub at all:

  - it never called: Claude is stuck before the hub (login, network, self-update), and no MCP
    source can be to blame;
  - it called and the hub answered late or not at all: the tool discovery is the culprit;
  - it called and the hub answered fast: the hub is fine, Claude is stuck on something else.

The hub runs in the same process as the engine, so a ring buffer is enough. No deps, no I/O.
"""
import collections
import time

# Only the two requests Claude makes before it accepts work. tools/call is not startup.
_TRACKED = ("initialize", "tools/list")
_EVENTS = collections.deque(maxlen=64)


def begin(method):
    """Record the start of a hub request. Returns a handle for `end`, or None if untracked."""
    if method not in _TRACKED:
        return None
    ev = {"t0": time.time(), "method": method, "dur": None}
    _EVENTS.append(ev)
    return ev


def end(ev):
    """Close a request opened by `begin`. Safe to call with None."""
    if ev is not None and ev["dur"] is None:
        ev["dur"] = time.time() - ev["t0"]


def since(t_start):
    """Summary of the tracked requests that began at or after `t_start` (epoch seconds).

    {"called": bool, "init_s": float|None, "list_s": float|None,
     "pending": "initialize"|"tools/list"|None, "pending_s": float}

    `*_s` is the slowest finished duration for that method. `pending` is the oldest request
    still unanswered, with how long it has been waiting.
    """
    out = {"called": False, "init_s": None, "list_s": None, "pending": None, "pending_s": 0.0}
    now = time.time()
    for ev in list(_EVENTS):
        if ev["t0"] < t_start:
            continue
        out["called"] = True
        if ev["dur"] is None:
            age = now - ev["t0"]
            if out["pending"] is None or age > out["pending_s"]:
                out["pending"], out["pending_s"] = ev["method"], age
            continue
        key = "init_s" if ev["method"] == "initialize" else "list_s"
        if out[key] is None or ev["dur"] > out[key]:
            out[key] = ev["dur"]
    return out


def chi_tiet(t_start):
    """Tách thời gian khởi động của MỘT lượt bắt đầu lúc `t_start` (V3.59, để đo vì sao quy trình chậm trên máy học viên).

    {"called": bool, "dau_s": giây từ t_start tới lúc Claude gọi hub lần đầu (= mở tiến trình Claude), "hub_s": tổng thời gian hub
    trả lời initialize + tools/list, "xong_s": giây từ t_start tới lúc hub trả lời xong yêu cầu cuối}. Ước lượng: bộ đệm dùng chung
    cả tiến trình, nên hai lượt chạy cùng lúc có thể lẫn số của nhau."""
    evs = [e for e in list(_EVENTS) if e["t0"] >= t_start]
    if not evs:
        return {"called": False, "dau_s": None, "hub_s": None, "xong_s": None}
    xong = [e for e in evs if e["dur"] is not None]
    return {"called": True, "dau_s": min(e["t0"] for e in evs) - t_start,
            "hub_s": sum(e["dur"] for e in xong) if xong else None,
            "xong_s": (max(e["t0"] + e["dur"] for e in xong) - t_start) if xong else None}
