# -*- coding:utf-8 -*-
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union

from tyme4py import AbstractTyme, AbstractCulture


class YearUnit(AbstractTyme, ABC):
    """年"""

    def __init__(self, year: int):
        self._year = year

    def get_year(self) -> int:
        return self._year

    def get_compare_index(self) -> int:
        """用于比较大小的索引"""
        return self._year * 10000


class MonthUnit(YearUnit, ABC):
    """月"""

    def __init__(self, year: int, month: int):
        super().__init__(year)
        self._month = month

    def get_month(self) -> int:
        return self._month

    def get_compare_index(self) -> int:
        return super().get_compare_index() + (self._month * 2 if self._month > 0 else 1 - self._month * 2) * 100


class DayUnit(MonthUnit, ABC):
    """日"""

    def __init__(self, year: int, month: int, day: int):
        super().__init__(year, month)
        self._day = day

    def get_day(self) -> int:
        return self._day

    def get_compare_index(self) -> int:
        return super().get_compare_index() + self._day


class SecondUnit(DayUnit, ABC):
    """秒"""

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

    def get_seconds_in_day(self) -> int:
        """当天秒数"""
        return self._hour * 3600 + self._minute * 60 + self._second

    def get_compare_index(self) -> int:
        return super().get_compare_index() * 86400 + self.get_seconds_in_day()

    @staticmethod
    def validate(year: int, month: int, day: int, hour: int, minute: int, second: int) -> None:
        AbstractCulture.validate_range(hour, 0, 23, 'hour')
        AbstractCulture.validate_range(minute, 0, 59, 'minute')
        AbstractCulture.validate_range(second, 0, 59, 'second')


class WeekUnit(MonthUnit, ABC):
    """周"""

    NAMES: List[str] = ['第一周', '第二周', '第三周', '第四周', '第五周', '第六周']
    """名称"""

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
        AbstractCulture.validate_range(index, 0, 5, 'week index')
        AbstractCulture.validate_range(start, 0, 6, 'week start')


class AbstractYear(YearUnit, ABC):
    """抽象年"""

    def __init__(self, year: int):
        super().__init__(year)

    def get_leap_month(self) -> int:
        """
        闰月
        :return: 闰月数字，1代表闰1月，0代表无闰月
        """
        return 0

    def get_month_count(self) -> int:
        """
        月数
        :return: 月数
        """
        return 12 if self.get_leap_month() < 1 else 13

    def get_name(self) -> str:
        return f"{self._year}年"

    @abstractmethod
    def next(self, n: int) -> Union[AbstractYear, None]:
        pass