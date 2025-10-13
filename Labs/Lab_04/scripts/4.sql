CREATE OR REPLACE FUNCTION create_record(
    in_client_id INT,
    in_specialist_id INT,
    in_services_id INT,
    in_comment TEXT
)
RETURNS INT
LANGUAGE plpython3u
AS $$
q = plpy.execute(f"SELECT 1 FROM Clients WHERE client_id = {in_client_id}")
if len(q) == 0:
    plpy.error(f"Client id {in_client_id} does not exist")

q = plpy.execute(f"SELECT 1 FROM Specialists WHERE specialist_id = {in_specialist_id}")
if len(q) == 0:
    plpy.error(f"Specialist id {in_specialist_id} does not exist")

q = plpy.execute(f"SELECT price FROM Services WHERE services_id = {in_services_id}")
if len(q) == 0:
    plpy.error(f"Service id {in_services_id} does not exist")
price = q[0]['price']
if price is None or price < 0:
    plpy.error("Service price invalid")

ins = plpy.execute(f"""
    INSERT INTO Records(client_id, specialist_id, services_id, comment)
    VALUES ({in_client_id}, {in_specialist_id}, {in_services_id}, {plpy.quote_literal(in_comment)})
    RETURNING record_id
""")

return ins[0]['record_id']
$$;

SELECT create_record(1, 2, 3, 'Первый визит');
