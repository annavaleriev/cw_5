import json  # импорт библиотеки json,которая позволяет работать с данными в формате JSON
from typing import Any  # импорт Any из модуля typing для работы с типами данных

import requests  # импорт библиотеки requests, которая позволяет отправлять HTTP-запросы

from settings import URL_HH  # импорт URL_HH из файла settings.py


class ApiHH:  # создание класса API_HH для получения вакансий с сайта HeadHunter

    """ Класс для получения вакансий с сайта HeadHunter по id компании"""

    def __init__(self) -> None:
        self.__id_list_company = []
        self.__current_id_company = None

    @property
    def id_list_company(self):
        return self.__id_list_company

    @id_list_company.setter
    def id_list_company(self, id_list_company):
        self.__id_list_company = id_list_company

    def get_response_by_page(self, page=0):
        params: dict = {
            "employer_id": self.__current_id_company,
            "per_page": 100,  # количество вакансий на странице
            "page": page
        }
        return requests.get(URL_HH, params=params).json()  # отправка запроса на сервер, который возвращает ответ

    def get_count_pages(self) -> int:
        """
        Метод для получения общего кол-ва найденных страниц
        :return: число страниц с вакансиями
        """
        return self.get_response_by_page()["pages"]

    def get_all_vacancies(self) -> list[dict]:
        """
        Метод, для получения списка вакансий по нужным критериям
        :return: список со словарями по всем найденным вакансиям
        """
        all_vacancies: list[dict] = []
        for id_company in self.__id_list_company:
            company_data = {
                'id': id_company,
                'vacancies': []
            }
            self.__current_id_company = id_company
            pages: int = self.get_count_pages()
            for page in range(pages):
                vacancies_by_page: list[dict] = self.get_response_by_page(page)["items"]
                company_data['vacancies'].extend(vacancies_by_page)
            all_vacancies.append(company_data)
        return all_vacancies


if __name__ == '__main__':
    test = ApiHH()
    test.id_list_company = [3127, 10521060]
    jjjj = test.get_all_vacancies()
    print(jjjj)
