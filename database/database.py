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
def create_orders_db():
    """
    Создаём таблицу с заказами
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INT,
                    order_price TEXT,
                    status TEXT,
                    bag_msg TEXT,
                    order_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

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
                        product_id INTEGER,
                        quantity INTEGER,
                        price INTEGER,
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

def add_product(sl: dict):
    """
    Добавление нового товара в таблицу products
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""INSERT INTO products (title, description, price, category, image_url, available)
                        VALUES (?, ?, ?, ?, ?, ?)""", (sl['name'], sl['descr'], sl['price'], sl['category'], sl['photo'], sl['available']))
            conn.commit()
        except Exception as e:
            print(f'ошибка при создании записи новго пользователя в products:{e}')
        finally:
            cur.close()
            conn.close()

def get_products_for_catalog(category: str | None = None):
    """
    Получаем товары по выбранной категории или среди всех категорий по умолчанию
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            if category:
                cur.execute("""SELECT * FROM products
                            WHERE category = ?""", (category,))
                a = cur.fetchall()
            else:
                cur.execute("""SELECT * FROM products
                            """)
                a = cur.fetchall()
            conn.commit()
        except Exception as e:
            print(f'ошибка при получении данных продукта для его демонстрации в каталоге:{e}')
            a = None
        finally:
            cur.close()
            conn.close()
    return a


def add_prod_to_user_bag(id: int, prod: tuple):
    """
    Добавляем товар в пользовательскую корзину, а если с данным id уже есть, то увеличиваем количество и цену
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM bag_{id} WHERE product_id = ?""", (prod[0], ))
            a = cur.fetchall()
            if a:
                cur.execute(f"""UPDATE bag_{id} SET quantity = ?, price = ? WHERE product_id = ?""", (a[0][2] + 1, a[0][3], prod[0]))
            else:
                cur.execute(f"""INSERT INTO bag_{id} (product_id, quantity, price) VALUES (?, 1, ?)""", (prod[0],  prod[3]))
            conn.commit()
        except Exception as e:
            print(f'ошибка при создании записи в корзине пользователя:{e}')
        finally:
            cur.close()
            conn.close()

def get_available_product(product_id: int):
    """
    Возвращает количество доступного товара в виде списка кортежей
    или None если произошла ошибка
    """
    with create_connection() as conn:
      if conn:
        cur = conn.cursor()
        try:
            cur.execute(f"""SELECT available FROM products
                            WHERE id = ?""", (product_id,))
            result = cur.fetchone()
            conn.commit()
            return result[0]
        except sq3.Error as e:
            print(f'ошибка при получении количества доступных товаров:{e}')
            return None
        finally:
            if cur:
              cur.close()
    return None

def get_quiantly_product(user_id: int, prod_id: int) :
    """
    Получает количество товара в корзине пользователя.
    """
    with create_connection() as conn:
      if conn:
        cur = conn.cursor()
        try:
          cur.execute(f"""SELECT quantity FROM bag_{user_id}
                           WHERE product_id = ?""", (prod_id,))
          result = cur.fetchone()
          conn.commit()
          if result:
             return result[0]
          else:
            return 0
        except sq3.Error as e:
            print(f'ошибка при получении количества товара в корзине: {e}')
            return None
        finally:
          if cur:
            cur.close()
    return None

def get_bag_products(user_id: int):
    """
    Получаем все товары из корзины пользователя и их названия из таблицы products
    """
    with create_connection() as conn:
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(f"""
                    SELECT bag_{user_id}.*, products.title
                    FROM bag_{user_id}
                    JOIN products ON bag_{user_id}.product_id = products.id
                """)
                result = cur.fetchall()
                conn.commit()
                return result
            except sq3.Error as e:
                 print(f'ошибка при получении товаров из корзины пользователя:{e}')
                 return None
            finally:
                if cur:
                    cur.close()
    return None

def get_product_in_bag_for_id(user_id: int, product_id: int):
    """
    Возвращает продукт из корзины по айди
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT bag_{user_id}.*, products.title
                    FROM bag_{user_id}
                    JOIN products ON bag_{user_id}.product_id = products.id
                    WHERE product_id = ? """, (product_id,))
            a = cur.fetchone()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить продукт из корзины:{e}')
        finally:
            cur.close()
            conn.close()

def change_quantityprod_in_bag(user_id: int, prod_id: int, new_quan: int):
    """
    Меняет количество товара в корзине пользователя
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""UPDATE bag_{user_id} SET quantity = ? WHERE product_id = ? """, (new_quan, prod_id))
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке изменить количество продукта в корзине:{e}')
        finally:
            cur.close()
            conn.close()

def delete_product_from_bag(user_id: int, prod_id: int):
    """
    Удаляем продукт из корзины пользователя
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""DELETE FROM bag_{user_id} WHERE product_id = ?""", (prod_id, ))
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке удалить продукт из корзины пользователя:{e}')
        finally:
            cur.close()
            conn.close()

def clear_bag(user_id: int):
    """
    Очищаем корзину пользователя после заказа
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""DELETE FROM bag_{user_id} """)
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке удалить все продукты из корзины пользователя:{e}')
        finally:
            cur.close()
            conn.close()

def create_new_order(user_id: int, price: int, bag_msg: str):
    """
    Создаём новую запись в таблице orders
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""INSERT INTO orders (user_id, order_price, status, bag_msg)
                        VALUES (?, ?, 'Оплачено', ?) """, (user_id, price, bag_msg))
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке удалить все продукты из корзины пользователя:{e}')
        finally:
            cur.close()
            conn.close()

def get_one_order_for_user(order_id: int):
    """
    Получаем все заказы от пользователя
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM orders WHERE id = ?""", (order_id, ))
            a = cur.fetchone()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить заказы пользователя:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def get_orders_for_user1(user_id: int):
    """
    Получаем все заказы от пользователя
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT id, order_price FROM orders WHERE user_id = ?""", (user_id, ))
            a = cur.fetchall()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить заказы пользователя:{e}')
            return None
        finally:
            cur.close()
            conn.close()


def get_products_to_redact_kb():
    """
    Получаем все продукты
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT id, title FROM products """)
            a = cur.fetchall()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить все продукты:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def get_product_with_prod_id(prod_id: int):
    """
    Получаем информацию по продукту по id
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM products
                        WHERE id = ?""", (prod_id, ))
            a = cur.fetchone()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить продукт:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def change_price_prod(prod_id: int, price: int):
    """
    Меняем цену товара
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""UPDATE products SET price = ? WHERE id = ?""", (price, prod_id))
            conn.commit()
        except Exception as e:
            print(f'ошибка при изменить цену:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def change_price_prod(prod_id: int, avail: int | str):
    """
    Меняем наличие товара
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""UPDATE products SET available = ? WHERE id = ?""", (avail, prod_id))
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке изменить наличие:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def del_product(prod_id: int):
    """
    Меняем наличие товара
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""DELETE FROM products WHERE id = ?""", (prod_id,))
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке изменить наличие:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def get_id_and_avail_from_bag(user_id: int):
    """
    получаем айди и наличие всех товаров
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT product_id, quantity FROM bag_{user_id}""")
            a = cur.fetchall()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке ие:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def change_available(prod_id: int, avail: int):
    """
    получаем айди и наличие всех товаров
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""UPDATE products SET available = available - ? WHERE id = ? AND available != "Несколько" """,(avail, prod_id) )
            conn.commit()
        except Exception as e:
            print(f'ошибка при попытке изменить наличие:{e}')
            return None
        finally:
            cur.close()
            conn.close()

def get_username_from_userid(user_id: str):
    """
    получаем username по айди юзера
    """
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"""SELECT username FROM users WHERE user_id = ? """,(user_id, ) )
            a = cur.fetchone()
            conn.commit()
            return a
        except Exception as e:
            print(f'ошибка при попытке получить юзернейм:{e}')
            return None
        finally:
            cur.close()
            conn.close()