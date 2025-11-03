-- CRUD Application Template for Oracle APEX
-- Replace placeholders: {TABLE_NAME}, {APP_NAME}, {PRIMARY_KEY}

-- Create sequence
CREATE SEQUENCE {TABLE_NAME}_seq START WITH 1000;

-- Create table with audit columns
CREATE TABLE {TABLE_NAME} (
    {PRIMARY_KEY} NUMBER PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    description VARCHAR2(500),
    status VARCHAR2(20) DEFAULT 'ACTIVE',
    created_by VARCHAR2(50),
    created_date DATE,
    updated_by VARCHAR2(50),
    updated_date DATE
);

-- Create trigger
CREATE OR REPLACE TRIGGER {TABLE_NAME}_biu_trg
BEFORE INSERT OR UPDATE ON {TABLE_NAME}
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        :NEW.{PRIMARY_KEY} := {TABLE_NAME}_seq.NEXTVAL;
        :NEW.created_by := v('APP_USER');
        :NEW.created_date := SYSDATE;
    END IF;
    IF UPDATING THEN
        :NEW.updated_by := v('APP_USER');
        :NEW.updated_date := SYSDATE;
    END IF;
END;
/

-- APEX Application Structure:
-- Page 1: Home Dashboard
-- Page 10: List (Interactive Grid)
-- Page 20: Form (Create/Edit)

-- Page 10: Interactive Grid
SELECT * FROM {TABLE_NAME} WHERE status = 'ACTIVE'

-- Page 20: Form with Automatic Row Processing (DML)
-- Items: P20_{PRIMARY_KEY}, P20_NAME, P20_DESCRIPTION, P20_STATUS
-- Process: Form - Automatic Row Processing (DML)
