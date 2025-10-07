DELETE FROM Services s
WHERE NOT EXISTS (
  SELECT 1
  FROM Records r
  WHERE r.services_id = s.services_id
);
