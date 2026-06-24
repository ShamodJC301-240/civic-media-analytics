# ~ load_postgres.py
# Load social media metrics into Postgres.

import argparse
import pandas as pd
from pathlib import Path

from db import get_engine, create_schema


# ~ Loader
# --------------------------------------------------
# Load CSV data into the media_events table.

def load_data_to_postgres(csv_path: str, if_exists: str = "append"):
    """Load a CSV of social media metrics into Postgres."""

    path = Path(csv_path)

    # Validate the file exists before attempting a load.
    if not path.exists():
        raise FileNotFoundError(
            f"CSV not found at: {csv_path}"
        )

    engine = get_engine()

    # Create the table if it doesn't exist.
    create_schema(engine)

    df = pd.read_csv(path)

    df.to_sql(
        "media_events",
        engine,
        if_exists=if_exists,
        index=False,
    )

    print(
        f"Loaded {len(df):,} rows into media_events "
        f"(if_exists='{if_exists}')."
    )


# ~ CLI
# --------------------------------------------------
# Parse command-line arguments and run the loader.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load a metrics CSV into Postgres."
    )

    parser.add_argument(
        "csv_path",
        help="Path to social_media_metrics.csv"
    )

    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace the table before loading."
    )

    args = parser.parse_args()

    # Append by default unless --replace is provided.
    mode = "replace" if args.replace else "append"

    load_data_to_postgres(
        args.csv_path,
        if_exists=mode
    )