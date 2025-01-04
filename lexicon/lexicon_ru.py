lexicon = {
    "common": {
        "start_message": "Привет! 👋 Добро пожаловать в наш онлайн-магазин {}! ",#имя магазина
        "help_message": "Вот список доступных команд:\n\n/start - Начать работу с ботом\n/help - Показать это сообщение\n/admin - Перейти в панель управления для админов\nвыйти из панели управления для админов",
        "back_button": "⬅️ Назад",
        "cancel_button": "❌ Отмена",
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
        "admin_panel": "⚙️ Панель администратора",
        "add_product_button": "➕ Добавить товар",
        "edit_product_button": "✏️ Редактировать товар",
        "delete_product_button": "🗑️ Удалить товар",
        "product_added": "✅ Товар добавлен.",
        "product_edited": "✏️ Товар отредактирован.",
        "product_deleted": "🗑️ Товар удален."
    }
}


LEXICON_COMMANDS = {
    '/start': 'Перезапустить бота',
    '/help': 'Помощь',
    '/start_admin': 'Перейти в панель управления админа',
    '/end_admin': 'Перейти в панель управления пользователя(от админа)'
}
