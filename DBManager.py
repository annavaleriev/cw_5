import psycopg2


class DBManager:
    """
    Класс для работы с базой данных
    """

    # @staticmethod
    def connect_database(self, sql):
        """
        Метод для подключения к базе данных
        :param sql:
        :return:
        """
        list_sgl = []
        try:
            with psycopg2.connect(
                    dbname="north",
                    user="postgres",
                    password="30051980",  # вспомнить как прятать пароль
                    host="localhost"
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    list_sgl = cursor.fetchall()
        finally:
            conn.close()
        return list_sgl

    def get_companies_and_vacancies_count(self):
        """ Метод, который получает список всех компаний и количество вакансий у каждой компании."""
        return self.connect_database("""SELECT name_company, COUNT(name_vacancy) FROM company
                                     INNER JOIN vacancy ON company.id_company = vacancy.id_employer
                                     GROUP BY name_company""")

    def get_all_vacancies(self):
        """ Метод, который получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию."""
        return self.connect_database("""SELECT name_company, name_vacancy, salary_from, salary_to, alternate_url
                                        FROM vacancy
                                        INNER JOIN company ON company.id_company = vacancy.id_employer""")

    def get_avg_salary(self):
        """" Метод, который получает среднюю зарплату по всем вакансиям."""
        return self.connect_database("""SELECT AVG(salary_from) + AVG(salary_to) /2 AS avg_salary
                                        FROM vacancy""")

    def get_vacancies_with_higher_salary(self):
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        return self.connect_database("""SELECT name_vacancy
                                        FROM vacancy
                                        WHERE (salary_from + salary_to) / 2 >
                                        (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 AS salary_avg 
                                        FROM vacancy)""")

    def get_vacancies_with_keyword(self):
        """ Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        return self.connect_database("""SELECT name_vacancy
                                        FROM vacancy
                                        WHERE name_vacancy LIKE '%{word}%'""")


