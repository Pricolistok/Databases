SELECT 'By units' AS criteria, s.title AS best_selling
FROM Services s
JOIN (
  SELECT services_id, COUNT(*) AS cnt
  FROM Records
  GROUP BY services_id
  ORDER BY cnt DESC
  LIMIT 1
) AS od ON od.services_id = s.services_id
UNION
SELECT 'By revenue' AS criteria, s.title AS best_selling
FROM Services s
JOIN (
  SELECT r.services_id, SUM(s2.price) AS sr
  FROM Records r
  JOIN Services s2 ON r.services_id = s2.services_id
  GROUP BY r.services_id
  ORDER BY sr DESC
  LIMIT 1
) AS od2 ON od2.services_id = s.services_id;
