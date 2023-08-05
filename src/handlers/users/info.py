from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.constants.keyboard_text import KeyBoardText as kb
from src.constants.constants import ABOUT_US, WHAT_WE_CAN
from src.loader import dp


@dp.message_handler(Text(equals=kb.ABOUT_US))
async def run_start_command(messages: Message):
    await messages.answer(ABOUT_US)


@dp.message_handler(Text(equals=kb.WHAT_WE_CAN))
async def run_start_command(messages: Message):
    await messages.answer(WHAT_WE_CAN)
