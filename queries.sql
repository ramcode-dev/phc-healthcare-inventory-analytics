-- PHC Inventory Analytics SQL Queries
-- Database: SQLite (in-memory analytics)

-- 1. District level risk aggregation and delivery delay breakdown
SELECT 
    District, 
    COUNT(*) AS Total_Centers,
    SUM(CASE WHEN Stockout_Risk LIKE 'Critical%' THEN 1 ELSE 0 END) AS Critical_Centers,
    ROUND(AVG(Delivery_Delay_Days), 1) AS Avg_Delay_Days
FROM phc_inventory
GROUP BY District
ORDER BY Critical_Centers DESC;


-- 2. Medicine supply fulfillment percentage across all centers
SELECT 
    Medicine_Name,
    ROUND(AVG(Stock_Ratio) * 100, 1) AS Stock_Fulfillment_Pct,
    SUM(CASE WHEN Stockout_Risk LIKE 'Critical%' THEN 1 ELSE 0 END) AS Shortage_Count
FROM phc_inventory
GROUP BY Medicine_Name
ORDER BY Stock_Fulfillment_Pct ASC;


-- 3. Centers requiring urgent restocking (Critical status + high delivery delay)
SELECT 
    Center_ID,
    Center_Name,
    District,
    Medicine_Name,
    Current_Stock_Qty,
    Required_Monthly_Qty,
    Delivery_Delay_Days
FROM phc_inventory
WHERE Stockout_Risk LIKE 'Critical%'
  AND Delivery_Delay_Days > 5
ORDER BY Delivery_Delay_Days DESC;
