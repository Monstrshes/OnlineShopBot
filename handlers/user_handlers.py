from aiogram import Router, F, Bot
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, FSInputFile

from lexicon.lexicon_ru import lexicon
from lexicon.lexicon_for_every_magazine import lexicon_for_shop

router = Router()

@router.message(StateFilter(FSMFillForm.default_state), CommandStart())
async def process_start_message(message: Message, state: FSMContext):
    await message.answer(
        text=lexicon['common']['start_message'].format(lexicon_for_shop['shop_name']),
        reply_markup=ReplyKeyboardRemove()
    )
