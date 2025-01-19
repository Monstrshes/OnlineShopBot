from aiogram import Router, F, Bot, types
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.filters import Command, CommandStart, StateFilter
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from copy import deepcopy
from aiogram.types.message import ContentType
import logging

from lexicon.lexicon_ru import lexicon
from lexicon.lexicon_for_every_magazine import lexicon_for_shop
from database.database import (create_users_bd, create_products_bd, create_bag_for_user, new_user_in_users, get_products_for_catalog, add_prod_to_user_bag, get_available_product,
                               get_quiantly_product, get_bag_products, get_product_in_bag_for_id, change_quantityprod_in_bag, delete_product_from_bag, create_orders_db,
                               clear_bag, create_new_order, get_one_order_for_user, get_orders_for_user1, get_id_and_avail_from_bag, change_available, get_username_from_userid
                               )
from keyboards.default_kb import (create_only_to_menu_kb, create_only_to_admin_panel_kb, create_menu_kb, create_in_bag_kb, create_choose_redact_kb, create_cancellation_kb,
                                  create_perconal_account_kb)
from database.additional_variables import new_product_ex, admin_categories_nodef, pr, ct,admin_categories_def
from keyboards.inline_kb import create_catalog_pagination_kb, create_categories_kb_to_show_catalpg, create_redact_bag_kb, create_inline_yes_no_kb, create_show_all_orders_kb
from services.services import create_products_list_for_bag, count_itogo
from config_data.config import load_config_pay


router = Router()

config_pay = load_config_pay()

create_users_bd() #Создаём базу данных всех пользователей
create_products_bd() #создаём каталог(базу данных всех товаров)
create_orders_db() #Создаём базу данных всех заказов

logger = logging.getLogger(__name__)

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

@router.message(StateFilter(default_state, FSMFillForm.menu, FSMFillForm.show_catalog, FSMFillForm.show_bag, FSMFillForm.payment, FSMFillForm.perconal_account), F.text == lexicon['common']['back_to_menu_button'])
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

            await callback.message.answer(
                text=lexicon['catalog']['last_product_eror'],
            )
            now_prod = products[now]
            keyboard = create_catalog_pagination_kb()
            await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
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
            await callback.message.answer(
                text=lexicon['catalog']['first_product_eror']
            )
            now_prod = products[now]
            keyboard = create_catalog_pagination_kb()
            await callback.message.answer_photo(
                photo=now_prod[5],
                caption=lexicon['catalog']['format_product_card'].format(now_prod[1], now_prod[2], now_prod[3], now_prod[4], now_prod[6]),
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
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await message.answer(
            text=lexicon['bag']['no_products'],
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
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await callback.message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await callback.message.answer(
            text=lexicon['bag']['no_products'],
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
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await message.answer(
            text=lexicon['bag']['no_products'],
            reply_markup=keyboard
        )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.redact_product), F.text == lexicon['common']['cancel_button'])
async def process_cancel_in_redact_product(message: Message, state: FSMContext):
    bag_products = get_bag_products(message.from_user.id)
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await message.answer(
            text=lexicon['bag']['no_products'],
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
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await message.answer(
            text=lexicon['bag']['no_products'],
            reply_markup=keyboard
        )
    await state.set_state(FSMFillForm.show_bag)

@router.message(StateFilter(FSMFillForm.show_bag), F.text == lexicon['bag_btns']['do_buy'])
async def process_do_buy(message: Message, state: FSMContext):
    keyboard = create_inline_yes_no_kb()
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=lexicon['bag']['buy_msg'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.do_buy)

@router.callback_query(StateFilter(FSMFillForm.do_buy), F.data == 'no')
async def process_cancel_buy(callback: CallbackQuery, state: FSMContext):
    bag_products = get_bag_products(callback.from_user.id)
    if bag_products:
        list_for_bag = create_products_list_for_bag(bag_products)
        itogo = count_itogo(bag_products)
        keyboard = create_in_bag_kb()
        await callback.message.answer(
            text=lexicon['bag']['bag_message'].format(list_for_bag, itogo),
            reply_markup=keyboard
        )
        await state.update_data({"summ_bag": itogo, "bag_msg": lexicon['bag']['bag_message'].format(list_for_bag, itogo)})
    else:
        keyboard = create_only_to_menu_kb()
        await callback.message.answer(
            text=lexicon['bag']['no_products'],
            reply_markup=keyboard
        )
    await state.set_state(FSMFillForm.show_bag)

@router.callback_query(StateFilter(FSMFillForm.do_buy), F.data == 'yes')
async def process_acess_buy(callback: CallbackQuery, state: FSMContext):
    sl = await state.get_data()
    await state.clear()
    summ_bag = int(sl['summ_bag'])
    bag_msg = sl.get('bag_msg')
    PRICE = types.LabeledPrice(label="Оплата корзины", amount=summ_bag*100)  # в копейках (руб)
    if config_pay.pay_token.split(':')[1] == 'TEST':
        await callback.message.answer(text= "Тестовый платеж!!!")

    await callback.bot.send_invoice(callback.message.chat.id,
                           title="Оплата корзины",
                           description="Оплата всех товаров, которые сейчас у вас в корзине",
                           provider_token=config_pay.pay_token,
                           currency="rub",
                           photo_url='https://cdn-icons-png.flaticon.com/512/107/107831.png',
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="payment_bag",
                           payload="test-invoice-payload")
    logger.info('Начинаем оплату')
    username = get_username_from_userid(callback.from_user.id)
    await state.update_data({'price': int(sl['summ_bag']), 'bag_msg': bag_msg, 'username': username[0]})
    await state.set_state(FSMFillForm.payment)

# pre checkout  (must be answered in 10 seconds)
@router.pre_checkout_query(StateFilter(FSMFillForm.payment))
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, state: FSMContext, bot: Bot):
    logger.info('Оплата прошла')
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@router.message(StateFilter(FSMFillForm.payment), F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext, bot: Bot, admin_chat):
    """
    Обработчик для успешных платежей
    """
    sl = await state.get_data()
    await state.clear()
    prod_list = get_id_and_avail_from_bag(message.from_user.id)
    for prod in prod_list:
        change_available(prod[0], prod[1])
    clear_bag(message.from_user.id)
    create_new_order(message.from_user.id, sl['price'], sl['bag_msg'])
    keyboard = create_only_to_menu_kb()
    await bot.send_message(
        chat_id=admin_chat,
        text=lexicon['admin']['admin_chat_new_order'].format(sl['price'], sl['username'], sl['bag_msg'][21:])
    )
    await message.answer(
            f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!",
            reply_markup=keyboard
            )

@router.message(StateFilter(FSMFillForm.menu), F.text == lexicon['menu_buttons']['perconal_account'])
async def process_show_perconal_account(message: Message, state: FSMContext):
    """
    Обрабатываем кнопку личный кабинет из меню
    """
    keyboard = create_perconal_account_kb()
    await message.answer(
        text=lexicon['perconal_ac']['show_pa_msg'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.perconal_account)

@router.message(StateFilter(FSMFillForm.perconal_account), F.text == lexicon['perconal_acc_btns']['show_orders'])
async def process_show_orders(message: Message, state: FSMContext):
    """
    Обрабатываем кнопку Посмотреть заказы из аккаунта
    """
    await message.answer(
        text=lexicon['common']['del_kb'],
        reply_markup=ReplyKeyboardRemove()
    )
    orders_list = get_orders_for_user1(message.from_user.id)
    keyboard = create_show_all_orders_kb(orders_list)
    await message.answer(
        text=lexicon['perconal_ac']['show_all_orders'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_orders)

@router.callback_query(StateFilter(FSMFillForm.show_orders), F.data == 'cancel')
async def process_cancel_from_show_orders(callback: CallbackQuery, state: FSMContext):
    keyboard = create_perconal_account_kb()
    await callback.message.answer(
        text=lexicon['perconal_ac']['show_pa_msg'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.perconal_account)

@router.callback_query(StateFilter(FSMFillForm.show_orders), F.data != 'cancel')
async def process_show_selected_order(callback:CallbackQuery, state: FSMContext):
    """
    Обрабатываем любую из инлайн кнопок с заказа
    """
    logger.info(f'callbackdata = {callback.data}')
    list_order = get_one_order_for_user(int(callback.data))
    print(list_order)
    keyboard = create_cancellation_kb()
    await callback.message.answer(
        text=lexicon['perconal_ac']['show_one_order_msg'].format(list_order[0], list_order[4][21:], list_order[5], list_order[3]),
        reply_markup=keyboard
    )

@router.message(StateFilter(FSMFillForm.show_orders), F.text == lexicon['common']['cancel_button'])
async def process_back_to_all_orders(message: Message, state: FSMContext):
    orders_list = get_orders_for_user1(message.from_user.id)
    keyboard = create_show_all_orders_kb(orders_list)
    await message.answer(
        text=lexicon['perconal_ac']['show_all_orders'],
        reply_markup=keyboard
    )
    await state.set_state(FSMFillForm.show_orders)
