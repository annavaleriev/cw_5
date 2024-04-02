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


def get_vacancy_hh(all_companies: list[dict]) -> list[Vacancy]:
    """
    Метод, который создает список объектов Vacancy на основе данных о вакансиях.
    :param all_companies: список со словарями
    :return: список с экземплярами класса Vacancy
    """
    list_vacancy: list = []
    for company in all_companies:
        for vacancy in company['vacancies']:
            list_vacancy.append(
                Vacancy(
                    name_vacancy=vacancy["name"],
                    salary_from=validate_field(vacancy["salary"], "from", 0),
                    salary_to=validate_field(vacancy["salary"], "to", 0),
                    alternate_url=vacancy["alternate_url"],
                    salary_currency=validate_field(vacancy["salary"], "currency", None),
                    id_employer=company['id']
                )
            )
    return list_vacancy


def convert_real_dict_row_to_dict(data):
    return {
        key: str(value)
        for key, value in data.items()
    }


def covert_to_json(data):
    result = list(map(convert_real_dict_row_to_dict, data))
    return json.dumps(result, indent=4, ensure_ascii=False)
