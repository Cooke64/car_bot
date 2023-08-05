from aiogram.types import Message

from src.loader import dp


@dp.message_handler()
async def get_error_message(message: Message):
    await message.answer(
        f'Пожалуйста, следуйте инструкции.\n'
        f'Я пока еще не настолько крут, как Chat GPT\n'
        f'Если чего-то не понял, нажми /help',
    )