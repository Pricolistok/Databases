SELECT s.services_id, s.title
FROM Services s
WHERE EXISTS (
  SELECT 1
  FROM Records r
  WHERE r.services_id = s.services_id
);
