#!/usr/bin/env python3
"""mcp_doi_quan.py - máy chủ MCP để Claude giao việc cho Đội Quân AI và xem tiến độ.

setup_suite.py đăng ký tệp này với Claude Code và Claude Desktop. Chỉ dùng thư viện chuẩn của Python,
nói chuyện với bảng trên máy bằng mã trong ~/.config/doi-quan-ai/.env (không bao giờ in mã ra).
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ENV = Path(os.environ.get("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
PROTOCOL = "2025-06-18"


def cfg():
    out = {}
    try:
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    except OSError:
        pass
    return out


def board(method, path, body=None):
    c = cfg()
    if not c.get("BOARD_TOKEN"):
        raise RuntimeError("Chưa có mã bảng. Mở TISA BOT một lần để bộ cài hoàn tất.")
    url = (c.get("BOARD_URL") or "http://127.0.0.1:7788").rstrip("/") + path
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + c["BOARD_TOKEN"], "Content-Type": "application/json", "User-Agent": "doi-quan-mcp/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.URLError as e:
        raise RuntimeError("Không gọi được bảng giao việc. TISA BOT có đang mở không? (%s)" % e)


def _slug(text, limit=34):
    s = unicodedata.normalize("NFD", text)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn").replace("đ", "d").replace("Đ", "D")
    s = re.sub(r"[^A-Za-z0-9 ]+", " ", s).strip()
    return re.sub(r"\s+", " ", s)[:limit].strip() or "viec moi"


def giao_viec(a):
    task = str(a.get("yeu_cau") or "").strip()
    if not task:
        raise RuntimeError("Thiếu yeu_cau")
    title = str(a.get("tieu_de") or "").strip() or (task if len(task) <= 90 else task[:88] + "…")
    kit = board("GET", "/api/v1/kit").get("doanh_nghiep") or {}
    office = (kit.get("thu_muc_van_phong") or "05 - Van Phong AI").strip()
    now = time.localtime()
    d, hm = time.strftime("%Y-%m-%d", now), time.strftime("%H:%M", now)
    iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    jid = "job-%x" % int(time.time() * 1000)
    doc = {"title": title, "task": task, "date": d, "time": hm, "created": iso, "updated": iso, "status": "hang-doi",
           "mode": "claude", "demo": False, "folder": "%s/03 - Ket qua/%s/%s/%s/%s %s/" % (office, d[:4], d[:7], d, hm.replace(":", ""), _slug(title)),
           "plan": [], "summary": "", "insights": [], "synced": False, "brain": "cho-nap", "settings": None, "files": [], "nguon": "claude-mcp"}
    board("PUT", "/api/db/results/" + jid, doc)
    return {"job_id": jid, "trang_thai": "hang-doi", "ghi_chu": "Đã đưa lên bảng, Tâm Tổng Quản nhận trong vài giây."}


def _gon(r):
    return {"job_id": r.get("id"), "tieu_de": r.get("title"), "trang_thai": r.get("status"), "tom_tat": r.get("summary", ""),
            "ngay": r.get("date"), "gio": r.get("time"), "thu_muc": r.get("folder", "")}


def danh_sach(a):
    n = max(1, min(int(a.get("so_luong") or 10), 50))
    docs = board("GET", "/api/db/results").get("docs") or []
    docs = sorted((x for x in docs if not x.get("demo")), key=lambda r: str(r.get("created", "")), reverse=True)
    return [_gon(r) for r in docs[:n]]


def xem_viec(a):
    jid = str(a.get("job_id") or "").strip()
    if not re.fullmatch(r"[\w-]+", jid):
        raise RuntimeError("job_id không hợp lệ")
    r = board("GET", "/api/db/results/" + jid)
    return dict(_gon(r), ke_hoach=[{"phan": p.get("n"), "nhan_su": p.get("agent"), "viec": p.get("viec"), "trang_thai": p.get("state"),
                                     "tien_do": p.get("pct"), "ket_qua": str(p.get("out") or "")[:1500]} for p in r.get("plan") or []])


def doi_hinh(_a):
    return board("GET", "/api/v1/kit")


TOOLS = {
    "giao_viec": (giao_viec, "Giao một việc cho Đội Quân AI (Tâm Tổng Quản chia việc, các nhân sự làm thật, tiến độ hiện trên bảng).",
                  {"yeu_cau": {"type": "string", "description": "Yêu cầu đầy đủ"}, "tieu_de": {"type": "string", "description": "Tên ngắn của việc (không bắt buộc)"}}, ["yeu_cau"]),
    "xem_viec": (xem_viec, "Xem tiến độ và kết quả từng phần của một việc trên bảng.",
                 {"job_id": {"type": "string"}}, ["job_id"]),
    "danh_sach_viec": (danh_sach, "Liệt kê các việc gần đây trên bảng giao việc.",
                       {"so_luong": {"type": "integer", "description": "Số việc, mặc định 10"}}, []),
    "doi_hinh": (doi_hinh, "Xem hồ sơ doanh nghiệp, luật và đội hình đang bật trên bảng.", {}, []),
}


def handle(msg):
    method, mid = msg.get("method"), msg.get("id")
    if method == "initialize":
        ver = (msg.get("params") or {}).get("protocolVersion") or PROTOCOL
        return {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": ver, "capabilities": {"tools": {}},
                                                         "serverInfo": {"name": "doi-quan-ai", "version": "1.0.0"}}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": k, "description": v[1], "inputSchema": {"type": "object", "properties": v[2], "required": v[3]}} for k, v in TOOLS.items()]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        p = msg.get("params") or {}
        tool = TOOLS.get(p.get("name"))
        if not tool:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "Không có công cụ này"}}
        try:
            text, is_err = json.dumps(tool[0](p.get("arguments") or {}), ensure_ascii=False, indent=2), False
        except Exception as e:  # noqa: BLE001 - trả lỗi về Claude, không làm chết máy chủ
            text, is_err = str(e), True
        return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "Không hỗ trợ " + str(method)}}


def main():
    # Windows mặc định không dùng UTF-8 cho stdin/stdout, sẽ hỏng chữ tiếng Việt.
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            reply = handle(json.loads(line))
        except ValueError:
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "JSON hỏng"}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
