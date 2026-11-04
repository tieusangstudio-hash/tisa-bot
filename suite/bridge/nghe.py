#!/usr/bin/env python3
"""nghe.py - đội AI nghe video, ghi âm, link YouTube ra chữ để nạp bộ não.

  python3 nghe.py tep <video-hoac-ghi-am> <ra.txt>        chép lời một tệp (mp4, mov, mp3, m4a, wav...)
  python3 nghe.py youtube <link> <thu-muc-ra>             lấy tiêu đề, mô tả, phụ đề; không có phụ đề thì tải tiếng rồi nghe

Nghe bằng Whisper của Groq (khóa Groq đã có trong TISA BOT), không in, không chép khóa ra đâu.
Tệp dài tự cắt khúc 10 phút. Kết quả là văn bản thô: đội đọc rồi mới chắt lọc.
"""
import asyncio, json, os, subprocess, sys, tempfile
from pathlib import Path

SERVER = None
for p in (str(Path(__file__).resolve().parents[2] / 'server'),):
    d = Path(p).expanduser()
    if (d / 'stt.py').exists():
        SERVER = d
        break

# cần httpx của TISA BOT: chạy lại bằng python của TISA BOT nếu python đang dùng thiếu
try:
    import httpx  # noqa: F401
except ImportError:
    py = SERVER and (SERVER.parent / '.venv' / 'bin' / 'python3')
    if py and py.exists() and os.environ.get('NGHE_REEXEC') != '1':
        os.environ['NGHE_REEXEC'] = '1'
        os.execv(str(py), [str(py), __file__] + sys.argv[1:])
    sys.exit('LỖI: thiếu thư viện httpx, không thấy python của TISA BOT')

sys.path.insert(0, str(SERVER))
import stt  # noqa: E402

KHUC = 600  # giây mỗi khúc


def tool(name):
    for d in ('/opt/homebrew/bin', '/usr/local/bin', str(Path.home() / '.openclaw/runtime/openclaw-tools/bin')):
        p = Path(d) / name
        if p.exists():
            return str(p)
    return name


def groq_key():
    try:
        st = json.loads((SERVER / 'settings.json').read_text(encoding='utf-8'))
    except Exception:
        return ''
    return st.get('groq_api_key') or ''


def do_dai(f):
    try:
        r = subprocess.run([tool('ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                           capture_output=True, text=True, timeout=60)
        return float(r.stdout.strip() or 0)
    except Exception:
        return 0.0


def nghe_tep(f, ra):
    key = groq_key()
    if not key:
        sys.exit('LỖI: TISA BOT chưa có khóa Groq (Cài đặt > Models > Groq), chưa nghe được')
    f = Path(f).expanduser()
    tong = do_dai(f)
    out = []
    with tempfile.TemporaryDirectory() as td:
        n = max(1, int(tong // KHUC) + (1 if tong % KHUC else 0)) if tong else 1
        for i in range(n):
            k = Path(td) / ('k%03d.mp3' % i)
            cmd = [tool('ffmpeg'), '-v', 'error', '-y', '-ss', str(i * KHUC), '-t', str(KHUC), '-i', str(f), '-vn', '-ac', '1', '-ar', '16000', '-b:a', '48k', str(k)]
            subprocess.run(cmd, check=True, timeout=900)
            if not k.exists() or k.stat().st_size < 2000:
                continue
            r = asyncio.run(stt.groq_nghe(k.read_bytes(), k.name, key, ngon_ngu=None))
            mm = '%02d:%02d' % divmod(i * KHUC // 60, 60)
            if r.get('ok'):
                out.append('[%s] %s' % (mm, stt.loc_ao_giac(r.get('text', '')).strip()))
            else:
                out.append('[%s] (chưa nghe được khúc này: %s)' % (mm, r.get('ly_do')))
            print('Đã nghe khúc %d/%d' % (i + 1, n), flush=True)
    text = '\n\n'.join(out).strip()
    Path(ra).expanduser().parent.mkdir(parents=True, exist_ok=True)
    Path(ra).expanduser().write_text('# Lời trong %s\n\nĐộ dài: %d phút\n\n%s\n' % (f.name, round(tong / 60), text), encoding='utf-8')
    print(json.dumps({'ok': True, 'ra': str(Path(ra).expanduser()), 'phut': round(tong / 60), 'so_chu': len(text.split())}, ensure_ascii=False))


def youtube(url, thu_muc):
    d = Path(thu_muc).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    yt = tool('yt-dlp')
    info = {}
    try:
        r = subprocess.run([yt, '-J', '--no-playlist', url], capture_output=True, text=True, timeout=180)
        info = json.loads(r.stdout or '{}')
    except Exception:
        pass
    meta = {'tieu_de': info.get('title', ''), 'kenh': info.get('channel') or info.get('uploader', ''), 'ngay': info.get('upload_date', ''),
            'phut': round((info.get('duration') or 0) / 60), 'luot_xem': info.get('view_count'), 'link': info.get('webpage_url') or url,
            'mo_ta': (info.get('description') or '')[:4000]}
    subprocess.run([yt, '--no-playlist', '--skip-download', '--write-subs', '--write-auto-subs', '--sub-langs', 'vi.*,vi,en.*,en',
                    '--convert-subs', 'srt', '-o', str(d / 'phu-de.%(ext)s'), url], capture_output=True, text=True, timeout=300)
    subs = sorted(d.glob('phu-de*.srt'), key=lambda p: (0 if '.vi' in p.name else 1, p.name))
    loi = ''
    if subs:
        lines, last = [], ''
        for ln in subs[0].read_text(encoding='utf-8', errors='ignore').splitlines():
            ln = ln.strip()
            if not ln or ln.isdigit() or '-->' in ln or ln == last:
                continue
            lines.append(ln)
            last = ln
        loi = ' '.join(lines)
        nguon = 'phụ đề ' + subs[0].name
    else:
        subprocess.run([yt, '--no-playlist', '-x', '--audio-format', 'mp3', '-o', str(d / 'tieng.%(ext)s'), url],
                       capture_output=True, text=True, timeout=1800)
        a = d / 'tieng.mp3'
        if a.exists():
            nghe_tep(a, d / 'loi.txt')
            loi = (d / 'loi.txt').read_text(encoding='utf-8')
            nguon = 'nghe bằng Whisper'
        else:
            nguon = 'không lấy được phụ đề hay tiếng'
    (d / 'youtube.md').write_text('# %s\n\n- Kênh: %s\n- Ngày đăng: %s\n- Độ dài: %s phút\n- Link: %s\n- Lời lấy từ: %s\n\n## Mô tả\n\n%s\n\n## Lời trong video\n\n%s\n' % (
        meta['tieu_de'], meta['kenh'], meta['ngay'], meta['phut'], meta['link'], nguon, meta['mo_ta'], loi), encoding='utf-8')
    print(json.dumps(dict(meta, mo_ta=None, ra=str(d / 'youtube.md'), nguon_loi=nguon, so_chu=len(loi.split())), ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'tep':
        nghe_tep(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == 'youtube':
        youtube(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)
