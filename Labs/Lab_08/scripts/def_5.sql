DROP FUNCTION IF EXISTS GetSpecilistsWithAge(int);
DROP TABLE IF EXISTS exported_json;

CREATE TABLE exported_json(
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT now(),
    file_path TEXT,
    json_data JSONB
);

CREATE OR REPLACE FUNCTION GetSpecilistsWithAge(FindAge int)
RETURNS void AS $$
DECLARE
    result_json JSONB;
BEGIN
    SELECT jsonb_agg(
        jsonb_build_object(
            'specialist_id', s.specialist_id,
            'first_name', s.first_name,
            'last_name', s.last_name,
            'birth_date', s.birth_date
        )
    )
    INTO result_json
    FROM specialists s
    WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birth_date)) > FindAge;

    IF result_json IS NULL THEN
        RAISE NOTICE 'Нет специалистов старше % лет', FindAge;
        RETURN;
    END IF;

    INSERT INTO exported_json(file_path, json_data)
    VALUES ('/specialists_result.json', result_json);

    RAISE NOTICE 'JSON сохранён в таблицу exported_json';
END;
$$ LANGUAGE plpgsql;


SELECT GetSpecilistsWithAge(110);

COPY (
  SELECT jsonb_pretty(json_data)
  FROM exported_json
  ORDER BY created_at DESC
  LIMIT 1
) TO '/var/lib/postgresql/export/specialists_result.json';




