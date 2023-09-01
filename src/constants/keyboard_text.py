from pydantic import BaseModel


class KeyBoardText:
    ABOUT_US = 'Информация о нас'
    PROD = '🚗 Наша продукция'
    WHAT_WE_CAN = '👷‍ Наши услуги'
    ORDER_JOB = '🛠️ Заказать установку'
    DONE_JOB = '🎞️ Готовые работы'
    QUESTIONS = '❓ Популярные вопросы'
    BACK_TO_MAIN = '◀ Вернуться в главное меню.'
    ADMIN_KB = 'Админ панель'
    CONTACT_US = '📞 Связаться с нами'


class AdminButtons:
    ADD_MEDIA = 'Добавить фото с описанием'
    ADD_CAR = 'Добавить авто'
    ORDERS = 'Заказы'
    BACK_TO_MAIN = '◀ Вернуться в главное меню.'
    DUMB_ALL_DATA = 'Загрузить все данные'
    DROP_ALL_DATA = 'Удалить все данные'


class OrderStateButtons:
    FINISH_ORDER = 'Завершить заказ'
    BACK_ONE_STEP = 'Назад'


class Command(BaseModel):
    command: str
    description: str


commands = [
    Command(command='/start', description='Запускает работу бота'),
    Command(command='/cancel',
            description='Отменить текущее действие'),
    Command(command='/help', description='Основные команды бота'),
    Command(command='/contact_us', description='Связаться с нами'),
]
