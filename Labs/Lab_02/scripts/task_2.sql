SELECT DISTINCT clients.client_id, clients.first_name, clients.birth_date
FROM clients WHERE clients.birth_date BETWEEN '1997-01-01' AND '2000-01-01';