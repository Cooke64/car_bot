from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.constants.keyboard_text import AdminButtons as kb
from src.database.user_order.user_order_crud import UserOrder
from src.loader import dp


@dp.message_handler(Text(equals=kb.ORDERS))
async def start_user_test(message: Message):
    orders = UserOrder.get_orders()
    for order in orders:
        await message.answer(
            order.order
        )
