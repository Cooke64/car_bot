from typing import List

from pydantic import BaseModel

from src.bot.database.fake_bd import fake_bd, devices as dev_list


class ModelItem(BaseModel):
    model_name: str
    model_coef: float


class Brand(BaseModel):
    brand_name: str
    brand_coef: float
    models: List[ModelItem]


class Model(BaseModel):
    brend: list[Brand]


class DeviceItem(BaseModel):
    name: str
    price: int | float


class DeviceList(BaseModel):
    devices: list[DeviceItem]


class OrderShema(BaseModel):
    username: str
    phone: str
    order: str


models = Model(**fake_bd)
brand_names = [model.brand_name for model in models.brend]
devices = DeviceList(**dev_list)
