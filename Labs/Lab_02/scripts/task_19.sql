UPDATE Services
SET price = (
  SELECT AVG(s2.price)
  FROM Records r
  JOIN Services s2 ON r.services_id = s2.services_id
  WHERE s2.services_id = 37
)
WHERE services_id = 37;
