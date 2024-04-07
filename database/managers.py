import configparser

from settings import DATABASE_CONFIG_PATH

import psycopg2
from psycopg2.extras import RealDictCursor

config = configparser.ConfigParser()
config.read(DATABASE_CONFIG_PATH)


class DBManager:
    """ Класс для работы с базой данных, подключение, отключение базе данных"""

    def __init__(self):
        self.cursor = None
        self.connection = None

    def __enter__(self):
        """Метод для подключения к базе данных"""
        try:
            self.connection = psycopg2.connect(**config['database'], cursor_factory=RealDictCursor)
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError:
            raise ValueError("Не удалось подключиться к базе данных")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для отключения от базы данных"""
        self.cursor.close()
        self.connection.close()
