import datetime
import logging
from typing import Optional

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from src.constants.constants import ORDER_SERVICE_DESCRIPTION
from src.constants.keyboard_text import (
    KeyBoardText as kb
)
from src.database.car_service.car_crud import car_crud
from src.database.devices.device_crud import DeviceCr
from src.database.fake_bd import devices
from src.database.user_order.user_order_crud import UserOrder
from src.handlers.users.utils.message_deleter import deleter
from src.handlers.users.utils.user_order_service import (
    validate_phone_number,
    get_result_message
)
from src.keayboards.inline_buttons import (
    TEST_USER_CHOICES,
    get_brands_list_kb,
    get_devices_list_kb,
    get_brand_models_kb, get_time_inline_kb
)
from src.keayboards.main_menu import get_kb
from src.keayboards.state_buttons import get_order_state_buttons
from src.loader import dp, bot
from src.services.tg_calendar import CalendarMarkup
from src.states.order_state import OrderProd, UserOrderData

__BRAND_NAMES: Optional[str] = None


@dp.message_handler(Text(equals=kb.ORDER_JOB))
async def start_user_test(message: Message):
    await message.answer(ORDER_SERVICE_DESCRIPTION)
    await message.answer(
        'Хотите заказать установку мультимедиа?',
        reply_markup=TEST_USER_CHOICES
    )
    await OrderProd.ready_to_start.set()


@dp.callback_query_handler(text=['1', '0'], state=OrderProd.ready_to_start)
async def test_user_capacity(call: CallbackQuery, state: FSMContext):
    await deleter(call, 2)
    if not int(call.data):
        await call.message.answer(
            'Вы можете сделать заказ в любое для вас время.',
            reply_markup=get_kb(call.message.from_user.id)
        )
        await state.finish()
        return
    else:
        await call.message.answer(
            'Давайте выберем марку вашего автомобиля',
            reply_markup=get_order_state_buttons())
        await call.message.answer(
            'Укажите, какой у вас автомобиль?',
            reply_markup=get_brands_list_kb()
        )
        await OrderProd.car_type.set()


@dp.callback_query_handler(
    text=car_crud.brands_names,
    state=OrderProd.car_type
)
async def get_production_type(call: CallbackQuery, state: FSMContext):
    await state.update_data(car_type=call.data)
    await deleter(call, 2)
    await call.message.answer(
        "Выберете доступноую модель авто",
        reply_markup=get_brand_models_kb(call.data)
    )
    await OrderProd.model_type.set()
    data = await state.get_data()
    global __BRAND_NAMES

    __BRAND_NAMES = data.get('car_type')


@dp.callback_query_handler(
    text=car_crud.get_brand_models(__BRAND_NAMES),
    state=OrderProd.model_type
)
async def get_production_type(call: CallbackQuery, state: FSMContext):
    await state.update_data(model_type=call.data)
    await deleter(call)
    await call.message.answer(
        "Выберете продукцию для установки",
        reply_markup=get_devices_list_kb()
    )
    await OrderProd.prod_type.set()


@dp.callback_query_handler(
    lambda call: call.data in [i.get('name') for i in devices.get('devices')],
    state=OrderProd.prod_type
)
async def get_calendar(call: CallbackQuery, state: FSMContext):
    await state.update_data(prod_type=call.data)
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await deleter(call)
    await call.message.answer(
        text='Выберите удобною Вам дату',
        reply_markup=CalendarMarkup(current_month, current_year).build,
    )
    await OrderProd.date.set()


@dp.callback_query_handler(lambda call: 'back' in call.data,
                           state=OrderProd.date)
@dp.callback_query_handler(lambda call: 'next' in call.data,
                           state=OrderProd.date)
@dp.callback_query_handler(lambda call: 'date' in call.data,
                           state=OrderProd.date)
async def calendar_handler(call: CallbackQuery, state: FSMContext):
    mes = call.data
    if 'date' in mes:
        await bot.delete_message(
            call.from_user.id, call.message.message_id
        )
    elif 'back' in mes or 'next' in mes:
        await get_next_month(call)
        return

    await state.update_data(date=call.data.split()[1])
    await call.message.answer(
        'Выберете удобное для Вас время.',
        reply_markup=get_time_inline_kb()
    )
    await OrderProd.time.set()


@dp.callback_query_handler(text=[f'{time}:00' for time in list(range(15, 21))],
                           state=OrderProd.time)
async def get_time(call: CallbackQuery, state: FSMContext):
    await state.update_data(time=call.data)
    await deleter(call)
    await call.message.answer(
        "Хотите заказать выездную установку?",
        reply_markup=TEST_USER_CHOICES
    )
    await OrderProd.self_or_not.set()


async def get_next_month(call: CallbackQuery) -> None:
    month, year = map(int, call.data.split()[1].split("."))
    calendar = CalendarMarkup(month, year)
    if 'next' in call.data:
        await call.message.edit_reply_markup(
            reply_markup=calendar.next_month())
    elif 'back' in call.data:
        await call.message.edit_reply_markup(
            reply_markup=calendar.previous_month())


@dp.callback_query_handler(text=['1', '0'], state=OrderProd.self_or_not)
async def get_name(call: CallbackQuery, state: FSMContext):
    await state.update_data(self_or_not=int(call.data))
    await deleter(call)
    await call.message.answer(
        'Напишите, как к вам можем обращаться',
    )
    await OrderProd.name.set()


@dp.message_handler(state=OrderProd.name)
async def get_phone_and_accept_order(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await deleter(message, 2)
    await message.answer("Оставьте ваш номер телефона, чтобы мы могли вам перезвонить и подтвердить заказ")
    await OrderProd.phone_number.set()


@dp.message_handler(state=OrderProd.phone_number)
async def get_phone_number_from_user(
        message: types.Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer(
            'Напишите свой номер телефона в правильном порядке.')
        return
    await deleter(message, 2)
    await state.update_data(phone_number=message.text)
    order_data = await state.get_data()
    mes = get_result_message(UserOrderData(**order_data))
    await message.answer("Проверьте ваш заказ. Все правильно?")
    await message.answer(text=mes, reply_markup=TEST_USER_CHOICES)
    await OrderProd.is_correct.set()


@dp.callback_query_handler(text=['1', '0'], state=OrderProd.is_correct)
async def finish_order(call: CallbackQuery, state: FSMContext):
    await deleter(call, 2)
    order_data = await state.get_data()
    if not int(call.data):
        await call.message.answer(
            'Давайте начнем с начала!',
            reply_markup=get_order_state_buttons())
        await call.message.answer(
            'Напишите, какой у вас автомобиль?',
            reply_markup=get_brands_list_kb()
        )
        await OrderProd.car_type.set()
    else:
        order = UserOrderData(**order_data)
        UserOrder.create_user_order(order)
        await call.message.answer('Вы вернулись на главную', reply_markup=get_kb(call.message.from_user.id),)
        await call.answer(
            'Ваш заказаз принят. В ближайшее время с вами свяжется наш сотрудинк, чтобы подтвердить заказ.',
            show_alert=True
        )
        logging.info(order)
        await state.finish()
