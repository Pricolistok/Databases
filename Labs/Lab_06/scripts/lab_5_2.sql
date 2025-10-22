--CREATE TABLE Clients_JSON (
--    id SERIAL PRIMARY KEY,
--    data JSONB
--);

INSERT INTO Clients_JSON (data)
VALUES ('{"first_name": "Ivan", "last_name": "Petrov", "birth_date": "1990-03-01", "email": "ivan@mail.com"}');
