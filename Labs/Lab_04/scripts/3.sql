CREATE OR REPLACE FUNCTION records_for_client(p_client_id INT)
RETURNS TABLE(
    record_id INT,
    client_id INT,
    specialist_id INT,
    services_id INT,
    service_title TEXT,
    specialist_name TEXT,
    comment TEXT
)
LANGUAGE plpython3u
AS $$
if p_client_id is None:
    plpy.error("client_id cannot be NULL")

sql = f"""
    SELECT r.record_id,
           r.client_id,
           r.specialist_id,
           r.services_id,
           s.title AS service_title,
           sp.first_name || ' ' || sp.last_name AS specialist_name,
           r.comment
    FROM Records r
    JOIN Services s ON r.services_id = s.services_id
    JOIN Specialists sp ON r.specialist_id = sp.specialist_id
    WHERE r.client_id = {p_client_id}
    ORDER BY r.record_id;
"""

res = plpy.execute(sql)
return res
$$;

SELECT * FROM records_for_client(1);
