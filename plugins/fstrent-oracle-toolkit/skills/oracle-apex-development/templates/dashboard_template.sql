-- Dashboard Template with Charts and KPIs

-- KPI Queries
-- Card 1: Total Records
SELECT COUNT(*) AS total FROM {TABLE_NAME}

-- Card 2: Active Records
SELECT COUNT(*) AS active FROM {TABLE_NAME} WHERE status = 'ACTIVE'

-- Card 3: Growth This Month
SELECT COUNT(*) AS new_this_month 
FROM {TABLE_NAME} 
WHERE created_date >= TRUNC(SYSDATE, 'MM')

-- Bar Chart: Records by Status
SELECT status, COUNT(*) AS count
FROM {TABLE_NAME}
GROUP BY status

-- Line Chart: Trend Over Time
SELECT TRUNC(created_date) AS date, COUNT(*) AS daily_count
FROM {TABLE_NAME}
WHERE created_date >= ADD_MONTHS(SYSDATE, -3)
GROUP BY TRUNC(created_date)
ORDER BY date

-- Pie Chart: Distribution
SELECT category, COUNT(*) AS count
FROM {TABLE_NAME}
GROUP BY category
