import requests

from settings import URL_HH


class ApiHH:

    """ Класс для получения вакансий с сайта HeadHunter по id компании"""

    def __init__(self) -> None:
        self.__id_list_company = []

    @property
    def id_list_company(self):
        return self.__id_list_company

    @id_list_company.setter
    def id_list_company(self, id_list_company):
        self.__id_list_company = id_list_company

    @staticmethod
    def get_response_by_page(id_company):
        """
        Метод для получения ответа от сервера по id компании и номеру страницы
        :return:  ответ от сервера
        """
        params: dict = {
            "employer_id": id_company,

        }
        return requests.get(URL_HH, params=params).json()

    def get_all_vacancies(self) -> list[dict]:
        """
        Метод, для получения списка вакансий по нужным критериям
        :return: список со словарями по всем найденным вакансиям
        """
        all_vacancies: list[dict] = []
        for id_company in self.__id_list_company:
            vacancies_by_page: list[dict] = self.get_response_by_page(id_company)[
                    "items"]
            all_vacancies.extend(vacancies_by_page)
        return all_vacancies
