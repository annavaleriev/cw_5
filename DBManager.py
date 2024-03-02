import psycopg2


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, databasename, user, password, host):
        self.connection = psycopg2.connect(
            dbname=databasename, user=user, password=password, host=host
        )

