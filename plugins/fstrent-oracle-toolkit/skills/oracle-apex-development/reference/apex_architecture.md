# Oracle APEX Architecture

## Overview
Oracle Application Express (APEX) is a low-code development platform for building scalable, secure enterprise applications. Understanding APEX architecture is crucial for effective development.

## APEX Architecture Layers

### 1. Database Layer
**Oracle Database** (11g R2 or higher)
- Stores application metadata
- Executes PL/SQL code
- Manages data and business logic
- Provides security and transaction management

**APEX Repository**:
```sql
-- Key APEX metadata tables
APEX_APPLICATIONS       -- Application definitions
APEX_APPLICATION_PAGES  -- Page definitions
APEX_APPLICATION_PAGE_ITEMS  -- Page item definitions
APEX_APPLICATION_PAGE_REGIONS  -- Region definitions
APEX_APPLICATION_PAGE_PROC  -- Page processes
APEX_APPLICATION_PAGE_VAL  -- Page validations
APEX_APPLICATION_AUTH  -- Authentication schemes
APEX_APPLICATION_AUTHORIZATION  -- Authorization schemes
APEX_APPLICATION_LISTS  -- Navigation lists
APEX_APPLICATION_LOVS  -- List of Values
```

### 2. Oracle REST Data Services (ORDS)
**Middleware Layer**:
- HTTP/HTTPS listener
- Routes requests to APEX engine
- Handles REST API calls
- Manages WebSocket connections
- Serves static files
- Connection pooling

**Configuration**:
```bash
# ORDS standalone mode
java -jar ords.war standalone

# ORDS with custom settings
java -jar ords.war standalone \
    --port 8080 \
    --apex-images /path/to/apex/images
```

### 3. APEX Engine
**Processing Engine**:
- Parses page definitions
- Executes page rendering
- Processes form submissions
- Manages session state
- Handles authentication/authorization
- Executes PL/SQL code
- Generates HTML/JavaScript

**Request Processing Flow**:
```
User Request (HTTP)
    ↓
ORDS (Web Listener)
    ↓
APEX Engine (PL/SQL)
    ↓
Parse Application/Page Metadata
    ↓
Execute Page Processing (Before Header)
    ↓
Render Page (Header, Body, Footer)
    ↓
Execute Page Processing (After Submit)
    ↓
Generate HTML/JavaScript/CSS
    ↓
ORDS returns response
    ↓
Browser renders page
```

### 4. Web Browser
**Client Layer**:
- Renders HTML/CSS
- Executes JavaScript
- Handles user interactions
- Makes AJAX requests
- Manages local storage/cookies

## Workspace Structure

### Workspace Components
A **Workspace** is a logical container for APEX applications:

```
Workspace: SALES_DEV
├── Applications
│   ├── App 100: Sales Management
│   ├── App 101: Inventory Tracker
│   └── App 102: Customer Portal
├── SQL Workshop
│   ├── Object Browser
│   ├── SQL Commands
│   ├── SQL Scripts
│   └── Utilities
├── Team Development
│   ├── Features
│   ├── Bugs
│   ├── To Dos
│   └── Milestones
├── Administration
│   ├── Manage Users and Groups
│   ├── Manage Service
│   └── Monitor Activity
└── Packaged Apps
    └── Sample Apps
```

### Workspace Schema
Each workspace has one or more **parsing schemas**:

```sql
-- Workspace: SALES_DEV
-- Parsing Schemas: SALES_SCHEMA, HR_SCHEMA

-- Applications can access tables/views from parsing schemas
-- Example: App 100 uses SALES_SCHEMA
SELECT * FROM sales_schema.customers;
SELECT * FROM sales_schema.orders;
```

## Application Architecture

### Application Components

**1. Pages**:
- Basic building blocks of APEX applications
- Page numbers: 1-9999
- Page 0: Global page (elements appear on all pages)
- Modal Dialog pages
- Master-Detail pages

**2. Regions**:
- Containers for content
- Types: Interactive Grid, Interactive Report, Form, Chart, Static Content, PL/SQL Dynamic Content
- Can be nested (parent-child)
- Display Points: Breadcrumb Bar, Content Body, Dialog Header, etc.

**3. Items**:
- Input fields and display elements
- Page Items: P10_FIRST_NAME, P10_DEPT_ID
- Application Items: AI_COMPANY_NAME, AI_FISCAL_YEAR
- Types: Text Field, Number Field, Date Picker, Select List, Checkbox, Switch, etc.

**4. Buttons**:
- Trigger actions or navigation
- Types: Standard, Hot (emphasized), Icon, Text
- Actions: Submit Page, Redirect, Execute JavaScript

**5. Processes**:
- Execute server-side logic
- Types: Form - Automatic Row Processing (DML), Execute Code, Close Dialog
- Timing: Before Header, After Header, Before Region, After Region, After Submit

**6. Validations**:
- Ensure data integrity
- Types: Item is NOT NULL, Item in LOV, PL/SQL Function Returning Boolean
- Display: Inline with Field, Inline with Field and Notification, Notification

**7. Computations**:
- Calculate derived values
- Set item values dynamically
- Timing: Before Header, After Header, Before Region, After Region

**8. Branches**:
- Control page flow
- Redirect after processing
- Conditional branching

**9. Dynamic Actions**:
- Client-side interactivity
- Events: Click, Change, Load, Custom
- Actions: Show, Hide, Set Value, Execute JavaScript, Refresh

### Shared Components

**Shared Components** are reusable across pages:

```
Shared Components
├── Application Items
├── Application Processes
├── Application Computations
├── Navigation
│   ├── Lists
│   ├── Navigation Bar Entries
│   └── Breadcrumbs
├── Security
│   ├── Authentication Schemes
│   ├── Authorization Schemes
│   └── Session State Protection
├── Logic
│   ├── Build Options
│   └── Application Settings
├── User Interface
│   ├── Themes
│   ├── Templates
│   ├── Shortcuts
│   └── Plug-ins
├── Files
│   ├── Static Application Files
│   └── Static Workspace Files
└── Data Components
    ├── List of Values
    └── Data Profiles
```

## Page Architecture

### Page Execution Model

**Page Lifecycle**:
```
1. Request Phase
   ├── Show Page (GET request)
   └── Submit Page (POST request)

2. Before Header Processing
   ├── Run Application Processes (Before Header)
   ├── Run Page Processes (Before Header)
   ├── Execute Computations (Before Header)
   └── Execute Validations (if submit)

3. Rendering Phase
   ├── Fetch session state
   ├── Execute Page Processes (Before Region)
   ├── Render Regions
   │   ├── Execute Region Queries
   │   ├── Render Items
   │   └── Apply Templates
   ├── Execute Page Processes (After Region)
   └── Generate HTML/JavaScript

4. After Submit Processing (if POST)
   ├── Execute Validations
   ├── Execute Page Processes (After Submit)
   ├── Execute Computations (After Submit)
   ├── Execute Branches
   └── Redirect or Show Page
```

### Page Template Structure

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Theme CSS -->
    <link rel="stylesheet" href="apex/theme/css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="custom.css">
    <!-- Page-level CSS -->
    <style>#PAGE_CSS#</style>
</head>
<body class="apex-page">
    <!-- Breadcrumb Bar -->
    <div class="t-BreadcrumbRegion">#REGION_POSITION_01#</div>

    <!-- Navigation Bar -->
    <nav class="t-NavigationBar">#NAVIGATION_BAR#</nav>

    <!-- Content Body -->
    <main class="t-Body">
        <!-- Regions -->
        #REGION_POSITION_02#
        #BODY#
        #REGION_POSITION_03#
    </main>

    <!-- Footer -->
    <footer class="t-Footer">#APP_VERSION#</footer>

    <!-- JavaScript -->
    <script src="apex/theme/js"></script>
    <script>#PAGE_JAVASCRIPT#</script>
</body>
</html>
```

## Session State Management

### Session State
APEX manages state across HTTP requests using sessions:

```sql
-- Session information
SELECT apex_authentication.is_authenticated AS is_auth,
       v('APP_SESSION') AS session_id,
       v('APP_USER') AS username,
       v('APP_PAGE_ID') AS current_page
FROM   dual;

-- Access page items
:P10_FIRST_NAME  -- In PL/SQL
v('P10_FIRST_NAME')  -- In SQL
&P10_FIRST_NAME.  -- In substitution strings
#P10_FIRST_NAME#  -- In JavaScript/HTML
```

### Session State Storage
```
Session State
├── Application Items (AI_*)
│   └── Persists across pages within session
├── Page Items (P10_*)
│   └── Persists within page/session
└── Collections
    └── Temporary data storage (like temp tables)
```

### Session State Protection
Protects against URL tampering:

```yaml
Session State Protection:
  - Unrestricted: No protection (development only)
  - Restricted: Checksum required for modifications
  - Arguments Must Have Checksum: All URL parameters verified
  - Checksum Required: All modifications verified
```

## Authentication Architecture

### Authentication Flow
```
1. User accesses application
    ↓
2. APEX checks session cookie
    ↓
3. If no session or expired:
   ├── Redirect to login page
   ├── User enters credentials
   ├── Authentication scheme validates
   └── Create session on success
    ↓
4. If valid session:
   └── Allow access to page (check authorization)
```

### Authentication Schemes
```sql
-- Built-in schemes
1. Database Account
   - Uses Oracle database accounts
   - SELECT username FROM dba_users

2. APEX Accounts
   - Managed in APEX workspace
   - APEX_UTIL.CREATE_USER

3. LDAP Directory
   - Authenticates against LDAP server
   - Common for enterprises

4. OAuth 2.0
   - Google, Facebook, GitHub, etc.
   - Token-based authentication

5. SAML
   - Single Sign-On
   - Enterprise SSO integration

6. Custom
   - PL/SQL function-based
   - External authentication API
```

### Authorization Architecture

**Authorization Schemes**:
```plsql
-- Example: Role-based authorization
CREATE OR REPLACE FUNCTION is_admin(
    p_username IN VARCHAR2
) RETURN BOOLEAN
IS
    l_is_admin BOOLEAN;
BEGIN
    SELECT COUNT(*) > 0
    INTO   l_is_admin
    FROM   app_users
    WHERE  username = p_username
    AND    role = 'ADMIN';

    RETURN l_is_admin;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END is_admin;
/

-- Apply to pages
-- Page 100 (Admin) -> Authorization Scheme: Is Admin
-- Result: Only admins can access Page 100
```

## REST API Architecture

### APEX RESTful Services (ORDS)
```sql
-- Define REST module
BEGIN
    ords.define_module(
        p_module_name => 'employees.v1',
        p_base_path => '/employees/'
    );

    -- Define GET handler
    ords.define_template(
        p_module_name => 'employees.v1',
        p_pattern => ':id'
    );

    ords.define_handler(
        p_module_name => 'employees.v1',
        p_pattern => ':id',
        p_method => 'GET',
        p_source_type => ords.source_type_query,
        p_source => 'SELECT * FROM employees WHERE emp_id = :id'
    );
END;
/

-- Access: https://server/ords/workspace/employees/1001
```

### REST Data Sources
```yaml
REST Data Source: GitHub Users
  URL: https://api.github.com/users/:username
  Method: GET
  Authentication: None (public API)

  Parameters:
    - username (URL Pattern)

  Response:
    Row Selector: .
    Columns:
      - LOGIN ($.login)
      - NAME ($.name)
      - BIO ($.bio)
      - FOLLOWERS ($.followers)

  Usage in APEX:
    SELECT login, name, bio, followers
    FROM   #APEX$SOURCE_DATA#
```

## Performance Architecture

### Caching Layers
```
Caching Strategy
├── Database
│   ├── Result Cache (SQL queries)
│   ├── PL/SQL Function Result Cache
│   └── Materialized Views
├── APEX Engine
│   ├── Page Cache (entire pages)
│   ├── Region Cache (region content)
│   └── Query Result Cache
├── ORDS
│   └── Static File Cache
└── Browser
    ├── Browser Cache (images, CSS, JS)
    └── Local Storage (client-side data)
```

### Connection Pooling
```yaml
ORDS Connection Pool:
  pool.initialSize: 10
  pool.minSize: 10
  pool.maxSize: 100
  pool.maxConnectionReuseCount: 1000
  pool.connectionWaitTimeout: 30
  pool.statementTimeout: 900
```

## Deployment Architecture

### Environment Topology
```
Production Environment
├── Load Balancer (HTTPS)
│   ├── ORDS Instance 1 (App Server 1)
│   ├── ORDS Instance 2 (App Server 2)
│   └── ORDS Instance 3 (App Server 3)
├── Oracle Database (RAC)
│   ├── Node 1
│   ├── Node 2
│   └── Node 3
└── Shared Storage
    ├── APEX Images
    └── Static Files
```

### High Availability Setup
```yaml
HA Configuration:
  Load Balancer:
    - Round-robin distribution
    - Health checks every 30s
    - SSL termination

  ORDS Instances:
    - Multiple ORDS instances
    - Session affinity enabled
    - Connection pooling

  Database:
    - Oracle RAC (2+ nodes)
    - Automatic failover
    - Data Guard for DR
```

## Monitoring and Logging

### APEX Views for Monitoring
```sql
-- Active sessions
SELECT workspace,
       application_id,
       application_name,
       user_name,
       page_id,
       session_length_sec
FROM   apex_workspace_sessions
WHERE  last_updated > SYSDATE - INTERVAL '1' HOUR;

-- Page views
SELECT application_id,
       page_id,
       COUNT(*) AS page_views,
       AVG(elapsed_time) AS avg_elapsed_ms
FROM   apex_workspace_activity_log
WHERE  time_stamp > SYSDATE - INTERVAL '1' DAY
GROUP BY application_id, page_id
ORDER BY page_views DESC;

-- Errors
SELECT application_id,
       page_id,
       error_message,
       COUNT(*) AS occurrences
FROM   apex_workspace_activity_log
WHERE  time_stamp > SYSDATE - INTERVAL '1' DAY
AND    error_message IS NOT NULL
GROUP BY application_id, page_id, error_message
ORDER BY occurrences DESC;
```

### Debug Logging
```plsql
-- Enable debug in PL/SQL
apex_debug.enable;
apex_debug.message('Processing employee ID: %s', :P10_EMP_ID);
apex_debug.message('Department: %s', :P10_DEPT_ID);

-- View debug log
-- View Debug button in Developer Toolbar
-- Or add &DEBUG=YES to URL
```

## Security Architecture

### Security Layers
```
Security Layers
├── Network Security
│   ├── Firewall
│   ├── HTTPS/TLS
│   └── VPN
├── ORDS Security
│   ├── Authentication
│   ├── IP Whitelisting
│   └── Rate Limiting
├── APEX Security
│   ├── Authentication Schemes
│   ├── Authorization Schemes
│   ├── Session State Protection
│   └── Input Validation
└── Database Security
    ├── User Privileges
    ├── VPD (Virtual Private Database)
    ├── Encryption (TDE)
    └── Audit Logging
```

### SQL Injection Prevention
```sql
-- VULNERABLE (never do this)
SELECT * FROM employees WHERE last_name = ''' || :P10_SEARCH || '''';

-- SAFE (use bind variables)
SELECT * FROM employees WHERE last_name = :P10_SEARCH;

-- SAFE (APEX built-in protection)
-- All APEX items automatically use bind variables
```

## Best Practices

### Architecture Best Practices
1. **Separate concerns**: Database (data), APEX (presentation), PL/SQL (business logic)
2. **Use connection pooling**: Configure ORDS for optimal performance
3. **Implement caching**: Use page/region cache for static content
4. **Plan for scalability**: Design for horizontal scaling (multiple ORDS instances)
5. **Security in depth**: Multiple security layers
6. **Monitor proactively**: Set up monitoring and alerting
7. **Version control**: Export and commit APEX applications regularly
8. **Document architecture**: Maintain architecture diagrams and documentation

### Development Best Practices
1. **Use workspaces**: Separate dev, test, prod workspaces
2. **Naming conventions**: Consistent naming for items, processes, etc.
3. **Shared components**: Maximize reuse
4. **Modular design**: Break complex applications into multiple apps
5. **Error handling**: Comprehensive error handling in PL/SQL
6. **Testing**: Unit, integration, and performance testing
7. **Documentation**: Comment complex processes and business logic

---

**Summary**: Understanding APEX architecture—from database to browser—is essential for building robust, scalable applications. Leverage APEX's built-in features, follow best practices, and design with security and performance in mind.
