#!/usr/bin/env python3
"""bang.py - nối TISA BOT với bảng giao việc Đội Quân AI (khung quản lý trên Cloudflare).

Khoá đọc từ ~/.config/doi-quan-ai/.env (bản cài học viên) hoặc ~/.config/doi-quan-ai/.env (bản đầu tiên), không bao giờ in ra màn hình:
  BOARD_URL=https://<địa chỉ bảng>
  BOARD_TOKEN=...            # mã TISA BOT dùng để ghi lên bảng
  JAVIS_URL=http://127.0.0.1:7777
  JAVIS_HOOK_ID=...          # webhook "Đội Quân AI nhận việc" trong TISA BOT
  JAVIS_HOOK_TOKEN=...

Lệnh cho nhân sự TISA BOT:
  bang.py lay <job>                                   xem việc (yêu cầu, kế hoạch, dữ liệu chủ nộp, hồ sơ doanh nghiệp, đội hình)
  bang.py doi                                         hồ sơ doanh nghiệp, luật và đội hình đang bật trên bảng
  bang.py ke-hoach <job> <ke-hoach.json>              đăng kế hoạch chia việc (danh sách phần)
  bang.py phan <job> <n> [--state run|done|duyet|owner|err] [--pct 40] [--out "..."|--out-file f.md] [--append "..."]
  bang.py anh <job> <file.png> [--title "Banner 1"]   tải ảnh/tệp lên bảng và gắn vào kết quả
  bang.py tai <blob-id> <đường-dẫn>                   tải tệp chủ nộp trên bảng về máy
  bang.py tai-het <job> <thư-mục> [--msg <msg_id>]    tải hết tệp chủ đính kèm (giữ nguyên thư mục con) về một thư mục
  bang.py phan <job> <n> --state owner --claude-prompt-file loi-nho.md   gắn lời nhờ Claude làm giúp cho phần chủ phải làm
  bang.py ky-nang <ma-nhan-su> --ten "..." --mo-ta "..." --duong-dan "skills/..."   đăng ký kỹ năng mới cho một nhân sự
  bang.py kho [--loai broll|anh|video|am-thanh|hieu-ung|nen|logo|khac] [--tim "từ khóa"]   xem tư liệu chủ để trong Kho tư liệu
  bang.py kho-tai <thư-mục> [--loai ...] [--tim ...] [--id <id>]   tải tư liệu trong kho về một thư mục
  bang.py kho-sua <id> --loai <ngan> --mo-ta "..." --the "a, b" --chuyen   ghi kết quả phân loại một tư liệu, chuyển tệp vào đúng ngăn
  bang.py dong-bo                                     đồng bộ ngay: kho tư liệu hai chiều, kết nối TISA BOT lên bảng
  bang.py lien-ket <thư-mục> [--bo]                   liên kết một thư mục trên máy vào kho (đội đọc thẳng, không tải lên mạng); --bo để bỏ
  bang.py phong-ban <phong-ban.json>                  đăng ký phòng ban mới và nhân sự của phòng lên bảng (Tâm dùng khi tạo phòng ban)
  bang.py chung-cat [--thu]                           tạo ngay việc chưng cất kiến thức (cầu nối tự tạo lúc 0h mỗi đêm); --thu chỉ in ra
  bang.py boc-tach <job> --tom-tat "..." --tep "obsidian:<trang.md>" --tep "tisa_bot:<trang.md>"   gửi bản bóc tách lên bảng để chủ xem, sửa
  bang.py link <job> --title "..." --url https://...  [--kind doc|sheet|file]
  bang.py xong <job> [--status cho-duyet|xong] --summary "..."
  bang.py hang-doi                                    các việc đang chờ chuyển cho TISA BOT
  bang.py tra-loi <msg_id> --from linh --text "..."    trả lời tin chủ nhắn (thêm --chua-xong nếu còn làm tiếp)
  bang.py tin                                         các tin chủ nhắn đang chờ
  bang.py nho-claude <loi-nho.md> [--gui]             chép lời nhờ, mở app Claude, dán vào cuộc trò chuyện mới (--gui: gửi luôn)
Lệnh cho máy:
  bang.py cau-noi [--moi 5]                           chạy mãi: thấy việc mới trên bảng là đẩy ngay vào webhook TISA BOT
  bang.py kiem-tra                                    kiểm tra kết nối bảng và TISA BOT (không in khoá)
"""
import argparse, calendar, hashlib, json, mimetypes, os, re, subprocess, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

def _env_path():
    if os.environ.get('DOI_QUAN_ENV'):
        return Path(os.environ['DOI_QUAN_ENV'])
    return Path.home() / '.config' / 'doi-quan-ai' / '.env'


ENV_FILE = _env_path()
BANG = str(Path(__file__).resolve())
PYQ = '"' + sys.executable + '"'
for _s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass


def load_env():
    cfg = {}
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    for k in ('BOARD_URL', 'BOARD_TOKEN', 'JAVIS_URL', 'JAVIS_HOOK_ID', 'JAVIS_HOOK_TOKEN', 'JAVIS_DIR', 'KHO_DIR'):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    cfg.setdefault('JAVIS_URL', 'http://127.0.0.1:7777')
    return cfg


C = load_env()


def die(msg, code=1):
    print('LỖI: ' + msg, file=sys.stderr)
    sys.exit(code)


def board(method, path, body=None, raw=None, ctype=None, timeout=60):
    if not C.get('BOARD_TOKEN') or not C.get('BOARD_URL'):
        die('chưa có BOARD_URL hoặc BOARD_TOKEN trong %s (chạy lại bộ cài đặt)' % ENV_FILE)
    url = C['BOARD_URL'].rstrip('/') + path
    data, headers = None, {'Authorization': 'Bearer ' + C['BOARD_TOKEN'], 'User-Agent': 'doi-quan-bang/1'}
    if raw is not None:
        data = raw
        headers['Content-Type'] = ctype or 'application/octet-stream'
    elif body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8') or '{}')
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode('utf-8')).get('error', '')
        except Exception:
            msg = ''
        raise RuntimeError('bảng trả %s %s' % (e.code, msg))


def out(o):
    print(json.dumps(o, ensure_ascii=False, indent=2))


def read_text(args):
    if getattr(args, 'out_file', None):
        return Path(args.out_file).read_text(encoding='utf-8')
    return args.out


def cmd_lay(a):
    out(board('GET', '/api/v1/job/' + a.job))


def cmd_ke_hoach(a):
    raw = Path(a.file).read_text(encoding='utf-8') if a.file != '-' else sys.stdin.read()
    p = json.loads(raw)
    if isinstance(p, list):
        p = {'plan': p}
    out(board('POST', '/api/v1/job/%s/plan' % a.job, p))


def cmd_phan(a):
    b = {'n': a.n}
    for k in ('state', 'agent', 'viec'):
        if getattr(a, k):
            b[k] = getattr(a, k)
    if a.pct is not None:
        b['pct'] = a.pct
    t = read_text(a)
    if t is not None:
        b['out'] = t
    if a.append:
        b['append'] = a.append
    if a.claude_prompt_file:
        b['claudePrompt'] = Path(a.claude_prompt_file).read_text(encoding='utf-8')
    out(board('POST', '/api/v1/job/%s/part' % a.job, b))


def cmd_ky_nang(a):
    try:
        cur = board('GET', '/api/db/settings/skills')
    except RuntimeError:
        cur = {}
    cur.pop('id', None)
    lst = [x for x in (cur.get(a.agent) or []) if x.get('ten') != a.ten]
    lst.append({'ten': a.ten, 'mo_ta': a.mo_ta or '', 'duong_dan': a.duong_dan or '', 'nguon': a.nguon or '', 'ngay': time.strftime('%Y-%m-%d')})
    cur[a.agent] = lst[-30:]
    board('PUT', '/api/db/settings/skills', cur)
    out({'ok': True, 'nhan_su': a.agent, 'ky_nang': [x['ten'] for x in cur[a.agent]]})


def cmd_anh(a):
    f = Path(a.file)
    if not f.is_file():
        die('không thấy tệp ' + str(f))
    ctype = mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
    q = urllib.parse.urlencode({'type': ctype, 'name': f.name})
    up = board('POST', '/api/assets?' + q, raw=f.read_bytes(), ctype=ctype, timeout=180)
    kind = 'image' if ctype.startswith('image/') else ('video' if ctype.startswith('video/') else 'file')
    board('POST', '/api/v1/job/%s/link' % a.job, {'title': a.title or f.stem, 'url': up['url'], 'kind': kind, 'file': f.name})
    out({'ok': True, 'url': up['url'], 'id': up['id'], 'kind': kind})


def _download(bid, dest):
    bid = str(bid).split('/_blob/')[-1]
    req = urllib.request.Request(C['BOARD_URL'].rstrip('/') + '/_blob/' + urllib.parse.quote(bid), headers={'Authorization': 'Bearer ' + C['BOARD_TOKEN'], 'User-Agent': 'doi-quan-bang/1'})
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + '.dang-tai')
    with urllib.request.urlopen(req, timeout=600) as r, open(tmp, 'wb') as fh:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)
    tmp.replace(dest)
    return dest


def cmd_tai(a):
    if not C.get('BOARD_TOKEN'):
        die('chưa có BOARD_TOKEN trong %s' % ENV_FILE)
    out({'ok': True, 'file': str(_download(a.id, a.dest).resolve())})


def _safe_rel(name):
    parts = [p for p in str(name or 'tep').replace('\\', '/').split('/') if p and p not in ('.', '..')]
    return Path(*parts) if parts else Path('tep')


def cmd_tai_het(a):
    if not C.get('BOARD_TOKEN'):
        die('chưa có BOARD_TOKEN trong %s' % ENV_FILE)
    if a.msg:
        m = board('GET', '/api/db/messages/' + urllib.parse.quote(a.msg))
        files = (m.get('files') or []) + (m.get('images') or [])
    else:
        files = board('GET', '/api/v1/job/' + a.job).get('files') or []
    root = Path(a.dir).expanduser()
    got = []
    for f in files:
        dest = root / _safe_rel(f.get('name'))
        try:
            _download(f['id'], dest)
            got.append({'ten': f.get('name'), 'file': str(dest.resolve())})
        except Exception as e:
            got.append({'ten': f.get('name'), 'loi': str(e)[:200]})
    out({'ok': True, 'thu_muc': str(root.resolve()), 'so_tep': len(got), 'tep': got})


def cmd_link(a):
    out(board('POST', '/api/v1/job/%s/link' % a.job, {'title': a.title, 'url': a.url, 'kind': a.kind}))


def cmd_xong(a):
    b = {'status': a.status}
    if a.summary:
        b['summary'] = a.summary
    out(board('POST', '/api/v1/job/%s/done' % a.job, b))


def cmd_doi(a):
    out(board('GET', '/api/v1/kit'))


def cmd_hang_doi(a):
    out(board('GET', '/api/v1/queue'))


def send_to_javis(job):
    if not (C.get('JAVIS_HOOK_ID') and C.get('JAVIS_HOOK_TOKEN')):
        raise RuntimeError('chưa có JAVIS_HOOK_ID / JAVIS_HOOK_TOKEN')
    url = C['JAVIS_URL'].rstrip('/') + '/hooks/' + C['JAVIS_HOOK_ID']
    lan = 'sua' if job.get('status') == 'can-sua' else 'duyet' if job.get('status') == 'da-duyet' else 'moi'
    body = {'loai': 'viec-tu-bang', 'lan': lan, 'job_id': job['id'], 'tieu_de': job.get('title', ''), 'yeu_cau': job.get('task', ''),
            'ngay': job.get('date', ''), 'gio': job.get('time', ''), 'thu_muc': job.get('folder', ''), 'bang': C['BOARD_URL']}
    if job.get('kind') == 'tao-skill':
        body['loai_viec'] = 'tao-ky-nang'
        body['ky_nang'] = {'cho_nhan_su': job.get('skillFor', ''), 'mong_muon': job.get('skillWish', ''), 'tim_tren_github': bool(job.get('github'))}
    if job.get('kind') == 'tao-phong-ban':
        body['loai_viec'] = 'tao-phong-ban'
        body['phong_ban'] = {'mong_muon': job.get('roomWish', ''), 'so_nhan_su': job.get('roomN', ''), 'tim_tren_github': bool(job.get('github')),
                             'lenh_dang_ky': PYQ + ' "%s" phong-ban phong-ban.json' % BANG}
    elif job.get('kind') == 'nap-kien-thuc':
        body['loai_viec'] = 'nap-kien-thuc'
        body['nap_kien_thuc'] = dict(nap_info(), link=job.get('ktLinks') or [], chu_y=job.get('ktFocus', ''))
    elif job.get('kind') == 'chung-cat-dem':
        body['loai_viec'] = 'chung-cat-dem'
        body['chung_cat'] = dict(nap_info(), tu_luc=job.get('tuLuc', ''))
    try:
        kr = kho_root()
        lk = lien_ket_list(kr) if kr else []
        if lk:
            body['thu_muc_lien_ket'] = [{'ten': x['ten'], 'duong_dan': x['duong_dan'], 'so_tep': x.get('so_tep')} for x in lk]
    except Exception:
        pass
    files = job.get('files') or []
    if files:
        body['tep_dinh_kem'] = {
            'so_tep': len(files),
            'tai_het': PYQ + ' "%s" tai-het %s "<duong-dan-bo-nao>/%stai-nguyen/chu-gui"' % (BANG, job['id'], job.get('folder', '')),
            'danh_sach': [{'ten': f.get('name'), 'loai': f.get('kind') or f.get('type'), 'kich_thuoc': f.get('size')} for f in files[:200]],
        }
    if lan == 'duyet':
        da = set(job.get('approvedNow') or [])
        plan = job.get('plan') or []
        body['da_duyet'] = [{'phan': p.get('n'), 'nhan_su': p.get('agent'), 'viec': p.get('viec', '')} for p in plan if p.get('n') in da]
        body['con_lai'] = [{'phan': p.get('n'), 'nhan_su': p.get('agent'), 'viec': p.get('viec', ''), 'trang_thai': p.get('state')} for p in plan if p.get('state') not in ('done', 'given', 'stop', 'skip')]
    if lan == 'sua':
        body['gop_y'] = [{'phan': p.get('n'), 'nhan_su': p.get('agent'), 'gop_y': p.get('note', '')} for p in job.get('plan') or [] if p.get('state') == 'sua']
    key = '%s:%s:%s' % (job['id'], job.get('status'), job.get('updated', ''))
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode('utf-8'), method='POST', headers={
        'Authorization': 'Bearer ' + C['JAVIS_HOOK_TOKEN'], 'Content-Type': 'application/json', 'Idempotency-Key': key[:200],
        'User-Agent': 'doi-quan-bang/1'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def post_hook(body, key):
    if not (C.get('JAVIS_HOOK_ID') and C.get('JAVIS_HOOK_TOKEN')):
        raise RuntimeError('chưa có JAVIS_HOOK_ID / JAVIS_HOOK_TOKEN')
    url = C['JAVIS_URL'].rstrip('/') + '/hooks/' + C['JAVIS_HOOK_ID']
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode('utf-8'), method='POST', headers={
        'Authorization': 'Bearer ' + C['JAVIS_HOOK_TOKEN'], 'Content-Type': 'application/json', 'Idempotency-Key': key[:200],
        'User-Agent': 'doi-quan-bang/1'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def send_msg_to_javis(m):
    body = {'loai': 'tin-nhan', 'msg_id': m['id'], 'job_id': m.get('jobId', ''), 'phan': m.get('part', 0), 'nhan_su': m.get('to', 'tam'),
            'yeu_cau': m.get('text', ''),
            'anh': [{'id': i.get('id'), 'ten': i.get('name'), 'tai_ve': PYQ + ' "%s" tai %s <duong-dan>' % (BANG, i.get('id'))} for i in (m.get('images') or [])],
            'tep': [{'id': f.get('id'), 'ten': f.get('name'), 'loai': f.get('kind') or f.get('type'), 'kich_thuoc': f.get('size'),
                     'tai_ve': PYQ + ' "%s" tai %s "<duong-dan>/%s"' % (BANG, f.get('id'), f.get('name'))} for f in (m.get('files') or [])],
            'tai_het_tep': (PYQ + ' "%s" tai-het - "<thu-muc>" --msg %s' % (BANG, m['id'])) if (m.get('files') or m.get('images')) else '',
            'kieu': m.get('kind', 'hoi'), 'tin': m.get('text', ''), 'viec': m.get('job', {}), 'phan_viec': m.get('phan'),
            'tro_chuyen_truoc': m.get('thread', []), 'nguoi': m.get('nguoi'), 'chu': m.get('chu'), 'bang': C['BOARD_URL']}
    return post_hook(body, 'tin:' + m['id'])


def open_local(m):
    """Mở thư mục (hoặc chỉ ra tệp) trong bộ não bằng Finder. Chỉ cho phép đường dẫn nằm trong bộ não."""
    if str(m.get('path') or '').startswith('kho:'):
        kr = kho_root()
        if not kr:
            raise RuntimeError('chưa có thư mục kho')
        kr.mkdir(parents=True, exist_ok=True)
        m = dict(m, path=str(m['path'])[4:])
        base = kr.resolve()
    else:
        k = board('GET', '/api/v1/kit')
        root = ((k.get('doanh_nghiep') or {}).get('bo_nao') or '').strip()
        if not root:
            raise RuntimeError('chưa có đường dẫn bộ não trong Cài đặt')
        base = Path(root).expanduser().resolve()
    target = (base / _safe_rel(m.get('path') or '.')).resolve() if m.get('path') else base
    if target != base and base not in target.parents:
        raise RuntimeError('đường dẫn nằm ngoài bộ não')
    f = target / _safe_rel(m['file']) if m.get('file') else None
    while not target.exists() and target != base:
        target = target.parent
    reveal = f is not None and f.exists()
    if sys.platform == 'darwin':
        subprocess.Popen(['open', '-R', str(f)] if reveal else ['open', str(target)])
    elif os.name == 'nt':
        subprocess.Popen(['explorer', '/select,', str(f)] if reveal else ['explorer', str(target)])
    else:
        subprocess.Popen(['xdg-open', str(target)])
    return str(f if reveal else target)


def handle_open(m):
    note, st = '', 'da-mo'
    try:
        made = calendar.timegm(time.strptime(str(m.get('created', ''))[:19], '%Y-%m-%dT%H:%M:%S'))
        if time.time() - made > 120:
            st, note = 'het-han', 'lệnh cũ, bỏ qua'
    except Exception:
        pass
    if st == 'da-mo':
        try:
            note = open_local(m)
        except Exception as e:
            st, note = 'loi', str(e)[:200]
    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
    board('PATCH', '/api/db/messages/' + urllib.parse.quote(m['id']), {'status': st, 'note': note})
    log('Mở thư mục: %s %s' % (st, note))


# ---------------- Kho tư liệu (chạy ngay trên máy) ----------------
# Tệp có sẵn trên máy (bỏ vào thư mục kho, hoặc lối tắt trỏ về tệp gốc ở Desktop, Tải về) KHÔNG đưa lên mạng:
# cầu nối chỉ ghi sổ .kho-catalog.json và MUC-LUC.md để đội AI tìm và dùng thẳng trên máy.
# Tệp chủ tải lên Kho tư liệu trên bảng thì chép về máy như cũ.
KHO_DIRS = {'anh': '01 - Anh san pham thuong hieu', 'broll': '02 - Video B-roll', 'video': '03 - Video da quay', 'am-thanh': '04 - Nhac am thanh',
            'hieu-ung': '05 - Hieu ung', 'nen': '06 - Nen background', 'logo': '07 - Logo nhan dien', 'khac': '08 - Khac',
            'thanh-pham': '09 - Video thanh pham', 'feedback': '10 - Feedback hoc vien', 'bai-hoc': '11 - Video bai hoc',
            'may': '12 - Thu muc lien ket tren may'}
KHO_INBOX = '00 - Bo vao day AI tu phan loai'
KHO_TEN = {'anh': 'Ảnh sản phẩm, thương hiệu', 'broll': 'Video B-roll', 'video': 'Video đã quay, clip gốc', 'am-thanh': 'Nhạc, âm thanh',
           'hieu-ung': 'Hiệu ứng', 'nen': 'Nền, background', 'logo': 'Logo, nhận diện', 'khac': 'Khác',
           'thanh-pham': 'Video thành phẩm, quảng cáo', 'feedback': 'Feedback, kết quả học viên', 'bai-hoc': 'Video bài học, hướng dẫn',
           'may': 'Thư mục liên kết trên máy'}
KHO_SKIP = {'MUC-LUC.md', 'HUONG-DAN.md', '.kho-index.json', '.kho-catalog.json', '.kho-catalog.json.tmp', '.DS_Store', 'Thumbs.db', 'desktop.ini'}
_KHO_BAO = {'h': None, 't': 0}


def _na(s):
    """Bỏ dấu, chữ thường: để tìm không cần gõ dấu."""
    s = unicodedata.normalize('NFD', str(s or '')).replace('đ', 'd').replace('Đ', 'D')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()


def _nfc(s):
    return unicodedata.normalize('NFC', str(s or ''))


def kho_list(loai=None, tim=None):
    docs = board('GET', '/api/db/library').get('docs') or []
    t = (tim or '').lower()
    out = [d for d in docs if d.get('blob') and (not loai or d.get('cat') == loai)
           and (not t or t in ' '.join([str(d.get('name', '')), str(d.get('note', '')), str(d.get('mo_ta', '')), ' '.join(d.get('the') or [])]).lower())]
    return sorted(out, key=lambda d: str(d.get('created', '')), reverse=True)


def _office():
    dn = board('GET', '/api/v1/kit').get('doanh_nghiep') or {}
    root = (dn.get('bo_nao') or '').strip()
    if not root:
        return None
    return Path(root).expanduser() / ((dn.get('thu_muc_van_phong') or '').strip() or '05 - Van Phong AI')


def brain_kho():
    office = _office()
    if not office:
        return None
    tn = sorted(x for x in office.glob('*') if x.is_dir() and 'tai nguyen' in x.name.lower()) if office.is_dir() else []
    return (tn[0] if tn else office) / 'Kho tu lieu'


def kho_root():
    if C.get('KHO_DIR'):
        return Path(C['KHO_DIR']).expanduser()
    return brain_kho()


def _idx(root):
    try:
        idx = json.loads((root / '.kho-index.json').read_text(encoding='utf-8'))
    except Exception:
        return {}
    return {k: v for k, v in idx.items() if not str(k).startswith('bo-qua:')}


def _save_idx(root, idx):
    (root / '.kho-index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding='utf-8')


def _cat_load(root):
    try:
        c = json.loads((root / '.kho-catalog.json').read_text(encoding='utf-8'))
        if isinstance(c.get('items'), dict):
            return c
    except Exception:
        pass
    return {'items': {}}


def _cat_save(root, c):
    tmp = root / '.kho-catalog.json.tmp'
    tmp.write_text(json.dumps(c, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    os.replace(str(tmp), str(root / '.kho-catalog.json'))


def _write_if(p, text):
    try:
        if p.exists() and p.read_text(encoding='utf-8') == text:
            return False
    except Exception:
        pass
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return True


def _uniq(dest, tag):
    return dest.with_name('%s-%s%s' % (dest.stem, tag[:6], dest.suffix)) if (dest.exists() or os.path.islink(str(dest))) else dest


def _size(n):
    n = float(n or 0)
    if n >= 1024 ** 3:
        return '%.1f GB' % (n / 1024 ** 3)
    return '%.0f KB' % (n / 1024) if n < 1048576 else '%.1f MB' % (n / 1048576)


def _kind(ctype, name):
    n = name.lower()
    if ctype.startswith('image/') or n.endswith(('.heic', '.webp')):
        return 'image'
    if ctype.startswith('video/') or n.endswith(('.mov', '.mp4', '.m4v', '.mkv', '.webm')):
        return 'video'
    if ctype.startswith('audio/') or n.endswith(('.mp3', '.wav', '.m4a', '.aac')):
        return 'audio'
    return 'file'


def _goc(goc):
    """'Desktop › Thư mục › Thư mục con' cho tệp gốc của lối tắt."""
    home, s = str(Path.home()), str(goc)
    for pre, ten in ((home + '/Desktop/', 'Desktop'), (home + '/Downloads/', 'Tải về'), (home + '/', 'Máy')):
        if s.startswith(pre):
            return ' › '.join([ten] + [_nfc(x) for x in Path(s[len(pre):]).parent.parts])
    return _nfc(str(Path(s).parent))


def _the_goc(goc):
    home, s = str(Path.home()), str(goc)
    for pre in (home + '/Desktop/', home + '/Downloads/'):
        if s.startswith(pre):
            return [_nfc(x).strip() for x in Path(s[len(pre):]).parent.parts if x.strip()][:6]
    return []


def scan_local(root, idx, cat):
    """Ghi sổ mọi tệp đang có trong thư mục kho trên máy. Không đưa tệp lên mạng, không đổi gì trên tệp."""
    items = cat['items']
    known = set(idx.values())
    rev = {v: k for k, v in KHO_DIRS.items()}
    found = {}
    for dp, dns, fns in os.walk(str(root)):
        dns[:] = sorted(d for d in dns if not d.startswith('.'))
        for fn in fns:
            if fn in KHO_SKIP or fn.startswith('.') or fn.endswith('.tmp'):
                continue
            p = Path(dp) / fn
            parts = p.relative_to(root).parts
            if len(parts) == 1 and fn.lower().endswith('.md'):
                continue
            rel = str(p.relative_to(root))
            if rel in known:
                continue
            link = os.path.islink(str(p))
            try:
                st, ok = os.stat(str(p)), True
            except OSError:
                st, ok = os.lstat(str(p)), False
            if not link and rel not in items and time.time() - st.st_mtime < 30:
                continue   # tệp đang chép vào, để lượt sau
            found[rel] = (p, link, ok, st, parts)
    for lk in lien_ket_list(root):
        base = Path(lk['duong_dan'])
        if not base.is_dir():
            continue
        cua = root / KHO_DIRS['may'] / lk['ten']
        try:
            if not os.path.islink(str(cua)) and not cua.exists():
                cua.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(str(base), str(cua))
        except OSError:
            pass
        dem = 0
        for dp, dns, fns in os.walk(str(base)):
            dns[:] = sorted(d for d in dns if not d.startswith('.') and d not in ('node_modules', '__MACOSX'))
            for fn in fns:
                if fn in KHO_SKIP or fn.startswith('.') or fn.endswith('.tmp'):
                    continue
                dem += 1
                if dem > LK_MAX:
                    break
                p = Path(dp) / fn
                rel = str(Path(KHO_DIRS['may']) / lk['ten'] / p.relative_to(base))
                if rel in known:
                    continue
                try:
                    st = os.stat(str(p))
                except OSError:
                    continue
                found[rel] = (p, 'lk', True, st, Path(rel).parts)
            if dem > LK_MAX:
                break
    changed = False
    gone = {}
    for rel in [r for r in items if r not in found]:
        it = items.pop(rel)
        gone[(it.get('ten'), it.get('kich_thuoc'))] = it
        changed = True
    for rel, (p, link, ok, st, parts) in sorted(found.items()):
        top = parts[0] if len(parts) > 1 else ''
        ngan = rev.get(top)
        it = items.get(rel)
        if it:
            if it.get('hong') != (not ok) or (ok and it.get('kich_thuoc') != st.st_size) or (ngan and it.get('ngan') != ngan):
                it['hong'] = not ok
                if ok:
                    it['kich_thuoc'] = st.st_size
                if ngan:
                    it['ngan'] = ngan
                changed = True
            continue
        old = gone.pop((p.name, st.st_size if ok else 0), None)
        if old:   # tệp được dời chỗ trong kho: giữ mô tả, thẻ
            old['ngan'] = ngan or old.get('ngan') or 'khac'
            old['hong'] = not ok
            items[rel] = old
            changed = True
            continue
        ctype = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
        it = {'id': 'may-' + hashlib.sha1(rel.encode('utf-8')).hexdigest()[:10], 'ten': _nfc(p.name), 'ngan': ngan or 'khac',
              'kieu': _kind(ctype, p.name), 'kich_thuoc': st.st_size if ok else 0, 'ngay': time.strftime('%Y-%m-%d'),
              'mo_ta': '', 'the': [], 'hong': not ok}
        if link == 'lk':
            it.update(nguon=str(p), phan_loai='xong', lk=True, mo_ta='Tệp trong thư mục liên kết "%s" trên máy' % _nfc(parts[1]), the=[_nfc(parts[1])])
        elif link:
            goc = os.readlink(str(p))
            goc = goc if os.path.isabs(goc) else os.path.normpath(os.path.join(str(p.parent), goc))
            it.update(nguon=goc, phan_loai='xong', mo_ta='Tệp gốc ở ' + _goc(goc), the=_the_goc(goc))
        else:
            it.update(phan_loai='cho', giu_ngan=bool(ngan))
        items[rel] = it
        changed = True
    return changed


def ask_classify(root, docs, idx, cat):
    """Nhờ TISA BOT xem từng tệp mới (tải lên bảng, hoặc chủ bỏ vào thư mục kho), viết mô tả, gắn thẻ, xếp ngăn."""
    now = time.time()
    loc = [(r, it) for r, it in cat['items'].items() if not it.get('hong') and
           (it.get('phan_loai') == 'cho' or (it.get('phan_loai') == 'dang' and now - float(it.get('hoi') or 0) > 7200))][:15]
    pend = [d for d in docs if d.get('phan_loai') == 'cho' and d['id'] in idx][:max(0, 15 - len(loc))]
    if not loc and not pend:
        return 0
    tl = [{'id': d['id'], 'ten': d.get('name'), 'kieu': d.get('kind'), 'kich_thuoc': _size(d.get('size')),
           'duong_dan': str(root / idx[d['id']]), 'ngan_hien_tai': d.get('cat'), 'chu_da_chon_ngan': bool(d.get('giu_ngan')),
           'ghi_chu_cua_chu': d.get('note', '')} for d in pend]
    tl += [{'id': it['id'], 'ten': it.get('ten'), 'kieu': it.get('kieu'), 'kich_thuoc': _size(it.get('kich_thuoc')),
            'duong_dan': str(root / r), 'ngan_hien_tai': it.get('ngan'), 'chu_da_chon_ngan': bool(it.get('giu_ngan')),
            'ghi_chu_cua_chu': ''} for r, it in loc]
    body = {'loai': 'phan-loai-kho', 'thu_muc_kho': str(root), 'muc_luc': str(root / 'MUC-LUC.md'),
            'ngan': {k: {'ten': KHO_TEN[k], 'thu_muc': v} for k, v in KHO_DIRS.items()},
            'lenh_sua': PYQ + ' "%s" kho-sua <id> --loai <ngan> --mo-ta "<mô tả>" --the "<thẻ 1>, <thẻ 2>" --chuyen' % BANG,
            'tu_lieu': tl}
    post_hook(body, 'kho:' + ','.join(sorted(x['id'] for x in tl)))
    for d in pend:
        board('PATCH', '/api/db/library/' + d['id'], {'phan_loai': 'dang'})
    for r, it in loc:
        it['phan_loai'], it['hoi'] = 'dang', now
    if loc:
        _cat_save(root, cat)
    log('Kho: đã nhờ TISA BOT phân loại %d tệp' % len(tl))
    return len(tl)


def _entries(root, docs, idx, cat):
    E = []
    for rel, it in cat['items'].items():
        E.append(dict(it, rel=rel, duong_dan=str(root / rel)))
    for d in docs or []:
        rel = idx.get(d['id'])
        if rel and (root / rel).exists():
            parts = Path(rel).parts
            ngan = {v: k for k, v in KHO_DIRS.items()}.get(parts[0]) if len(parts) > 1 else None
            E.append({'id': d['id'], 'ten': Path(d.get('name') or '').name, 'ngan': ngan or d.get('cat') or 'khac', 'kieu': d.get('kind') or 'file',
                      'kich_thuoc': d.get('size') or 0, 'ngay': str(d.get('created', ''))[:10], 'mo_ta': d.get('mo_ta', ''),
                      'the': d.get('the') or [], 'ghi_chu': d.get('note', ''), 'phan_loai': d.get('phan_loai'), 'rel': rel,
                      'duong_dan': str(root / rel), 'tu_bang': True})
    return E


def _line(e, root):
    s = '- `%s` · %s' % (_nfc(e['rel']), _size(e.get('kich_thuoc')))
    if e.get('mo_ta') and not e.get('nguon'):
        s += ' · %s' % e['mo_ta']
    if e.get('the') and not e.get('nguon'):
        s += ' · thẻ: %s' % ', '.join(e['the'])
    if e.get('ghi_chu'):
        s += ' · chủ ghi: %s' % e['ghi_chu']
    if e.get('hong'):
        s += ' · LỐI TẮT HỎNG (tệp gốc đã bị dời hoặc đổi tên)'
    return s


def write_muc_luc(root, docs, idx, cat):
    """MUC-LUC.md tổng ở gốc kho, mỗi ngăn một MUC-LUC.md riêng; chép bản tổng và các ngăn vào bộ não."""
    E = _entries(root, docs, idx, cat)
    by = {k: [] for k in KHO_DIRS}
    pend, hong = [], []
    for e in E:
        if e.get('phan_loai') in ('cho', 'dang'):
            pend.append(e)
        if e.get('hong'):
            hong.append(e)
        by.setdefault(e.get('ngan') or 'khac', []).append(e)
    tong = sum(int(e.get('kich_thuoc') or 0) for e in E)
    head = ['# Kho tư liệu', '',
            'Tư liệu thật của doanh nghiệp cho đội AI: đăng bài, dựng clip, thiết kế. Tệp nằm ngay trên máy, không đưa lên mạng.',
            'Phần lớn là lối tắt trỏ về tệp gốc ở Desktop hoặc Tải về: đọc, mở, dựng từ lối tắt là dùng tệp gốc. Không xóa, không sửa đè tệp gốc.',
            '', 'Thư mục kho: `%s`' % root,
            'Tổng: %d tư liệu, %s.' % (len(E), _size(tong)),
            'Tìm nhanh (không cần gõ dấu): `python3 "%s" kho --tim "từ khóa"`, thêm `--loai <ngăn>` để lọc.' % BANG, '',
            '| Ngăn | Mã | Số tệp | Dung lượng | Mục lục chi tiết |', '|---|---|---|---|---|']
    head_b = list(head)
    ml_brain = {}
    for k, folder in KHO_DIRS.items():
        L = by.get(k) or []
        row = '| %s | `%s` | %d | %s | ' % (KHO_TEN[k], k, len(L), _size(sum(int(e.get('kich_thuoc') or 0) for e in L)))
        head.append(row + '`%s/MUC-LUC.md` |' % folder)
        head_b.append(row + '[[MUC-LUC - %s]] |' % folder)
        lines = ['# %s' % KHO_TEN[k], '', 'Ngăn `%s` của kho tư liệu: %d tệp, %s.' % (k, len(L), _size(sum(int(e.get('kich_thuoc') or 0) for e in L))),
                 'Đường dẫn đầy đủ của mỗi tệp = `%s/` + đường dẫn bên dưới.' % root, '']
        groups = {}
        for e in L:
            parts = Path(e['rel']).parts
            g = _nfc(parts[1]) if len(parts) > 2 else 'Tệp để thẳng trong ngăn'
            groups.setdefault(g, []).append(e)
        for g in sorted(groups):
            G = sorted(groups[g], key=lambda e: _na(e['rel']))
            src = G[0].get('nguon')
            lines += ['## %s (%d)' % (g, len(G)), '']
            if src and all(x.get('nguon') for x in G):
                lines += ['Lối tắt trỏ về tệp gốc ở %s.' % ' › '.join(_goc(src).split(' › ')[:2]), '']
            lines += [_line(e, root) for e in G] + ['']
        text = '\n'.join(lines)
        if (root / folder).is_dir():
            _write_if(root / folder / 'MUC-LUC.md', text)
        ml_brain[folder] = text
    tail = []
    if pend:
        tail += ['', '## Đang chờ AI phân loại (%d)' % len(pend), ''] + ['- `%s`' % _nfc(e['rel']) for e in pend]
    if hong:
        tail += ['', '## Lối tắt hỏng (%d)' % len(hong), '', 'Tệp gốc đã bị dời hoặc đổi tên. Chủ dời lại, hoặc bỏ qua.', ''] + ['- `%s`' % _nfc(e['rel']) for e in hong[:200]]
    _write_if(root / 'MUC-LUC.md', '\n'.join(head + tail) + '\n')
    bk = None
    try:
        bk = brain_kho()
    except Exception:
        pass
    if bk and bk.resolve() != root.resolve():
        try:
            _write_if(bk / 'MUC-LUC.md', '\n'.join(head_b + tail) + '\n\nBản chép trong bộ não. Tệp thật nằm ở thư mục kho bên trên.\n')
            for folder, t in ml_brain.items():
                _write_if(bk / ('MUC-LUC - %s.md' % folder), t)
        except Exception:
            pass
    return E


def bao_kho(root, E):
    """Báo tóm tắt kho trên máy lên bảng (chỉ số đếm, không gửi tệp). Chỉ ghi khi có thay đổi hoặc mỗi 6 giờ."""
    ngan = {}
    for e in E:
        x = ngan.setdefault(e.get('ngan') or 'khac', [0, 0])
        x[0] += 1
        x[1] += int(e.get('kich_thuoc') or 0)
    doc = {'thu_muc': str(root), 'tong': len(E), 'dung_luong': sum(v[1] for v in ngan.values()),
           'ngan': {k: {'so': v[0], 'dung_luong': v[1], 'thu_muc': KHO_DIRS.get(k, '')} for k, v in ngan.items()},
           'cho': sum(1 for e in E if e.get('phan_loai') in ('cho', 'dang')), 'hong': sum(1 for e in E if e.get('hong'))}
    h = json.dumps(doc, sort_keys=True)
    if h == _KHO_BAO['h'] and time.time() - _KHO_BAO['t'] < 6 * 3600:
        return
    doc['cap_nhat'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    board('PUT', '/api/db/settings/khomay', doc)
    _KHO_BAO['h'], _KHO_BAO['t'] = h, time.time()


def sync_kho(classify=True):
    """Tệp mới trên bảng chép về máy; ghi sổ tệp có sẵn trong kho trên máy (không đưa lên mạng); nhờ AI phân loại tệp mới; viết MUC-LUC.md."""
    root = kho_root()
    if not root:
        return 0
    root.mkdir(parents=True, exist_ok=True)
    for v in list(KHO_DIRS.values()) + [KHO_INBOX]:
        (root / v).mkdir(exist_ok=True)
    idx = _idx(root)
    try:
        docs = kho_list()
    except Exception as e:
        docs = None
        log('Kho: chưa đọc được kho trên bảng (%s), vẫn ghi sổ kho trên máy' % e)
    n = 0
    for d in docs or []:
        if d['id'] in idx:
            continue
        folder = KHO_INBOX if (d.get('phan_loai') in ('cho', 'dang') and not d.get('giu_ngan')) else KHO_DIRS.get(d.get('cat'), KHO_DIRS['khac'])
        dest = _uniq(root / folder / Path(_safe_rel(d.get('name'))).name, d['id'])
        try:
            _download(d['blob'], dest)
            idx[d['id']] = str(dest.relative_to(root))
            n += 1
        except Exception as e:
            log('Chưa chép được %s: %s' % (d.get('name'), e))
    _save_idx(root, idx)
    cat = _cat_load(root)
    if scan_local(root, idx, cat):
        _cat_save(root, cat)
    if classify:
        try:
            if ask_classify(root, docs or [], idx, cat) and docs is not None:
                docs = kho_list()
        except Exception as e:
            log('Kho: chưa nhờ phân loại được: %s' % e)
    E = write_muc_luc(root, docs or [], idx, cat)
    try:
        bao_kho(root, E)
    except Exception as e:
        log('Kho: chưa báo tóm tắt lên bảng: %s' % e)
    if n:
        log('Kho tư liệu: đã chép %d tệp mới về %s' % (n, root))
    return n


def cmd_kho(a):
    root = kho_root()
    if not root:
        die('chưa có thư mục kho')
    idx, cat = _idx(root), _cat_load(root)
    try:
        docs = kho_list()
    except Exception:
        docs = []
    E = _entries(root, docs, idx, cat)
    if a.loai:
        E = [e for e in E if e.get('ngan') == a.loai]
    if a.tim:
        ws = _na(a.tim).split()
        E = [e for e in E if all(w in _na(' '.join([e['rel'], e.get('mo_ta', ''), ' '.join(e.get('the') or []), e.get('ghi_chu', ''), e.get('nguon', '')])) for w in ws)]
    tong = len(E)
    E = sorted(E, key=lambda e: (str(e.get('ngay', '')), e['rel']), reverse=True)[:max(1, a.gioi_han)]
    out({'thu_muc_kho': str(root), 'muc_luc': str(root / 'MUC-LUC.md'),
         'ngan': {k: {'ten': KHO_TEN[k], 'thu_muc': str(root / v)} for k, v in KHO_DIRS.items()},
         'tong_khop': tong, 'dang_hien': len(E),
         'tu_lieu': [{'id': e['id'], 'ten': e.get('ten'), 'ngan': e.get('ngan'), 'kieu': e.get('kieu'), 'kich_thuoc': _size(e.get('kich_thuoc')),
                      'mo_ta': e.get('mo_ta', ''), 'the': e.get('the') or [], 'ghi_chu': e.get('ghi_chu', ''),
                      'duong_dan': e['duong_dan'], 'tep_goc': e.get('nguon', ''), 'loi_tat_hong': bool(e.get('hong'))} for e in E]})


def cmd_kho_tai(a):
    """Chép tư liệu tải lên từ bảng về một thư mục (tư liệu trên máy thì dùng thẳng đường dẫn, không cần chép)."""
    docs = kho_list(a.loai, a.tim)
    if a.id:
        docs = [d for d in docs if d['id'] == a.id]
    root, got = Path(a.dir).expanduser(), []
    for d in docs:
        dest = root / _safe_rel(d.get('name'))
        try:
            _download(d['blob'], dest)
            got.append({'ten': d.get('name'), 'file': str(dest.resolve())})
        except Exception as e:
            got.append({'ten': d.get('name'), 'loi': str(e)[:200]})
    out({'ok': True, 'thu_muc': str(root.resolve()), 'so_tep': len(got), 'tep': got})


def cmd_kho_sua(a):
    root = kho_root()
    if not root:
        die('chưa có thư mục kho')
    idx = _idx(root)
    if a.loai and a.loai not in KHO_DIRS:
        die('ngăn không hợp lệ, chọn một trong: ' + ', '.join(KHO_DIRS))
    if a.id.startswith('may-'):
        cat = _cat_load(root)
        hit = [(r, it) for r, it in cat['items'].items() if it.get('id') == a.id]
        if not hit:
            die('không thấy tư liệu %s trong kho trên máy' % a.id)
        rel, it = hit[0]
        ngan = a.loai or it.get('ngan') or 'khac'
        it.update(ngan=ngan, phan_loai='xong')
        it.pop('hoi', None)
        if a.mo_ta:
            it['mo_ta'] = a.mo_ta.strip()[:600]
        if a.the:
            it['the'] = [t.strip() for t in a.the.split(',') if t.strip()][:12]
        moved = ''
        if a.chuyen and not it.get('lk'):   # tệp trong thư mục liên kết: không bao giờ dời tệp gốc của chủ
            src = root / rel
            parts = Path(rel).parts
            dst = root / KHO_DIRS[ngan] / (Path(*parts[1:]) if len(parts) > 1 else Path(parts[0]))
            if src.parent != dst.parent and (src.exists() or os.path.islink(str(src))):
                dst = _uniq(dst, a.id[4:])
                dst.parent.mkdir(parents=True, exist_ok=True)
                os.rename(str(src), str(dst))
                nrel = str(dst.relative_to(root))
                cat['items'][nrel] = cat['items'].pop(rel)
                rel, moved = nrel, str(dst)
        _cat_save(root, cat)
        try:
            docs = kho_list()
        except Exception:
            docs = []
        write_muc_luc(root, docs, idx, cat)
        out({'ok': True, 'id': a.id, 'ngan': ngan, 'chuyen_toi': moved or str(root / rel)})
        return
    d = board('GET', '/api/db/library/' + urllib.parse.quote(a.id))
    cat_ = a.loai or d.get('cat') or 'khac'
    if cat_ not in KHO_DIRS:
        cat_ = 'khac'
    patch = {'cat': cat_, 'phan_loai': 'xong'}
    if a.mo_ta:
        patch['mo_ta'] = a.mo_ta.strip()[:600]
    if a.the:
        patch['the'] = [t.strip() for t in a.the.split(',') if t.strip()][:12]
    moved = ''
    if a.chuyen and a.id in idx and (root / idx[a.id]).exists():
        src = root / idx[a.id]
        dst = root / KHO_DIRS[cat_] / src.name
        if src.resolve() != dst.resolve():
            dst = _uniq(dst, a.id)
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)
            idx[a.id] = str(dst.relative_to(root))
            moved = str(dst)
    board('PATCH', '/api/db/library/' + urllib.parse.quote(a.id), patch)
    _save_idx(root, idx)
    write_muc_luc(root, kho_list(), idx, _cat_load(root))
    out({'ok': True, 'id': a.id, 'ngan': cat_, 'chuyen_toi': moved or str(root / idx.get(a.id, ''))})


# ---------------- Kết nối của TISA BOT ----------------
# ---------------- Thư mục liên kết trên máy ----------------
# Chủ bấm "Liên kết thư mục trên máy" trên bảng và chọn một thư mục: bảng chỉ gửi TÊN thư mục và vài đường dẫn mẫu,
# không gửi tệp. Cầu nối tìm đúng thư mục đó trên máy, đặt lối tắt vào ngăn 12 của kho và ghi sổ từng tệp để đội đọc thẳng.
LK_FILE = '.thu-muc-lien-ket.json'
LK_MAX = 5000


def lien_ket_list(root):
    try:
        L = json.loads((Path(root) / LK_FILE).read_text(encoding='utf-8'))
        return [x for x in L if isinstance(x, dict) and x.get('ten') and x.get('duong_dan')]
    except Exception:
        return []


def _lk_save(root, L):
    (Path(root) / LK_FILE).write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding='utf-8')


def _noi(p):
    return _goc(str(Path(p) / 'x'))


def _tim_thu_muc(ten, mau):
    """Tìm thư mục tên `ten` trên máy (Desktop, Tài liệu, Tải về, iCloud/Drive, ổ ngoài, thư mục nhà). Chọn thư mục khớp nhiều tệp mẫu nhất."""
    ten_n, home = _nfc(ten), Path.home()
    uu_tien = [home / x for x in ('Desktop', 'Documents', 'Downloads', 'Movies', 'Pictures', 'Music', 'Dropbox')]
    for d in (home / 'Library' / 'CloudStorage', Path('/Volumes')):
        try:
            uu_tien += sorted(p for p in d.iterdir() if p.is_dir() and p.name != 'Macintosh HD')
        except Exception:
            pass
    BO = {'Library', 'Applications', 'node_modules', '__MACOSX', '.Trash', 'System'}
    seen, cand = set(), []

    def walk(d, depth):
        if depth > 6 or len(seen) > 60000:
            return
        try:
            es = list(os.scandir(str(d)))
        except Exception:
            return
        for e in es:
            try:
                if not e.is_dir(follow_symlinks=False) or e.name.startswith('.') or e.name in BO:
                    continue
            except OSError:
                continue
            if e.path in seen:
                continue
            seen.add(e.path)
            if _nfc(e.name) == ten_n:
                cand.append(Path(e.path))
            walk(e.path, depth + 1)

    for g in uu_tien:
        if g.is_dir():
            seen.add(str(g))
            if _nfc(g.name) == ten_n:
                cand.append(g)
            walk(g, 1)
    if not cand:
        walk(home, 1)
    mau = [m for m in (mau or []) if isinstance(m, dict) and m.get('p')][:60]
    best, bs = None, -1
    for c in dict.fromkeys(cand):
        sc = 0
        for m in mau:
            q = c / _safe_rel(m['p'])
            try:
                if q.is_file() and (not m.get('s') or q.stat().st_size == int(m['s'])):
                    sc += 1
            except Exception:
                pass
        if sc > bs:
            best, bs = c, sc
    if best is None:
        return None, 0.0
    return best, (bs / len(mau)) if mau else 1.0


def _lien_ket(root, ten, rp):
    """Đặt lối tắt tới thư mục rp vào ngăn 12 của kho, ghi vào sổ thư mục liên kết. Trả câu báo cho chủ."""
    rp = Path(rp).resolve()
    if rp == root.resolve() or root.resolve() in rp.parents:
        return 'Thư mục "%s" nằm sẵn trong kho tư liệu trên máy, đội đã dùng thẳng rồi.' % ten
    if rp == Path.home() or len(rp.parts) <= 3:
        raise RuntimeError('thư mục "%s" quá rộng (cả ổ hay cả thư mục nhà), anh chọn thư mục nhỏ hơn' % ten)
    dst = root / KHO_DIRS['may']
    dst.mkdir(parents=True, exist_ok=True)
    cua = dst / ten
    if os.path.islink(str(cua)):
        os.unlink(str(cua))
    if not cua.exists():
        os.symlink(str(rp), str(cua))
    n = 0
    for _, dns, fns in os.walk(str(rp)):
        dns[:] = [d for d in dns if not d.startswith('.')]
        n += len([x for x in fns if not x.startswith('.')])
    L = [x for x in lien_ket_list(root) if x['ten'] != ten]
    L.append({'ten': ten, 'duong_dan': str(rp), 'so_tep': n, 'luc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    _lk_save(root, L)
    return 'Đã liên kết "%s" (%d tệp) ở %s. Đội đọc thẳng trên máy, không tải lên mạng.%s' % (
        ten, n, _noi(rp), ' Thư mục có hơn %d tệp, đội chỉ ghi sổ %d tệp đầu.' % (LK_MAX, LK_MAX) if n > LK_MAX else '')


def _bo_lien_ket(root, ten):
    cua = root / KHO_DIRS['may'] / ten
    if os.path.islink(str(cua)):
        os.unlink(str(cua))
    _lk_save(root, [x for x in lien_ket_list(root) if x['ten'] != ten])
    return 'Đã bỏ liên kết "%s". Tệp gốc trên máy vẫn nguyên.' % ten


def handle_link(m):
    d = m.get('data') or {}
    ten = _nfc(str(d.get('ten') or m.get('path') or '').strip().strip('/'))
    st, note = 'da-mo', ''
    try:
        made = calendar.timegm(time.strptime(str(m.get('created', ''))[:19], '%Y-%m-%dT%H:%M:%S'))
        if time.time() - made > 3600:
            raise RuntimeError('yêu cầu cũ hơn 1 giờ, anh bấm liên kết lại')
        root = kho_root()
        if not root:
            raise RuntimeError('chưa có thư mục kho trên máy')
        if not ten or '/' in ten or ten in ('.', '..'):
            raise RuntimeError('thiếu tên thư mục')
        root.mkdir(parents=True, exist_ok=True)
        if d.get('bo'):
            note = _bo_lien_ket(root, ten)
        else:
            p, diem = _tim_thu_muc(ten, d.get('mau'))
            if not p:
                raise RuntimeError('chưa tìm thấy thư mục "%s" trên máy (đã tìm Desktop, Tài liệu, Tải về, iCloud, Google Drive, ổ ngoài). Anh để thư mục ở Desktop rồi bấm liên kết lại' % ten)
            if diem < 0.5:
                raise RuntimeError('thấy thư mục "%s" ở %s nhưng tệp bên trong không giống thư mục anh chọn' % (ten, _noi(p)))
            note = _lien_ket(root, ten, p)
        try:
            sync_kho(classify=False)
        except Exception as e:
            log('Kho: chưa ghi sổ thư mục liên kết: %s' % e)
        try:
            sync_ket_noi()
        except Exception:
            pass
    except Exception as e:
        st, note = 'loi', str(e)[:300]
    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
    board('PATCH', '/api/db/messages/' + urllib.parse.quote(m['id']), {'status': st, 'note': note})
    log('Liên kết thư mục: %s %s' % (st, note))


def cmd_lien_ket(a):
    root = kho_root()
    if not root:
        die('chưa có thư mục kho')
    p = Path(a.dir).expanduser()
    ten = _nfc(p.name)
    if a.bo:
        note = _bo_lien_ket(root, ten)
    else:
        if not p.is_dir():
            die('không thấy thư mục %s' % p)
        note = _lien_ket(root, ten, p)
    sync_kho(classify=False)
    try:
        sync_ket_noi()
    except Exception:
        pass
    out({'ok': True, 'bao': note, 'thu_muc_lien_ket': lien_ket_list(root)})


# ---------------- Bộ não: nạp kiến thức, chưng cất đêm ----------------
NGHE = str(Path(BANG).with_name('nghe.py'))


def nap_info():
    try:
        bo_nao = (board('GET', '/api/v1/kit').get('doanh_nghiep') or {}).get('bo_nao', '')
    except Exception:
        bo_nao = ''
    # Mặc định Obsidian mở chính thư mục bộ não; muốn tách riêng thì đặt OBSIDIAN_DIR.
    obs = Path(os.environ.get('OBSIDIAN_DIR') or C.get('OBSIDIAN_DIR') or bo_nao or (Path.home() / 'Desktop'))
    return {'obsidian': str(obs), 'so_tay_obsidian': str(obs / 'CLAUDE.md'), 'bo_nao_tisa_bot': bo_nao,
            'nghe_tep': PYQ + ' "%s" tep "<tệp video hoặc ghi âm>" "<ra.txt>"' % NGHE,
            'nghe_youtube': PYQ + ' "%s" youtube "<link>" "<thư mục ra>"' % NGHE}


def _slug_tieu_de(t, mx=34):
    s = re.sub(r'[^A-Za-z0-9 ]+', ' ', _na(t))
    out = ''
    for w in s.split():
        nx = (out + ' ' + w) if out else w
        if len(nx) > mx:
            break
        out = nx
    out = out or 'viec'
    return out[0].upper() + out[1:].lower()


def _b36(n):
    a, s = '0123456789abcdefghijklmnopqrstuvwxyz', ''
    while n:
        n, r = divmod(n, 36)
        s = a[r] + s
    return s or '0'


def tao_viec_chung_cat(tu, thu=False):
    dn = board('GET', '/api/v1/kit').get('doanh_nghiep') or {}
    office = (dn.get('thu_muc_van_phong') or '').strip() or 'Van Phong AI'
    lt = time.localtime()
    d, hm = time.strftime('%Y-%m-%d', lt), time.strftime('%H:%M', lt)
    iso = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    title = 'Chưng cất kiến thức đêm %s' % time.strftime('%d/%m', lt)
    task = ('Chưng cất kiến thức mới (lệnh tự động lúc 0h mỗi đêm). Quét mọi dữ liệu làm việc mới từ %s (giờ quốc tế) tới giờ: '
            'hội thoại với khách trên Fanpage, Zalo, bình luận (Hộp thư TISA BOT); việc chủ giao, góp ý, duyệt và tin nhắn anh hướng dẫn trên bảng; '
            'kết quả các việc đã xong; tài liệu và kiến thức mới nạp. Rút ra điều mới đáng nhớ (khách hay hỏi gì, phản đối nào, câu trả lời nào chốt được, '
            'chủ muốn làm việc thế nào, quy tắc mới, số liệu mới có ngày), chưng cất và cập nhật vào bộ não TISA BOT và Obsidian '
            '. Cách làm: theo mục "Chưng cất kiến thức đêm" trong skill dq-nhan-viec-tu-bang.') % tu
    jid = 'job-' + _b36(int(time.time() * 1000))
    doc = {'title': title, 'task': task, 'date': d, 'time': hm, 'created': iso, 'updated': iso, 'status': 'hang-doi', 'mode': 'claude',
           'demo': False, 'folder': '%s/03 - Ket qua/%s/%s/%s/%s %s/' % (office, d[:4], d[:7], d, hm.replace(':', ''), _slug_tieu_de(title)),
           'plan': [], 'summary': '', 'insights': [], 'synced': False, 'brain': 'cho-nap', 'files': [], 'kind': 'chung-cat-dem', 'tuLuc': tu}
    if thu:
        out(dict(doc, id=jid))
        return jid
    board('PUT', '/api/db/results/' + jid, doc)
    return jid


CC_FILE = ENV_FILE.parent / 'chung-cat-dem.json'


def chung_cat_tick():
    """Mỗi đêm từ 0h: tạo một việc chưng cất kiến thức trên bảng (máy ngủ lúc 0h thì tạo khi máy thức, trước 12h trưa)."""
    if os.environ.get('CHUNG_CAT') == '0':
        return
    lt = time.localtime()
    if lt.tm_hour >= 12:
        return
    hom_nay = time.strftime('%Y-%m-%d', lt)
    try:
        st = json.loads(CC_FILE.read_text(encoding='utf-8'))
    except Exception:
        st = {}
    if st.get('ngay') == hom_nay:
        return
    tu = st.get('luc') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 86400))
    jid = tao_viec_chung_cat(tu)
    CC_FILE.parent.mkdir(parents=True, exist_ok=True)
    CC_FILE.write_text(json.dumps({'ngay': hom_nay, 'luc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'viec': jid}), encoding='utf-8')
    log('Đã tạo việc chưng cất kiến thức đêm: %s' % jid)


def cmd_chung_cat(a):
    try:
        st = json.loads(CC_FILE.read_text(encoding='utf-8'))
    except Exception:
        st = {}
    tu = st.get('luc') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 86400))
    jid = tao_viec_chung_cat(tu, thu=a.thu)
    if not a.thu:
        out({'ok': True, 'viec': jid})


# ---------------- Bản bóc tách: chủ xem và sửa trên bảng ----------------
BT_MAX = 40000
BT_NOI = {'obsidian': 'Obsidian ', 'tisa_bot': 'Bộ não TISA BOT'}


def _goc_cho_phep():
    out = [Path(nap_info()['obsidian']).expanduser()]
    try:
        bn = (board('GET', '/api/v1/kit').get('doanh_nghiep') or {}).get('bo_nao', '')
        if bn:
            out.append(Path(bn).expanduser())
    except Exception:
        pass
    return [p.resolve() for p in out if p.exists()]


def cmd_boc_tach(a):
    """Gửi các trang vừa nạp lên bảng: chủ bấm Xem chi tiết bóc tách để đọc, sửa."""
    goc = _goc_cho_phep()
    tep = []
    for spec in a.tep or []:
        noi, _, path = str(spec).partition(':')
        if noi not in BT_NOI or not path:
            die('--tep phải có dạng obsidian:<đường dẫn> hoặc tisa_bot:<đường dẫn>')
        p = Path(path).expanduser().resolve()
        if p.suffix.lower() != '.md' or not p.is_file():
            die('không thấy trang %s' % p)
        if not any(g == p or g in p.parents for g in goc):
            die('trang %s không nằm trong Obsidian hay bộ não TISA BOT' % p)
        t = p.read_text(encoding='utf-8')
        tep.append({'noi': noi, 'ten': p.name, 'duong_dan': str(p), 'noi_dung': t[:BT_MAX], 'cat_bot': len(t) > BT_MAX})
    if not tep:
        die('cần ít nhất một --tep')
    bt = {'tom_tat': (a.tom_tat or '').strip()[:1500], 'tep': tep, 'cap_nhat': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    board('PATCH', '/api/db/results/' + urllib.parse.quote(a.job), {'bocTach': bt})
    out({'ok': True, 'job': a.job, 'tep': [x['duong_dan'] for x in tep]})


def handle_phan_loai_ngay(m):
    """Chủ bấm Phân tích, sắp xếp ngay: quét kho, đưa tệp kẹt quá 10 phút về hàng chờ, nhờ AI xem và xếp ngăn ngay."""
    st, note = 'da-mo', ''
    try:
        root = kho_root()
        if not root:
            raise RuntimeError('chưa có thư mục kho trên máy')
        sync_kho(classify=False)
        cat, now, k = _cat_load(root), time.time(), 0
        for it in cat['items'].values():
            if it.get('phan_loai') == 'dang' and now - float(it.get('hoi') or 0) > 600:
                it['phan_loai'] = 'cho'
                k += 1
        if k:
            _cat_save(root, cat)
        if not javis_up():
            raise RuntimeError('TISA BOT trên máy chưa mở nên chưa nhờ AI được. Mở TISA BOT rồi bấm lại.')
        try:
            docs = kho_list()
        except Exception:
            docs = []
        n = ask_classify(root, docs, _idx(root), cat)
        cho = sum(1 for it in _cat_load(root)['items'].values() if it.get('phan_loai') in ('cho', 'dang'))
        if n:
            note = 'Đã nhờ AI xem và xếp ngăn %d tệp ngay, khoảng 1 đến 3 phút là xong.%s' % (
                n, (' Còn %d tệp, AI làm tiếp từng lượt 15 tệp.' % (cho - n)) if cho > n else '')
        else:
            note = 'Không còn tệp nào chờ phân loại. Tệp vừa bỏ vào dưới 30 giây thì đợi chút rồi bấm lại.'
        try:
            sync_kho(classify=False)
        except Exception:
            pass
    except Exception as e:
        st, note = 'loi', str(e)[:300]
    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
    board('PATCH', '/api/db/messages/' + urllib.parse.quote(m['id']), {'status': st, 'note': note})
    log('Phân loại ngay: %s %s' % (st, note))


def handle_ghi_boc_tach(m):
    """Chủ sửa bản bóc tách trên bảng và bấm Lưu: ghi đúng trang đó trong Obsidian / bộ não TISA BOT (giữ bản cũ để quay lại)."""
    st, note = 'da-mo', ''
    try:
        jid = str((m.get('data') or {}).get('job') or '')
        if not jid:
            raise RuntimeError('thiếu mã việc')
        r = board('GET', '/api/db/results/' + urllib.parse.quote(jid))
        bt = r.get('bocTach') or {}
        goc = _goc_cho_phep()
        luu = ENV_FILE.parent / 'sao-luu-boc-tach'
        n, loi = 0, []
        for t in bt.get('tep') or []:
            if not t.get('cho_ghi'):
                continue
            p = Path(str(t.get('duong_dan') or '')).expanduser().resolve()
            if p.suffix.lower() != '.md' or not any(g in p.parents for g in goc):
                loi.append('%s nằm ngoài bộ não, không ghi' % p.name)
                t['cho_ghi'] = False
                continue
            if t.get('cat_bot'):
                loi.append('%s dài quá nên bảng chỉ giữ một phần, không ghi đè' % p.name)
                t['cho_ghi'] = False
                continue
            if p.exists():
                luu.mkdir(parents=True, exist_ok=True)
                (luu / ('%s-%s' % (time.strftime('%Y%m%d-%H%M%S'), p.name))).write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(str(t.get('noi_dung') or ''), encoding='utf-8')
            t['cho_ghi'] = False
            t['da_ghi_luc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            n += 1
        board('PATCH', '/api/db/results/' + urllib.parse.quote(jid), {'bocTach': bt})
        note = ('Đã ghi %d trang anh sửa vào bộ não.' % n) + (' ' + '; '.join(loi) if loi else '')
        if not n and loi:
            st = 'loi'
    except Exception as e:
        st, note = 'loi', str(e)[:300]
    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
    board('PATCH', '/api/db/messages/' + urllib.parse.quote(m['id']), {'status': st, 'note': note})
    log('Ghi bản bóc tách: %s %s' % (st, note))


# ---------------- Giám sát việc bị kẹt ----------------
# Việc đang chạy mà quá KET_PHUT phút không có tiến độ: soi sổ webhook của TISA BOT để biết lượt làm việc cuối ra sao
# (còn chạy, lỗi, hay đã kết thúc mà bỏ dở), ghi lý do lên bảng để chủ thấy và bấm Làm tiếp / Tạm dừng / Kết thúc.
KET_PHUT = 45
RUN_ST = ('dang-chay', 'da-duyet', 'cho-that', 'can-sua')
P_XONG = ('done', 'given', 'skip', 'stop', 'duyet', 'owner')


def _ts(iso):
    try:
        return calendar.timegm(time.strptime(str(iso)[:19], '%Y-%m-%dT%H:%M:%S'))
    except Exception:
        return 0


def _gio(ts):
    return time.strftime('%H:%M %d/%m', time.localtime(ts)) if ts else ''


def _luot_cuoi(jid):
    """Lượt TISA BOT cuối cùng nhận việc này: (trạng thái sự kiện, trạng thái lượt, giờ bắt đầu, giờ xong, lỗi, lời cuối)."""
    import sqlite3
    d = javis_dir()
    f = d / 'webhook_events.sqlite3' if d else None
    if not f or not f.exists():
        return None
    con = sqlite3.connect('file:%s?mode=ro' % f, uri=True, timeout=5)
    try:
        ev = con.execute("select id, received_at, status from events where cast(body as text) like ? order by received_at desc limit 1", ('%' + jid + '%',)).fetchone()
        if not ev:
            return {}
        dl = con.execute("select status, dispatched_at, finished_at, detail, result from deliveries where event_id=? order by generation desc limit 1", (ev[0],)).fetchone()
        o = {'su_kien': ev[2], 'nhan_luc': ev[1]}
        if dl:
            o.update(luot=dl[0], bat_dau=dl[1], xong_luc=dl[2], loi=str(dl[3] or '')[:300], loi_cuoi=str(dl[4] or '')[:400])
        return o
    finally:
        con.close()


def giam_sat_ket():
    docs = board('GET', '/api/db/results', timeout=30).get('docs') or []
    try:
        ten = {x.get('ma'): x.get('ten') for x in (board('GET', '/api/v1/kit').get('doi') or [])}
    except Exception:
        ten = {}
    now = time.time()
    for r in docs:
        if r.get('demo') or r.get('status') not in RUN_ST:
            continue
        con = [p for p in (r.get('plan') or []) if p.get('state') not in P_XONG]
        if not con and r.get('plan'):
            continue
        moc = r.get('updated') or r.get('created') or ''
        t = _ts(moc)
        if not t or now - t < KET_PHUT * 60 or (r.get('ket') or {}).get('moc') == moc:
            continue
        L = _luot_cuoi(r['id'])
        tam = ten.get('tam') or 'Tâm'
        ds = ', '.join('%s phần %s%s' % (ten.get(p.get('agent')) or p.get('agent'), p.get('n'), (' (%s%%)' % p['pct']) if p.get('pct') else '') for p in con[:6])
        k = {'moc': moc, 'tu': moc, 'luc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        if L is None:
            k['ly_do'] = 'Không đọc được sổ việc của TISA BOT trên máy để biết nguyên nhân.'
        elif not L:
            k['ly_do'] = 'TISA BOT chưa nhận được việc này. Kiểm tra TISA BOT trên máy có đang mở không, rồi bấm Nhờ %s làm tiếp.' % tam
        else:
            lt = str(L.get('luot') or '')
            if lt in ('pending', 'queued', 'running', 'dispatched', 'claimed', 'in_progress') and now - float(L.get('bat_dau') or L.get('nhan_luc') or 0) < 3 * 3600:
                continue   # TISA BOT vẫn đang làm lượt này: chưa coi là kẹt
            if lt in ('failed', 'dead', 'error', 'cancelled', 'canceled', 'expired'):
                k['ly_do'] = 'Lượt làm việc của TISA BOT bị lỗi lúc %s: %s' % (_gio(L.get('xong_luc') or L.get('bat_dau')), L.get('loi') or lt)
            elif lt in ('pending', 'queued', 'running', 'dispatched', 'claimed', 'in_progress'):
                k['ly_do'] = 'TISA BOT nhận việc lúc %s nhưng chạy quá 3 giờ không báo gì, có thể đã treo.' % _gio(L.get('bat_dau') or L.get('nhan_luc'))
            else:
                nen = any(w in (L.get('loi_cuoi') or '').lower() for w in ('nền', 'song song', 'đang chờ', 'đang chạy'))
                k['ly_do'] = ('Lượt làm việc cuối của %s kết thúc lúc %s nhưng còn %d phần chưa xong%s.%s' % (
                    tam, _gio(L.get('xong_luc')), len(con), (': ' + ds) if ds else '',
                    ' %s để việc chạy nền rồi kết thúc lượt, việc nền dừng theo nên không ai làm tiếp.' % tam if nen else ' Không có lượt nào làm tiếp sau đó.'))
                k['loi_cuoi'] = L.get('loi_cuoi') or ''
        board('PATCH', '/api/db/results/' + urllib.parse.quote(r['id']), {'ket': k})
        log('Việc kẹt %s: %s' % (r['id'], k['ly_do'][:120]))


# ---------------- Phòng ban mới ----------------
MAU_PHONG = ['#C2410C', '#0F766E', '#7C3AED', '#BE185D', '#4D7C0F', '#0369A1', '#A16207', '#334155']


def _ma(s, n=30):
    return re.sub(r'[^a-z0-9]+', '-', _na(s)).strip('-')[:n].strip('-') or 'moi'


def cmd_phong_ban(a):
    """Đăng ký phòng ban mới và nhân sự của phòng lên bảng (thêm hoặc sửa theo mã phòng)."""
    spec = json.loads(Path(a.file).read_text(encoding='utf-8'))
    ph, ns = spec.get('phong') or {}, spec.get('nhan_su') or []
    if not str(ph.get('ten') or '').strip() or not ns:
        die('phong-ban.json cần "phong" có "ten", và ít nhất một người trong "nhan_su"')
    try:
        kit = board('GET', '/api/db/settings/kit')
    except RuntimeError as e:
        if ' 404' not in str(e):
            raise
        kit = {}
    kit.pop('id', None)
    team = kit.get('team') if isinstance(kit.get('team'), dict) else {}
    rx = [r for r in (team.get('roomsX') or []) if isinstance(r, dict)]
    ma = str(ph.get('ma') or '')
    rid = ma if re.match(r'^x-[\w-]{2,40}$', ma) else 'x-' + _ma(re.sub(r'(?i)^ph[oò]ng\s+', '', _nfc(ph['ten'])))
    cu = next((r for r in rx if r.get('id') == rid), None)
    dung = {r.get('color') for r in rx if r.get('id') != rid}
    mau = str(ph.get('mau') or '')
    color = mau if re.match(r'^#[0-9a-fA-F]{6}$', mau) else (cu or {}).get('color') or next((c for c in MAU_PHONG if c not in dung), MAU_PHONG[0])
    ten_phong = _nfc(str(ph['ten']).strip())
    if not ten_phong.lower().startswith('phòng'):
        ten_phong = 'Phòng ' + ten_phong
    room = {'id': rid, 'name': ten_phong[:60], 'color': color, 'desc': str(ph.get('mo_ta') or '')[:240],
            'sau': str(ph.get('sau') or '')[:40], 'ngay': (cu or {}).get('ngay') or time.strftime('%Y-%m-%d')}
    rx = [r for r in rx if r.get('id') != rid] + [room]
    custom = [x for x in (team.get('custom') or []) if isinstance(x, dict)]
    them = []
    for n in ns[:6]:
        ten = _nfc(str(n.get('ten') or '').strip())[:60]
        if not ten:
            continue
        m2 = str(n.get('ma') or '')
        aid = m2 if re.match(r'^x-[\w-]{2,40}$', m2) else 'x-' + _ma(ten)
        ag = {'id': aid, 'name': ten, 'title': str(n.get('chuc_danh') or '')[:120], 'room': rid, 'gender': 'm' if n.get('gioi') == 'm' else 'f',
              'jobs': [str(j)[:120] for j in (n.get('viec') or [])][:8], 'to': str(n.get('ban_giao_cho') or '')[:120],
              'input': str(n.get('nhan_tu') or '')[:200], 'output': str(n.get('dau_ra') or '')[:200], 'skill': str(n.get('ky_nang') or '')[:120]}
        custom = [x for x in custom if x.get('id') != aid] + [ag]
        them.append({'ma': aid, 'ten': ten})
    if not them:
        die('chưa có nhân sự nào có tên')
    team['roomsX'] = rx[-8:]
    team['custom'] = custom[-40:]
    kit['team'] = team
    board('PUT', '/api/db/settings/kit', kit)
    out({'ok': True, 'phong': {'ma': rid, 'ten': room['name'], 'mau': color, 'sau': room['sau']}, 'nhan_su': them,
         'luu_y': 'Bảng hiện phòng mới khi anh tải lại trang. Mã nhân sự mới dùng được ngay trong plan.json.'})


def javis_dir():
    if C.get('JAVIS_DIR') and (Path(C['JAVIS_DIR']).expanduser() / 'mcp_servers.json').exists():
        return Path(C['JAVIS_DIR']).expanduser()
    for p in (str(Path(__file__).resolve().parents[2] / 'server'),):
        d = Path(p).expanduser()
        if (d / 'settings.json').exists():
            return d
    return None


def _rj(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:
        return {}


def sync_ket_noi():
    """Đọc tên và trạng thái các kết nối của TISA BOT (không đọc khóa) rồi báo lên bảng."""
    d = javis_dir()
    if not d:
        return False
    mcp = _rj(d / 'mcp_servers.json').get('connections') or []
    acc = _rj(d / 'channel_accounts.json').get('accounts') or []
    bots = _rj(d / 'chatbots.json').get('bots') or []
    st = _rj(d / 'settings.json')
    m = st.get('model') or {}
    main = m.get('main') or {}
    oa = m.get('openai_oauth') or {}
    packs = _rj(d / 'packs.json')
    doc = {
        'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'mcp': [{'ten': c.get('label') or c.get('slug') or '', 'loai': c.get('connector_id') or '', 'cach': 'MCP ' + (c.get('transport') or ''), 'bat': bool(c.get('enabled', True))} for c in mcp],
        'kenh': [{'kenh': a.get('channel') or '', 'ten': a.get('label') or ''} for a in acc],
        'bots': [{'ten': b.get('name') or '', 'kenh': b.get('channel') or '', 'bat': bool(b.get('enabled'))} for b in bots],
        'mo_hinh': {'chinh': ('%s %s' % ('Claude' if 'anthropic' in str(main.get('provider', '')) else main.get('provider', ''), main.get('model', ''))).strip(),
                    'chatgpt': ('đã kết nối' + (' (gói %s)' % oa['plan'] if oa.get('plan') else '')) if oa.get('access_token') else 'chưa kết nối'},
        'goi': sorted(packs.keys()) if isinstance(packs, dict) else [],
    }
    try:
        kr = kho_root()
        if kr:
            doc['kho_may'] = str(kr)
            doc['thu_muc_lien_ket'] = [{'ten': x['ten'], 'duong_dan': x['duong_dan'], 'so_tep': x.get('so_tep'), 'luc': x.get('luc')} for x in lien_ket_list(kr)]
    except Exception:
        pass
    board('PUT', '/api/db/settings/tisabot', doc)
    return True


def cmd_dong_bo(a):
    n = sync_kho()
    ok = sync_ket_noi()
    root = kho_root()
    out({'ok': True, 'kho_tep_moi_tu_bang': n, 'kho_tren_may': len(_cat_load(root)['items']) if root else 0,
         'ket_noi': 'đã báo lên bảng' if ok else 'không thấy thư mục TISA BOT'})


def cmd_tra_loi(a):
    t = Path(a.text_file).read_text(encoding='utf-8') if a.text_file else (a.text or '')
    if not t.strip():
        die('thiếu nội dung trả lời (--text hoặc --text-file)')
    body = {'replyTo': a.msg, 'from': a.from_ or '', 'text': t, 'done': not a.chua_xong}
    if a.claude_prompt_file:
        body['claudePrompt'] = Path(a.claude_prompt_file).read_text(encoding='utf-8')
    out(board('POST', '/api/v1/tin/tra-loi', body))


def cmd_nho_claude(a):
    """Chép lời nhờ vào bộ nhớ tạm, mở app Claude, mở cuộc trò chuyện mới và dán (thử gửi luôn nếu --gui)."""
    import subprocess
    prompt = Path(a.file).read_text(encoding='utf-8')
    res = {'chep': False, 'mo_claude': False, 'dan': False, 'gui': False}
    try:
        subprocess.run(['pbcopy'], input=prompt.encode('utf-8'), check=True)
        res['chep'] = True
    except Exception as e:
        res['loi_chep'] = str(e)[:200]
    try:
        subprocess.run(['open', '-a', 'Claude'], check=True, timeout=20)
        res['mo_claude'] = True
    except Exception as e:
        res['loi_mo'] = str(e)[:200]
    if res['chep'] and res['mo_claude'] and not a.chi_mo:
        script = ['-e', 'delay 2', '-e', 'tell application "Claude" to activate', '-e', 'delay 1',
                  '-e', 'tell application "System Events" to keystroke "n" using command down', '-e', 'delay 1.5',
                  '-e', 'tell application "System Events" to keystroke "v" using command down']
        if a.gui:
            script += ['-e', 'delay 0.8', '-e', 'tell application "System Events" to key code 36']
        r = subprocess.run(['osascript'] + script, capture_output=True, text=True, timeout=40)
        if r.returncode == 0:
            res['dan'] = True
            res['gui'] = bool(a.gui)
        else:
            res['loi_dan'] = (r.stderr or '').strip()[:300]
    out(res)


def cmd_tin(a):
    out(board('GET', '/api/v1/tin/hang-doi'))


def log(msg):
    print(time.strftime('%Y-%m-%d %H:%M:%S ') + msg, flush=True)


def javis_up():
    try:
        with urllib.request.urlopen(C['JAVIS_URL'].rstrip('/') + '/health', timeout=4) as r:
            return r.status < 500
    except urllib.error.HTTPError as e:
        return e.code < 500
    except Exception:
        return False


def cmd_cau_noi(a):
    log('Cầu nối bảng -> TISA BOT đang chạy (mỗi %ss). Kho tư liệu chạy trên máy, không đưa tệp của máy lên mạng.' % a.moi)
    fails, ver_j, ver_m, up_at, up = 0, None, None, 0, True
    me = Path(BANG)
    try:
        m0 = me.stat().st_mtime
    except OSError:
        m0 = None
    kho_at, kho_ver, kn_at, kho_scan, cc_at, ket_at = 0, None, 0, 0, 0, 0
    while True:
        try:   # có bản cầu nối mới (cập nhật khung): tự khởi động lại bằng bản mới
            if m0 is not None and me.stat().st_mtime != m0:
                time.sleep(2)
                log('Có bản cầu nối mới, khởi động lại')
                os.execv(sys.executable, [sys.executable, BANG] + sys.argv[1:])
        except OSError:
            pass
        try:
            if time.time() - kho_at > 60:
                kho_at = time.time()
                try:
                    v = (board('GET', '/api/ver', timeout=20).get('cols') or {}).get('library')
                    if v != kho_ver or time.time() - kho_scan > 120:
                        sync_kho(classify=up)
                        kho_ver, kho_scan = v, time.time()
                except Exception as e:
                    log('Chưa đồng bộ được kho tư liệu: %s' % e)
            if time.time() - kn_at > 600:
                kn_at = time.time()
                try:
                    sync_ket_noi()
                except Exception as e:
                    log('Chưa đồng bộ được kết nối TISA BOT: %s' % e)
            if time.time() - ket_at > 300:
                ket_at = time.time()
                try:
                    giam_sat_ket()
                except Exception as e:
                    log('Chưa soi được việc kẹt: %s' % e)
            if time.time() - cc_at > 60:
                cc_at = time.time()
                try:
                    chung_cat_tick()
                except Exception as e:
                    log('Chưa tạo được việc chưng cất đêm: %s' % e)
            if time.time() - up_at > 30:
                was, up, up_at = up, javis_up(), time.time()
                if was != up:
                    log('TISA BOT %s' % ('đang chạy' if up else 'chưa mở: việc mới được giữ trên bảng'))
            if not up:
                time.sleep(15)   # TISA BOT chưa mở: không nhận việc, bảng tự báo "chưa thấy TISA BOT" sau 3 phút
                continue
            q = board('GET', '/api/v1/queue' + ('?since=%s' % ver_j if ver_j is not None else ''), timeout=20)
            ok = True
            for j in q.get('jobs', []):
                try:
                    st = send_to_javis(j)
                    board('POST', '/api/v1/ack/' + j['id'], {'state': 'da-gui', 'note': 'TISA BOT nhận (%s)' % st})
                    log('Đã chuyển cho TISA BOT: %s %s' % (j['id'], j.get('title', '')[:60]))
                except Exception as e:
                    ok = False
                    log('Chưa chuyển được %s: %s' % (j['id'], e))
            # chỉ nhớ phiên bản khi đã chuyển hết, để việc chưa chuyển được thử lại ở lượt sau
            ver_j = q.get('ver') if ok and not q.get('jobs') else None
            t = board('GET', '/api/v1/tin/hang-doi' + ('?since=%s' % ver_m if ver_m is not None else ''), timeout=20)
            ok = True
            for m in t.get('tin', []):
                if m.get('kind') == 'kiem-tra-ket-noi':
                    try:
                        sync_ket_noi()
                        board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
                        board('PATCH', '/api/db/messages/' + urllib.parse.quote(m['id']), {'status': 'da-mo', 'note': 'đã đồng bộ'})
                        log('Đã đồng bộ kết nối TISA BOT theo yêu cầu')
                    except Exception as e:
                        log('Chưa đồng bộ được kết nối: %s' % e)
                    continue
                if m.get('kind') == 'phan-loai-ngay':
                    try:
                        handle_phan_loai_ngay(m)
                    except Exception as e:
                        log('Chưa phân loại ngay được: %s' % e)
                    continue
                if m.get('kind') == 'ghi-boc-tach':
                    try:
                        handle_ghi_boc_tach(m)
                    except Exception as e:
                        log('Chưa ghi được bản bóc tách: %s' % e)
                    continue
                if m.get('kind') == 'lien-ket-thu-muc':
                    try:
                        handle_link(m)
                    except Exception as e:
                        log('Chưa liên kết được thư mục: %s' % e)
                    continue
                if m.get('kind') == 'mo-thu-muc':
                    try:
                        handle_open(m)
                    except Exception as e:
                        log('Chưa mở được thư mục: %s' % e)
                    continue
                if m.get('dm') and _chat_nhanh(m):   # CHAT-NOI-BO: chat nội bộ đi đường nhanh
                    continue
                try:
                    st = send_msg_to_javis(m)
                    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
                    log('Đã chuyển tin nhắn cho %s (%s): %s' % (m.get('to'), st, m.get('text', '')[:50]))
                except Exception as e:
                    ok = False
                    log('Chưa chuyển được tin %s: %s' % (m['id'], e))
            ver_m = t.get('ver') if ok and not t.get('tin') else None
            fails = 0
        except Exception as e:
            fails += 1
            ver_j = ver_m = None
            if fails in (1, 10) or fails % 60 == 0:
                log('Chưa nối được bảng: %s' % e)
        time.sleep((min(a.moi, 1.5) if _chat_gan() else a.moi) if fails < 10 else 30)  # CHAT-NOI-BO


def cmd_kiem_tra(a):
    print('Tệp khoá:', ENV_FILE, 'có' if ENV_FILE.is_file() else 'CHƯA CÓ')
    for k in ('BOARD_URL', 'BOARD_TOKEN', 'JAVIS_URL', 'JAVIS_HOOK_ID', 'JAVIS_HOOK_TOKEN'):
        print(' ', k, ':', ('đã có' if C.get(k) else 'THIẾU') + (' (' + C[k] + ')' if k in ('BOARD_URL', 'JAVIS_URL') and C.get(k) else ''))
    try:
        q = board('GET', '/api/v1/queue', timeout=15)
        print('Bảng: kết nối được, đang chờ chuyển', len(q.get('jobs', [])), 'việc')
    except Exception as e:
        print('Bảng: CHƯA kết nối được:', e)
    try:
        with urllib.request.urlopen(C['JAVIS_URL'].rstrip('/') + '/health', timeout=5) as r:
            print('TISA BOT: đang chạy (%s)' % r.status)
    except Exception as e:
        print('TISA BOT: không thấy ở', C['JAVIS_URL'], e)


# ---------------- Chat nội bộ: đường nhanh (CHAT-NOI-BO) ----------------
_CN = {'mod': None, 'brain': '', 'at': 0}


def _chat_mod():
    if _CN['mod'] is None:
        sys.path.insert(0, str(Path(BANG).parent))
        import chat_nhanh
        _CN['mod'] = chat_nhanh
    return _CN['mod']


def _chat_brain():
    if time.time() - _CN['at'] > 600:
        try:
            _CN['brain'] = ((board('GET', '/api/v1/kit').get('doanh_nghiep') or {}).get('bo_nao') or '').strip()
            _CN['at'] = time.time()
        except Exception:
            pass
    return str(Path(_CN['brain']).expanduser()) if _CN['brain'] else ''


def _chat_nhanh(m):
    try:
        return _chat_mod().nhan(m, board, C, log, send_msg_to_javis, BANG, _chat_brain())
    except Exception as e:
        log('Chat nhanh chưa chạy được, gửi đường thường: %s' % e)
        return False


def _chat_gan():
    try:
        return time.time() - _chat_mod().CHAT_LUC[0] < 300
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser(description='Nối TISA BOT với bảng giao việc Đội Quân AI')
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('lay'); s.add_argument('job'); s.set_defaults(f=cmd_lay)
    s = sp.add_parser('ke-hoach'); s.add_argument('job'); s.add_argument('file'); s.set_defaults(f=cmd_ke_hoach)
    s = sp.add_parser('phan'); s.add_argument('job'); s.add_argument('n', type=int)
    s.add_argument('--state'); s.add_argument('--agent'); s.add_argument('--viec'); s.add_argument('--pct', type=int)
    s.add_argument('--out'); s.add_argument('--out-file'); s.add_argument('--append'); s.add_argument('--claude-prompt-file'); s.set_defaults(f=cmd_phan)
    s = sp.add_parser('kho'); s.add_argument('--loai'); s.add_argument('--tim'); s.add_argument('--gioi-han', type=int, default=80); s.set_defaults(f=cmd_kho)
    s = sp.add_parser('kho-tai'); s.add_argument('dir'); s.add_argument('--loai'); s.add_argument('--tim'); s.add_argument('--id'); s.set_defaults(f=cmd_kho_tai)
    s = sp.add_parser('dong-bo'); s.set_defaults(f=cmd_dong_bo)
    s = sp.add_parser('lien-ket'); s.add_argument('dir'); s.add_argument('--bo', action='store_true'); s.set_defaults(f=cmd_lien_ket)
    s = sp.add_parser('phong-ban'); s.add_argument('file'); s.set_defaults(f=cmd_phong_ban)
    s = sp.add_parser('chung-cat'); s.add_argument('--thu', action='store_true'); s.set_defaults(f=cmd_chung_cat)
    s = sp.add_parser('boc-tach'); s.add_argument('job'); s.add_argument('--tom-tat'); s.add_argument('--tep', action='append'); s.set_defaults(f=cmd_boc_tach)
    s = sp.add_parser('kho-sua'); s.add_argument('id'); s.add_argument('--loai'); s.add_argument('--mo-ta'); s.add_argument('--the'); s.add_argument('--chuyen', action='store_true'); s.set_defaults(f=cmd_kho_sua)
    s = sp.add_parser('ky-nang'); s.add_argument('agent'); s.add_argument('--ten', required=True); s.add_argument('--mo-ta'); s.add_argument('--duong-dan'); s.add_argument('--nguon'); s.set_defaults(f=cmd_ky_nang)
    s = sp.add_parser('anh'); s.add_argument('job'); s.add_argument('file'); s.add_argument('--title'); s.set_defaults(f=cmd_anh)
    s = sp.add_parser('tai'); s.add_argument('id'); s.add_argument('dest'); s.set_defaults(f=cmd_tai)
    s = sp.add_parser('tai-het'); s.add_argument('job'); s.add_argument('dir'); s.add_argument('--msg'); s.set_defaults(f=cmd_tai_het)
    s = sp.add_parser('link'); s.add_argument('job'); s.add_argument('--title', required=True); s.add_argument('--url', required=True)
    s.add_argument('--kind', default='doc'); s.set_defaults(f=cmd_link)
    s = sp.add_parser('xong'); s.add_argument('job'); s.add_argument('--status', default='cho-duyet'); s.add_argument('--summary'); s.set_defaults(f=cmd_xong)
    s = sp.add_parser('hang-doi'); s.set_defaults(f=cmd_hang_doi)
    s = sp.add_parser('tra-loi'); s.add_argument('msg'); s.add_argument('--from', dest='from_'); s.add_argument('--text'); s.add_argument('--text-file')
    s.add_argument('--chua-xong', action='store_true'); s.add_argument('--claude-prompt-file'); s.set_defaults(f=cmd_tra_loi)
    s = sp.add_parser('nho-claude'); s.add_argument('file'); s.add_argument('--gui', action='store_true'); s.add_argument('--chi-mo', action='store_true')
    s.set_defaults(f=cmd_nho_claude)
    s = sp.add_parser('tin'); s.set_defaults(f=cmd_tin)
    s = sp.add_parser('cau-noi'); s.add_argument('--moi', type=int, default=5); s.set_defaults(f=cmd_cau_noi)
    s = sp.add_parser('doi'); s.set_defaults(f=cmd_doi)
    s = sp.add_parser('kiem-tra'); s.set_defaults(f=cmd_kiem_tra)
    a = ap.parse_args()
    try:
        a.f(a)
    except RuntimeError as e:
        die(str(e))


if __name__ == '__main__':
    main()
