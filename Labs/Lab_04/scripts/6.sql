DROP TYPE IF EXISTS Person CASCADE;

CREATE TYPE Person AS (
    first_name TEXT,
    last_name  TEXT,
    birth_date DATE
);

DROP FUNCTION IF EXISTS person_from_client(INT);

CREATE OR REPLACE FUNCTION person_from_client(p_client_id INT)
RETURNS Person
LANGUAGE plpython3u
AS $$
if p_client_id is None:
    plpy.error("client_id cannot be NULL")

sql = f"""
    SELECT first_name, last_name, birth_date
    FROM Clients
    WHERE client_id = {p_client_id}
"""
q = plpy.execute(sql)

if len(q) == 0:
    return None

row = q[0]
return (row['first_name'], row['last_name'], row['birth_date'])
$$;

SELECT person_from_client(1);
