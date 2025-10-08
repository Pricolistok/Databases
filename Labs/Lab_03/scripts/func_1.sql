DROP FUNCTION IF EXISTS CntRecordsClient(TEXT, TEXT, TEXT);

CREATE OR REPLACE FUNCTION CntRecordsClient(firstName_p TEXT, lastName_p TEXT, email_p TEXT)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    result INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO result
    FROM records r
    JOIN clients c ON r.client_id = c.client_id
    WHERE c.first_name = firstName_p
      AND c.last_name = lastName_p
      AND c.email = email_p;

    RETURN result;
END;
$$;



SELECT CntRecordsClient('Jody', 'Garcia', 'conwayjames@example.org');
