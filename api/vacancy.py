class Vacancy:
    """
    Класс для работы с вакансиями
    """
    __slots__ = (
        "name_vacancy",
        "salary_from",
        "salary_to",
        "alternate_url",
        "id_employer",
        "salary_currency"
    )

    def __init__(
            self,
            name_vacancy: str,
            salary_from: int,
            salary_to: int,
            salary_currency: str,
            alternate_url: str,
            id_employer: str
    ):
        self.name_vacancy = name_vacancy
        self.salary_to = salary_to
        self.salary_from = salary_from
        self.alternate_url = alternate_url
        self.id_employer = id_employer
        self.salary_currency = salary_currency

    def check_currency(self) -> str:
        """
        Метод, который проверяет указана ли валюта
        :return: валюту для отображения
        """
        if self.salary_currency is not None:
            return self.salary_currency
        else:
            return ""

    @property
    def work_with_salary(self) -> str:
        """
        Метод, который работает с заработной платой
        :return: заработную плату для отображения в вакансии
        """
        salary_from = int(self.salary_from) if self.salary_from else 0
        salary_to = int(self.salary_to) if self.salary_to else 0

        if salary_from <= 0 and salary_to <= 0:
            return "Не указана заработная плата"
        elif salary_from and salary_to:
            return f"{salary_from} - {salary_to} {self.check_currency()}"
        elif salary_from:
            return f"от {salary_from} {self.check_currency()}"
        elif salary_to:
            return f"до {salary_to} {self.check_currency()}"
