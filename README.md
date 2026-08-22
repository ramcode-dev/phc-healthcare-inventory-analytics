# Public Healthcare Medicine Supply & Demand Analytics

## 📌 Project Overview
An end-to-end data analytics project focused on monitoring public healthcare center (PHC) medicine stocks, detecting delivery delays, and identifying high-risk stockout centers across regional districts.

Designed for **Government & Health Informatics R&D** workflows (aligned with C-DAC Bangalore Knowledge Associate domain areas).

---

## 🛠️ Tech Stack & Skills
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Database & Querying:** SQL (SQLite / SQLite3 in Python)
* **Visualization:** Matplotlib, Seaborn
* **Data Format:** CSV

---

## 📊 Key Highlights & Analytics Findings
1. **Data Cleaning:** Replaced missing stock values with median medicine inventories, parsed missing delivery delay entries, and derived `Stock_Ratio`.
2. **Risk Categorization:** Automatically flagged centers as `CRITICAL (< 25%)`, `WARNING (25-60%)`, or `SAFE (> 60%)`.
3. **SQL Reporting:** Grouped centers by district and medicine type to prioritize delivery route dispatch.

---

## 🚀 How to Run

1. Clone repository:
```bash
git clone <your-repo-link>
cd project1_healthcare_inventory_analytics
```

2. Run the automated data generation & analysis pipeline:
```bash
python generate_data.py
python analysis.py
```

3. Check output:
* Dataset saved at: `dataset/phc_medicine_supply.csv`
* Chart saved at: `charts/stockout_risk_by_district.png`
* SQL queries available in: `queries.sql`
