import requests


# list_id_company = ('3127', '10521060', '5267014', '15478', '84585', '1740', '697715', '903111', '39305', '2180')
def get_company(list_id_company: tuple[int]) -> list[tuple[int, str, str]]:
    """ Метод для получения списка всех компаний и количество вакансий у каждой компании."""
    list_company = []
    for id_company in list_id_company:
        url_hh = f"https://api.hh.ru/vacancies?employer_id={id_company}"  # тут тоже прятала ссылку + вообще проверить эту ссылку
        response = requests.get(url=url_hh).json()
        list_company.append(response["id"], response["name"],
                            response["vacancies_url"])  # проверить как называется в документации
    return list_company


# def get_vacancy_hh(list_company):
#     list_vacancy = []
#     for company in list_company:
#         response = requests.get(company[2]).json()
#
#         for company in response["items"]:
#             if company["salary"] is None and company["salary"]["from"] is None and company["salary"]["to"] is None:
#                 list_vacancy.append([company["name"], None, company['salary']['to']),
#                                     company['salary']['currency'], company['alternate_url'], company["employer"]["id"]]
#             elif company["salary"] is not None and company['salary']['to'] is None and company['salary']['from'] is not None):
#                 list_vacancy.append([company["name"], company['salary']['from'], None,
#                                      company['salary']['currency'], company['alternate_url'],
#                                      company["employer"]["id"]])
#             elif company['salary'] is None:
#                 list_vacancy.append([company["name"], None, None, None, company['alternate_url'], company["employer"]["id"]])
#             else:
#                 list_vacancy.append([company["name"], company['salary']['from'], company['salary']['to'],
#                                      company['salary']['currency'], company['alternate_url'],
#                                      company["employer"]["id"]])
#
# return list_vacancy

def get_vacancy_hh(list_company: list[tuple[int, str, str]]) -> list[tuple[str, int, int, str, str, int]]:
    """Метод, который получает информацию о вакансиях для заданных компаний с сайта hh.ru"""

    list_vacancy = []
    for company in list_company:
        response = requests.get(company[2]).json()

        for vacancy in response["items"]:
            if vacancy["salary"] is None:
                list_vacancy.append([vacancy["name"], None, None, None, vacancy["alternate_url"],
                                     vacancy["employer"]["id"]])
            elif vacancy["salary"]["from"] is not None and vacancy["salary"]["to"] is None:
                list_vacancy.append([vacancy["name"], vacancy["salary"]["from"], None, vacancy["salary"]["currency"],
                                     vacancy["alternate_url"], vacancy["employer"]["id"]])
            elif vacancy["salary"]["to"] is not None and vacancy["salary"]["from"] is None:
                list_vacancy.append([vacancy["name"], None, vacancy["salary"]["to"], vacancy["salary"]["currency"],
                                     vacancy["alternate_url"], vacancy["employer"]["id"]])
            else:
                list_vacancy.append([vacancy["name"], vacancy["salary"]["from"], vacancy["salary"]["to"],
                                     vacancy["salary"]["currency"], vacancy["alternate_url"], vacancy["employer"]["id"]])

    return list_vacancy



# employer = vacancy["employer"],
# employer_id = vacancy["employer_id"],
# title = vacancy["name"],
# salary_from = validate_field(vacancy["salary"], "from", 0),
# salary_to = validate_field(vacancy["salary"], "to", 0),
# experience = vacancy["snippet"]["requirement"],
# responsibility = validate_field(vacancy["snippet"], "responsibility", None),
# url = vacancy["alternate_url"],
# area = validate_field(vacancy["address"], "city", ""),
# employment = validate_field(vacancy["employment"], "name", None),
# currency = validate_field(vacancy["salary"], "currency", None)
