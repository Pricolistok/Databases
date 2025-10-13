CREATE OR REPLACE FUNCTION records_before_insert_trg()
RETURNS TRIGGER
LANGUAGE plpython3u
AS $$
client_id = TD['new']['client_id']
service_id = TD['new']['services_id']

q = plpy.execute(f"SELECT birth_date FROM Clients WHERE client_id = {client_id}")
if len(q) == 0:
    plpy.error(f"Client with id {client_id} does not exist")

birth_date = q[0]['birth_date']
if birth_date is None:
    plpy.error("Client birth_date is NULL")

q_age = plpy.execute(f"SELECT EXTRACT(YEAR FROM age(current_date, DATE '{birth_date}')) AS age")
age = q_age[0]['age']

if age < 18:
    plpy.error(f"Client is under 18 (age = {age})")

q = plpy.execute(f"SELECT 1 FROM Services WHERE services_id = {service_id}")
if len(q) == 0:
    plpy.error(f"Service with id {service_id} does not exist")

return "OK"
$$;

DROP TRIGGER IF EXISTS trg_records_before_insert ON Records;

CREATE TRIGGER trg_records_before_insert
BEFORE INSERT ON Records
FOR EACH ROW
EXECUTE FUNCTION records_before_insert_trg();

INSERT INTO Records(client_id, specialist_id, services_id, comment)
VALUES (1, 1, 1, 'Проверка возраста');

