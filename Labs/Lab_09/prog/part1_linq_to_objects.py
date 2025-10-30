from py_linq import Enumerable
import datetime

def run():

    clients = [
        {"client_id": 1, "first_name": "Ivan", "last_name": "Petrov", "birth_date": datetime.date(1990, 3, 2), "email": "ivan@mail.com"},
        {"client_id": 2, "first_name": "Anna", "last_name": "Sidorova", "birth_date": datetime.date(2001, 7, 14), "email": "anna@mail.com"},
        {"client_id": 3, "first_name": "Oleg", "last_name": "Ivanov", "birth_date": datetime.date(1985, 11, 29), "email": "oleg@mail.com"},
    ]

    services = [
        {"services_id": 1, "title": "Massage"},
        {"services_id": 2, "title": "Haircut"},
    ]

    records = [
        {"client_id": 1, "services_id": 1},
        {"client_id": 2, "services_id": 2},
    ]

    clients_enum = Enumerable(clients)

    before_1990 = clients_enum.where(lambda c: c["birth_date"].year < 1990)
    print("Клиенты, рождённые до 1990:", list(before_1990))

    sorted_clients = clients_enum.order_by(lambda c: c["last_name"])
    print("Сортировка по фамилии:", [c["last_name"] for c in sorted_clients])

    emails = clients_enum.select(lambda c: c["email"])
    print("Список email:", list(emails))

    grouped = clients_enum.group_by(key_names=["initial"], key=lambda c: c["last_name"][0])
    print("Группировка по первой букве фамилии:")
    for g in grouped:
        print(g.key.initial, [c["last_name"] for c in g])

    client_records = [
        {"client": c["first_name"], "service_id": r["services_id"]}
        for r in records
        for c in clients
        if r["client_id"] == c["client_id"]
    ]

    full_join = [
        {"client": cr["client"], "service": s["title"]}
        for cr in client_records
        for s in services
        if cr["service_id"] == s["services_id"]
    ]

    print("Join клиентов и услуг:", full_join)
