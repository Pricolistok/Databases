SELECT client_id,
       details -> 'preferences' AS preferences
FROM Clients;

SELECT client_id,
       details ->> 'address' AS address,
       details ->> 'phone' AS phone
FROM Clients;

SELECT client_id, details
FROM Clients
WHERE details ? 'address';

UPDATE Clients
SET details = jsonb_set(details, '{email_verified}', 'true'::jsonb)
WHERE client_id = 1;

SELECT client_id, jsonb_array_elements(details -> 'preferences') AS preference
FROM Clients;
