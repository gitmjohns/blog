import os
from openai import OpenAI
from datetime import datetime
from pytrends.request import TrendReq
import random

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Try fetching trending topics
pytrends = TrendReq(hl="en-US", tz=360)
try:
    trending_searches = pytrends.today_searches(pn="US")
    topics = trending_searches.tolist()
except Exception:
    print("⚠️ Could not fetch Google Trends, using fallback topic.")
    topics = ["Technology news", "Global events", "Popular culture"]

topic = random.choice(topics)
print(f"📝 Selected topic: {topic}")

# Prompt for OpenAI
prompt = f"Write a short, engaging blog post about the trending topic: {topic}. Keep it under 400 words."

# Generate post via OpenAI
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    # Get content safely
    post_content = response.choices[0].message.get("content") or response.choices[0].text
except Exception as e:
    print(f"⚠️ OpenAI API failed: {e}")
    post_content = f"This is a fallback post about {topic}."

# Format for Jekyll
date = datetime.now().strftime("%Y-%m-%d")
safe_topic = "".join(c if c.isalnum() or c in "-_" else "-" for c in topic)
filename = f"_posts/{date}-{safe_topic}.md"

front_matter = f"""---
layout: post
title: "{topic}"
date: {date}
---
"""

# Write the file
os.makedirs("_posts", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + post_content)

print(f"✅ Blog post generated: {filename}")
