class Vacancy:
    """
    Класс для работы с вакансиями
    """
    __slots__ = ("employer", "employer_id", "title", "salary_from", "salary_to", "experience", "responsibility",
                 "url", "area", "employment", "currency")

    def __init__(self, employer: str, employer_id: int,  title: str, salary_from: int, salary_to: int, experience: str,
                 responsibility: str, url: str, area: str, employment: str, currency: str):
        self.employer = employer  # название компании
        self.employer_id = employer_id  # id компании
        self.title = title
        self.salary_to = salary_to
        self.salary_from = salary_from
        self.experience = experience  # требования
        self.responsibility = responsibility  # описание вакансии
        self.url = url
        self.area = area
        self.employment = employment  # тип занятости
        self.currency = currency

    def check_currency(self) -> str:
        """
        Метод, который проверяет указана ли валюта
        :return: валюту для отображения
        """
        if self.currency is not None:
            return self.currency
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

        return (f"Компания: {self.employer}\n"
                f"Вакансия: {self.title}\n"
                f"{self.url}\n"
                f"Зарплата: {self.work_with_salary}\n"
                f"Тип занятости: {self.employment}\n"
                f"Город: {self.area}\n"
                f"Описание вакансии: {self.responsibility}\n"
                f"Требования:{self.experience}\n\n"
                f"******************************************************************\n\n"
                )

    # def __gt__(self, other) -> bool:
    #     """
    #     Метод, который сравнивает заработные платы какая больше
    #     :param other: Другой объект типа Salary, с которым сравнивается текущий объект
    #     :return: True, если заработная плата текущего объекта больше, чем у другого объекта, иначе False
    #     """
    #     return self.avg_salary > other.avg_salary
    #
    # def __lt__(self, other) -> bool:
    #     """
    #     Метод, который сравнивает заработные платы какая меньше
    #     :param other: Другой объект типа Salary, с которым сравнивается текущий объект
    #     :return: True, если заработная плата текущего объекта меньше, чем у другого объекта, иначе False
    #     """
    #     return self.avg_salary < other.avg_salary
    #
    # @property
    # def avg_salary(self) -> float:
    #     """
    #     Метод, который вычисляет среднюю заработную плату
    #     :return: cреднюю заработную плату
    #     """
    #     return (self.salary_from + self.salary_to) / 2

    def to_dict(self) -> dict:
        """
        Метод, который возвращает словарь с данными по вакансии
        :return: cловарь с данными по вакансии
        """
        vacancy_dict: dict = {
            "employer": self.employer,
            "employer_id": self.employer_id,
            "title": self.title,
            "salary_to": self.salary_to,
            "salary_from": self.salary_from,
            "experience": self.experience,
            "responsibility": self.responsibility,
            "url": self.url,
            "area": self.area,
            "employment": self.employment,
            "currency": self.currency
        }
        return vacancy_dict
