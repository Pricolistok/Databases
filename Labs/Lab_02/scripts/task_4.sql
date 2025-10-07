SELECT record_id, client_id, specialist_id, services_id
FROM Records
WHERE client_id IN (
  SELECT client_id
  FROM Clients
  WHERE email LIKE '%.com'
)
AND specialist_id = 1;
