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