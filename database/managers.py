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
