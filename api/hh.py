import requests  # импорт библиотеки requests, которая позволяет отправлять HTTP-запросы

from settings import URL_HH  # импорт URL_HH из файла settings.py


class ApiHH:  # создание класса API_HH для получения вакансий с сайта HeadHunter

    """ Класс для получения вакансий с сайта HeadHunter по id компании"""

    def __init__(self) -> None:  # конструктор класса
        self.__id_list_company = []  # список id компаний
        self.__current_id_company = None  # id текущей компании

    @property  # декоратор для создания свойства id_list_company
    def id_list_company(self):
        return self.__id_list_company

    @id_list_company.setter  # декоратор для установки значения id_list_company
    def id_list_company(self, id_list_company):
        self.__id_list_company = id_list_company

    def get_response_by_page(self, page=0):
        """
        Метод для получения ответа от сервера по id компании и номеру страницы
        :param page:  номер страницы
        :return:  ответ от сервера
        """
        params: dict = {
            "employer_id": self.__current_id_company,  # id компании
            "per_page": 100,  # количество вакансий на странице
            "page": page  # номер страницы
        }
        return requests.get(URL_HH, params=params).json()  # отправка запроса на сервер, который возвращает ответ

    def get_count_pages(self) -> int:
        """
        Метод для получения общего кол-ва найденных страниц
        :return: число страниц с вакансиями
        """
        return self.get_response_by_page()["pages"]  # возвращает общее количество страниц с вакансиями

    def get_all_vacancies(self) -> list[dict]:
        """
        Метод, для получения списка вакансий по нужным критериям
        :return: список со словарями по всем найденным вакансиям
        """
        all_vacancies: list[dict] = []  # список для хранения всех вакансий
        for id_company in self.__id_list_company:  # перебор всех id компаний
            company_data = {  # создание словаря для хранения данных о компании, шаблон
                'id': id_company,
                'vacancies': []
            }
            self.__current_id_company = id_company  # установка id текущей компании, переопределение переменной
            pages: int = self.get_count_pages()  # получение количества страниц с вакансиями
            for page in range(pages):  # перебор всех страниц с вакансиями
                vacancies_by_page: list[dict] = self.get_response_by_page(page)[
                    "items"]  # получение вакансий на странице
                company_data['vacancies'].extend(vacancies_by_page)  # добавление вакансий в список вакансий компании
            all_vacancies.append(company_data)  # добавление данных о компании в список всех вакансий
        return all_vacancies  # возвращает список всех вакансий


# if __name__ == '__main__':
#     test = ApiHH()
#     test.id_list_company = [3127, 10521060]
#     jjjj = test.get_all_vacancies()
#     print(jjjj)
