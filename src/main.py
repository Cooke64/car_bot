import logging

from aiogram import executor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.bot.config import settings
from src.bot.services.set_bot_commands import set_commands

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('loger_data.log'))
logger.addHandler(logging.StreamHandler())


async def on_startup(dp_instanse):
    await set_commands(dp_instanse)
    logging.info('Работаем')


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup)
