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
from database.database import (create_users_bd, create_products_bd, create_bag_for_user, new_user_in_users, get_products_for_catalog, add_prod_to_user_bag, get_available_product,
                               get_quiantly_product, get_bag_products, get_product_in_bag_for_id, change_quantityprod_in_bag, delete_product_from_bag)
from keyboards.default_kb import (create_only_to_menu_kb, create_only_to_admin_panel_kb, create_menu_kb, create_in_bag_kb, create_choose_redact_kb, create_cancellation_kb)
from database.additional_variables import new_product_ex, admin_categories_nodef, pr, ct,admin_categories_def
from keyboards.inline_kb import create_catalog_pagination_kb, create_categories_kb_to_show_catalpg, create_redact_bag_kb
from services.services import create_products_list_for_bag, count_itogo

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

@router.message(StateFilter(default_state, FSMFillForm.menu, FSMFillForm.show_catalog, FSMFillForm.show_bag), F.text == lexicon['common']['back_to_menu_button'])
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
    """
    Добавляем товар в корзину, обрабатывая инлайн кнопку в каталоге
    """
    data = await state.get_data()
    products = data['products']
    now = data['now']
    now_prod = products[now]
    available = get_available_product(now_prod[0])
    quiantly = get_quiantly_product(callback.from_user.id, now_prod[0])
    if available == 'Несколько' or quiantly + 1 <= available:
        add_prod_to_user_bag(callback.from_user.id, now_prod)
        await callback.message.answer(
            text=lexicon['catalog']['aded_to_bag']
        )
    else:
        await callback.message.answer(
            text=lexicon['catalog']['not_aded_to_bag_av']
        )
    keyboard = create_catalog_pagination_kb()
    await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
                reply_markup=keyboard
    )

@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data == 'back_menu')
async def process_back_menu_from_catalog(callback: CallbackQuery, state: FSMContext):
    keyboard = create_menu_kb()
    await callback.message.answer(
        text =lexicon['common']['menu_message'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu)


@router.callback_query(StateFilter(FSMFillForm.show_catalog), F.data == 'cancel')
async def process_back_menu_from_catalog_(callback: CallbackQuery, state: FSMContext):
    keyboard = create_menu_kb()
    await callback.message.answer(
        text =lexicon['common']['menu_message'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.menu)

@router.message(StateFilter(FSMFillForm.menu), F.text == lexicon['menu_buttons']['cart_title'])
async def process_to_user_bag_go(message: Message, state: FSMContext):
    bag_products = get_bag_products(message.from_user.id)
    list_for_bag = create_products_list_for_bag(bag_products)
    itogo = count_itogo(bag_products)
    keyboard = create_in_bag_kb()
    await message.answer(
        text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.show_bag), F.text == lexicon['bag_btns']['redact'])
async def process_go_to_redact_bag(message: Message, state: FSMContext):
    bag_products = get_bag_products(message.from_user.id)
    keyboard = create_redact_bag_kb(bag_products)
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['bag']['redact_bag_message'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.redact_bag)

@router.callback_query(StateFilter(FSMFillForm.redact_bag), F.data != 'cancel')
async def process_choose_product_to_redact(callback: CallbackQuery, state: FSMContext):
    keyboard = create_choose_redact_kb()
    pr = get_product_in_bag_for_id(callback.from_user.id, int(callback.data))
    await callback.message.answer(
        text=lexicon['cart']['cart_item'].format(pr[4], pr[2], pr[3], pr[3]*pr[2]),
        reply_markup=keyboard
    )
    await state.update_data({'product_id_to_redact': int(callback.data)})
    await state.set_state(FSMFillForm.redact_product)

@router.callback_query(StateFilter(FSMFillForm.redact_bag), F.data == 'cancel')
async def process_cancel_from_redact_bag(callback: CallbackQuery, state: FSMContext):
    bag_products = get_bag_products(callback.from_user.id)
    list_for_bag = create_products_list_for_bag(bag_products)
    itogo = count_itogo(bag_products)
    keyboard = create_in_bag_kb()
    await callback.message.answer(
        text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.redact_product), F.text == lexicon['bag_btns']['redact_quantity'])
async def process_redact_quantity_product(message: Message, state: FSMContext):
    keyboard = create_cancellation_kb()
    await message.answer(
        text=lexicon['bag']['redact_quantity_prod'],
        reply_markup=keyboard
    )

@router.message(StateFilter(FSMFillForm.redact_product), lambda x: x.text.isdigit() and 0 < int(x.text))
async def process_change_quantity_product(message: Message, state: FSMContext):
    prod_id = await state.get_data()
    available = get_available_product(prod_id['product_id_to_redact'])
    if available == 'Несколько' or available >= int(message.text):
        change_quantityprod_in_bag(message.from_user.id, prod_id['product_id_to_redact'], int(message.text))
        await message.answer(
            text=lexicon['bag']['quantity_changed']
        )
    else:
        await message.answer(
            text=lexicon['bag']['quantity_more_than_avail']
        )
    bag_products = get_bag_products(message.from_user.id)
    list_for_bag = create_products_list_for_bag(bag_products)
    itogo = count_itogo(bag_products)
    keyboard = create_in_bag_kb()
    await message.answer(
        text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.redact_product), F.text == lexicon['common']['cancel_button'])
async def process_cancel_in_redact_product(message: Message, state: FSMContext):
    bag_products = get_bag_products(message.from_user.id)
    list_for_bag = create_products_list_for_bag(bag_products)
    itogo = count_itogo(bag_products)
    keyboard = create_in_bag_kb()
    await message.answer(
        text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.redact_product), F.text == lexicon['bag_btns']['delete'])
async def process_delete_product_from_bag(message: Message, state: FSMContext):
    prod_id = await state.get_data()
    delete_product_from_bag(message.from_user.id, prod_id['product_id_to_redact'])
    await message.answer(
        text=lexicon['bag']['product_deleted']
    )
    bag_products = get_bag_products(message.from_user.id)
    list_for_bag = create_products_list_for_bag(bag_products)
    itogo = count_itogo(bag_products)
    keyboard = create_in_bag_kb()
    await message.answer(
        text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_bag)