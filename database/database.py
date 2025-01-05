import sqlite3 as sq3
from config_data.config import load_config_db

config = load_config_db()


def create_connection():
    """Создает соединение с БД"""
    try:
        conn = sq3.connect(f"{config.path}")
        return conn
    except sq3.Error as e:
        print(f"Ошибка при подключении к БД: {e}")
        return None

def create_users_bd():
    """"
    Создаём таблицу со всеми пользователями
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    role TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                    );""")
            conn.commit()
        except Exception as e:
            print(f'Ошибка при создании таблицы users:{e}')

        finally:
            cur.close()
            conn.close()

def create_products_bd():
    """
    Создаем каталог товаров
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        price REAL,
                        category TEXT,
                        image_url TEXT,
                        available INT);""")
            conn.commit()
        except Exception as e:
            print(f'ошибка при создании таблицы products:{e}')
        finally:
            cur.close()
            conn.close()

def create_bag_for_user(user_id: int):
    """
    Создаём корзину для пользователя
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""CREATE TABLE IF NOT EXISTS bag_{user_id}(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (product_id) REFERENCES products(id));""") #Связываем базу данных с users по user_id и с products по product_id
            conn.commit()
        except Exception as e:
            print(f'ошибка при создании таблицы корзины для пользователя:{e}')
        finally:
            cur.close()
            conn.close()

def new_user_in_users(user_id: int, username: str, first_name: str, last_name: str, role: str):
    """
    Добавляем нового пользователя в таблицу users
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""INSERT INTO users (user_id, username, first_name, last_name, role)
                        VALUES (?, ?, ?, ?, ?)""", (user_id, username, first_name, last_name, role))
            conn.commit()
        except Exception as e:
            print(f'ошибка при создании записи новго пользователя в users:{e}')
        finally:
            cur.close()
            conn.close()