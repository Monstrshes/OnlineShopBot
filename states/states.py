from aiogram.fsm.state import  State, StatesGroup

class FSMFillForm(StatesGroup):
    menu = State() #Состояние меню обычного пользолателя
    show_catalog = State() #Состояние просмотра каталога товаров для пользователя
    show_bag = State() #состояние для просмотра корзины для обычного пользователя
    redact_bag = State() #Состояние для редактирования корзины
    redact_product = State() #Состояние для редактирования конкретного продукта из корзины
    do_buy = State() #состояние для покупки для пользователя
    payment = State()

    menu_a = State() #Состояние меню админа
    add_product_price_a = State() #состояние для добавления цены товара для админа
    add_product_name_a = State() #Состоляние для добавления назавания товара
    add_product_descr_a = State() #Состояние для ввода описания товара
    add_product_photo_a = State() #состояние для ввода фото товара
    add_product_category = State() #состояние для выбора категории  продукта
    add_product_available_a = State() #Состояние для ввода количества товара
    y_or_n_to_add_product_a  = State() #окончательное согласие или отказ на добавление товара