# Sales Analytics Dashboard

## Overview
Interactive dashboard for visualizing sales data with charts, KPIs, and drill-down capabilities.

## Database Schema
```sql
-- Sales Data
CREATE TABLE sales_data (
    sale_id NUMBER PRIMARY KEY,
    sale_date DATE NOT NULL,
    region VARCHAR2(50) NOT NULL,
    product_name VARCHAR2(100) NOT NULL,
    category VARCHAR2(50),
    sales_amount NUMBER(12,2) NOT NULL,
    quantity NUMBER NOT NULL,
    customer_name VARCHAR2(100)
);

-- Create indexes
CREATE INDEX sales_date_idx ON sales_data(sale_date);
CREATE INDEX sales_region_idx ON sales_data(region);
CREATE INDEX sales_category_idx ON sales_data(category);
```

## Dashboard Layout

### Top Row: KPI Cards
```sql
-- Card 1: Total Sales (YTD)
SELECT TO_CHAR(SUM(sales_amount), '$999,999,990') AS total_sales
FROM sales_data
WHERE EXTRACT(YEAR FROM sale_date) = EXTRACT(YEAR FROM SYSDATE)

-- Card 2: Average Order Value
SELECT TO_CHAR(AVG(sales_amount), '$999,999,990') AS avg_order
FROM sales_data
WHERE sale_date >= ADD_MONTHS(SYSDATE, -1)

-- Card 3: Total Orders (This Month)
SELECT COUNT(*) AS total_orders
FROM sales_data
WHERE sale_date >= TRUNC(SYSDATE, 'MM')

-- Card 4: Growth % (MoM)
WITH current_month AS (
    SELECT SUM(sales_amount) AS curr
    FROM sales_data
    WHERE sale_date >= TRUNC(SYSDATE, 'MM')
), prev_month AS (
    SELECT SUM(sales_amount) AS prev
    FROM sales_data
    WHERE sale_date >= ADD_MONTHS(TRUNC(SYSDATE, 'MM'), -1)
    AND sale_date < TRUNC(SYSDATE, 'MM')
)
SELECT ROUND(((curr - prev) / prev) * 100, 1) || '%' AS growth
FROM current_month, prev_month
```

### Middle Left: Sales by Region (Bar Chart)
```sql
SELECT region,
       SUM(sales_amount) AS total_sales
FROM sales_data
WHERE sale_date >= ADD_MONTHS(SYSDATE, -12)
GROUP BY region
ORDER BY total_sales DESC
```

### Middle Right: Sales Trend (Line Chart)
```sql
SELECT TO_CHAR(sale_date, 'YYYY-MM') AS month,
       SUM(sales_amount) AS monthly_sales
FROM sales_data
WHERE sale_date >= ADD_MONTHS(SYSDATE, -12)
GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
ORDER BY month
```

### Bottom Left: Top Products (Pie Chart)
```sql
SELECT product_name,
       SUM(sales_amount) AS sales
FROM sales_data
WHERE sale_date >= ADD_MONTHS(SYSDATE, -3)
GROUP BY product_name
ORDER BY sales DESC
FETCH FIRST 10 ROWS ONLY
```

### Bottom Right: Recent Orders (Interactive Report)
```sql
SELECT sale_id,
       sale_date,
       customer_name,
       product_name,
       TO_CHAR(sales_amount, '$999,999,990.00') AS amount
FROM sales_data
WHERE sale_date >= SYSDATE - 7
ORDER BY sale_date DESC
```

## Features
- Real-time KPI metrics
- Interactive charts with drill-down
- Date range filters
- Region/category filters
- Export to PDF/Excel
- Auto-refresh (every 5 minutes)
- Responsive design (mobile-friendly)

## Filters
- Date Range: P10_DATE_FROM, P10_DATE_TO
- Region: P10_REGION (multi-select)
- Category: P10_CATEGORY (multi-select)
- Dynamic Actions to refresh all regions on filter change
