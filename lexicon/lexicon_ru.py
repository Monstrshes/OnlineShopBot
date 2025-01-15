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
        "no_products_available": "😞 Извините, пока нет доступных товаров.",
        'del_kb': 'Удаляем ненужную клавиатуру)'
    },
    "catalog": {
        "catalog_title": "🛍️ Каталог товаров",
        "format_product_card": "<b>{}</b> \n\n\t{} \n\n<b>Цена:</b> {} \n\n<b>Категория:</b> {} \n\n<i>В наличии: {}</i>",
        "select_category": "Выберите категорию товаров, которую вы хотите посмотерть:",
        "select_product": "Выберите товар:",
        "product_info": "ℹ️ {title}\n\n{description}\n\nЦена: {price} руб.",
        "add_to_cart_button": "🛒 Добавить в корзину",
        'last_product_eror': '<b>Ошибка!</b> Больше товаров нет( \nНажмите на любую другую кнопку',
        'first_product_eror': '<b>Ошибка!</b> Это первый товар \nНажмите на любую другую кнопку',
        'aded_to_bag': '<b>Успешно добавлено в корзину!</b>',
        'not_aded_to_bag_av': 'К сожалению, такого количества товара нет в наличии'
    },
    'bag':{
        'bag_message': 'Это - ваша корзина: \n\n{} \n<b>Итого:{}</b>',
        'redact_bag_message': 'Выберите продукт, который вы хотели бы редактировать',
        'redact_quantity_prod': 'Введите необходимое количество данного продукта(число > 0)',
        'quantity_changed': 'Количество товара в корзине успешно изменено',
        'quantity_more_than_avail': 'Столько товара нет в наличии. <b>Количество товара в корзине не изменено</b>',
        'product_deleted': 'Товар успешно удалён',
        'buy_msg': 'Хотите оплатить товары из вашей корзины?',
        'no_products': 'В ваше корзине ничего нет( Добавьте что-нибудь в неё, а потом возвращайтесь'
    },
    "cart": {
        "cart_title": "🛒 Ваша корзина",
        "cart_item": " {} - {} шт. x {} руб. = {} руб.",
        "total_amount": "💰 Итого: {total_amount} руб.",
        "checkout_button": "✅ Перейти к оформлению заказа",
        "clear_cart_button": "🗑️ Очистить корзину"
    },
    'perconal_ac':{
        'show_pa_msg': 'Вы в вашем личном кабинете. \n\nВыберите, что вы хотите сделать дальше',
        'show_all_orders': 'Это все ваши заказы. \nНажмите на один из них, чтобы увидеть более подробную информацию.',
        'inline_bt_orders': 'Заказ №{} на сумму {}р.',
        'show_one_order_msg': 'Номер Вашего заказа: {}\nОн включает в себя: \n{} \n\nЗаказ сделан: {} \n\nСтатус заказа: <b>{}</b>'
    },
    "admin": {
        "successfully_to_admin" : "Вы успешно активировали команду /start_admin и сейчас вы - админ. \nЧтобы перейти к панели управления админов, нажмите кнопку ниже. \nЧтобы вернуться в состояние обычного пользователя, воспользуйтесь командой /end_admin",
        "user_not_admin": "Вы не можете активировать команду /start_admin, так как не являетесь админом. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "end_admin_not_in_admin_state": "Вы пытаетесь вызвать команду /end_admin, не находясь в состоянии админа. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "end_admin_in_admin_state": "Вы успешно активировали команду /end_admin и теперь вы - обычный пользователь. \nЧтобы вернуться в меню нажмите кнопку ниже",
        "message_in_admin_panel": "Вы в панели администратора. \nВыберите, что вы хотите сделать, нажав кнопку ниже(при нажатии кнопки посмотреть товары, можно так же с ними взаимодействовать) ",
        "add_name_product": 'Введите название товара:',
        'add_descr_product': 'Введите описание товара:',
        'add_price_product': 'Введите цену товара(число >0):',
        'add_photo_product': 'Пришлите фото товара:',
        'add_category_product': 'Выберите категорию товара:',
        'add_avaible_product': 'Введите количество товара, которое вы готовы продать или нажмите на кнопку "Несколько", если не хотите это делать',
        "admin_panel": "⚙️ Панель администратора",
        "add_product_button": "➕ Добавить товар",
        "edit_product_button": "✏️ Редактировать товар",
        "delete_product_button": "🗑️ Удалить товар",
        "product_added": "✅ Товар добавлен.",
        "product_edited": "✏️ Товар отредактирован.",
        "product_deleted": "🗑️ Товар удален.",
        'no_photo_button' :'Товар без фото',
        'no_available_button': 'Несколько',
        'product_not_add' : '<b>ТОВАР НЕ ДОБАВЛЕН</b>. Вы снова в панели администратора',
        'yes_or_no_to_product':'Вот так выглядит ваш товар. \nДобавляем?',
        'product_no_add':'Товар не добавлен',
        'product_is_add': 'ТОВАР ДОБАВЛЕН'
    },
    'menu_buttons': {
        "catalog_title": "🛍️ Каталог товаров",
        "cart_title": "🛒 Ваша корзина",
        "perconal_account": "Личный кабинет"
    },
    "admin_panel_buttons": {
        "add_product": "➕Добавить товар",
        "show_product": "👀Посмотреть товары"
    },
    'eror_msg': 'Что-то пошло не так. Нажмите /help, чтобы узнать список доступных команд и вернуться в меню',
    'pagination_btns': {
        '⬅️' :'back',
        'Добавить в корзину': 'add_to_bag',
        '➡️': 'next',
        'Вернуться в меню':'back_menu'
        },
    'bag_btns':{
        'redact': '✏️Редактировать корзину',
        'do_buy': '💰Оформить заказ',
        'redact_quantity': '✏️Изменить количество',
        'delete': '❌Удалить из корзины'
    },
    'perconal_acc_btns': {
        'show_orders': '👀Посмотреть заказы',
        'helping': 'Поддержка'

    }
}


LEXICON_COMMANDS = {
    '/start': 'Перезапустить бота',
    '/help': 'Помощь и доступные команды',
    '/start_admin': 'Перейти в панель управления админа',
    '/end_admin': 'Перейти в панель управления пользователя(от админа)'
}
