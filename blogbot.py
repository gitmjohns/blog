import os
import requests
import feedparser
from datetime import datetime
import hashlib
import yaml

# Your RSS feed sources
FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.sciencedaily.com/rss/top/science.xml"
]

POSTS_DIR = "_posts"

def slugify(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")

def fetch_articles():
    articles = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            source_url = entry.link
            title = entry.title
            summary = entry.summary if hasattr(entry, "summary") else ""
            date = datetime(*entry.published_parsed[:6])
            uid = hashlib.md5(source_url.encode()).hexdigest()[:10]

            # Here's the trick: put the raw link **inside** the blurb
            content = f"""{summary[:200]}...  
            
Direct source link: {source_url}
"""

            articles.append({
                "title": title,
                "date": date,
                "slug": slugify(title)[:40] + "-" + uid,
                "content": content,
                "source_url": source_url
            })
    return articles

def write_post(article):
    filename = f"{article['date'].strftime('%Y-%m-%d')}-{article['slug']}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if os.path.exists(filepath):
        return  # Skip duplicates

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"layout: post\n")
        f.write(f"title: \"{article['title']}\"\n")
        f.write(f"date: {article['date'].strftime('%Y-%m-%d %H:%M:%S %z')}\n")
        f.write(f"categories: news\n")
        f.write("---\n\n")
        f.write(article["content"])
        f.write(f"\n\n[Read the full article here]({article['source_url']})\n")

def main():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    articles = fetch_articles()
    for article in articles:
        write_post(article)

if __name__ == "__main__":
    main()
