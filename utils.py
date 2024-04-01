import json

from api.vacancy import Vacancy


def load_jsonfile(filename: str):
    """ Функция для загрузки json файла """
    with open(filename, "r", encoding='UTF-8') as file:  # открывает файл в режиме чтения
        result = json.load(file)  # загружает файл в формате json
    return result  # возвращает словарь


# def load_companies(filename: str):
#     """ Функция для загрузки списка компаний """
#     result = load_jsonfile(filename)  # загружает файл в формате json
#     return result  # возвращает словарь
def validate_field(field: dict, sub_field: str, default_returning_value) -> str or int or None:
    """
    Метод, который проверяет, есть ли указанное поле в словаре и вообще словарь ли это.
    :param field: словарь с данными о вакансии
    :param sub_field: название поля
    :param default_returning_value: значение по умолчанию
    """
    if field is None or not isinstance(field, dict) or field.get(sub_field) is None:
        return default_returning_value
    return field[sub_field]

def get_vacancy_hh(all_vacancies: list[dict]) -> list[Vacancy]:
    """
    Метод, который создает список объектов Vacancy на основе данных о вакансиях.
    :param all_vacancies: список со словарями с вакансиями с HeadHunter
    :return: список с экземплярами класса Vacancy
    """
    list_vacancy: list = []
    for vacancy in all_vacancies:
        list_vacancy.append(
            Vacancy(
                title=vacancy["name"],
                salary_from=validate_field(vacancy["salary"], "from", 0),
                salary_to=validate_field(vacancy["salary"], "to", 0),
                experience=vacancy["snippet"]["requirement"],
                responsibility=validate_field(vacancy["snippet"], "responsibility", None),
                url=vacancy["alternate_url"],
                area=validate_field(vacancy["address"], "city", ""),
                employment=validate_field(vacancy["employment"], "name", None),
                currency=validate_field(vacancy["salary"], "currency", None)
            )
        )
    return list_vacancy
