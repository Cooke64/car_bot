from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.constants.keyboard_text import AdminButtons

admin_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(AdminButtons.ADD_MEDIA),
            KeyboardButton(AdminButtons.ADD_CAR),
            KeyboardButton(AdminButtons.DUMB_ALL_DATA),
            KeyboardButton(AdminButtons.DROP_ALL_DATA),
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
