-- APEX RESTful Service Template

-- Module: {module_name}.v1
-- Base Path: /{resource}/

-- GET Handler (Single Record)
-- Template: /:id
-- Method: GET
SELECT {columns}
FROM {TABLE_NAME}
WHERE {PRIMARY_KEY} = :id

-- GET Handler (Collection)
-- Template: /
-- Method: GET
SELECT {columns}
FROM {TABLE_NAME}
WHERE (:status IS NULL OR status = :status)
ORDER BY created_date DESC

-- POST Handler (Create)
-- Method: POST
DECLARE
    l_id NUMBER;
BEGIN
    INSERT INTO {TABLE_NAME} (name, description, status)
    VALUES (
        apex_json.get_varchar2('name'),
        apex_json.get_varchar2('description'),
        apex_json.get_varchar2('status')
    ) RETURNING {PRIMARY_KEY} INTO l_id;
    
    :status_code := 201;
    apex_json.open_object;
    apex_json.write('id', l_id);
    apex_json.write('message', 'Created successfully');
    apex_json.close_object;
END;

-- PUT Handler (Update)
-- Template: /:id
-- Method: PUT
UPDATE {TABLE_NAME}
SET name = apex_json.get_varchar2('name'),
    description = apex_json.get_varchar2('description')
WHERE {PRIMARY_KEY} = :id

-- DELETE Handler
-- Template: /:id
-- Method: DELETE
DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = :id
