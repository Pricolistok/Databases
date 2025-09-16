CREATE TABLE Clients(
	client_id SERIAL PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	birth_date Date,
	email TEXT NOT NULL
);

CREATE TABLE Specialists(
	specialist_id SERIAL PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	birth_date Date,
	email TEXT NOT NULL
);

CREATE TABLE Services(
	services_id SERIAL PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	price Int NOT NULL
);

CREATE TABLE Records(
	record_id SERIAL PRIMARY KEY,
	client_id INT NOT NULL,
	specialist_id INT NOT NULL,
	services_id INT NOT NULL,
	comment TEXT
);

