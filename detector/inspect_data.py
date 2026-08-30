import pandas as pd

pd.set_option("display.max_columns", None)  # <-- this stops columns from being hidden

def inspect(filepath):
    print("=" * 60)
    print(f"Inspecting: {filepath}")
    print("=" * 60)
    df = pd.read_csv(filepath)
    print("Columns:", df.columns.tolist())
    print()
    print("First 3 rows:")
    print(df.head(3))
    print()
    print("Unique values in 'class' column:", df["class"].unique() if "class" in df.columns else "no 'class' column")
    print()
    print("Total rows:", len(df))
    print()

inspect("../data/Dataset_uav_cyber.csv")
inspect("../data/merged_wifi_attacks_dataset.csv")