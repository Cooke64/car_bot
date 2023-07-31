from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.constants.keyboard_text import OrderStateButtons


def get_order_state_buttons():
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=OrderStateButtons.FINISH_ORDER),
            ],
        ],
        resize_keyboard=True
    )
    return buttons
