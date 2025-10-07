SELECT r.specialist_id, sp.first_name || ' ' || sp.last_name AS specialist_name,
       AVG(s.price) AS average_price
FROM Records r
JOIN Services s ON r.services_id = s.services_id
JOIN Specialists sp ON r.specialist_id = sp.specialist_id
GROUP BY r.specialist_id, sp.first_name, sp.last_name
HAVING AVG(s.price) > (SELECT AVG(price) FROM Services);
