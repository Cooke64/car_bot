from enum import Enum

from aiogram.dispatcher.filters.state import StatesGroup, State
from pydantic import BaseModel, Field


class OrderProd(StatesGroup):
    ready_to_start = State()
    car_type = State()
    model_type = State()
    prod_type = State()
    date = State()
    time = State()
    self_or_not = State()
    # Самостоятельная доставка или установка
    name = State()
    phone_number = State()
    is_correct = State()


class UserOrderData(BaseModel):
    car_type: str
    prod_type: str
    model_type: str | None
    date: str
    self_or_not: str | int
    name: str
    phone_number: str
    time: str


class MediaMesTypes(Enum):
    devices = 'devices'
    done_job = 'done_job'


AVAIBLE_MEDIA_MESSAGES = [item.value for item in MediaMesTypes]
