import os
import random
from openai import OpenAI
from datetime import date

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# List of fallback topics
topics = [
    "Technology news",
    "Health and wellness",
    "Science breakthroughs",
    "Popular culture",
    "Global events",
    "Business and economy",
    "Sports highlights",
    "Travel and lifestyle"
]

# Pick a random topic
topic = random.choice(topics)
print(f"📝 Selected topic: {topic}")

# Ask OpenAI for a blog post
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful writing assistant that creates short blog posts."},
        {"role": "user", "content": f"Write a concise, engaging blog post (200-300 words) about {topic}."}
    ]
)

blog_content = response.choices[0].message.content

# Format blog post in Jekyll markdown format
today = date.today()
filename = f"_posts/{today}-" + topic.replace(" ", "-") + ".md"

with open(filename, "w") as f:
    f.write(f"---\nlayout: post\ntitle: {topic}\ndate: {today}\n---\n")
    f.write(blog_content)

print(f"✅ Blog post saved to {filename}")
