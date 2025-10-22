# app.py
from database import execute_query, query_drop


def display_menu():
    """Отобразить меню"""
    print("\n" + "=" * 50)
    print("Лабораторная работа №6 - Доступ к данным РБД")
    print("=" * 50)
    print("1. Скалярный запрос")
    print("2. Запрос с JOIN")
    print("3. CTE с оконными функциями")
    print("4. Запрос к метаданным")
    print("5. Вызвать скалярную функцию")
    print("6. Вызвать табличную функцию")
    print("7. Вызвать хранимую процедуру")
    print("8. Вызвать системную функцию")
    print("9. Создать таблицу")
    print("10. Вставить данные")
    print("0. Выход")
    print("=" * 50)


def scalar_query():
    """1. Скалярный запрос - количество клиентов"""
    print("\n--- Количество клиентов ---")
    query = "SELECT COUNT(*) FROM Clients;"
    result = execute_query(query, fetch=True)
    if result:
        print(f"Всего клиентов: {result[0][0]}")


def join_query():
    """2. Запрос с несколькими JOIN"""
    print("\n--- Записи с детальной информацией ---")
    query = """
    SELECT r.record_id, c.first_name, c.last_name, s.first_name, sv.title, r.comment
    FROM Records r
    JOIN Clients c ON r.client_id = c.client_id
    JOIN Specialists s ON r.specialist_id = s.specialist_id
    JOIN Services sv ON r.services_id = sv.services_id
    LIMIT 10;
    """
    result = execute_query(query, fetch=True)
    if result:
        for row in result:
            print(f"Запись {row[0]}: {row[1]} {row[2]} -> {row[3]} | Услуга: {row[4]}")


def cte_window_query():
    """3. CTE с оконными функциями"""
    print("\n--- Статистика по услугам ---")
    query = """
    WITH service_stats AS (
        SELECT 
            s.title,
            s.price,
            COUNT(r.record_id) as usage_count,
            RANK() OVER (ORDER BY COUNT(r.record_id) DESC) as rank
        FROM Services s
        LEFT JOIN Records r ON s.services_id = r.services_id
        GROUP BY s.services_id, s.title, s.price
    )
    SELECT title, price, usage_count, rank
    FROM service_stats
    ORDER BY rank;
    """
    result = execute_query(query, fetch=True)
    if result:
        for row in result:
            print(f"Услуга: {row[0]} | Цена: {row[1]} | Использований: {row[2]} | Ранг: {row[3]}")


def metadata_query():
    """4. Запрос к метаданным"""
    print("\n--- Информация о таблицах ---")
    query = """
    SELECT table_name, table_type 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """
    result = execute_query(query, fetch=True)
    if result:
        for row in result:
            print(f"Таблица: {row[0]} ({row[1]})")


def call_scalar_function():
    """5. Вызов скалярной функции"""
    print("\n--- Количество записей клиента ---")

    # Сначала удаляем старую функцию, затем создаем новую
    drop_func = "DROP FUNCTION IF EXISTS CntRecordsClient(integer);"
    execute_query(drop_func)

    # Создаем исправленную функцию с явным указанием таблицы
    create_func = """
    CREATE OR REPLACE FUNCTION CntRecordsClient(input_id INT)
    RETURNS INT AS $$
    DECLARE 
        record_count INT;
    BEGIN
        SELECT COUNT(*) INTO record_count 
        FROM records 
        WHERE records.client_id = input_id;
        RETURN record_count;
    END; $$ LANGUAGE plpgsql;
    """
    execute_query(create_func)

    try:
        client_id = int(input("Введите ID клиента: "))
        query = "SELECT CntRecordsClient(%s);"
        result = execute_query(query, (client_id,), fetch=True)
        if result:
            print(f"Количество записей для клиента {client_id}: {result[0][0]}")
    except ValueError:
        print("Ошибка: ID клиента должен быть числом")


def call_table_function():
    """6. Вызов табличной функции"""
    print("\n--- Специалисты по возрасту ---")

    # Создаем функцию если её нет
    create_func = """
    CREATE OR REPLACE FUNCTION GetSpecialistsWithAge(min_age INT)
    RETURNS TABLE(
        specialist_id INT,
        first_name TEXT, 
        last_name TEXT, 
        birth_date DATE
    ) AS $$
    BEGIN 
        RETURN QUERY 
        SELECT s.specialist_id, s.first_name, s.last_name, s.birth_date 
        FROM Specialists s 
        WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birth_date)) > min_age;
    END; $$ LANGUAGE plpgsql;
    """
    execute_query(create_func)

    try:
        age = int(input("Введите минимальный возраст: "))
        query = "SELECT * FROM GetSpecialistsWithAge(%s);"
        result = execute_query(query, (age,), fetch=True)
        if result:
            if len(result) == 0:
                print("Специалисты не найдены")
            else:
                print("Найденные специалисты:")
                for row in result:
                    print(f"ID: {row[0]}, Имя: {row[1]} {row[2]}, Дата рождения: {row[3]}")
    except ValueError:
        print("Ошибка: возраст должен быть числом")


def call_stored_procedure():
    """7. Вызов хранимой процедуры"""
    print("\n--- Выбор процедуры ---")
    print("1 - Добавить запись")
    print("2 - Связанные клиенты")
    print("3 - Услуги клиента")
    print("4 - Метаданные таблицы")

    choice = input("Выберите процедуру (1-4): ")

    if choice == '1':
        # Создаем процедуру если её нет
        create_proc = """
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
        END; $$;
        """
        execute_query(create_proc)

        try:
            client_id = int(input("ID клиента: "))
            specialist_id = int(input("ID специалиста: "))
            services_id = int(input("ID услуги: "))
            comment = input("Комментарий: ")
            query = "CALL add_record(%s, %s, %s, %s)"
            result = execute_query(query, (client_id, specialist_id, services_id, comment))
            if result:
                print("Запись успешно добавлена!")
        except ValueError:
            print("Ошибка: ID должны быть числами")

    elif choice == '2':
        try:
            client_id = int(input("ID клиента: "))
            query = "CALL get_connected_clients(%s)"
            result = execute_query(query, (client_id,))
            if result:
                print("Процедура выполнена успешно!")
        except ValueError:
            print("Ошибка: ID клиента должен быть числом")

    elif choice == '3':
        try:
            client_id = int(input("ID клиента: "))
            query = "CALL get_client_services(%s)"
            result = execute_query(query, (client_id,))
            if result:
                print("Процедура выполнена успешно!")
        except ValueError:
            print("Ошибка: ID клиента должен быть числом")

    elif choice == '4':
        table_name = input("Имя таблицы: ")
        query = "CALL show_table_metadata(%s)"
        result = execute_query(query, (table_name,))
        if result:
            print("Процедура выполнена успешно!")


def call_system_function():
    """8. Вызов системной функции"""
    print("\n--- Системная информация ---")
    query = "SELECT version(), current_database(), current_user, now();"
    result = execute_query(query, fetch=True)
    if result:
        print(f"PostgreSQL: {result[0][0]}")
        print(f"База данных: {result[0][1]}")
        print(f"Пользователь: {result[0][2]}")
        print(f"Текущее время: {result[0][3]}")


def create_table():
    """9. Создать таблицу"""
    print("\n--- Создание таблицы отзывов ---")
    query = """
    CREATE TABLE IF NOT EXISTS Reviews (
        review_id SERIAL PRIMARY KEY,
        client_id INT NOT NULL,
        specialist_id INT NOT NULL,
        rating INT CHECK (rating >= 1 AND rating <= 5),
        comment TEXT,
        created_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (client_id) REFERENCES Clients(client_id),
        FOREIGN KEY (specialist_id) REFERENCES Specialists(specialist_id)
    );
    """
    result = execute_query(query)
    if result:
        print("Таблица Reviews создана успешно!")


def insert_data():
    """10. Вставить данные"""
    print("\n--- Добавление отзыва ---")

    # Сначала создаем таблицу если её нет
    create_table()

    try:
        client_id = int(input("ID клиента: "))
        specialist_id = int(input("ID специалиста: "))
        rating = int(input("Оценка (1-5): "))
        comment = input("Комментарий: ")

        query = """
        INSERT INTO Reviews (client_id, specialist_id, rating, comment)
        VALUES (%s, %s, %s, %s);
        """
        result = execute_query(query, (client_id, specialist_id, rating, comment))
        if result:
            print("Отзыв добавлен успешно!")
    except ValueError:
        print("Ошибка: ID и оценка должны быть числами")

def dropper():
    try:
        query = """
        DROP DATABASE CRM;
        """
        query_drop(query)

        print("БД Удалена!")
    except ValueError:
        print("Ошибка")


def main():
    """Главная функция"""
    while True:
        display_menu()
        choice = input("Выберите пункт: ")

        if choice == '0':
            print("Выход из программы")
            break

        options = {
            '1': scalar_query,
            '2': join_query,
            '3': cte_window_query,
            '4': metadata_query,
            '5': call_scalar_function,
            '6': call_table_function,
            '7': call_stored_procedure,
            '8': call_system_function,
            '9': create_table,
            '10': insert_data,
            '11': dropper
        }

        if choice in options:
            options[choice]()
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()