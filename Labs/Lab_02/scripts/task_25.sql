WITH duplicated AS (
  SELECT client_id, specialist_id, services_id, comment FROM Records
  UNION ALL
  SELECT client_id, specialist_id, services_id, comment FROM Records
),
numbered AS (
  SELECT client_id, specialist_id, services_id, comment,
         ROW_NUMBER() OVER (PARTITION BY client_id, specialist_id, services_id, comment ORDER BY client_id) AS rn
  FROM duplicated
)
SELECT client_id, specialist_id, services_id, comment
FROM numbered
WHERE rn = 1;
