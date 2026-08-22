import os
import csv
import random
from datetime import datetime, timedelta

# Create synthetic healthcare inventory dataset
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

districts = ["West Tripura", "South Tripura", "Dhalai", "Unakoti", "Gomati"]
medicines = ["Paracetamol 500mg", "Amoxicillin 250mg", "ORS Packets", "Metformin 500mg", "Azithromycin 500mg", "Amlodipine 5mg"]

header = ["Center_ID", "Center_Name", "District", "Medicine_Name", "Required_Monthly_Qty", "Current_Stock_Qty", "Delivery_Delay_Days", "Last_Restock_Date"]

rows = []
for i in range(1, 101):
    center_id = f"PHC_{100 + i}"
    center_name = f"Health Center {i}"
    district = random.choice(districts)
    medicine = random.choice(medicines)
    required = random.randint(300, 2000)
    
    if i % 15 == 0:
        stock = "" # Missing stock value
    else:
        stock = random.randint(50, 1800)
        
    delay = random.choice([0, 2, 5, 8, 12, 15, ""])
    days_ago = random.randint(5, 45)
    last_restock = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    
    rows.append([center_id, center_name, district, medicine, required, stock, delay, last_restock])

file_path = os.path.join(DATASET_DIR, "phc_medicine_supply.csv")

with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Dataset generated successfully at {file_path} with {len(rows)} records!")
