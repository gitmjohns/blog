import feedparser
import os
from datetime import datetime
import random
import re

# Folder for Jekyll posts
POSTS_DIR = "_posts"
os.makedirs(POSTS_DIR, exist_ok=True)

# A few free RSS feeds (you can add more if you like)
RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
]

# Pick a random feed
feed_url = random.choice(RSS_FEEDS)
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No articles found in feed.")
    exit()

# Pick a random article from the feed
entry = random.choice(feed.entries)

# Clean title for filename
def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

title = entry.title
slug = slugify(title)
date = datetime.now().strftime("%Y-%m-%d")
filename = f"{date}-{slug}.md"
filepath = os.path.join(POSTS_DIR, filename)

# Build post content
content = f"""---
layout: post
title: "{title}"
date: {date}
---

{entry.get('summary', 'No summary available.')}

[Read more here]({entry.link})
"""

# Save post
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ New blog post saved: {filepath}")
