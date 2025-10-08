CREATE OR REPLACE PROCEDURE get_connected_clients(p_client_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        WITH RECURSIVE connected_clients AS (
            SELECT client_id, specialist_id
            FROM Records
            WHERE client_id = p_client_id

            UNION

            SELECT r2.client_id, r2.specialist_id
            FROM Records r2
            INNER JOIN connected_clients cc ON r2.specialist_id = cc.specialist_id
            WHERE r2.client_id != cc.client_id
        )
        SELECT DISTINCT client_id
        FROM connected_clients
        WHERE client_id != p_client_id
    LOOP
        RAISE NOTICE 'Связанный клиент: %', r.client_id;
    END LOOP;
END;
$$;


CALL get_connected_clients(1);
