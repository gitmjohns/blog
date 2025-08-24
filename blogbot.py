import feedparser
import os
from datetime import datetime
import hashlib
import re

# List of RSS/Atom feeds to pull from
FEEDS = [
    "https://www.sciencedaily.com/rss/top/science.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "https://www.theguardian.com/science/rss",
    "https://www.economist.com/science-and-technology/rss.xml",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://www.space.com/feeds/all",
    "https://www.technologyreview.com/feed/",
    "https://www.wired.com/feed/category/science/latest/rss",
    "https://www.newscientist.com/feeds/home/",
]

# Path to posts folder
POSTS_DIR = "_posts"

def slugify(title):
    """Make a safe filename from the title"""
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def make_post(entry, feed_url):
    # Title
    title = entry.get("title", "Untitled").strip()

    # Extract source URL
    source_url = None
    if "link" in entry and entry.link:
        source_url = entry.link.strip()
    elif "id" in entry and entry.id:
        source_url = entry.id.strip()

    # Ensure fallback
    if not source_url:
        source_url = feed_url  # at least link back to feed

    # Content (short blurb)
    summary = entry.get("summary", "")
    clean_summary = re.sub(r"<.*?>", "", summary).strip()

    # Date
    published = None
    if "published_parsed" in entry and entry.published_parsed:
        published = datetime(*entry.published_parsed[:6])
    else:
        published = datetime.utcnow()

    # Hash ensures unique filenames
    unique_str = title + source_url
    hash_id = hashlib.md5(unique_str.encode("utf-8")).hexdigest()[:8]

    # Filename
    slug = slugify(title)
    filename = f"{published.strftime('%Y-%m-%d')}-{slug}-{hash_id}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if os.path.exists(filepath):
        print(f"Skipping duplicate: {title}")
        return

    # Front matter
    front_matter = f"""---
layout: post
title: "{title.replace('"', "'")}"
date: {published.strftime('%Y-%m-%d %H:%M:%S %z')}
categories: news
source_url: {source_url}
---

{clean_summary}

[Read the full article here]({source_url})
"""

    # Save post
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(front_matter)

    print(f"Created: {filename}")

def main():
    os.makedirs(POSTS_DIR, exist_ok=True)

    for feed_url in FEEDS:
        print(f"Fetching {feed_url} ...")
        d = feedparser.parse(feed_url)

        if not d.entries:
            print(f"No entries found in {feed_url}")
            continue

        for entry in d.entries[:3]:  # limit per feed to avoid overload
            make_post(entry, feed_url)

if __name__ == "__main__":
    main()
