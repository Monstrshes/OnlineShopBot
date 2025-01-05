from aiogram import Router, F, Bot
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, FSInputFile

from lexicon.lexicon_ru import lexicon
from lexicon.lexicon_for_every_magazine import lexicon_for_shop
from  database.database import create_users_bd, create_products_bd, create_bag_for_user
from keyboards.default_kb import create_only_to_menu_kb
from keyboards.default_kb_a import create_admin_panel_kb

router = Router()

@router.message(StateFilter(FSMFillForm.menu_a, FSMFillForm.add_product_a), Command(commands='end_admin'))
async def process_end_admin_in_admin(message: Message, state: FSMContext):
    """
    Возвращаем админа в соястояние обычного пользователя
    """
    keyboard = create_only_to_menu_kb()
    await message.answer(
        text=lexicon['admin']['end_admin_in_admin_state'],
        reply_markup=keyboard
    )
    await state.set_state(default_state)

@router.message(StateFilter(FSMFillForm.menu_a), F.text == lexicon['admin']['admin_panel'])
async def process_to_panel_admin(message: Message, state: FSMContext):
    """
    Обрабатываем кнопку Панель администратора
    """
    keyboard = create_admin_panel_kb()
    await message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )