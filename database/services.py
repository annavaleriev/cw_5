import requests

from api.vacancy import Vacancy
from database.managers import DBManager
from settings import COMPANIES_JSON_PATH, URL_HH
from utils import load_jsonfile


class Service:
    """Класс для работы с базой данных"""
    __manager = None  # Создание атрибута класса __manager, который будет использоваться для работы с базой данных

    @property  # Декоратор для создания свойства manager
    def manager(self):
        """Метод для получения значения атрибута __manager"""
        if self.__manager is None:  # Проверка, если атрибут __manager не установлен
            raise NotImplementedError("""Менеджер базы данных не установлен. " 
                                       Пожалуйста, установите менеджер перед выполнением операции.""")  # Вывод ошибки
        return self.__manager  # Возврат значения атрибута __manager

    @manager.setter  # Декоратор для установки значения атрибута __manager
    def manager(self, obj):
        """Метод для установки значения атрибута __manager"""
        if not isinstance(obj, DBManager):  # Проверка, если объект не является экземпляром класса DBManager
            raise ValueError("""Неверный тип объекта для установки атрибута manager. 
                                Ожидается объект класса DBManager или его подкласса.""")  # Вывод ошибки
        self.__manager = obj  # Установка значения атрибута __manager

    def get_all_vacancies(self):
        """ Метод, который получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT name_company, name_vacancy, salary_from, salary_to, alternate_url
                    FROM vacancy
                    JOIN company ON company.id_company = vacancy.id_employer;
                """
            )
            # Выполнение запроса
            return manager.cursor.fetchall()  # Возврат результата запроса

    def get_companies_and_vacancies_count(self):
        """Метод, который получает список всех компаний и количество вакансий в каждой из них."""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT name_company, COUNT(*) 
                    FROM company
                    INNER JOIN vacancy ON company.id_company = vacancy.id_employer
                    GROUP BY name_company;
                """
            )  # Выполнение запроса
            return manager.cursor.fetchall()  # Возврат результата запроса

    def get_avg_salary(self):
        """Метод, который получает среднюю зарплату по всем вакансиям."""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT AVG((salary_from + salary_to)/2)  AS avg_salary
                    FROM vacancy
                """
            )  # Выполнение запроса
            return manager.cursor.fetchall()  # Возврат результата запроса

    def get_vacancies_with_higher_salary(self):
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT name_vacancy
                    FROM vacancy
                    WHERE ((salary_from) + (salary_to)) / 2 >
                    (SELECT  AVG((salary_from + salary_to)/2) AS salary_avg 
                    FROM vacancy)
                """
            )  # Выполнение запроса
            return manager.cursor.fetchall()  # Возврат результата запроса

    def get_vacancies_with_keyword(self, keyword):
        """Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT name_vacancy
                    FROM vacancy
                    WHERE name_vacancy ILIKE %s
                """,
                (f"%{keyword}%",)
            )  # Выполнение запроса,
            # передача параметра в запрос в виде кортежа (f"%{keyword}%",)
            return manager.cursor.fetchall()  # Возврат результата запроса

    def load_companies(self):
        """Метод, который загружает данные о компаниях в базу данных"""
        companies = load_jsonfile(COMPANIES_JSON_PATH)  # Загрузка данных о компаниях из файла
        with self.manager as manager:  # Открытие контекстного менеджера
            companies_data = []  # Создание списка для хранения данных о компаниях
            for company in companies:  # Перебор всех компаний
                companies_data.append(tuple(company.values()))  # Добавление данных о компании в список

            query = """ 
                        INSERT INTO company (name_company, id_hh_company)
                        VALUES (%s, %s)
                    
            """
            manager.cursor.executemany(query, companies_data)  # Выполнение запроса
            manager.connection.commit()  # Сохранение изменений в базе данных

    def load_vacancies_to_db(self, keyword=None, company_id=None):
        """Метод, который загружает данные о вакансиях в базу данных"""
        params = {
            "area": 1,  # Москва
            "per_page": 100, # Количество вакансий на странице
            "page": 0 # Номер страницы
        }

        all_vacancies = [] # Создание списка для хранения всех вакансий

        while True: # Бесконечный цикл
            response = requests.get(URL_HH, params=params)  # Отправка запроса на сервер
            if response.status_code == 200: # Проверка, если статус код ответа 200
                data = response.json()  # Получение данных из ответа
                vacancies = data.get("items", []) # Получение списка вакансий из данных
                all_vacancies.extend(vacancies) # Добавление вакансий в список всех вакансий

                if len(vacancies) < params["per_page"]: # Проверка, если количество вакансий меньше, чем на странице
                    break # Выход из цикла

                params["page"] += 1 # Увеличение номера страницы на 1
            else: # Проверка, если статус код ответа не равен 200
                print("Ошибка при получении данных", response.status_code) # Вывод сообщения об ошибке
                break # Выход из цикла

        with self.manager as manager: # Открытие контекстного менеджера
            for vacancy_data in all_vacancies: # Перебор всех вакансий
                vacancy = Vacancy.get_vacancy_hh(vacancy_data) # Получение данных о вакансии
                vacancy_dict = vacancy.get_vacancy_dict() # Получение словаря с данными о вакансии

                query = """
                                    INSERT INTO vacancy (name_vacancy, salary_from, salary_to, currency, area, url, id_employer)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """ # Запрос на добавление данных о вакансии в базу данных

            values = ( # Значения для добавления в базу данных
                vacancy_dict["name"],
                vacancy_dict["salary_from"],
                vacancy_dict["salary_to"],
                vacancy_dict["currency"],
                vacancy_dict["area"],
                vacancy_dict["url"],
                vacancy_dict["employer_id"]
            )
            manager.cursor.execute(query, values) # Выполнение запроса
        manager.connection.commit() # Сохранение изменений в базе данных

