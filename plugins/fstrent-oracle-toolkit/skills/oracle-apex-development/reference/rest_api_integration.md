# Oracle APEX REST API Integration

## REST Data Sources

### Configure REST Data Source
```yaml
Name: GitHub User API
Base URL: https://api.github.com
Service URL Path: /users/:username

HTTP Method: GET
Request Headers:
  - Accept: application/vnd.github.v3+json
  - User-Agent: APEX-App

Authentication: None (public API)

Response Processing:
  Row Selector: .
  Columns:
    - LOGIN: $.login
    - NAME: $.name
    - BIO: $.bio
    - FOLLOWERS: $.followers
    - PUBLIC_REPOS: $.public_repos
```

### Use in Interactive Report
```sql
-- Region: GitHub User Info
-- Source Type: REST Data Source
-- REST Source: GitHub User API

SELECT login,
       name,
       bio,
       followers,
       public_repos
FROM   #APEX$SOURCE_DATA#
WHERE  :P30_USERNAME IS NOT NULL

-- Parameters:
-- USERNAME = :P30_USERNAME
```

## OAuth 2.0 Integration

### Configure Web Credentials
```yaml
Web Credentials:
  Name: GitHub OAuth
  Authentication Type: OAuth2 Client Credentials
  Client ID: your_client_id
  Client Secret: your_client_secret
  Token URL: https://github.com/login/oauth/access_token
```

### Use with REST Data Source
```yaml
REST Data Source:
  Name: GitHub Private Repos
  Authentication Required: Yes
  Credentials: GitHub OAuth
```

## APEX RESTful Services

### Create REST Handler
```plsql
-- Module: employees.v1
-- Template: /employees/:id
-- Handler: GET

-- Source Type: Query
-- Source:
SELECT emp_id,
       first_name,
       last_name,
       email,
       salary
FROM   employees
WHERE  emp_id = :id
AND    active_flag = 'Y'

-- Response: JSON (automatic)
```

### POST Handler
```plsql
-- Handler: POST /employees
-- Source Type: PL/SQL

DECLARE
    l_body CLOB;
    l_emp_id NUMBER;
BEGIN
    l_body := :body_text;
    
    INSERT INTO employees (
        first_name, last_name, email, dept_id
    ) VALUES (
        apex_json.get_varchar2(p_path => 'firstName'),
        apex_json.get_varchar2(p_path => 'lastName'),
        apex_json.get_varchar2(p_path => 'email'),
        apex_json.get_number(p_path => 'deptId')
    ) RETURNING emp_id INTO l_emp_id;
    
    :status_code := 201;
    apex_json.open_object;
    apex_json.write('empId', l_emp_id);
    apex_json.write('message', 'Employee created');
    apex_json.close_object;
END;
```

## Web Source Modules

### Parse JSON Response
```plsql
DECLARE
    l_response CLOB;
    l_values apex_json.t_values;
BEGIN
    l_response := apex_web_service.make_rest_request(
        p_url => 'https://api.example.com/data',
        p_http_method => 'GET'
    );
    
    apex_json.parse(l_values, l_response);
    
    -- Extract values
    l_name := apex_json.get_varchar2(
        p_values => l_values,
        p_path => 'data.name'
    );
END;
```

---

**Summary**: Integrate external REST APIs using REST Data Sources, implement OAuth authentication, and create your own REST APIs with APEX RESTful Services.
