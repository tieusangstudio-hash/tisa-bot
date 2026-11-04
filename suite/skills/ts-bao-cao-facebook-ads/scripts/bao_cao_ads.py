#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bao_cao_ads.py — Đọc file CSV xuất từ Trình quản lý quảng cáo Meta (Facebook / Instagram Ads),
TÍNH LẠI các chỉ số từ số gốc và xuất báo cáo dạng bảng Markdown (tiếng Việt).

Chỉ dùng thư viện có sẵn của Python 3.8+ — KHÔNG cần cài thêm gì.

CÁCH CHẠY
  macOS / Linux : python3 scripts/bao_cao_ads.py duong-dan/file.csv
  Windows       : py scripts\\bao_cao_ads.py duong-dan\\file.csv

  Chạy thử với file mẫu đi kèm:
  macOS / Linux : python3 scripts/bao_cao_ads.py assets/mau-xuat-ads-manager.csv --cpa-muc-tieu 60000
  Windows       : py scripts\\bao_cao_ads.py assets\\mau-xuat-ads-manager.csv --cpa-muc-tieu 60000

TÙY CHỌN
  --cpa-muc-tieu 80000        Chi phí/kết quả mục tiêu (cùng đơn vị tiền với file).
                              Không nhập thì so với trung bình của chính tài khoản (theo từng loại kết quả).
  --tan-suat-canh-bao 3       Ngưỡng tần suất để cảnh báo quảng cáo bị "mỏi" (mặc định 3).
  --cap tu-dong|chien-dich|nhom|quang-cao
                              Gộp dữ liệu theo cấp nào (mặc định: cấp chi tiết nhất có trong file).
  --dau-thap-phan tu-dong|.|, Dấu thập phân trong file (mặc định tự đoán).
  --cot khoa=Tên cột          Chỉ định tay tên cột khi tự nhận diện sai (dùng được nhiều lần).
                              Khóa hợp lệ: campaign, adset, ad, start, end, spend, impressions, reach,
                              clicks_link, clicks_all, results, result_type, leads, purchases,
                              purchase_value, messages, video_3s, thruplay.
  --ra bao-cao.md             Ghi báo cáo ra file (mặc định in ra màn hình).
  --xuat-csv chuan-hoa.csv    Ghi thêm bản dữ liệu đã chuẩn hóa (file gốc KHÔNG bị sửa).

GHI CHÚ CHO AI
  - Script chỉ ĐỌC file, không kết nối mạng, không thay đổi quảng cáo.
  - Đề xuất GIỮ / THEO DÕI / THỬ MỚI / GIẢM / TẮT chỉ là gợi ý theo ngưỡng, người dùng phải duyệt.
  - Nếu cảnh báo "không tìm thấy cột", hỏi người dùng tên cột thật rồi chạy lại với --cot.
"""

import argparse
import csv
import io
import os
import re
import sys
import unicodedata

# ---------------------------------------------------------------------------
# Tiện ích chữ & số
# ---------------------------------------------------------------------------


def bo_dau(s):
    """Bỏ dấu tiếng Việt, chữ thường, gom khoảng trắng, bỏ ký tự đặc biệt."""
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def doc_so(raw, dau_thap_phan="tu-dong"):
    """Đổi chuỗi số (có thể có dấu chấm/phẩy, ký hiệu tiền, %) thành float. Trả về None nếu trống."""
    if raw is None:
        return None
    s = str(raw).strip()
    if s == "" or s in {"-", "—", "–"} or bo_dau(s) in {"n a", "na", "none", "null"}:
        return None
    s = re.sub(r"[^0-9,.\-]", "", s)
    if s in {"", "-", ".", ","}:
        return None
    if dau_thap_phan == ".":
        s = s.replace(",", "")
    elif dau_thap_phan == ",":
        s = s.replace(".", "").replace(",", ".")
    else:
        if "." in s and "," in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "," in s:
            if re.fullmatch(r"-?\d{1,3}(,\d{3})+", s):
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
        elif "." in s:
            if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
                s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def chia(a, b, nhan=1.0):
    if a is None or b is None or b == 0:
        return None
    return a / b * nhan


def fmt_so(x, le=0):
    """Định dạng kiểu Việt Nam: 1.234.567,89"""
    if x is None:
        return "—"
    s = f"{x:,.{le}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def fmt_tien(x, tien_te=""):
    if x is None:
        return "—"
    le = 0 if (tien_te in {"VND", "đ", ""} or abs(x) >= 1000) else 2
    return fmt_so(x, le) + (f" {tien_te}" if tien_te else "")


def fmt_pt(x):
    return "—" if x is None else fmt_so(x, 2) + "%"


def md(s):
    return str(s).replace("|", "/").replace("\n", " ").strip() or "(không tên)"


# ---------------------------------------------------------------------------
# Nhận diện cột (tiếng Việt và tiếng Anh)
# ---------------------------------------------------------------------------

LOAI_TRU_CHI_PHI = ("cost", "chi phi", "cpm", "cpc", "ctr", "gia tri", "value", "roas", "unique", "duy nhat")


def _co(h, *cum):
    return any(c in h for c in cum)


def _dau(h, *cum):
    return any(h.startswith(c) for c in cum)


QUY_TAC_COT = [
    ("campaign", lambda h: _dau(h, "campaign name", "ten chien dich")),
    ("adset", lambda h: _dau(h, "ad set name", "ten nhom quang cao")),
    ("ad", lambda h: _dau(h, "ad name", "ten quang cao")),
    ("start", lambda h: _dau(h, "reporting starts", "bat dau bao cao", "ngay bat dau")),
    ("end", lambda h: _dau(h, "reporting ends", "ket thuc bao cao", "ngay ket thuc")),
    ("spend", lambda h: _co(h, "amount spent", "so tien da chi") or _dau(h, "spend", "chi tieu")),
    ("impressions", lambda h: _dau(h, "impressions", "luot hien thi") and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("reach", lambda h: _dau(h, "reach", "nguoi tiep can", "tiep can", "luot tiep can")
     and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("clicks_link", lambda h: _dau(h, "link clicks", "luot click vao lien ket", "luot nhap vao lien ket")
     and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("clicks_all", lambda h: _dau(h, "clicks all", "luot click tat ca", "luot nhap tat ca")
     and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("result_type", lambda h: _dau(h, "result indicator", "result type", "chi bao ket qua", "loai ket qua")),
    ("results", lambda h: h in {"results", "ket qua"}),
    ("leads", lambda h: (_dau(h, "leads", "khach hang tiem nang") and not _co(h, *LOAI_TRU_CHI_PHI))),
    ("purchase_value", lambda h: _co(h, "purchases conversion value", "purchase conversion value",
                                     "gia tri chuyen doi luot mua", "gia tri chuyen doi mua hang")),
    ("purchases", lambda h: h in {"purchases", "website purchases", "luot mua", "luot mua tren trang web",
                                  "luot mua hang"}),
    ("messages", lambda h: _co(h, "messaging conversations started", "cuoc tro chuyen qua tin nhan",
                               "cuoc tro chuyen bang tin nhan") and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("video_3s", lambda h: (_co(h, "3 second video plays") or (_co(h, "3 giay") and _co(h, "video", "phat")))
     and not _co(h, *LOAI_TRU_CHI_PHI)),
    ("thruplay", lambda h: _dau(h, "thruplays", "thruplay", "luot thruplay") and not _co(h, *LOAI_TRU_CHI_PHI)),
    # Cột do Ads Manager tự tính — chỉ dùng để ĐỐI CHIẾU, không dùng để tính
    ("given_cpm", lambda h: _dau(h, "cpm")),
    ("given_ctr_link", lambda h: _dau(h, "ctr") and _co(h, "link", "lien ket")),
    ("given_cpc_link", lambda h: _dau(h, "cpc") and _co(h, "link", "lien ket")),
    ("given_cpr", lambda h: _dau(h, "cost per result", "chi phi tren moi ket qua")),
]

TEN_KHOA = {
    "campaign": "Tên chiến dịch", "adset": "Tên nhóm quảng cáo", "ad": "Tên quảng cáo",
    "start": "Ngày bắt đầu", "end": "Ngày kết thúc", "spend": "Số tiền đã chi tiêu",
    "impressions": "Lượt hiển thị", "reach": "Người tiếp cận", "clicks_link": "Lượt click vào liên kết",
    "clicks_all": "Lượt click (tất cả)", "results": "Kết quả", "result_type": "Chỉ báo kết quả",
    "leads": "Khách hàng tiềm năng", "purchases": "Lượt mua", "purchase_value": "Giá trị chuyển đổi lượt mua",
    "messages": "Cuộc trò chuyện qua tin nhắn", "video_3s": "Lượt phát video 3 giây", "thruplay": "ThruPlay",
}

SO_GOC = ["spend", "impressions", "reach", "clicks_link", "clicks_all", "results", "leads", "purchases",
          "purchase_value", "messages", "video_3s", "thruplay"]


def nhan_dien_cot(tieu_de, chi_dinh):
    """Trả về dict khóa -> chỉ số cột."""
    ket_qua = {}
    da_dung = set()
    chuan = [bo_dau(t) for t in tieu_de]
    for khoa, ten in chi_dinh.items():
        for i, t in enumerate(tieu_de):
            if t.strip() == ten.strip() or bo_dau(t) == bo_dau(ten):
                ket_qua[khoa] = i
                da_dung.add(i)
                break
    for khoa, ham in QUY_TAC_COT:
        if khoa in ket_qua:
            continue
        for i, h in enumerate(chuan):
            if i in da_dung:
                continue
            if ham(h):
                ket_qua[khoa] = i
                da_dung.add(i)
                break
    return ket_qua


def tien_te_tu_tieu_de(tieu_de, idx):
    if idx is None:
        return ""
    m = re.search(r"\(([A-Z]{3})\)", tieu_de[idx])
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# Đọc file
# ---------------------------------------------------------------------------


def doc_csv(duong_dan):
    with open(duong_dan, "rb") as f:
        du_lieu = f.read()
    van_ban = None
    if du_lieu.startswith(b"\xff\xfe") or du_lieu.startswith(b"\xfe\xff"):
        van_ban = du_lieu.decode("utf-16")
    else:
        for ma in ("utf-8-sig", "cp1258", "latin-1"):
            try:
                van_ban = du_lieu.decode(ma)
                break
            except UnicodeDecodeError:
                continue
    mau = van_ban[:4096]
    try:
        dialect = csv.Sniffer().sniff(mau, delimiters=",;\t")
        dau_phan_cach = dialect.delimiter
    except csv.Error:
        dau_phan_cach = ","
    dong = list(csv.reader(io.StringIO(van_ban), delimiter=dau_phan_cach))
    dong = [d for d in dong if any(o.strip() for o in d)]
    return dong, dau_phan_cach


def doan_dau_thap_phan(dong, chi_so_cot):
    """Đoán dấu thập phân cho CẢ FILE dựa trên các ô số (tránh đọc nhầm '1.234' từng ô)."""
    cham = phay = 0
    for d in dong:
        for i in chi_so_cot:
            if i >= len(d):
                continue
            s = re.sub(r"[^0-9,.\-]", "", d[i])
            if re.fullmatch(r"-?\d{1,3}(,\d{3})+\.\d+", s) or (
                    re.fullmatch(r"-?\d+\.\d+", s) and len(s.split(".")[1]) != 3):
                cham += 1
            elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+,\d+", s) or (
                    re.fullmatch(r"-?\d+,\d+", s) and len(s.split(",")[1]) != 3):
                phay += 1
    if cham > phay:
        return "."
    if phay > cham:
        return ","
    return "tu-dong"


def tim_dong_tieu_de(dong):
    for i, d in enumerate(dong[:15]):
        cot = nhan_dien_cot(d, {})
        if "spend" in cot or "campaign" in cot or "impressions" in cot:
            return i
    return 0


# ---------------------------------------------------------------------------
# Tính toán
# ---------------------------------------------------------------------------


def tinh_kpi(g):
    k = dict(g)
    k["freq"] = chia(g.get("impressions"), g.get("reach"))
    k["cpm"] = chia(g.get("spend"), g.get("impressions"), 1000)
    k["ctr_link"] = chia(g.get("clicks_link"), g.get("impressions"), 100)
    k["ctr_all"] = chia(g.get("clicks_all"), g.get("impressions"), 100)
    k["cpc"] = chia(g.get("spend"), g.get("clicks_link"))
    k["cpr"] = chia(g.get("spend"), g.get("kq")) if g.get("kq") else None
    k["cvr"] = chia(g.get("kq"), g.get("clicks_link"), 100)
    k["cpl"] = chia(g.get("spend"), g.get("leads")) if g.get("leads") else None
    k["cpa_mua"] = chia(g.get("spend"), g.get("purchases")) if g.get("purchases") else None
    k["roas"] = chia(g.get("purchase_value"), g.get("spend"))
    k["cp_tin_nhan"] = chia(g.get("spend"), g.get("messages")) if g.get("messages") else None
    k["hook"] = chia(g.get("video_3s"), g.get("impressions"), 100)
    k["thruplay_rate"] = chia(g.get("thruplay"), g.get("impressions"), 100)
    return k


def de_xuat(k, ref, nguong_tan_suat):
    spend = k.get("spend") or 0
    kq = k.get("kq") or 0
    if spend <= 0:
        return "—", "—"
    if kq >= 10:
        tin_cay = "Cao"
    elif kq >= 3:
        tin_cay = "Trung bình"
    else:
        tin_cay = "Thấp"
    if not ref:
        quyet = "THEO DÕI (chưa có mốc so sánh)"
    elif kq == 0:
        quyet = "TẮT (cân nhắc)" if spend >= 2 * ref else "THEO DÕI (chưa đủ dữ liệu)"
    else:
        ti_le = k["cpr"] / ref
        if ti_le <= 0.8:
            quyet = "GIỮ (ứng viên tăng ngân sách)"
        elif ti_le <= 1.2:
            quyet = "GIỮ"
        elif ti_le <= 1.5:
            quyet = "THEO DÕI"
        else:
            quyet = "GIẢM"
    if k.get("freq") and k["freq"] >= nguong_tan_suat:
        quyet += " + THỬ MỚI creative"
    return quyet, tin_cay


def lech(given, tinh):
    if given is None or tinh is None or tinh == 0:
        return False
    return abs(given - tinh) / abs(tinh) > 0.05


# ---------------------------------------------------------------------------
# Chương trình chính
# ---------------------------------------------------------------------------


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Báo cáo Facebook Ads từ file CSV xuất từ Ads Manager.")
    ap.add_argument("file_csv")
    ap.add_argument("--cpa-muc-tieu", type=float, default=None)
    ap.add_argument("--tan-suat-canh-bao", type=float, default=3.0)
    ap.add_argument("--cap", choices=["tu-dong", "chien-dich", "nhom", "quang-cao"], default="tu-dong")
    ap.add_argument("--dau-thap-phan", choices=["tu-dong", ".", ","], default="tu-dong")
    ap.add_argument("--cot", action="append", default=[], help="khoa=Tên cột")
    ap.add_argument("--ra", default=None)
    ap.add_argument("--xuat-csv", default=None)
    a = ap.parse_args()

    if not os.path.isfile(a.file_csv):
        print(f"Không tìm thấy file: {a.file_csv}")
        sys.exit(1)

    chi_dinh = {}
    for c in a.cot:
        if "=" in c:
            k, v = c.split("=", 1)
            chi_dinh[k.strip()] = v.strip()

    dong, dau_pc = doc_csv(a.file_csv)
    if not dong:
        print("File trống.")
        sys.exit(1)
    i_td = tim_dong_tieu_de(dong)
    tieu_de = dong[i_td]
    cot = nhan_dien_cot(tieu_de, chi_dinh)
    tien_te = tien_te_tu_tieu_de(tieu_de, cot.get("spend"))
    canh_bao = []
    chat_luong = []
    if a.dau_thap_phan == "tu-dong":
        cot_so = [i for k, i in cot.items() if k in SO_GOC or k.startswith("given_")]
        a.dau_thap_phan = doan_dau_thap_phan(dong[i_td + 1:], cot_so)

    thieu_quan_trong = [k for k in ("spend", "impressions") if k not in cot]
    if thieu_quan_trong:
        print("Không tìm thấy cột bắt buộc: " + ", ".join(TEN_KHOA[k] for k in thieu_quan_trong))
        print("Các cột có trong file: " + " | ".join(tieu_de))
        print("Hãy chạy lại với --cot, ví dụ: --cot \"spend=Số tiền đã chi tiêu (VND)\"")
        sys.exit(2)

    # Cấp gộp
    co_cap = [c for c in ("campaign", "adset", "ad") if c in cot]
    if a.cap == "tu-dong":
        cap = co_cap[-1] if co_cap else None
    else:
        cap = {"chien-dich": "campaign", "nhom": "adset", "quang-cao": "ad"}[a.cap]
        if cap not in cot:
            canh_bao.append(f"File không có cột cấp '{a.cap}', dùng cấp chi tiết nhất có sẵn.")
            cap = co_cap[-1] if co_cap else None
    ten_cap = {"campaign": "chiến dịch", "adset": "nhóm quảng cáo", "ad": "quảng cáo", None: "toàn tài khoản"}[cap]
    duong_cap = co_cap[: co_cap.index(cap) + 1] if cap else []

    # Đọc từng dòng
    nhom = {}
    thu_tu = []
    bo_qua = 0
    tong_file = None
    ngay = []
    loai_kq_set = set()
    dong_lech = {"CPM": 0, "CTR (liên kết)": 0, "CPC (liên kết)": 0, "Chi phí/kết quả": 0}
    vi_du_lech = []
    chuan_hoa = []

    def lay(d, khoa):
        i = cot.get(khoa)
        if i is None or i >= len(d):
            return ""
        return d[i]

    for d in dong[i_td + 1:]:
        ten_dau = bo_dau(" ".join(lay(d, c) for c in co_cap)) if co_cap else ""
        if ten_dau.startswith(("results from", "ket qua tu", "total", "tong")):
            tong_file = d
            continue
        so = {k: doc_so(lay(d, k), a.dau_thap_phan) for k in SO_GOC if k in cot}
        if all(v is None for v in so.values()):
            bo_qua += 1
            continue
        loai_kq = lay(d, "result_type").strip() if "result_type" in cot else ""
        if "results" in cot:
            kq = so.get("results")
            if loai_kq:
                loai_kq_set.add(loai_kq)
        elif "purchases" in cot:
            kq, loai_kq = so.get("purchases"), "Lượt mua"
        elif "leads" in cot:
            kq, loai_kq = so.get("leads"), "Khách hàng tiềm năng"
        elif "messages" in cot:
            kq, loai_kq = so.get("messages"), "Cuộc trò chuyện qua tin nhắn"
        else:
            kq = None
        for c in ("start", "end"):
            v = lay(d, c).strip()
            if v:
                ngay.append(v)

        # Đối chiếu cột Ads Manager tự tính
        tinh = tinh_kpi({**so, "kq": kq})
        cap_doi = [
            ("CPM", "given_cpm", "cpm"), ("CTR (liên kết)", "given_ctr_link", "ctr_link"),
            ("CPC (liên kết)", "given_cpc_link", "cpc"), ("Chi phí/kết quả", "given_cpr", "cpr"),
        ]
        for nhan, k_given, k_tinh in cap_doi:
            if k_given in cot and lech(doc_so(lay(d, k_given), a.dau_thap_phan), tinh.get(k_tinh)):
                dong_lech[nhan] += 1
                if len(vi_du_lech) < 3:
                    vi_du_lech.append(f"{md(lay(d, cap) if cap else 'dòng')}: {nhan} trong file = "
                                      f"{lay(d, k_given)}, tính lại = {fmt_so(tinh.get(k_tinh), 2)}")

        khoa = tuple(lay(d, c).strip() for c in duong_cap) + (loai_kq,)
        if khoa not in nhom:
            nhom[khoa] = {k: None for k in SO_GOC}
            nhom[khoa].update({"kq": None, "so_dong": 0, "loai_kq": loai_kq,
                               "ten": md(lay(d, cap)) if cap else "Toàn tài khoản",
                               "cha": md(lay(d, duong_cap[-2])) if len(duong_cap) >= 2 else ""})
            thu_tu.append(khoa)
        g = nhom[khoa]
        g["so_dong"] += 1
        for k, v in list(so.items()) + [("kq", kq)]:
            if v is not None:
                g[k] = (g[k] or 0) + v
        chuan_hoa.append({**{TEN_KHOA.get(c, c): lay(d, c) for c in co_cap},
                          **{TEN_KHOA[k]: ("" if v is None else v) for k, v in so.items()},
                          "Kết quả dùng để tính": "" if kq is None else kq, "Loại kết quả": loai_kq})

    if not nhom:
        print("Không đọc được dòng dữ liệu nào. Kiểm tra lại file CSV.")
        sys.exit(1)

    ds = [tinh_kpi(nhom[k]) for k in thu_tu]

    # Tổng
    tong = {k: None for k in SO_GOC}
    tong["kq"] = None
    for g in ds:
        for k in SO_GOC + ["kq"]:
            if g.get(k) is not None:
                tong[k] = (tong[k] or 0) + g[k]
    T = tinh_kpi(tong)

    # Chỉ số theo trường tùy chọn: chỉ tính trên các dòng CÓ trường đó (tránh trộn mục tiêu khác nhau)
    def tong_neu_co(truong, cot_tong):
        return sum((g.get(cot_tong) or 0) for g in ds if g.get(truong) is not None)

    T["cpl"] = chia(tong_neu_co("leads", "spend"), tong.get("leads")) if tong.get("leads") else None
    T["cpa_mua"] = chia(tong_neu_co("purchases", "spend"), tong.get("purchases")) if tong.get("purchases") else None
    T["cp_tin_nhan"] = chia(tong_neu_co("messages", "spend"), tong.get("messages")) if tong.get("messages") else None
    T["roas"] = chia(tong.get("purchase_value"), tong_neu_co("purchase_value", "spend"))
    T["hook"] = chia(tong.get("video_3s"), tong_neu_co("video_3s", "impressions"), 100)
    T["thruplay_rate"] = chia(tong.get("thruplay"), tong_neu_co("thruplay", "impressions"), 100)

    # Mốc so sánh theo từng loại kết quả
    ref = {}
    for g in ds:
        lk = g["loai_kq"]
        ref.setdefault(lk, [0.0, 0.0])
        ref[lk][0] += g.get("spend") or 0
        ref[lk][1] += g.get("kq") or 0
    ref_cpr = {}
    for lk, (s, r) in ref.items():
        ref_cpr[lk] = a.cpa_muc_tieu if a.cpa_muc_tieu else (s / r if r else None)

    for g in ds:
        g["de_xuat"], g["tin_cay"] = de_xuat(g, ref_cpr.get(g["loai_kq"]), a.tan_suat_canh_bao)

    # Chất lượng dữ liệu
    thieu = [TEN_KHOA[k] for k in ("reach", "clicks_link", "results") if k not in cot]
    if thieu:
        chat_luong.append("Thiếu cột: " + ", ".join(thieu) + " → một số chỉ số không tính được.")
    if bo_qua:
        chat_luong.append(f"Bỏ qua {bo_qua} dòng không có số liệu.")
    gop = [g for g in ds if g["so_dong"] > 1]
    if gop:
        chat_luong.append(f"{len(gop)} {ten_cap} có nhiều dòng (vd chia theo ngày) đã được cộng dồn; "
                          "'Người tiếp cận' cộng dồn có thể bị đếm trùng nên tần suất chỉ là ước lượng.")
    if len(ds) > 1 and "reach" in cot:
        chat_luong.append("Tiếp cận tổng = cộng các dòng (một người có thể thấy nhiều quảng cáo) "
                          "→ tần suất tổng là ước lượng thấp hơn thực tế, xem số chính xác trong Ads Manager.")
    if len({g["loai_kq"] for g in ds}) > 1:
        canh_bao.append("File có NHIỀU loại kết quả khác nhau (" + "; ".join(sorted({g['loai_kq'] or '(trống)'
                        for g in ds})) + "). Chỉ so chi phí/kết quả giữa các dòng CÙNG loại; "
                        "dòng tổng 'Kết quả' chỉ mang tính tham khảo.")
    if any(dong_lech.values()):
        chat_luong.append("Cột do Ads Manager tự tính lệch >5% so với tính lại ở: " + ", ".join(
            f"{k} ({v} dòng)" for k, v in dong_lech.items() if v) +
            ". Thường do làm tròn, khác định nghĩa (vd click tất cả/click liên kết) hoặc sai dấu thập phân "
            "— thử --dau-thap-phan nếu nghi ngờ.")
        chat_luong.extend("  - Ví dụ: " + v for v in vi_du_lech)
    if tong_file is not None:
        chat_luong.append("File có dòng tổng của Ads Manager; script đã bỏ qua dòng này và tự cộng lại.")
        so_tong_file = doc_so(tong_file[cot["spend"]] if cot["spend"] < len(tong_file) else "", a.dau_thap_phan)
        if so_tong_file and T.get("spend") and lech(so_tong_file, T["spend"]):
            canh_bao.append(f"Tổng chi tiêu trong file ({fmt_tien(so_tong_file, tien_te)}) khác tổng cộng lại "
                            f"({fmt_tien(T['spend'], tien_te)}) — kiểm tra dòng bị thiếu hoặc trùng.")

    # Cảnh báo theo chỉ số
    for g in ds:
        if g.get("freq") and g["freq"] >= a.tan_suat_canh_bao:
            canh_bao.append(f"Tần suất cao ({fmt_so(g['freq'], 2)}) ở '{g['ten']}' → người xem thấy lặp lại nhiều, "
                            "nguy cơ mỏi quảng cáo.")
        if (g.get("spend") or 0) > 0 and not g.get("kq"):
            canh_bao.append(f"'{g['ten']}' đã chi {fmt_tien(g['spend'], tien_te)} nhưng chưa có kết quả.")
        if (T.get("ctr_link") and g.get("ctr_link") is not None and (g.get("impressions") or 0) >= 1000
                and g["ctr_link"] < 0.5 * T["ctr_link"]):
            canh_bao.append(f"CTR liên kết của '{g['ten']}' ({fmt_pt(g['ctr_link'])}) thấp hơn một nửa mức chung "
                            f"({fmt_pt(T['ctr_link'])}) → xem lại hook/hình/CTA.")
        if T.get("cpm") and g.get("cpm") and (g.get("impressions") or 0) >= 1000 and g["cpm"] > 1.5 * T["cpm"]:
            canh_bao.append(f"CPM của '{g['ten']}' ({fmt_tien(g['cpm'], tien_te)}) cao hơn 1,5 lần mức chung "
                            f"({fmt_tien(T['cpm'], tien_te)}) → đối tượng hẹp/cạnh tranh hoặc creative bị chấm thấp.")

    # ------------------------------------------------------------------ Xuất báo cáo
    co_roas = "purchase_value" in cot
    khoang_ngay = f"{min(ngay)} → {max(ngay)}" if ngay else "[CẦN BỔ SUNG: khoảng ngày]"
    o = []
    o.append("# Báo cáo Facebook Ads (tính lại từ file CSV)")
    o.append("")
    o.append(f"- File: `{os.path.basename(a.file_csv)}` · dấu phân cách cột: `{dau_pc}`")
    o.append(f"- Khoảng ngày: {khoang_ngay}")
    o.append(f"- Cấp phân tích: {ten_cap} · số dòng dữ liệu: {sum(g['so_dong'] for g in ds)}")
    o.append(f"- Tiền tệ: {tien_te or '[CẦN BỔ SUNG: đơn vị tiền]'}")
    if a.cpa_muc_tieu:
        o.append(f"- Chi phí/kết quả mục tiêu: {fmt_tien(a.cpa_muc_tieu, tien_te)}")
    else:
        o.append("- Chi phí/kết quả mục tiêu: chưa nhập → so với trung bình của chính tài khoản (theo từng loại kết quả)")
    o.append("")
    o.append("## 1. Tổng quan")
    o.append("")
    o.append("| Chỉ số | Giá trị | Công thức |")
    o.append("|---|---|---|")
    hang = [
        ("Chi tiêu", fmt_tien(T.get("spend"), tien_te), "tổng cột chi tiêu"),
        ("Lượt hiển thị", fmt_so(T.get("impressions")), "tổng"),
        ("Người tiếp cận (ước lượng)", fmt_so(T.get("reach")), "tổng các dòng"),
        ("Tần suất (ước lượng)", fmt_so(T.get("freq"), 2), "hiển thị ÷ tiếp cận"),
        ("CPM", fmt_tien(T.get("cpm"), tien_te), "chi tiêu ÷ hiển thị × 1.000"),
        ("Click liên kết", fmt_so(T.get("clicks_link")), "tổng"),
        ("CTR liên kết", fmt_pt(T.get("ctr_link")), "click liên kết ÷ hiển thị × 100%"),
        ("CPC liên kết", fmt_tien(T.get("cpc"), tien_te), "chi tiêu ÷ click liên kết"),
        ("Kết quả (mọi loại)", fmt_so(T.get("kq")), "tổng cột kết quả"),
        ("Chi phí/kết quả (tham khảo)", fmt_tien(T.get("cpr"), tien_te), "chi tiêu ÷ kết quả"),
    ]
    if "leads" in cot:
        hang.append(("CPL (chi phí/khách tiềm năng)", fmt_tien(T.get("cpl"), tien_te), "chi tiêu ÷ số lead"))
    if "messages" in cot:
        hang.append(("Chi phí/tin nhắn", fmt_tien(T.get("cp_tin_nhan"), tien_te), "chi tiêu ÷ cuộc trò chuyện"))
    if "purchases" in cot:
        hang.append(("CPA mua hàng", fmt_tien(T.get("cpa_mua"), tien_te), "chi tiêu ÷ lượt mua"))
    if co_roas:
        hang.append(("ROAS", fmt_so(T.get("roas"), 2), "doanh thu ÷ chi tiêu (chỉ các dòng có doanh thu)"))
    if "video_3s" in cot:
        hang.append(("Tỉ lệ xem 3 giây (hook)", fmt_pt(T.get("hook")),
                     "lượt phát 3 giây ÷ hiển thị × 100% (chỉ quảng cáo video)"))
    if "thruplay" in cot:
        hang.append(("Tỉ lệ ThruPlay", fmt_pt(T.get("thruplay_rate")), "ThruPlay ÷ hiển thị × 100% (chỉ video)"))
    for h in hang:
        o.append("| " + " | ".join(h) + " |")
    o.append("")

    o.append(f"## 2. Chi tiết theo {ten_cap} (xếp theo chi tiêu)")
    o.append("")
    cot_bang = ["Tên", "Loại kết quả", "Chi tiêu", "Hiển thị", "Tần suất", "CPM", "CTR link", "CPC",
                "Kết quả", "Chi phí/KQ"] + (["ROAS"] if co_roas else []) + ["Đề xuất", "Độ tin cậy"]
    o.append("| " + " | ".join(cot_bang) + " |")
    o.append("|" + "---|" * len(cot_bang))
    for g in sorted(ds, key=lambda x: -(x.get("spend") or 0)):
        ten = g["ten"] + (f" ({g['cha']})" if g.get("cha") else "")
        dong_bang = [ten, md(g["loai_kq"] or "—"), fmt_tien(g.get("spend"), tien_te), fmt_so(g.get("impressions")),
                     fmt_so(g.get("freq"), 2), fmt_tien(g.get("cpm"), tien_te), fmt_pt(g.get("ctr_link")),
                     fmt_tien(g.get("cpc"), tien_te), fmt_so(g.get("kq")), fmt_tien(g.get("cpr"), tien_te)]
        if co_roas:
            dong_bang.append(fmt_so(g.get("roas"), 2))
        dong_bang += [g["de_xuat"], g["tin_cay"]]
        o.append("| " + " | ".join(dong_bang) + " |")
    o.append("")

    o.append("## 3. Tốt nhất / kém nhất (chi phí/kết quả, so trong cùng loại kết quả)")
    o.append("")
    for lk in sorted({g["loai_kq"] for g in ds}):
        nhom_lk = [g for g in ds if g["loai_kq"] == lk and g.get("kq")]
        if not nhom_lk:
            continue
        nhom_lk.sort(key=lambda x: x["cpr"])
        o.append(f"**{md(lk or 'Kết quả')}** — mốc so sánh: {fmt_tien(ref_cpr.get(lk), tien_te)}")
        o.append("")
        so_tot = min(3, (len(nhom_lk) + 1) // 2)
        tot = nhom_lk[:so_tot]
        kem = [g for g in nhom_lk[::-1][:3] if g not in tot]
        o.append("- Tốt nhất: " + "; ".join(f"{g['ten']} ({fmt_tien(g['cpr'], tien_te)})" for g in tot))
        if kem:
            o.append("- Kém nhất: " + "; ".join(f"{g['ten']} ({fmt_tien(g['cpr'], tien_te)})" for g in kem))
        o.append("")
    khong_kq = [g for g in ds if (g.get("spend") or 0) > 0 and not g.get("kq")]
    if khong_kq:
        o.append("- Đã chi tiêu nhưng 0 kết quả: " + "; ".join(
            f"{g['ten']} ({fmt_tien(g['spend'], tien_te)})" for g in khong_kq))
        o.append("")

    o.append("## 4. Cảnh báo")
    o.append("")
    o.extend(f"- {c}" for c in canh_bao) if canh_bao else o.append("- Không có cảnh báo theo ngưỡng mặc định.")
    o.append("")
    o.append("## 5. Chất lượng dữ liệu")
    o.append("")
    o.extend(f"- {c}" if not c.startswith("  ") else c for c in chat_luong) if chat_luong else \
        o.append("- Dữ liệu đọc được đầy đủ, không phát hiện lệch đáng kể.")
    o.append("")
    o.append("## 6. Cách đọc đề xuất (gợi ý theo ngưỡng — người dùng duyệt trước khi thay đổi quảng cáo)")
    o.append("")
    o.append("- Mốc = chi phí/kết quả mục tiêu (nếu nhập) hoặc trung bình của tài khoản cho cùng loại kết quả.")
    o.append("- GIỮ (ứng viên tăng ngân sách): chi phí/kết quả ≤ 80% mốc. GIỮ: 80–120%. THEO DÕI: 120–150%. "
             "GIẢM: > 150%.")
    o.append("- 0 kết quả: chi ≥ 2 × mốc → TẮT (cân nhắc); chi < 2 × mốc → THEO DÕI (chưa đủ dữ liệu).")
    o.append(f"- Tần suất ≥ {fmt_so(a.tan_suat_canh_bao, 1)} → thêm THỬ MỚI creative.")
    o.append("- Độ tin cậy: ≥ 10 kết quả = Cao; 3–9 = Trung bình; < 3 = Thấp (chưa nên kết luận mạnh).")
    o.append("")
    o.append("## 7. Dữ liệu còn thiếu để kết luận chắc hơn")
    o.append("")
    thieu_kl = []
    if not co_roas:
        thieu_kl.append("Doanh thu/giá trị đơn → chưa tính được ROAS.")
    thieu_kl.append("Số lead/tin nhắn chốt thành đơn (dữ liệu ngoài Ads Manager) → chưa đánh giá được khâu chốt sale.")
    thieu_kl.append("Số liệu kỳ trước cùng độ dài → chưa so sánh được xu hướng.")
    o.extend(f"- {t}" for t in thieu_kl)
    o.append("")

    bao_cao = "\n".join(o)
    if a.ra:
        with open(a.ra, "w", encoding="utf-8") as f:
            f.write(bao_cao + "\n")
        print(f"Đã ghi báo cáo: {a.ra}")
    else:
        print(bao_cao)

    if a.xuat_csv and chuan_hoa:
        ten_cot = list(chuan_hoa[0].keys())
        for r in chuan_hoa:
            for k in r:
                if k not in ten_cot:
                    ten_cot.append(k)
        with open(a.xuat_csv, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=ten_cot)
            w.writeheader()
            w.writerows(chuan_hoa)
        print(f"Đã ghi dữ liệu chuẩn hóa: {a.xuat_csv}")


if __name__ == "__main__":
    main()
