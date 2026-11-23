"""tisa_gon_ho_so.py - (V3.45, chủ yêu cầu 22/11 "tối ưu token mà công việc vẫn hiệu quả") Lời dặn của cộng sự khi CHỦ chat trong dashboard.

Đo 22/11 trên máy chủ: hồ sơ Trợ Lý Hằng dài 100.404 ký tự, riêng mục "PHẦN 5. SẢN PHẨM VÀ DỊCH VỤ" 78.650 ký tự. Mỗi lượt chủ chat
với Hằng (giao việc, hỏi han) nạp lại cả khối này, và mỗi vòng gọi công cụ đọc lại nó (lượt có 10-300 vòng). Phần lớn lượt không cần
toàn bộ danh mục sản phẩm.

Cách làm: mục nào trong lời dặn dài hơn NGUONG_MUC ký tự thì chỉ giữ đoạn đầu (thường là ý chính, giá, lịch) và một dòng chỉ đường:
cộng sự tự mở đúng tệp hồ sơ bằng công cụ Read khi cần chi tiết. Chỉ áp cho chat của CHỦ với cộng sự (trang Cộng sự, CLI, Telegram,
giọng nói); bot trả lời khách (Fanpage, Zalo) đi đường khác (chatbot_runtime) và vẫn nạp đủ như cũ.
"""
from __future__ import annotations

import os
import re

NGUONG_TONG = int(os.getenv("TISA_GON_HO_SO_TONG") or 40000)     # lời dặn ngắn hơn mức này: để nguyên
NGUONG_MUC = int(os.getenv("TISA_GON_HO_SO_MUC") or 12000)       # mục dài hơn mức này mới tách
GIU_DAU = 2500                                                    # ký tự đầu của mục được giữ lại
_TIEU_DE = re.compile(r"(?m)^(#{1,3}) .+$")


def gon(text: str, duong_dan: str = "") -> str:
    """Rút gọn lời dặn quá dài. Trả nguyên văn nếu không cần hoặc có gì bất thường."""
    s = str(text or "")
    if os.getenv("TISA_GON_HO_SO") == "0" or len(s) <= NGUONG_TONG:
        return s
    try:
        moc = [m for m in _TIEU_DE.finditer(s)]
        if not moc:
            return s
        ra, tu = [], 0
        da_tach = 0
        for i, m in enumerate(moc):
            dau = m.start()
            cuoi = moc[i + 1].start() if i + 1 < len(moc) else len(s)
            # mục con (### khi mục là ##) thuộc về mục cha: gộp tới tiêu đề cùng cấp hoặc cao hơn tiếp theo
            cap = len(m.group(1))
            j = i + 1
            # tiêu đề cấp 1 (#) thường bao trùm cả tệp: không coi là một mục để gom, chỉ gom mục con cho cấp 2 trở xuống
            while cap >= 2 and j < len(moc) and len(moc[j].group(1)) > cap:
                j += 1
            cuoi = moc[j].start() if j < len(moc) else len(s)
            if dau < tu:
                continue
            ra.append(s[tu:dau])
            muc = s[dau:cuoi]
            if len(muc) > NGUONG_MUC:
                giu = muc[:GIU_DAU].rsplit("\n", 1)[0]
                tieu_de = m.group(0).strip()
                ra.append(giu + "\n\n[... Phần còn lại của mục \"%s\" (%d ký tự) được tách ra để tiết kiệm token. Khi cần chi tiết trong mục này "
                          "(giá, lịch, nội dung, câu trả lời mẫu...), đọc tệp hồ sơ `%s` bằng công cụ Read rồi tìm đúng tiêu đề mục. "
                          "Đừng đoán khi chưa đọc.]\n\n" % (tieu_de.lstrip("# ")[:80], len(muc), duong_dan or "hồ sơ cộng sự"))
                da_tach += len(muc) - GIU_DAU
            else:
                ra.append(muc)
            tu = cuoi
        ra.append(s[tu:])
        kq = "".join(ra)
        return kq if da_tach > 0 and len(kq) < len(s) else s
    except Exception:  # noqa: BLE001 - rút gọn hỏng thì dùng nguyên văn, không được phá lượt chat
        return s
