import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://username:password@localhost:5432/civic_kpi"
)

df = pd.read_csv("../data/social_media_metrics.csv")

df.to_sql(
    "media_events",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded.")