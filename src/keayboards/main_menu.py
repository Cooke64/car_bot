from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import settings
from src.constants.keyboard_text import KeyBoardText

main_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KeyBoardText.PROD),
            KeyboardButton(text=KeyBoardText.ABOUT_US),
        ],
        [
            KeyboardButton(text=KeyBoardText.WHAT_WE_CAN),
            KeyboardButton(text=KeyBoardText.DONE_JOB),
        ],
        [
            KeyboardButton(text=KeyBoardText.ORDER_JOB),
        ],
    ],
    resize_keyboard=True
)
admins = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KeyBoardText.PROD),
            KeyboardButton(text=KeyBoardText.ABOUT_US),
        ],
        [
            KeyboardButton(text=KeyBoardText.WHAT_WE_CAN),
            KeyboardButton(text=KeyBoardText.DONE_JOB),
        ],
        [
            KeyboardButton(text=KeyBoardText.ORDER_JOB),
            KeyboardButton(text=KeyBoardText.ADMIN_KB)
        ],
    ],
    resize_keyboard=True
)


def get_kb(user_id: int):
    if user_id in settings.admins_id_list:
        return admins
    return main_menu_buttons
