# Oracle APEX Performance Tuning

## SQL Optimization

### Use Indexes
```sql
-- Create indexes on filter columns
CREATE INDEX emp_dept_id_idx ON employees(dept_id);
CREATE INDEX emp_last_name_idx ON employees(last_name);
CREATE INDEX emp_hire_date_idx ON employees(hire_date);

-- Composite index for common queries
CREATE INDEX emp_dept_status_idx ON employees(dept_id, active_flag);
```

### Query Optimization
```sql
-- SLOW: Function in WHERE clause
SELECT * FROM employees
WHERE UPPER(last_name) = :P10_SEARCH;

-- FAST: Function-based index or computed column
CREATE INDEX emp_last_name_upper_idx ON employees(UPPER(last_name));
-- OR
ALTER TABLE employees ADD last_name_upper AS (UPPER(last_name));
CREATE INDEX emp_last_name_upper_idx ON employees(last_name_upper);
```

### Use Result Cache
```sql
CREATE OR REPLACE FUNCTION get_dept_name(p_dept_id NUMBER)
RETURN VARCHAR2
RESULT_CACHE
IS
    l_dept_name VARCHAR2(100);
BEGIN
    SELECT dept_name INTO l_dept_name
    FROM departments
    WHERE dept_id = p_dept_id;
    RETURN l_dept_name;
END;
/
```

## Caching Strategies

### Page Cache
```yaml
Page Cache:
  Cache: Yes
  Cache By User: No
  Timeout: 15 minutes
  
-- Use for static/semi-static pages
```

### Region Cache
```yaml
Region Cache:
  Cache: Yes
  Cache By User: Yes
  Cache Timeout: 5 minutes
  
-- Use for personalized but cacheable content
```

### Query Result Cache
```sql
SELECT /*+ result_cache */ dept_id, dept_name
FROM departments;
```

## Session State Management

### Clear Unnecessary State
```plsql
-- Clear after processing
apex_util.clear_page_cache(10);

-- Clear specific items
apex_util.set_session_state('P10_TEMP_VALUE', NULL);
```

### Minimize Session State
```yaml
-- Use Display Only items when possible
-- Don't store computed values in session state
-- Calculate on-demand instead
```

## Application Tuning

### Pagination
```yaml
Interactive Grid/Report:
  Pagination: Page (not Load All)
  Rows Per Page: 100
  
-- Don't load 10,000 rows without pagination
```

### Lazy Loading
```yaml
Interactive Grid:
  Lazy Loading: Yes
  Load on Scroll: Yes
```

### Minimize Network Round-trips
```yaml
Dynamic Actions:
  Wait: 500ms (debounce)
  Fire On: Key Release
  
-- Prevents excessive AJAX calls
```

## Monitoring

### Check Performance
```sql
-- Page view statistics
SELECT application_id,
       page_id,
       AVG(elapsed_time) AS avg_ms,
       MAX(elapsed_time) AS max_ms,
       COUNT(*) AS views
FROM apex_workspace_activity_log
WHERE time_stamp > SYSDATE - 1
GROUP BY application_id, page_id
ORDER BY avg_ms DESC;

-- Slow queries
SELECT sql_text,
       elapsed_time,
       executions,
       buffer_gets
FROM v$sql
WHERE parsing_schema_name = 'MYSCHEMA'
ORDER BY elapsed_time DESC;
```

---

**Summary**: Optimize SQL queries with indexes, use caching appropriately, minimize session state, implement pagination, and monitor performance regularly.
