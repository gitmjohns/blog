import openai
import datetime
import os
from pytrends.request import TrendReq
import random

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get trending topics from Google Trends
pytrends = TrendReq(hl="en-US", tz=360)
trending_searches = pytrends.trending_searches(pn="united_states")
topics = trending_searches[0].tolist()
topic = random.choice(topics)  # pick a random trending topic

# Ask OpenAI to generate a blog post
prompt = f"""
Write a detailed, SEO-friendly blog post about the trending topic: "{topic}".
- Length: 600-800 words
- Include a clear introduction, main body, and conclusion
- Use a neutral, informative tone
- Suggest why the topic is important right now
"""

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1000,
    temperature=0.7,
)

post_content = response.choices[0].message["content"].strip()

# Prepare file path
today = datetime.datetime.utcnow()
filename = today.strftime("_posts/%Y-%m-%d-") + topic.replace(" ", "-") + ".md"

# Front matter for Jekyll
front_matter = f"""---
layout: post
title: "{topic}"
date: {today.strftime("%Y-%m-%d %H:%M:%S")} +0000
categories: trending
---

"""

# Write the blog post
with open(filename, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + post_content)

print(f"✅ New post created: {filename}")
