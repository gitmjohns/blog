import feedparser
import os
from datetime import datetime
import random

# Large, diverse RSS feed list
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.theguardian.com/world/rss",
    "https://www.reutersagency.com/feed/?best-topics=world&post_type=best",
    "https://www.npr.org/rss/rss.php?id=1004",
    "https://www.wired.com/feed/rss",
    "https://www.nationalgeographic.com/content/nationalgeographic/en_us/news.rss",
    "https://techcrunch.com/feed/",
    "https://www.cnn.com/rss/edition_world.rss",
    "https://www.sciencedaily.com/rss/top/science.xml",
    "https://www.scientificamerican.com/feed/rss/",
    "https://www.economist.com/the-world-this-week/rss.xml",
    "https://www.forbes.com/world/rss2/",
    "https://www.bloomberg.com/feed/podcast/etf-report.xml",
    "https://www.vox.com/rss/index.xml",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.ft.com/?format=rss",
    "https://www.politico.com/rss/world.xml",
    "https://www.huffpost.com/section/world-news/feed",
    "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "https://www.engadget.com/rss.xml",
    "https://www.space.com/feeds/all",
    "https://www.sciencemag.org/rss/news_current.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://www.latimes.com/world/rss2.0.xml",
    "https://www.independent.co.uk/news/world/rss",
    "https://www.usatoday.com/rss/news/world",
    "https://www.nbcnews.com/id/3032091/device/rss/rss.xml",
    "https://www.bbc.co.uk/news/technology/rss.xml",
    "https://www.techradar.com/rss",
    "https://www.nature.com/subjects/news/rss",
    "https://www.sciencedaily.com/rss/mind_brain.xml",
    "https://www.technologyreview.com/feed/"
]

# Pick a random feed and entry
feed_url = random.choice(RSS_FEEDS)
feed = feedparser.parse(feed_url)

if not feed.entries:
    print("⚠️ No articles found in feed.")
    exit()

entry = random.choice(feed.entries)

# Extract data
title = entry.title
link = entry.link
summary = getattr(entry, "summary", "") or getattr(entry, "description", "No summary available.")

# Make summary longer (approx 500–700 chars)
summary = summary.replace("\n", " ")
if len(summary) > 700:
    summary = summary[:700] + "..."
elif len(summary) < 500:
    summary = summary + "..."  # pad short summaries

# Format filename
date = datetime.utcnow().strftime("%Y-%m-%d")
timestamp = datetime.utcnow().strftime("%H-%M-%S")
slug = title.lower().replace(" ", "-").replace("/", "-")[:50]
filename = f"_posts/{date}-{timestamp}.md"

# Build post content with source_url
content = f"""---
layout: post
title: "{title.replace('"', '')}"
date: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} +0000
categories: news
source_url: {link}
---

{summary}

[Read the full article here]({link})
"""

# Ensure _posts exists
os.makedirs("_posts", exist_ok=True)

# Write post
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ New post created: {filename}")
