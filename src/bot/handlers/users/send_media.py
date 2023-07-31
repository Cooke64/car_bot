from aiogram import types

from src.bot.loader import dp


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_photo_id_to_user(message: types.Message):
    await message.reply('Не стоит нам отправлять медиафайлы:)')


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def send_video_id_to_user(message: types.Message):
    await message.reply('Не стоит нам отправлять медиафайлы:)')
