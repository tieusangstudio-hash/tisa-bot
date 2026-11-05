"""tisa_nhan_ban.py - nhân bản một cộng sự thành nhân sự mới: cùng hướng dẫn, skill, model, đổi tên khác.

Hai bên cùng thấy: bản mới là một hồ sơ thật trong <brain>/agents, vòng đồng bộ đưa lên Đội Quân AI đúng phòng của bản gốc.
"""
import re
import time
from pathlib import Path

import yaml

from tisa_team_sync import BAT_DAU, KET_THUC, _ascii, read_agent

TEN_TOI_DA = 60


def _slug_trong(agents, ten):
    goc = _ascii(ten)[:37].strip("-")
    if len(goc) < 2:
        goc = ("nhan-su-" + goc).strip("-")
    slug, n = goc, 2
    while (agents / (slug + ".md")).exists():
        slug, n = "%s-%d" % (goc, n), n + 1
    return slug


def _doi_ten(body, cu, moi):
    """Hướng dẫn gọi tên bản gốc thì đổi sang tên mới, phần trách nhiệm đồng bộ giữ nguyên."""
    tim = re.compile(r"(?<!\w)" + re.escape(cu) + r"(?!\w)", re.I)
    m = re.search(re.escape(BAT_DAU) + r".*?" + re.escape(KET_THUC), body, re.S)
    if not m:
        return tim.sub(lambda _: moi, body)
    return tim.sub(lambda _: moi, body[:m.start()]) + m.group(0) + tim.sub(lambda _: moi, body[m.end():])


def nhan_ban(agents, slug, ten):
    ten = " ".join(str(ten or "").split())[:TEN_TOI_DA]
    if not ten:
        return {"ok": False, "error": "Chưa có tên nhân sự mới."}
    goc = agents / (Path(str(slug)).name + ".md")
    if not goc.is_file():
        return {"ok": False, "error": "Không còn cộng sự này."}
    cur = read_agent(goc)
    meta = dict(cur["meta"])
    moi = _slug_trong(agents, ten)
    ten_cu = str(meta.get("name") or goc.stem)
    meta.pop("pinned", None)
    meta.update(name=ten, slug=moi, updated=time.strftime("%Y-%m-%d"))
    (agents / (moi + ".md")).write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip() + "\n---\n" + _doi_ten(cur["body"], ten_cu, ten), encoding="utf-8")
    return {"ok": True, "slug": moi, "name": ten}
