CREATE TEMP TABLE best_selling AS
SELECT s.services_id,
       COUNT(r.record_id) AS bookings,
       SUM(s.price)::money AS revenue
FROM Records r
JOIN Services s ON r.services_id = s.services_id
WHERE s.services_id IS NOT NULL
GROUP BY s.services_id;
