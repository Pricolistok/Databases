CREATE OR REPLACE PROCEDURE get_client_services(p_client_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    cur CURSOR FOR
        SELECT s.title, s.price
        FROM Records r
        JOIN Services s ON r.services_id = s.services_id
        WHERE r.client_id = p_client_id;
BEGIN
    OPEN cur;

    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;

        RAISE NOTICE 'Услуга: %, Цена: %', rec.title, rec.price;
    END LOOP;

    CLOSE cur;
END;
$$;

CALL get_client_services(1);
