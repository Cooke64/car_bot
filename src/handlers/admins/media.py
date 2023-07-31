from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    ContentType, InputFile
)

from get_media_files import get_media, save_photo_with_descr,  \
    get_media_divecs, done_save_devices_photos
from src.bot.constants.constants import ADD_MEDIA_HELP_TEXT
from src.bot.constants.keyboard_text import AdminButtons as kb
from src.bot.database.images.image_crud import Images
from src.bot.keayboards.inline_buttons import (
    TEST_USER_CHOICES,
    MEDIA_TYPES
)
from src.bot.keayboards.main_menu import main_menu_buttons
from src.bot.loader import dp, bot
from src.bot.states.add_media import AddMedia, AddMediaShema
from src.bot.states.order_state import AVAIBLE_MEDIA_MESSAGES


async def start_adding_mediamessage(
        bot_type: Message | CallbackQuery) -> None:
    messageor_query = isinstance(bot_type, Message)
    replyer = bot_type.answer if messageor_query else bot_type.message.answer
    await replyer(
        ADD_MEDIA_HELP_TEXT,
        reply_markup=ReplyKeyboardRemove()
    )
    await replyer(
        'Загрузим медисообщение?',
        reply_markup=TEST_USER_CHOICES
    )
    await AddMedia.ready_to_start.set()


@dp.message_handler(Text(equals=kb.ADD_MEDIA))
async def start_user_test(message: Message):
    await start_adding_mediamessage(message)


@dp.callback_query_handler(text=['1', '0'], state=AddMedia.ready_to_start)
async def add_media_type_message(call: CallbackQuery, state: FSMContext):
    await state.update_data(ready_to_start=call.data)
    data = await state.get_data()
    if not int(data.get('ready_to_start')):
        await call.message.reply(
            text='текст',
            reply_markup=main_menu_buttons
        )
        await state.finish()
        return
    else:
        await call.message.reply(
            'Выбрать тип медисообщения',
            reply_markup=MEDIA_TYPES
        )
        await AddMedia.media_type.set()


@dp.callback_query_handler(
    text=AVAIBLE_MEDIA_MESSAGES,
    state=AddMedia.media_type
)
async def add_image(call: CallbackQuery, state: FSMContext):
    await state.update_data(media_type=call.data)
    await call.message.reply('Отправь описание. Описания может не быть.')
    await AddMedia.description.set()


@dp.message_handler(state=AddMedia.description)
async def add_descr(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply('Отправь фотографию')
    await AddMedia.media_file.set()


@dp.message_handler(state=AddMedia.media_file, content_types=ContentType.PHOTO)
async def dd_photo_and_get_results(message: Message, state: FSMContext):
    medai_file = {
        'photo_id': message.photo[-1].file_id,
        'file_unique_id': message.photo[-1].file_unique_id
    }
    async with state.proxy() as data:
        data['medai_file'] = medai_file
    data = await state.get_data()
    Images.add_photo_in_db(AddMediaShema(**data))
    mes = 'Закончили'
    await message.answer(mes, reply_markup=main_menu_buttons)
    await state.finish()


# Загрузка фотографий готовой работы из базы данных.
@dp.message_handler(Text(equals=kb.LOAD_WORK))
async def load_done_images(message: Message):
    for i, name in get_media():
        photo = InputFile(i)
        res = await bot.send_photo(chat_id=message.chat.id, photo=photo)
        medai_file = {
            'photo_id': res.photo[-1].file_id,
            'file_unique_id': res.photo[-1].file_unique_id,
            'name': name.split('.')[0]
        }
        save_photo_with_descr(medai_file)


@dp.message_handler(Text(equals=kb.LOAD_DEVICES))
async def load_done_images(message: Message):
    for i, name in get_media_divecs():
        photo = InputFile(i)
        res = await bot.send_photo(chat_id=message.chat.id, photo=photo)
        medai_file = {
            'photo_id': res.photo[-1].file_id,
            'file_unique_id': res.photo[-1].file_unique_id,
            'name': name.split('.')[0]
        }
        done_save_devices_photos(medai_file)
