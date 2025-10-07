SELECT s.services_id, s.price, s.title, srv.price AS record_price,
       AVG(srv.price) OVER (PARTITION BY s.services_id, s.title) AS avg_price,
       MIN(srv.price) OVER (PARTITION BY s.services_id, s.title) AS min_price,
       MAX(srv.price) OVER (PARTITION BY s.services_id, s.title) AS max_price
FROM Services s
LEFT JOIN Records r ON r.services_id = s.services_id
LEFT JOIN Services srv ON r.services_id = srv.services_id;
