-- Form Template with Validations

-- Form Source
SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = :P20_ID

-- Items Configuration
-- P20_ID: Hidden (Primary Key)
-- P20_NAME: Text Field (Required, Max Length 100)
-- P20_EMAIL: Text Field (Required, Email Validation)
-- P20_PHONE: Text Field (Format Mask: (999) 999-9999)
-- P20_STATUS: Select List (LOV: ACTIVE, INACTIVE, PENDING)

-- Validations
-- 1. Name Required
-- 2. Email Format: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$
-- 3. Phone Format: ^\(\d{3}\) \d{3}-\d{4}$
-- 4. Duplicate Check (PL/SQL):
SELECT COUNT(*) FROM {TABLE_NAME}
WHERE name = :P20_NAME AND {PRIMARY_KEY} != NVL(:P20_ID, -1)
HAVING COUNT(*) > 0

-- Process: Form - Automatic Row Processing (DML)
-- Success Message: Record saved successfully
-- Branch: Page 10 (after processing)
