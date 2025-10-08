CREATE OR REPLACE PROCEDURE show_table_metadata(p_table_name TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;  -- переменная для хранения данных из курсора
    cur CURSOR FOR
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = p_table_name
        ORDER BY ordinal_position;
BEGIN
    OPEN cur;

    RAISE NOTICE 'Структура таблицы "%":', p_table_name;

    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;

        RAISE NOTICE 'Столбец: %, Тип: %, NULL допустим: %',
            rec.column_name, rec.data_type, rec.is_nullable;
    END LOOP;

    CLOSE cur;
END;
$$;

CALL show_table_metadata('clients');

