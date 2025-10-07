CREATE TABLE IF NOT EXISTS dbo_myemployees (
  employee_id smallint PRIMARY KEY,
  first_name text NOT NULL,
  last_name text NOT NULL,
  title text NOT NULL,
  dept_id smallint NOT NULL,
  manager_id int NULL
);

INSERT INTO dbo_myemployees (employee_id, first_name, last_name, title, dept_id, manager_id) VALUES
  (1, 'Иван', 'Петров', 'Главный исполнительный директор', 16, NULL),
  (2, 'Анна', 'Сидорова', 'Технический директор', 16, 1),
  (3, 'Пётр', 'Иванов', 'Инженер', 16, 2),
  (4, 'Мария', 'Кузнецова', 'Инженер', 16, 2)
ON CONFLICT (employee_id) DO NOTHING;

WITH DirectReports (manager_id, employee_id, title, dept_id, level) AS (
  -- закреплённый элемент (корень)
  SELECT manager_id, employee_id, title, dept_id, 0 AS level
  FROM dbo_myemployees
  WHERE manager_id IS NULL
  UNION ALL
  -- рекурсивное добавление потомков
  SELECT e.manager_id, e.employee_id, e.title, e.dept_id, dr.level + 1
  FROM dbo_myemployees e
  INNER JOIN DirectReports dr ON e.manager_id = dr.employee_id
)
SELECT manager_id, employee_id, title, dept_id, level
FROM DirectReports;
