class Vacancy:
    """ Класс для работы с вакансиями"""

    def __init__(self, vacancy_information: dict):  # сразу принимает словарь с данными по вакансии, в 4 курсовой
        # ниже в методе to_dict возвращает словарь с данными по вакансии, значит метода to_dict не будет

        """ Конструктор класса Vacancy"""

        # self.id = vacancy_information["id"] # id вакансии, это мне вообще нужно?
        self.name = vacancy_information["name"]  # Название вакансии
        self.salary_from = vacancy_information["salary_from"]  # Зарплата от
        self.salary_to = vacancy_information["salary_to"]  # Зарплата до
        self.currency = vacancy_information["currency"]  # Валюта
        self.area = vacancy_information["area"]  # Город
        self.url = vacancy_information["url"]  # Ссылка на вакансию
        self.employer = vacancy_information["employer"]  # Работодатель
        self.employer_id = vacancy_information["employer_id"]  # id работодателя
        self.requirement = vacancy_information["requirement"]  # Требования
        self.experience = vacancy_information["experience"]  # Опыт
        # self.salary_avg = self.avg_salary  # Средняя зарплата

    def __str__(self):
        """ Выводит сообщение для пользователя по вакансии"""

        return (f"Работодатель: {self.employer}\n"
                f"Город: {self.area}\n"
                "Вакансия: {self.name}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: {self.work_with_salary}\n"
                f"Требования: {self.requirement}\n"
                f"Опыт: {self.experience}\n"
                f"******************************************************************\n\n"
                )

    def check_currency(self) -> str:  # Проверка валюты в вакансии
        """
        Метод, который проверяет указана ли валюта
        :return: валюту для отображения
        """
        if self.currency is not None:
            return self.currency
        else:
            return ""

    @property
    def work_with_salary(self) -> str:  # Работа с зарплатой, метод  для отображения зарплаты в вакансии
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

    def __gt__(self, other) -> bool:  # Сравнение зарплаты в вакансии
        """
        Метод, который сравнивает заработные платы какая больше
        :param other: Другой объект типа Salary, с которым сравнивается текущий объект
        :return: True, если заработная плата текущего объекта больше, чем у другого объекта, иначе False
        """
        return self.avg_salary > other.avg_salary

    def __lt__(self, other) -> bool:  # Сравнение зарплаты в вакансии
        """
        Метод, который сравнивает заработные платы какая меньше
        :param other: Другой объект типа Salary, с которым сравнивается текущий объект
        :return: True, если заработная плата текущего объекта меньше, чем у другого объекта, иначе False
        """
        return self.avg_salary < other.avg_salary

    @property
    def avg_salary(self) -> float:  # Вычисление средней зарплаты
        """
        Метод, который вычисляет среднюю заработную плату
        :return: cреднюю заработную плату
        """
        return (self.salary_from + self.salary_to) / 2

    @classmethod  # классовый метод, который принимает класс в качестве первого аргумента. Используется для создания
    # методов, которые работают с классом, но не требуют создания экземпляра класса.
    def get_vacancy_hh(cls, vacancy_from_hh: dict):

        """ Метод, который создает объект Vacancy на основе данных о вакансии с HeadHunter"""
        # get_vacancy_hh видимо, так же
        vacancy = {  # создаем словарь с данными по вакансии
            "name": cls.check_params(vacancy_from_hh, "name"),  # Название вакансии
            "salary_from": cls.check_params(vacancy_from_hh, "salary", "from", 0),  # Зарплата от
            "salary_to": cls.check_params(vacancy_from_hh, "salary", "to", 0),  # Зарплата до
            "currency": cls.check_params(vacancy_from_hh, "salary", "currency"),  # Валюта
            "area": cls.check_params(vacancy_from_hh, "address", "city"),  # Город
            "url": cls.check_params(vacancy_from_hh, "alternate_url"),  # Ссылка на вакансию
            "employer": cls.check_params(vacancy_from_hh, "employer", "name"),  # Работодатель
            "employer_id": cls.check_params(vacancy_from_hh, "employer", "id"),  # id работодателя
            "requirement": cls.check_params(vacancy_from_hh, "snippet", "requirement"),  # Требования
            "experience": cls.check_params(vacancy_from_hh, "snippet", "responsibility")  # Опыт
        }
        return Vacancy(vacancy)  # возвращаем объект Vacancy с данными по вакансии

    # надо как-то проверить наличик дааных в словаре, в 4 курсовой это validate_field

    @staticmethod  # статический метод, который не требует создания объекта класса.
    def check_params(vacancy_information: dict, param1: str, param2: str = None,
                     param3: int = None):  # Проверка наличия данных в словаре по вакансии
        """ Метод, который проверяет наличие данных в словаре по вакансии"""

        try:  # проверка наличия данных в словаре
            if param3 is None:  # если параметр 3 не указан
                if param2 is None:  # если параметр 2 не указан
                    return vacancy_information[param1]  # возвращаем значение по ключу param1
                else:  # иначе
                    return vacancy_information[param1][param2]  # возвращаем значение по ключу param1 и param2
            else:  # иначе
                return vacancy_information[param1][param2][
                    param3]  # возвращаем значение по ключу param1, param2 и param3
        except KeyError:  # если не получилось вернуть значение
            return None  # возвращаем None

    @staticmethod
    def check_param_2(vacancy_information: dict, *params: str):
        # Проверка наличия данных в словаре по вакансии c использованием *args
        """ Метод, который проверяет наличие данных в словаре по вакансии"""

        try:  # проверка наличия данных в словаре
            result = vacancy_information  # присваиваем переменной result значение словаря
            for param in params:  # перебираем параметры
                result = result[param]  # присваиваем переменной result значение по ключу param
            return result  # возвращаем result
        except KeyError:  # если не получилось вернуть значение
            return None  # возвращаем None
