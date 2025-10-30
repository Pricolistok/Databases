from random import randint
from faker import Faker
import csv

fake = Faker()

CNT_CLIENTS = 5000
CNT_SPECIALISTS = 3000
CNT_SERVICES = 2000
CNT_RECORDS = 5000

emails = []

def main():
    # Clients.csv
    with open("Clients.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["first_name", "last_name", "birth_date", "email"])
        
        for i in range(CNT_CLIENTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            writer.writerow([first_name, last_name, birth_day, email])

    # Specialists.csv
    with open("Specialists.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["first_name", "last_name", "birth_date", "email"])
        
        for i in range(CNT_SPECIALISTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            writer.writerow([first_name, last_name, birth_day, email])

    # Services.csv
    with open("Services.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "description", "price"])
        
        for i in range(CNT_SERVICES):
            title = fake.word()
            description = fake.text()
            price = randint(0, 10000)
            writer.writerow([title, description, price])

    # Records.csv
    with open("Records.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["client_id", "specialist_id", "services_id", "comment"])
        
        for i in range(CNT_RECORDS):
            client_id = randint(1, CNT_CLIENTS)
            specialist_id = randint(1, CNT_SPECIALISTS)
            services_id = randint(1, CNT_SERVICES)
            comment = fake.text().replace("\n", " ")
            writer.writerow([client_id, specialist_id, services_id, comment])


if __name__ == '__main__':
    main()