# Oracle APEX Forms and Reports

## Forms Development

### Basic Form Pattern
```sql
-- Form Region on EMPLOYEES table
-- Type: Form
-- Source: Table EMPLOYEES
-- Primary Key: EMP_ID

Items:
- P20_EMP_ID (Hidden, Primary Key)
- P20_FIRST_NAME (Text Field, Required)
- P20_LAST_NAME (Text Field, Required)
- P20_EMAIL (Text Field, Required, Email validation)
- P20_SALARY (Number Field, Format: $999,999,990.00)
- P20_DEPT_ID (Select List, LOV from departments)
```

### Master-Detail Forms
```yaml
Master Form (Page 10):
  Table: DEPARTMENTS
  Primary Key: DEPT_ID
  Items: P10_DEPT_ID, P10_DEPT_NAME, P10_BUDGET

Detail Region (Page 10):
  Type: Interactive Grid
  Source: SELECT * FROM employees WHERE dept_id = :P10_DEPT_ID
  Master-Detail Relationship: DEPT_ID
```

### Form Validations
```plsql
-- Validation: Email Must Be Unique
SELECT COUNT(*)
FROM   employees
WHERE  email = :P20_EMAIL
AND    emp_id != NVL(:P20_EMP_ID, -1)
HAVING COUNT(*) > 0

-- Error Message: Email already exists
```

### Dynamic LOVs (Cascade)
```yaml
Dynamic Action: Change Department
When: Change
Item: P20_DEPT_ID

Action: Set Value
  SQL Query: SELECT manager_id FROM departments WHERE dept_id = :P20_DEPT_ID
  Items to Submit: P20_DEPT_ID
  Affected Elements: P20_MANAGER_ID
```

## Reports Development

### Interactive Report
```sql
-- Region: Employee Report
-- Type: Interactive Report
SELECT emp_id,
       first_name || ' ' || last_name AS full_name,
       email,
       dept_name,
       TO_CHAR(hire_date, 'MM/DD/YYYY') AS hire_date,
       TO_CHAR(salary, '$999,999,990.00') AS salary
FROM   emp_dept_vw
WHERE  active_flag = 'Y'

-- Features:
-- Search: Yes
-- Filter: Yes
-- Sort: Yes
-- Break: Yes
-- Highlight: Yes
-- Download: CSV, HTML, PDF
-- Subscription: Yes
```

### Classic Report with Links
```sql
SELECT emp_id,
       first_name,
       last_name,
       email,
       APEX_PAGE.GET_URL(
           p_page => 20,
           p_items => 'P20_EMP_ID',
           p_values => emp_id
       ) AS edit_link,
       '<a href="javascript:confirmDelete(' || emp_id || ')">Delete</a>' AS delete_link
FROM   employees
```

### Report with Conditional Formatting
```sql
-- Column: SALARY
-- Conditional Highlighting
Condition Type: PL/SQL Expression
Expression: #SALARY# > 100000
CSS Class: highlight-high-salary

-- CSS:
.highlight-high-salary {
    background-color: #90ee90;
    font-weight: bold;
}
```

### Drill-Down Reports
```yaml
Level 1 Report (Departments):
  SELECT dept_id, dept_name, COUNT(*) emp_count
  FROM employees
  GROUP BY dept_id, dept_name

  Link Column: DEPT_NAME
  Target: Page 20 (Employee Detail)
  Set Items: P20_DEPT_ID = #DEPT_ID#

Level 2 Report (Employees in Department):
  SELECT * FROM employees WHERE dept_id = :P20_DEPT_ID
```

## Form Patterns

### Pattern 1: Wizard Form
```yaml
Page 30 (Step 1): Basic Information
  Items: First Name, Last Name, Email

Page 31 (Step 2): Employment Details
  Items: Hire Date, Department, Salary

Page 32 (Step 3): Review and Confirm
  Display all entered information

Page 33 (Step 4): Completion
  Process: Insert into database
  Message: Employee created successfully
```

### Pattern 2: Inline Edit Form
```yaml
Report with Inline Edit:
  Region: Employees (Interactive Report)
  
  Edit Link:
    Type: Link to custom target
    Target: javascript:editEmployee(#EMP_ID#)
  
  JavaScript Function:
    function editEmployee(empId) {
        apex.item('P10_EMP_ID').setValue(empId);
        apex.region('emp_form').refresh();
    }
  
  Form Region (same page):
    Source: SELECT * FROM employees WHERE emp_id = :P10_EMP_ID
```

### Pattern 3: Modal Dialog Form
```yaml
Report Page (Page 10):
  Button: Add Employee
  Target:
    Type: Page in this Application
    Page: 20 (Employee Form)
    Clear Cache: 20
  Open As: Modal Dialog

Form Page (Page 20):
  Modal Dialog: Yes
  Width: 600px
  
  Buttons:
    - CREATE/SAVE (Database Action: Submit)
    - CANCEL (Action: Cancel Dialog)
  
  Process: Form - Automatic Row Processing (DML)
  
  Branch: Close Dialog (After Processing)
  Success Message: Employee saved successfully
```

## Report Patterns

### Pattern 1: Search and Filter Report
```sql
-- Page Items for Filters
P30_SEARCH_NAME (Text Field)
P30_DEPT_ID (Select List)
P30_DATE_FROM (Date Picker)
P30_DATE_TO (Date Picker)

-- Report Source
SELECT *
FROM   employees
WHERE  (:P30_SEARCH_NAME IS NULL OR
        UPPER(first_name || ' ' || last_name) LIKE '%' || UPPER(:P30_SEARCH_NAME) || '%')
AND    (:P30_DEPT_ID IS NULL OR dept_id = :P30_DEPT_ID)
AND    (:P30_DATE_FROM IS NULL OR hire_date >= :P30_DATE_FROM)
AND    (:P30_DATE_TO IS NULL OR hire_date <= :P30_DATE_TO)
```

### Pattern 2: Report with Aggregates
```sql
-- Interactive Report with Break and Aggregates
SELECT dept_name,
       first_name,
       last_name,
       salary
FROM   emp_dept_vw
ORDER BY dept_name, last_name

-- Configure:
-- Control Break: DEPT_NAME
-- Aggregate: SUM(SALARY) on Break
-- Show: Total rows per department
```

### Pattern 3: Faceted Search Report
```yaml
Region Type: Faceted Search
Facets:
  - Department (Checkbox Group)
  - Hire Date Range (Date Range)
  - Salary Range (Range)

Target Region: Employee Report (Interactive Report)

Report dynamically filters based on facet selections
```

## Best Practices

### Forms
1. Use Automatic Row Processing (DML) when possible
2. Implement proper validations (client and server)
3. Use LOVs instead of free text where applicable
4. Provide clear labels and help text
5. Use modal dialogs for focused data entry
6. Implement lost update detection
7. Clear cache on form load (Clear Cache: form_page)
8. Show success messages after save
9. Handle errors gracefully
10. Use consistent button labels (CREATE, SAVE, CANCEL, DELETE)

### Reports
1. Use Interactive Reports for user flexibility
2. Implement pagination for large datasets
3. Provide meaningful column headings
4. Use proper formatting (dates, numbers, currency)
5. Enable download capabilities (CSV, PDF)
6. Use conditional formatting for insights
7. Implement search and filter options
8. Create drill-down for detail navigation
9. Show aggregates where appropriate
10. Test with realistic data volumes

---

**Summary**: Forms and Reports are foundational APEX components. Use patterns appropriate for your use case, implement proper validations, and optimize for performance.
