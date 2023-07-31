import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.bot.constants import constants
from src.bot.constants.keyboard_text import KeyBoardText, \
    OrderStateButtons as ok
from src.bot.keayboards.inline_buttons import get_contact_links
from src.bot.keayboards.main_menu import get_kb
from src.bot.loader import dp


@dp.message_handler(text='/start')
async def run_start_command(messages: Message):
    mes = constants.START_SCREEN
    await messages.answer(mes, reply_markup=get_kb(messages.from_user.id))
    logging.debug(messages.from_user)


@dp.message_handler(Text(equals=KeyBoardText.CONTACT_US))
@dp.message_handler(text='/contact_us')
async def get_contatcs_command(messages: Message):
    mes = constants.CONTACT_US
    await messages.answer(mes, reply_markup=get_contact_links())
    await messages.answer(
        'Так же вы можете заказать звонок нашему администратору в рабочее время',
        reply_markup=get_kb(messages.from_user.id))


@dp.message_handler(Text(equals=KeyBoardText.BACK_TO_MAIN))
@dp.message_handler(Text(equals=ok.FINISH_ORDER, ignore_case=True), state="*")
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Вы вернулись на главную.',
        reply_markup=get_kb(message.from_user.id)
    )


@dp.message_handler(commands="/cancel", state="*")
@dp.message_handler(Text(equals="/cancel", ignore_case=True), state="*")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Вы вернулись на главную.',
        reply_markup=get_kb(message.from_user.id)
    )


@dp.message_handler(text="/help", state="*")
async def cmd_help(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        f'Здесь Вы можете получить описание работы бота\n{constants.HELP_TEXT}',
        reply_markup=get_kb(message.from_user.id)
    )
