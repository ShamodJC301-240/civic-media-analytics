from faker import Faker
import random
import csv
from pathlib import Path

fake = Faker()

# Output path 
output_path = Path("data") / "social_media_metrics.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

platforms = ["youtube", "instagram", "tiktok", "twitter", "facebook"]
content_types = ["video", "post", "reel", "story", "short"]

rows = []

# Generate 200 rows of fake data
for _ in range(200):
    platform = random.choice(platforms)
    content_type = random.choice(content_types)

    views = random.randint(500, 100000)
    likes = int(views * random.uniform(0.01, 0.15))
    shares = int(likes * random.uniform(0.05, 0.5))
    comments = int(likes * random.uniform(0.03, 0.4))

    rows.append([
        platform,
        content_type,
        views,
        likes,
        shares,
        comments
    ])

# Write CSV
with open(output_path, "w", newline="") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "platform",
        "content_type",
        "views",
        "likes",
        "shares",
        "comments"
    ])

    # Data
    writer.writerows(rows)

print(f"CSV created at: {output_path.resolve()}")