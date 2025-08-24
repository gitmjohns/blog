import feedparser
import os
from datetime import datetime

# Full set of RSS feed sources
FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.sciencedaily.com/rss/top.xml",
    "https://www.economist.com/the-world-this-week/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
    "https://www.npr.org/rss/rss.php?id=1004",
    "https://www.cbsnews.com/latest/rss/world",
    "https://www.nbcnews.com/id/3032507/device/rss/rss.xml",
    "https://www.theguardian.com/world/rss",
    "https://apnews.com/apf-intlnews?format=xml"
]

POSTS_DIR = "_posts"

def slugify(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")

def fetch_and_create_posts():
    os.makedirs(POSTS_DIR, exist_ok=True)

    for feed_url in FEEDS:
        print(f"Fetching {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:3]:  # take up to 3 per feed
            title = entry.title
            link = entry.link
            summary = getattr(entry, "summary", "")[:280]  # trim summary
            published = getattr(entry, "published", None)

            # Parse datetime safely
            try:
                dt = datetime(*entry.published_parsed[:6])
            except Exception:
                dt = datetime.utcnow()

            slug = slugify(title)[:50]
            filename = f"{POSTS_DIR}/{dt.strftime('%Y-%m-%d')}-{slug}.md"

            if os.path.exists(filename):
                continue

            # Put the raw source link directly inside the post body
            blurb = f"{summary}\n\nSource: {link}"

            content = f"""---
layout: post
title: "{title}"
date: {dt.strftime('%Y-%m-%d %H:%M:%S %z')}
categories: news
source_url: {link}
---

{blurb}
"""

            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Created {filename}")

if __name__ == "__main__":
    fetch_and_create_posts()
