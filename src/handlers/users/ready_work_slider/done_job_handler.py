from aiogram.dispatcher.filters import Text
from aiogram.types import (
    Message,
    CallbackQuery,
    InputMedia,
    ChatActions
)

from src.bot.constants.constants import OUR_JOB
from src.bot.constants.keyboard_text import KeyBoardText as kb
from src.bot.database.images.image_crud import Images
from src.bot.handlers.users.utils.slider_keyboard import (
    get_photo_items,
    get_photo_callback_keyboard,
    items_callback
)
from src.bot.loader import dp, bot
from src.bot.states.order_state import MediaMesTypes


@dp.message_handler(Text(equals=kb.DONE_JOB))
async def get_photo_slider(message: Message):
    items = get_photo_items(MediaMesTypes.done_job.value)
    if items:
        photo_data = items[0]
        await message.answer(OUR_JOB)
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_data.get('image_url'),
            caption=f'<b>{photo_data.get("description")}</b>',
            reply_markup=get_photo_callback_keyboard(
                len(items),
                user_id=message.from_user.id,
                file_path=photo_data.get('slug')
            )
        )
        return
    await message.answer('Фоток пока нет, но скоро будут загружены', )


@dp.callback_query_handler(items_callback.filter())
async def photo_callback_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get('page'))
    items = get_photo_items(MediaMesTypes.done_job.value)
    items_data = items[page]
    file_path = items_data.get('image_url')
    caption = f"<b>{items_data.get('description')}</b>"
    keyboard = get_photo_callback_keyboard(
        len_items=len(items),
        page=page,
        user_id=query.message.from_user.id,
        file_path=items_data.get('slug')
    )
    file = InputMedia(media=file_path, caption=caption)
    await bot.send_chat_action(query.message.chat.id, ChatActions.UPLOAD_PHOTO)
    await query.message.edit_media(file, keyboard)


@dp.callback_query_handler(
    lambda call: call.data.startswith('remove_photo'))
async def remove_photo(call: CallbackQuery):
    unique_id = call.data.split()[1]
    Images.remove_done_job(unique_id)
    await call.message.answer('Удалено')
