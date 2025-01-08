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
from database.database import create_users_bd, create_products_bd, create_bag_for_user, new_user_in_users, get_products_for_catalog, add_prod_to_user_bag
from keyboards.default_kb import create_only_to_menu_kb, create_only_to_admin_panel_kb, create_menu_kb
from database.additional_variables import new_product_ex, admin_categories_nodef, pr, ct,admin_categories_def
from keyboards.inline_kb import create_catalog_pagination_kb, create_categories_kb_to_show_catalpg


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
        pr[f'new_prod_by_{message.from_user.id}'] = deepcopy(new_product_ex)
        ct[f'admin_{message.from_user.id}_categories'] = deepcopy(admin_categories_nodef)
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

@router.message(StateFilter(FSMFillForm.menu, FSMFillForm.show_catalog, FSMFillForm.show_bag, FSMFillForm.do_buy), Command(commands='end_admin'))
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

@router.message(StateFilter(default_state, FSMFillForm.menu, FSMFillForm.show_catalog), F.text == lexicon['common']['back_to_menu_button'])
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

@router.message(StateFilter(FSMFillForm.menu), F.text == lexicon['catalog']['catalog_title'])
async def process_go_to_catalog(message: Message, state: FSMContext):
    """
    Обрабатываем кнопку Каталог товаров
    """
    if ct[f'admin_{message.from_user.id}_categories']:
        keyboard = create_categories_kb_to_show_catalpg(ct[f'admin_{message.from_user.id}_categories'])
    else:
        keyboard = create_categories_kb_to_show_catalpg(admin_categories_def)
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['catalog']['select_category'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_catalog)

@router.callback_query(StateFilter(FSMFillForm.show_catalog), ~F.data.in_(lexicon['pagination_btns'].values()) & ~F.data.in_(['cancel', 'all_cat', 'back_menu']))
async def process_get_catalpg_for_category(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатываем выбор одной из категорий
    """
    products = get_products_for_catalog(callback.data)
    now_prod = products[0]
    keyboard = create_catalog_pagination_kb()
    await callback.message.answer_photo(
        photo=now_prod[5],
        caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
        reply_markup=keyboard
    )
    await state.update_data({'products' : products, 'now': 0})


@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data == 'all_cat')
async def process_get_catalpg_for_all_category(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатываем выбор всех категорий
    """
    products = get_products_for_catalog()
    now_prod = products[0]
    keyboard = create_catalog_pagination_kb()
    await callback.message.answer_photo(
        photo=now_prod[5],
        caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
        reply_markup=keyboard
    )
    await state.update_data({'products' : products, 'now': 0})

@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data.in_(['next', 'back']))
async def process_get_next_or_back_product_in_catalog(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатываем кнопку с переходои к следующему или предыдущему товару
    """
    data =await state.get_data()
    products = data['products']
    now = data['now']
    if callback.data == 'next':
        now += 1
        if now <= len(products) - 1:
            now_prod = products[now]
            keyboard = create_catalog_pagination_kb()
            await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
                reply_markup=keyboard
            )
        else:
            now -= 1
            keyboard = create_only_to_menu_kb()
            await callback.message.answer(
                text=lexicon['catalog']['last_product_eror'],
                reply_markup=keyboard
            )
    elif callback.data == 'back':
        now -= 1
        if now >= 0:
            now_prod = products[now]
            keyboard = create_catalog_pagination_kb()
            await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
                reply_markup=keyboard
            )
        else:
            now += 1
            keyboard = create_only_to_menu_kb()
            await callback.message.answer(
                text=lexicon['catalog']['first_product_eror'],
                reply_markup=keyboard
            )
    await state.update_data({'products' : products, 'now': now})

@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data=='add_to_bag')
async def process_add_product_to_user_bag(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    products = data['products']
    now = data['now']
    now_prod = products[now]
    add_prod_to_user_bag(callback.from_user.id, now_prod)
    keyboard = create_catalog_pagination_kb()
    await callback.message.answer(
        text=lexicon['catalog']['aded_to_bag']
    )
    await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
                reply_markup=keyboard
    )

@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data=='back_menu')
@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data=='cancel')
async def process_back_menu_from_catalog(callback: CallbackQuery, state: FSMContext):
    keyboard = create_menu_kb()
    await callback.message.answer(
        text =lexicon['common']['menu_message'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu)