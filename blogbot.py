import os
import openai
from datetime import datetime
from pytrends.request import TrendReq
import random

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fetch trending topic
pytrends = TrendReq(hl="en-US", tz=360)

try:
    trending_searches = pytrends.today_searches(pn="US")
    topics = trending_searches.tolist()
except Exception as e:
    print("⚠️ Could not fetch Google Trends, using fallback topic.")
    topics = ["Technology news", "Global events", "Popular culture"]

topic = random.choice(topics)
print(f"📝 Selected topic: {topic}")

# Generate a blog post using OpenAI
prompt = f"Write a short, engaging blog post about the trending topic: {topic}. Keep it under 400 words."

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500,
    temperature=0.7,
)

post_content = response["choices"][0]["message"]["content"]

# Format as Jekyll blog post
date = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{date}-{topic.replace(' ', '-')}.md"

front_matter = f"""---
layout: post
title: "{topic}"
date: {date}
---
"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + post_content)

print(f"✅ Blog post generated: {filename}")
