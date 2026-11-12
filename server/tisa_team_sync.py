"""tisa_team_sync.py - giữ đội hình Đội Quân AI và cộng sự TISA BOT luôn khớp nhau.

Đội Quân AI chỉ là giao diện quản lý, nguồn gốc vận hành là TISA BOT: nhân sự thật nằm ở <brain>/agents/*.md và
<brain>/skills/. Mỗi vòng (10 giây):
  bảng -> TISA BOT: thêm, sửa, tắt, xoá nhân sự và phòng ban thì tạo/sửa hồ sơ, skill vai trò, thành viên nhóm.
  TISA BOT -> bảng: thêm, sửa, xoá cộng sự, đổi skill thì bảng hiện đúng như vậy.
Hai bên cùng sửa một người trong một vòng thì TISA BOT thắng. Xoá trên bảng chỉ chuyển hồ sơ vào agents/_da-xoa/, không mất hẳn.
Chỉ đồng bộ phần đội hình, không đụng vào lời dặn riêng học viên viết trong hồ sơ.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import subprocess
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

HE_THONG = {"tisa-core"}    # hồ sơ do TISA BOT tự tạo để nhận báo cáo, lõi không cho vào nhóm nên không đồng bộ lên bảng
BAT_DAU = "<!-- dong-bo-doi-quan:bat-dau -->"
KET_THUC = "<!-- dong-bo-doi-quan:ket-thuc -->"
PHONG_CONG_SU = {"id": "x-cong-su", "name": "Phòng Cộng Sự", "color": "#3B82F6", "desc": "Cộng sự tạo bên TISA BOT"}
MAC_DINH_MODEL = "claude-sonnet-5-5"
TEAM_NAME = "Đội Quân AI"
TEAM_RULES = """## Luật chung của Đội Quân AI
- Giao việc là làm thật: dùng công cụ đang có để ra sản phẩm thật; tự quyết chi tiết nhỏ và ghi rõ đã quyết gì.
- Trước khi làm, đọc bộ não lấy dữ liệu mới nhất: `00-DOC-TRUOC.md`, `muc-luc.md`, `01-ho-so/`, kết quả cũ cùng chủ đề.
- Trung thực: chỉ báo xong khi có bằng chứng (file, link, ảnh). Chưa làm được thì nói rõ đang chờ gì. Không bịa số liệu, nguồn, kết quả khách hàng.
- Đăng bài công khai, nhắn khách, tiêu tiền: chỉ chuẩn bị, chờ chủ duyệt.
- Khóa, mật khẩu, mã bí mật không bao giờ ghi vào bộ não, kết quả hay tin nhắn.
- Lưu kết quả vào đúng thư mục việc được giao (`05 - Van Phong AI/03 - Ket qua/...`), mỗi nhân sự một tệp.
- Mỗi người chỉ trả kết quả của đúng phần việc mình được giao. Không chép lại, không tóm tắt lại, không lặp kết quả của người khác. Cần dựa vào phần của người trước thì ghi một câu "dùng bản của <tên>", không dán lại nội dung.
- Kết quả viết gọn một lần: đã làm gì, sản phẩm (nội dung hoặc đường dẫn tệp), cần chủ quyết gì. Tiến độ đang làm báo bằng lệnh tiến độ, không nhét vào kết quả.
- Kết thúc bằng một khối BÀN GIAO ngắn (tối đa 3 dòng): sản phẩm nằm ở đâu, chuyển cho ai, cần chủ quyết gì. Không nhắc lại nội dung vừa nộp.
"""


def render_block(a):
    """Phần trách nhiệm trong hồ sơ cộng sự, viết ra y hệt lúc đóng gói để không tạo khác biệt giả."""
    li = "\n".join("- " + str(x) for x in a.get("jobs") or [])
    return (BAT_DAU + "\n## Trách nhiệm (đồng bộ với Đội Quân AI)\n" + (li + "\n" if li else "")
            + "\n- Nhận từ: %s\n- Bàn giao: %s\n- Chuyển cho: %s\n" % (a.get("input", ""), a.get("output", ""), a.get("to", "")) + KET_THUC)


def doc_block(body):
    """Đọc ngược render_block: phần trách nhiệm đang ghi trong hồ sơ."""
    m = re.search(re.escape(BAT_DAU) + r"(.*?)" + re.escape(KET_THUC), body, re.S)
    if not m:
        return {}
    ra = {"jobs": [], "input": "", "output": "", "to": ""}
    nhan = {"- Nhận từ:": "input", "- Bàn giao:": "output", "- Chuyển cho:": "to"}
    for d in m.group(1).splitlines():
        khoa = next((k for k in nhan if d.startswith(k)), None)
        if khoa:
            ra[nhan[khoa]] = d[len(khoa):].strip()
        elif d.startswith("- "):
            ra["jobs"].append(d[2:])
    return ra


def role_of(a):
    jobs = a.get("jobs") or []
    return "%s: %s" % (a.get("title", ""), jobs[0]) if jobs else str(a.get("title", ""))


def _ascii(text):
    s = unicodedata.normalize("NFD", str(text)).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _hash(o):
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------- Tâm Tổng Quản xếp phòng cho cộng sự mới
# Từ khoá (không dấu) nói công việc nào thuộc phòng nào. Chức danh tính nặng gấp 3 so với một việc phụ trách.
TU_KHOA_PHONG = {
    "dieu-hanh": ["dieu hanh", "dieu phoi", "tong quan", "giam doc", "quan ly du an", "ke hoach", "thu ky", "tro ly", "van hanh", "chia viec"],
    "nghien-cuu": ["nghien cuu", "thi truong", "doi thu", "khao sat", "insight", "xu huong", "trend", "seo", "tu khoa", "chan dung khach"],
    "sang-tao": ["content", "viet bai", "noi dung", "copywriter", "thiet ke", "hinh anh", "video", "dung phim", "kich ban", "sang tao",
                 "banner", "bien tap", "caption", "anh quang cao", "dao dien", "nhiep anh", "ebook"],
    "kenh": ["kenh", "cong dong", "fanpage", "group", "dang bai", "social", "tiktok", "youtube", "zalo oa", "community", "lich dang", "da kenh"],
    "quang-cao": ["quang cao", "ads", "facebook ads", "google ads", "chien dich", "ngan sach", "remarketing", "chay ads", "performance"],
    "so-lieu": ["so lieu", "bao cao", "phan tich", "dashboard", "thong ke", "kpi", "data", "excel", "bang tinh"],
    "tu-van": ["tu van", "cham soc", "ban hang", "sale", "khach hang", "inbox", "chot don", "telesale", "cskh", "lead", "crm", "xu ly tu choi"],
    "huan-luyen": ["huan luyen", "dao tao", "danh gia", "cham diem", "coach", "huong dan nhan su"],
    "tai-chinh": ["tai chinh", "ke toan", "chi phi", "doanh thu", "hoa don", "thue", "luong", "loi nhuan", "thu chi"],
    "kiem-duyet": ["kiem duyet", "kiem tra noi dung", "phap ly", "thuong hieu", "tuan thu", "soat loi", "duyet bai"],
    "hoc-vu": ["san pham", "dich vu", "hoc vu", "khoa hoc", "tai lieu", "faq", "cau hoi thuong gap", "giao trinh", "giang vien", "bao gia"],
    "cong-nghe": ["cong nghe", "ky thuat", "tu dong", "lap trinh", "web", "landing page", "code", "api", "tich hop", "he thong", "automation", "n8n", "pixel", "website"],
}


def _chu(text):
    """Chữ không dấu, cách nhau bằng 1 dấu cách, bọc dấu cách hai đầu để so từ trọn vẹn."""
    return " " + _ascii(text).replace("-", " ") + " "


def de_xuat_phong(a, team):
    """(mã phòng, lý do) hợp công việc của cộng sự nhất, hoặc ("", "") khi chưa đủ căn cứ.
    a: tên, chức danh (title hoặc role), việc phụ trách (jobs). team: kit["team"] (có phòng gốc và phòng tự tạo)."""
    ten = _chu(a.get("name") or "")
    chuc = _chu(str(a.get("title") or "").split(":")[0])
    viec = [_chu(j) for j in (a.get("jobs") or [])] + [_chu(a.get("output") or ""), _chu(a.get("input") or "")]
    rn = team.get("roomNames") or {}
    phong = [r for r in (team.get("rooms") or []) + (team.get("roomsX") or []) if isinstance(r, dict) and r.get("id") and r["id"] != PHONG_CONG_SU["id"]]
    tot, diem_tot, lydo = "", 0, ""
    for r in phong:
        tk = list(TU_KHOA_PHONG.get(r["id"], []))
        # Phòng chủ tự tạo: lấy chính các từ trong tên và mô tả phòng làm từ khoá.
        if r["id"] not in TU_KHOA_PHONG:
            moi = _ascii(" ".join([str(rn.get(r["id"]) or r.get("name") or ""), str(r.get("desc") or "")])).replace("-", " ").split()
            tk = [w for w in dict.fromkeys(moi) if len(w) >= 3 and w not in ("phong", "cua", "cho", "va", "nhan", "su", "doi")]
        diem, thay = 0, []
        for k in tk:
            m = " " + k + " "
            if m in chuc:
                diem += 3
                thay.append(k)
            if m in ten:
                diem += 1
            n = sum(1 for v in viec if m in v)
            if n:
                diem += min(n, 3)
                thay.append(k)
        if diem > diem_tot:
            tot, diem_tot, lydo = r["id"], diem, ", ".join(dict.fromkeys(thay))[:80]
    if diem_tot >= 2:
        return tot, lydo
    return "", ""


# ---------------------------------------------------------------- hồ sơ cộng sự trên đĩa
def read_agent(path):
    import yaml
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    meta = {}
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
    return {"meta": meta if isinstance(meta, dict) else {}, "text": text, "body": text[m.end():] if m else text}


def write_agent(path, cur, a, room, skills):
    import yaml
    meta = dict(cur["meta"])
    meta.update(name=a["name"], role=role_of(a), skills=skills)
    meta["tags"] = list(dict.fromkeys([TEAM_NAME, room] + [t for t in meta.get("tags") or [] if t != TEAM_NAME and t != room and t in cur.get("giu_tag", [])]))
    block = render_block(a)
    body = cur["body"]
    if BAT_DAU in body and KET_THUC in body:
        new_body = re.sub(re.escape(BAT_DAU) + r".*?" + re.escape(KET_THUC), lambda _: block, body, count=1, flags=re.S)
    else:
        new_body = block + "\n\n" + body
    # Không có gì khác thì không ghi, để tệp đóng gói giữ nguyên.
    if meta == cur["meta"] and new_body == body:
        return
    path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip() + "\n---\n" + new_body, encoding="utf-8")


def new_agent_file(path, a, room, skills):
    meta = {"type": "agent", "slug": path.stem, "model": MAC_DINH_MODEL, "model_provider": "anthropic-cli", "updated": time.strftime("%Y-%m-%d")}
    body = ("Bạn là %s, %s, thuộc %s trong Đội Quân AI, chạy trên TISA BOT.\n\n"
            "Kết quả tốt: sản phẩm thật dùng được ngay, có nguồn khi có số liệu, đúng luật bên dưới.\n\n## Cách làm\n"
            "1. Đọc kỹ việc được giao và skill `%s`.\n2. Đọc bộ não lấy dữ liệu mới nhất.\n3. Làm thật, tự soát; nội dung công khai chuyển Liêm Kiểm Duyệt soát.\n4. Bàn giao.\n\n%s"
            % (a["name"], str(a.get("title", "")).lower(), room, path.stem, TEAM_RULES))
    write_agent(path, {"meta": meta, "body": body, "text": ""}, a, room, skills)


def new_skill_file(folder, a, room):
    f = folder / "SKILL.md"
    if f.exists():
        return
    folder.mkdir(parents=True, exist_ok=True)
    li = "\n".join("- " + str(x) for x in a.get("jobs") or [])
    f.write_text("---\nname: %s\ndescription: %s\ngroup: %s\n---\n# %s - %s\n\nĐóng vai %s, %s.\n\n## Việc phụ trách\n%s\n\n## Đầu vào, đầu ra\n- Nhận: %s\n- Bàn giao: %s\n- Chuyển cho: %s\n\n%s" % (
        json.dumps(a["name"], ensure_ascii=False), json.dumps("%s trong Đội Quân AI." % a.get("title", ""), ensure_ascii=False), json.dumps(room, ensure_ascii=False),
        a["name"], a.get("title", ""), a["name"], room, li, a.get("input", ""), a.get("output", ""), a.get("to", ""), TEAM_RULES), encoding="utf-8")


def skill_info(skills_dir, name):
    try:
        text = (skills_dir / name / "SKILL.md").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', text, re.M)
    return re.sub(r"^Gọi bằng /[\w-]+\.\s*", "", (m.group(1) if m else "").replace('\\"', '"'))[:200]


# ---------------------------------------------------------------- đội hình trên bảng
def board_roster(kit):
    T = kit.get("team") or {}
    ed, off, rn = T.get("edits") or {}, T.get("off") or [], T.get("roomNames") or {}
    rooms = {r["id"]: rn.get(r["id"]) or r.get("name") or r["id"] for r in (T.get("rooms") or []) + (T.get("roomsX") or []) if isinstance(r, dict) and r.get("id")}
    out = {}
    for a in T.get("agents") or []:
        if not a.get("id") or a["id"] == "chu":
            continue
        e = ed.get(a["id"]) or {}
        o = dict(a)
        for k in ("name", "title", "room"):
            if e.get(k):
                o[k] = str(e[k])
        o.update(slug="dq-" + str(a.get("skill") or a["id"]), off=a["id"] != "tam" and a["id"] in off, custom=False)
        out[a["id"]] = o
    for a in T.get("custom") or []:
        if not (isinstance(a, dict) and re.match(r"^x-[\w-]{2,40}$", str(a.get("id"))) and str(a.get("name") or "").strip()):
            continue
        sk = str(a.get("skill") or "")
        # `skill` giữ đúng tên hồ sơ bên TISA BOT (cộng sự tạo bên đó có thể không có tiền tố dq-).
        slug = sk if re.match(r"^[\w-]+$", sk) and sk != "tu-chon" else "dq-" + (_ascii(a["name"]) or _ascii(a["id"][2:]))
        out[a["id"]] = dict(a, slug=slug, off=a["id"] in off, custom=True)
    for a in out.values():
        a["room_name"] = rooms.get(a.get("room")) or next(iter(rooms.values()), "")
    return out


def sig_of(a):
    return _hash({k: a.get(k) for k in ("name", "title", "room_name", "jobs", "input", "output", "to", "off")})


def file_sig(cur):
    m = cur["meta"]
    return _hash({"name": m.get("name"), "role": m.get("role"), "skills": m.get("skills") or []})


# ---------------------------------------------------------------- một vòng đồng bộ
class Sync:
    def __init__(self, brain, data_dir, env_path, bot_url, session=None, log=print, chi_tu_nay=False, ket_noi=True):
        # chi_tu_nay: bảng đặt ngoài (Cloudflare) đã có người từ trước; hồ sơ có sẵn lúc bật đồng bộ lần đầu thì để yên, chỉ cộng sự tạo SAU đó mới lên bảng.
        # ket_noi: có báo danh sách kết nối và kho tư liệu lên bảng hay không (bảng đặt ngoài: không, chỉ đồng bộ đội hình).
        self.chi_tu_nay, self.ket_noi = chi_tu_nay, ket_noi
        self.brain, self.env_path, self.bot, self.session, self.log = Path(brain), Path(env_path), bot_url.rstrip("/"), session, log
        self.agents, self.skills = self.brain / "agents", self.brain / "skills"
        self.state_path = Path(data_dir) / "team-sync.json"
        self.dau_ket_noi = None
        self._bo_nhom = set()

    def cfg(self):
        out = {}
        try:
            for line in self.env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip()
        except OSError:
            pass
        return out

    def board(self, method, path, body=None):
        c = self.cfg()
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        req = urllib.request.Request(c["BOARD_URL"].rstrip("/") + path, data=data, method=method, headers={
            "Authorization": "Bearer " + c["BOARD_TOKEN"], "Content-Type": "application/json", "User-Agent": "tisa-team-sync/1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8") or "{}")

    def bot_call(self, method, path, body=None):
        token = self.session() if self.session else ""
        headers = {"Content-Type": "application/json", "User-Agent": "tisa-team-sync/1", "Origin": self.bot}
        if token:
            headers["Cookie"] = "tisa_session=" + token
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        with urllib.request.urlopen(urllib.request.Request(self.bot + path, data=data, method=method, headers=headers), timeout=30) as r:
            return json.loads(r.read().decode("utf-8") or "{}")

    def load_state(self):
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {"agents": {}, "members": []}

    def run_once(self):
        cfg = self.cfg()
        if not (cfg.get("BOARD_URL") and cfg.get("BOARD_TOKEN")) or not self.agents.is_dir():
            return False
        try:
            kit = self.board("GET", "/api/db/settings/kit")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            raise
        kit.pop("id", None)
        team = kit.setdefault("team", {})
        roster = board_roster(kit)
        state = self.load_state()
        known = state["agents"]
        by_slug = {a["slug"]: ma for ma, a in roster.items()}
        files = {p.stem: p for p in self.agents.glob("*.md") if p.stem not in HE_THONG}   # trợ lý hệ thống của TISA BOT không phải nhân sự của đội
        kit_dirty = False
        if self.chi_tu_nay and not state.get("da_chup"):
            # Chụp danh sách hồ sơ đang có (chưa thuộc bảng) làm mốc: các hồ sơ này không bị đẩy lên bảng.
            state["bo_qua"] = sorted(s for s in files if s not in by_slug)
            state["da_chup"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.save_state(state)
            self.log("Đồng bộ đội hình: lấy mốc %d hồ sơ có sẵn, chỉ cộng sự tạo từ nay mới lên bảng" % len(state["bo_qua"]))
        bo_qua = set(state.get("bo_qua") or [])

        # Một bộ não chung: bảng luôn trỏ về bộ não của TISA BOT, kể cả khi thư mục cài bị chuyển chỗ.
        chung = kit.setdefault("brain", {})
        if chung.get("abs") != self.brain.as_posix() or chung.get("path") != self.brain.as_posix():
            chung.update(abs=self.brain.as_posix(), path=self.brain.as_posix())
            kit_dirty = True

        def custom_list():
            return [x for x in team.get("custom") or [] if isinstance(x, dict)]

        # 1. Cộng sự mới, đã xoá hoặc đã sửa bên TISA BOT -> bảng (TISA BOT là nguồn gốc nên xét trước).
        # Nhân sự vừa thêm trên bảng chưa có `skill`: ghi lại tên hồ sơ để các vòng sau luôn khớp.
        for x in custom_list():
            if x.get("id") in roster and x.get("skill") != roster[x["id"]]["slug"]:
                x["skill"] = roster[x["id"]]["slug"]
                kit_dirty = True
        da_biet = {r.get("slug") for r in known.values()}
        for slug, path in files.items():
            if slug in by_slug or slug in da_biet or slug in bo_qua:     # da_biet: vừa xoá trên bảng, bước 3 cất hồ sơ
                continue
            cur = read_agent(path)
            ma = "x-" + _ascii(re.sub(r"^dq-", "", slug))[:40]
            rx = [r for r in team.get("roomsX") or [] if isinstance(r, dict)]
            # Bản nhân bản mang theo trách nhiệm và về đúng phòng của bản gốc (ghi ở hồ sơ).
            khoi = doc_block(cur["body"])
            ten_phong = {(team.get("roomNames") or {}).get(r.get("id")) or r.get("name"): r.get("id") for r in (team.get("rooms") or []) + rx if isinstance(r, dict)}
            phong = next((ten_phong[t] for t in cur["meta"].get("tags") or [] if t in ten_phong), None)
            tam_xep = None
            if not phong:
                # Tâm Tổng Quản xếp phòng theo công việc; chưa đủ căn cứ thì vào Phòng Cộng Sự.
                moi = {"name": str(cur["meta"].get("name") or slug), "title": str(cur["meta"].get("role") or ""), "jobs": khoi.get("jobs", []),
                       "input": khoi.get("input", ""), "output": khoi.get("output", "")}
                phong, ly_do = de_xuat_phong(moi, team)
                if phong:
                    tam_xep = ly_do
                else:
                    phong = PHONG_CONG_SU["id"]
                    if not any(r.get("id") == phong for r in rx):
                        team["roomsX"] = rx + [dict(PHONG_CONG_SU, ngay=time.strftime("%Y-%m-%d"))]
            team["custom"] = [x for x in custom_list() if x.get("id") != ma] + [{
                "id": ma, "name": str(cur["meta"].get("name") or slug), "title": str(cur["meta"].get("role") or "").split(":")[0][:120],
                "room": phong, "gender": "f", "jobs": khoi.get("jobs", []), "skill": slug, "to": khoi.get("to", ""), "input": khoi.get("input", ""), "output": khoi.get("output", "")}]
            kit_dirty = True
            self.log("TISA BOT -> bảng: thêm %s" % slug)
            if tam_xep is not None:
                self.ghi_tam_xep(team, state, ma, phong, tam_xep)
        # Cộng sự đang nằm ở Phòng Cộng Sự mà Tâm chưa xét: xếp vào phòng hợp việc, một lần. Chủ chuyển phòng tay thì không đụng nữa.
        da_xet = state.setdefault("tam_xep", [])
        for x in custom_list():
            if x.get("id") in da_xet or x.get("room") != PHONG_CONG_SU["id"]:
                continue
            da_xet.append(x["id"])
            phong, ly_do = de_xuat_phong(x, team)
            if phong and phong != x.get("room"):
                x["room"] = phong
                self.ghi_tam_xep(team, state, x["id"], phong, ly_do)
                kit_dirty = True
                self.log("Tâm Tổng Quản xếp %s vào phòng %s (%s)" % (x.get("name"), phong, ly_do))
        for ma, a in list(roster.items()):
            rec = known.get(ma)
            if a["slug"] not in files and rec and rec.get("co_tep"):
                # Có hồ sơ lúc trước mà nay mất: học viên đã xoá cộng sự bên TISA BOT.
                if a["custom"]:
                    team["custom"] = [x for x in custom_list() if x.get("id") != ma]
                else:
                    team["off"] = sorted(set(team.get("off") or []) | {ma})
                known.pop(ma, None)
                kit_dirty = True
                self.log("TISA BOT -> bảng: bỏ %s" % a["slug"])
            elif a["slug"] in files and rec and rec.get("file_sig") and file_sig(read_agent(files[a["slug"]])) != rec["file_sig"]:
                m = read_agent(files[a["slug"]])["meta"]
                name, title = str(m.get("name") or a["name"]), str(m.get("role") or "").split(":")[0] or a.get("title", "")
                if (name, title) != (a["name"], a.get("title")):
                    if a["custom"]:
                        team["custom"] = [dict(x, name=name, title=title) if x.get("id") == ma else x for x in custom_list()]
                    else:
                        ed = team.setdefault("edits", {})
                        ed[ma] = dict(ed.get(ma) or {}, name=name, title=title)
                    kit_dirty = True
                    self.log("TISA BOT -> bảng: sửa %s" % a["slug"])
        if kit_dirty:
            self.board("PUT", "/api/db/settings/kit", kit)
            roster = board_roster(kit)

        # 2. Bảng -> TISA BOT: tạo và sửa hồ sơ, skill vai trò.
        try:
            reg = self.board("GET", "/api/db/settings/skills")
        except urllib.error.HTTPError:
            reg = {}
        reg.pop("id", None)
        new_reg, reg_dirty = dict(reg), False
        for ma, a in roster.items():
            path = self.agents / (a["slug"] + ".md")
            if not path.exists():
                if a["off"]:
                    continue
                base = [a["slug"], "dq-bao-cao-bang"]
                new_skill_file(self.skills / a["slug"], a, a["room_name"])
                new_agent_file(path, a, a["room_name"], base)
                self.log("Bảng -> TISA BOT: tạo %s" % a["slug"])
            cur = read_agent(path)
            skills = list(cur["meta"].get("skills") or [])
            # Skill đăng ký trên bảng (bang.py ky-nang) mà chưa có trong hồ sơ thì thêm vào hồ sơ.
            for it in reg.get(ma) or []:
                folder = Path(str(it.get("duong_dan") or "")).name
                if it.get("nguon") != "TISA BOT" and folder and (self.skills / folder).is_dir() and folder not in skills:
                    skills.append(folder)
            rec = known.get(ma) or {}
            sb = sig_of(a)
            if rec.get("board_sig") != sb or skills != (cur["meta"].get("skills") or []):
                write_agent(path, cur, a, a["room_name"], skills)
                cur = read_agent(path)
            # Trang Đội ngũ hiện đúng bộ skill của cộng sự.
            want = [{"ten": s, "mo_ta": skill_info(self.skills, s), "duong_dan": "skills/" + s, "nguon": "TISA BOT"} for s in skills if s != "dq-bao-cao-bang"][:30]
            if [(x.get("ten"), x.get("mo_ta")) for x in reg.get(ma) or []] != [(x["ten"], x["mo_ta"]) for x in want]:
                new_reg[ma] = [dict(x, ngay=time.strftime("%Y-%m-%d")) for x in want]
                reg_dirty = True
            known[ma] = {"slug": a["slug"], "board_sig": sb, "file_sig": file_sig(cur), "co_tep": True, "custom": a["custom"]}
        for ma in [m for m in new_reg if m not in roster]:
            new_reg.pop(ma)
            reg_dirty = True
        if reg_dirty:
            self.board("PUT", "/api/db/settings/skills", new_reg)

        # 3. Nhân sự đã xoá hẳn trên bảng: cất hồ sơ, không xoá mất.
        for ma in [m for m in known if m not in roster]:
            rec = known.pop(ma)
            p = self.agents / (rec.get("slug", "") + ".md")
            if p.exists():
                dest = self.agents / "_da-xoa"
                dest.mkdir(exist_ok=True)
                shutil.move(str(p), str(dest / (p.stem + "-" + time.strftime("%Y%m%d%H%M%S") + ".md")))
                self.log("Bảng -> TISA BOT: cất hồ sơ %s" % p.stem)

        # Ghi trước bước 4: nếu sổ không kịp ghi, cộng sự xoá ngay sau đó sẽ bị coi là nhân sự mới trên bảng và tạo lại.
        state["agents"] = known
        self.save_state(state)

        if self.ket_noi:
            self.sync_ket_noi(cfg)

        # 4. Thành viên nhóm khớp đội hình đang bật. Chỉ gọi TISA BOT khi có khác biệt.
        active = sorted(a["slug"] for a in roster.values() if not a["off"] and (self.agents / (a["slug"] + ".md")).exists())
        if active != state.get("members"):
            try:
                if self.sync_members(active):
                    state["members"] = active
                    self.save_state(state)
            except urllib.error.HTTPError as e:     # cộng sự vừa tạo chưa vào danh sách của TISA BOT: vòng sau thử lại
                self.log("Nhóm: chưa khớp được, vòng sau thử lại: %s %s" % (e, (e.read() or b"")[:200].decode("utf-8", "replace")))
        return True

    def ghi_tam_xep(self, team, state, ma, phong, ly_do):
        """Ghi để bảng hiện được "Tâm Tổng Quản đã xếp vào phòng ..." và để không xét lại cộng sự này."""
        if ma not in state.setdefault("tam_xep", []):
            state["tam_xep"].append(ma)
        team.setdefault("tamXep", {})[ma] = {"phong": phong, "ly_do": ly_do, "ngay": time.strftime("%Y-%m-%d")}

    def sync_ket_noi(self, cfg):
        """Cài hay gỡ MCP, API, kênh, gói bên TISA BOT thì mục Kết nối trên bảng đổi theo ngay."""
        d = Path(cfg.get("TISA_DIR") or "")
        dau = []
        for ten in ("mcp_servers.json", "channel_accounts.json", "chatbots.json", "settings.json", "packs.json"):
            try:
                st = (d / ten).stat()
                dau.append((ten, st.st_mtime_ns, st.st_size))
            except OSError:
                dau.append((ten, 0, 0))
        if dau == self.dau_ket_noi:
            return
        r = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "suite" / "bridge" / "bang.py"), "dong-bo"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode == 0:
            self.dau_ket_noi = dau
        else:
            self.log("Kết nối: chưa báo được lên bảng: %s" % (r.stderr or r.stdout)[-300:])

    def save_state(self, state):
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=0), encoding="utf-8")

    def sync_members(self, active):
        team = next((t for t in self.bot_call("GET", "/teams?brain=brain").get("teams") or [] if t.get("name") == TEAM_NAME), None)
        if not team:
            return False    # setup_suite tạo nhóm trước, vòng sau làm tiếp
        detail = self.bot_call("GET", "/teams/%s?brain=brain" % team["team_id"])
        members = (detail.get("team") or detail).get("members") or detail.get("members") or []
        have = {str(m.get("slug") or m.get("agent_slug")): m for m in members}
        for slug in active:
            if slug not in have:
                try:
                    self.bot_call("POST", "/teams/%s/members?brain=brain" % team["team_id"], {"slug": slug})
                    self.log("Nhóm: thêm %s" % slug)
                except urllib.error.HTTPError as e:
                    if e.code != 400:
                        raise
                    # Lõi báo chưa có trợ lý này (hồ sơ vừa tạo hoặc loại không vào nhóm): bỏ qua người này, không chặn cả nhóm.
                    if slug not in self._bo_nhom:
                        self._bo_nhom.add(slug)
                        self.log("Nhóm: lõi chưa nhận %s, bỏ qua (%s)" % (slug, (e.read() or b"")[:120].decode("utf-8", "replace")))
        for slug, m in have.items():
            if slug not in active:
                self.bot_call("DELETE", "/teams/%s/members/%s?brain=brain" % (team["team_id"], m.get("agent_key")))
                self.log("Nhóm: bỏ %s" % slug)
        return True
