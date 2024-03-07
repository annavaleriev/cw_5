import requests


# list_id_company = ('3127', '10521060', '5267014', '15478', '84585', '1740', '697715', '903111', '39305', '2180')
def get_company(list_id_company: tuple[int]) -> list[tuple[int, str, str]]:
    """ Метод для получения списка всех компаний и количество вакансий у каждой компании."""
    list_company = []
    for id_company in list_id_company:
        url_hh = f"https://api.hh.ru/vacancies?employer_id={id_company}"  # тут тоже прятала ссылку + вообще проверить эту ссылку
        response = requests.get(url=url_hh).json()
        list_company.append(response["id"], response["name"], response["vacancies_url"])
    return list_company
