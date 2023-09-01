from src.database.car_service.car_crud import car_crud
from src.database.car_service.car_service_model import CarBrend, Model
from src.database.devices.device_model import Device
from src.database.images.image_model import DeviceImages, DoneJobImages
from src.database.user_order.user_order_model import UserOrders, Order

models = [CarBrend, Model, Device,
          DeviceImages, DoneJobImages,
          UserOrders,
          Order]


async def drop_all() -> None:
    for item in models:
        car_crud.drop_table(item)
        print(item)
    return
