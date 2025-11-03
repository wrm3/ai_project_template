-- Interactive Report Template with Drill-Down

-- Main Report Query
SELECT id,
       name,
       status,
       created_date,
       APEX_PAGE.GET_URL(
           p_page => 20,
           p_items => 'P20_ID',
           p_values => id
       ) AS edit_link
FROM {TABLE_NAME}
WHERE (:P10_SEARCH IS NULL 
   OR UPPER(name) LIKE '%' || UPPER(:P10_SEARCH) || '%')
AND (:P10_STATUS IS NULL OR status = :P10_STATUS)

-- Interactive Report Features:
-- - Search Bar
-- - Actions Menu
-- - Download (CSV, PDF)
-- - Subscription
-- - Saved Reports
