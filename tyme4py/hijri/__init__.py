# -*- coding:utf-8 -*-
from __future__ import annotations

from typing import List

from tyme4py.jd import JulianDay
from tyme4py.solar import SolarDay
from tyme4py.unit import YearUnit, MonthUnit, DayUnit


class HijriYear(YearUnit):
    """回历年"""
    def __init__(self, year):
        HijriYear.validate(year)
        super().__init__(year)

    @staticmethod
    def validate(year):
        if year < -640 or year > 9666:
            raise ValueError(f'illegal hijri year: {year}')

    @classmethod
    def from_year(cls, year):
        return cls(year)

    def get_day_count(self):
        return 355 if self.is_leap() else 354

    def is_leap(self):
        i = (self._year - 1) % 30
        return i in (1, 4, 6, 9, 12, 15, 17, 20, 23, 25, 28)

    def get_name(self):
        return f'{self._year}年'

    def next(self, n):
        return HijriYear.from_year(self._year + n)

    def get_months(self):
        months = []
        for i in range(1, 13):
            months.append(HijriMonth(self._year, i))
        return months

    def get_first_month(self):
        return HijriMonth(self._year, 1)


class HijriMonth(MonthUnit):
    NAMES: List[str] = ['穆哈兰姆月', '色法尔月', '赖比尔·敖外鲁月', '赖比尔·阿色尼月', '主马达·敖外鲁月', '主马达·阿色尼月', '赖哲卜月', '舍尔邦月', '赖买丹月', '闪瓦鲁月', '都尔喀尔德月', '都尔黑哲月']

    @staticmethod
    def validate(year, month):
        if month < 1 or month > 12:
            raise ValueError(f'illegal hijri month: {month}')
        HijriYear.validate(year)

    def __init__(self, year, month):
        HijriMonth.validate(year, month)
        super().__init__(year, month)

    @classmethod
    def from_ym(cls, year, month):
        return cls(year, month)

    def get_hijri_year(self):
        return HijriYear(self._year)

    def get_day_count(self):
        d = 29 if self._month % 2 == 0 else 30
        if self._month == 12 and self.get_hijri_year().is_leap():
            d += 1
        return d

    def get_index_in_year(self):
        return self._month - 1

    def get_name(self):
        return self.NAMES[self.get_index_in_year()]

    def __str__(self):
        return f'{self.get_hijri_year()}{self.get_name()}'

    def next(self, n):
        i: int = self._month - 1 + n
        return HijriMonth((self._year * 12 + i) // 12, self.index_of(i, 12) + 1)

    def get_days(self):
        size = self.get_day_count()
        days = []
        for i in range(1, size + 1):
            days.append(HijriDay(self._year, self._month, i))
        return days

    def get_first_day(self):
        return HijriDay(self._year, self._month, 1)


class HijriDay(DayUnit):
    NAMES: List[str] = ['1日', '2日', '3日', '4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日', '14日', '15日', '16日', '17日', '18日', '19日', '20日', '21日', '22日', '23日', '24日', '25日', '26日', '27日', '28日', '29日', '30日']

    @staticmethod
    def validate(year, month, day):
        if day < 1 or day > HijriMonth.from_ym(year, month).get_day_count():
            raise ValueError(f'illegal hijri day: {year}-{month}-{day}')

    def __init__(self, year, month, day):
        HijriDay.validate(year, month, day)
        super().__init__(year, month, day)

    @classmethod
    def from_ymd(cls, year, month, day):
        return cls(year, month, day)

    def get_hijri_month(self):
        return HijriMonth(self._year, self._month)

    def get_name(self):
        return self.NAMES[self._day - 1]

    def __str__(self):
        return f'{self.get_hijri_month()}{self.get_name()}'

    def next(self, n):
        return self.get_solar_day().next(n).get_hijri_day()

    def is_before(self, target: HijriDay):
        if self._year != target._year:
            return self._year < target._year
        if self._month != target._month:
            return self._month < target._month
        return self._day < target._day

    def is_after(self, target: HijriDay):
        if self._year != target._year:
            return self._year > target._year
        if self._month != target._month:
            return self._month > target._month
        return self._day > target._day

    def get_index_in_year(self):
        return self.subtract(HijriDay(self._year, 1, 1))

    def subtract(self, target):
        return int(self.get_julian_day().subtract(target.get_julian_day()))

    def get_julian_day(self):
        return JulianDay((11 * self._year + 3) // 30 + 354 * self._year + 30 * self._month - (self._month - 1) // 2 + self._day + 1948055)

    def get_solar_day(self):
        return SolarDay(622, 7, 16).next(self.subtract(HijriDay(1, 1, 1)))
