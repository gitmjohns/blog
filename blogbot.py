import feedparser
import os
from datetime import datetime
import random

# Multiple RSS feeds for diversity
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.theguardian.com/world/rss"
]

# Choose a random feed each run
feed_url = random.choice(RSS_FEEDS)
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No articles found.")
    exit()

# Pick a random article from the feed
entry = random.choice(feed.entries)

title = entry.title
link = entry.link
summary = getattr(entry, "summary", "No summary available.")

# Make summary longer (truncate if very long)
summary = summary.replace("\n", " ")
if len(summary) > 500:
    summary = summary[:500] + "..."

# Create Jekyll-style markdown file in _posts
date_str = datetime.utcnow().strftime("%Y-%m-%d")
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
slug = title.lower().replace(" ", "-").replace("/", "-")[:50]

filename = f"_posts/{date_str}-{slug}.md"

os.makedirs("_posts", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\n")
    f.write(f"layout: post\n")
    f.write(f'title: "{title}"\n')
    f.write(f"date: {timestamp}\n")
    f.write(f"---\n\n")
    f.write(f"{summary}\n\n")
    f.write(f"[Read more]({link})\n")

print(f"✅ New post created: {filename}")
