lexicon = {
    "common": {
        "start_message": "Привет! 👋 Добро пожаловать в наш онлайн-магазин {}! \nЧтобы узнать о доступных командах и перейти в меню, вопспользуйтесь командой /help",#имя магазина
        "help_message": "Вот список доступных команд:\n\n/start - Начать работу с ботом\n/help - Показать это сообщение\n/start_admin - Перейти в панель управления для админов\n/end_admin - Выйти из панели управления для админов\nЧтобы попасть в меню нажмите кнопку ниже.",
        "menu_message": "Вы в главном меню. Выберите, что хотите делать дальше.",
        "back_button": "⬅️ Назад",
        "cancel_button": "❌ Отмена",
        "back_to_menu_button": "Вернуться в меню",
        "added_to_cart": "✅ Товар добавлен в корзину!",
        "empty_cart": "🗑️ Ваша корзина пуста.",
        "cleared_cart": "🛒 Корзина очищена.",
        "no_products_available": "😞 Извините, пока нет доступных товаров."
    },
    "catalog": {
        "catalog_title": "🛍️ Каталог товаров",
        "select_category": "Выберите категорию:",
        "select_product": "Выберите товар:",
        "product_info": "ℹ️ {title}\n\n{description}\n\nЦена: {price} руб.",
        "add_to_cart_button": "🛒 Добавить в корзину"
    },
    "cart": {
        "cart_title": "🛒 Ваша корзина",
        "cart_item": "{index}. {title} - {quantity} шт. x {price} руб. = {total} руб.",
        "total_amount": "💰 Итого: {total_amount} руб.",
        "checkout_button": "✅ Перейти к оформлению заказа",
        "clear_cart_button": "🗑️ Очистить корзину"
    },
    "checkout": {
        "checkout_title": "🛒 Оформление заказа",
        "enter_name": "Введите ваше имя:",
        "enter_phone": "Введите ваш номер телефона:",
        "enter_address": "Введите ваш адрес доставки:",
        "order_confirmation": "🎉 Ваш заказ оформлен!\n\nДетали заказа:\n\n{order_details}",
        "confirmation_button": "✅ Подтвердить заказ"
    },
     "payment": {
        "add_payment_start": "Введите название платежа:",
        "add_payment_date": "Введите дату платежа в формате YYYY-MM-DD:",
         "add_payment_amount": "Введите сумму платежа:",
        "add_payment_category": "Введите категорию платежа:",
         "add_payment_added": "Платеж добавлен.",
         "add_payment_invalid_date": "Неверный формат даты, введите в формате YYYY-MM-DD",
          "add_payment_not_digit": "Сумма должна быть числом",
        "list_payments_title": "Список предстоящих платежей:",
         "list_payments_empty": "Нет предстоящих платежей.",
        "list_payment_item": "ID: {id}\nНазвание: {name}\nДата: {date}\nСумма: {amount}\nКатегория: {category}\n\n",
        "plan_payments_title": "Планирование платежей:",
        "plan_payments_empty": "Нет запланированных платежей.",
        "plan_payment_item": "Дата: {date}\nСумма: {amount}\n\n",
        },
    "admin": {
        "successfully_to_admin" : "Вы успешно активировали команду /start_admin и сейчас вы - админ. \nЧтобы перейти к панели управления админов, нажмите кнопку ниже. \n Чтобы вернуться в состояние обычного пользователя, воспользуйтесь командой /end_admin",
        "user_not_admin": "Вы не можете активировать команду /start_admin, так как не являетесь админом. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "end_admin_not_in_admin_state": "Вы пытаетесь вызвать команду /end_admin, не находясь в состоянии админа. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "end_admin_in_admin_state": "Вы успешно активировали команду /end_admin и теперь вы - обычный пользователь. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "message_in_admin_panel": "Вы в панели администратора. \nВыберите, что вы хотите сделать, нажав кнопку ниже(при нажатии кнопки посмотерть товары, можно так же с ними взаимодействовать) ",
        "admin_panel": "⚙️ Панель администратора",
        "add_product_button": "➕ Добавить товар",
        "edit_product_button": "✏️ Редактировать товар",
        "delete_product_button": "🗑️ Удалить товар",
        "product_added": "✅ Товар добавлен.",
        "product_edited": "✏️ Товар отредактирован.",
        "product_deleted": "🗑️ Товар удален."
    },
    'menu_buttons': {
        "catalog_title": "🛍️ Каталог товаров",
        "cart_title": "🛒 Ваша корзина",
        "perconal_account": "Личный кабинет"
    },
    "admin_panel_buttons": {
        "add_product": "➕Добавить товар",
        "show_product": "👀Посмотреть товары"
    }
}


LEXICON_COMMANDS = {
    '/start': 'Перезапустить бота',
    '/help': 'Помощь и доступные команды',
    '/start_admin': 'Перейти в панель управления админа',
    '/end_admin': 'Перейти в панель управления пользователя(от админа)'
}
