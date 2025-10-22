ALTER TABLE Clients
ADD COLUMN details JSONB;

UPDATE Clients
SET details = jsonb_build_object(
    'address', 'Moscow, Lenina 5',
    'phone', '89995554433',
    'preferences', jsonb_build_array('haircut', 'coloring')
)
WHERE client_id = 1;

UPDATE Clients
SET details = jsonb_build_object(
    'address', 'Saint-Petersburg, Nevsky 20',
    'phone', '89997778866',
    'preferences', jsonb_build_array('manicure', 'spa')
)
WHERE client_id = 2;
