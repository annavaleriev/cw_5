import json

from api.hh import ApiHH
from api.vacancy import Vacancy
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

    choice = input("Введите номер пункта: ")
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
            salary_currency = item.get('salary_currency', '')
            salary_from = item.get('salary_from', "")
            salary_to = item.get('salary_to', "")
            alternate_url = item.get('alternate_url', 'Не указана')
            name_vacancy = item.get('name_vacancy', 'Не указана')
            name_company = item.get('name_company', 'Не указана')
            id_employer = item.get('id_employer', '')
            vacancy = Vacancy(
                name_vacancy,
                salary_from,
                salary_to,
                salary_currency,
                alternate_url,
                id_employer
            )
            print(
                f"Компания: {name_company}, Вакансия: {name_vacancy}, "
                f"Зарплата: {vacancy.work_with_salary}, {alternate_url}"
            )

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
            salary_currency = item.get('salary_currency', '')
            salary_from = item.get('salary_from', "")
            salary_to = item.get('salary_to', "")
            alternate_url = item.get('alternate_url', 'Не указана')
            name_vacancy = item.get('name_vacancy', 'Не указана')
            id_employer = item.get('id_employer', '')
            vacancy = Vacancy(
                name_vacancy,
                salary_from,
                salary_to,
                salary_currency,
                alternate_url,
                id_employer
            )
            print(
                f" Вакансия: {name_vacancy}, "
                f"Зарплата: {vacancy.work_with_salary}, {alternate_url}"
            )

    elif choice == "5":
        keyword = input("Введите ключевое слово для поиска: ").lower()
        vacancies = service.get_vacancies_with_keyword(keyword)
        if not vacancies:
            print("Вакансий по данному ключевому слову не найдено!")
        else:
            all_vacancies_json = (covert_to_json(vacancies))
            data = json.loads(all_vacancies_json)
            for item in data:
                salary_currency = item.get('salary_currency', '')
                salary_from = item.get('salary_from', "")
                salary_to = item.get('salary_to', "")
                alternate_url = item.get('alternate_url', 'Не указана')
                name_vacancy = item.get('name_vacancy', 'Не указана')
                id_employer = item.get('id_employer', '')
                vacancy = Vacancy(
                    name_vacancy,
                    salary_from,
                    salary_to,
                    salary_currency,
                    alternate_url,
                    id_employer
                )
                print(
                    f" Вакансия: {name_vacancy}, "
                    f"Зарплата: {vacancy.work_with_salary}, {alternate_url}"
                )
    else:
        print("Некорректный ввод команды! Попробуйте еще раз!")
