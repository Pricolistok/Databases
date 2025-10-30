import time
import json
import logging
import psycopg2
import redis
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Параметры подключения
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5433'),
    'user': os.getenv('DB_USER', 'prico'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'database': 'postgres'
}

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': 6379,
    'db': 0
}

def wait_for_db(max_retries=30, retry_interval=2):
    """Ожидание готовности базы данных"""
    logger.info("Ожидание готовности PostgreSQL...")
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            logger.info("PostgreSQL готов!")
            return True
        except psycopg2.OperationalError as e:
            logger.info(f"Попытка {i+1}/{max_retries}: PostgreSQL еще не готов...")
            time.sleep(retry_interval)
    
    logger.error("Не удалось подключиться к PostgreSQL")
    return False

def wait_for_redis(max_retries=10, retry_interval=1):
    """Ожидание готовности Redis"""
    logger.info("Ожидание готовности Redis...")
    for i in range(max_retries):
        try:
            redis_client = redis.Redis(**REDIS_CONFIG)
            redis_client.ping()
            logger.info("Redis готов!")
            return True
        except redis.ConnectionError as e:
            logger.info(f"Попытка {i+1}/{max_retries}: Redis еще не готов...")
            time.sleep(retry_interval)
    
    logger.error("Не удалось подключиться к Redis")
    return False

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_redis_connection():
    return redis.Redis(**REDIS_CONFIG)

# Статистический запрос: топ-5 самых популярных услуг
def get_top_services_from_db():
    query = """
    SELECT s.services_id, s.title, COUNT(r.record_id) as record_count
    FROM Services s
    JOIN Records r ON s.services_id = r.services_id
    GROUP BY s.services_id, s.title
    ORDER BY record_count DESC
    LIMIT 5;
    """
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [{'id': row[0], 'title': row[1], 'count': row[2]} for row in results]
    finally:
        conn.close()

def get_top_services_from_cache(redis_client):
    cache_key = "top_5_services"
    
    # Пытаемся получить данные из кэша
    start_time = time.time()
    cached_data = redis_client.get(cache_key)
    cache_get_time = time.time() - start_time
    
    if cached_data is not None:
        logger.info("Данные получены из кэша Redis")
        return json.loads(cached_data), cache_get_time
    else:
        # Данных в кэше нет, запрашиваем из БД
        db_start_time = time.time()
        data_from_db = get_top_services_from_db()
        db_query_time = time.time() - db_start_time
        
        # Сохраняем в кэш на 5 секунд
        cache_set_start = time.time()
        redis_client.setex(cache_key, 5, json.dumps(data_from_db))
        cache_set_time = time.time() - cache_set_start
        
        total_cache_time = cache_get_time + db_query_time + cache_set_time
        logger.info(f"Данные получены из БД и сохранены в кэш")
        
        return data_from_db, total_cache_time

def measure_performance():
    # Ожидаем готовности БД и Redis
    if not wait_for_db():
        return
    
    if not wait_for_redis():
        return
    
    redis_client = get_redis_connection()
    
    # Создаем папку для результатов
    os.makedirs('/app/results', exist_ok=True)
    results_file = f'/app/results/results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # Заголовок CSV файла
    with open(results_file, 'w') as f:
        f.write("timestamp,direct_query_time,cached_query_time,data_state\n")
    
    iteration = 0
    data_states = ['stable', 'inserting', 'deleting', 'updating']
    current_state_index = 0
    
    logger.info("Начало измерения производительности...")
    
    try:
        while True:
            iteration += 1
            current_state = data_states[current_state_index]
            
            # Замер времени прямого запроса к БД
            db_start_time = time.time()
            direct_data = get_top_services_from_db()
            direct_query_time = (time.time() - db_start_time) * 1000  # в миллисекундах
            
            # Замер времени запроса через кэш
            cached_data, cached_query_time = get_top_services_from_cache(redis_client)
            cached_query_time_ms = cached_query_time * 1000  # в миллисекундах
            
            timestamp = datetime.now().isoformat()
            
            # Запись результатов
            with open(results_file, 'a') as f:
                f.write(f"{timestamp},{direct_query_time:.4f},{cached_query_time_ms:.4f},{current_state}\n")
            
            logger.info(f"Итерация {iteration}: "
                       f"Прямой запрос: {direct_query_time:.2f} мс, "
                       f"Через кэш: {cached_query_time_ms:.2f} мс, "
                       f"Состояние: {current_state}")
            
            # Вывод текущих данных (для отладки)
            if iteration % 10 == 0:
                logger.info(f"Текущий топ услуг: {direct_data}")
            
            # Смена состояния данных каждые ~30 секунд (6 итераций по 5 секунд)
            if iteration % 6 == 0:
                current_state_index = (current_state_index + 1) % len(data_states)
                logger.info(f"Смена состояния данных на: {data_states[current_state_index]}")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("Приложение остановлено")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    measure_performance()