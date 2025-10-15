import os

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Input/output paths
processed_dir = os.path.join("..", "..", "data", "processed")
input_file = os.path.join(processed_dir, "val_data.csv")
output_file = os.path.join(processed_dir, "features.csv")

# Read validated data
df = pd.read_csv(input_file)

# Drop College_ID (not a feature)
df = df.drop(columns=["College_ID"])

# Encode categorical features
IE = "Internship_Experience"
df[IE] = df[IE].map({"Yes": 1, "No": 0})
df["Placement"] = df["Placement"].map({"Yes": 1, "No": 0})  # target

# Optional: create interaction features
df["IQ_x_Academic"] = df["IQ"] * df["Academic_Performance"]
df["CGPA_x_ExtraCurricular"] = df["CGPA"] * df["Extra_Curricular_Score"]

# Optional: scale numeric features
numeric_cols = [
    "IQ",
    "Prev_Sem_Result",
    "CGPA",
    "Academic_Performance",
    "Extra_Curricular_Score",
    "Communication_Skills",
    "Projects_Completed",
    "IQ_x_Academic",
    "CGPA_x_ExtraCurricular",
]

scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save processed features
os.makedirs(processed_dir, exist_ok=True)
df.to_csv(output_file, index=False)
print(f"Feature-engineered data saved at {output_file}")
