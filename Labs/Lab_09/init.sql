-- Создание таблиц (ваша структура)
CREATE TABLE IF NOT EXISTS Clients(
    client_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date Date,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Specialists(
    specialist_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date Date,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Services(
    services_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price Int NOT NULL,
    CONSTRAINT check_price CHECK (price >= 0 AND price <= 1000000)
);

CREATE TABLE IF NOT EXISTS Records(
    record_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    specialist_id INT NOT NULL,
    services_id INT NOT NULL,
    comment TEXT,
    CONSTRAINT fk_clients FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
    CONSTRAINT fk_specialists FOREIGN KEY (specialist_id) REFERENCES Specialists(specialist_id) ON DELETE CASCADE,
    CONSTRAINT fk_services FOREIGN KEY (services_id) REFERENCES Services(services_id) ON DELETE CASCADE
);

-- Наполнение данными
INSERT INTO Clients (first_name, last_name, birth_date, email) VALUES
('Иван', 'Иванов', '1990-05-15', 'ivanov@mail.ru'),
('Петр', 'Петров', '1985-08-20', 'petrov@mail.ru'),
('Мария', 'Сидорова', '1992-03-10', 'sidorova@mail.ru'),
('Анна', 'Кузнецова', '1988-11-25', 'kuznetsova@mail.ru'),
('Сергей', 'Смирнов', '1995-07-03', 'smirnov@mail.ru'),
('Ольга', 'Попова', '1991-09-14', 'popova@mail.ru'),
('Алексей', 'Васильев', '1987-12-30', 'vasilev@mail.ru'),
('Елена', 'Новикова', '1993-04-18', 'novikova@mail.ru');

INSERT INTO Specialists (first_name, last_name, birth_date, email) VALUES
('Дмитрий', 'Фролов', '1980-06-12', 'frolov@company.ru'),
('Наталья', 'Орлова', '1983-02-28', 'orlova@company.ru'),
('Артем', 'Лебедев', '1978-09-05', 'lebedev@company.ru'),
('Ирина', 'Волкова', '1986-07-19', 'volkova@company.ru');

INSERT INTO Services (title, description, price) VALUES
('Консультация', 'Первичная консультация специалиста', 2000),
('Диагностика', 'Полная диагностика состояния', 5000),
('Лечение', 'Комплексное лечение', 15000),
('Массаж', 'Расслабляющий массаж', 3000),
('Чистка', 'Профилактическая чистка', 2500),
('Обследование', 'Расширенное обследование', 8000);

INSERT INTO Records (client_id, specialist_id, services_id, comment) VALUES
(1, 1, 1, 'Первичный прием'),
(2, 2, 2, 'Плановое обследование'),
(3, 3, 3, 'Курс лечения'),
(4, 4, 4, 'Расслабляющая процедура'),
(5, 1, 5, 'Профилактика'),
(6, 2, 6, 'Расширенная диагностика'),
(7, 3, 1, 'Повторная консультация'),
(8, 4, 2, 'Ежегодный осмотр'),
(1, 2, 3, 'Продолжение лечения'),
(2, 3, 4, 'Массаж спины'),
(3, 4, 5, 'Гигиеническая чистка'),
(4, 1, 6, 'Комплексное обследование'),
(5, 2, 1, 'Срочная консультация'),
(6, 3, 2, 'Диагностика по жалобам'),
(7, 4, 3, 'Назначение лечения'),
(8, 1, 4, 'Релаксационный массаж');