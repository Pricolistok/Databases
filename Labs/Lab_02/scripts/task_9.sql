SELECT client_id, first_name, last_name,
 CASE EXTRACT(YEAR FROM birth_date)::int
  WHEN EXTRACT(YEAR FROM CURRENT_DATE)::int THEN 'Born this year'
  WHEN (EXTRACT(YEAR FROM CURRENT_DATE)::int - 1) THEN 'Born last year'
  ELSE (EXTRACT(YEAR FROM CURRENT_DATE)::int - EXTRACT(YEAR FROM birth_date)::int)::text || ' years ago'
 END AS when_text
FROM Clients;
