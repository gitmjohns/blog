from datetime import datetime
import random

# Fallback topic
topics = ["Technology news", "Global events", "Popular culture"]
topic = random.choice(topics)
print(f"📝 Selected topic: {topic}")

# Dummy post content
post_content = f"This is a test blog post about {topic}. It does not use OpenAI API."

# Format as Jekyll blog post
date = datetime.now().strftime("%Y-%m-%d")
safe_topic = "".join(c if c.isalnum() or c in "-_" else "-" for c in topic)
filename = f"_posts/{date}-{safe_topic}.md"

front_matter = f"""---
layout: post
title: "{topic}"
date: {date}
---
"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(front_matter + "\n" + post_content)

print(f"✅ Dummy blog post generated: {filename}")
