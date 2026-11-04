#!/usr/bin/env python3
r"""Kiểm tra sổ nguồn nghiên cứu đối thủ (CSV) trước khi viết kết luận.

Tìm: cột bắt buộc bị thiếu, ô trống, URL sai, ngày không đúng dạng YYYY-MM-DD,
nhãn trạng thái/độ tin cậy không hợp lệ, URL trùng. Chỉ dùng thư viện chuẩn Python 3.

Cách chạy:
  macOS / Linux:  python3 scripts/kiem_tra_nguon.py so-nguon.csv --json-out ket-qua-kiem-tra.json
  Windows:        py scripts\kiem_tra_nguon.py so-nguon.csv --json-out ket-qua-kiem-tra.json

Cột chấp nhận (tiếng Anh hoặc tiếng Việt): competitor/Đối thủ, channel/Kênh, source_url/URL nguồn,
accessed_date/Ngày truy cập, evidence/Thông tin ghi nhận, status/Trạng thái, confidence/Độ tin cậy.
Trạng thái hợp lệ: SỰ THẬT, SUY LUẬN, CHƯA KIỂM CHỨNG. Độ tin cậy: cao, trung bình, thấp.
Mã thoát 0 = đạt, 1 = còn lỗi.
"""
import argparse, csv, json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = ['competitor','channel','source_url','accessed_date','evidence','status','confidence']
ALIASES = {
    'Đối thủ':'competitor', 'Kênh':'channel', 'URL':'source_url', 'URL nguồn':'source_url',
    'Ngày truy cập':'accessed_date', 'Thông tin ghi nhận':'evidence',
    'Trạng thái':'status', 'Độ tin cậy':'confidence'
}
STATUSES = {'DỮ KIỆN','SỰ THẬT','SUY LUẬN','CHƯA XÁC MINH','CHƯA KIỂM CHỨNG'}
CONFIDENCE = {'cao','trung bình','thấp'}

def valid_url(value):
    try:
        p=urlparse(value)
        return p.scheme in {'http','https'} and bool(p.netloc)
    except Exception:
        return False

def check(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        raw=list(csv.DictReader(f))
    rows=[{ALIASES.get(k,k):v for k,v in row.items()} for row in raw]
    missing_columns=[c for c in REQUIRED if not rows or c not in rows[0]]
    issues=[]
    urls=[]
    for i,row in enumerate(rows,2):
        for col in REQUIRED:
            if not (row.get(col) or '').strip(): issues.append({'row':i,'field':col,'issue':'missing'})
        url=(row.get('source_url') or '').strip(); urls.append(url)
        if url and not valid_url(url): issues.append({'row':i,'field':'source_url','issue':'invalid_url'})
        if row.get('status','').strip().upper() not in STATUSES: issues.append({'row':i,'field':'status','issue':'invalid_status'})
        if row.get('confidence','').strip().lower() not in CONFIDENCE: issues.append({'row':i,'field':'confidence','issue':'invalid_confidence'})
        d=(row.get('accessed_date') or '').strip()
        if d:
            try: date.fromisoformat(d)
            except ValueError: issues.append({'row':i,'field':'accessed_date','issue':'use_yyyy_mm_dd'})
    for url,count in Counter(u for u in urls if u).items():
        if count>1: issues.append({'row':None,'field':'source_url','issue':'duplicate_url','value':url,'count':count})
    return {'file':str(path),'rows':len(rows),'missing_columns':missing_columns,'issues':issues,'passed':not missing_columns and not issues}

def main():
    ap=argparse.ArgumentParser(description='Kiểm tra sổ nguồn nghiên cứu đối thủ dạng CSV.')
    ap.add_argument('csv_file',type=Path)
    ap.add_argument('--json-out',type=Path)
    args=ap.parse_args()
    result=check(args.csv_file)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    print(text)
    if args.json_out: args.json_out.write_text(text+'\n',encoding='utf-8')
    raise SystemExit(0 if result['passed'] else 1)

if __name__=='__main__': main()
