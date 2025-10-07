WITH cte AS (
  SELECT r.specialist_id, COUNT(*) AS number_of_appointments
  FROM Records r
  WHERE r.specialist_id IS NOT NULL
  GROUP BY r.specialist_id
)
SELECT AVG(number_of_appointments) AS avg_appointments_per_specialist
FROM cte;
