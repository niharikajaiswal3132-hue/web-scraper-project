import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
from collections import Counter
import re
import textwrap

# ---------------- PAGE ----------------
st.set_page_config(page_title="News Dashboard", layout="wide")

st.title("🧠 News Intelligence Dashboard (Freelancing Ready)")

# ---------------- SOURCES ----------------
rss_feeds = {
    "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Business": "https://news.google.com/rss/search?q=Business&hl=en-IN&gl=IN&ceid=IN:en",
    "Technology": "https://news.google.com/rss/search?q=Technology&hl=en-IN&gl=IN&ceid=IN:en",
    "Sports": "https://news.google.com/rss/search?q=Sports&hl=en-IN&gl=IN&ceid=IN:en",
    "Politics": "https://news.google.com/rss/search?q=Politics+World&hl=en-IN&gl=IN&ceid=IN:en"
}

# ---------------- SIDEBAR ----------------
category = st.sidebar.selectbox("Category", list(rss_feeds.keys()))
search = st.sidebar.text_input("Search News")
sort_option = st.sidebar.selectbox("Sort", ["Latest First", "Oldest First"])

# ---------------- STOPWORDS ----------------
stop_words = {
    "the", "and", "for", "with", "this", "that", "from",
    "india", "news", "will", "have", "said"
}

# ---------------- SUMMARY FUNCTION ----------------
def generate_summary(title):
    return textwrap.shorten(title, width=80, placeholder="...")

# ---------------- DATE FIX ----------------
def parse_date(entry):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        return datetime.now()
    except:
        return datetime.now()

# ---------------- FETCH FEED ----------------
feed = feedparser.parse(rss_feeds[category])

if not feed.entries:
    st.error("No news found")
    st.stop()

# ---------------- DATA ----------------
articles = []
all_words = []

# ---------------- PROCESS ----------------
for entry in feed.entries:

    title = getattr(entry, "title", "")
    link = getattr(entry, "link", "#")
    published = parse_date(entry)

    # search filter
    if search and search.lower() not in title.lower():
        continue

    # summary
    summary = generate_summary(title)

    # trending words
    words = re.findall(r"[a-zA-Z]{3,}", title.lower())
    words = [w for w in words if w not in stop_words]
    all_words.extend(words)

    articles.append({
        "title": title,
        "link": link,
        "published": published,
        "summary": summary
    })

# ---------------- SORT ----------------
articles = sorted(
    articles,
    key=lambda x: x["published"],
    reverse=(sort_option == "Latest First")
)

# ---------------- DASHBOARD ----------------
st.subheader("📊 Quick Stats")

c1, c2 = st.columns(2)
c1.metric("Total Articles", len(articles))
c2.metric("Category", category)

# ---------------- TRENDING ----------------
st.subheader("🔥 Trending Topics")

top_words = Counter(all_words).most_common(10)

trend_df = pd.DataFrame(top_words, columns=["Keyword", "Count"])
st.bar_chart(trend_df.set_index("Keyword"))

# ---------------- NEWS DISPLAY ----------------
st.subheader("📰 Latest News")

for a in articles:

    st.markdown(f"### 📰 {a['title']}")
    st.write("📅", a["published"].strftime("%Y-%m-%d %H:%M"))
    st.write("🧠 Summary:", a["summary"])
    st.markdown(f"[Read Full Article]({a['link']})")
    st.divider()