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