/*
    В этой схеме:

    employee_id - уникальный идентификатор сотрудника (primary key)
    name - имя сотрудника
    department - отдел, в котором работает сотрудник (можно хранить строкой или идентификатором)
    employee_id - ссылка на начальника (foreign key, которая ссылается на EmployeeID того же отношения)
*/

CREATE TABLE employee (
  employee_id INTEGER PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  department VARCHAR(50) NOT NULL,
  manager_id INTEGER,
  FOREIGN KEY (manager_id) REFERENCES employee(employee_id)
  UNIQUE (department)
);