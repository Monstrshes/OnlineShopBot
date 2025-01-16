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
from database.database import  add_product, get_products_to_redact_kb, get_product_with_prod_id, change_price_prod, change_price_prod, del_product
from keyboards.default_kb import create_only_to_menu_kb, create_cancellation_kb, create_yes_no_kb
from keyboards.default_kb_a import create_admin_panel_kb, create_add_photo_kb, create_add_available_kb, create_redact_product_kb
from database.additional_variables import admin_categories_def, new_product_ex, pr, ct
from keyboards.inline_kb_a import create_categories_kb, create_products_to_redact_kb

router = Router()

@router.message(StateFilter(FSMFillForm.y_or_n_to_add_product_a,FSMFillForm.menu_a, FSMFillForm.add_product_available_a, FSMFillForm.add_product_category, FSMFillForm.add_product_descr_a, FSMFillForm.add_product_name_a, FSMFillForm.add_product_photo_a, FSMFillForm.add_product_price_a, FSMFillForm.redact_avail, FSMFillForm.redact_price, FSMFillForm.redact_product_a), Command(commands='end_admin'))
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
    await state.clear()
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

@router.message(StateFilter(FSMFillForm.menu_a), F.text == lexicon['admin_panel_buttons']['show_product'])
async def process_go_to_redact_catalog(message: Message,  state: FSMContext):
    """
    обрабатываем кнопку редактировать товары в панели админа
    """
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )

    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_product_a)

@router.callback_query(StateFilter(FSMFillForm.redact_product_a), F.data == 'cancel')
async def process_cancel_to_chose_product(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатываем инлайн-кнопку отмена
    """
    keyboard = create_admin_panel_kb()
    await callback.message.answer(
        text=lexicon['admin']['product_no_add']
    )
    await callback.message.answer(
        text=lexicon['admin']['message_in_admin_panel'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu_a)

@router.callback_query(StateFilter(FSMFillForm.redact_product_a), F.data != 'cancel')
async def process_go_to_prod_to_redact(callback: CallbackQuery, state: FSMContext):
    now_prod = get_product_with_prod_id(int(callback.data))
    keyboard = create_redact_product_kb()
    await callback.message.answer_photo(
        photo=now_prod[5],
        caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
        reply_markup=keyboard
    )
    await state.update_data({'prod_id': now_prod[0]})


@router.message(StateFilter(FSMFillForm.redact_product_a), F.text == lexicon['redact_product_btns']['redact_price'])
async def process_change_price(message: Message, state: FSMContext):
    keyboard = create_cancellation_kb()
    await message.answer(
        text=lexicon['admin']['add_price_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_price)

@router.message(StateFilter(FSMFillForm.redact_price), lambda x: x.text.isdigit() and 0 < int(x.text))
async def process_cnanged_price(message: Message, state: FSMContext):
    sl = await state.get_data()
    await state.clear()
    change_price_prod(sl['prod_id'], int(message.text))
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['admin']['price_changed']
    )

    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_product_a)

@router.message(StateFilter(FSMFillForm.redact_price, FSMFillForm.redact_avail, FSMFillForm.redact_product_a), F.text == lexicon['common']['cancel_button'])
async def process_cancel_to_change(message: Message, state: FSMContext):
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.clear()
    await state.set_state(FSMFillForm.redact_product_a)


#############################################
@router.message(StateFilter(FSMFillForm.redact_product_a), F.text == lexicon['redact_product_btns']['redact_avail'])
async def process_change_price(message: Message, state: FSMContext):
    keyboard = create_add_available_kb()
    await message.answer(
        text=lexicon['admin']['add_avaible_product'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_avail)

@router.message(StateFilter(FSMFillForm.redact_avail), lambda x: x.text.isdigit() and 0 < int(x.text))
async def process_cnanged_price(message: Message, state: FSMContext):
    sl = await state.get_data()
    await state.clear()
    change_price_prod(sl['prod_id'], int(message.text))
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['admin']['avail_changed']
    )

    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_product_a)

@router.message(StateFilter(FSMFillForm.redact_avail), F.text == 'Несколько')
async def process_cnanged_price1(message: Message, state: FSMContext):
    sl = await state.get_data()
    await state.clear()
    change_price_prod(sl['prod_id'], message.text)
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['admin']['avail_changed']
    )

    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_product_a)

@router.message(StateFilter(FSMFillForm.redact_product_a), F.text == lexicon['redact_product_btns']['del_prod'])
async def process_delete_product(message: Message, state: FSMContext):
    sl = await state.get_data()
    await state.clear()
    del_product(sl['prod_id'])
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['admin']['prod_deleted']
    )

    list_prod = get_products_to_redact_kb()
    keyboard = create_products_to_redact_kb(list_prod)
    await message.answer(
        text=lexicon['admin']['choose_prod_to_red'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_product_a)