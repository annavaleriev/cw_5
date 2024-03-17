import json  # импорт библиотеки json,которая позволяет работать с данными в формате JSON

import requests  # импорт библиотеки requests, которая позволяет отправлять HTTP-запросы

from settings import URL_HH  # импорт URL_HH из файла settings.py


class API_HH:  # создание класса API_HH для получения вакансий с сайта HeadHunter

    """ Класс для получения вакансий с сайта HeadHunter по id компании"""

    def get_all_vacancies(self, id: int) -> list[dict]:  # создание метода get_all_vacancies, который получает
        # список вакансий по id по нужным критериям
        """ Метод, для получения списка вакансий по id по нужным критериям"""

        # создание словаря params, который содержит параметры запроса, которые будут передаваться
        params: dict = {
            "employer_id": id,  # в запросе id компании
            "per_page": 100,  # количество вакансий на странице
            "page": 0  # номер страницы
        }
        response = requests.get(URL_HH, params=params)  # отправка запроса на сервер, который возвращает ответ
        response_data = json.loads(response.text)  # преобразование ответа в формате JSON в словарь
        number_pages = response_data["pages"]  # количество страниц с вакансиями
        all_vacancies = []  # создание пустого списка all_vacancies

        if 'items' in response_data:  # если в словаре response_data есть ключ 'items'
            all_vacancies.extend(response_data['items'])  # добавление в список all_vacancies всех вакансий из словаря

        else:  # если в словаре response_data нет ключа 'items'
            return all_vacancies  # возврат пустого списка all_vacancies

        if number_pages > 1:  # если количество страниц с вакансиями больше 1
            for page in range(1, number_pages):  # для каждой страницы в диапазоне от 1 до number_pages.
                # Это мы делаем, чтобы получить все вакансии
                params["page"] = page  # в словарь params добавляем ключ "page" и значение page.
                response = requests.get(URL_HH, params=params)  # отправка запроса на сервер, который возвращает ответ
                response_data = json.loads(response.text)  # преобразование ответа в формате JSON в словарь
                all_vacancies.extend(
                    response_data['items'])  # добавление в список all_vacancies всех вакансий из словаря

        return all_vacancies  # возврат списка all_vacancies
