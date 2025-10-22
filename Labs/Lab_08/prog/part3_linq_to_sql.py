from db.db_utils import select_query, modify_query

def run():
    print("\n=== LINQ to SQL ===")

    print("Клиенты, родившиеся после 1995:")
    rows = select_query("SELECT first_name, last_name, birth_date FROM clients WHERE birth_date > '1995-01-01'")
    for r in rows:
        print(r)

    print("\nЗаписи с клиентами и услугами:")
    query = """
        SELECT c.first_name, c.last_name, s.title, r.comment
        FROM records r
        JOIN clients c ON r.client_id = c.client_id
        JOIN services s ON r.services_id = s.services_id;
    """
    for row in select_query(query):
        print(row)

    modify_query("INSERT INTO services (title, description, price) VALUES (%s, %s, %s)", ("TempService", "Temp", 100))
    modify_query("UPDATE services SET price = %s WHERE title = %s", (200, "TempService"))
    modify_query("DELETE FROM services WHERE title = %s", ("TempService",))


    print("\nКлиенты, рождённые до 1990 (через процедуру):")
    rows = select_query("SELECT * FROM get_clients_by_year(%s)", (1990,))
    for r in rows:
        print(r)
