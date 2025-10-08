
CREATE TABLE Clients_Log (
    log_id SERIAL PRIMARY KEY,
    client_id INT,
    action TEXT,
    log_time TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_new_client()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Clients_Log (client_id, action, log_time)
    VALUES (NEW.client_id, 'Добавлен новый клиент', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_client_insert
AFTER INSERT ON Clients
FOR EACH ROW
EXECUTE FUNCTION log_new_client();

INSERT INTO Clients (first_name, last_name, birth_date, email)
VALUES ('Иван', 'Петров', '1990-01-01', 'ivan@mail.com'),
       ('Ольга', 'Сидорова', '1995-05-05', 'olga@mail.com');

