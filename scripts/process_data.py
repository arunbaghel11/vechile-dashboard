"""
Reads raw CSVs → adds YoY & QoQ % change columns.
Run after scrape; saves processed_*.csv back to data/.
"""
import os
import pandas as pd
from datetime import datetime

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

def add_growth(df, group_cols, val_col):
    if "date" in df.columns:
        df = df.sort_values("date")
        df["YoY_%"] = df.groupby(group_cols)[val_col].pct_change(periods=12).round(3)*100
        df["QoQ_%"] = df.groupby(group_cols)[val_col].pct_change(periods=3).round(3)*100
    else:
        df["YoY_%"] = None
        df["QoQ_%"] = None
    return df

def main():
    # Process vehicle_class_group.csv
    vcg = pd.read_csv(f"{DATA}/vehicle_class_group.csv")
    # Add a dummy date column (today) for compatibility
    vcg["date"] = datetime.today().date()
    vcg_long = vcg.melt(id_vars=["date", "Vehicle Class"], value_vars=["4WIC", "LMV", "MMV", "HMV", "TOTAL"],
                        var_name="category", value_name="registrations")
    vcg_out = add_growth(vcg_long, ["Vehicle Class", "category"], "registrations")
    vcg_out.to_csv(f"{DATA}/processed_vehicle_class_group.csv", index=False)
    print("Processed vehicle_class_group.csv")

if __name__ == "__main__":
    main()