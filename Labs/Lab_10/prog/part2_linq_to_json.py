import json
from py_linq import Enumerable
from db.db_utils import select_query

def run():

    try:
        rows = select_query("SELECT client_id, first_name, last_name, birth_date, email FROM clients")
        columns = ["client_id", "first_name", "last_name", "birth_date", "email"]
        clients = [dict(zip(columns, row)) for row in rows]

        with open("clients.json", "w") as f:
            json.dump(clients, f, default=str, indent=4)
        print("JSON файл создан из БД")
    except Exception as e:
        print("Ошибка подключения к PostgreSQL:", e)
        return

    with open("clients.json") as f:
        clients = json.load(f)

    data_enum = Enumerable(clients)

    emails = data_enum.select(lambda c: c["email"])
    print("Email-адреса:", list(emails))

    updated = data_enum.select(
        lambda c: {**c, "email": "new_" + c["email"]} if c["client_id"] == 1 else c
    )
    with open("clients.json", "w") as f:
        json.dump(list(updated), f, default=str, indent=4)
    print("JSON обновлён")

    new_client = {
        "client_id": 999,
        "first_name": "Test",
        "last_name": "User",
        "birth_date": "2000-01-01",
        "email": "test@mail.com"
    }
    new_data = data_enum.concat(Enumerable([new_client]))
    with open("clients.json", "w") as f:
        json.dump(list(new_data), f, default=str, indent=4)
    print("Новый клиент добавлен в JSON")
