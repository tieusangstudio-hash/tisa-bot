#!/usr/bin/env python3
"""Thử bot Telegram: tìm Chat ID và gửi 1 tin nhắn mẫu. Chỉ dùng thư viện có sẵn của Python 3.

Token KHÔNG truyền qua tham số dòng lệnh (tránh lưu vào lịch sử lệnh) — đặt biến môi trường trước khi chạy.

macOS (Terminal):
    export TELEGRAM_BOT_TOKEN="dán-token-vào-đây"
    python3 scripts/thu_telegram.py tim-chat-id
    export TELEGRAM_CHAT_ID="số-vừa-tìm-được"
    python3 scripts/thu_telegram.py gui-thu

Windows (PowerShell):
    $env:TELEGRAM_BOT_TOKEN="dán-token-vào-đây"
    py scripts\\thu_telegram.py tim-chat-id
    $env:TELEGRAM_CHAT_ID="số-vừa-tìm-được"
    py scripts\\thu_telegram.py gui-thu

Trước khi chạy `tim-chat-id`: nhắn 1 tin bất kỳ cho bot (chat riêng), hoặc thêm bot vào nhóm rồi nhắn 1 tin trong nhóm.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime


def api(method, payload=None):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        sys.exit("Chưa đặt biến môi trường TELEGRAM_BOT_TOKEN. Xem hướng dẫn ở đầu file.")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        hint = {
            401: "Token sai hoặc đã bị thu hồi — lấy token mới ở @BotFather (/mybots → API Token).",
            400: "Chat ID sai, hoặc bạn chưa nhắn cho bot lần nào.",
            403: "Bot bị chặn hoặc đã bị xóa khỏi nhóm.",
        }.get(e.code, "")
        sys.exit(f"Lỗi Telegram {e.code}: {body}\n{hint}")


def tim_chat_id():
    me = api("getMe")["result"]
    print(f"Bot: {me.get('first_name')} (@{me.get('username')})")
    updates = api("getUpdates").get("result", [])
    seen = {}
    for u in updates:
        msg = u.get("message") or u.get("channel_post") or u.get("my_chat_member") or {}
        chat = msg.get("chat") or {}
        if chat.get("id") is not None:
            name = chat.get("title") or " ".join(filter(None, [chat.get("first_name"), chat.get("last_name")]))
            seen[chat["id"]] = (chat.get("type"), name)
    if not seen:
        print("Chưa thấy tin nhắn nào. Hãy nhắn 1 tin cho bot (hoặc trong nhóm có bot) rồi chạy lại.")
        print("Nếu bot đang gắn webhook, getUpdates sẽ trống — dùng @userinfobot để xem ID cá nhân.")
        return
    print("Các Chat ID tìm thấy:")
    for cid, (ctype, name) in seen.items():
        loai = "nhóm" if ctype in ("group", "supergroup") else ("kênh" if ctype == "channel" else "cá nhân")
        print(f"  {cid}   ({loai}: {name})")


def gui_thu():
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not chat_id:
        sys.exit("Chưa đặt biến môi trường TELEGRAM_CHAT_ID. Chạy `tim-chat-id` trước.")
    text = (
        "✅ <b>Bot báo đơn đã hoạt động</b>\n"
        f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        "Từ giờ có đơn/có tiền vào, tin nhắn sẽ hiện ở đây."
    )
    api("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
    print("Đã gửi tin thử. Mở Telegram trên điện thoại để kiểm tra.")


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else ""
    if lenh == "tim-chat-id":
        tim_chat_id()
    elif lenh == "gui-thu":
        gui_thu()
    else:
        print(__doc__)
