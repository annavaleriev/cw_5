import configparser  # Импорт библиотеки configparser, это библиотека для работы с файлами конфигурации.

from settings import DATABASE_CONFIG_PATH  # Импорт переменной DATABASE_CONFIG_PATH из файла settings.py

import psycopg2  # Импорт библиотеки psycopg2, это библиотека для работы с базой данных PostgreSQL из Python.
from psycopg2.extras import RealDictCursor  # Импорт библиотеки RealDictCursor - Этот тип курсора возвращает
# результаты запроса в виде словаря, где ключами являются имена столбцов,
# а значениями - соответствующие значения в строке результата.

# Чтение кофигурационного файла
config = configparser.ConfigParser()  # Создание объекта класса ConfigParser из библиотеки configparser
config.read(DATABASE_CONFIG_PATH)  # Чтение файла конфигурации базы данных


class DBManager:  # Создание контекстного менеджера внутри класса DBManager
    """ Класс для работы с базой данных, подключение, отключение базе данных"""

    def __init__(self):  # Инициализация класса
        self.cursor = None  # Создание атрибута cursor, который будет использоваться для выполнения запросов к базе данных
        self.connection = None  # Создание атрибута connection, который будет использоваться для подключения к базе данных

    def __enter__(self):
        """Метод для подключения к базе данных"""
        try:  # Обработка исключений, если подключение не удалось
            self.connection = psycopg2.connect(**config['database'], cursor_factory=RealDictCursor)
            # Подключение к базе данных
            self.cursor = self.connection.cursor()  # Создание курсора, который будет использоваться для выполнения запросов
        except psycopg2.OperationalError:  # Обработка исключений. OperationalError - это класс исключения, который
            # предоставляется библиотекой psycopg2 для обработки ошибок, связанных с операциями, связанными
            # с базой данных PostgreSQL.
            raise ValueError("Не удалось подключиться к базе данных")  # Вывод ошибки, если подключение не удалось
        return self  # Возврат значения, если подключение удалось. self - это объект класса

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для отключения от базы данных"""
        self.cursor.close()  # Закрытие курсора
        self.connection.close()  # Закрытие соединения


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


service = Service()  # Создание объекта класса Service. Для того чтобы использовать методы класса Service
db_manager = DBManager()  # Создание объекта класса DBManager. Для того чтобы использовать методы класса DBManager

service.manager = db_manager  # Установка значения атрибута manager объекта service. Для того чтобы использовать
# методы класса DBManager
# print(service.get_all_vacancies())  # Вызов метода get_aLL_vacancies объекта service.
# print(service.get_companies_and_vacancies_count()[0]['name_company'])  # Вызов метода get_companies_and_vacancies_count объекта service
# print(service.get_avg_salary())  # Вызов метода get_avg_salary объекта service
# print(service.get_vacancies_with_higher_salary())  # Вызов метода get_vacancies_with_higher_salary объекта service
# print(service.get_vacancies_with_keyword('моряк'))  # Вызов метода get_vacancies_with_keyword объекта service


