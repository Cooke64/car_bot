from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.constants.keyboard_text import AdminButtons

admin_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(AdminButtons.ADD_MEDIA),
            KeyboardButton(AdminButtons.ADD_CAR),
            KeyboardButton(AdminButtons.LOAD_WORK),
            KeyboardButton(AdminButtons.LOAD_DEVICES)
        ],
        [
            KeyboardButton(AdminButtons.ORDERS)
        ],
        [
            KeyboardButton(AdminButtons.BACK_TO_MAIN)
        ]
    ],
    resize_keyboard=True
)
