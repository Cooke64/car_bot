from aiogram.dispatcher.filters.state import StatesGroup, State
from pydantic import BaseModel


class BuyProd(StatesGroup):
    is_correct_item = State()
    date = State()
    time = State()
    need_delivery = State()
    # Самостоятельная доставка или установка
    name = State()
    phone_number = State()
    is_correct = State()


class BuyProdSchema(BaseModel):
    date: str | None
    time: str | None
    need_delivery: int
    name: str
    phone_number: str
    device_name: str | None
