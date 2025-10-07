\copy Clients(first_name, last_name, birth_date, email) FROM 'Clients.csv' DELIMITER ',' CSV HEADER;

\copy Specialists(first_name, last_name, birth_date, email) FROM 'Specialists.csv' DELIMITER ',' CSV HEADER;

\copy Services(title, description, price) FROM 'Services.csv' DELIMITER ',' CSV HEADER;

\copy Records(client_id, specialist_id, services_id, comment) FROM 'Records.csv' DELIMITER ',' CSV HEADER;