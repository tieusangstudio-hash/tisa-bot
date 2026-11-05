"""tisa_quyen_qc.py - công cụ quảng cáo: chỉ tên nằm trong danh sách đọc mới là đọc, còn lại coi là nguy hiểm.

Phân loại chung của mcp_catalog lấy mặc định là "đọc" khi tên công cụ lạ. Với công cụ tiêu tiền thật thì mặc định đó sai:
máy chủ chính chủ thêm công cụ ghi mới là lọt ngay qua mức Chỉ đọc (Google `manage_labels`, Meta `ads_fb_partner_permission_manager`).
"""
from fnmatch import fnmatch

CHI_DOC = {
    "meta-ads": ("ads_get_*", "ads_insights_*", "ads_library_search", "ads_account_get_activity_logs", "ads_catalog_get_*", "ads_catalog_list_*",
                 "ads_catalog_event_source_get*", "ads_experiment_list_tests", "ads_experiment_*_get_test", "ads_experiment_check_eligibility",
                 "ads_pixel_*_read"),
    "google-ads": ("list_*", "get_*", "search", "search_*", "customers_*", "metadata_*"),
    "tiktok-ads": ("get_*", "*_get", "list_*"),
}
# Trong danh sách đọc mà vẫn có quyền ghi: chặn trước.
KHONG_BAO_GIO_DOC = ("*_create*", "*_update*", "*_delete*", "*_activate*", "*permission*", "*_boost*", "*_upload*", "manage_*")


def loai(connector_id, tool):
    """'read' hoặc 'danger' cho công cụ quảng cáo; None nếu kết nối này không phải quảng cáo."""
    mau = CHI_DOC.get(str(connector_id or ""))
    if mau is None:
        return None
    t = str(tool or "").lower()
    if any(fnmatch(t, m) for m in KHONG_BAO_GIO_DOC):
        return "danger"
    return "read" if any(fnmatch(t, m) for m in mau) else "danger"


def sua_the(by_id):
    """Thẻ kết nối trong kho còn ghi tình trạng cũ. Sửa lúc nạp để máy đã cài gói cũ cũng thấy đúng."""
    g = by_id.get("meta-ads-graph")
    if g:
        g["name"] = "Meta Ads (tự tạo app, chỉ đọc)"
    m = by_id.get("meta-ads")
    if m:
        m["name"] = "Meta Ads (MCP chính chủ của Meta)"
        m["description"] = "Máy chủ MCP chính chủ của Meta, có cả công cụ tạo chiến dịch. Chỉ cần xem số liệu thì dùng thẻ Meta Ads (tự tạo app, chỉ đọc)."
        a = m.get("auth")
        if isinstance(a, dict):
            a["guide"] = ("Meta đã cho nối máy chủ này bằng app của chính bạn, xem hướng dẫn ở liên kết bên dưới. TISA BOT chưa kiểm chứng trọn đường này, "
                          "nên có thể bấm Kết nối vẫn báo lỗi.\n\nChỉ cần xem số liệu thì dùng thẻ Meta Ads (tự tạo app, chỉ đọc).")
            a["guide_url"] = "https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started"
