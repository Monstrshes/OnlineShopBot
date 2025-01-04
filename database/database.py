import sqlite3 as sq3
from config_data.config import load_config

config = load_config()

def create_connection():
    """Создает соединение с БД"""
    try:
        conn = sq3.connect(f"{config.db_path}")
        return conn
    except sq3.Error as e:
        print(f"Ошибка при подключении к БД: {e}")
        return None
