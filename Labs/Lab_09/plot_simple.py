import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Найти последний файл с результатами
results_files = glob.glob('results/results_*.csv')
if not results_files:
    print("Файлы с результатами не найдены!")
    exit()

latest_file = max(results_files, key=os.path.getctime)
print(f"Используется файл: {latest_file}")

df = pd.read_csv(latest_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ИСПРАВЛЕННАЯ СТРОКА: добавлены скобки вокруг figsize
plt.figure(figsize=(12, 8))

# График 1: Сравнение времени запросов
plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['direct_query_time'], label='Прямой запрос к БД', marker='o', linewidth=2)
plt.plot(df['timestamp'], df['cached_query_time'], label='Запрос через Redis кэш', marker='s', linewidth=2)
plt.ylabel('Время (мс)')
plt.title('Сравнение времени выполнения запросов: Прямой запрос к PostgreSQL vs Кэширование через Redis')
plt.legend()
plt.grid(True, alpha=0.3)

# График 2: Выигрыш от кэширования
plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['direct_query_time'] - df['cached_query_time'], 
         label='Выигрыш от кэширования', color='green', marker='^', linewidth=2)
plt.ylabel('Разница (мс)')
plt.xlabel('Время')
plt.title('Выигрыш в производительности при использовании Redis кэша')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results_comparison.png', dpi=300, bbox_inches='tight')
print("График сохранен как 'results_comparison.png'")

# Статистика
print("\n=== СТАТИСТИКА ===")
print(f"Среднее время прямого запроса: {df['direct_query_time'].mean():.2f} мс")
print(f"Среднее время кэшированного запроса: {df['cached_query_time'].mean():.2f} мс")
print(f"Максимальный выигрыш: {(df['direct_query_time'] - df['cached_query_time']).max():.2f} мс")
print(f"Минимальный выигрыш: {(df['direct_query_time'] - df['cached_query_time']).min():.2f} мс")

# Показать график
plt.show()