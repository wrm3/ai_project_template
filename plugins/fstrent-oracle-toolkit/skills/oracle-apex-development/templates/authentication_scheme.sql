-- Custom Authentication Scheme Template

-- Authentication Function
CREATE OR REPLACE FUNCTION custom_auth(
    p_username IN VARCHAR2,
    p_password IN VARCHAR2
) RETURN BOOLEAN
IS
    l_password_hash VARCHAR2(4000);
    l_stored_hash VARCHAR2(4000);
    l_is_valid BOOLEAN := FALSE;
BEGIN
    -- Hash the provided password
    l_password_hash := DBMS_CRYPTO.HASH(
        UTL_RAW.CAST_TO_RAW(p_password || 'SALT'),
        DBMS_CRYPTO.HASH_SH256
    );
    
    -- Get stored hash
    SELECT password_hash
    INTO l_stored_hash
    FROM app_users
    WHERE username = p_username
    AND active_flag = 'Y';
    
    -- Compare hashes
    IF l_password_hash = l_stored_hash THEN
        -- Update last login
        UPDATE app_users
        SET last_login = SYSDATE
        WHERE username = p_username;
        COMMIT;
        
        l_is_valid := TRUE;
    END IF;
    
    RETURN l_is_valid;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN FALSE;
    WHEN OTHERS THEN
        apex_debug.error('Authentication error: %s', SQLERRM);
        RETURN FALSE;
END custom_auth;
/

-- APEX Authentication Scheme Configuration:
-- Name: Custom Database Authentication
-- Scheme Type: Custom
-- Authentication Function: custom_auth
