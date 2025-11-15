# Oracle APEX Development Skill

## Overview
Comprehensive guidance for Oracle Application Express (APEX) low-code development. This skill provides patterns, templates, and best practices for building enterprise web applications rapidly using declarative programming, PL/SQL integration, and the Oracle database.

Oracle APEX enables developers to build scalable, secure, data-driven applications with minimal code, leveraging the power of the Oracle database and SQL/PL/SQL.

## When to Use This Skill

### Automatic Activation Triggers
This skill should be invoked when the user mentions:
- "APEX application"
- "Oracle APEX"
- "low-code application"
- "Interactive Grid"
- "Interactive Report"
- "APEX form"
- "APEX dashboard"
- "APEX REST"
- "APEX authentication"
- "APEX deployment"

### Use Cases
- Building database-centric web applications
- Creating data entry forms with validation
- Developing interactive reports and dashboards
- Implementing CRUD (Create, Read, Update, Delete) operations
- Integrating REST APIs with Oracle database
- Modernizing legacy applications
- Building internal business applications
- Creating data visualization and analytics tools
- Implementing user authentication and authorization
- Rapid prototyping and MVPs

### When NOT to Use
- Building mobile-first native applications (use APEX PWA or native development)
- Applications requiring complex real-time interactions (consider WebSocket frameworks)
- Microservices architecture without Oracle database
- Applications without database backend
- Pure static websites (use static site generators)

## Integration with SubAgents

### Primary SubAgent: oracle-apex-specialist
The **oracle-apex-specialist** SubAgent (Claude Opus) is the primary agent for APEX development:
- Handles complex application architecture
- Designs security and authentication schemes
- Optimizes performance for enterprise scale
- Creates custom plugins and components

**When to delegate to oracle-apex-specialist**:
- Multi-page application development
- Complex business logic requiring PL/SQL packages
- Authentication/authorization implementation
- Performance optimization for large datasets
- REST API integration design
- Migration from legacy systems

### Secondary SubAgent: database-expert
The **database-expert** SubAgent collaborates on database aspects:
- Schema design and normalization
- SQL query optimization
- Index strategy
- PL/SQL package development
- Database security

**When to delegate to database-expert**:
- Complex SQL queries with joins and subqueries
- PL/SQL package design for business logic
- Performance tuning for slow queries
- Database schema changes
- Partitioning and indexing strategies

### Supporting SubAgents

**security-auditor**:
- Review APEX applications for security vulnerabilities
- Test for SQL injection and XSS
- Validate authentication schemes
- Review authorization implementations

**devops-engineer**:
- Set up CI/CD pipelines for APEX deployments
- Configure environments (dev, test, prod)
- Implement backup and recovery
- Monitor application performance

**technical-writer**:
- Create user documentation
- Write API documentation
- Document deployment procedures
- Create training materials

## Integration with Other Skills

### hanx-database-tools
The **hanx-database-tools** skill provides complementary database capabilities:
- Oracle database connection management
- SQL execution and query optimization
- Database schema inspection
- PL/SQL testing and debugging

**Usage Pattern**:
```yaml
1. Use hanx-database-tools to:
   - Connect to Oracle database
   - Create schema (tables, views, sequences)
   - Test PL/SQL packages
   - Optimize SQL queries

2. Use oracle-apex-development to:
   - Build APEX application on schema
   - Create interactive grids and reports
   - Implement authentication
   - Deploy application
```

### web-tools
For testing and monitoring APEX applications:
- Test APEX REST APIs
- Scrape data for migration
- Monitor application endpoints
- Validate OAuth integrations

## APEX Development Workflow

### Phase 1: Planning and Design
```yaml
1. Requirements Gathering:
   - Identify user personas
   - Define functional requirements
   - List data entities and relationships
   - Determine security requirements
   - Estimate data volumes and user load

2. Database Design:
   - Design normalized schema (3NF)
   - Create ER diagram
   - Define primary keys (use sequences)
   - Plan foreign key relationships
   - Design views for complex queries

3. Application Structure:
   - Plan page hierarchy
   - Design navigation flow
   - Identify shared components
   - Define authentication scheme
   - Plan authorization schemes

4. UI/UX Design:
   - Sketch page layouts
   - Select APEX theme (Universal Theme)
   - Design responsive layouts
   - Plan interactive features
   - Consider accessibility (WCAG)
```

### Phase 2: Database Implementation
```sql
-- Step 1: Create sequences
CREATE SEQUENCE emp_seq START WITH 1000 INCREMENT BY 1;

-- Step 2: Create tables
CREATE TABLE employees (
    emp_id         NUMBER PRIMARY KEY,
    first_name     VARCHAR2(50) NOT NULL,
    last_name      VARCHAR2(50) NOT NULL,
    email          VARCHAR2(100) UNIQUE NOT NULL,
    phone          VARCHAR2(20),
    hire_date      DATE NOT NULL,
    salary         NUMBER(10,2),
    dept_id        NUMBER,
    is_manager     VARCHAR2(1) DEFAULT 'N',
    active_flag    VARCHAR2(1) DEFAULT 'Y',
    created_by     VARCHAR2(50) NOT NULL,
    created_date   DATE NOT NULL,
    updated_by     VARCHAR2(50),
    updated_date   DATE,
    CONSTRAINT emp_dept_fk FOREIGN KEY (dept_id)
        REFERENCES departments(dept_id),
    CONSTRAINT emp_email_chk CHECK (email LIKE '%@%.%'),
    CONSTRAINT emp_active_chk CHECK (active_flag IN ('Y','N')),
    CONSTRAINT emp_is_mgr_chk CHECK (is_manager IN ('Y','N'))
);

-- Step 3: Create indexes
CREATE INDEX emp_dept_id_idx ON employees(dept_id);
CREATE INDEX emp_last_name_idx ON employees(last_name);
CREATE INDEX emp_hire_date_idx ON employees(hire_date);

-- Step 4: Create views
CREATE OR REPLACE VIEW emp_dept_vw AS
SELECT e.emp_id,
       e.first_name,
       e.last_name,
       e.email,
       e.hire_date,
       e.salary,
       d.dept_name,
       d.location,
       m.first_name || ' ' || m.last_name AS manager_name
FROM   employees e
JOIN   departments d ON e.dept_id = d.dept_id
LEFT JOIN employees m ON d.manager_id = m.emp_id
WHERE  e.active_flag = 'Y';

-- Step 5: Create triggers
CREATE OR REPLACE TRIGGER emp_biu_trg
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Set emp_id from sequence
    IF inserting AND :new.emp_id IS NULL THEN
        :new.emp_id := emp_seq.NEXTVAL;
    END IF;

    -- Set audit columns
    IF inserting THEN
        :new.created_by := COALESCE(v('APP_USER'), USER);
        :new.created_date := SYSDATE;
    END IF;

    IF updating THEN
        :new.updated_by := COALESCE(v('APP_USER'), USER);
        :new.updated_date := SYSDATE;
    END IF;

    -- Validate salary
    IF :new.salary IS NOT NULL AND :new.salary < 0 THEN
        raise_application_error(-20001, 'Salary cannot be negative');
    END IF;
END;
/

-- Step 6: Create PL/SQL packages (see templates/packages/)
```

### Phase 3: APEX Application Creation
```yaml
1. Create Application:
   - App Builder > Create Application
   - Name: Employee Management System
   - Theme: Universal Theme (42)
   - Authentication: Database Accounts

2. Create Pages:
   - Page 1: Home Dashboard
   - Page 10: Employees (Interactive Grid)
   - Page 20: Employee Form
   - Page 30: Departments (Interactive Report)
   - Page 40: Department Form
   - Page 50: Reports (Charts and Analytics)
   - Page 100: Administration
   - Page 101: Login

3. Configure Shared Components:
   - Lists: Navigation Menu
   - LOVs: Departments, Managers
   - Authorization Schemes: Is Admin, Is Manager
   - Processes: Send Email, Log Activity
   - Computations: Calculate Age, Tenure

4. Implement Security:
   - Authentication Scheme
   - Authorization Schemes for pages
   - Session State Protection
   - Input validation
```

### Phase 4: Page Development

**Interactive Grid (Page 10)**:
```sql
-- Region: Employees
-- Type: Interactive Grid
-- Source:
SELECT emp_id,
       first_name,
       last_name,
       email,
       phone,
       hire_date,
       salary,
       dept_id,
       is_manager
FROM   employees
WHERE  active_flag = 'Y'

-- Settings:
-- Editable: Yes
-- Toolbar: Show
-- Add Row Button: Yes
-- Row Actions: Edit, Delete
-- DML: Automatic Row Processing
-- Primary Key: EMP_ID
-- Pagination: Load All Rows (if < 1000 rows)

-- Columns:
-- EMP_ID: Hidden, Primary Key
-- DEPT_ID: Select List, LOV: SELECT dept_id d, dept_name r FROM departments
-- SALARY: Number Field, Format: $999,999,990.00
-- IS_MANAGER: Switch, On Value: Y, Off Value: N
```

**Form (Page 20)**:
```yaml
Region: Employee Details
Type: Form
Source Type: Table
Table Name: EMPLOYEES
Primary Key Column: EMP_ID

Items:
  P20_EMP_ID:
    Type: Hidden
    Primary Key: Yes

  P20_FIRST_NAME:
    Type: Text Field
    Label: First Name
    Required: Yes
    Max Length: 50

  P20_LAST_NAME:
    Type: Text Field
    Label: Last Name
    Required: Yes
    Max Length: 50

  P20_EMAIL:
    Type: Text Field
    Label: Email
    Required: Yes
    Validation: Must be valid email format

  P20_PHONE:
    Type: Text Field
    Label: Phone
    Format Mask: (999) 999-9999

  P20_HIRE_DATE:
    Type: Date Picker
    Label: Hire Date
    Required: Yes
    Format Mask: MM/DD/YYYY
    Default: &SYSDATE.

  P20_SALARY:
    Type: Number Field
    Label: Salary
    Format Mask: $999,999,990.00
    Min Value: 0

  P20_DEPT_ID:
    Type: Select List
    Label: Department
    Required: Yes
    LOV: SELECT dept_id d, dept_name r FROM departments ORDER BY dept_name

  P20_IS_MANAGER:
    Type: Switch
    Label: Manager
    On Value: Y
    Off Value: N

Buttons:
  - CREATE (shown on insert)
  - SAVE (shown on update)
  - DELETE
  - CANCEL

Processes:
  - Process Form (Automatic Row Processing - DML)
  - Close Dialog (After Processing, on success)

Validations:
  - Email format validation
  - Salary positive validation
  - Hire date not in future
```

**Interactive Report (Page 30)**:
```sql
-- Region: Departments
-- Type: Interactive Report
-- Source:
SELECT d.dept_id,
       d.dept_name,
       d.location,
       m.first_name || ' ' || m.last_name AS manager_name,
       d.budget,
       COUNT(e.emp_id) AS employee_count,
       SUM(e.salary) AS total_salary,
       d.budget - NVL(SUM(e.salary), 0) AS budget_remaining
FROM   departments d
LEFT JOIN employees m ON d.manager_id = m.emp_id
LEFT JOIN employees e ON d.dept_id = e.dept_id AND e.active_flag = 'Y'
GROUP BY d.dept_id, d.dept_name, d.location,
         m.first_name, m.last_name, d.budget
ORDER BY d.dept_name

-- Columns:
-- DEPT_ID: Link to form (Page 40, set P40_DEPT_ID)
-- TOTAL_SALARY, BUDGET, BUDGET_REMAINING: Format as currency
-- Conditional highlighting: BUDGET_REMAINING < 0 (red background)

-- Features Enabled:
-- Search Bar: Yes
-- Actions Menu: Yes (Filter, Sort, Control Break, Highlight, etc.)
-- Download: CSV, HTML, PDF, Email
-- Subscription: Yes
-- Saved Reports: Yes
```

**Chart (Page 50)**:
```sql
-- Region: Sales by Region
-- Type: Bar Chart
-- Source:
SELECT region,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 1 THEN sales_amount ELSE 0 END) AS jan,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 2 THEN sales_amount ELSE 0 END) AS feb,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 3 THEN sales_amount ELSE 0 END) AS mar,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 4 THEN sales_amount ELSE 0 END) AS apr,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 5 THEN sales_amount ELSE 0 END) AS may,
       SUM(CASE WHEN EXTRACT(MONTH FROM sale_date) = 6 THEN sales_amount ELSE 0 END) AS jun
FROM   sales_data
WHERE  sale_date >= TRUNC(SYSDATE, 'YEAR')
GROUP BY region
ORDER BY region

-- Chart Settings:
-- Type: Bar (Horizontal)
-- Label: Region
-- Series: Jan, Feb, Mar, Apr, May, Jun
-- Format: $999,999,990
-- Legend: Show
-- Animation: On Initial Load
```

### Phase 5: Business Logic Implementation
```plsql
-- Create PL/SQL package for business logic
CREATE OR REPLACE PACKAGE emp_mgmt_pkg AS
    -- Employee management business logic

    PROCEDURE create_employee(
        p_first_name   IN VARCHAR2,
        p_last_name    IN VARCHAR2,
        p_email        IN VARCHAR2,
        p_dept_id      IN NUMBER,
        p_salary       IN NUMBER,
        p_hire_date    IN DATE DEFAULT SYSDATE,
        p_emp_id       OUT NUMBER
    );

    PROCEDURE update_employee(
        p_emp_id       IN NUMBER,
        p_first_name   IN VARCHAR2 DEFAULT NULL,
        p_last_name    IN VARCHAR2 DEFAULT NULL,
        p_email        IN VARCHAR2 DEFAULT NULL,
        p_salary       IN NUMBER DEFAULT NULL
    );

    PROCEDURE terminate_employee(
        p_emp_id       IN NUMBER,
        p_term_date    IN DATE DEFAULT SYSDATE,
        p_term_reason  IN VARCHAR2
    );

    FUNCTION get_dept_headcount(
        p_dept_id IN NUMBER
    ) RETURN NUMBER;

    FUNCTION get_emp_tenure_years(
        p_emp_id IN NUMBER
    ) RETURN NUMBER;

    PROCEDURE promote_to_manager(
        p_emp_id       IN NUMBER,
        p_dept_id      IN NUMBER,
        p_effective_dt IN DATE DEFAULT SYSDATE
    );

END emp_mgmt_pkg;
/

-- Implement package body (see templates/packages/)

-- Call from APEX process
BEGIN
    emp_mgmt_pkg.create_employee(
        p_first_name => :P20_FIRST_NAME,
        p_last_name  => :P20_LAST_NAME,
        p_email      => :P20_EMAIL,
        p_dept_id    => :P20_DEPT_ID,
        p_salary     => :P20_SALARY,
        p_emp_id     => :P20_EMP_ID
    );
END;
```

### Phase 6: Security Implementation
```yaml
Authentication Scheme:
  Name: Database Account Authentication
  Type: Database Account
  Cookie Name: APEX_EMS_SESSION
  Session Timeout: 3600 (1 hour)
  Maximum Session Length: 28800 (8 hours)

Authorization Schemes:
  1. Is Administrator:
     Type: PL/SQL Function Returning Boolean
     Code: |
       RETURN emp_mgmt_pkg.is_user_admin(:APP_USER);

  2. Is Manager:
     Type: PL/SQL Function Returning Boolean
     Code: |
       RETURN emp_mgmt_pkg.is_user_manager(:APP_USER);

  3. Is Employee Owner:
     Type: PL/SQL Function Returning Boolean
     Code: |
       RETURN emp_mgmt_pkg.is_employee_owner(
           p_username => :APP_USER,
           p_emp_id => :P20_EMP_ID
       );

Apply Authorization:
  - Page 100 (Administration): Is Administrator
  - Page 40 (Department Form): Is Manager
  - Page 20 Delete Button: Is Administrator
  - Page 20 Salary Field: Is Manager

Session State Protection:
  - Enable for all pages
  - Checksum required for all items
```

### Phase 7: Testing
```yaml
Unit Testing:
  - Test all validations
  - Test authorization schemes
  - Test PL/SQL packages
  - Test form submissions
  - Test report filters

Integration Testing:
  - Test complete workflows
  - Test error scenarios
  - Test concurrent users
  - Test large datasets
  - Test REST API integrations

Performance Testing:
  - Load test with 100+ concurrent users
  - Test with realistic data volumes
  - Measure page load times
  - Identify slow queries
  - Optimize as needed

Security Testing:
  - Test for SQL injection
  - Test for XSS vulnerabilities
  - Test authorization bypasses
  - Test session hijacking
  - Run APEX Advisor

User Acceptance Testing:
  - Test with actual users
  - Gather feedback
  - Refine UI/UX
  - Fix bugs
  - Document known issues
```

### Phase 8: Deployment
```yaml
Pre-Deployment:
  1. Export application:
     - App Builder > Export/Import > Export
     - Include supporting objects
     - Split into multiple files (optional)

  2. Prepare deployment script:
     - Create install.sql with prompts
     - Include rollback script
     - Document prerequisites
     - Test in staging environment

  3. Version control:
     - Commit to Git repository
     - Tag release version
     - Update CHANGELOG

Deployment:
  1. Backup production:
     - Export existing application
     - Backup database schema
     - Document current state

  2. Deploy to production:
     - Run install script
     - Import application
     - Run supporting object scripts
     - Update application alias

  3. Smoke testing:
     - Test critical workflows
     - Verify authentication
     - Check data integrity
     - Test integrations

Post-Deployment:
  1. Monitor application:
     - Check logs for errors
     - Monitor performance
     - Watch user activity
     - Gather feedback

  2. Document deployment:
     - Record deployment date/time
     - Document issues encountered
     - Note lessons learned
     - Update runbook
```

## Reference Guides

### Available Guides
The following comprehensive reference guides are available in the `reference/` directory:

1. **apex_architecture.md** - APEX architecture, workspace structure, application components
2. **interactive_grids.md** - Interactive Grid development, advanced features, customization
3. **forms_reports.md** - Forms and Reports best practices, patterns
4. **charts_visualizations.md** - Data visualization, chart types, configuration
5. **plsql_integration.md** - PL/SQL integration patterns, package design, error handling
6. **rest_api_integration.md** - REST Data Sources, Web Source Modules, OAuth
7. **authentication_security.md** - Security best practices, authentication schemes
8. **performance_tuning.md** - Performance optimization, SQL tuning, caching

### Quick Reference Patterns

**Pattern 1: Cascade LOVs**
```yaml
Dynamic Action: Change Department
When: Change
Item: P10_DEPT_ID

True Action:
  Action: Set Value
  Set Type: SQL Query
  SQL: SELECT manager_id FROM departments WHERE dept_id = :P10_DEPT_ID
  Items to Submit: P10_DEPT_ID
  Affected Elements: P10_MANAGER_ID
```

**Pattern 2: Conditional Display**
```yaml
Item: P10_SALARY
Condition Type: PL/SQL Expression
PL/SQL Expression: emp_mgmt_pkg.is_user_manager(:APP_USER)
```

**Pattern 3: Dynamic Report Filter**
```sql
SELECT * FROM employees
WHERE  (:P30_DEPT_ID IS NULL OR dept_id = :P30_DEPT_ID)
AND    (:P30_SEARCH IS NULL OR
        UPPER(first_name || ' ' || last_name) LIKE '%' || UPPER(:P30_SEARCH) || '%')
```

**Pattern 4: Modal Dialog**
```yaml
Button: Edit Employee
Target:
  Type: Page in this Application
  Page: 20
  Set Items: P20_EMP_ID = #EMP_ID#
  Clear Cache: 20

Dialog:
  Open as: Modal Dialog
  Width: 600
  Height: Auto
  Resizable: Yes
```

## Templates

### Available Templates
The following ready-to-use templates are available in the `templates/` directory:

1. **crud_application.sql** - Complete CRUD application with search
2. **dashboard_template.sql** - Dashboard with charts and KPIs
3. **report_template.sql** - Interactive report with drill-down
4. **form_template.sql** - Form with validations and dynamic actions
5. **api_template.sql** - REST API module template
6. **authentication_scheme.sql** - Custom authentication template

### Template Usage
```bash
# Copy template to working directory
cp templates/crud_application.sql my_app.sql

# Customize placeholders
sed -i 's/TABLE_NAME/employees/g' my_app.sql
sed -i 's/APP_NAME/Employee Management/g' my_app.sql

# Import to APEX
sqlcl admin/password@database
@my_app.sql
```

## Example Applications

### Available Examples
The following complete example applications are available in the `examples/` directory:

1. **employee_management_app.md** - Complete employee management system
   - Employee CRUD with search
   - Department management
   - Manager assignment
   - Salary updates with approval
   - Reports and dashboards

2. **sales_dashboard.md** - Sales analytics dashboard
   - Sales by region charts
   - Trend analysis
   - Top products/customers
   - Real-time KPIs
   - Export capabilities

3. **inventory_tracker.md** - Inventory management application
   - Product catalog
   - Stock levels monitoring
   - Purchase orders
   - Supplier management
   - Low stock alerts

4. **api_integration_example.md** - Third-party API integration
   - GitHub API integration
   - REST Data Source configuration
   - OAuth authentication
   - Data synchronization
   - Error handling

### Example Application Features
Each example includes:
- Complete database schema (DDL)
- PL/SQL packages for business logic
- APEX application export
- Page-by-page documentation
- Screenshots and diagrams
- Testing procedures
- Deployment instructions

## Utility Scripts

### Available Scripts
The following utility scripts are available in the `scripts/` directory:

1. **apex_export.py** - Export APEX applications
2. **apex_import.py** - Import applications to different workspaces
3. **apex_deployment.py** - Deploy to multiple environments
4. **apex_backup.py** - Backup APEX workspace and applications

### Script Usage

**Export Application**:
```bash
python scripts/apex_export.py \
    --host mydb.example.com \
    --port 1521 \
    --service XEPDB1 \
    --username admin \
    --app-id 100 \
    --output-dir exports/
```

**Import Application**:
```bash
python scripts/apex_import.py \
    --host targetdb.example.com \
    --port 1521 \
    --service PRODDB \
    --username admin \
    --file exports/f100.sql \
    --workspace PRODUCTION
```

**Deploy to Multiple Environments**:
```bash
python scripts/apex_deployment.py \
    --config deploy_config.yml \
    --app-id 100 \
    --version 1.2.0
```

**Backup Workspace**:
```bash
python scripts/apex_backup.py \
    --host mydb.example.com \
    --port 1521 \
    --service XEPDB1 \
    --username admin \
    --workspace DEV \
    --output-dir backups/
```

## Common Issues and Solutions

### Issue 1: Session State Issues
**Problem**: Items not retaining values across page submissions

**Solution**:
```yaml
Check:
  1. Item is in Session State (not Display Only)
  2. Item is not being cleared unintentionally
  3. Session State Protection is not blocking updates
  4. Item name is correct (case-sensitive)

Fix:
  - Set item as "Session State Protected: Unrestricted"
  - Or add item to Session State Protection whitelist
```

### Issue 2: Performance Issues
**Problem**: Pages load slowly with large datasets

**Solution**:
```sql
-- Implement pagination
-- Interactive Grid: Set pagination to "Page" with 100 rows
-- Interactive Report: Row Ranges 15

-- Optimize SQL queries
-- Add indexes on filter columns
CREATE INDEX emp_search_idx ON employees(
    UPPER(first_name || ' ' || last_name)
);

-- Use caching
-- Enable region caching for static data
-- Cache: 1 hour, Cached by User: No
```

### Issue 3: Authorization Not Working
**Problem**: Users seeing pages they shouldn't access

**Solution**:
```yaml
Verify:
  1. Authorization Scheme is created correctly
  2. Authorization Scheme is applied to page/component
  3. User has correct privileges in database
  4. Session context is set properly

Debug:
  - Enable Debug mode (&DEBUG=YES)
  - Check authorization evaluation in debug log
  - Test authorization scheme directly
```

### Issue 4: REST Integration Failures
**Problem**: REST Data Source not returning data

**Solution**:
```yaml
Troubleshoot:
  1. Test REST endpoint in browser/Postman
  2. Check Response Format (JSON/XML)
  3. Verify Row Selector path
  4. Check authentication (API key, OAuth)
  5. Review APEX Web Services access control

Fix:
  - Update Row Selector to match response structure
  - Add proper authentication headers
  - Enable debug logging for Web Services
```

## Best Practices Summary

### Development Best Practices
1. **Use bind variables** in all SQL queries
2. **Encapsulate logic** in PL/SQL packages
3. **Apply authorization** to sensitive pages/components
4. **Enable Session State Protection**
5. **Clear session state** when not needed
6. **Use meaningful naming** conventions
7. **Create indexes** on filter and foreign key columns
8. **Implement error handling** in all PL/SQL code
9. **Use substitution strings** for maintainability
10. **Version control** application exports

### Security Best Practices
1. **Never trust user input** - validate everything
2. **Use bind variables** to prevent SQL injection
3. **Escape output** to prevent XSS
4. **Implement authorization** at multiple levels
5. **Enable HTTPS** for production
6. **Use strong authentication** (LDAP, SSO, OAuth)
7. **Audit sensitive operations**
8. **Protect session state**
9. **Implement rate limiting** for APIs
10. **Keep APEX updated** with latest patches

### Performance Best Practices
1. **Optimize SQL queries** (use EXPLAIN PLAN)
2. **Create appropriate indexes**
3. **Implement pagination** for large datasets
4. **Use caching** strategically
5. **Minimize session state items**
6. **Optimize images** and static files
7. **Use CDN** for static content
8. **Lazy load** components when possible
9. **Monitor APEX views** for bottlenecks
10. **Regular database maintenance** (stats, cleanup)

## Getting Help

### Resources
- **Oracle APEX Documentation**: https://docs.oracle.com/en/database/oracle/apex/
- **APEX API Reference**: https://docs.oracle.com/en/database/oracle/apex/23.1/aeapi/
- **APEX Community**: https://apex.oracle.com/community
- **APEX.WORLD**: https://apex.world/
- **Ask Tom (Oracle)**: https://asktom.oracle.com/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/oracle-apex

### When to Ask for Help
- Stuck on complex SQL query optimization
- Need architecture review for large application
- Security concerns or vulnerabilities
- Performance issues not resolved by standard techniques
- Integration with unfamiliar APIs or systems
- Custom plugin development
- Migration from legacy systems

### Escalation Path
1. **Self-service**: Check reference guides and examples
2. **oracle-apex-specialist**: Delegate to SubAgent for complex issues
3. **database-expert**: For database-specific problems
4. **security-auditor**: For security reviews
5. **Community**: Post on APEX forums or Stack Overflow
6. **Oracle Support**: For product bugs or critical issues

## Success Criteria
- APEX application deployed and accessible
- All CRUD operations working correctly
- Reports and charts displaying accurate data
- Authentication and authorization functioning properly
- No security vulnerabilities (SQL injection, XSS)
- Page load times acceptable (<3 seconds)
- Application follows APEX best practices
- Code is maintainable and documented
- Tests passing (unit, integration, UAT)
- Users satisfied with functionality and usability

---

**Remember**: Oracle APEX enables rapid development of enterprise-grade applications. Focus on declarative development, leverage built-in features, and encapsulate complex logic in PL/SQL packages for the best results.
