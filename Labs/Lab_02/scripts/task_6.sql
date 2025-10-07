SELECT services_id, title, price
FROM Services
WHERE price > ALL (
  SELECT price
  FROM Services
  WHERE title ILIKE '%basic%'
);
