CREATE OR REPLACE VIEW AllPeople AS
SELECT client_id AS id, first_name, last_name, birth_date, email, 'Client' AS role
FROM Clients
UNION ALL
SELECT specialist_id AS id, first_name, last_name, birth_date, email, 'Specialist' AS role
FROM Specialists;


CREATE OR REPLACE FUNCTION insert_into_allpeople()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role = 'Client' THEN
        INSERT INTO Clients (first_name, last_name, birth_date, email)
        VALUES (NEW.first_name, NEW.last_name, NEW.birth_date, NEW.email);
    ELSIF NEW.role = 'Specialist' THEN
        INSERT INTO Specialists (first_name, last_name, birth_date, email)
        VALUES (NEW.first_name, NEW.last_name, NEW.birth_date, NEW.email);
    ELSE
        RAISE EXCEPTION 'Неверное значение role. Используйте "Client" или "Specialist".';
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER instead_of_insert_allpeople
INSTEAD OF INSERT ON AllPeople
FOR EACH ROW
EXECUTE FUNCTION insert_into_allpeople();

INSERT INTO AllPeople (first_name, last_name, birth_date, email, role)
VALUES 
('Анна', 'Иванова', '1995-03-14', 'anna@mail.com', 'Client'),
('Павел', 'Сергеев', '1988-07-22', 'pavel@mail.com', 'Specialist');


SELECT * FROM Clients;
SELECT * FROM Specialists;
SELECT * FROM AllPeople;