import time
import psycopg2
import os
import random
from datetime import datetime

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5433'),
    'user': os.getenv('DB_USER', 'prico'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'database': 'postgres'
}

def wait_for_db(max_retries=30, retry_interval=2):
    """Ожидание готовности базы данных"""
    print("Ожидание готовности PostgreSQL...")
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("PostgreSQL готов!")
            return True
        except psycopg2.OperationalError as e:
            print(f"Попытка {i+1}/{max_retries}: PostgreSQL еще не готов...")
            time.sleep(retry_interval)
    
    print("Не удалось подключиться к PostgreSQL")
    return False

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_data():
    """Добавление новых записей"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Получаем существующие ID
            cursor.execute("SELECT client_id FROM Clients ORDER BY random() LIMIT 1")
            client_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT specialist_id FROM Specialists ORDER BY random() LIMIT 1")
            specialist_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT services_id FROM Services ORDER BY random() LIMIT 1")
            services_id = cursor.fetchone()[0]
            
            # Добавляем новую запись
            cursor.execute("""
                INSERT INTO Records (client_id, specialist_id, services_id, comment)
                VALUES (%s, %s, %s, %s)
            """, (client_id, specialist_id, services_id, f"Новая запись {datetime.now()}"))
            
            conn.commit()
            print(f"{datetime.now()}: Добавлена новая запись")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
    finally:
        conn.close()

def delete_data():
    """Удаление последних записей"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Records 
                WHERE record_id IN (
                    SELECT record_id FROM Records 
                    ORDER BY record_id DESC 
                    LIMIT 2
                )
            """)
            conn.commit()
            print(f"{datetime.now()}: Удалены последние записи")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
    finally:
        conn.close()

def update_data():
    """Обновление комментариев в записях"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE Records 
                SET comment = 'Обновленный комментарий ' || CURRENT_TIMESTAMP::text
                WHERE record_id IN (
                    SELECT record_id FROM Records 
                    ORDER BY random() 
                    LIMIT 3
                )
            """)
            conn.commit()
            print(f"{datetime.now()}: Обновлены комментарии записей")
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
    finally:
        conn.close()

def main():
    # Ожидаем готовности БД
    if not wait_for_db():
        return
    
    operations = [insert_data, delete_data, update_data]
    current_op = 0
    
    print("Скрипт изменения данных запущен...")
    
    while True:
        time.sleep(30)  # Изменяем данные каждые 30 секунд
        
        try:
            operations[current_op]()
            current_op = (current_op + 1) % len(operations)
            
        except Exception as e:
            print(f"Ошибка при изменении данных: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()