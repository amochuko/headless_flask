DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE departments (
    dept_no char(4) NOT NULL,
    dept_name varchar(40) NOT NULL,
    PRIMARY KEY (dept_no), UNIQUE KEY dept_name (dept_name)
    );

 CREATE TABLE employees (
  emp_no int(11) NOT NULL AUTO_INCREMENT,
  birth_date date NOT NULL,
  first_name varchar(14) NOT NULL,
  last_name varchar(16) NOT NULL,
  gender enum('M','F') NOT NULL,
  hire_date date NOT NULL,
  PRIMARY KEY (emp_no)
  )


