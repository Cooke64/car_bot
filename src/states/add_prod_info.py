from enum import Enum

from aiogram.dispatcher.filters.state import StatesGroup, State
from pydantic import BaseModel


class AddCarBrendModels(StatesGroup):
    brend_name = State()
    brend_coef = State()
    model_name = State()
    model_coef = State()
