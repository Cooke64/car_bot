import datetime
from calendar import monthrange
from itertools import zip_longest
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


month_by_number = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

DAY_NAMES = [
    "Пн",
    "Вт",
    "Ср",
    "Чт",
    "Пт",
    "Сб",
    "Вс",
]


class Markup:
    """Класс для создания и сборки клавиатуры календаря."""

    def __init__(
        self,
        title: str,
        days_header: List[InlineKeyboardButton],
        day_list: List[InlineKeyboardButton],
        nav_buttons: List[InlineKeyboardButton],
    ) -> None:
        """Инициализация всех значений."""
        self.keyboard = InlineKeyboardMarkup()
        self.title = title
        self.days_header = days_header
        self.days = day_list
        self.nav_buttons = nav_buttons

    @property
    def kb(self) -> InlineKeyboardMarkup:
        self.keyboard.add(self.title).row(*self.days_header)
        rows_with_days_numbers = list(zip_longest(*[iter(self.days)] * 7))
        for row in rows_with_days_numbers:
            self.keyboard.row(*row)
        self.keyboard.row(*self.nav_buttons)
        return self.keyboard


class CalendarMarkup:
    """Класс для создания календаря."""

    def __init__(self, month: int, year: int) -> None:
        """Инициализация всех значений."""
        self.month = month
        self.year = year

    def next_month(self) -> InlineKeyboardMarkup:
        """Получение данных на следующий месяц."""
        current_month = datetime.date(self.year, self.month, 5)
        current_days_count = monthrange(self.year, self.month)[1]
        next_date = current_month + datetime.timedelta(days=current_days_count)
        return CalendarMarkup(next_date.month, next_date.year).build

    def previous_month(self) -> InlineKeyboardMarkup:
        """Получение данных на предыдущий месяц."""
        current_month = datetime.date(self.year, self.month, 5)
        current_days_count = monthrange(self.year, self.month)[1]
        next_date = current_month - datetime.timedelta(days=current_days_count)
        return CalendarMarkup(next_date.month, next_date.year).build

    def title(self) -> InlineKeyboardButton:
        """Создание заголовка календаря."""
        return InlineKeyboardButton(
            text=f"{month_by_number[self.month]} {self.year}",
            callback_data="None",
        )

    @staticmethod
    def days_header() -> List[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(text=day, callback_data="None")
            for day in DAY_NAMES
        ]

    def get_days(self, days_count) -> int:
        is_current_month = self.month == datetime.datetime.now().month
        print(self.month == datetime.datetime.now().month)
        return datetime.datetime.now().day if is_current_month else 1

    def days(self) -> List[InlineKeyboardButton]:
        """Метод для заполнения календаря днями месяца."""
        start_day, days_count = monthrange(self.year, self.month)
        week_days = [
            InlineKeyboardButton(text=" ", callback_data="None")
        ] * start_day
        for i in range(self.get_days(days_count), days_count + 1):
            week_days.append(
                InlineKeyboardButton(
                    text=str(i),
                    callback_data=f"date {i}.{self.month}.{self.year}",
                )
            )
        if len(week_days) % 7 != 0:
            week_days += [
                InlineKeyboardButton(text=" ", callback_data="None")
            ] * (7 - len(week_days) % 7)
        return week_days

    def nav_buttons(self) -> List[InlineKeyboardButton]:
        """Добавление кнопок для перемещения по календарю."""
        return [
            InlineKeyboardButton(
                text="<", callback_data=f"back {self.month}.{self.year}"
            ),
            InlineKeyboardButton(
                text=">", callback_data=f"next {self.month}.{self.year}"
            ),
        ]

    @property
    def build(self) -> InlineKeyboardMarkup:
        """Передача данных для сборки клавиатуры."""
        return Markup(
            self.title(),
            self.days_header(),
            self.days(),
            self.nav_buttons(),
        ).kb
