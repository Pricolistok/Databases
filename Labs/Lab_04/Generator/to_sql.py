from random import randint
from faker import Faker

fake = Faker()

CNT_CLIENTS = 5000
CNT_SPECIALISTS = 3000
CNT_SERVICES = 2000
CNT_RECORDS = 5000

emails = []

def main():
    with open("insert_data.sql", "w", encoding='utf-8') as file:
        file.write("INSERT INTO Clients (first_name, last_name, birth_date, email) VALUES\n")
        for i in range(CNT_CLIENTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            file.write(f"('{first_name}', '{last_name}', '{birth_day}', '{email}')")
            if i != CNT_CLIENTS - 1:
                file.write(",\n")
            else:
                file.write(";\n")

        file.write("INSERT INTO Specialists (first_name, last_name, birth_date, email) VALUES\n")
        for i in range(CNT_SPECIALISTS):
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_day = fake.date_of_birth()
            email = fake.email()
            while email in emails:
                email = fake.email()
            emails.append(email)
            file.write(f"('{first_name}', '{last_name}', '{birth_day}', '{email}')")
            if i != CNT_SPECIALISTS - 1:
                file.write(",\n")
            else:
                file.write(";\n")

        file.write("INSERT INTO Services (title, description, price) VALUES\n")
        for i in range(CNT_SERVICES):
            title = fake.word()
            description = fake.text()
            price = randint(0, 10000)
            file.write(f"('{title}', '{description}', {price})")
            if i != CNT_SERVICES - 1:
                file.write(",\n")
            else:
                file.write(";\n")

        file.write("INSERT INTO Records (client_id, specialist_id, services_id, comment) VALUES\n")
        for i in range(CNT_RECORDS):
            client_id = randint(1, CNT_CLIENTS)
            specialist_id = randint(1, CNT_SPECIALISTS)
            services_id = randint(1, CNT_SERVICES)
            comment = fake.text().replace("\n", " ")
            file.write(f"({client_id}, {specialist_id}, {services_id}, '{comment}')")
            if i != CNT_RECORDS - 1:
                file.write(",\n")
            else:
                file.write(";\n")


if __name__ == '__main__':
    main()