import os
import pathlib

from src.constants.db_main import PHOTO_DESCR_PROD
from src.constants.media_description import DEVICES
from src.database.images.image_crud import Images
from src.states.add_media import AddMediaShema, MediaFile
from src.states.order_state import MediaMesTypes


def get_media():
    BASE_DIRECTORY = pathlib.Path(__file__).absolute().parent
    dir_ = os.listdir(f'{BASE_DIRECTORY}/media')
    for item in dir_:
        if item != 'devices':
            yield f'{BASE_DIRECTORY}\\media\\{item}', item


def get_media_divecs():
    BASE_DIRECTORY = pathlib.Path(__file__).absolute().parent
    dir_ = os.listdir(f'{BASE_DIRECTORY}/media/devices')
    for item in dir_:
        yield f'{BASE_DIRECTORY}\\media\\devices\\{item}', item


def done_save_devices_photos(media_data: dict, device_id):
    name = media_data.pop('name')
    Images.add_photo_in_db(
        AddMediaShema(
            media_type=MediaMesTypes.devices.value,
            description=DEVICES.get(name),
            medai_file=MediaFile(**media_data)),
        device_id
    )


def get_time_list():
    return [f'{time}:00' for time in list(range(15, 21))]
