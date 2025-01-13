from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]

@dataclass
class DataBase:
    path: str #путь до места, где хранимтся база данных

@dataclass
class PAY_TOKEN:
    pay_token : str

@dataclass
class Config:
    tg_bot: TgBot



# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config_tgbot(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )

def load_config_db(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)
    return DataBase(
        path=env('PATH_TO_BD')
    )

def load_config_pay(path: str | None = None) -> PAY_TOKEN:
    env = Env()
    env.read_env(path)
    return PAY_TOKEN(
        pay_token=env('PAY_TOKEN')
    )
