from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message
)

from src.constants.keyboard_text import KeyBoardText as kb, AdminButtons as ab
from src.handlers.admins.services.damb_all_data import dumb_data
from src.handlers.admins.services.drop_all_data import drop_all
from src.keayboards.admin_buttons import admin_buttons

from src.loader import dp


@dp.message_handler(Text(equals=kb.ADMIN_KB))
async def start_admin_menu(message: Message):
    await message.answer(
        'Админка',
        reply_markup=admin_buttons
    )


@dp.message_handler(Text(equals=ab.DUMB_ALL_DATA))
async def dumb_all_data(message: Message):
    await dumb_data(message)
    await message.answer('Загружены все данные на сайт')


@dp.message_handler(Text(equals=ab.DROP_ALL_DATA))
async def dumb_all_data(message: Message):
    await drop_all()
    await message.answer('Все данные удалены')
