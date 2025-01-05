from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from lexicon.lexicon_ru import lexicon

def create_admin_panel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lexicon['admin_panel_buttons']['add_product'])],
            [KeyboardButton(text=lexicon['admin_panel_buttons']['show_product'])]
        ],
        resize_keyboard=True
    )
    return keyboard