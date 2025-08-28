USE walmart_sales;

-- 1. Primary key uniqueness check (store, dept, date)
SELECT store, dept, date, COUNT(*) AS c
FROM walmart_sales_clean
GROUP BY store, dept, date
HAVING c > 1;

-- 2. Check for negative sales
SELECT COUNT(*) AS negative_sales
FROM walmart_sales_clean
WHERE weekly_sales < 0;

-- 3. Date range
SELECT MIN(date) AS min_date, MAX(date) AS max_date
FROM walmart_sales_clean;

-- 4. Missing value check
SELECT
  SUM(CASE WHEN weekly_sales IS NULL THEN 1 ELSE 0 END) AS missing_sales,
  SUM(CASE WHEN store IS NULL THEN 1 ELSE 0 END) AS missing_store,
  SUM(CASE WHEN dept IS NULL THEN 1 ELSE 0 END) AS missing_dept
FROM walmart_sales_clean;



