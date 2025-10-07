SELECT s.services_id, s.price, s.title,
       AVG(srv.price) AS avg_price,
       MIN(srv.price) AS min_price
FROM Services s
LEFT JOIN Records r ON r.services_id = s.services_id
LEFT JOIN Services srv ON r.services_id = srv.services_id
WHERE s.services_id IS NOT NULL
GROUP BY s.services_id, s.price, s.title;
