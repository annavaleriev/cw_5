import psycopg2

from DBManager import DBManager
from utils import get_company, get_vacancy_hh

list_id_company = ('3127', '10521060', '5267014', '15478', '84585', '1740', '697715', '903111', '39305', '2180')

list_company = get_company(list_id_company)
list_vacancy_company = get_vacancy_hh(list_company)

try:
    with psycopg2.connect(
            dbname="north",
            user="postgres",
            password="30051980",  # вспомнить как прятать пароль
            host="localhost") as conn:
        with conn.cursor() as cursor:
            cursor.exsecutemany('INSERT INTO company VALUES (%s, %s, %s)', list_company), #С помощью метода executemany()
            # курсора выполняются SQL-запросы для массовой вставки данных в таблицу company и vacancy.
            cursor.exsecutemany('INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)', list_vacancy_company)
            #Вместо %s в SQL-запросах используются заполнители, которые будут заменены данными из списка list_company
            # и list_vacancy_company.
finally:
    conn.close()


test_DBManager = DBManager()
print(test_DBManager.get_companies_and_vacancies_count())
print(test_DBManager.get_all_vacancies())
print(test_DBManager.get_avg_salary())
print(test_DBManager.get_vacancies_with_higher_salary())
print(test_DBManager.get_vacancies_with_keyword('Python'))
