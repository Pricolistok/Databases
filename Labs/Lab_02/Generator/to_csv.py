from random import randint
from faker import Faker
import csv
import os
import uuid
from datetime import datetime
import time
import json

fake = Faker()

CNT_CLIENTS = 50
CNT_SPECIALISTS = 30
CNT_SERVICES = 20
CNT_RECORDS = 50

emails = []

# Папки для разных форматов
OUTPUT_DIRS = {
    'csv': os.path.join(os.path.dirname(__file__), "csv_input"),
    'json': os.path.join(os.path.dirname(__file__), "json_input"),
    'xml': os.path.join(os.path.dirname(__file__), "xml_input")
}

# Создаем папки если их нет
for dir_path in OUTPUT_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

def generate_clients():
    # CSV
    filename_csv = f"{uuid.uuid4().hex}_Clients_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath_csv = os.path.join(OUTPUT_DIRS['csv'], filename_csv)
    
    with open(filepath_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["first_name", "last_name", "birth_date", "email"])
        for _ in range(CNT_CLIENTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            writer.writerow([first_name, last_name, birth_day, email])
    
    # JSON
    filename_json = f"{uuid.uuid4().hex}_Clients_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    filepath_json = os.path.join(OUTPUT_DIRS['json'], filename_json)
    
    clients_data = []
    for _ in range(CNT_CLIENTS):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_day = fake.date_of_birth()
        email = fake.email()
        while email in emails:
            email = fake.email()
        emails.append(email)
        
        clients_data.append({
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_day.isoformat(),
            "email": email
        })
    
    with open(filepath_json, "w", encoding='utf-8') as file:
        json.dump(clients_data, file, indent=2, ensure_ascii=False)
    
    print(f"Created: {filename_csv} and {filename_json}")

def generate_specialists():
    # CSV
    filename_csv = f"{uuid.uuid4().hex}_Specialists_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath_csv = os.path.join(OUTPUT_DIRS['csv'], filename_csv)
    
    with open(filepath_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["first_name", "last_name", "birth_date", "email"])
        for _ in range(CNT_SPECIALISTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            writer.writerow([first_name, last_name, birth_day, email])
    
    # JSON
    filename_json = f"{uuid.uuid4().hex}_Specialists_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    filepath_json = os.path.join(OUTPUT_DIRS['json'], filename_json)
    
    specialists_data = []
    for _ in range(CNT_SPECIALISTS):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_day = fake.date_of_birth()
        email = fake.email()
        while email in emails:
            email = fake.email()
        emails.append(email)
        
        specialists_data.append({
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_day.isoformat(),
            "email": email
        })
    
    with open(filepath_json, "w", encoding='utf-8') as file:
        json.dump(specialists_data, file, indent=2, ensure_ascii=False)
    
    print(f"Created: {filename_csv} and {filename_json}")

def generate_services():
    # CSV
    filename_csv = f"{uuid.uuid4().hex}_Services_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath_csv = os.path.join(OUTPUT_DIRS['csv'], filename_csv)
    
    with open(filepath_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "description", "price"])
        for _ in range(CNT_SERVICES):
            title = fake.word()
            description = fake.text()
            price = randint(0, 10000)
            writer.writerow([title, description, price])
    
    # JSON
    filename_json = f"{uuid.uuid4().hex}_Services_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    filepath_json = os.path.join(OUTPUT_DIRS['json'], filename_json)
    
    services_data = []
    for _ in range(CNT_SERVICES):
        title = fake.word()
        description = fake.text()
        price = randint(0, 10000)
        
        services_data.append({
            "title": title,
            "description": description,
            "price": price
        })
    
    with open(filepath_json, "w", encoding='utf-8') as file:
        json.dump(services_data, file, indent=2, ensure_ascii=False)
    
    print(f"Created: {filename_csv} and {filename_json}")

def generate_records():
    # CSV
    filename_csv = f"{uuid.uuid4().hex}_Records_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filepath_csv = os.path.join(OUTPUT_DIRS['csv'], filename_csv)
    
    with open(filepath_csv, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["client_id", "specialist_id", "services_id", "comment"])
        for _ in range(CNT_RECORDS):
            client_id = randint(1, CNT_CLIENTS)
            specialist_id = randint(1, CNT_SPECIALISTS)
            services_id = randint(1, CNT_SERVICES)
            comment = fake.text().replace("\n", " ")
            writer.writerow([client_id, specialist_id, services_id, comment])
    
    # JSON
    filename_json = f"{uuid.uuid4().hex}_Records_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    filepath_json = os.path.join(OUTPUT_DIRS['json'], filename_json)
    
    records_data = []
    for _ in range(CNT_RECORDS):
        client_id = randint(1, CNT_CLIENTS)
        specialist_id = randint(1, CNT_SPECIALISTS)
        services_id = randint(1, CNT_SERVICES)
        comment = fake.text().replace("\n", " ")
        
        records_data.append({
            "client_id": client_id,
            "specialist_id": specialist_id,
            "services_id": services_id,
            "comment": comment
        })
    
    with open(filepath_json, "w", encoding='utf-8') as file:
        json.dump(records_data, file, indent=2, ensure_ascii=False)
    
    print(f"Created: {filename_csv} and {filename_json}")

if __name__ == "__main__":
    while True:
        generate_clients()
        generate_specialists()
        generate_services()
        generate_records()
        print("Waiting 5 minutes for next generation...")
        time.sleep(5 * 60)  # пауза 5 минут