import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

csv_path = os.path.join(DATASET_DIR, "phc_medicine_supply.csv")

if not os.path.exists(csv_path):
    import generate_data

print("==================================================================")
print("  PROJECT 1: PUBLIC HEALTHCARE MEDICINE SUPPLY & DEMAND ANALYTICS")
print("==================================================================")

# 1. Load Raw Dataset
df = pd.read_csv(csv_path)
print(f"\n[STEP 1] Loaded raw dataset from {csv_path}: {len(df)} records found.")

# 2. Data Cleaning
print("\n[STEP 2] Performing Data Cleaning...")
df['Current_Stock_Qty'] = pd.to_numeric(df['Current_Stock_Qty'], errors='coerce')
df['Delivery_Delay_Days'] = pd.to_numeric(df['Delivery_Delay_Days'], errors='coerce')

df['Current_Stock_Qty'] = df['Current_Stock_Qty'].fillna(df.groupby('Medicine_Name')['Current_Stock_Qty'].transform('median'))
df['Delivery_Delay_Days'] = df['Delivery_Delay_Days'].fillna(0)

df['Stock_Ratio'] = (df['Current_Stock_Qty'] / df['Required_Monthly_Qty']).round(2)

def assign_risk(ratio):
    if ratio < 0.25:
        return 'CRITICAL (Under 25%)'
    elif ratio < 0.60:
        return 'WARNING (25% - 60%)'
    else:
        return 'SAFE (Above 60%)'

df['Stockout_Risk'] = df['Stock_Ratio'].apply(assign_risk)
print("Data Cleaning Complete. Missing values handled and Risk Levels assigned.")

# 3. SQL Integration & Analytics
print("\n[STEP 3] Running SQL Analytics using SQLite Database...")
conn = sqlite3.connect(":memory:")
df.to_sql("phc_inventory", conn, index=False, if_exists="replace")

query_critical = """
SELECT 
    District, 
    COUNT(*) AS Total_Centers,
    SUM(CASE WHEN Stockout_Risk LIKE 'CRITICAL%' THEN 1 ELSE 0 END) AS Critical_Stockout_Count,
    ROUND(AVG(Delivery_Delay_Days), 1) AS Avg_Delivery_Delay
FROM phc_inventory
GROUP BY District
ORDER BY Critical_Stockout_Count DESC;
"""
df_sql_result = pd.read_sql_query(query_critical, conn)
print("\n--- SQL Query Result: District-wise Critical Stockout Summary ---")
print(df_sql_result.to_string(index=False))

query_medicines = """
SELECT 
    Medicine_Name,
    ROUND(AVG(Stock_Ratio) * 100, 1) AS Avg_Stock_Satisfaction_Pct,
    SUM(CASE WHEN Stockout_Risk LIKE 'CRITICAL%' THEN 1 ELSE 0 END) AS Critical_Count
FROM phc_inventory
GROUP BY Medicine_Name
ORDER BY Avg_Stock_Satisfaction_Pct ASC;
"""
df_med_result = pd.read_sql_query(query_medicines, conn)
print("\n--- SQL Query Result: Medicine Supply Deficit ---")
print(df_med_result.to_string(index=False))

# 4. Data Visualization
print("\n[STEP 4] Generating Data Visualization Chart...")
plt.figure(figsize=(9, 5))
district_risk = pd.crosstab(df['District'], df['Stockout_Risk'])
district_risk.plot(kind='bar', stacked=True, color=['#e74c3c', '#f39c12', '#2ecc71'], figsize=(9, 5))

plt.title("Public Health Center Stockout Risk Level by District", fontsize=12, fontweight='bold')
plt.xlabel("District", fontsize=10)
plt.ylabel("Number of Health Centers", fontsize=10)
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Stockout Risk Level")
plt.tight_layout()

chart_path = os.path.join(CHARTS_DIR, "stockout_risk_by_district.png")
plt.savefig(chart_path, dpi=300)
plt.close()
print(f"Chart saved successfully at: {chart_path}")

print("\n==================================================================")
print("  PROJECT 1 ANALYSIS COMPLETE! Output generated successfully.")
print("==================================================================")
