from aiogram.dispatcher.filters.state import StatesGroup, State
from pydantic import BaseModel


class AddMedia(StatesGroup):
    ready_to_start = State()
    media_type = State()
    media_file = State()
    description = State()


class MediaFile(BaseModel):
    photo_id: str
    file_unique_id: str


class AddMediaShema(BaseModel):
    media_type: str
    description: str | None
    medai_file: MediaFile
