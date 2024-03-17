import requests

from settings import URL_HH, COUNT_VACANCIES_BY_PAGE


class HeadHunterAPI:
    """
    Класс для получения вакансий с сайта HeadHunter по id компании
    """

    @property
    def url(self) -> str:
        """
        Property для url
        :return: url в виде строки
        """
        return URL_HH

    # def get_all_vacancies(self, id: int) -> list[dict]:
    #     """
    #     Метод, для получения списка вакансий по id по нужным критериям
    #     :return:
    #     """
    #     params = {
    #         "per_page": 100,
    #         "page": 0
    #         "employer_id": id
    #     }
    #     response = requests.get(self.url, params=params)

    def get_response_by_page(self, page=0) -> dict[str]:
        """
        Метод для получения вакансия по id компании с сайта HeadHunter
        :param page: номер страницы для получения данных
        :return: словарь со списком вакансий в формате json
        """
        params: dict[str] = {
            "employer_id": id,
            "per_page": COUNT_VACANCIES_BY_PAGE,
            "page": page,
        }
        return requests.get(self.url, params).json()

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
        pages: int = self.get_count_pages()
        all_vacancies: list = []
        for page in range(pages):
            vacancies_by_page: list[dict] = self.get_response_by_page(page)["items"]
            all_vacancies.extend(vacancies_by_page)
        return all_vacancies
