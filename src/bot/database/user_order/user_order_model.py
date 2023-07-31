from datetime import datetime

from sqlalchemy import Column as _, Integer, String, DateTime, Boolean, \
    ForeignKey, Text
from sqlalchemy.orm import relationship

from src.bot.database.base.base_model import BaseModel


class UserOrders(BaseModel):
    __tablename__ = 'users_orders'
    username = _(String(100), nullable=False, unique=True)
    user_id = _(String(50), nullable=False)
    created_on = _(DateTime(), default=datetime.now, nullable=False)
    user_date = _(String(200), nullable=False)
    phone = _(String(50), nullable=True)
    car_brend_id = _(Integer, ForeignKey('cars_brends.id'))
    model_id = _(Integer, ForeignKey('models.id'))
    device_id = _(Integer, ForeignKey('devices.id'))
    need_delivery = _(Boolean, default=False)
    need_install = _(Boolean, default=True)


class Order(BaseModel):
    __tablename__ = 'orders'
    username = _(String(100), nullable=False)
    phone = _(String(50), nullable=True)
    order = _(Text(), nullable=True)
    need_delivery = _(Boolean, default=False)
    need_install = _(Boolean, default=True)


