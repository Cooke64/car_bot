from aiogram.types import CallbackQuery, Message

from src.loader import bot


async def deleter(repl: CallbackQuery | Message, amount=1):
    chat_id = repl.from_user.id
    if isinstance(repl, CallbackQuery):
        mes_id = repl.message.message_id
    else:
        mes_id = repl.message_id
    for i in range(0, amount):
        await bot.delete_message(chat_id, mes_id - i)
