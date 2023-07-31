from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from src.bot.constants.keyboard_text import AdminButtons as kb
from src.bot.database.car_service.car_crud import car_crud
from src.bot.database.car_service.car_service_model import BrendModelShema
from src.bot.keayboards.main_menu import get_kb
from src.bot.keayboards.state_buttons import get_order_state_buttons
from src.bot.loader import dp
from src.bot.states.add_prod_info import AddCarBrendModels


def check_and_get_coef(coef: str) -> float:
    if ',' in coef:
        coef = '.'.join(coef.split(','))
    if 0.5 < float(coef) < 2:
        return float(coef)


@dp.message_handler(Text(equals=kb.ADD_CAR))
async def start_user_test(message: Message):
    await message.answer(
        'Введи марку автомобиля',
        reply_markup=get_order_state_buttons()
    )
    await AddCarBrendModels.brend_name.set()


def check_brand(brend_name):
    return car_crud.get_brand_by_name(brend_name)


@dp.message_handler(state=AddCarBrendModels.brend_name)
async def has_crime(message: Message, state: FSMContext):
    await state.update_data(brend_name=message.text)
    if check_brand(message.text):
        await message.answer("Такой автомобиль уже есть\nВведи марку авто")
        await AddCarBrendModels.model_name.set()
    else:
        await message.answer("Введи коэфицент марки авто от 0.5 до 2.0")
        await AddCarBrendModels.brend_coef.set()


@dp.message_handler(state=AddCarBrendModels.brend_coef)
async def has_crime(message: Message, state: FSMContext):
    coef = check_and_get_coef(message.text)
    if not coef:
        await message.answer(
            'Коэфицент должен быть в пределах от 0.5 до 2.0',
        )
        return
    await state.update_data(brend_coef=coef)
    await message.answer("Введи марку авто")
    await AddCarBrendModels.model_name.set()


def check_model(model_name):
    return car_crud.get_model_by_name(model_name)


@dp.message_handler(state=AddCarBrendModels.model_name)
async def has_crime(message: Message, state: FSMContext):
    if not check_model(model_name=message.text):
        await state.update_data(model_name=message.text)
        await message.answer("Введи коэфицент новой марки от 0.5 до 2.0")
        await AddCarBrendModels.model_coef.set()
    else:
        order_data = await state.get_data()
        car_crud.create_auto(order_data)
        await message.answer(
            'Такая модель уже есть. Добавлена новый автомобильный бренд',
            reply_markup=get_kb(message.from_user.id)
        )
        await state.finish()


@dp.message_handler(state=AddCarBrendModels.model_coef)
async def has_crime(message: Message, state: FSMContext):
    coef = check_and_get_coef(message.text)
    if not coef:
        await message.answer(
            'Коэфицент должен быть в пределах от 0.5 до 2.0',
        )
        return
    await state.update_data(model_coef=coef)
    order_data = await state.get_data()
    car_crud.create_auto(BrendModelShema(**order_data))
    await message.answer(
        'Добавлено новое',
        reply_markup=get_kb(message.from_user.id)
    )
    await state.finish()
