
from pathlib import Path
import pandas as pd



# Relative path for this file 
BASE_DIR = Path(__file__).resolve().parent

# Go up one level to project root
PROJECT_ROOT = BASE_DIR.parent

# Data folder path
Sample_data = PROJECT_ROOT / "testing" / "data" / "social_media_metrics.csv"

 
# Loading data
def load_data():
    df = pd.read_csv(Sample_data)
    return df

# Our KPIs
 
# Content totals 
def total_content(df):
    return len(df)

# Total views
def total_views(df):
    return df["views"].sum()

# Total engagement
def total_engagement(df):
    return df["likes"].sum() + df["shares"].sum() + df["comments"].sum()


 
# Engagement rates
def engagement_rate(df):
    views = df["views"].sum()

    if views == 0:
        return 0

    return total_engagement(df) / views

 
# Breakdowns for each platform
def platform_breakdown(df):
    return df.groupby("platform")[["views", "likes", "shares", "comments"]].sum()
 
# Here is how we run everything
if __name__ == "__main__":
    df = load_data()

    print("\n" + "-" * 40)
    print("CIVIC MEDIA KPI REPORT")
    print("-" * 40)

    print(f"Total Content: {total_content(df):,}")
    print(f"Total Views: {total_views(df):,}")
    print(f"Total Engagement: {total_engagement(df):,}")
    print(f"Engagement Rate: {engagement_rate(df):.2%}")

    print("\n" + "-" * 40)
    print("PLATFORM BREAKDOWN")
    print("-" * 40)
    
    breakdown = platform_breakdown(df)

    print("\n--- PLATFORM BREAKDOWN ---")
    print(breakdown.apply(lambda col: col.map(lambda x: f"{x:,}")))