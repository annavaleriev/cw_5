CREATE TABLE company
(
	id_company serial  PRIMARY KEY,
	name_company varchar NOT NULL,
	id_hh_company varchar NOT NULL
);

CREATE TABLE vacancy
(
	id_vacancy serial PRIMARY key, 
	name_vacancy varchar NOT NULL,
	salary_from integer,
	salary_to integer,
	salary_currency varchar,
	alternate_url varchar NOT NULL,
	id_employer integer references company(id_company)
);