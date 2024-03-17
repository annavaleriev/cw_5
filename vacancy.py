class Vacancy:

    """ Класс для работы с вакансиями"""

    def __init__(self, vacancy_information: dict):  # сразу принимает словарь с данными по вакансии, в 4 курсовой
        # ниже в методе to_dict возвращает словарь с данными по вакансии

        """ Конструктор класса Vacancy"""

        # self.id = vacancy_information["id"] # id вакансии, это мне вообще нужно?
        self.name = vacancy_information["name"]  # Название вакансии
        self.salary_from = vacancy_information["salary_from"]  # Зарплата от
        self.salary_to = vacancy_information["salary_to"]  # Зарплата до
        self.currency = vacancy_information["currency"] # Валюта
        self.area = vacancy_information["area"] # Город
        self.url = vacancy_information["url"]  # Ссылка на вакансию
        self.employer = vacancy_information["employer"]  # Работодатель
        self.employer_id = vacancy_information["employer_id"]  # id работодателя
        self.requirement = vacancy_information["requirement"]  # Требования
        self.experience = vacancy_information["experience"] # Опыт
        # self.salary_avg = self.avg_salary  # Средняя зарплата

    def __str__(self):
        """ Выводит сообщение для пользователя по вакансии"""

        # if self.requirement is None: # Проверка, если требования не указаны
        #     requirement = None # Присвоение переменной значения None
        # else:
        #     requirement = self.requirement[:200] + "..." # Присвоение переменной значения требований
        return (f"Работодатель: {self.employer}\n"
                f"Город: {self.area}\n"
                "Вакансия: {self.name}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: {self.work_with_salary}\n"
                f"Требования: {self.requirement}\n"
                f"Опыт: {self.experience}\n"                                              
                f"******************************************************************\n\n"
                )

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

