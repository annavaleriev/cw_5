import json


def load_jsonfile(filename: str):
    """ Функция для загрузки json файла """
    with open(filename, "r", encoding='UTF-8') as file:  # открывает файл в режиме чтения
        result = json.load(file)  # загружает файл в формате json
    return result  # возвращает словарь


# def load_companies(filename: str):
#     """ Функция для загрузки списка компаний """
#     result = load_jsonfile(filename)  # загружает файл в формате json
#     return result  # возвращает словарь
