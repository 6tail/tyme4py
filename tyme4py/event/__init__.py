# -*- coding:utf-8 -*-
from __future__ import annotations

import re
from typing import Union, List, TYPE_CHECKING

from tyme4py import AbstractCulture
from tyme4py.enums import EventType

if TYPE_CHECKING:
    from tyme4py.solar import SolarMonth, SolarDay, SolarTerm
    from tyme4py.lunar import LunarMonth, LunarDay


class Event(AbstractCulture):
    """事件"""

    def __init__(self, name: str, data: str):
        Event.validate(data)
        self._name = name
        self._data = data

    @staticmethod
    def validate(data: str) -> None:
        if len(data) != 9:
            raise ValueError(f'illegal event data: {data}')

    @staticmethod
    def builder() -> EventBuilder:
        """构造器"""
        return EventBuilder()

    @classmethod
    def from_name(cls, name: str) -> Union[Event, None]:
        pattern: re.Pattern[str] = re.compile(f'{EventManager.REGEX}{name}')
        matcher: Union[re.Match[str], None] = pattern.search(EventManager.DATA)
        return cls(name, matcher.group(1)) if matcher else None

    def _get_char_index(self, index: int) -> int:
        return EventManager.CHARS.index(self._data[index])

    def get_value(self, index: int) -> int:
        return self._get_char_index(index) - 31

    def get_month(self, year: int) -> List[int]:
        y: int = year
        m: int = self.get_value(2)
        if m > 12:
            m = 1
            y += 1
        return [y, m]

    def get_type(self) -> EventType:
        """事件类型"""
        n: int = self._get_char_index(1)
        if n == 1:
            return EventType.SOLAR_WEEK
        if n == 2:
            return EventType.LUNAR_DAY
        if n == 3:
            return EventType.TERM_DAY
        if n == 4:
            return EventType.TERM_HS
        if n == 5:
            return EventType.TERM_EB
        return EventType.SOLAR_DAY

    def get_name(self) -> str:
        """名称"""
        return self._name

    def get_data(self) -> str:
        """数据"""
        return self._data

    def get_start_year(self) -> int:
        """起始年"""
        n: int = 0
        size: int = len(EventManager.CHARS)
        for i in range(0, 3):
            n = n * size + self._get_char_index(6 + i)
        return n

    def get_solar_day(self, year: int) -> Union[SolarDay, None]:
        if year < self.get_start_year():
            return None
        t: EventType = self.get_type()
        d: Union[SolarDay, None] = None
        if t == EventType.SOLAR_DAY:
            d = self._get_solar_day_by_solar_day(year)
        elif t == EventType.SOLAR_WEEK:
            d = self._get_solar_day_by_week(year)
        elif t == EventType.LUNAR_DAY:
            d = self._get_solar_day_by_lunar_day(year)
        elif t == EventType.TERM_DAY:
            d = self._get_solar_day_by_term(year)
        elif t == EventType.TERM_HS:
            d = self._get_solar_day_by_term_heaven_stem(year)
        elif t == EventType.TERM_EB:
            d = self._get_solar_day_by_term_earth_branch(year)
        if d is None:
            return None
        offset: int = self.get_value(5)
        return d if 0 == offset else d.next(offset)

    def _get_solar_day_by_solar_day(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.solar import SolarMonth, SolarDay
        month: List[int] = self.get_month(year)
        y: int = month[0]
        m: int = month[1]
        d: int = self.get_value(3)
        delay: int = self.get_value(4)
        last_day: int = SolarMonth.from_ym(y, m).get_day_count()
        if d > last_day:
            if 0 == delay:
                return None
            elif delay < 0:
                return SolarDay.from_ymd(y, m, d + delay)
            return SolarDay.from_ymd(y, m, last_day).next(delay)
        return SolarDay.from_ymd(y, m, d)

    def _get_solar_day_by_lunar_day(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.lunar import LunarMonth, LunarDay
        month: List[int] = self.get_month(year)
        y: int = month[0]
        m: int = month[1]
        d: int = self.get_value(3)
        delay: int = self.get_value(4)
        last_day: int = LunarMonth.from_ym(y, m).get_day_count()
        if d > last_day:
            if 0 == delay:
                return None
            elif delay < 0:
                return LunarDay.from_ymd(y, m, d + delay).get_solar_day()
            return LunarDay.from_ymd(y, m, last_day).get_solar_day().next(delay)
        return LunarDay.from_ymd(y, m, d).get_solar_day()

    def _get_solar_day_by_week(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.solar import SolarMonth, SolarDay
        # 第几个星期
        n: int = self.get_value(3)
        if n == 0:
            return None
        m: SolarMonth = SolarMonth.from_ym(year, self.get_value(2))
        # 星期几
        w: int = self.get_value(4)
        if n > 0:
            # 当月第1天
            d: SolarDay = m.get_first_day()
            # 往后找第几个星期几
            return d.next(d.get_week().steps_to(w) + 7 * n - 7)

        # 当月最后一天
        d: SolarDay = SolarDay.from_ymd(year, m.get_month(), m.get_day_count())
        # 往前找第几个星期几
        return d.next(d.get_week().steps_back_to(w) + 7 * n + 7)

    def _get_solar_day_by_term(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.solar import SolarTerm, SolarDay
        d: SolarDay = SolarTerm.from_index(year, self.get_value(2)).get_solar_day()
        offset: int = self.get_value(4)
        return d if 0 == offset else d.next(offset)

    def _get_solar_day_by_term_heaven_stem(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.solar import SolarDay
        d: SolarDay = self._get_solar_day_by_term(year)
        return d.next(d.get_lunar_day().get_sixty_cycle().get_heaven_stem().steps_to(self.get_value(3)))

    def _get_solar_day_by_term_earth_branch(self, year: int) -> Union[SolarDay, None]:
        from tyme4py.solar import SolarDay
        d: SolarDay = self._get_solar_day_by_term(year)
        return d.next(d.get_lunar_day().get_sixty_cycle().get_earth_branch().steps_to(self.get_value(3)))

    @classmethod
    def from_solar_day(cls, d: SolarDay) -> List[Event]:
        """
        指定公历日的事件列表
        :param d: 公历日
        """
        l: List[Event] = []
        for e in cls.all():
            if d == e.get_solar_day(d.get_year()):
                l.append(e)
        return l

    @classmethod
    def all(cls) -> List[Event]:
        l: List[Event] = []
        pattern: re.Pattern[str] = re.compile(f'{EventManager.REGEX}(.[^@]+)')
        matcher: Union[re.Match[str], None] = pattern.search(EventManager.DATA)
        while matcher:
            l.append(cls(matcher.group(2), matcher.group(1)))
            matcher = pattern.search(EventManager.DATA, matcher.end())
        return l


class EventBuilder:
    """事件构造器"""

    def __init__(self):
        self._name = ''
        self._data = ['@', '_', '_', '_', '_', '_', '0', '0', '0']

    def name(self, n: str) -> EventBuilder:
        self._name = n
        return self

    @staticmethod
    def _get_char(index: int) -> str:
        return EventManager.CHARS[index]

    def _set_value(self, index: int, n: int) -> EventBuilder:
        self._data[index] = self._get_char(31 + n)
        return self

    @staticmethod
    def encode_type(t: EventType) -> str:
        n: int = 0
        if t == EventType.SOLAR_WEEK:
            n = 1
        elif t == EventType.LUNAR_DAY:
            n = 2
        elif t == EventType.TERM_DAY:
            n = 3
        elif t == EventType.TERM_HS:
            n = 4
        elif t == EventType.TERM_EB:
            n = 5
        return EventBuilder._get_char(n)

    def _content(self, t: EventType, a: int, b: int, c: int) -> EventBuilder:
        self._data[1] = self.encode_type(t)
        return self._set_value(2, a)._set_value(3, b)._set_value(4, c)

    def solar_day(self, solar_month: int, solar_day: int, delay_days: int) -> EventBuilder:
        """
        公历日
        :param solar_month: 公历月（1至12）
        :param solar_day: 公历日（1至31）
        :param delay_days: 顺延天数，例如生日在2月29，非闰年没有2月29，是+1天，还是-1天（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._content(EventType.SOLAR_DAY, solar_month, solar_day, delay_days)

    def lunar_day(self, lunar_month: int, lunar_day: int, delay_days: int) -> EventBuilder:
        """
        农历日
        :param lunar_month: 农历月（-12至-1，1至12，闰月为负）
        :param lunar_day: 农历日（1至30）
        :param delay_days: 顺延天数，例如生日在某月的三十，但下一年当月可能只有29天，是+1天，还是-1天（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._content(EventType.LUNAR_DAY, lunar_month, lunar_day, delay_days)

    def solar_week(self, solar_month: int, week_index: int, week: int) -> EventBuilder:
        """
        公历第几个星期几
        :param solar_month: 公历月（1至12）
        :param week_index: 第几个星期（1为第1个星期，-1为倒数第1个星期）
        :param week: 星期几（0至6，0代表星期天，1代表星期一）
        :return: 事件构造器
        """
        return self._content(EventType.SOLAR_WEEK, solar_month, week_index, week)

    def term_day(self, term_index: int, delay_days: int) -> EventBuilder:
        """
        节气
        :param term_index: 节气索引（0至23）
        :param delay_days: 顺延天数（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._content(EventType.TERM_DAY, term_index, 0, delay_days)

    def term_heaven_stem(self, term_index: int, heaven_stem_index: int, delay_days: int) -> EventBuilder:
        """
        节气天干
        :param term_index: 节气索引（0至23）
        :param heaven_stem_index: 天干索引（0至9）
        :param delay_days: 顺延天数（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._content(EventType.TERM_HS, term_index, heaven_stem_index, delay_days)

    def term_earth_branch(self, term_index: int, earth_branch_index: int, delay_days: int) -> EventBuilder:
        """
        节气地支
        :param term_index: 节气索引（0至23）
        :param earth_branch_index: 地支索引（0至11）
        :param delay_days: 顺延天数（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._content(EventType.TERM_EB, term_index, earth_branch_index, delay_days)

    def start_year(self, year: int) -> EventBuilder:
        """
        起始年
        :param year: 年
        :return: 事件构造器
        """
        size: int = len(EventManager.CHARS)
        n: int = year
        for i in range(3):
            self._data[8 - i] = self._get_char(n % size)
            n //= size
        return self

    def offset(self, days: int) -> EventBuilder:
        """
        偏移天数
        :param days: 天数（最远支持-31至31天）
        :return: 事件构造器
        """
        return self._set_value(5, days)

    def build(self) -> Event:
        """
        生成事件
        :return: 事件
        """
        return Event(self._name, ''.join(self._data))


class EventManager:
    """事件管理器"""

    CHARS: str = '0123456789ABCDEFGHIJKLMNOPQRSTU_VWXYZabcdefghijklmnopqrstuvwxyz'
    """有效字符"""
    DATA: str = ''
    """全量事件数据"""
    REGEX: str = '(@[0-9A-Za-z_]{8})'
    """数据匹配的正则表达式"""

    @classmethod
    def remove(cls, name: str) -> None:
        """
        删除事件
        :param name: 名称
        """
        cls.DATA = re.sub(rf'{cls.REGEX}{name}', '', cls.DATA)

    @classmethod
    def _save_or_update(cls, name: str, data: str) -> None:
        """
        删除事件
        :param name: 名称
        """
        pattern: re.Pattern[str] = re.compile(f'{cls.REGEX}{name}')
        matcher: Union[re.Match[str], None] = pattern.search(cls.DATA)
        if matcher:
            cls.DATA = re.sub(rf'{cls.REGEX}{name}', data, EventManager.DATA)
        else:
            cls.DATA += data

    @classmethod
    def update(cls, name: str, e: Event) -> None:
        cls._save_or_update(name, e.get_data() + name if e.get_name() is None or len(e.get_name()) < 1 else e.get_name())

    @classmethod
    def update_data(cls, name: str, data: str) -> None:
        Event.validate(data)
        cls._save_or_update(name, data)
