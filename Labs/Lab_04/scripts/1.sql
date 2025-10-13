CREATE OR REPLACE FUNCTION get_full_name(entity TEXT, entity_id INT)
RETURNS TEXT
LANGUAGE plpython3u
AS $$
if entity not in ('client','specialist'):
    plpy.error("entity must be 'client' or 'specialist'")

if entity == 'client':
    sql = "SELECT first_name, last_name FROM Clients WHERE client_id = %s" % entity_id
else:
    sql = "SELECT first_name, last_name FROM Specialists WHERE specialist_id = %s" % entity_id

q = plpy.execute(sql)

if len(q) == 0:
    return None

row = q[0]
return "{} {}".format(row['first_name'], row['last_name'])
$$;

SELECT get_full_name('client', 1);

