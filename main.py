import configparser

import psycopg2

from DBManager import DBManager
from settings import DATABASE_CONFIG_PATH
from utils import get_company, get_vacancy_hh

# Чтение кофигурационного файла
config = configparser.ConfigParser()
config.read(DATABASE_CONFIG_PATH)

# # Получение пароля для подключения к базе данных
# DB_PASSWORD = config['database']['DB_PASSWORD']

# Установка соединения с базой данных. Psycopg2 - это библиотека для работы с базой данных PostgreSQL.
connection = psycopg2.connect(**config['database'])
print()

with connection.cursor() as cursor:
    cursor.execute('SELECT *  FROM vacancy JOIN company using ("id_company")')
    aaaa = cursor.fetchall()
    print(aaaa)





















#
# list_id_company = ('3127', '10521060', '5267014', '15478', '84585', '1740', '697715', '903111', '39305', '2180')
#
# list_company = get_company(list_id_company)
# list_vacancy_company = get_vacancy_hh(list_company)
#
# try:
#     with psycopg2.connect(
#             dbname="north",
#             user="postgres",
#             password="30051980",  # вспомнить как прятать пароль
#             host="localhost") as conn:
#         with conn.cursor() as cursor:
#             cursor.exsecutemany('INSERT INTO company VALUES (%s, %s, %s)', list_company), #С помощью метода executemany()
#             # курсора выполняются SQL-запросы для массовой вставки данных в таблицу company и vacancy.
#             cursor.exsecutemany('INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)', list_vacancy_company)
#             #Вместо %s в SQL-запросах используются заполнители, которые будут заменены данными из списка list_company
#             # и list_vacancy_company.
# finally:
#     conn.close()
#
#
# test_DBManager = DBManager()
# print(test_DBManager.get_companies_and_vacancies_count())
# print(test_DBManager.get_all_vacancies())
# print(test_DBManager.get_avg_salary())
# print(test_DBManager.get_vacancies_with_higher_salary())
# print(test_DBManager.get_vacancies_with_keyword('Моряк'))
#
