from aiogram.fsm.state import  State, StatesGroup

class FSMFillForm(StatesGroup):
    menu = State() #Состояние меню обычного пользолателя
    show_catalog = State() #Состояние просмотра каталога товаров для пользователя
    show_bag = State() #состояние для просмотра корзины для обычного пользователя
    do_buy = State() #состояние для покупки для пользователя

    menu_a = State() #Состояние меню админа
    add_product_a = State() #состояние для добавления товара для админа