"""Read-only visitor edition of Video Studio."""
import streamlit as st

import json
from pathlib import Path

feed = Path(__file__).with_name("news.json")
data = json.loads(feed.read_text()) if feed.exists() else {}

st.set_page_config(page_title="视频工作室 · 公开版", layout="centered")
st.markdown("""
<style>
.stApp { background: radial-gradient(ellipse at top, #15344d, #090f1b 60%); color: #edf5ff; }
.stApp :is(h1, h2, h3, p, button) { color: #edf5ff; }
.stApp a { color: #83e9ff; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stAlert"] { background: #152a40; }
</style>
""", unsafe_allow_html=True)

st.caption("VIDEO STUDIO · 公开版")
st.title("AI 新闻与每日优选")
st.write("浏览每日精选、热点榜和近期 AI 报道。")
featured, trending, news = st.tabs(["每日优选", "热点 TOP 10", "AI 实时新闻"])

with featured:
    editions = data.get("featured", [])
    if not editions:
        st.info("暂无每日精选。")
    for item in editions:
        with st.container(border=True):
            st.caption(f"{item['daily_edition']} · {item['source']}")
            st.subheader(item["title"])
            st.markdown(f"[阅读报道 ↗]({item['url']})")

with trending:
    rows = data.get("trending", [])
    if rows:
        st.caption(f"{rows[0]['day']} · 按 Google 新闻检索顺序去重")
    else:
        st.info("暂无热点榜单。")
    for item in rows:
        with st.container(border=True):
            st.subheader(f"{item['rank']:02d} · {item['title']}")
            st.caption(item["source"])
            st.markdown(f"[阅读报道 ↗]({item['url']})")

with news:
    articles = data.get("articles", [])
    if not articles:
        st.info("暂无新闻。")
    for item in articles:
        with st.container(border=True):
            st.subheader(item["title"])
            st.caption(item["source"])
            st.markdown(f"[阅读报道 ↗]({item['url']})")
