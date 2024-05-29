from database.managers import DBManager
from database.services import Service


def load_json_to_db():
    """

    """
    db_manager = DBManager()
    service = Service()
    service.manager = db_manager

    service.load_companies()


if __name__ == '__main__':
    load_json_to_db()
