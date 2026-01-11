# -*- coding:utf-8 -*-
from __future__ import annotations

from abc import ABC

from tyme4py import AbstractTyme


class YearUnit(AbstractTyme, ABC):
    """年"""

    _year: int

    def __init__(self, year: int):
        self._year = year

    def get_year(self) -> int:
        return self._year


class MonthUnit(YearUnit, ABC):
    """月"""

    _month: int

    def __init__(self, year: int, month: int):
        super().__init__(year)
        self._month = month

    def get_month(self) -> int:
        return self._month


class DayUnit(MonthUnit, ABC):
    """日"""

    _day: int

    def __init__(self, year: int, month: int, day: int):
        super().__init__(year, month)
        self._day = day

    def get_day(self) -> int:
        return self._day


class SecondUnit(DayUnit, ABC):
    """秒"""

    _hour: int
    _minute: int
    _second: int

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        super().__init__(year, month, day)
        self._hour = hour
        self._minute = minute
        self._second = second

    def get_hour(self) -> int:
        return self._hour

    def get_minute(self) -> int:
        return self._minute

    def get_second(self) -> int:
        return self._second

    @staticmethod
    def validate(year: int, month: int, day: int, hour: int, minute: int, second: int) -> None:
        if hour < 0 or hour > 23:
            raise ValueError(f'illegal hour: {hour}')
        if minute < 0 or minute > 59:
            raise ValueError(f'illegal minute: {minute}')
        if second < 0 or second > 59:
            raise ValueError(f'illegal second: {second}')


class WeekUnit(MonthUnit, ABC):
    """周"""

    _index: int
    _start: int

    def __init__(self, year: int, month: int, index: int, start: int):
        super().__init__(year, month)
        self._index = index
        self._start = start

    def get_index(self) -> int:
        return self._index

    def get_start(self) -> int:
        return self._start

    @staticmethod
    def validate(year: int, month: int, index: int, start: int) -> None:
        if index < 0 or index > 5:
            raise ValueError(f'illegal week index: {index}')
        if start < 0 or start > 6:
            raise ValueError(f'illegal week start: {start}')
