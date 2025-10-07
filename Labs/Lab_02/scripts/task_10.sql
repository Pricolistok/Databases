SELECT title,
 CASE
  WHEN price < 10 THEN 'Inexpensive'
  WHEN price < 50 THEN 'Fair'
  WHEN price < 100 THEN 'Expensive'
  ELSE 'Very Expensive'
 END AS price_category
FROM Services;
