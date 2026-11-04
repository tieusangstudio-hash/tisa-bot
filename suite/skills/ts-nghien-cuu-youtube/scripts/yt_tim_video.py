#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tìm video YouTube theo chủ đề, lọc theo lượt xem / số người đăng ký kênh,
tính chỉ số vượt cỡ (view ÷ sub), view/ngày, tỉ lệ tương tác.
Thuộc skill /ts-nghien-cuu-youtube (Bộ skill TISA AI Agent).

Dùng YouTube Data API v3 bằng thư viện chuẩn (urllib) — KHÔNG cần cài thêm gì.

KHÓA API (API key) — chọn 1 trong 2 cách:
  1) Biến môi trường YOUTUBE_API_KEY
       macOS:    export YOUTUBE_API_KEY="khoa-cua-ban"
       Windows:  set YOUTUBE_API_KEY=khoa-cua-ban          (Command Prompt)
                 $env:YOUTUBE_API_KEY="khoa-cua-ban"       (PowerShell)
  2) Tham số --key khoa-cua-ban

CÁCH CHẠY:
  macOS:    python3 yt_tim_video.py --q "quay video bằng điện thoại" --q "edit video capcut" --min-views 10000 --out ket-qua.json
  Windows:  py yt_tim_video.py --q "quay video bằng điện thoại" --min-views 10000 --out ket-qua.json

  Chạy lại bảng từ file JSON đã lưu (không cần mạng, không tốn hạn mức):
            python3 yt_tim_video.py --tu-file ket-qua.json --min-views 50000

THAM SỐ:
  --q TEXT            Từ khóa tìm kiếm (dùng nhiều lần cho nhiều từ khóa)
  --min-views N       Lượt xem tối thiểu (mặc định 0)
  --min-subs N        Số người đăng ký tối thiểu của kênh (mặc định 0)
  --max-subs N        Số người đăng ký tối đa của kênh (để tìm kênh nhỏ mà video vượt cỡ)
  --region VN         Mã quốc gia (mặc định VN)
  --lang vi           Ngôn ngữ ưu tiên (mặc định vi)
  --max N             Số video lấy mỗi từ khóa, tối đa 50 (mặc định 25)
  --order relevance   Cách xếp khi tìm: relevance | viewCount | date (mặc định relevance)
  --days N            Chỉ lấy video đăng trong N ngày gần đây (mặc định: không giới hạn)
  --sort outlier      Xếp bảng theo: outlier | views | per_day | engagement (mặc định outlier)
  --top N             Số dòng in ra bảng (mặc định 30)
  --out FILE.json     Lưu dữ liệu đầy đủ ra file JSON
  --tu-file FILE.json Đọc dữ liệu từ file JSON đã lưu thay vì gọi API

HẠN MỨC MIỄN PHÍ: 10.000 đơn vị/ngày. Mỗi từ khóa tốn khoảng 102 đơn vị
(tìm kiếm 100 + lấy thống kê video và kênh ~2) → khoảng 90 từ khóa/ngày.
"""

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

API = "https://www.googleapis.com/youtube/v3/"


def loi(tb, ma=1):
    print("LỖI: " + tb, file=sys.stderr)
    sys.exit(ma)


def goi_api(duong_dan, tham_so, khoa):
    tham_so = dict(tham_so)
    tham_so["key"] = khoa
    url = API + duong_dan + "?" + urllib.parse.urlencode(tham_so)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            chi_tiet = json.loads(e.read().decode("utf-8"))
            ly_do = chi_tiet["error"]["errors"][0].get("reason", "")
            thong_diep = chi_tiet["error"].get("message", "")
        except Exception:
            ly_do, thong_diep = "", str(e)
        if ly_do in ("quotaExceeded", "dailyLimitExceeded"):
            loi("Đã hết hạn mức miễn phí hôm nay (10.000 đơn vị). Thử lại sau 14h–15h chiều giờ Việt Nam "
                "(hạn mức reset lúc nửa đêm giờ Mỹ) hoặc dùng --tu-file với dữ liệu đã lưu.")
        if ly_do in ("keyInvalid", "badRequest") or "API key not valid" in thong_diep:
            loi("Khóa API không đúng. Kiểm tra lại đã chép đủ khóa chưa (không có khoảng trắng thừa).")
        if ly_do in ("accessNotConfigured", "forbidden") or e.code == 403:
            loi("Khóa bị từ chối (403). Kiểm tra đã BẬT 'YouTube Data API v3' trong Google Cloud Console "
                "và khóa không bị giới hạn sai. Chi tiết: " + thong_diep)
        loi(f"API trả lỗi {e.code}: {thong_diep}")
    except urllib.error.URLError as e:
        loi(f"Không kết nối được mạng tới YouTube: {e.reason}. Kiểm tra Internet rồi thử lại.")


def chia_lo(ds, n=50):
    for i in range(0, len(ds), n):
        yield ds[i:i + n]


def doc_thoi_gian(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def thoi_luong_giay(iso):
    """PT1H2M10S -> giây."""
    if not iso or not iso.startswith("P"):
        return None
    tong, so, trong_ngay = 0, "", False
    for ky_tu in iso[1:]:
        if ky_tu == "T":
            trong_ngay = True
        elif ky_tu.isdigit():
            so += ky_tu
        else:
            gia_tri = int(so or 0)
            so = ""
            if ky_tu == "D":
                tong += gia_tri * 86400
            elif ky_tu == "H" and trong_ngay:
                tong += gia_tri * 3600
            elif ky_tu == "M" and trong_ngay:
                tong += gia_tri * 60
            elif ky_tu == "S":
                tong += gia_tri
    return tong


def lay_du_lieu(args, khoa):
    gom = {}  # video_id -> {tu_khoa: [...]}
    for q in args.q:
        tham_so = {
            "part": "snippet", "q": q, "type": "video", "maxResults": min(max(args.max, 1), 50),
            "regionCode": args.region, "relevanceLanguage": args.lang, "order": args.order,
        }
        if args.days:
            moc = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)
            tham_so["publishedAfter"] = moc.strftime("%Y-%m-%dT%H:%M:%SZ")
        kq = goi_api("search", tham_so, khoa)
        for it in kq.get("items", []):
            vid = it.get("id", {}).get("videoId")
            if vid:
                gom.setdefault(vid, set()).add(q)
        print(f"• '{q}': {len(kq.get('items', []))} video", file=sys.stderr)

    if not gom:
        return []
    video = {}
    for lo in chia_lo(list(gom)):
        kq = goi_api("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(lo)}, khoa)
        for it in kq.get("items", []):
            video[it["id"]] = it

    kenh_ids = sorted({v["snippet"]["channelId"] for v in video.values()})
    kenh = {}
    for lo in chia_lo(kenh_ids):
        kq = goi_api("channels", {"part": "snippet,statistics", "id": ",".join(lo)}, khoa)
        for it in kq.get("items", []):
            kenh[it["id"]] = it

    ds = []
    for vid, v in video.items():
        sn, st = v.get("snippet", {}), v.get("statistics", {})
        k = kenh.get(sn.get("channelId"), {})
        kst = k.get("statistics", {})
        an_sub = kst.get("hiddenSubscriberCount", False)
        ds.append({
            "video_id": vid,
            "link": f"https://www.youtube.com/watch?v={vid}",
            "tieu_de": sn.get("title", ""),
            "kenh": sn.get("channelTitle", ""),
            "kenh_id": sn.get("channelId", ""),
            "ngay_dang": sn.get("publishedAt", ""),
            "thoi_luong_giay": thoi_luong_giay(v.get("contentDetails", {}).get("duration")),
            "view": int(st.get("viewCount", 0) or 0),
            "like": int(st["likeCount"]) if "likeCount" in st else None,
            "binh_luan": int(st["commentCount"]) if "commentCount" in st else None,
            "sub": None if an_sub else int(kst.get("subscriberCount", 0) or 0),
            "tu_khoa": sorted(gom[vid]),
        })
    return ds


def tinh_chi_so(ds, hom_nay):
    for v in ds:
        ngay = doc_thoi_gian(v.get("ngay_dang", ""))
        so_ngay = max((hom_nay - ngay).total_seconds() / 86400, 1) if ngay else None
        v["so_ngay"] = round(so_ngay, 1) if so_ngay else None
        v["view_ngay"] = round(v["view"] / so_ngay, 1) if so_ngay else None
        sub = v.get("sub")
        v["vuot_co"] = round(v["view"] / sub, 2) if sub else None
        tuong_tac = (v.get("like") or 0) + (v.get("binh_luan") or 0)
        v["tuong_tac_pct"] = round(tuong_tac / v["view"] * 100, 2) if v["view"] else None
        tl = v.get("thoi_luong_giay")
        v["dang"] = "Ngắn ≤60s" if tl is not None and tl <= 60 else ("Dài" if tl else "?")
    return ds


def loc(ds, a):
    kq = []
    for v in ds:
        if v["view"] < a.min_views:
            continue
        sub = v.get("sub")
        if a.min_subs and (sub is None or sub < a.min_subs):
            continue
        if a.max_subs is not None and (sub is None or sub > a.max_subs):
            continue
        kq.append(v)
    khoa_xep = {
        "outlier": lambda v: v["vuot_co"] if v["vuot_co"] is not None else -1,
        "views": lambda v: v["view"],
        "per_day": lambda v: v["view_ngay"] or 0,
        "engagement": lambda v: v["tuong_tac_pct"] or 0,
    }[a.sort]
    return sorted(kq, key=khoa_xep, reverse=True)


def gon(n):
    if n is None:
        return "ẩn"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}tr".replace(".", ",")
    if n >= 1_000:
        return f"{n / 1_000:.1f}N".replace(".", ",")
    return str(int(n))


def nghin(n):
    """10000 -> 10.000 (kiểu Việt Nam)."""
    return f"{int(n):,}".replace(",", ".")


def md(x):
    return str(x).replace("|", "\\|").replace("\n", " ").strip()


def danh_gia_vuot_co(x):
    if x is None:
        return "—"
    if x >= 10:
        return "RẤT VƯỢT CỠ"
    if x >= 3:
        return "Vượt cỡ"
    if x >= 1:
        return "Khá"
    return "Bình thường"


def in_bang(ds, top):
    dong = [
        "| # | Tiêu đề | Kênh | View | Sub kênh | Vượt cỡ (view÷sub) | View/ngày | Tương tác % | Dạng | Ngày đăng |",
        "|---:|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for i, v in enumerate(ds[:top], start=1):
        vc = "—" if v["vuot_co"] is None else f"{v['vuot_co']:.2f}".replace(".", ",") + f" ({danh_gia_vuot_co(v['vuot_co'])})"
        tt = "—" if v["tuong_tac_pct"] is None else f"{v['tuong_tac_pct']:.2f}".replace(".", ",")
        dong.append(
            f"| {i} | [{md(v['tieu_de'])[:80]}]({v['link']}) | {md(v['kenh'])} | {gon(v['view'])} | {gon(v['sub'])} | "
            f"{vc} | {gon(v['view_ngay'])} | {tt} | {v['dang']} | {str(v['ngay_dang'])[:10]} |"
        )
    return "\n".join(dong)


def main():
    p = argparse.ArgumentParser(description="Nghiên cứu video YouTube theo chủ đề (YouTube Data API v3).")
    p.add_argument("--q", action="append", default=[], help="Từ khóa (dùng nhiều lần)")
    p.add_argument("--key", help="Khóa API (nếu không đặt biến môi trường YOUTUBE_API_KEY)")
    p.add_argument("--min-views", type=int, default=0)
    p.add_argument("--min-subs", type=int, default=0)
    p.add_argument("--max-subs", type=int, default=None)
    p.add_argument("--region", default="VN")
    p.add_argument("--lang", default="vi")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--order", choices=["relevance", "viewCount", "date"], default="relevance")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--sort", choices=["outlier", "views", "per_day", "engagement"], default="outlier")
    p.add_argument("--top", type=int, default=30)
    p.add_argument("--out", help="Lưu dữ liệu ra file JSON")
    p.add_argument("--tu-file", help="Đọc dữ liệu từ file JSON đã lưu (không gọi API)")
    a = p.parse_args()

    if a.tu_file:
        try:
            with open(a.tu_file, "r", encoding="utf-8-sig") as f:
                goc = json.load(f)
        except FileNotFoundError:
            loi(f"Không tìm thấy file '{a.tu_file}'.")
        except json.JSONDecodeError as e:
            loi(f"File JSON sai cú pháp dòng {e.lineno}: {e.msg}")
        ds = goc.get("video", goc if isinstance(goc, list) else [])
        tu_khoa = goc.get("tu_khoa", []) if isinstance(goc, dict) else []
        hom_nay = doc_thoi_gian(goc.get("thoi_diem_lay", "")) if isinstance(goc, dict) else None
        hom_nay = hom_nay or dt.datetime.now(dt.timezone.utc)
        nguon = f"file {a.tu_file}"
    else:
        if not a.q:
            loi("Cần ít nhất 1 từ khóa: --q \"từ khóa\".")
        khoa = a.key or os.environ.get("YOUTUBE_API_KEY", "").strip()
        if not khoa:
            loi("Chưa có khóa API. Đặt biến môi trường YOUTUBE_API_KEY hoặc thêm --key. "
                "Xem hướng dẫn lấy khóa miễn phí trong references/lay-api-key.md.")
        hom_nay = dt.datetime.now(dt.timezone.utc)
        ds = lay_du_lieu(a, khoa)
        tu_khoa = a.q
        nguon = "YouTube Data API v3"

    ds = tinh_chi_so(ds, hom_nay)
    loc_xong = loc(ds, a)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump({
                "thoi_diem_lay": hom_nay.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "nguon": nguon, "tu_khoa": tu_khoa, "khu_vuc": a.region, "ngon_ngu": a.lang,
                "bo_loc": {"min_views": a.min_views, "min_subs": a.min_subs, "max_subs": a.max_subs},
                "video": ds,
            }, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu dữ liệu đầy đủ ({len(ds)} video): {a.out}", file=sys.stderr)

    print(f"# Nghiên cứu YouTube — {', '.join(tu_khoa) or '(không rõ từ khóa)'}")
    print()
    bo_loc = [f"view ≥ {nghin(a.min_views)}"]
    if a.min_subs:
        bo_loc.append(f"sub ≥ {nghin(a.min_subs)}")
    if a.max_subs is not None:
        bo_loc.append(f"sub ≤ {nghin(a.max_subs)}")
    print(f"Nguồn: {nguon} · Lấy lúc: {hom_nay.strftime('%Y-%m-%d %H:%M')} UTC · "
          f"Tổng {len(ds)} video, còn {len(loc_xong)} sau lọc ({'; '.join(bo_loc)}) · Xếp theo: {a.sort}")
    print()
    if not loc_xong:
        print("Không có video nào qua bộ lọc. Thử giảm --min-views hoặc bỏ --max-subs.")
        return
    print(in_bang(loc_xong, a.top))
    print()
    co_vc = [v["vuot_co"] for v in loc_xong if v["vuot_co"] is not None]
    if co_vc:
        co_vc.sort()
        giua = co_vc[len(co_vc) // 2]
        print(f"Chỉ số vượt cỡ trung vị: {giua:.2f}".replace(".", ",") +
              f" · Số video vượt cỡ (≥ 3): {sum(1 for x in co_vc if x >= 3)}")
    an = sum(1 for v in loc_xong if v["sub"] is None)
    if an:
        print(f"Lưu ý: {an} video thuộc kênh ẩn số người đăng ký → không tính được chỉ số vượt cỡ.")
    print("Chú thích: Vượt cỡ = view ÷ sub (≥ 3 là video được đề xuất vượt xa tệp người theo dõi). "
          "Tương tác % = (like + bình luận) ÷ view × 100.")


if __name__ == "__main__":
    main()
