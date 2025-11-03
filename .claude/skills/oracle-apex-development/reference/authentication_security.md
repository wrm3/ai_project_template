# Oracle APEX Authentication and Security

## Authentication Schemes

### Database Account
```yaml
Scheme Type: Database Account
Cookie Name: APEX_SESSION
Session Timeout: 3600 seconds
Invalid Session Target: Login page
```

### LDAP Directory
```yaml
Scheme Type: LDAP Directory
LDAP Host: ldap.company.com
LDAP Port: 389
Distinguished Name: CN=%LDAP_USER%,OU=Users,DC=company,DC=com
```

### OAuth 2.0
```yaml
Scheme Type: Social Sign-In
Provider: Google
Client ID: your_client_id.apps.googleusercontent.com
Client Secret: your_client_secret
Scope: email profile
```

## Authorization Schemes

### Role-Based Authorization
```plsql
-- Authorization Scheme: Is Manager
-- Type: PL/SQL Function Returning Boolean

DECLARE
    l_is_manager BOOLEAN;
BEGIN
    SELECT COUNT(*) > 0
    INTO   l_is_manager
    FROM   app_users
    WHERE  username = :APP_USER
    AND    role = 'MANAGER';
    
    RETURN l_is_manager;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END;
```

### Apply to Components
```yaml
Page Authorization:
  Page 100 (Admin): Is Administrator
  Page 20 (Edit Employee): Is Manager

Button Authorization:
  DELETE button: Is Administrator

Item Authorization:
  P20_SALARY: Is Manager or Is HR
```

## Session State Protection

### Enable Protection
```yaml
Session State Protection:
  Application Level: Restricted
  Page Level: Arguments Must Have Checksum
  Item Level: Checksum Required - Session Level

-- Protects against URL tampering
-- Example: /apex/f?p=100:10:SESSION::NO::P10_EMP_ID:1001
-- Requires checksum to modify P10_EMP_ID
```

## SQL Injection Prevention

### Use Bind Variables
```sql
-- VULNERABLE (NEVER DO THIS)
SELECT * FROM employees 
WHERE last_name = ''' || :P10_SEARCH || '''';

-- SAFE (Always use bind variables)
SELECT * FROM employees 
WHERE last_name = :P10_SEARCH;
```

### Dynamic SQL
```plsql
-- When dynamic SQL is necessary
EXECUTE IMMEDIATE 'SELECT * FROM ' || 
                  apex_escape.noop(:P10_TABLE_NAME) || 
                  ' WHERE id = :1'
INTO l_result
USING :P10_ID;
```

## XSS Prevention

### Escape Output
```plsql
-- Display user input safely
:P10_DISPLAY := apex_escape.html(:P10_USER_INPUT);
```

### JavaScript Escaping
```javascript
// In JavaScript
var userName = apex.util.escapeHTML('#P10_USERNAME#');
```

## HTTPS/TLS

### Force HTTPS
```yaml
Application Definition:
  Session Management:
    Require Secure Session State: Yes
    Application Alias: myapp
    
ORDS Configuration:
  standalone.https.port: 8443
  ssl.cert: /path/to/cert.pem
  ssl.cert.key: /path/to/key.pem
```

---

**Summary**: Implement multi-layered security: strong authentication, proper authorization, session protection, SQL injection prevention, XSS escaping, and HTTPS enforcement.
