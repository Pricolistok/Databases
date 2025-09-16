ALTER TABLE Records
ADD CONSTRAINT fk_clients
FOREIGN KEY (client_id)
REFERENCES Clients(client_id)
ON DELETE CASCADE;

ALTER TABLE Records
ADD CONSTRAINT fk_specialists
FOREIGN KEY (specialist_id)
REFERENCES Specialists(specialist_id)
ON DELETE CASCADE;

ALTER TABLE Records
ADD CONSTRAINT fk_services
FOREIGN KEY (services_id)
REFERENCES Services(services_id)
ON DELETE CASCADE;

ALTER TABLE Services
ADD CONSTRAINT check_price
CHECK (price >= 0 AND price <= 1000000);

ALTER TABLE Clients
ADD CONSTRAINT unique_email_clients
UNIQUE(email);

ALTER TABLE Specialists
ADD CONSTRAINT unique_email_specialists
UNIQUE(email);
