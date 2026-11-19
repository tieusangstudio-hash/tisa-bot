"""Địa chỉ HTTPS cho hộp Kết nối Meta khi trang TISA BOT đang mở bằng http (127.0.0.1, địa chỉ mạng LAN).

Facebook chỉ nhận địa chỉ quay về HTTPS. Bản gốc lấy địa chỉ theo đúng cái trình duyệt đang dùng, nên học viên mở TISA BOT bằng
http://127.0.0.1:... thì nút "Đăng nhập Facebook" bị khóa dù máy đã bật Truy cập từ xa (đường hầm Cloudflare) và đã có địa chỉ https công khai.
Ở đây: trang đang https thì giữ nguyên; đang http mà đường hầm của chính máy này đang chạy thì dùng địa chỉ https của đường hầm.
Không đụng gì tới máy khác: đọc đúng đường hầm của máy đang chạy TISA BOT này."""


def https_base(base: str) -> str:
    base = str(base or "")
    if base.startswith("https://"):
        return base
    try:
        import remote_tunnel as rt
        m = rt.MANAGER
        if getattr(m, "state", "") != "running":
            return base
        url = str(getattr(m, "url", "") or "")
        if not url:
            hosts = [h for h, _ in (getattr(m, "ingress", None) or [])]
            url = ("https://" + hosts[0]) if hosts else ""
        if url.startswith("https://"):
            return url.rstrip("/")
    except Exception:  # noqa: BLE001 - lỗi đọc đường hầm thì giữ địa chỉ cũ, không làm hỏng hộp Kết nối
        pass
    return base
