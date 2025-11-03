# Oracle APEX Development Rules

## Overview
Best practices and standards for Oracle Application Express (APEX) low-code development. These rules ensure consistency, security, performance, and maintainability across APEX applications.

## Naming Conventions

### Application Items
```yaml
Format: AI_{NAME}
Examples:
  - AI_COMPANY_NAME
  - AI_FISCAL_YEAR
  - AI_USER_ROLE
  - AI_THEME_PREFERENCE

Purpose: Global variables accessible across all pages
Convention: ALL_CAPS with AI_ prefix
```

### Page Items
```yaml
Format: P{PAGE_NUM}_{NAME}
Examples:
  - P10_EMP_ID
  - P10_FIRST_NAME
  - P20_DEPT_ID
  - P30_SEARCH_TERM

Purpose: Page-specific items
Convention: Page number + underscore + ALL_CAPS name
```

### Regions
```yaml
Format: Descriptive Name (Title Case)
Examples:
  - Employees
  - Department Details
  - Sales by Region
  - Search Criteria

Convention: Clear, concise, title case
```

### Buttons
```yaml
Format: ACTION_NAME (ALL_CAPS)
Examples:
  - CREATE
  - SAVE
  - CANCEL
  - DELETE
  - SEARCH
  - EXPORT
  - REFRESH

Convention: Action verb in ALL_CAPS
```

### Processes
```yaml
Format: Descriptive Action (Title Case)
Examples:
  - Create Employee
  - Update Salary
  - Send Email Notification
  - Validate Duplicate
  - Close Dialog

Convention: Verb + Object in title case
```

### Validations
```yaml
Format: Item/Field Description
Examples:
  - P10_EMAIL is Valid
  - P10_SALARY is Positive
  - P10_NAME is Not Duplicate
  - Department has Manager

Convention: Descriptive statement
```

## SQL Standards for APEX

### Always Use Bind Variables
```sql
-- CORRECT: Use bind variables (prevents SQL injection)
SELECT * FROM employees
WHERE dept_id = :P10_DEPT_ID
AND hire_date >= :P10_DATE_FROM

-- WRONG: String concatenation (SQL injection risk)
SELECT * FROM employees
WHERE dept_id = ''' || :P10_DEPT_ID || '''
```

### Explicit Column Names
```sql
-- CORRECT: Explicit columns
SELECT emp_id, first_name, last_name, email, salary
FROM employees

-- WRONG: SELECT * (performance and maintenance issues)
SELECT * FROM employees
```

### Use Table Aliases
```sql
-- CORRECT: Readable with aliases
SELECT e.emp_id,
       e.first_name,
       d.dept_name,
       l.city
FROM   employees e
JOIN   departments d ON e.dept_id = d.dept_id
JOIN   locations l ON d.location_id = l.location_id

-- WRONG: No aliases (hard to read)
SELECT employees.emp_id, employees.first_name
FROM employees
JOIN departments ON employees.dept_id = departments.dept_id
```

### Format for Readability
```sql
-- CORRECT: Well-formatted
SELECT e.emp_id,
       e.first_name,
       e.last_name,
       d.dept_name,
       TO_CHAR(e.salary, '$999,999,990.00') AS formatted_salary
FROM   employees e
JOIN   departments d ON e.dept_id = d.dept_id
WHERE  e.active_flag = 'Y'
AND    e.hire_date >= ADD_MONTHS(SYSDATE, -12)
ORDER BY e.last_name, e.first_name;

-- WRONG: Unformatted (hard to read)
SELECT e.emp_id,e.first_name,e.last_name FROM employees e WHERE e.active_flag='Y';
```

## PL/SQL Standards

### Encapsulate Business Logic
```plsql
-- CORRECT: Business logic in package
CREATE OR REPLACE PACKAGE emp_mgmt_pkg AS
    PROCEDURE create_employee(...);
    PROCEDURE update_salary(...);
    FUNCTION is_manager(p_username VARCHAR2) RETURN BOOLEAN;
END emp_mgmt_pkg;
/

-- Call from APEX
BEGIN
    emp_mgmt_pkg.create_employee(...);
END;

-- WRONG: Complex logic directly in APEX process
-- Maintenance nightmare, code duplication
```

### Use Constants
```plsql
-- CORRECT: Define constants
CREATE OR REPLACE PACKAGE BODY emp_mgmt_pkg AS
    c_max_salary CONSTANT NUMBER := 500000;
    c_min_salary CONSTANT NUMBER := 30000;

    PROCEDURE validate_salary(p_salary NUMBER) IS
    BEGIN
        IF p_salary < c_min_salary THEN
            raise_application_error(-20001,
                'Salary must be at least ' || c_min_salary);
        END IF;
    END;
END;
/

-- WRONG: Magic numbers scattered in code
IF p_salary < 30000 THEN ...
```

### Error Handling
```plsql
-- CORRECT: Comprehensive error handling
BEGIN
    -- Validation
    IF :P20_SALARY < 0 THEN
        apex_error.add_error(
            p_message => 'Salary must be positive',
            p_display_location => apex_error.c_inline_with_field,
            p_page_item_name => 'P20_SALARY'
        );
        RETURN;
    END IF;

    -- Business logic
    emp_mgmt_pkg.create_employee(...);

    -- Success message
    apex_application.g_print_success_message :=
        'Employee created successfully';

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        apex_debug.error('Error: %s', SQLERRM);
        apex_error.add_error(
            p_message => 'System error. Please contact support.',
            p_display_location => apex_error.c_inline_in_notification
        );
        ROLLBACK;
END;
```

## Security Standards

### SQL Injection Prevention
```sql
-- ALWAYS use bind variables
-- NEVER concatenate user input into SQL

-- CORRECT
WHERE last_name = :P10_SEARCH

-- WRONG
WHERE last_name = ''' || :P10_SEARCH || '''
```

### Authorization Checks
```yaml
Apply authorization to:
  - Sensitive pages (Admin, HR, Finance)
  - Delete buttons
  - Salary/compensation fields
  - Reports with sensitive data

Authorization Scheme Examples:
  - Is Administrator
  - Is Manager
  - Is HR Personnel
  - Is Employee Owner
```

### Session State Protection
```yaml
Enable Session State Protection:
  Application Level: Restricted
  Page Level: Arguments Must Have Checksum

Protects against:
  - URL tampering
  - Unauthorized item modifications
  - Session hijacking attempts
```

### Input Validation
```yaml
Validate ALL user inputs:
  - Required fields
  - Format validation (email, phone, date)
  - Range validation (min/max values)
  - Business rule validation
  - Duplicate checks

Example Validations:
  - Email Format: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$
  - Phone Format: ^\(\d{3}\) \d{3}-\d{4}$
  - Positive Numbers: value > 0
  - Date Range: between valid dates
```

## Performance Standards

### Query Optimization
```sql
-- Create indexes on:
-- - Primary keys (automatic)
-- - Foreign keys
-- - WHERE clause columns
-- - ORDER BY columns
-- - JOIN columns

CREATE INDEX emp_dept_id_idx ON employees(dept_id);
CREATE INDEX emp_last_name_idx ON employees(last_name);
CREATE INDEX emp_hire_date_idx ON employees(hire_date);

-- Composite indexes for common queries
CREATE INDEX emp_dept_status_idx ON employees(dept_id, active_flag);
```

### Pagination
```yaml
For datasets > 1,000 rows:
  Interactive Grid:
    Pagination: Page (not Load All)
    Rows Per Page: 100

  Interactive Report:
    Row Ranges: 15
    Pagination: Row Ranges X to Y
```

### Caching
```yaml
Use caching for:
  - Static reference data (countries, states)
  - Infrequently changing data (departments)
  - Public pages (no personalization)

Cache Settings:
  - Cache Timeout: 5-60 minutes (depends on data volatility)
  - Cache By User: No (for shared data)
  - Cache By User: Yes (for personalized data)
```

### Session State
```yaml
Best Practices:
  - Clear session state when not needed
  - Don't store large objects in session state
  - Use collections for temporary data (like temp tables)
  - Clear cache after processing: apex_util.clear_page_cache(10)
```

## Testing Standards

### Unit Testing
```yaml
Test ALL of:
  - Form submissions (insert, update, delete)
  - Validations (all validation rules)
  - Authorization schemes (access control)
  - PL/SQL packages (business logic)
  - Error handling (various error scenarios)
```

### Integration Testing
```yaml
Test complete workflows:
  - User registration and login
  - CRUD operations end-to-end
  - Multi-page processes (wizards)
  - Master-detail relationships
  - REST API integrations
```

### Performance Testing
```yaml
Load Test with:
  - 100+ concurrent users
  - Realistic data volumes (1M+ rows)
  - Long-running processes
  - Peak usage scenarios

Measure:
  - Page load times (< 3 seconds)
  - Query execution times
  - Transaction throughput
  - Memory usage
```

### Security Testing
```yaml
Test for:
  - SQL injection attempts
  - XSS vulnerabilities
  - Authorization bypasses
  - Session hijacking
  - CSRF attacks

Tools:
  - APEX Advisor (built-in)
  - Manual penetration testing
  - OWASP security testing
```

## Deployment Standards

### Version Control
```yaml
Commit to Git:
  - Export APEX application after changes
  - Commit with meaningful message
  - Tag releases (v1.0.0, v1.1.0, etc.)
  - Branch for features/fixes

Example:
  git add f100.sql
  git commit -m "feat: Add employee search functionality"
  git tag v1.2.0
  git push origin main --tags
```

### Deployment Process
```yaml
1. Export from development
2. Test in staging environment
3. Run smoke tests
4. Deploy to production (during maintenance window)
5. Run smoke tests in production
6. Monitor for errors
7. Rollback plan ready

Never deploy directly to production without testing!
```

### Database Changes
```yaml
For schema changes:
  1. Create migration script
  2. Test in development
  3. Create rollback script
  4. Test rollback
  5. Document changes
  6. Deploy to staging
  7. Test thoroughly
  8. Deploy to production
  9. Verify success
```

## Documentation Standards

### Code Comments
```plsql
-- CORRECT: Meaningful comments
-- Calculate employee tenure in years
l_tenure := TRUNC(MONTHS_BETWEEN(SYSDATE, l_hire_date) / 12);

-- WRONG: Obvious or no comments
l_tenure := TRUNC(MONTHS_BETWEEN(SYSDATE, l_hire_date) / 12); -- calculate tenure
```

### Page Documentation
```yaml
Document complex pages:
  - Purpose of page
  - Items and their purpose
  - Validations and why
  - Processes execution order
  - Dynamic actions behavior
  - Special considerations

Use page comments or external documentation
```

### API Documentation
```yaml
For REST APIs, document:
  - Endpoints
  - Methods (GET, POST, PUT, DELETE)
  - Parameters
  - Request body format
  - Response format
  - Error codes
  - Authentication requirements
  - Rate limits
```

## Code Review Checklist

### Security
- [ ] All SQL uses bind variables
- [ ] Authorization applied to sensitive pages/items
- [ ] Session State Protection enabled
- [ ] Input validation implemented
- [ ] XSS prevention (output escaping)
- [ ] HTTPS enforced

### Performance
- [ ] Indexes on filter/sort columns
- [ ] Pagination for large datasets
- [ ] Caching used appropriately
- [ ] Queries optimized (EXPLAIN PLAN)
- [ ] Session state minimized

### Code Quality
- [ ] Business logic in PL/SQL packages
- [ ] Consistent naming conventions
- [ ] Error handling implemented
- [ ] Code commented appropriately
- [ ] No duplicate code
- [ ] Follows DRY principle

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Performance acceptable
- [ ] Security tested
- [ ] Browser compatibility verified

### Documentation
- [ ] Code commented
- [ ] Complex logic documented
- [ ] API documented
- [ ] Deployment procedure documented

---

**Summary**: Follow these rules consistently to build secure, performant, and maintainable APEX applications. Use code reviews to enforce standards and share knowledge across the team.
