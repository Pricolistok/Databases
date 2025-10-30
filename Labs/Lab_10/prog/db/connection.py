import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="crm",
            user="prico",
            password="1234",
            host="localhost",
            port="5433"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к PostgreSQL:", e)
        raise
