SELECT AVG(TotalPrice) AS actual_avg,
       SUM(TotalPrice) / COUNT(record_id) AS calc_avg
FROM (
  SELECT r.record_id, SUM(s.price) AS TotalPrice
  FROM Records r
  JOIN Services s ON r.services_id = s.services_id
  GROUP BY r.record_id
) AS tot_records;
