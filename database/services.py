from database.managers import DBManager
from settings import COMPANIES_JSON_PATH
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
                    SELECT name_vacancy, salary_from, salary_to, salary_currency, alternate_url
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
                    SELECT name_company, name_vacancy, salary_from, salary_to, salary_currency, alternate_url
                    FROM vacancy
                    LEFT JOIN company 
                    ON vacancy.id_employer = company.id_company
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

            query = """ 
                        INSERT INTO company (name_company, id_hh_company)
                        VALUES (%(name)s, %(id)s)
                    
            """
            manager.cursor.executemany(query, companies)  # Выполнение запроса
            manager.connection.commit()  # Сохранение изменений в базе данных

    def get_companies_ids(self):
        """Метод, который получает id компаний из базы данных"""
        with self.manager as manager:  # Открытие контекстного менеджера
            manager.cursor.execute(
                """
                    SELECT id_hh_company
                    FROM company
                """
            )  # Выполнение запроса
            companies = manager.cursor.fetchall()  # Возврат результата запроса
        companies_ids = []
        for company in companies:
            companies_ids.append(company['id_hh_company'])
        return companies_ids

    def load_vacancies(self, vacancies: list[dict]):
        """Метод, который загружает данные о вакансиях в базу данных"""
        with self.manager as manager:
            for vacancy in vacancies:
                manager.cursor.execute(
                    """
                        SELECT id_company
                        FROM company
                        WHERE id_hh_company = %s
                    """, (vacancy['id_employer'],)
                )
                id_employer = manager.cursor.fetchone()
                vacancy['id_employer'] = id_employer['id_company']

                query = """
                            INSERT INTO vacancy (name_vacancy, salary_from, salary_to, salary_currency, alternate_url, id_employer)
                            VALUES (%(name_vacancy)s, %(salary_from)s, %(salary_to)s, %(salary_currency)s, %(alternate_url)s, %(id_employer)s)
                """  # Запрос на добавление данных о вакансии в базу данных
                manager.cursor.execute(query, vacancy)  # Выполнение запроса

            manager.connection.commit()  # Сохранение изменений в базе данных

    def drop_vacancies(self):
        """Метод, который удаляет данные о вакансиях из базы данных"""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    DELETE FROM vacancy
                """
            )
        manager.connection.commit()
