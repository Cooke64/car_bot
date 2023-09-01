from aiogram.types import InputFile, Message

from get_media_files import (
    get_media_divecs,
    get_media
)
from src.constants.db_main import (
    BRANDS_AND_MODELS,
    DEVICES_LIST,
    PHOTO_DESCR_PROD
)
from src.constants.media_description import DEVICES
from src.database.car_service.car_crud import car_crud
from src.database.devices.device_crud import DeviceCr
from src.database.images.image_crud import Images
from src.database.shemas import ModelShema, DeviceList
from src.loader import bot
from src.states.add_media import MediaFile, AddMediaShema
from src.states.order_state import MediaMesTypes


async def send_photo(
        file_to_save: str, name: str, chat_id: int
) -> tuple[str, MediaFile]:
    saved_image_name = name.split('.')[0]
    res = await bot.send_photo(
        chat_id=chat_id,
        photo=InputFile(file_to_save)
    )
    photo = res.photo[-1]
    medai_file = {
        'photo_id': photo.file_id,
        'file_unique_id': photo.file_unique_id,
    }
    return saved_image_name, MediaFile(**medai_file)


async def dumb_devices(message: Message):
    all_devices = DeviceList(**DEVICES_LIST).devices
    for i, name in get_media_divecs():
        saved_image_name, medai_file = await send_photo(i, name, message.chat.id)
        new_device = DeviceCr.create_new_device(
            [i for i in all_devices if i.photo_name == name.split('.')[0]]
        )
        Images.add_photo_in_db(
            AddMediaShema(
                media_type=MediaMesTypes.devices.value,
                description=DEVICES.get(saved_image_name),
                medai_file=medai_file),
            new_device.id
        )


async def dumb_done_jobs(message: Message):
    for i, name in get_media():
        saved_image_name, medai_file = await send_photo(i, name, message.chat.id)
        Images.add_photo_in_db(
            AddMediaShema(
                media_type=MediaMesTypes.done_job.value,
                description=PHOTO_DESCR_PROD.get(saved_image_name),
                medai_file=medai_file)
        )


def dumb_cars_and_models():
    for brend in ModelShema(**BRANDS_AND_MODELS).brend:
        car_crud.create_brand_models(brend)


async def dumb_data(message: Message):
    dumb_cars_and_models()
    await dumb_devices(message)
    await dumb_done_jobs(message)

dumb_cars_and_models()