SELECT DISTINCT c1.email, c1.first_name, c1.birth_date
FROM clients c1 JOIN clients AS c2 ON c2.birth_date = c1.birth_date 
WHERE c2.client_id  <> c1.client_id 
AND c1.birth_date > '2000-01-01'
ORDER BY c1.birth_date , c1.email;
