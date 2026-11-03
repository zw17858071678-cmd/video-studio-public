from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import requests

output = Path(__file__).with_name("news.json")
now = datetime.now(timezone(timedelta(hours=8)))
day = now.date().isoformat()
previous = json.loads(output.read_text()) if output.exists() else {}
if previous.get("updated_day") == day:
    raise SystemExit(0)

response = requests.get("https://news.google.com/rss/search", params={
    "q": "人工智能 when:2d", "hl": "zh-TW", "gl": "TW", "ceid": "TW:zh-Hant",
}, timeout=20)
response.raise_for_status()
articles, seen = [], set()
for item in ET.fromstring(response.content).findall("./channel/item"):
    source = item.findtext("source", "").strip()
    title = item.findtext("title", "").strip().removesuffix(f" - {source}")
    url = item.findtext("link", "").strip()
    if not title or not source or title in seen or not url.startswith("https://news.google.com/rss/articles/"):
        continue
    try:
        date = parsedate_to_datetime(item.findtext("pubDate", ""))
    except ValueError:
        continue
    if not now - timedelta(days=2) <= date <= now:
        continue
    seen.add(title)
    articles.append(dict(title=title, source=source, url=url))

if not articles:
    raise SystemExit("新闻源没有提供可发布报道，保留上次内容。")

featured = previous.get("featured", [])
used = {item["title"] for item in featured}
terms = ("發布", "发布", "推出", "更新", "開放", "开放", "教學", "教程", "實測", "实测")
pick = next((item for item in articles if item["title"] not in used
             and any(term in item["title"] for term in terms)), None)
if pick:
    featured = [dict(pick, daily_edition=day), *featured][:30]
trending = [dict(item, day=day, rank=rank) for rank, item in enumerate(articles[:10], 1)]
data = dict(updated_day=day, featured=featured, trending=trending, articles=articles[:15])
temporary = output.with_suffix(".tmp")
temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
temporary.replace(output)
