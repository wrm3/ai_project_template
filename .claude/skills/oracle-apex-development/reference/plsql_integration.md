# Oracle APEX PL/SQL Integration

## PL/SQL Package Design

### Package Structure
```plsql
CREATE OR REPLACE PACKAGE emp_mgmt_pkg AS
    -- Constants
    c_max_salary CONSTANT NUMBER := 500000;
    
    -- Procedures
    PROCEDURE create_employee(
        p_first_name IN VARCHAR2,
        p_last_name IN VARCHAR2,
        p_email IN VARCHAR2,
        p_dept_id IN NUMBER,
        p_salary IN NUMBER,
        p_emp_id OUT NUMBER
    );
    
    PROCEDURE update_salary(
        p_emp_id IN NUMBER,
        p_new_salary IN NUMBER
    );
    
    -- Functions
    FUNCTION get_dept_headcount(p_dept_id IN NUMBER) RETURN NUMBER;
    FUNCTION is_user_manager(p_username IN VARCHAR2) RETURN BOOLEAN;
END emp_mgmt_pkg;
/

CREATE OR REPLACE PACKAGE BODY emp_mgmt_pkg AS
    -- Implementation here
END emp_mgmt_pkg;
/
```

## Call from APEX Processes

### Execute Code Process
```plsql
-- Process: Create Employee
-- Type: Execute Code
BEGIN
    emp_mgmt_pkg.create_employee(
        p_first_name => :P20_FIRST_NAME,
        p_last_name => :P20_LAST_NAME,
        p_email => :P20_EMAIL,
        p_dept_id => :P20_DEPT_ID,
        p_salary => :P20_SALARY,
        p_emp_id => :P20_EMP_ID
    );
    
    apex_application.g_print_success_message := 
        'Employee created successfully';
EXCEPTION
    WHEN OTHERS THEN
        apex_error.add_error(
            p_message => 'Error: ' || SQLERRM,
            p_display_location => apex_error.c_inline_in_notification
        );
END;
```

### PL/SQL Function Body
```plsql
-- Validation: Check Manager Privileges
-- Type: PL/SQL Function Body (returning Boolean)
BEGIN
    RETURN emp_mgmt_pkg.is_user_manager(:APP_USER);
END;
```

## APEX APIs

### Session State
```plsql
-- Set item values
apex_util.set_session_state('P10_EMP_ID', 1001);

-- Get item values
l_emp_id := apex_util.get_session_state('P10_EMP_ID');

-- Clear session state
apex_util.clear_page_cache(10);
```

### Email
```plsql
-- Send email
apex_mail.send(
    p_to => 'user@example.com',
    p_from => 'noreply@company.com',
    p_subject => 'Welcome to Company',
    p_body => 'Welcome ' || :P10_FIRST_NAME || '!',
    p_body_html => '<h1>Welcome!</h1><p>Thank you for joining.</p>'
);

apex_mail.push_queue;
```

### Collections
```plsql
-- Create collection
apex_collection.create_or_truncate_collection('EMP_SELECTION');

-- Add member
apex_collection.add_member(
    p_collection_name => 'EMP_SELECTION',
    p_c001 => l_emp_id,
    p_c002 => l_emp_name
);

-- Query collection
SELECT c001 AS emp_id, c002 AS emp_name
FROM apex_collections
WHERE collection_name = 'EMP_SELECTION';
```

## Error Handling

### Best Practices
```plsql
DECLARE
    e_validation_error EXCEPTION;
BEGIN
    -- Validation
    IF :P20_SALARY < 0 THEN
        RAISE e_validation_error;
    END IF;
    
    -- Business logic
    emp_mgmt_pkg.create_employee(...);
    
    COMMIT;
EXCEPTION
    WHEN e_validation_error THEN
        apex_error.add_error(
            p_message => 'Salary must be positive',
            p_display_location => apex_error.c_inline_with_field,
            p_page_item_name => 'P20_SALARY'
        );
    WHEN OTHERS THEN
        apex_debug.error('Unexpected error: %s', SQLERRM);
        apex_error.add_error(
            p_message => 'System error. Please contact support.',
            p_display_location => apex_error.c_inline_in_notification
        );
        ROLLBACK;
END;
```

---

**Summary**: Encapsulate business logic in PL/SQL packages, use APEX APIs effectively, and implement robust error handling.
