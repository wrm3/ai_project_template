# Oracle APEX Interactive Grids

## Overview
Interactive Grids are powerful, editable data grids in APEX that allow users to view, edit, add, and delete records directly inline. They combine the functionality of spreadsheets with database-backed CRUD operations.

## Key Features
- Inline editing (cell-level or row-level)
- Add/Delete rows
- Sorting, filtering, searching
- Column reordering and resizing
- Aggregations (sum, average, count, etc.)
- Row selection (single or multiple)
- Master-detail relationships
- Export to CSV/Excel
- Customizable toolbars
- Responsive design
- Keyboard navigation

## Basic Interactive Grid

### Simple Read-Only Grid
```sql
-- Region: Employees
-- Type: Interactive Grid
-- Source:
SELECT emp_id,
       first_name,
       last_name,
       email,
       hire_date,
       salary,
       dept_name
FROM   emp_dept_vw
ORDER BY last_name, first_name

-- Attributes:
-- Editable: No
-- Toolbar: Show
-- Pagination: Load All Rows (if < 1000 rows)
```

### Editable Grid with DML
```sql
-- Region: Employees (Editable)
-- Type: Interactive Grid
-- Source:
SELECT emp_id,
       first_name,
       last_name,
       email,
       phone,
       hire_date,
       salary,
       dept_id
FROM   employees
WHERE  active_flag = 'Y'

-- Attributes:
-- Editable: Yes
-- Edit Mode: Row (or Cell)
-- Toolbar: Show
-- Add Row: Yes
-- Row Actions: Edit, Delete
-- Lost Update Detection: Yes

-- DML Configuration:
-- Edit Enabled: Yes
-- Add Row Enabled: Yes
-- Delete Row Enabled: Yes
-- Lost Update Type: Values
-- Primary Key Column: EMP_ID
-- Automatic Row Processing: Yes
```

## Column Configuration

### Column Types and Formatting

**Text Column**:
```yaml
Column: FIRST_NAME
Type: Text Field
Heading: First Name
Width: 150
Alignment: Start
Sortable: Yes
Required: Yes
Maximum Length: 50
```

**Number Column**:
```yaml
Column: SALARY
Type: Number Field
Heading: Salary
Width: 120
Alignment: End
Format Mask: $999,999,990.00
Sortable: Yes
Required: No
Min Value: 0
Max Value: 999999
```

**Date Column**:
```yaml
Column: HIRE_DATE
Type: Date Picker
Heading: Hire Date
Width: 120
Format Mask: MM/DD/YYYY
Sortable: Yes
Required: Yes
Min Date: 01/01/2000
Max Date: &SYSDATE.
```

**Select List Column**:
```yaml
Column: DEPT_ID
Type: Select List
Heading: Department
LOV: SELECT dept_id d, dept_name r FROM departments ORDER BY dept_name
Display Extra Values: No
Null Display Value: - Select Department -
Width: 150
Required: Yes
```

**Switch Column**:
```yaml
Column: IS_MANAGER
Type: Switch
Heading: Manager
On Label: Yes
Off Label: No
On Value: Y
Off Value: N
Width: 80
```

### Column Display Conditions

**Hide Column**:
```yaml
Column: EMP_ID
Type: Hidden
Primary Key: Yes
```

**Conditional Display**:
```yaml
Column: SALARY
Condition Type: PL/SQL Expression
PL/SQL Expression: emp_pkg.is_manager(:APP_USER)
-- Only managers can see salary
```

### Column Validation

**Built-in Validations**:
```yaml
Column: EMAIL
Validation: Must Match Regular Expression
Expression: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$
Error Message: Invalid email format
```

**PL/SQL Validation**:
```yaml
Column: SALARY
Validation Type: PL/SQL Function Body
PL/SQL Code: |
  BEGIN
      IF :SALARY IS NOT NULL AND :SALARY < 30000 THEN
          RETURN FALSE;
      END IF;
      RETURN TRUE;
  END;
Error Message: Salary must be at least $30,000
```

## Advanced Features

### Master-Detail Interactive Grids

**Master Grid (Page 10 - Departments)**:
```sql
-- Region: Departments
-- Type: Interactive Grid
-- Static ID: dept_grid
SELECT dept_id,
       dept_name,
       location,
       budget
FROM   departments

-- Primary Key: DEPT_ID
-- Editable: Yes
```

**Detail Grid (Page 10 - Employees)**:
```sql
-- Region: Employees
-- Type: Interactive Grid
-- Static ID: emp_grid
-- Master Region: Departments (dept_grid)

SELECT emp_id,
       first_name,
       last_name,
       email,
       salary,
       dept_id
FROM   employees
WHERE  dept_id = :DEPT_ID -- Bind to master grid selection

-- Master Detail Relationship:
-- Detail Column: DEPT_ID
-- Master Column: DEPT_ID
-- Editable: Yes
```

### Aggregations

**Built-in Aggregations**:
```yaml
Column: SALARY
Aggregation: Sum
Show Aggregation: Yes
Position: Footer

Available Aggregations:
  - Sum
  - Average
  - Count
  - Max
  - Min
  - Median
```

**Custom Aggregation**:
```sql
-- JavaScript in Page Properties
function customAggregation(options) {
    var total = 0;
    var count = 0;

    options.model.forEach(function(record) {
        var value = record[options.columnName];
        if (value !== null) {
            total += value;
            count++;
        }
    });

    return count > 0 ? (total / count).toFixed(2) : 0;
}

-- Apply to column
-- Aggregation Type: Custom
-- Function Name: customAggregation
```

### Conditional Formatting

**Highlight Rows**:
```javascript
// JavaScript in Page Properties - Function and Global Variable Declaration
function highlightLowSalary(config) {
    return function(cellValue, record) {
        var salary = record.SALARY;
        if (salary < 50000) {
            return "apex-low-salary";
        }
        return "";
    };
}

// CSS in Page Properties - Inline
.apex-low-salary {
    background-color: #fee;
    font-weight: bold;
}
```

**Cell Rendering**:
```javascript
// Custom cell rendering
function renderSalaryCell(cellValue, record) {
    var salary = parseFloat(cellValue);
    var color = salary > 100000 ? 'green' : 'black';
    return '<span style="color:' + color + '">' +
           apex.locale.formatNumber(salary, '$999,999,990.00') +
           '</span>';
}

// Apply to SALARY column
// Column Type: Display Only
// Column Rendering: Custom (use JavaScript)
```

### Toolbar Customization

**Add Custom Buttons**:
```javascript
// Page Properties - Execute when Page Loads
var ig$ = apex.region("emp_grid").widget();
var toolbar = ig$.interactiveGrid("getToolbar");

// Add custom button
toolbar.addButton({
    type: "BUTTON",
    label: "Export to PDF",
    icon: "fa-file-pdf-o",
    iconOnly: false,
    action: function() {
        // Custom export logic
        exportToPDF();
    }
});

// Custom export function
function exportToPDF() {
    apex.server.process(
        'EXPORT_TO_PDF',
        {
            pageItems: '#P10_DEPT_ID'
        },
        {
            success: function(data) {
                // Download PDF
                window.location = data.file_url;
            }
        }
    );
}
```

**Hide Default Buttons**:
```javascript
// Hide Add Row button
var toolbar = apex.region("emp_grid").widget()
              .interactiveGrid("getToolbar");
toolbar.hide("add-row");

// Show/Hide dynamically
if (apex.item("P10_USER_ROLE").getValue() === 'ADMIN') {
    toolbar.show("delete");
} else {
    toolbar.hide("delete");
}
```

### Row Selection

**Enable Row Selection**:
```yaml
Interactive Grid Attributes:
  Selection: Row
  Multiple Selection: Yes
  Show Row Selector: Yes
```

**Get Selected Rows**:
```javascript
// Get selected rows in JavaScript
var ig$ = apex.region("emp_grid").widget();
var grid = ig$.interactiveGrid("getViews", "grid");
var model = ig$.interactiveGrid("getViews", "grid").model;
var selectedRecords = grid.getSelectedRecords();

// Process selected rows
selectedRecords.forEach(function(record) {
    var empId = model.getValue(record, "EMP_ID");
    var firstName = model.getValue(record, "FIRST_NAME");
    console.log(empId, firstName);
});
```

**Bulk Operations on Selected Rows**:
```javascript
// Button: Delete Selected
function deleteSelected() {
    var ig$ = apex.region("emp_grid").widget();
    var grid = ig$.interactiveGrid("getViews", "grid");
    var model = ig$.interactiveGrid("getViews", "grid").model;
    var selectedRecords = grid.getSelectedRecords();

    if (selectedRecords.length === 0) {
        apex.message.alert("Please select at least one row");
        return;
    }

    apex.message.confirm("Delete " + selectedRecords.length + " rows?",
        function(ok) {
            if (ok) {
                selectedRecords.forEach(function(record) {
                    model.deleteRecords([record]);
                });
                // Save changes
                apex.region("emp_grid").widget()
                    .interactiveGrid("getActions").invoke("save");
            }
        }
    );
}
```

## Custom Validations

### Server-Side Validation

**Page-level Validation**:
```plsql
-- Validation: Check Duplicate Email
-- Type: Function Body (returning Error Text)
DECLARE
    l_count NUMBER;
BEGIN
    -- Get current grid data from session state
    FOR rec IN (
        SELECT c001 AS emp_id,
               c002 AS email
        FROM   apex_collections
        WHERE  collection_name = 'EMP_GRID_CHANGES'
    ) LOOP
        SELECT COUNT(*)
        INTO   l_count
        FROM   employees
        WHERE  email = rec.email
        AND    emp_id != NVL(rec.emp_id, -1);

        IF l_count > 0 THEN
            RETURN 'Duplicate email: ' || rec.email;
        END IF;
    END LOOP;

    RETURN NULL; -- No errors
END;
```

### Client-Side Validation

**JavaScript Validation**:
```javascript
// Page Properties - Execute when Page Loads
function setupValidation() {
    var ig$ = apex.region("emp_grid").widget();
    var model = ig$.interactiveGrid("getViews", "grid").model;

    // Add validation for email column
    model.validationRules.email = {
        type: "pattern",
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: "Invalid email format"
    };

    // Add custom validation function
    model.addValidation("salary", function(value, record) {
        if (value !== null && value < 30000) {
            return {
                type: "error",
                message: "Salary must be at least $30,000"
            };
        }
        return null;
    });
}

setupValidation();
```

## Performance Optimization

### Pagination

**Enable Pagination for Large Datasets**:
```yaml
Interactive Grid:
  Pagination Type: Page
  Rows Per Page: 100

  # Benefits:
  # - Loads only 100 rows at a time
  # - Reduces initial page load time
  # - Better for 1000+ row datasets
```

**Lazy Loading**:
```yaml
Interactive Grid:
  Lazy Loading: Yes
  Batch Size: 50

  # Loads data in batches as user scrolls
```

### SQL Query Optimization

**Use Indexed Columns**:
```sql
-- Create indexes on filter columns
CREATE INDEX emp_dept_id_idx ON employees(dept_id);
CREATE INDEX emp_last_name_idx ON employees(last_name);

-- Interactive Grid query automatically benefits
SELECT emp_id, first_name, last_name, dept_id
FROM   employees
WHERE  dept_id = :P10_DEPT_ID -- Uses index
ORDER BY last_name; -- Uses index
```

**Avoid Complex Joins in Grid**:
```sql
-- SLOW: Complex joins in Interactive Grid
SELECT e.emp_id,
       e.first_name,
       d.dept_name,
       l.city,
       c.country_name
FROM   employees e
JOIN   departments d ON e.dept_id = d.dept_id
JOIN   locations l ON d.location_id = l.location_id
JOIN   countries c ON l.country_id = c.country_id;

-- FAST: Use view instead
CREATE OR REPLACE VIEW emp_full_vw AS
SELECT e.emp_id,
       e.first_name,
       d.dept_name,
       l.city,
       c.country_name
FROM   employees e
JOIN   departments d ON e.dept_id = d.dept_id
JOIN   locations l ON d.location_id = l.location_id
JOIN   countries c ON l.country_id = c.country_id;

-- Interactive Grid
SELECT * FROM emp_full_vw;
```

### Client-Side Performance

**Minimize Column Count**:
```yaml
# Show only necessary columns
# Too many columns (20+) can slow rendering
# Hide unnecessary columns or use detail view
```

**Disable Features Not Needed**:
```yaml
# If editing not required:
Editable: No

# If filtering not used:
Toolbar: Hide

# Improves initial render time
```

## Export and Import

### Export Data

**Built-in Export**:
```yaml
Interactive Grid:
  Enable Download: CSV, HTML, PDF

  # Users can export via Actions menu
  Actions > Download > CSV
```

**Custom Export**:
```javascript
// Custom export to Excel with formatting
function exportToExcel() {
    var ig$ = apex.region("emp_grid").widget();
    var model = ig$.interactiveGrid("getViews", "grid").model;
    var data = [];

    model.forEach(function(record) {
        data.push({
            emp_id: model.getValue(record, "EMP_ID"),
            first_name: model.getValue(record, "FIRST_NAME"),
            last_name: model.getValue(record, "LAST_NAME"),
            salary: model.getValue(record, "SALARY")
        });
    });

    // Send to server for Excel generation
    apex.server.process(
        'GENERATE_EXCEL',
        {
            x01: JSON.stringify(data)
        },
        {
            success: function(response) {
                window.location = response.file_url;
            }
        }
    );
}
```

### Import Data

**Upload and Import**:
```yaml
Page Items:
  P10_FILE_UPLOAD: File Browse

Process: Import from CSV
Type: Execute Code
PL/SQL Code: |
  DECLARE
      l_file BLOB;
  BEGIN
      -- Get uploaded file
      SELECT file_content
      INTO   l_file
      FROM   apex_application_temp_files
      WHERE  name = :P10_FILE_UPLOAD;

      -- Parse CSV and insert
      emp_pkg.import_from_csv(l_file);

      -- Refresh grid
      apex_application.g_print_success_message :=
          'Data imported successfully';
  END;
```

## Common Patterns

### Pattern 1: Filter by Department
```yaml
Page Item: P10_DEPT_ID (Select List)

Interactive Grid Source:
  SELECT * FROM employees
  WHERE (:P10_DEPT_ID IS NULL OR dept_id = :P10_DEPT_ID)

Dynamic Action:
  When: Change
  Item: P10_DEPT_ID
  Action: Refresh
  Region: Employees Grid
```

### Pattern 2: Search Box
```yaml
Page Item: P10_SEARCH (Text Field)

Interactive Grid Source:
  SELECT * FROM employees
  WHERE :P10_SEARCH IS NULL
  OR UPPER(first_name || ' ' || last_name)
     LIKE '%' || UPPER(:P10_SEARCH) || '%'

Dynamic Action:
  When: Key Release
  Item: P10_SEARCH
  Action: Refresh
  Region: Employees Grid
  Wait: 500ms (debounce)
```

### Pattern 3: Computed Column
```sql
-- Interactive Grid Source
SELECT emp_id,
       first_name,
       last_name,
       hire_date,
       TRUNC(MONTHS_BETWEEN(SYSDATE, hire_date) / 12) AS tenure_years,
       salary,
       salary * 1.1 AS proposed_salary
FROM   employees

-- TENURE_YEARS and PROPOSED_SALARY are read-only computed
```

## Best Practices

### Do
- Use pagination for datasets > 1,000 rows
- Create indexes on filter/sort columns
- Use views for complex joins
- Enable Lost Update Detection
- Set appropriate column widths
- Use meaningful column headings
- Implement proper validations
- Test with realistic data volumes
- Use keyboard navigation shortcuts
- Provide clear error messages

### Don't
- Load 10,000+ rows without pagination
- Use SELECT * in production
- Allow editing without primary key
- Skip validations on user input
- Ignore performance implications
- Forget to test save operations
- Use complex calculations in SQL (use views)
- Disable Lost Update Detection in multi-user apps
- Forget to handle NULL values
- Ignore browser console errors

## Troubleshooting

### Issue: Changes Not Saving
**Solution**:
```yaml
Check:
  1. Primary Key column is set
  2. Table has primary key constraint
  3. User has UPDATE privilege on table
  4. Lost Update Detection is configured
  5. No validation errors
  6. Session state protection not blocking

Debug:
  - Enable Debug mode (&DEBUG=YES)
  - Check Developer Console for errors
  - Review DML process execution
```

### Issue: Slow Performance
**Solution**:
```yaml
Optimize:
  1. Enable pagination (Page, not Load All)
  2. Add indexes on sort/filter columns
  3. Simplify SQL query (use views)
  4. Reduce column count
  5. Disable unnecessary features
  6. Use WHERE clause to filter data
  7. Check execution plan (EXPLAIN PLAN)
```

---

**Summary**: Interactive Grids are powerful components for editable data management. Configure appropriately, optimize queries, and implement proper validations for the best user experience.
