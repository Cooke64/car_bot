import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from src.bot.config import settings
from src.bot.database.images.image_crud import Images
from src.bot.database.images.image_model import DeviceImages, DoneJobImages
from src.bot.states.order_state import MediaMesTypes

items_callback = CallbackData("PhotoItems", "page")
MEDIA = list[DeviceImages | DoneJobImages]


def get_photo_items(medi_type: str):
    try:
        if medi_type == MediaMesTypes.devices.value:
            items_from_bd: MEDIA = Images.get_all_devices_images()
        else:
            items_from_bd: MEDIA = Images.get_done_job_images()

        photos = [
            {
                'slug': item.file_unique_id,
                'image_url': item.photo_id,
                'description': item.description
            } for item in
            items_from_bd
        ]
        return photos
    except (KeyError, ValueError) as e:
        logging.error(e)
        pass


def get_photo_callback_keyboard(
        len_items: int,
        page: int = 0,
        user_id: int | None = None,
        file_path: str | None = None
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    has_next_page = len_items > page + 1
    if page != 0:
        keyboard.add(
            InlineKeyboardButton(
                text='< Назад',
                callback_data=items_callback.new(page=page - 1)
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=f'{page + 1}',
            callback_data='dont_click_me'
        )
    )
    if str(user_id) in settings.admins_id_list:
        keyboard.add(
            InlineKeyboardButton(
                text=f'remove_photo {page + 1}',
                callback_data=f'remove_photo {file_path}'
            )
        )
    if has_next_page:
        keyboard.add(
            InlineKeyboardButton(
                text='Вперёд >',
                callback_data=items_callback.new(page=page + 1)
            )
        )
    return keyboard
