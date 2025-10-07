SELECT s.services_id,
       s.price,
       (SELECT AVG(s2.price)
        FROM Records r2
        JOIN Services s2 ON r2.services_id = s2.services_id
        WHERE r2.services_id = s.services_id) AS avg_booked_price,
       (SELECT MIN(s3.price)
        FROM Records r3
        JOIN Services s3 ON r3.services_id = s3.services_id
        WHERE r3.services_id = s.services_id) AS min_booked_price,
       s.title
FROM Services s
WHERE s.price IS NOT NULL;
