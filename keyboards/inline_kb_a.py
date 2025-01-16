from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import lexicon


def create_categories_kb(list_c: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []
    for btn in list_c:
        a = InlineKeyboardButton(text=btn, callback_data=btn)
        buttons.append(a)
    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    builder.row(*buttons, width=1)
    return builder.as_markup()

def create_products_to_redact_kb(list_prod: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []
    for prod in list_prod:
        a = InlineKeyboardButton(text=prod[1], callback_data=str(prod[0]))
        buttons.append(a)
    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    builder.row(*buttons, width=1)
    return builder.as_markup()