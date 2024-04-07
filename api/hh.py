import requests  # импорт библиотеки requests, которая позволяет отправлять HTTP-запросы

from settings import URL_HH  # импорт URL_HH из файла settings.py


class ApiHH:  # создание класса API_HH для получения вакансий с сайта HeadHunter

    """ Класс для получения вакансий с сайта HeadHunter по id компании"""

    def __init__(self) -> None:  # конструктор класса
        self.__id_list_company = []  # список id компаний

    @property  # декоратор для создания свойства id_list_company
    def id_list_company(self):
        return self.__id_list_company

    @id_list_company.setter  # декоратор для установки значения id_list_company
    def id_list_company(self, id_list_company):
        self.__id_list_company = id_list_company

    @staticmethod  # декоратор для создания статического метода
    def get_response_by_page(id_company):
        """
        Метод для получения ответа от сервера по id компании и номеру страницы
        :return:  ответ от сервера
        """
        params: dict = {
            "employer_id": id_company,  # id компании

        }
        return requests.get(URL_HH, params=params).json()  # отправка запроса на сервер, который возвращает ответ

    def get_all_vacancies(self) -> list[dict]:
        """
        Метод, для получения списка вакансий по нужным критериям
        :return: список со словарями по всем найденным вакансиям
        """
        all_vacancies: list[dict] = []  # список для хранения всех вакансий
        for id_company in self.__id_list_company:  # перебор всех id компаний
            vacancies_by_page: list[dict] = self.get_response_by_page(id_company)[
                    "items"]  # получение вакансий на странице
            all_vacancies.extend(vacancies_by_page)  # добавление данных о компании в список всех вакансий
        return all_vacancies  # возвращает список всех вакансий


# if __name__ == '__main__':
#     test = ApiHH()
#     test.id_list_company = [3127]
#     jjjj = test.get_all_vacancies()
#     print(jjjj)
