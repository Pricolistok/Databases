DROP FUNCTION IF EXISTS get_related_specialists(INT) CASCADE;

CREATE OR REPLACE FUNCTION get_related_specialists(_specialist_id INT)
RETURNS TABLE(
    specialist_id INT,
    first_name TEXT,
    last_name TEXT,
    level INT
) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE related(specialist_id, first_name, last_name, level, path) AS (
        -- начальный уровень
        SELECT s.specialist_id, s.first_name, s.last_name, 0, ARRAY[s.specialist_id]::INT[]
        FROM Specialists s
        WHERE s.specialist_id = _specialist_id

        UNION ALL

        -- рекурсивный уровень
        SELECT s2.specialist_id, s2.first_name, s2.last_name, r.level + 1, r.path || s2.specialist_id
        FROM related r
        JOIN Records rec1 ON rec1.specialist_id = r.specialist_id
        JOIN Records rec2 ON rec1.client_id = rec2.client_id
        JOIN Specialists s2 ON s2.specialist_id = rec2.specialist_id
        WHERE s2.specialist_id <> ALL(r.path)
    )
    SELECT DISTINCT r.specialist_id, r.first_name, r.last_name, r.level
    FROM related r;
END;
$$ LANGUAGE plpgsql;

-- Пример вызова
SELECT * FROM get_related_specialists(3);
