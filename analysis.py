"""
Public Health Center (PHC) Inventory Analytics

Author: Ram
Description: Data cleaning, SQL aggregation, and risk analysis of medicine supply
            and stockout delays across regional primary healthcare centers.
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "phc_medicine_supply.csv")
CHART_PATH = os.path.join(BASE_DIR, "charts", "stockout_risk_by_district.png")


def load_and_prep_data(filepath):
    df = pd.read_csv(filepath)

    # Clean numeric fields
    df["Current_Stock_Qty"] = pd.to_numeric(df["Current_Stock_Qty"], errors="coerce")
    df["Delivery_Delay_Days"] = pd.to_numeric(df["Delivery_Delay_Days"], errors="coerce")

    # Impute missing stock values using median per medicine
    med_medians = df.groupby("Medicine_Name")["Current_Stock_Qty"].transform("median")
    df["Current_Stock_Qty"] = df["Current_Stock_Qty"].fillna(med_medians)
    df["Delivery_Delay_Days"] = df["Delivery_Delay_Days"].fillna(0)

    # Stock satisfaction ratio & risk tag
    df["Stock_Ratio"] = (df["Current_Stock_Qty"] / df["Required_Monthly_Qty"]).round(2)

    def calc_risk(r):
        if r < 0.25:
            return "Critical (<25%)"
        elif r < 0.60:
            return "Warning (25-60%)"
        return "Optimal (>60%)"

    df["Stockout_Risk"] = df["Stock_Ratio"].apply(calc_risk)
    return df


def analyze_with_sql(df):
    conn = sqlite3.connect(":memory:")
    df.to_sql("phc_inventory", conn, index=False, if_exists="replace")

    query_district = """
    SELECT 
        District, 
        COUNT(*) AS Total_Centers,
        SUM(CASE WHEN Stockout_Risk LIKE 'Critical%' THEN 1 ELSE 0 END) AS Critical_Centers,
        ROUND(AVG(Delivery_Delay_Days), 1) AS Avg_Delay_Days
    FROM phc_inventory
    GROUP BY District
    ORDER BY Critical_Centers DESC;
    """

    query_medicine = """
    SELECT 
        Medicine_Name,
        ROUND(AVG(Stock_Ratio) * 100, 1) AS Stock_Fulfillment_Pct,
        SUM(CASE WHEN Stockout_Risk LIKE 'Critical%' THEN 1 ELSE 0 END) AS Shortage_Count
    FROM phc_inventory
    GROUP BY Medicine_Name
    ORDER BY Stock_Fulfillment_Pct ASC;
    """

    district_summary = pd.read_sql_query(query_district, conn)
    medicine_summary = pd.read_sql_query(query_medicine, conn)
    conn.close()

    return district_summary, medicine_summary


def generate_visualization(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ct = pd.crosstab(df["District"], df["Stockout_Risk"])
    
    # Reorder columns logically if present
    cols = [c for c in ["Critical (<25%)", "Warning (25-60%)", "Optimal (>60%)"] if c in ct.columns]
    ct = ct[cols]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ct.plot(kind="bar", stacked=True, color=["#d9534f", "#f0ad4e", "#5cb85c"], ax=ax)

    ax.set_title("Health Center Stockout Risk Distribution by District", fontsize=11, fontweight="bold")
    ax.set_xlabel("District", fontsize=9)
    ax.set_ylabel("Number of Centers", fontsize=9)
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()

    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing dataset at {DATA_PATH}")

    df = load_and_prep_data(DATA_PATH)
    district_df, medicine_df = analyze_with_sql(df)

    print("--- District Inventory Summary ---")
    print(district_df.to_string(index=False))

    print("\n--- Medicine Fulfillment Deficit ---")
    print(medicine_df.to_string(index=False))

    generate_visualization(df, CHART_PATH)
    print(f"\nSaved risk distribution chart to {CHART_PATH}")


if __name__ == "__main__":
    main()
