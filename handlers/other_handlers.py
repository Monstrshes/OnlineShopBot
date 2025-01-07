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

router = Router()

@router.message()
async def process_other_message(message: Message):
    await message.answer(
        text=lexicon['eror_msg']
    )