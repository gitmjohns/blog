import feedparser
import os
from datetime import datetime
import random

# List of RSS feeds (you can add/remove any you want)
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.feedburner.com/TechCrunch/"
]

# Pick a random feed and parse it
feed_url = random.choice(RSS_FEEDS)
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No articles found in the feed.")
    exit()

# Pick a random article from the feed
article = random.choice(feed.entries)

title = article.get("title", "Untitled")
summary = article.get("summary", "No summary available.")
date = datetime.now().strftime("%Y-%m-%d")

# Format a valid Jekyll post filename
filename = f"_posts/{date}-{title.replace(' ', '-').replace('/', '-')[:50]}.md"

# Ensure _posts directory exists
os.makedirs("_posts", exist_ok=True)

# Write markdown file
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\n")
    f.write(f"layout: post\n")
    f.write(f"title: \"{title}\"\n")
    f.write(f"date: {date}\n")
    f.write(f"---\n\n")
    f.write(summary)

print(f"✅ New post created: {filename}")
