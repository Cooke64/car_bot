from aiogram.types import BotCommand

from src.bot.constants.keyboard_text import commands as com


async def set_commands(dp):
    commands = [
        BotCommand(**item.dict()) for item in com
    ]
    await dp.bot.set_my_commands(commands)
