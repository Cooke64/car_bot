from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message
)

from src.bot.constants.keyboard_text import KeyBoardText as kb
from src.bot.keayboards.admin_buttons import admin_buttons
from src.bot.loader import dp


@dp.message_handler(Text(equals=kb.ADMIN_KB))
async def start_user_test(message: Message):
    await message.answer(
        'Админка',
        reply_markup=admin_buttons
    )
