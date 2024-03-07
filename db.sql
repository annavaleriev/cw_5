CREATE TABLE vacancy
(
	name_vacancy varchar NOT NULL,
	salary_from integer,
	salary_to integer,
	salary_currency varchar,
	alternate_url varchar NOT NULL,
	id_employer integer NOT NULL
);

CREATE TABLE company
(
	id_company integer PRIMARY KEY,
	name_company varchar NOT NULL,
	url_vacancies varchar NOT NULL
);