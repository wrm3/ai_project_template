# Oracle APEX Charts and Visualizations

## Chart Types

### Bar Chart
```sql
-- Horizontal Bar Chart - Sales by Region
SELECT region,
       SUM(sales_amount) AS total_sales
FROM   sales_data
WHERE  sale_date >= ADD_MONTHS(SYSDATE, -12)
GROUP BY region
ORDER BY total_sales DESC

-- Chart Configuration:
-- Type: Bar
-- Orientation: Horizontal
-- Label: REGION
-- Value: TOTAL_SALES
-- Format: $999,999,990
-- Color Scheme: Modern
```

### Line Chart
```sql
-- Line Chart - Sales Trend Over Time
SELECT TO_CHAR(sale_date, 'YYYY-MM') AS month,
       SUM(sales_amount) AS monthly_sales
FROM   sales_data
WHERE  sale_date >= ADD_MONTHS(SYSDATE, -12)
GROUP BY TO_CHAR(sale_date, 'YYYY-MM')
ORDER BY month

-- Chart Configuration:
-- Type: Line
-- Label: MONTH
-- Value: MONTHLY_SALES
-- Show Data Points: Yes
-- Smooth Lines: Yes
```

### Pie Chart
```sql
-- Pie Chart - Market Share by Product
SELECT product_name,
       SUM(sales_amount) AS sales
FROM   product_sales_vw
WHERE  sale_year = TO_CHAR(SYSDATE, 'YYYY')
GROUP BY product_name
ORDER BY sales DESC

-- Chart Configuration:
-- Type: Pie
-- Label: PRODUCT_NAME
-- Value: SALES
-- Show Values: Yes (percentage)
-- Show Legend: Yes
```

### Combination Chart
```sql
-- Combination Chart - Revenue and Profit
SELECT month_name,
       revenue,
       profit,
       target
FROM   monthly_financials
WHERE  fiscal_year = :P10_FISCAL_YEAR
ORDER BY month_num

-- Chart Configuration:
-- Type: Combination
-- Series 1: REVENUE (Bar)
-- Series 2: PROFIT (Bar)
-- Series 3: TARGET (Line)
```

### Gauge Chart
```sql
-- Gauge Chart - Sales Target Achievement
SELECT ROUND((actual_sales / target_sales) * 100, 1) AS achievement_pct,
       target_sales,
       actual_sales
FROM   sales_summary
WHERE  quarter = :P10_QUARTER

-- Chart Configuration:
-- Type: Gauge
-- Value: ACHIEVEMENT_PCT
-- Minimum: 0
-- Maximum: 150
-- Threshold Regions:
--   0-75: Red
--   75-90: Yellow
--   90-150: Green
```

## Advanced Visualizations

### Gantt Chart
```sql
-- Project Timeline
SELECT task_name,
       resource_name,
       start_date,
       end_date,
       CASE status
           WHEN 'COMPLETE' THEN 'green'
           WHEN 'IN_PROGRESS' THEN 'blue'
           ELSE 'gray'
       END AS bar_color
FROM   project_tasks
WHERE  project_id = :P10_PROJECT_ID
ORDER BY start_date

-- Chart Configuration:
-- Type: Gantt
-- Task: TASK_NAME
-- Resource: RESOURCE_NAME
-- Start Date: START_DATE
-- End Date: END_DATE
-- Color: BAR_COLOR
```

### Map Chart
```sql
-- Geographic Sales Map
SELECT country_code,
       country_name,
       SUM(sales_amount) AS total_sales
FROM   sales_by_country_vw
WHERE  sale_year = TO_CHAR(SYSDATE, 'YYYY')
GROUP BY country_code, country_name

-- Chart Configuration:
-- Type: Map
-- Region: Country (based on country_code)
-- Value: TOTAL_SALES
-- Color Scale: Quantile
-- Tooltip: COUNTRY_NAME, TOTAL_SALES
```

### Timeline Chart
```sql
-- Event Timeline
SELECT event_name,
       event_date,
       event_type,
       description
FROM   company_events
WHERE  event_date BETWEEN :P10_START_DATE AND :P10_END_DATE
ORDER BY event_date

-- Chart Configuration:
-- Type: Timeline
-- Label: EVENT_NAME
-- Date: EVENT_DATE
-- Category: EVENT_TYPE
```

## Chart Features

### Interactive Features
```yaml
Enable Interactive Features:
  - Drill Down: Yes (navigate to detail page)
  - Tooltips: Yes (show on hover)
  - Legend: Yes (filter by clicking)
  - Zoom: Yes (for large datasets)
  - Pan: Yes (for scrolling)
  - Export: Image (PNG), PDF
```

### Drill-Down Navigation
```sql
-- Chart with Drill-Down Link
SELECT region,
       SUM(sales_amount) AS total_sales
FROM   sales_data
GROUP BY region

-- Chart Link:
-- Target: Page 20 (Region Detail)
-- Set Items: P20_REGION = &REGION.
-- Link Text: #REGION# - #TOTAL_SALES#
```

### Custom Tooltips
```javascript
// Custom tooltip formatting
function chartTooltip() {
    return {
        renderer: function(context) {
            return {
                insert: context.id + ': $' +
                        apex.locale.formatNumber(context.value, '999,999,990') +
                        '<br>Click for details'
            };
        }
    };
}
```

## Dashboard Design

### Multi-Chart Dashboard
```yaml
Dashboard Page Layout:
  Region 1 (Top Left): KPI Cards (4 cards)
    - Total Revenue
    - Total Customers
    - Avg Order Value
    - Growth %

  Region 2 (Top Right): Gauge Charts (3 gauges)
    - Sales Target Achievement
    - Customer Satisfaction
    - On-Time Delivery

  Region 3 (Middle Left): Line Chart
    - Monthly Sales Trend

  Region 4 (Middle Right): Pie Chart
    - Sales by Product Category

  Region 5 (Bottom): Interactive Report
    - Top 10 Customers
```

### Responsive Design
```yaml
Grid Layout:
  - Desktop: 4 columns
  - Tablet: 2 columns
  - Mobile: 1 column

Chart Responsiveness:
  - Auto-resize: Yes
  - Min Height: 300px
  - Max Height: 600px
```

## Performance Optimization

### Optimize Queries
```sql
-- SLOW: Suboptimal query
SELECT region,
       (SELECT SUM(amount) FROM orders WHERE region = r.name) AS sales
FROM   regions r

-- FAST: Optimized with join
SELECT r.region,
       COALESCE(SUM(o.amount), 0) AS sales
FROM   regions r
LEFT JOIN orders o ON r.name = o.region
GROUP BY r.region
```

### Caching
```yaml
Chart Region Caching:
  Cache: Yes
  Cache By User: No (same data for all users)
  Cache Timeout: 15 minutes

-- For static/semi-static data
-- Reduces database queries
```

### Pagination
```yaml
For large datasets:
  Chart Pagination: Yes
  Rows to Display: 20
  Show All Option: Yes

-- Shows top 20 items by default
-- Option to view all
```

## Best Practices

### Chart Selection
- **Bar/Column**: Compare categories
- **Line**: Show trends over time
- **Pie**: Show proportions (max 7 slices)
- **Gauge**: Show KPI vs target
- **Map**: Geographic distribution
- **Gantt**: Project timelines

### Design Principles
1. Choose appropriate chart type
2. Use consistent color schemes
3. Provide clear titles and labels
4. Show meaningful tooltips
5. Enable drill-down for details
6. Optimize queries for performance
7. Test with realistic data volumes
8. Consider mobile responsiveness
9. Use legends appropriately
10. Export capabilities when needed

---

**Summary**: Choose the right chart type for your data, optimize queries, and design for interactivity to create compelling visualizations.
