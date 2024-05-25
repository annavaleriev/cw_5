from database.managers import DBManager
from settings import COMPANIES_JSON_PATH
from utils import load_jsonfile


class Service:
    """Класс для работы с базой данных"""
    __manager = None

    @property
    def manager(self):
        """Метод для получения значения атрибута __manager"""
        if self.__manager is None:
            raise NotImplementedError("""Менеджер базы данных не установлен. "
                                       Пожалуйста, установите менеджер перед выполнением операции.""")
        return self.__manager

    @manager.setter
    def manager(self, obj):
        """Метод для установки значения атрибута __manager"""
        if not isinstance(obj, DBManager):
            raise ValueError("""Неверный тип объекта для установки атрибута manager.
                                Ожидается объект класса DBManager или его подкласса.""")
        self.__manager = obj

    def get_all_vacancies(self):
        """ Метод, который получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT name_company, name_vacancy, salary_from, salary_to, alternate_url
                    FROM vacancy
                    JOIN company ON company.id_company = vacancy.id_employer;
                """
            )
            return manager.cursor.fetchall()

    def get_companies_and_vacancies_count(self):
        """Метод, который получает список всех компаний и количество вакансий в каждой из них."""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT name_company, COUNT(*)
                    FROM company
                    INNER JOIN vacancy ON company.id_company = vacancy.id_employer
                    GROUP BY name_company;
                """
            )
            return manager.cursor.fetchall()

    def get_avg_salary(self):
        """Метод, который получает среднюю зарплату по всем вакансиям."""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT AVG((salary_from + salary_to)/2)  AS avg_salary
                    FROM vacancy
                """
            )
            return manager.cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT name_vacancy, salary_from, salary_to, salary_currency, alternate_url
                    FROM vacancy
                    WHERE ((salary_from) + (salary_to)) / 2 >
                    (SELECT  AVG((salary_from + salary_to)/2) AS salary_avg
                    FROM vacancy)
                """
            )
            return manager.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT name_company, name_vacancy, salary_from, salary_to, salary_currency, alternate_url
                    FROM vacancy
                    LEFT JOIN company
                    ON vacancy.id_employer = company.id_company
                    WHERE name_vacancy ILIKE %s
                """,
                (f"%{keyword}%",)
            )
            return manager.cursor.fetchall()

    def load_companies(self):
        """Метод, который загружает данные о компаниях в базу данных"""
        companies = load_jsonfile(COMPANIES_JSON_PATH)
        with self.manager as manager:

            query = """
                        INSERT INTO company (name_company, id_hh_company)
                        VALUES (%(name)s,%(id)s)                    
            """
            manager.cursor.executemany(query, companies)
            manager.connection.commit()

    def get_companies_ids(self):
        """Метод, который получает id компаний из базы данных"""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    SELECT id_hh_company
                    FROM company
                """
            )
            companies = manager.cursor.fetchall()
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
                """
                manager.cursor.execute(query, vacancy)

            manager.connection.commit()

    def drop_vacancies(self):
        """Метод, который удаляет данные о вакансиях из базы данных"""
        with self.manager as manager:
            manager.cursor.execute(
                """
                    DELETE FROM vacancy
                """
            )
        manager.connection.commit()
