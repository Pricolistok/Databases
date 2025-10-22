import psycopg2
from config import DB_CONFIG, DB_CONFIG_DROP


def get_connection():
    """Получить соединение с базой данных"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

def get_connection_drop():
    """Получить соединение с базой данных"""
    try:
        conn = psycopg2.connect(**DB_CONFIG_DROP)
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    """Выполнить запрос к базе данных"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                conn.close()
                return result
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        conn.rollback()
        conn.close()
        return None


def query_drop(query, params=None, fetch=False):
    conn = get_connection_drop()
    if not conn:
        return None

    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                conn.close()
                return result
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        conn.rollback()
        conn.close()
        return None