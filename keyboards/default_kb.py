from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from lexicon.lexicon_ru import lexicon

def create_only_to_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lexicon['common']['back_to_menu_button'])]],
        resize_keyboard=True
    )
    return keyboard

def create_only_to_admin_panel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lexicon['admin']['admin_panel'])]],
        resize_keyboard=True
    )
    return keyboard

def create_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lexicon['menu_buttons']['catalog_title'])],
            [KeyboardButton(text=lexicon['menu_buttons']['cart_title'])],
            [KeyboardButton(text=lexicon['menu_buttons']['perconal_account'])]
            ],
        resize_keyboard=True
    )
    return keyboard