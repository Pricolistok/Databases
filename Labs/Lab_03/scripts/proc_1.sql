CREATE OR REPLACE PROCEDURE add_record(
    p_client_id INT,
    p_specialist_id INT,
    p_services_id INT,
    p_comment TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Records(client_id, specialist_id, services_id, comment)
    VALUES (p_client_id, p_specialist_id, p_services_id, p_comment);
    RAISE NOTICE 'Запись добавлена: клиент %, специалист %, услуга %', p_client_id, p_specialist_id, p_services_id;
END;
$$;

CALL add_record(1, 2, 3, 'Первый визит клиента');

