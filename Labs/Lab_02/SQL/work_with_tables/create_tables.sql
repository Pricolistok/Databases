CREATE TABLE Clients(
	client_id SERIAL PRIMARY KEY,
	first_name TEXT,
	last_name TEXT,
	birth_date Date,
	email TEXT
);

CREATE TABLE Specialists(
	specialist_id SERIAL PRIMARY KEY,
	first_name TEXT,
	last_name TEXT,
	birth_date Date,
	email TEXT
);

CREATE TABLE Services(
	services_id SERIAL PRIMARY KEY,
	title TEXT,
	description TEXT,
	price Int
);

CREATE TABLE Records(
	record_id SERIAL PRIMARY KEY,
	client_id INT,
	specialist_id INT,
	services_id INT,
	comment TEXT
);

