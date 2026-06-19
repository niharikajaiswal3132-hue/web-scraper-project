import feedparser
import hashlib

RSS_FEEDS = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "Google News": "https://news.google.com/rss",
    "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
}

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

def fetch_news():
    articles = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "id": hash_text(entry.title + source),
                "title": entry.title,
                "source": source,
                "link": entry.link,
                "published": getattr(entry, "published", "Unknown"),
                "summary": getattr(entry, "summary", ""),
                "raw": (entry.title + " " + getattr(entry, "summary", "")).lower()
            })

    return articles