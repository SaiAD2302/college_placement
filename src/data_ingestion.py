import os
from datetime import datetime

import pandas as pd

data_directory = "../data"
raw_directory = "raw"
file_name = "CollegePlacement.csv"


def ingest_raw():
    path = os.path.join(data_directory, raw_directory, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError("File at {path} not found.")
    data = pd.read_csv(path)
    print(
        f"""Loaded raw data with {data.shape[0]} rows and
{data.shape[1]} columns."""
    )
    return data


def save_snapshot(df1: pd.DataFrame):
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    s_file_name = f"CollegePlacement_{ts}.csv"
    snapshot_path = os.path.join(data_directory, raw_directory, s_file_name)
    df1.to_csv(snapshot_path, index=False)
    print(f"Snapshot saved to {snapshot_path}")


if __name__ == "__main__":
    df = ingest_raw()
    save_snapshot(df)
    print(df.head())
