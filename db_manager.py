import psycopg2  # Импорт библиотеки psycopg2, это библиотека для работы с базой данных PostgreSQL из Python.
from psycopg2.extras import RealDictCursor  # Импорт библиотеки RealDictCursor - Этот тип курсора возвращает
# результаты запроса в виде словаря, где ключами являются имена столбцов,
# а значениями - соответствующие значения в строке результата.


class DBManager:  # Создание контекстного менеджера внутри класса DBManager
    """ Класс для работы с базой данных, подключение, отключение базе данных"""

    def __init__(self):  # Инициализация класса
        self.cursor = None  # Создание атрибута cursor, который будет использоваться для выполнения запросов к базе данных
        self.connection = None  # Создание атрибута connection, который будет использоваться для подключения к базе данных

    def __enter__(self):
        """Метод для подключения к базе данных"""
        try:  # Обработка исключений, если подключение не удалось
            self.connection = psycopg2.connect(dbname='vacancy', user='postgres', password='30051980', host='localhost',
                                               cursor_factory=RealDictCursor)  # Подключение к базе данных
            #TODO актуальные данные подключения и спрятать. Или не тут прятать?
            self.cursor = self.connection.cursor()  # Создание курсора, который будет использоваться для выполнения запросов
        except psycopg2.OperationalError:  # Обработка исключений. OperationalError - это класс исключения, который
            # предоставляется библиотекой psycopg2 для обработки ошибок, связанных с операциями, связанными с базой данных PostgreSQL.
            raise ValueError("Не удалось подключиться к базе данных")  # Вывод ошибки, если подключение не удалось
        return self  # Возврат значения, если подключение удалось. self - это объект класса

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для отключения от базы данных"""
        self.cursor.close()  # Закрытие курсора
        self.connection.close()  # Закрытие соединения

    def get_all_vacancies(self):
        """ Метод, который получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute("""SELECT name_company, name_vacancy, salary_from, salary_to, alternate_url
                                        FROM vacancy
                                        INNER JOIN company ON company.id_company = vacancy.id_employer""")
        # TODO: Проверить запрос,ошибка Unable to resolve column 'name_company'
        # Выполнение запроса. Метод execute - это метод объекта курсора (cursor), который используется для выполнения
        # SQL-запросов к базе данных. Он позволяет отправлять SQL-запросы на сервер базы данных PostgreSQL
        # для выполнения и получения результата.
        return self.cursor.fetchall()  # Возврат результата запроса, который был выполнен методом execute.
        # Метод fetchall() является одним из методов объекта курсора в библиотеке psycopg2 и используется
        # для извлечения всех строк результата выполнения запроса к базе данных.


class Service:
    __manager = None

    @property
    def manager(self):
        if self.__manager is None:
            raise NotImplementedError("afsdfjksdghfjk")
        return self.__manager

    @manager.setter
    def manager(self, obj):
        if not isinstance(obj, DBManager):
            raise ValueError("sdfljkhsdjkfghsdkhfgsdkhjfg")
        self.__manager = obj

    def get_vacancies(self):
        with self.manager as manager:
            manager.cursor.execute("dsfdsfdsfsdf")
            return manager.cursor.fetchall()


service = Service()
db_manager = DBManager()

service.manager = db_manager
service.get_vacancies()
