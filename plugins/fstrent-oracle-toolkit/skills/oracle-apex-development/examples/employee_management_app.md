# Employee Management Application

## Overview
Complete CRUD application for managing employees with departments, search functionality, and reports.

## Database Schema
```sql
-- Departments Table
CREATE TABLE departments (
    dept_id NUMBER PRIMARY KEY,
    dept_name VARCHAR2(100) NOT NULL UNIQUE,
    location VARCHAR2(100),
    manager_id NUMBER,
    budget NUMBER(12,2),
    created_by VARCHAR2(50),
    created_date DATE
);

-- Employees Table
CREATE TABLE employees (
    emp_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(20),
    hire_date DATE NOT NULL,
    salary NUMBER(10,2),
    dept_id NUMBER,
    is_manager VARCHAR2(1) DEFAULT 'N',
    active_flag VARCHAR2(1) DEFAULT 'Y',
    CONSTRAINT emp_dept_fk FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Create sequences and triggers (see templates/)
```

## Application Structure

### Page 1: Home Dashboard
- Welcome message
- KPI cards (Total Employees, Active, Departments)
- Quick links to main pages

### Page 10: Employee List (Interactive Grid)
```sql
SELECT emp_id, first_name, last_name, email, phone, hire_date, salary, dept_id
FROM employees
WHERE active_flag = 'Y'
-- Editable, with Add/Delete buttons
```

### Page 20: Employee Form
- Form fields: All employee attributes
- LOV for department
- Validations: email format, unique email, positive salary
- Process: Automatic Row Processing (DML)

### Page 30: Department List (Interactive Report)
```sql
SELECT dept_id, dept_name, location, manager_name, budget, employee_count
FROM dept_summary_vw
```

### Page 40: Department Form
- Department details
- Manager selection (LOV from employees where is_manager='Y')
- Budget field with currency format

### Page 50: Reports
- Employees by Department (Bar Chart)
- Salary Distribution (Histogram)
- New Hires Trend (Line Chart)
- Department Headcount (Pie Chart)

## Features
- Full CRUD operations
- Search and filter
- Master-detail relationship
- Validations and error handling
- Reports and analytics
- Authorization (managers can approve)
- Audit trail (created_by, updated_by)

## Testing
1. Create departments
2. Add employees
3. Assign managers
4. Test search functionality
5. Generate reports
6. Test validations
7. Test authorization

## Deployment
1. Run DDL scripts
2. Import APEX application
3. Configure authentication
4. Test in staging
5. Deploy to production
