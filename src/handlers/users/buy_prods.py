import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from src.database.devices.device_crud import DeviceCr
from src.database.images.image_crud import Images
from src.handlers.users.order_job import get_next_month
from src.handlers.users.utils.inform_admins import notify_admins
from src.handlers.users.utils.message_deleter import deleter
from src.handlers.users.utils.user_order_service import \
    validate_phone_number
from src.keayboards.inline_buttons import (
    TEST_USER_CHOICES, get_time_inline_kb
)
from src.keayboards.main_menu import get_kb
from src.keayboards.state_buttons import get_order_state_buttons
from src.loader import dp, bot
from src.services.tg_calendar import CalendarMarkup
from src.states.buy_prod import BuyProd, BuyProdSchema


@dp.callback_query_handler(lambda call: call.data.startswith('buy'))
async def buy_prods_start(call: CallbackQuery, state: FSMContext):
    await deleter(call, 2)
    image = Images.get_photo(call.data.split()[1])
    if image:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=image.photo_id,
            caption=f'<b>{image.description}</b>',
            reply_markup=get_order_state_buttons()

        )
        await call.message.answer(
            'Хотите приобрести данный товар?',
            reply_markup=TEST_USER_CHOICES
        )
        await BuyProd.is_correct_item.set()
        await state.set_data(data={'device_name': image.device.name})


@dp.callback_query_handler(text=['1', '0'], state=BuyProd.is_correct_item)
async def is_this_item_buy(call: CallbackQuery, state: FSMContext):
    await deleter(call, 2)
    if not int(call.data):
        await call.message.answer(
            'Вы вернулись на главную.',
            reply_markup=get_kb(call.message.from_user.id)
        )
        await state.finish()
        return
    else:
        await call.message.answer(
            'Вам необходима доставка?',
            reply_markup=TEST_USER_CHOICES)
        await BuyProd.need_delivery.set()


@dp.callback_query_handler(text=['1', '0'], state=BuyProd.need_delivery)
async def need_delivery(call: CallbackQuery, state: FSMContext):
    await deleter(call)
    await state.update_data(need_delivery=int(call.data))
    if not int(call.data):
        await call.message.answer('Введите ваше имя')
        await BuyProd.name.set()
    else:
        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        await call.message.answer(
            'Выберете число доставки?',
            reply_markup=CalendarMarkup(current_month, current_year).build)
        await BuyProd.date.set()


@dp.callback_query_handler(lambda call: 'back' in call.data,
                           state=BuyProd.date)
@dp.callback_query_handler(lambda call: 'next' in call.data,
                           state=BuyProd.date)
@dp.callback_query_handler(lambda call: 'date' in call.data,
                           state=BuyProd.date)
async def get_date(call: CallbackQuery, state: FSMContext):
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
    await BuyProd.time.set()


@dp.callback_query_handler(text=[f'{time}:00' for time in list(range(15, 21))],
                           state=BuyProd.time)
async def get_time(call: CallbackQuery, state: FSMContext):
    await state.update_data(time=call.data)
    await deleter(call)
    await call.message.answer('Напишите Ваше имя', )
    await BuyProd.name.set()


@dp.message_handler(state=BuyProd.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await deleter(message, 2)
    await message.answer("Укажите ваш номер телефона", )
    await BuyProd.phone_number.set()


def checked_message(order_data: BuyProdSchema) -> str:
    device = DeviceCr.get_device_by_name(order_data.device_name)
    message = f'{order_data.name}, Ваш заказ {device.name} по цене {device.price}.\n'
    if order_data.need_delivery:
        message += f'Доставка запланирована на {order_data.time} {order_data.date}.'
    return message


@dp.message_handler(state=BuyProd.phone_number)
async def get_phone_number_from_user(
        message: Message, state: FSMContext):
    if not validate_phone_number(message.text):
        await message.answer(
            'Напишите свой номер телефона в правильном порядке.')
        return
    await deleter(message, 2)
    await state.update_data(phone_number=message.text)
    order_data = await state.get_data()
    get_mes = checked_message(BuyProdSchema(**order_data))
    await message.answer(f"Проверьте ваш заказ. Все правильно?\n{get_mes}",
                         reply_markup=TEST_USER_CHOICES)
    await BuyProd.is_correct.set()


@dp.callback_query_handler(text=['1', '0'], state=BuyProd.is_correct)
async def get_result(call: CallbackQuery, state: FSMContext):
    await deleter(call)
    if not int(call.data):
        await call.message.answer(
            'Вам необходима доставка?',
            reply_markup=TEST_USER_CHOICES)
        await BuyProd.need_delivery.set()
    else:
        order_data = await state.get_data()
        await notify_admins(BuyProdSchema(**order_data))
        await call.message.answer(
            'Ваш заказаз принят. Ожидайте звонка от администратора.',
            reply_markup=get_kb(call.message.from_user.id)
        )
        await state.finish()
