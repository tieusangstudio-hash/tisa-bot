"""chat_nhanh.py - đường nhanh cho Chat nội bộ trên bảng Đội Quân AI.

Tin chủ nhắn riêng một nhân sự (có `dm`) đi thẳng vào khung chat cộng sự của TISA BOT
(POST /chat/stream, đúng agent đó, giữ phiên riêng từng người) thay vì đi webhook chạy việc nặng.
Trả lời thường chỉ vài giây. Có token TISA BOT loại "Chỉ chat" (TISA_API_TOKEN trong ~/.config/doi-quan-ai/.env) thì đi khung chat cộng sự;
không có thì gọi thẳng Claude trên máy (cùng tài khoản TISA BOT đang dùng), đóng vai đúng nhân sự, giữ phiên riêng.
Lỗi thì gửi theo đường cũ (webhook), không mất tin.

  python3 chat_nhanh.py dat-khoa      dán token TISA BOT (ẩn khi gõ), lưu vào .env
  python3 chat_nhanh.py thu tam "..."  hỏi thử một nhân sự, in thời gian trả lời
"""
import json, os, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ENV = Path(os.environ.get('DOI_QUAN_ENV') or Path.home() / '.config' / 'doi-quan-ai' / '.env')
PHIEN = ENV.parent / 'chat-phien.json'
LOCK = threading.Lock()
KHOA = {}          # mỗi nhân sự một khóa: tin của cùng một người trả lời lần lượt
CHAT_LUC = [0.0]   # lúc có tin chat gần nhất: cầu nối hỏi bảng dày hơn trong 5 phút sau đó


def _env():
    c = {}
    try:
        for line in ENV.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                c[k.strip()] = v.strip().strip('"\'')
    except FileNotFoundError:
        pass
    return c


def _phien_doc():
    try:
        return json.loads(PHIEN.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _phien_ghi(d):
    PHIEN.parent.mkdir(parents=True, exist_ok=True)
    PHIEN.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    os.chmod(PHIEN, 0o600)


def _na(s):
    s = unicodedata.normalize('NFD', str(s or '')).replace('đ', 'd').replace('Đ', 'D')
    return ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn').lower()


def agent_slug(brain, ma):
    """Mã nhân sự trên bảng (tam, linh...) -> tên tệp agent trong brain (dq-tam-tong-quan)."""
    d = Path(brain) / 'agents'
    if not d.is_dir():
        return ''
    ma = _na(ma)
    for f in sorted(d.glob('*.md')):
        st = _na(f.stem)
        if st == ma or st.startswith('dq-%s-' % ma) or st == 'dq-' + ma:
            return f.stem
    return ''


def _message(m):
    t = str(m.get('text') or '').strip()
    extra = []
    imgs, files = m.get('images') or [], m.get('files') or []
    if imgs or files:
        extra.append('Anh gửi kèm %d ảnh, %d tệp (tải về bằng: %s; ảnh từng cái: %s).' % (
            len(imgs), len(files), m.get('_tai_het', ''), '; '.join(i.get('tai_ve', '') for i in m.get('_anh', [])[:6])))
    head = ('[Chat nội bộ trên bảng Đội Quân AI. Chủ nhắn riêng cho bạn. Trả lời ngay, ngắn gọn, tiếng Việt, xưng em gọi anh. '
            'Việc nhỏ thì làm luôn. Việc lớn nhiều bước, cần duyệt, đăng bài, nhắn khách, tiêu tiền thì nói kế hoạch ngắn và mời anh bật nút "Giao thành việc" rồi gửi lại.]')
    return head + '\n\n' + t + ('\n\n' + '\n'.join(extra) if extra else '')


def _stream(url, token, form, timeout=600):
    data = urllib.parse.urlencode(form).encode('utf-8')
    req = urllib.request.Request(url.rstrip('/') + '/chat/stream', data=data, method='POST', headers={
        'Authorization': 'Bearer ' + token, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/event-stream',
        'User-Agent': 'doi-quan-bang/1'})
    last = None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode('utf-8', 'replace').strip()
            if not line.startswith('data:'):
                continue
            try:
                g = json.loads(line[5:].strip())
            except Exception:
                continue
            if g.get('type') == 'response':
                last = g
            elif g.get('type') == 'error':
                raise RuntimeError(str(g.get('content') or 'lỗi')[:300])
    if not last:
        raise RuntimeError('TISA BOT không trả lời')
    return last


def hoi(ma, text, brain, url, token, log=print):
    """Một lượt hỏi nhân sự `ma`. Trả (câu trả lời, giây)."""
    slug = agent_slug(brain, ma)
    with LOCK:
        ph = _phien_doc()
    key = '%s|%s' % (brain, slug or ma)
    form = {'message': text, 'brain': brain if slug else '', 'agent': slug, 'session': ph.get(key, ''), 'host': 'bang-doi-quan'}
    t0 = time.time()
    try:
        g = _stream(url, token, form)
    except urllib.error.HTTPError as e:
        if e.code == 400 and form['session']:   # phiên cũ không còn: mở phiên mới
            form['session'] = ''
            g = _stream(url, token, form)
        else:
            raise
    if g.get('session'):
        with LOCK:
            ph = _phien_doc()
            ph[key] = g['session']
            _phien_ghi(ph)
    return str(g.get('text') or '').strip(), time.time() - t0


def _claude_bin():
    try:
        b = json.loads((Path(__file__).resolve().parents[2] / 'server' / 'bin_paths.json').read_text(encoding='utf-8')).get('claude')
        if b and Path(b).exists():
            return b
    except Exception:
        pass
    import shutil
    return shutil.which('claude') or ''


def _agent_md(brain, slug):
    try:
        t = (Path(brain) / 'agents' / (slug + '.md')).read_text(encoding='utf-8')
    except Exception:
        return '', ''
    model = ''
    if t.startswith('---'):
        head, _, body = t[3:].partition('\n---')
        for line in head.splitlines():
            if line.strip().startswith('model:'):
                model = line.split(':', 1)[1].strip().strip('"\'')
        t = body
    return t.strip()[:12000], model


def _alias(model):
    m = (model or '').lower()
    for a in ('haiku', 'sonnet', 'opus'):
        if a in m:
            return a
    return 'opus'


def hoi_cli(ma, m, brain, log=print):
    """Không cần token: gọi thẳng Claude trên máy (cùng tài khoản TISA BOT đang dùng), đóng vai đúng nhân sự, giữ phiên riêng."""
    exe = _claude_bin()
    if not exe:
        raise RuntimeError('không thấy lệnh claude trên máy')
    slug = agent_slug(brain, ma)
    body, model = _agent_md(brain, slug) if slug else ('', '')
    nguoi, chu = m.get('nguoi') or {}, m.get('chu') or {}
    sysp = ((body or 'Bạn là %s trong Đội Quân AI.' % (nguoi.get('ten') or ma)) +
            '\n\nBạn đang chat riêng với chủ (%s) trong Chat nội bộ của bảng Đội Quân AI. Trả lời ngay, ngắn gọn, tiếng Việt, xưng em gọi anh. '
            'Anh không rành kỹ thuật: tránh từ chuyên môn, bước nào thì đánh số. Được đọc bộ não (thư mục hiện tại) khi cần số liệu, quy tắc, giá; không bịa. '
            'Việc lớn nhiều bước, cần duyệt, đăng bài, nhắn khách, tiêu tiền: nói kế hoạch ngắn và mời anh bật nút "Giao thành việc" rồi gửi lại. '
            'Không nêu giá, giảm giá, số lượng còn lại nếu chưa có trong bộ não. Không dùng dấu gạch ngang dài.' % (chu.get('ten') or 'chủ'))
    mdl = str(m.get('model') or 'auto')
    if mdl not in ('haiku', 'sonnet', 'opus'):   # Tự động: câu ngắn không kèm tệp thì Sonnet cho rẻ, còn lại theo mô hình của nhân sự
        mdl = 'sonnet' if (len(str(m.get('text') or '')) <= 280 and not m.get('images') and not m.get('files')) else _alias(model)
    eff = str(m.get('effort') or 'medium')
    if eff not in ('low', 'medium', 'high'):
        eff = 'medium'
    key = 'cli|%s|%s' % (brain, slug or ma)
    with LOCK:
        ph = _phien_doc()
    sid = ph.get(key, '')
    import subprocess
    def run(resume):
        cmd = [exe, '-p', _message(m), '--model', mdl, '--effort', eff, '--output-format', 'json', '--append-system-prompt', sysp,
               '--allowedTools', 'Read', 'Grep', 'Glob']
        if resume:
            cmd += ['--resume', resume]
        env = dict(os.environ, PATH=os.path.dirname(exe) + os.pathsep + os.environ.get('PATH', '/usr/bin:/bin'))
        r = subprocess.run(cmd, cwd=brain if Path(brain).is_dir() else None, capture_output=True, text=True, timeout=300, env=env)
        out = (r.stdout or '').strip()
        d = json.loads(out[out.find('{'):]) if '{' in out else {}
        if r.returncode != 0 or d.get('is_error') or not d.get('result'):
            raise RuntimeError((d.get('result') or r.stderr or out or 'claude lỗi')[:300])
        return d
    t0 = time.time()
    try:
        d = run(sid)
    except Exception:
        if not sid:
            raise
        d = run('')
    if d.get('session_id'):
        with LOCK:
            ph = _phien_doc()
            ph[key] = d['session_id']
            _phien_ghi(ph)
    log('Chat nhanh: %s dùng %s, nghĩ %s' % (ma, mdl, eff))
    return str(d.get('result') or '').strip(), time.time() - t0


def nhan(m, board, C, log, fallback, bang_path, brain):
    """Cầu nối gọi khi có tin chat. True = đã nhận theo đường nhanh."""
    CHAT_LUC[0] = time.time()
    token = _env().get('TISA_API_TOKEN') or C.get('TISA_API_TOKEN')
    if not brain or (not token and not _claude_bin()):
        return False
    board('POST', '/api/v1/tin/%s/ack' % m['id'], {})
    m = dict(m)
    m['_tai_het'] = 'python3 "%s" tai-het - "<thư mục>" --msg %s' % (bang_path, m['id'])
    m['_anh'] = [{'tai_ve': 'python3 "%s" tai %s <đường dẫn>' % (bang_path, i.get('id'))} for i in (m.get('images') or [])]
    ma = m.get('to') or 'tam'

    def chay():
        k = KHOA.setdefault(ma, threading.Lock())
        with k:
            try:
                if token:
                    text, giay = hoi(ma, _message(m), brain, C['TISA_URL'], token, log)
                else:
                    text, giay = hoi_cli(ma, m, brain, log)
                if not text:
                    raise RuntimeError('câu trả lời rỗng')
                board('POST', '/api/v1/tin/tra-loi', {'replyTo': m['id'], 'from': ma, 'text': text[:8000]})
                log('Chat nhanh: %s trả lời trong %.1f giây' % (ma, giay))
            except Exception as e:
                log('Chat nhanh lỗi (%s), chuyển đường thường: %s' % (ma, e))
                try:
                    fallback(m)
                except Exception as e2:
                    log('Đường thường cũng lỗi: %s' % e2)
    threading.Thread(target=chay, daemon=True).start()
    return True


def _main():
    import getpass
    a = sys.argv[1:]
    if a[:1] == ['dat-khoa']:
        print('Dán token TISA BOT (bắt đầu bằng jvs_), bấm Enter. Token không hiện trên màn hình.')
        tok = getpass.getpass('Token: ').strip()
        if not tok.startswith('jvs_') or len(tok) < 20:
            sys.exit('Token không đúng dạng (phải bắt đầu bằng jvs_), chưa lưu.')
        lines = []
        try:
            lines = [l for l in ENV.read_text(encoding='utf-8').splitlines() if not l.startswith('TISA_API_TOKEN=')]
        except FileNotFoundError:
            ENV.parent.mkdir(parents=True, exist_ok=True)
        lines.append('TISA_API_TOKEN=' + tok)
        ENV.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        os.chmod(ENV, 0o600)
        print('Đã lưu. Thử hỏi Tâm...')
        a = ['thu', 'tam', 'Em trả lời đúng một câu: chat nhanh đã chạy.']
    if a[:1] == ['thu'] and len(a) >= 3:
        c = _env()
        brain = c.get('CHAT_BRAIN') or str(Path(__file__).resolve().parents[2] / 'brains' / 'Brain Default')
        text, giay = hoi(a[1], _message({'text': a[2]}), brain, c.get('TISA_URL', 'http://127.0.0.1:7777'), c.get('TISA_API_TOKEN', ''))
        print('%s (%.1f giây): %s' % (a[1], giay, text[:500]))
        return
    print(__doc__)


if __name__ == '__main__':
    _main()
