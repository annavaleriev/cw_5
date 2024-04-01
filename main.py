# from api.api_hh import Api_HH
# from database.db_manager import DBManager, Service
# from settings import COMPANIES_JSON_PATH
# from utils import load_companies
#
#
# def main():
#     database_name = "vacancy"  # имя базы данных
#     id_companies = COMPANIES_JSON_PATH  # путь к файлу с id компаний
#
#     load_file_id_companies = load_companies(id_companies)  # загружаем файл с id компаний
#
#     db_manager = DBManager()  # создаем объект класса DBManager
#     # with db_manager as manager:
#
#     service = Service()  # создаем объект класса Service
#     service.manager = db_manager  # присваиваем атрибуту manager объекта service объект db_manager
#     # чтобы он дальше работал с методами класса DBManager
#
#     hh_api = Api_HH()  # создаем объект класса Api_HH
#
#
#     # for company in load_file_id_companies:  # перебор по  каждой компании в списке компаний
#     #     vacancy_info = hh_api.get_all_vacancies(company["id"])  # получаем список вакансий по id компании
#     # #
#     # vacancy = []  # создаем пустой список vacancy
#     # for vacancy in vacancy_info:  # перебор по каждой вакансии в списке вакансий
#     #     vacancy = Vacancy.get_vacancy_hh(vacancy_info)
#     #     vacancy.append(vacancy)  # добавляем в список vacancy вакансию
#
from api.hh import ApiHH
from database.managers import DBManager
from database.services import Service

# print("""
#     Привет! Выберите один из пунктов,чтобы получить информацию:
#     1. Получить список всех компаний и количество вакансий в каждой из них
#     # 2. Получить список вакансий выбранной компании с подробной информацией
#     2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
#     3. Получить среднюю зарплату по всем вакансиям
#     4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
#     5. Получить список всех вакансий по ключевому слову
#     """)
#
#     choice = input("Введите номер пункта: ")  # ввод номера пункта пользователем
#     if choice == "1":
#         service.get_companies_and_vacancies_count()
#         db_manager.get_companies_and_vacancies_count()
#     # elif choice == "2":
#     #     company_id = int(input("Введите id компании: ")) # это странно, что пользователь должен знать id компании
#     #     hh_api.get_all_vacancies(company_id) # def get_all_vacancies у меня нет запроса на id компании
#     elif choice == "2":
#         service.get_all_vacancies()
#     elif choice == "3":
#         service.get_avg_salary()
#     elif choice == "4":
#         service.get_vacancies_with_higher_salary()
#     elif choice == "5":
#         keyword = input("Введите ключевое слово: ")
#         service.get_vacancies_with_keyword(keyword)
#     else:
#         print("Некорректный ввод команды! Попробуйте еще раз!")


db_manager = DBManager()
hh = ApiHH()


service = Service()
service.manager = db_manager
# service.load_companies()
hhh = service.get_companies_ids()
hh.id_list_company = hhh
all_vac = hh.get_all_vacancies()
print()



# service.get_all_vacancies()