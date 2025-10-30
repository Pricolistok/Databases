SELECT json_agg(c) AS clients_json
FROM Clients c;

SELECT json_agg(s) AS specialists_json
FROM Specialists s;

SELECT json_agg(sv) AS services_json
FROM Services sv;

SELECT json_agg(r) AS records_json
FROM Records r;

SELECT row_to_json(c)
FROM Clients c;
