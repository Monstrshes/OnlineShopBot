from aiogram import Router, F, Bot
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, FSInputFile

from lexicon.lexicon_ru import lexicon
from lexicon.lexicon_for_every_magazine import lexicon_for_shop
from  database.database import create_users_bd, create_products_bd, create_bag_for_user, new_user_in_users
from keyboards.default_kb import create_only_to_menu_kb, create_only_to_admin_panel_kb, create_menu_kb


router = Router()

create_users_bd() #Создаём базу данных всех пользователей
create_products_bd() #создаём каталог(базу данных всех товаров)

@router.message(CommandStart())
async def process_start_message(message: Message, state: FSMContext, admin_ids):
    """
    Обрабатываем на /start в любых состояниях
    """
    create_bag_for_user(message.from_user.id)
    if message.from_user.id in admin_ids:
        role = 'admin'
    else: role = 'user'
    new_user_in_users(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, role)
    await message.answer(
        text=lexicon['common']['start_message'].format(lexicon_for_shop['shop_name']),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(default_state)


@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    """
    Обрабатываем /help в любом состоянии
    """
    keyboard = create_only_to_menu_kb()
    await message.answer(
        text=lexicon['common']['help_message'],
        reply_markup=keyboard
    )
    await state.set_state(default_state)

@router.message(Command(commands='start_admin'))
async def process_to_admin_panel(message: Message, state: FSMContext, admin_ids):
    """
    Обрабатываем команду /start_admin. Если пользователь админ - переводим его к панели админа, иначе говорим ему, что он не админ.
    """
    if message.from_user.id in admin_ids:
        keyboard = create_only_to_admin_panel_kb()
        await message.answer(
            text=lexicon['admin']['successfully_to_admin'],
            reply_markup=keyboard
        )
        await state.set_state(FSMFillForm.menu_a)

    else:
        keyboard = create_only_to_menu_kb()
        await message.answer(
            text=lexicon['admin']['user_not_admin'],
            reply_markup=keyboard
        )
        await state.set_state(default_state)

@router.message(~StateFilter(FSMFillForm.menu_a, FSMFillForm.add_product_a), Command(commands='end_admin'))
async def process_to_end_admin_NOT_IN_ADMIN_STATE(message: Message, state: FSMContext):
    """
    Обрабатываем команду /end_admin НЕ В СОСТОЯНИИ АДМИНА.
    Эту же команду в состоянии админа я обработаю в admin_handlers
    """
    keyboard = create_only_to_menu_kb()
    await message.answer(
        text=lexicon['admin']['end_admin_not_in_admin_state'],
        reply_markup=keyboard
    )
    await state.set_state(default_state)

@router.message(StateFilter(default_state), F.text == lexicon['common']['back_to_menu_button'])
async def process_go_to_menu(message: Message, state: FSMContext):
    """
    Обрабатывваем кнопку Вернуться в меню в следующих состояниях:
    1. default_state
    """
    keyboard = create_menu_kb()
    await message.answer(
        text =lexicon['common']['menu_message'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu)