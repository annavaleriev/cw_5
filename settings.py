from pathlib import Path

from utils import load_jsonfile

ROOT_PATH = Path(__file__).parent
DATABASE_CONFIG_PATH = ROOT_PATH.joinpath('config.ini')

COMPANIES_JSON_PATH = ROOT_PATH.joinpath('fixtures', 'companies.json')

URL_HH = "https://api.hh.ru/vacancies"
