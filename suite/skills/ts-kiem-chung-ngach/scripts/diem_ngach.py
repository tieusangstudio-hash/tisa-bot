#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính "Điểm ngách" 100 điểm có trọng số + ước tính quy mô thị trường.
Thuộc skill /ts-kiem-chung-ngach (Bộ skill TISA AI Agent).

CÁCH CHẠY (chỉ cần Python 3, không cài thêm gì):
  macOS:    python3 diem_ngach.py vi-du-ngach.json
  Windows:  py diem_ngach.py vi-du-ngach.json

TÙY CHỌN:
  --out bao-cao-diem.md   Lưu kết quả ra file Markdown.
  --ngay 2026-11-04       Ngày kiểm tra hôm nay (để cảnh báo nguồn cũ quá 180 ngày).

CÁCH TÍNH:
  Mỗi tiêu chí chấm 0–10. Điểm quy đổi = điểm × trọng số ÷ 10. Tổng trọng số = 100.
  >= 70 : NÊN LÀM
  50–69 : LÀM CÓ ĐIỀU KIỆN
  < 50  : KHÔNG NÊN
  Luật chặn: 'muc_do_dau' hoặc 'kha_nang_chi_tra' <= 3 thì KHÔNG được ra NÊN LÀM.
  Luật bằng chứng: tiêu chí nào có ít hơn 3 nguồn (link khác nhau) sẽ bị cảnh báo;
  nếu đó là 'muc_do_dau' hoặc 'kha_nang_chi_tra' thì không được ra NÊN LÀM.
  Tiêu chí 'phu_hop_nguoi_lam' là tự đánh giá, không bắt buộc nguồn web.
"""

import argparse
import datetime as dt
import json
import sys
from urllib.parse import urlparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Bộ tiêu chí mặc định (mã, tên, trọng số, ý nghĩa điểm 10)
TIEU_CHI = [
    ("muc_do_dau", "Mức độ đau / cấp thiết", 20,
     "Khách đang khổ thật, cần giải quyết sớm, đã từng chi tiền cho cách khác"),
    ("kha_nang_chi_tra", "Khả năng & sẵn lòng chi trả", 20,
     "Khách có tiền và đã quen trả tiền cho thứ tương tự ở mức giá bạn muốn bán"),
    ("nhu_cau_tim_kiem", "Nhu cầu tìm kiếm", 15,
     "Nhiều người chủ động tìm trên Google/YouTube/TikTok/sàn, có số liệu cụ thể"),
    ("xu_huong", "Xu hướng", 10,
     "Quan tâm đang tăng đều 12–24 tháng, không phải trào lưu chớp nhoáng"),
    ("canh_tranh", "Mức cạnh tranh (có chỗ trống)", 10,
     "Có người bán (chứng tỏ có tiền) nhưng còn góc chưa ai làm tốt; 10 = còn nhiều chỗ trống"),
    ("kenh_tiep_can", "Kênh tiếp cận khách", 15,
     "Biết rõ khách tụ tập ở đâu, tiếp cận được với chi phí thấp"),
    ("phu_hop_nguoi_lam", "Độ phù hợp với người làm", 10,
     "Bạn có kỹ năng, kinh nghiệm, uy tín hoặc nguồn lực để làm tốt hơn mặt bằng chung"),
]
CHAN = {"muc_do_dau", "kha_nang_chi_tra"}
TU_DANH_GIA = {"phu_hop_nguoi_lam"}  # dựa trên hồ sơ người làm, không cần nguồn web
NGUONG_NEN = 70
NGUONG_DIEU_KIEN = 50


def loi(tb):
    print("LỖI: " + tb, file=sys.stderr)
    sys.exit(1)


def md(x):
    return str(x if x is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def so(x, le=1):
    s = f"{x:,.{le}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def tien(x):
    """Định dạng tiền VND gọn: tỷ / triệu / nghìn."""
    if x >= 1e9:
        return so(x / 1e9, 2) + " tỷ đ"
    if x >= 1e6:
        return so(x / 1e6, 1) + " triệu đ"
    if x >= 1e3:
        return so(x / 1e3, 0) + " nghìn đ"
    return so(x, 0) + " đ"


def ten_mien(link):
    try:
        h = urlparse(str(link)).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def doc_ngay(s):
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(description="Tính Điểm ngách 100 điểm có trọng số.")
    p.add_argument("file_json")
    p.add_argument("--out")
    p.add_argument("--ngay", help="Ngày kiểm tra (YYYY-MM-DD), mặc định hôm nay")
    a = p.parse_args()

    try:
        with open(a.file_json, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
    except FileNotFoundError:
        loi(f"Không tìm thấy file '{a.file_json}'.")
    except json.JSONDecodeError as e:
        loi(f"JSON sai cú pháp ở dòng {e.lineno}, cột {e.colno}: {e.msg}.")

    hom_nay = doc_ngay(a.ngay) if a.ngay else dt.date.today()

    # Trọng số: cho phép ghi đè nhưng tổng phải = 100
    trong_so = {ma: ts for ma, _, ts, _ in TIEU_CHI}
    trong_so.update(d.get("trong_so", {}) or {})
    tong_ts = sum(trong_so[ma] for ma, *_ in TIEU_CHI)
    if abs(tong_ts - 100) > 0.01:
        loi(f"Tổng trọng số đang là {tong_ts}, phải bằng 100.")

    nhap = {t.get("ma"): t for t in d.get("tieu_chi", []) if isinstance(t, dict)}
    thieu = [ma for ma, *_ in TIEU_CHI if ma not in nhap]
    if thieu:
        loi("Thiếu tiêu chí: " + ", ".join(thieu) + ". Xem file mẫu vi-du-ngach.json.")

    dong, canh_bao, tong = [], [], 0.0
    bi_chan, thieu_bang_chung = [], []
    for ma, ten, _, _ in TIEU_CHI:
        t = nhap[ma]
        try:
            diem = float(t.get("diem"))
        except (TypeError, ValueError):
            loi(f"Tiêu chí '{ma}': 'diem' phải là số 0–10.")
        if not 0 <= diem <= 10:
            loi(f"Tiêu chí '{ma}': điểm {diem} nằm ngoài 0–10.")
        ts = trong_so[ma]
        quy_doi = diem * ts / 10
        tong += quy_doi

        nguon = t.get("nguon", []) or []
        links = {str(n.get("link")).strip().rstrip("/").lower()
                 for n in nguon if isinstance(n, dict) and n.get("link")}
        mien = {ten_mien(l) for l in links} - {""}
        so_nguon = len(links)
        if ma in TU_DANH_GIA:
            pass  # tiêu chí tự đánh giá, không bắt buộc 3 nguồn web
        elif so_nguon < 3:
            canh_bao.append(f"- **{ten}**: mới có {so_nguon} nguồn (cần ≥ 3 nguồn độc lập) → điểm này chưa đủ tin cậy.")
            if ma in CHAN:
                thieu_bang_chung.append(ten)
        elif len(mien) < 2:
            canh_bao.append(f"- **{ten}**: cả {so_nguon} nguồn đều từ một nền tảng ({', '.join(sorted(mien))}) "
                            "→ nên thêm nguồn từ nơi khác cho khách quan.")
        for n in nguon:
            nd = doc_ngay(n.get("ngay")) if isinstance(n, dict) else None
            if isinstance(n, dict) and n.get("link") and nd is None:
                canh_bao.append(f"- **{ten}**: nguồn {md(n.get('link'))} chưa ghi ngày kiểm tra.")
            elif nd and hom_nay and (hom_nay - nd).days > 180:
                canh_bao.append(f"- **{ten}**: nguồn {md(n.get('link'))} kiểm tra đã hơn 180 ngày → nên kiểm lại.")
        if ma in CHAN and diem <= 3:
            bi_chan.append(ten)

        dong.append(f"| {ten} | {so(ts, 0)} | {so(diem)} | **{so(quy_doi)}** | {so_nguon} | {md(t.get('bang_chung')) or '—'} |")

    tong = round(tong, 1)
    if tong >= NGUONG_NEN and not bi_chan and not thieu_bang_chung:
        ket_luan = "NÊN LÀM"
        giai_thich = "Tín hiệu tốt. Vẫn chạy phép thử trả tiền trước khi đầu tư lớn."
    elif tong >= NGUONG_DIEU_KIEN:
        ket_luan = "LÀM CÓ ĐIỀU KIỆN"
        giai_thich = "Chỉ làm khi phép thử trả tiền đạt ngưỡng; tập trung sửa tiêu chí điểm thấp nhất."
    else:
        ket_luan = "KHÔNG NÊN"
        giai_thich = "Rủi ro cao. Đổi góc ngách (khách khác, vấn đề hẹp hơn) rồi kiểm chứng lại."
    if bi_chan:
        canh_bao.insert(0, "- **Luật chặn:** " + ", ".join(bi_chan) +
                        " ≤ 3 điểm → không được kết luận NÊN LÀM dù tổng điểm cao.")
    if thieu_bang_chung and tong >= NGUONG_NEN:
        canh_bao.insert(0, "- **Thiếu bằng chứng:** " + ", ".join(thieu_bang_chung) +
                        " chưa đủ 3 nguồn → tạm hạ xuống LÀM CÓ ĐIỀU KIỆN cho tới khi bổ sung.")

    ra = [f"# Điểm ngách — {md(d.get('y_tuong', 'chưa đặt tên'))}", ""]
    if d.get("khach_hang"):
        ra += [f"Khách hàng: {md(d['khach_hang'])}", ""]
    ra += ["| Tiêu chí | Trọng số | Điểm /10 | Quy đổi | Số nguồn | Bằng chứng chính |",
           "|---|---:|---:|---:|---:|---|"]
    ra += dong
    ra += [f"| **TỔNG** | **100** | | **{so(tong)} / 100** | | |", ""]
    ra += [f"## Kết luận: **{ket_luan}** ({so(tong)}/100)", "", giai_thich, ""]
    ra += [f"Ngưỡng: ≥ {NGUONG_NEN} NÊN LÀM · {NGUONG_DIEU_KIEN}–{NGUONG_NEN - 1} LÀM CÓ ĐIỀU KIỆN · "
           f"< {NGUONG_DIEU_KIEN} KHÔNG NÊN.", ""]

    # Ước tính quy mô thị trường
    tt = d.get("thi_truong")
    if isinstance(tt, dict) and tt:
        try:
            n = float(tt["tong_so_khach"])
            gia_tri = float(tt["chi_tieu_moi_khach_nam"])
            voi_toi = float(tt["ti_le_voi_toi"])
            chiem = float(tt["ti_le_chiem_nam_dau"])
        except (KeyError, TypeError, ValueError):
            loi("'thi_truong' cần đủ: tong_so_khach, chi_tieu_moi_khach_nam, ti_le_voi_toi, ti_le_chiem_nam_dau.")
        tong_tt = n * gia_tri
        voi_toi_tt = tong_tt * voi_toi
        chiem_tt = voi_toi_tt * chiem
        so_khach_chiem = n * voi_toi * chiem
        ra += ["## Ước tính quy mô thị trường (đơn giản, có giả định)", "",
               "| Tầng | Cách tính | Số khách | Giá trị/năm |",
               "|---|---|---:|---:|",
               f"| Tổng thị trường | {so(n, 0)} khách × {tien(gia_tri)}/năm | {so(n, 0)} | {tien(tong_tt)} |",
               f"| Phần với tới được | × {so(voi_toi * 100)}% (kênh, khu vực, ngôn ngữ bạn phục vụ được) | "
               f"{so(n * voi_toi, 0)} | {tien(voi_toi_tt)} |",
               f"| Phần chiếm được năm đầu | × {so(chiem * 100)}% | {so(so_khach_chiem, 0)} | **{tien(chiem_tt)}** |",
               ""]
        if tt.get("gia_dinh"):
            ra += ["Giả định: " + md(tt["gia_dinh"]), ""]
        if chiem > 0.05:
            canh_bao.append(f"- Tỉ lệ chiếm năm đầu {so(chiem * 100)}% là khá lạc quan với người mới (thường 0,5–3%).")

    ra += ["## Cảnh báo", ""]
    ra += canh_bao if canh_bao else ["- Không có cảnh báo."]
    van_ban = "\n".join(ra) + "\n"
    print(van_ban)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(van_ban)
        print(f"Đã lưu: {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
