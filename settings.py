from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATABASE_CONFIG_PATH = ROOT_PATH.joinpath('config.ini')

COMPANIES_JSON_PATH = ROOT_PATH.joinpath('companies.json')

URL_HH = "https://api.hh.ru/vacancies"