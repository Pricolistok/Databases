INSERT INTO Records (client_id, specialist_id, services_id, comment)
SELECT (
  SELECT client_id FROM Clients WHERE email = 'alice@example.com' LIMIT 1
),
1,
services_id,
'Inserted via script'
FROM Services
WHERE title = 'Relaxing Massage';
