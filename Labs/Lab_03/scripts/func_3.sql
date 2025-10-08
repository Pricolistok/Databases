DROP FUNCTION IF EXISTS CntRecordsClient(int, int);

CREATE OR REPLACE FUNCTION GetSpecilistsWithAge(FindAge_1 int, FindAge_2 int)
RETURNS table(
	specialist_id INT,
	first_name TEXT, 
	last_name TEXT, 
	birth_date DATE
) AS $$
DECLARE cur_year int;
BEGIN 
	cur_year := EXTRACT(YEAR FROM CURRENT_DATE);
	RETURN QUERY 
	SELECT s.specialist_id, s.first_name, s.last_name, s.birth_date FROM specialists s WHERE (cur_year - EXTRACT(YEAR FROM s.birth_date)) = FindAge_1;

	RETURN QUERY 
		SELECT s1.specialist_id, s1.first_name, s1.last_name, s1.birth_date FROM specialists s1 WHERE (cur_year - EXTRACT(YEAR FROM s1.birth_date)) = FindAge_2;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM GetSpecilistsWithAge(110, 20);
