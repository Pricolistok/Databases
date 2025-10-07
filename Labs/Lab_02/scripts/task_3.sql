SELECT DISTINCT clients.first_name
FROM records JOIN clients ON records.record_id = clients.client_id 
WHERE clients.first_name LIKE '%Tam%';