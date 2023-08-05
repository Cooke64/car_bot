import logging

from aiogram.utils.exceptions import ChatNotFound

from src.config import settings
from src.database.devices.device_crud import DeviceCr
from src.database.shemas import OrderShema
from src.database.user_order.user_order_crud import UserOrder
from src.loader import bot
from src.states.buy_prod import BuyProdSchema
from src.states.order_state import UserOrderData


def get_prod_order(order_data: BuyProdSchema) -> str:
    device = DeviceCr.get_device_by_name(order_data.device_name)
    message = f'{order_data.name} сделал заказ {order_data.device_name}'
    if order_data.need_delivery:
        message += f' доставка запланирована на {order_data.time} {order_data.date}'
    else:
        message += f' без доставки'
    return message


def get_install_order(order_data: UserOrderData) -> str:
    mes = f"""Установка для автомобиля {order_data.car_type.capitalize()} {order_data.model_type}
    Установка назначена на {order_data.date} в  {order_data.time},
    {order_data.name.capitalize()} оставил телефон для связи {order_data.phone_number} """
    return mes


def get_message(mes_data: BuyProdSchema | UserOrderData) -> str:
    mes = isinstance(mes_data, BuyProdSchema)
    return get_prod_order(mes_data) if mes else get_install_order(mes_data)


async def notify_admins(message_data: BuyProdSchema | UserOrderData):
    mes = get_message(message_data)
    data_to_save = OrderShema(
        username=message_data.name,
        phone=message_data.phone_number,
        order=mes,
    )
    for admin_id in settings.admins_id_list:
        try:
            await bot.send_message(admin_id, mes)
        except ChatNotFound:
            logging.error(
                'Пользователи не найдены или ошибочный id для админа')
    UserOrder.create_user_order(data_to_save)
    logging.info(mes)
