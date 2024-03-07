from vacancy import Vacancy


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


def get_vacancy_hh(all_vacancies: list[dict]) -> list[Vacancy]:
    """
    Метод, который создает список объектов Vacancy на основе данных о вакансиях.
    :param all_vacancies: список со словарями с вакансиями с HeadHunter
    :return: список с экземплярами класса Vacancy
    """
    list_vacancy: list = []
    for vacancy in all_vacancies:
        list_vacancy.append(
            Vacancy(
                employer=vacancy["employer"],
                employer_id=vacancy["employer_id"],
                title=vacancy["name"],
                salary_from=validate_field(vacancy["salary"], "from", 0),
                salary_to=validate_field(vacancy["salary"], "to", 0),
                experience=vacancy["snippet"]["requirement"],
                responsibility=validate_field(vacancy["snippet"], "responsibility", None),
                url=vacancy["alternate_url"],
                area=validate_field(vacancy["address"], "city", ""),
                employment=validate_field(vacancy["employment"], "name", None),
                currency=validate_field(vacancy["salary"], "currency", None)
            )
        )
    return list_vacancy


def get_sorted_vacancies_by_salary(list_vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Метод, который сортирует вакансии по зарплате
    :param list_vacancies: список с вакансиями
    :return: список с отсортированными вакансиями по заработной плате
    """
    list_vacancies.sort(reverse=True)
    return list_vacancies


# def get_filtered_vacancies_by_town(list_vacancies: list[dict], town: str) -> list[Vacancy]:
#     """
#     Метод, который фильтрует вакансии по городу
#     :param list_vacancies: список с вакансиями
#     :param town: город
#     :return: список с отфильтрованными вакансиями по городу
#     """
#     return list(filter(lambda vacancy: town in vacancy.area.lower(), list_vacancies))


def validate_input(valid_numbers: tuple, choice_text: str) -> int or str:
    """
    Метод, который проверяет введенное пользователем число
    :param valid_numbers: варианты ввода цифры пользователем
    :param choice_text: текст, который выводится пользователю при некорректном вводе
    :return: число, которое ввел пользователь или текст, который выводится пользователю при некорректном вводе
    """
    while True:
        try:
            user_input: int = int(input("Введите цифру: "))
            if user_input in valid_numbers:
                return user_input
            print(choice_text)
        except ValueError:
            print(f"Вы ввели слово. Вам нужно выбрать число от {min(valid_numbers)} до {max(valid_numbers)}.\n")


def show_vacancies_info(combined_vacancies: list[Vacancy]) -> None:
    """
    Метод, который выводит информацию о вакансиях
    :param combined_vacancies: список с экземплярами класса Vacancy
    :return: выводит информацию о вакансии
    """
    for vacancy in combined_vacancies:
        print(vacancy)
