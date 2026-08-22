-- ====================================================================
-- PROJECT 1: PUBLIC HEALTHCARE MEDICINE SUPPLY & DEMAND ANALYTICS
-- SQL QUERIES FOR REPORITNG AND INSIGHTS
-- ====================================================================

-- 1. Identify Districts with the Highest Critical Stockout Risk
SELECT 
    District, 
    COUNT(*) AS Total_Centers,
    SUM(CASE WHEN Stockout_Risk LIKE 'CRITICAL%' THEN 1 ELSE 0 END) AS Critical_Stockout_Count,
    ROUND(AVG(Delivery_Delay_Days), 1) AS Avg_Delivery_Delay_Days
FROM phc_inventory
GROUP BY District
ORDER BY Critical_Stockout_Count DESC;


-- 2. Identify Specific Medicines Facing Supply Deficit Across All Centers
SELECT 
    Medicine_Name,
    ROUND(AVG(Stock_Ratio) * 100, 1) AS Avg_Stock_Satisfaction_Pct,
    SUM(CASE WHEN Stockout_Risk LIKE 'CRITICAL%' THEN 1 ELSE 0 END) AS Critical_Count
FROM phc_inventory
GROUP BY Medicine_Name
ORDER BY Avg_Stock_Satisfaction_Pct ASC;


-- 3. High-Priority Restock Action List (Health Centers requiring urgent supply)
SELECT 
    Center_ID,
    Center_Name,
    District,
    Medicine_Name,
    Current_Stock_Qty,
    Required_Monthly_Qty,
    Delivery_Delay_Days
FROM phc_inventory
WHERE Stockout_Risk LIKE 'CRITICAL%'
  AND Delivery_Delay_Days > 5
ORDER BY Delivery_Delay_Days DESC;
