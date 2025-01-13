from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import lexicon

def create_catalog_pagination_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []
    for btn in lexicon['pagination_btns'].keys():
        buttons.append(InlineKeyboardButton(text=btn, callback_data=lexicon['pagination_btns'][btn]))
    builder.row(*buttons, width=3)
    return builder.as_markup()

def create_categories_kb_to_show_catalpg(list_c: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []
    for btn in list_c:
        a = InlineKeyboardButton(text=btn, callback_data=btn)
        buttons.append(a)
    buttons.append(InlineKeyboardButton(text='Все категории', callback_data='all_cat'))
    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    builder.row(*buttons, width=1)
    return builder.as_markup()

def create_redact_bag_kb(bag_products: list[tuple]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []
    for btn in bag_products:
        a = InlineKeyboardButton(text = btn[4][:25], callback_data=str(btn[1]))
        buttons.append(a)
    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    builder.row(*buttons, width=1)
    return builder.as_markup()

def create_inline_yes_no_kb():
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text = 'Да', callback_data='yes'), InlineKeyboardButton(text = 'Нет', callback_data='no')]
    builder.row(*buttons, width=1)
    return builder.as_markup()