# PHC Medicine Inventory Analytics

A Python & SQL data project analyzing medicine stock levels and delivery delays across Primary Healthcare Centers (PHCs).

## Overview
Regional healthcare centers often face supply chain bottlenecks leading to stockouts of key medicines. This project processes inventory logs from 100 health centers to identify districts with critical stock shortages and evaluate supplier delivery delays.

## Data Processing & Workflow
1. **Cleaning:** Handled missing stock counts by imputing medians by medicine category; converted delivery delay fields into numeric format.
2. **Feature Engineering:** Calculated a stock fulfillment ratio (`Current_Stock / Required_Monthly`) and categorized risk levels (`Critical`, `Warning`, `Optimal`).
3. **SQL Analytics:** Queried in-memory SQLite tables to group risk counts and calculate delivery delay averages per district.
4. **Visualization:** Plotting stacked bar charts of stockout risk levels per district using Matplotlib.

## Repository Structure
* `dataset/phc_medicine_supply.csv`: Raw healthcare center inventory log dataset.
* `analysis.py`: Main processing script (Pandas + SQLite + Matplotlib).
* `queries.sql`: Standalone SQL queries used in the analysis.
* `charts/stockout_risk_by_district.png`: Generated visualization output.

## Setup & Running
```bash
python analysis.py
```
