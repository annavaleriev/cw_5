import json

from api.hh import ApiHH
from database.managers import DBManager
from database.services import Service
from utils import covert_to_json

db_manager = DBManager()
service = Service()
service.manager = db_manager
hh = ApiHH()


def main():

    print("""
    Привет! Выберите один из пунктов,чтобы получить информацию:

    1. Получить список всех компаний и количество вакансий в каждой из них мз базы данных. 
    Компании: Мегафон, Simplenight, SberAutoTech, VK, Авито, Яндекс, Ostrovok.ru, Газпром автоматизация, Газпром нефть, Озон.
    2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
    3. Получить среднюю зарплату по всем вакансиям
    4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
    5. Получить список всех вакансий по ключевому слову
    """)

    choice = input("Введите номер пункта: ")  # ввод номера пункта пользователем
    if choice == "1":
        all_vacancies = service.get_companies_and_vacancies_count()
        all_vacancies_json = (covert_to_json(all_vacancies))
        data = json.loads(all_vacancies_json)
        for item in data:
            print(f"Компания: {item['name_company']}, вакансий в базе: {item['count']}")

    elif choice == "2":
        all_vacancies = service.get_all_vacancies()
        all_vacancies_json = (covert_to_json(all_vacancies))
        data = json.loads(all_vacancies_json)
        for item in data:
            print(
                f"Компания: {item['name_company']}, Вакансия: {item['name_vacancy']}, "
                f"Зарплата: {item['salary_from']} - {item['salary_to']}, {item['alternate_url']}")

    elif choice == "3":
        salary = service.get_avg_salary()
        salary_json = (covert_to_json(salary))
        data = json.loads(salary_json)
        for item in data:
            print(f"Средняя зарплата по всем вакансиям: {item['avg_salary']}.")

    elif choice == "4":
        vacancies = service.get_vacancies_with_higher_salary()
        all_vacancies_json = (covert_to_json(vacancies))
        data = json.loads(all_vacancies_json)
        for item in data:
            print(f" Вакансия: {item['name_vacancy']}, Зарплата: {item['salary_from']} - "
                  f"{item['salary_to']} {item['salary_currency']}, {item['alternate_url']}")

    elif choice == "5":
        keyword = input("Введите ключевое слово для поиска: ").lower()
        vacancies = service.get_vacancies_with_keyword(keyword)
        all_vacancies_json = (covert_to_json(vacancies))
        data = json.loads(all_vacancies_json)
        for item in data:
            print(f" Вакансия: {item['name_vacancy']}, Зарплата: {item['salary_from']} - "
                  f"{item['salary_to']}, {item['alternate_url']}")
    else:
        print("Некорректный ввод команды! Попробуйте еще раз!")
