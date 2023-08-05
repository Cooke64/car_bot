from typing import List

from pydantic import BaseModel, Field

from src.database.fake_bd import fake_bd, devices as dev_list


class ModelItem(BaseModel):
    model_name: str
    model_coef: float


class Brand(BaseModel):
    brand_name: str
    brand_coef: float
    models: List[ModelItem]


class ModelShema(BaseModel):
    brend: list[Brand]


class DeviceItem(BaseModel):
    name: str
    price: int | float
    description: str
    photo_name: str | None


class DeviceList(BaseModel):
    devices: list[DeviceItem]


class OrderShema(BaseModel):
    username: str = Field(alias="username")
    phone: str
    order: str

