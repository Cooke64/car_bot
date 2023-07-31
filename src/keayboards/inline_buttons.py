from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.database.car_service.car_crud import car_crud
from src.bot.database.shemas import devices

TEST_USER_CHOICES = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='✅ Да', callback_data='1'
            ),
            InlineKeyboardButton(
                text='❌ Нет', callback_data='0'
            ),
        ],
    ],
    row_width=2,
)


def get_brands_list_kb():
    brands = car_crud.get_all_brends()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=item.name, callback_data=item.name
                ) for item in brands
            ],
        ],
        row_width=2,
    )
    return kb


def get_brand_models_kb(brand_name: str):
    models = car_crud.get_brand_models(brand_name)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=item.name, callback_data=item.name
                ) for item in models
            ],
        ],
        row_width=2,
    )
    return kb


def get_devices_list_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=item.name, callback_data=item.name
                ) for item in devices.devices
            ],
        ],
        row_width=2,
    )
    return kb


def get_contact_links():
    inline_links = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Отзывы на авито',
                    url='https://www.avito.ru/moskva/zapchasti_i_aksessuary/magnitola_chevrolet_cruze_tipa_tesla_na_android_3293449825'
                ),
                InlineKeyboardButton(
                    text='Наш инстаграмм',
                    url='https://www.avito.ru/moskva/zapchasti_i_aksessuary/magnitola_chevrolet_cruze_tipa_tesla_na_android_3293449825'
                ),
            ],
        ],
        row_width=2,
    )
    return inline_links


MEDIA_TYPES = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='#devices', callback_data='devices'
            ),
            InlineKeyboardButton(
                text='#done_job', callback_data='done_job'
            ),
        ],
    ],
    row_width=2,
)


def get_time_inline_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=item, callback_data=item
                ) for item in [f'{time}:00' for time in list(range(15, 21))]
            ],
        ],
        row_width=2,
    )
    return kb
