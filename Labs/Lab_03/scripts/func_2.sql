DROP FUNCTION IF EXISTS CntRecordsClient(int);

CREATE OR REPLACE FUNCTION GetSpecilistsWithAge(FindAge int)
RETURNS table(
	specialist_id INT,
	first_name TEXT, 
	last_name TEXT, 
	birth_date DATE
) AS $$
BEGIN 
	RETURN QUERY 
	SELECT s.specialist_id, s.first_name, s.last_name, s.birth_date FROM specialists s WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, s.birth_date)) > FindAge;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM GetSpecilistsWithAge(110);
