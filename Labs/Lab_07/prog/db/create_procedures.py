from db.connection import get_connection

def create_stored_procedures():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE OR REPLACE FUNCTION get_clients_by_year(year_limit INT)
        RETURNS TABLE (
            client_id INT,
            first_name TEXT,
            last_name TEXT,
            birth_date DATE,
            email TEXT
        )
        AS $$
        BEGIN
            RETURN QUERY
            SELECT c.client_id, c.first_name, c.last_name, c.birth_date, c.email
            FROM clients c
            WHERE EXTRACT(YEAR FROM c.birth_date) < year_limit;
        END;
        $$ LANGUAGE plpgsql;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE add_client(
            p_first_name TEXT,
            p_last_name TEXT,
            p_birth_date DATE,
            p_email TEXT
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            INSERT INTO clients(first_name, last_name, birth_date, email)
            VALUES (p_first_name, p_last_name, p_birth_date, p_email);
        END;
        $$;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE update_client_email(
            p_client_id INT,
            p_new_email TEXT
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            UPDATE clients
            SET email = p_new_email
            WHERE client_id = p_client_id;
        END;
        $$;
    """)

    cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_client(p_client_id INT)
        LANGUAGE plpgsql
        AS $$
        BEGIN
            DELETE FROM clients WHERE client_id = p_client_id;
        END;
        $$;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Все процедуры успешно созданы!")

if __name__ == "__main__":
    create_stored_procedures()
