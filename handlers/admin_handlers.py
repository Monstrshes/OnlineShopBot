from aiogram import Router, F, Bot
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from copy import deepcopy

from lexicon.lexicon_ru import lexicon
from lexicon.lexicon_for_every_magazine import lexicon_for_shop
from database.database import  add_product
from keyboards.default_kb import create_only_to_menu_kb, create_cancellation_kb, create_yes_no_kb
from keyboards.default_kb_a import create_admin_panel_kb, create_add_photo_kb, create_add_available_kb
from database.additional_variables import admin_categories_def, new_product_ex, pr, ct
from keyboards.inline_kb_a import create_categories_kb

router = Router()

@router.message(StateFilter(FSMFillForm.y_or_n_to_add_product_a,FSMFillForm.menu_a, FSMFillForm.add_product_available_a, FSMFillForm.add_product_category, FSMFillForm.add_product_descr_a, FSMFillForm.add_product_name_a, FSMFillForm.add_product_photo_a, FSMFillForm.add_product_price_a), Command(commands='end_admin'))
async def process_end_admin_in_admin(message: Message, state: FSMContext):
    """
    Возвращаем админа в соястояние обычного пользователя
    """
    pr[f'new_prod_by_{message.from_user.id}'].clear()
    pr[f'new_prod_by_{message.from_user.id}'] = deepcopy(new_product_ex)
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

@router.message(StateFilter(FSMFillForm.menu_a), F.text == lexicon['admin_panel_buttons']['add_product'])
async def process_start_add_product(message: Message, state: FSMContext):
    """
    Обрабатываем нажатие кнопки Добавить товар
    """
    keyboard = create_cancellation_kb()
    await message.answer(
        text=lexicon['admin']['add_name_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_name_a)

@router.message(StateFilter(FSMFillForm.add_product_available_a, FSMFillForm.add_product_descr_a, FSMFillForm.add_product_name_a, FSMFillForm.add_product_photo_a, FSMFillForm.add_product_price_a), F.text == lexicon['common']['cancel_button'])
async def process_back_to_admin_panel(message: Message, state: FSMContext):
    pr[f'new_prod_by_{message.from_user.id}'].clear()
    pr[f'new_prod_by_{message.from_user.id}'] = deepcopy(new_product_ex)
    keyboard = create_admin_panel_kb()
    await message.answer(
        text=lexicon['admin']['product_no_add']
    )
    await message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu_a)

@router.message(StateFilter(FSMFillForm.add_product_name_a))
async def process_add_name_product(message: Message, state: FSMContext):
    """
    Обрабатываем ввод названия товара
    """
    pr[f'new_prod_by_{message.from_user.id}']['name'] = message.text
    keyboard = create_cancellation_kb()
    await message.answer(
        text=lexicon['admin']['add_descr_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_descr_a)

@router.message(StateFilter(FSMFillForm.add_product_descr_a))
async def process_add_description_product(message: Message, state: FSMContext):
    """
    Обрабатываем ввод описания товара
    """
    pr[f'new_prod_by_{message.from_user.id}']['descr'] = message.text
    keyboard = create_cancellation_kb()
    await message.answer(
        text=lexicon['admin']['add_price_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_price_a)

@router.message(StateFilter(FSMFillForm.add_product_price_a), lambda x: x.text.isdigit() and 0 < int(x.text))
async def process_add_price_product(message: Message, state: FSMContext):
    """
    Обрабатываем ввод цены товара
    """
    pr[f'new_prod_by_{message.from_user.id}']['price'] = int(message.text)
    if ct[f'admin_{message.from_user.id}_categories']:
        keyboard = create_categories_kb(ct[f'admin_{message.from_user.id}_categories'])
    else:
        keyboard = create_categories_kb(admin_categories_def)
    await message.answer(
        text=lexicon['admin']['add_category_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_category)

@router.callback_query(StateFilter(FSMFillForm.add_product_category), F.data != 'cancel')
async def process_add_category_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text = lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    pr[f'new_prod_by_{callback.from_user.id}']['category'] = callback.data
    keyboard = create_add_photo_kb()
    await callback.message.answer(
        text=lexicon['admin']['add_photo_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_photo_a)

@router.callback_query(StateFilter(FSMFillForm.add_product_category), F.data == 'cancel')
async def process_add_category_product(callback: CallbackQuery, state: FSMContext):
    """
    Кнопка Отмена вместо выбора  категории
    """
    pr[f'new_prod_by_{callback.from_user.id}'].clear()
    pr[f'new_prod_by_{callback.from_user.id}'] = deepcopy(new_product_ex)
    keyboard = create_admin_panel_kb()
    await callback.message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )
    await callback.message.answer(
        tetxt=lexicon['admin']['product_not_add'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu_a)


@router.message(StateFilter(FSMFillForm.add_product_photo_a), F.photo)
async def process_add_photo_product(message: Message, state: FSMContext):
    """
    Обрабатываем отправку фото товара
    """
    pr[f'new_prod_by_{message.from_user.id}']['photo'] = message.photo[0].file_id
    keyboard = create_add_available_kb()
    await message.answer(
        text = lexicon['admin']['add_avaible_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_available_a)

@router.message(StateFilter(FSMFillForm.add_product_photo_a), F.text == lexicon['admin']['no_photo_button'])
async def process_no_photo_product(message: Message, state: FSMContext):
    """
    Обрабатываем отправку фото товара
    """
    pr[f'new_prod_by_{message.from_user.id}']['photo'] = 'no photo'
    keyboard = create_add_available_kb()
    await message.answer(
        text = lexicon['admin']['add_avaible_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.add_product_available_a)


@router.message(StateFilter(FSMFillForm.add_product_available_a), lambda x: x.text.isdigit() and 0 < int(x.text))
async def process_add_count_available_product(message: Message, state: FSMContext):
    pr[f'new_prod_by_{message.from_user.id}']['available'] = int(message.text)
    pr[f'new_prod_by_{message.from_user.id}']['is_full'] = True
    keyboard = create_yes_no_kb()
    await message.answer_photo(
        photo=pr[f'new_prod_by_{message.from_user.id}']['photo'],
        caption=lexicon['catalog']['format_product_card'].format(pr[f'new_prod_by_{message.from_user.id}']['name'], pr[f'new_prod_by_{message.from_user.id}']['descr'], pr[f'new_prod_by_{message.from_user.id}']['price'], pr[f'new_prod_by_{message.from_user.id}']['category'], pr[f'new_prod_by_{message.from_user.id}']['available'])
    )
    await message.answer(
        text=lexicon['admin']['yes_or_no_to_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.y_or_n_to_add_product_a)

@router.message(StateFilter(FSMFillForm.add_product_available_a), F.text == 'Несколько')
async def pprocess_add_count_available_product(message: Message, state: FSMContext):
    """
    обрабатываем  кнопку несколько при  вводе товара в наличии
    """
    pr[f'new_prod_by_{message.from_user.id}']['available'] = message.text
    pr[f'new_prod_by_{message.from_user.id}']['is_full'] = True
    keyboard = create_yes_no_kb()
    await message.answer_photo(
        photo=pr[f'new_prod_by_{message.from_user.id}']['photo'],
        caption=lexicon['catalog']['format_product_card'].format(pr[f'new_prod_by_{message.from_user.id}']['name'], pr[f'new_prod_by_{message.from_user.id}']['descr'], pr[f'new_prod_by_{message.from_user.id}']['price'], pr[f'new_prod_by_{message.from_user.id}']['category'], pr[f'new_prod_by_{message.from_user.id}']['available'])
    )
    await message.answer(
        text=lexicon['admin']['yes_or_no_to_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.y_or_n_to_add_product_a)

@router.message(StateFilter(FSMFillForm.y_or_n_to_add_product_a), F.text == 'Да')
async def process_adding_product(message: Message, state: FSMContext):
    """
    Обрабатываем кнопку Да и добавляем товар
    """
    if pr[f'new_prod_by_{message.from_user.id}']['is_full'] == True:
        add_product(pr[f'new_prod_by_{message.from_user.id}'])
    pr[f'new_prod_by_{message.from_user.id}'].clear()
    pr[f'new_prod_by_{message.from_user.id}'] = deepcopy(new_product_ex)
    keyboard = create_admin_panel_kb()
    await message.answer(
        text=lexicon['admin']['product_is_add']
    )
    await message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu_a)

@router.message(StateFilter(FSMFillForm.y_or_n_to_add_product_a), F.text == 'Нет')
async def process_not_adding_product(message: Message, state: FSMContext):
    pr[f'new_prod_by_{message.from_user.id}'].clear()
    pr[f'new_prod_by_{message.from_user.id}'] = deepcopy(new_product_ex)
    keyboard = create_admin_panel_kb()
    await message.answer(
        text=lexicon['admin']['product_no_add']
    )
    await message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu_a)
