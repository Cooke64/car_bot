import re

from src.bot.database.car_service.car_crud import car_crud
from src.bot.database.shemas import models, devices, DeviceItem, Brand
from src.bot.states.order_state import UserOrderData


def get_cost(order_data: UserOrderData):
    try:
        brand = car_crud.get_brand_by_name(order_data.car_type)
        device: DeviceItem = [item for item in devices.devices if item.name == item.name][0]
        if brand and device:
            return brand.car_coef * device.price
        return 0
    except IndexError:
        return 0


def validate_phone_number(number: str) -> bool:
    pattern = '^((8|\+7)[\- ]?)(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    r_2 = re.compile(pattern)
    return True if r_2.search(number) else False


def get_result_message(order_data: UserOrderData):
    res = get_cost(order_data)
    mes = f"""{order_data.name.capitalize()}, для автомобиля {order_data.car_type.capitalize()} {order_data.model_type}
Ваш заказ установка {order_data.prod_type} составляет {res}
Установка назначена на {order_data.date} в  {order_data.time},
Ваш телефон для связи {order_data.phone_number}"""
    return mes
