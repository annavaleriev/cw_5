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
        if self.salary_from and self.salary_to:
            return f"{self.salary_from} - {self.salary_to} {self.check_currency()}"
        elif self.salary_from:
            return f"от {self.salary_from} {self.check_currency()}"
        elif self.salary_to:
            return f"до {self.salary_to} {self.check_currency()}"
        else:
            return "Не указана заработная плата"

    def __str__(self) -> str:
        """
        Выводит сообщение для пользователя по вакансии
        :return:строку с данными по вакансии
        """

        return (
            f"Вакансия: {self.name_vacancy}\n"
            f"{self.alternate_url}\n"
            f"Зарплата: {self.work_with_salary}\n"
            f"******************************************************************\n\n"
        )

    def __gt__(self, other) -> bool:
        """
        Метод, который сравнивает заработные платы какая больше
        :param other: Другой объект типа Salary, с которым сравнивается текущий объект
        :return: True, если заработная плата текущего объекта больше, чем у другого объекта, иначе False
        """
        return self.avg_salary > other.avg_salary

    def __lt__(self, other) -> bool:
        """
        Метод, который сравнивает заработные платы какая меньше
        :param other: Другой объект типа Salary, с которым сравнивается текущий объект
        :return: True, если заработная плата текущего объекта меньше, чем у другого объекта, иначе False
        """
        return self.avg_salary < other.avg_salary

    @property
    def avg_salary(self) -> float:
        """
        Метод, который вычисляет среднюю заработную плату
        :return: cреднюю заработную плату
        """
        return (self.salary_from + self.salary_to) / 2

    def to_dict(self) -> dict:
        """
        Метод, который возвращает словарь с данными по вакансии
        :return: cловарь с данными по вакансии
        """
        vacancy_dict: dict = {
            "name_vacancy": self.name_vacancy,
            "salary_to": self.salary_to,
            "salary_from": self.salary_from,
            "alternate_url": self.alternate_url,
            "id_employer": self.id_employer,
            "salary_currency": self.salary_currency,
        }
        return vacancy_dict
