import json
import os
from datetime import datetime

import pandas as pd

from data_ingestion import ingest_raw

processed_dir = os.path.join("..", "data", "processed")
report_dir = os.path.join("data", "reports")
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)


def val(df: pd.DataFrame, id_column: str = "College_ID") -> dict:
    summary = {}
    if id_column in df.columns:
        n = len(df)
        nd = df[id_column].nunique()
        if n != nd:
            print("Duplicate ids exist:", n - nd)
    miss = df.isnull().sum()
    missing = miss[miss > 0]

    summary["missing"] = missing.to_dict()
    if not missing.empty:
        print("Missing values per column")
        print(missing)
    else:
        print("No missing values")
    summary["dtypes"] = df.dtypes.to_dict()
    print("column data types")
    print(df.dtypes)
    return summary


def save_val_report(summary: dict):
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    report_path = os.path.join(report_dir, f"val_report_{ts}.json")
    safe_summary = {}
    for i, j in summary.items():
        if isinstance(j, dict):
            safe_summary[i] = {str(ii): str(jj) for ii, jj in j.items()}
        else:
            safe_summary[i] = str(j)
        with open(report_path, "w") as f:
            json.dump(safe_summary, f, indent=4)
        print(f"report saved to {report_path}")
        return report_path


def save_val_data(df: pd.DataFrame, filename: str = "val_data.csv"):
    path = os.path.join(processed_dir, filename)
    df.to_csv(path, index=False)
    print(f"data saved to {path}")
    return path


if __name__ == "__main__":
    df = ingest_raw()
    summary = val(df)
    print(summary)
    print(save_val_report(summary))
    print(save_val_data(df))
