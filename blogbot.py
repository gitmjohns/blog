import feedparser
import os
from datetime import datetime
import random
import re

# Configuration
POSTS_DIR = "_posts"
NUM_ARTICLES_PER_POST = 3  # how many RSS entries per post
os.makedirs(POSTS_DIR, exist_ok=True)

# RSS feeds
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
]

# Pick a random feed
feed_url = random.choice(RSS_FEEDS)
print(f"📡 Fetching from: {feed_url}")
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No entries found in this feed.")
    exit()

# Take first NUM_ARTICLES_PER_POST entries
selected_entries = feed.entries[:NUM_ARTICLES_PER_POST]

# Prepare post content
date = datetime.now().strftime("%Y-%m-%d")
titles_for_filename = "-".join([entry.title[:20] for entry in selected_entries])
slug = re.sub(r'[^a-z0-9]+', '-', titles_for_filename.lower()).strip("-")
filename = f"{date}-{slug}.md"
filepath = os.path.join(POSTS_DIR, filename)

post_content = f"---\nlayout: post\ntitle: \"RSS Digest {date}\"\ndate: {date}\n---\n\n"

for entry in selected_entries:
    title = entry.title
    summary = entry.get("summary", "No summary available.")
    link = entry.get("link", "#")
    post_content += f"### {title}\n\n{summary}\n\n[Read more]({link})\n\n---\n\n"

# Write the post
with open(filepath, "w", encoding="utf-8") as f:
    f.write(post_content)

print(f"✅ New digest post created: {filepath}")
