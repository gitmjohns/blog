import feedparser
import os
from datetime import datetime
import random

# Choose feed
feeds = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
]
feed_url = random.choice(feeds)

print(f"📡 Fetching from: {feed_url}")
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No entries found from this feed.")
else:
    entry = feed.entries[0]  # first article
    title = entry.title.replace(":", "-")
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{date}-{title[:30].replace(' ', '-')}.md"

    print(f"📝 Writing new post: {filename}")

    content = f"""---
layout: post
title: "{entry.title}"
date: {date}
---

{entry.summary if 'summary' in entry else 'No summary available.'}
"""

    os.makedirs("_posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Blog post created successfully!")
