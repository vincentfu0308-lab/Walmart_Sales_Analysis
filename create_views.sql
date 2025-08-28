USE walmart_sales;

-- 1) Daily overall sales trend
CREATE OR REPLACE VIEW vw_sales_daily AS
SELECT 
    date,
    SUM(weekly_sales) AS total_weekly_sales
FROM walmart_sales_clean
GROUP BY date
ORDER BY date;

-- 2) Store total sales ranking
CREATE OR REPLACE VIEW vw_store_rank AS
SELECT 
    store,
    SUM(weekly_sales) AS total_sales
FROM walmart_sales_clean
GROUP BY store
ORDER BY total_sales DESC;

-- 3) Store type performance
CREATE OR REPLACE VIEW vw_type_sales AS
SELECT 
    type,
    COUNT(DISTINCT store) AS num_stores,
    SUM(weekly_sales) AS total_sales,
    AVG(weekly_sales) AS avg_weekly_sales
FROM walmart_sales_clean
GROUP BY type;

-- Preview results from the views
SELECT * FROM vw_sales_daily;
SELECT * FROM vw_store_rank;
SELECT * FROM vw_type_sales;