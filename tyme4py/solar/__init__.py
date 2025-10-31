# -*- coding:utf-8 -*-
from __future__ import annotations

from math import floor, ceil
from typing import TYPE_CHECKING

from tyme4py import LoopTyme, AbstractCultureDay, AbstractTyme
from tyme4py.culture import Week, Constellation, PhaseDay, Phase
from tyme4py.culture.dog import DogDay, Dog
from tyme4py.culture.nine import NineDay, Nine
from tyme4py.culture.phenology import PhenologyDay, Phenology
from tyme4py.culture.plumrain import PlumRainDay, PlumRain
from tyme4py.enums import HideHeavenStemType
from tyme4py.util import ShouXingUtil
from tyme4py.jd import JulianDay
from tyme4py.festival import SolarFestival
from tyme4py.holiday import LegalHoliday

if TYPE_CHECKING:
    from tyme4py.lunar import LunarDay, LunarMonth, LunarHour
    from tyme4py.sixtycycle import HideHeavenStemDay, SixtyCycleDay, SixtyCycleHour
    from tyme4py.rabbyung import RabByungYear, RabByungDay


class SolarTerm(LoopTyme):
    """节气"""
    NAMES = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪']
    """名称"""
    _year: int
    """年"""
    _cursory_julian_day: float
    """儒略日（用于日历，只精确到日中午12:00）"""

    def __init__(self, year: int, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)
        y = year
        if isinstance(index_or_name, int):
            size = self.NAMES.__len__()
            y = (year * size + index_or_name) // size
        jd = floor((y - 2000) * 365.2422 + 180)
        # 355对应2000.12冬至，计算粗略估计值
        w = floor((jd - 355 + 183) / 365.2422) * 365.2422 + 355
        if ShouXingUtil.calc_qi(w) > jd:
            w -= 365.2422
        self._year = y
        self._cursory_julian_day = ShouXingUtil.calc_qi(w + 15.2184 * self.get_index())

    @classmethod
    def from_index(cls, year: int, index: int) -> SolarTerm:
        return cls(year, index)

    @classmethod
    def from_name(cls, year: int, name: str) -> SolarTerm:
        return cls(year, name)

    def next(self, n: int) -> SolarTerm:
        size = self.get_size()
        i = self.get_index() + n
        return SolarTerm((self._year * size + i) // size, self._index_of_by(i))

    def is_jie(self) -> bool:
        """是否节令"""
        return self._index % 2 == 1

    def is_qi(self) -> bool:
        """是否气令"""
        return self._index % 2 == 0

    def get_julian_day(self) -> JulianDay:
        """
        儒略日（精确到秒）
        :return : 儒略日
        """
        return JulianDay.from_julian_day(ShouXingUtil.qi_accurate2(self._cursory_julian_day) + JulianDay.J2000)

    def get_solar_day(self) -> SolarDay:
        """
        公历日（用于日历）
        @return: 公历日
        """
        return JulianDay.from_julian_day(self._cursory_julian_day + JulianDay.J2000).get_solar_day()

    def get_year(self) -> int:
        return self._year

    def get_cursory_julian_day(self) -> float:
        """
        儒略日（用于日历，只精确到日中午12:00）
        @return: 儒略日
        """
        return self._cursory_julian_day


class SolarTermDay(AbstractCultureDay):
    """节气第几天"""

    def __init__(self, solar_term: SolarTerm, day_index: int):
        super().__init__(solar_term, day_index)

    def get_solar_term(self) -> SolarTerm:
        """
        :return: 节气
        """
        return self.get_culture()


class SolarYear(AbstractTyme):
    """公历年"""

    _year: int

    def __init__(self, year: int):
        if year < 1 or year > 9999:
            raise ValueError(f'illegal solar year: {year}')
        self._year = year

    @classmethod
    def from_year(cls, year: int) -> SolarYear:
        return cls(year)

    def get_year(self) -> int:
        return self._year

    def get_day_count(self) -> int:
        if self._year == 1582:
            return 355
        return 366 if self.is_leap() else 365

    def is_leap(self) -> bool:
        if self._year < 1600:
            return self._year % 4 == 0
        return (self._year % 4 == 0 and self._year % 100 != 0) or (self._year % 400 == 0)

    def get_name(self) -> str:
        return f"{self._year}年"

    def next(self, n: int) -> SolarYear:
        return SolarYear.from_year(self._year + n)

    def get_months(self) -> list[SolarMonth]:
        return [SolarMonth.from_ym(self._year, month) for month in range(1, 13)]

    def get_seasons(self) -> list[SolarSeason]:
        return [SolarSeason.from_index(self._year, i) for i in range(4)]

    def get_half_years(self) -> list[SolarHalfYear]:
        return [SolarHalfYear.from_index(self._year, i) for i in range(2)]

    def get_rab_byung_year(self) -> RabByungYear:
        from tyme4py.rabbyung import RabByungYear
        return RabByungYear.from_year(self._year)


class SolarHalfYear(AbstractTyme):
    """公历半年"""
    NAMES = ['上半年', '下半年']
    _year: SolarYear
    """公历年"""
    _index: int
    """索引"""

    def __init__(self, year: int, index: int):
        if index < 0 or index > 1:
            raise ValueError(f'illegal solar half year index: {index}')
        self._year = SolarYear.from_year(year)
        self._index = index

    @classmethod
    def from_index(cls, year: int, index: int) -> SolarHalfYear:
        return cls(year, index)

    def get_solar_year(self) -> SolarYear:
        return self._year

    def get_year(self) -> int:
        return self._year.get_year()

    def get_index(self) -> int:
        return self._index

    def get_name(self) -> str:
        return self.NAMES[self._index]

    def __str__(self) -> str:
        return f'{self._year}{self.get_name()}'

    def next(self, n: int) -> SolarHalfYear:
        i = self.get_index() + n
        return SolarHalfYear.from_index((self.get_year() * 2 + i) // 2, self.index_of(i, 2))

    def get_months(self) -> list[SolarMonth]:
        y = self.get_year()
        return [SolarMonth.from_ym(y, self._index * 6 + i) for i in range(1, 7)]

    def get_seasons(self) -> list[SolarSeason]:
        y = self.get_year()
        return [SolarSeason.from_index(y, self._index * 2 + i) for i in range(2)]


class SolarSeason(AbstractTyme):
    """公历季度"""
    NAMES = ['一季度', '二季度', '三季度', '四季度']
    _year: SolarYear
    _index: int

    def __init__(self, year: int, index: int):
        if index < 0 or index > 3:
            raise ValueError(f'illegal solar season index: {index}')
        self._year = SolarYear.from_year(year)
        self._index = index

    @classmethod
    def from_index(cls, year: int, index: int) -> SolarSeason:
        return cls(year, index)

    def get_solar_year(self) -> SolarYear:
        return self._year

    def get_year(self) -> int:
        return self._year.get_year()

    def get_index(self) -> int:
        return self._index

    def get_name(self) -> str:
        return self.NAMES[self._index]

    def __str__(self) -> str:
        return f'{self._year}{self.get_name()}'

    def next(self, n: int) -> SolarSeason:
        i = self.get_index() + n
        return SolarSeason.from_index((self.get_year() * 4 + i) // 4, self.index_of(i, 4))

    def get_months(self) -> list[SolarMonth]:
        y = self.get_year()
        return [SolarMonth.from_ym(y, self._index * 3 + i) for i in range(1, 4)]


class SolarMonth(AbstractTyme):
    """公历月"""
    NAMES: [str] = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    _DAYS: [int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    """每月天数"""
    _year: SolarYear
    """公历年"""
    _month: int
    """月"""

    def __init__(self, year: int, month: int):
        """
        :param year:  年
        :param month: 月
        """
        if month < 1 or month > 12:
            raise ValueError(f'illegal solar month: {month}')
        self._year = SolarYear(year)
        self._month = month

    @classmethod
    def from_ym(cls, year: int, month: int) -> SolarMonth:
        return cls(year, month)

    def get_solar_year(self) -> SolarYear:
        """
        :return: 公历年
        """
        return self._year

    def get_year(self) -> int:
        """
        :return: 公历年数字，范围为1到9999。
        """
        return self._year.get_year()

    def get_month(self) -> int:
        """
        :return: 月份数字，范围为1到12
        """
        return self._month

    def get_day_count(self) -> int:
        """
        当月的总天数
        :return:  天数（1582年10月只有21天)
        """
        if 1582 == self.get_year() and 10 == self._month:
            return 21
        d: int = self._DAYS[self.get_index_in_year()]
        # 公历闰年2月多一天
        if 2 == self._month and self._year.is_leap():
            d += 1
        return d

    def get_index_in_year(self) -> int:
        """
        位于当年的月索引
        :return: 位于当年的索引(0-11)
        """
        return self._month - 1

    def get_season(self) -> SolarSeason:
        """
        :return: 公历季度  SolarSeason
        """
        return SolarSeason(self.get_year(), int(self.get_index_in_year() / 3))

    def get_week_count(self, start: int) -> int:
        """
        当月有几周
        :param start:起始星期，1234560分别代表星期一至星期天
        :return:周数
        """
        return ceil((self.index_of(SolarDay(self.get_year(), self._month, 1).get_week().get_index() - start,
                                   7) + self.get_day_count()) / 7)

    def get_name(self) -> str:
        return self.NAMES[self.get_index_in_year()]

    def __str__(self) -> str:
        return self._year.__str__() + self.get_name()

    def next(self, n: int) -> SolarMonth:
        i = self._month - 1 + n
        return SolarMonth.from_ym((self.get_year() * 12 + i) // 12, self.index_of(i, 12) + 1)

    def get_weeks(self, start: int) -> list[SolarWeek]:
        """
        本月的公历周列表
        :param start: 星期几作为一周的开始，1234560分别代表星期一至星期天
        :return: 周列表
        """
        l: [SolarWeek] = []
        y: int = self.get_year()
        for i in range(0, self.get_week_count(start)):
            l.append(SolarWeek(y, self._month, i, start))
        return l

    def get_days(self) -> list[SolarDay]:
        """
        本月的公历日列表
        :return: 公历日 SolarDay 的列表，从1日开始
        """
        l: [SolarDay] = []
        y: int = self.get_year()
        for i in range(1, self.get_day_count()):
            l.append(SolarDay(y, self._month, i))
        return l


class SolarWeek(AbstractTyme):
    """公历周"""
    NAMES: [str] = ['第一周', '第二周', '第三周', '第四周', '第五周', '第六周']
    _month: SolarMonth
    """公历月"""
    _index: int
    """索引，0-5"""
    _start: Week
    """起始星期"""

    def __init__(self, year: int, month: int, index: int, start: int):
        """
        :param year:  年
        :param month: 月
        :param index: 索引，0-5
        :param start: 起始星期，1234560分别代表星期一至星期天
        """
        if index < 0 or index > 5:
            raise ValueError(f'illegal solar week index: {index}')
        if start < 0 or start > 6:
            raise ValueError(f'illegal solar week start: {start}')
        m: SolarMonth = SolarMonth(year, month)
        if index >= m.get_week_count(start):
            raise ValueError(f'illegal solar week index: {index} in month: {m}')

        self._month = m
        self._index = index
        self._start = Week(start)

    @classmethod
    def from_ym(cls, year: int, month: int, index: int, start: int) -> SolarWeek:
        return cls(year, month, index, start)

    def get_solar_month(self) -> SolarMonth:
        """
        :return: 公历月
        """
        return self._month

    def get_year(self) -> int:
        """
        :return: 年
        """
        return self._month.get_year()

    def get_month(self) -> int:
        """
        :return: 月
        """
        return self._month.get_month()

    def get_index(self) -> int:
        """
        :return: 索引，0-5
        """
        return self._index

    def get_index_in_year(self) -> int:
        """
        位于当年的索引
        :return: 索引  注意：索引值是从0开始，即0代表第一周
        """
        i: int = 0
        # 本周第1天
        first_day: SolarDay = self.get_first_day()
        # 今年第1周
        w: SolarWeek = SolarWeek(self.get_year(), 1, 0, self._start.get_index())
        while not w.get_first_day() == first_day:
            w = w.next(1)
            i += 1
        return i

    def get_start(self) -> Week:
        """
        起始星期
        :return: 星期
        """
        return self._start

    def get_name(self) -> str:
        return self.NAMES[self._index]

    def __str__(self) -> str:
        return self._month.__str__() + self.get_name()

    def next(self, n: int) -> SolarWeek:
        start_index: int = self._start.get_index()
        d: int = self._index
        m: SolarMonth = self._month
        if n > 0:
            d += n
            week_count: int = m.get_week_count(start_index)
            while d >= week_count:
                d -= week_count
                m = m.next(1)
                if not SolarDay(m.get_year(), m.get_month(), 1).get_week() == self._start:
                    d += 1
                week_count = m.get_week_count(start_index)
        elif n < 0:
            d += n
            while d < 0:
                if not SolarDay(m.get_year(), m.get_month(), 1).get_week() == self._start:
                    d -= 1
                m = m.next(-1)
                d += m.get_week_count(start_index)
        return SolarWeek(m.get_year(), m.get_month(), d, start_index)

    def get_first_day(self) -> SolarDay:
        """
        本周第1天
        :return: 公历日
        """
        first_day: SolarDay = SolarDay(self.get_year(), self.get_month(), 1)
        return first_day.next(self._index * 7 - self.index_of(first_day.get_week().get_index() - self._start.get_index(), 7))

    def get_days(self) -> list[SolarDay]:
        """
        本周公历日列表
        :return: 公历日列表
        """
        l: [SolarDay] = []
        d: SolarDay = self.get_first_day()
        l.append(d)
        for i in range(1, 7):
            l.append(d.next(i))
        return l

    def __eq__(self, o: SolarWeek) -> bool:
        return o and o.get_first_day() == self.get_first_day()


class SolarDay(AbstractTyme):
    """
    公历日
    """
    NAMES: [str] = ['1日', '2日', '3日', '4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日', '14日', '15日', '16日', '17日', '18日', '19日', '20日', '21日', '22日', '23日', '24日', '25日', '26日', '27日', '28日', '29日', '30日', '31日']
    _month: SolarMonth
    """公历月"""
    _day: int
    """日"""

    def __init__(self, year: int, month: int, day: int):
        if day < 1:
            raise ValueError(f'illegal solar day: {year}-{month}-{day}')
        m: SolarMonth = SolarMonth(year, month)
        if 1582 == year and 10 == month:
            if (4 < day < 15) or day > 31:
                raise ValueError(f'illegal solar day: {year}-{month}-{day}')
        elif day > m.get_day_count():
            raise ValueError(f'illegal solar day: {year}-{month}-{day}')
        self._month = m
        self._day = day

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> SolarDay:
        return cls(year, month, day)

    def get_solar_month(self) -> SolarMonth:
        """
        :return: 公历月
        """
        return self._month

    def get_year(self) -> int:
        """
        :return: 年
        """
        return self._month.get_year()

    def get_month(self) -> int:
        """
        :return: 月
        """
        return self._month.get_month()

    def get_day(self) -> int:
        """
        :return: 日
        """
        return self._day

    def get_week(self) -> Week:
        """
        :return: 星期
        """
        return self.get_julian_day().get_week()

    def get_constellation(self) -> Constellation:
        """
        :return: 星座 Constellation
        """
        y: int = self.get_month() * 100 + self._day
        return Constellation.from_index(9 if y > 1221 or y < 120 else 10 if y < 219 else 11 if y < 321 else 0 if y < 420 else 1 if y < 521 else 2 if y < 622 else 3 if y < 723 else 4 if y < 823 else 5 if y < 923 else 6 if y < 1024 else 7 if y < 1123 else 8)

    def get_name(self) -> str:
        return self.NAMES[self._day - 1]

    def __str__(self) -> str:
        return self._month.__str__() + self.get_name()

    def next(self, n: int) -> SolarDay:
        return self.get_julian_day().next(n).get_solar_day()

    def is_before(self, target: SolarDay) -> bool:
        """
        是否在指定公历日之前
        :param target: 公历日
        :return: true/false
        """
        a_year: int = self.get_year()
        b_year: int = target.get_year()
        if a_year != b_year:
            return a_year < b_year
        a_month: int = self.get_month()
        b_month: int = target.get_month()
        return a_month < b_month if a_month != b_month else self._day < target.get_day()

    def is_after(self, target: SolarDay) -> bool:
        """
        是否在指定公历日之后
        :param target: 公历日
        :return: true/false
        """
        a_year: int = self.get_year()
        b_year: int = target.get_year()
        if a_year != b_year:
            return a_year > b_year
        a_month: int = self.get_month()
        b_month: int = target.get_month()
        return a_month > b_month if a_month != b_month else self._day > target.get_day()

    def get_term(self) -> SolarTerm:
        """
        :return: 当天所在的节气 SolarTerm
        """
        return self.get_term_day().get_solar_term()

    def get_term_day(self) -> SolarTermDay:
        """
        :return: 节气第几天
        """
        y: int = self.get_year()
        i: int = self.get_month() * 2
        if i == 24:
            y += 1
            i = 0
        term: SolarTerm = SolarTerm(y, i)
        day: SolarDay = term.get_solar_day()
        while self.is_before(day):
            term = term.next(-1)
            day = term.get_solar_day()
        return SolarTermDay(term, self.subtract(day))

    def get_solar_week(self, start: int) -> SolarWeek:
        """
        公历周
        :param start: 起始星期，1234560分别代表星期一至星期天
        :return: 公历周
        """
        y: int = self.get_year()
        m: int = self.get_month()
        return SolarWeek(y, m, ceil((self._day + SolarDay(y, m, 1).get_week().next(-start).get_index()) / 7.0) - 1, start)

    def get_phenology_day(self) -> PhenologyDay:
        """
        当天所在的七十二候
        :return: 七十二候 PhenologyDay
        """
        d: SolarTermDay = self.get_term_day()
        day_index: int = d.get_day_index()
        index: int = day_index // 5
        if index > 2:
            index = 2
        term: SolarTerm = d.get_solar_term()
        return PhenologyDay(Phenology(term.get_year(), term.get_index() * 3 + index), day_index - index * 5)

    def get_phenology(self) -> Phenology:
        """
        当天所在的候
        :return: 候 Phenology
        """
        return self.get_phenology_day().get_phenology()

    def get_dog_day(self) -> DogDay | None:
        """
        当天所在的三伏天
        :return: 三伏天 DogDay
        """
        # 夏至
        xia_zhi: SolarTerm = SolarTerm(self.get_year(), 12)
        # 第1个庚日
        start: SolarDay = xia_zhi.get_solar_day()
        # 第3个庚日，即初伏第1天
        start = start.next(start.get_lunar_day().get_sixty_cycle().get_heaven_stem().steps_to(6) + 20)
        days: int = self.subtract(start)
        # 初伏以前
        if days < 0:
            return None
        if days < 10:
            return DogDay(Dog(0), days)

        # 第4个庚日，中伏第1天
        start = start.next(10)
        days = self.subtract(start)
        if days < 10:
            return DogDay(Dog(1), days)

        # 第5个庚日，中伏第11天或末伏第1天
        start = start.next(10)
        days = self.subtract(start)
        # 立秋
        if xia_zhi.next(3).get_solar_day().is_after(start):
            if days < 10:
                return DogDay(Dog(1), days + 10)
            start = start.next(10)
            days = self.subtract(start)
        if days < 10:
            return DogDay(Dog(2), days)
        return None

    def get_plum_rain_day(self) -> PlumRainDay | None:
        """
        当天所在的梅雨天（芒种后的第1个丙日入梅，小暑后的第1个未日出梅）
        :return: 梅雨天
        """
        # 芒种
        grain_in_ear: SolarTerm = SolarTerm(self.get_year(), 11)
        start: SolarDay = grain_in_ear.get_solar_day()
        # 芒种后的第1个丙日
        start = start.next(start.get_lunar_day().get_sixty_cycle().get_heaven_stem().steps_to(2))
        # 小暑
        end: SolarDay = grain_in_ear.next(2).get_solar_day()
        # 小暑后的第1个未日
        end = end.next(end.get_lunar_day().get_sixty_cycle().get_earth_branch().steps_to(7))
        if self.is_before(start) or self.is_after(end):
            return None
        return PlumRainDay(PlumRain(1), 0) if self == end else PlumRainDay(PlumRain(0), self.subtract(start))

    def get_hide_heaven_stem_day(self) -> HideHeavenStemDay:
        """
        :return: 人元司令分野
        """
        from tyme4py.sixtycycle import HideHeavenStemDay, HideHeavenStem
        day_counts: [int] = [3, 5, 7, 9, 10, 30]
        term: SolarTerm = self.get_term()
        if term.is_qi():
            term = term.next(-1)
        day_index: int = self.subtract(term.get_solar_day())
        start_index: int = (term.get_index() - 1) * 3
        data: str = '93705542220504xx1513904541632524533533105544806564xx7573304542018584xx95'[start_index: start_index + 6]
        days: int = 0
        heaven_stem_index: int = 0
        type_index: int = 0
        while type_index < 3:
            i: int = type_index * 2
            d: str = data[i: i + 1]
            count: int = 0
            if d != 'x':
                heaven_stem_index = int(d, 10)
                count = day_counts[int(data[i + 1: i + 2], 10)]
                days += count

            if day_index <= days:
                day_index -= days - count
                break

            type_index += 1

        hide_type: HideHeavenStemType
        if type_index == 0:
            hide_type = HideHeavenStemType.RESIDUAL
        elif type_index == 1:
            hide_type = HideHeavenStemType.MIDDLE
        else:
            hide_type = HideHeavenStemType.MAIN
        return HideHeavenStemDay(HideHeavenStem(heaven_stem_index, hide_type), day_index)

    def get_nine_day(self) -> NineDay | None:
        """
        当天所在的数九天
        :return: 数九天 NineDay
        """
        year: int = self.get_year()
        start: SolarDay = SolarTerm(year + 1, 0).get_solar_day()
        if self.is_before(start):
            start = SolarTerm(year, 0).get_solar_day()

        end: SolarDay = start.next(81)
        if self.is_before(start) or (not self.is_before(end)):
            return None

        days: int = self.subtract(start)
        return NineDay(Nine(int(days / 9)), days % 9)

    def get_index_in_year(self) -> int:
        """
        位于当年的索引
        :return: 索引
        """
        return self.subtract(SolarDay(self.get_year(), 1, 1))

    def subtract(self, target: SolarDay) -> int:
        """
        公历日期相减，获得相差天数
        :param target: 公历
        :return: 两个公历日之间相差的天数
        """
        return int(self.get_julian_day().subtract(target.get_julian_day()))

    def get_julian_day(self) -> JulianDay:
        """
        公历日转儒略日
        :return: 儒略日
        """
        return JulianDay.from_ymd_hms(self.get_year(), self.get_month(), self._day, 0, 0, 0)

    def get_lunar_day(self) -> LunarDay:
        """
        :return: 农历日
        """
        from tyme4py.lunar import LunarMonth, LunarDay
        m: LunarMonth = LunarMonth.from_ym(self.get_year(), self.get_month())
        days: int = self.subtract(m.get_first_julian_day().get_solar_day())
        while days < 0:
            m = m.next(-1)
            days += m.get_day_count()
        return LunarDay(m.get_year(), m.get_month_with_leap(), days + 1)

    def get_sixty_cycle_day(self) -> SixtyCycleDay:
        from tyme4py.sixtycycle import SixtyCycleDay
        return SixtyCycleDay.from_solar_day(self)

    def get_rab_byung_day(self) -> RabByungDay:
        from tyme4py.rabbyung import RabByungDay
        return RabByungDay.from_solar_day(self)

    def get_legal_holiday(self) -> LegalHoliday | None:
        """
        法定假日，如果当天不是法定假日，返回None
        :return: 法定假日
        """
        return LegalHoliday.from_ymd(self.get_year(), self.get_month(), self._day)

    def get_festival(self) -> SolarFestival | None:
        """
        公历现代节日，如果当天不是公历现代节日，返回None
        :return: 公历现代节日
        """
        return SolarFestival.from_ymd(self.get_year(), self.get_month(), self._day)

    def get_phase_day(self) -> PhaseDay:
        """
        月相第几天
        :return: 月相第几天
        """
        month = self.get_lunar_day().get_lunar_month().next(1)
        p = Phase.from_index(month.get_year(), month.get_month_with_leap(), 0)
        d = p.get_solar_day()
        while d.is_after(self):
            p = p.next(-1)
            d = p.get_solar_day()
        return PhaseDay(p, self.subtract(d))

    def get_phase(self) -> Phase:
        """
        月相
        :return: 月相 Phase。
        """
        return self.get_phase_day().get_phase()


class SolarTime(AbstractTyme):
    """公历时刻"""
    _day: SolarDay
    """公历日"""
    _hour: int
    """时"""
    _minute: int
    """分"""
    _second: int
    """秒"""

    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        if hour < 0 or hour > 23:
            raise ValueError(f'illegal hour: {hour}')
        if minute < 0 or minute > 59:
            raise ValueError(f'illegal minute: {minute}')
        if second < 0 or second > 59:
            raise ValueError(f'illegal second: {second}')

        self._day = SolarDay(year, month, day)
        self._hour = hour
        self._minute = minute
        self._second = second

    @classmethod
    def from_ymd_hms(cls, year: int, month: int, day: int, hour: int, minute: int, second: int) -> SolarTime:
        """
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param second: 秒
        :return: 公历时刻
        """
        return cls(year, month, day, hour, minute, second)

    def get_solar_day(self) -> SolarDay:
        """
        :return: 公历日
        """
        return self._day

    def get_year(self) -> int:
        """
        :return: 年
        """
        return self._day.get_year()

    def get_month(self) -> int:
        """
        :return: 月
        """
        return self._day.get_month()

    def get_day(self) -> int:
        """
        :return: 日
        """
        return self._day.get_day()

    def get_hour(self) -> int:
        """
        :return: 时
        """
        return self._hour

    def get_minute(self) -> int:
        """
        :return: 分
        """
        return self._minute

    def get_second(self) -> int:
        """
        :return: 秒
        """
        return self._second

    def get_name(self) -> str:
        return f'{self._hour:02d}:{self._minute:02d}:{self._second:02d}'

    def __str__(self) -> str:
        return f'{self._day} {self.get_name()}'

    def next(self, n: int) -> SolarTime:
        """
        推移
        :param n: 推移秒数
        :return:  公历时刻
        """
        if n == 0:
            return SolarTime(self.get_year(), self.get_month(), self.get_day(), self._hour, self._minute, self._second)
        ts: int = self._second + n
        tm: int = self._minute + floor(ts / 60)
        ts %= 60
        if ts < 0:
            ts += 60
            tm -= 1
        th: int = self._hour + int(tm / 60)
        tm %= 60
        if tm < 0:
            tm += 60
            th -= 1
        td: int = int(th / 24)
        th %= 24
        if th < 0:
            th += 24
            td -= 1
        d: SolarDay = self._day.next(td)
        return SolarTime(d.get_year(), d.get_month(), d.get_day(), th, tm, ts)

    def is_before(self, target: SolarTime) -> bool:
        """
        是否在指定公历时刻之前
        :param target: 公历时刻
        :return: true/false
        """
        if not self._day == target.get_solar_day():
            return self._day.is_before(target.get_solar_day())
        if self._hour != target.get_hour():
            return self._hour < target.get_hour()
        return self._minute < target.get_minute() if self._minute != target.get_minute() else self._second < target.get_second()

    def is_after(self, target: SolarTime) -> bool:
        """
        是否在指定公历时刻之后
        :param target: 公历时刻
        :return: true/false
        """
        if not self._day == target.get_solar_day():
            return self._day.is_after(target.get_solar_day())
        if self._hour != target.get_hour():
            return self._hour > target.get_hour()
        return self._minute > target.get_minute() if self._minute != target.get_minute() else self._second > target.get_second()

    def get_term(self) -> SolarTerm:
        """
        当时所在的节气
        :return: 节气 SolarTerm
        """
        term: SolarTerm = self.get_solar_day().get_term()
        if self.is_before(term.get_julian_day().get_solar_time()):
            term = term.next(-1)
        return term

    def get_phenology(self) -> Phenology:
        """
        当时所在的候
        :return: 候 Phenology
        """
        p: Phenology = self.get_solar_day().get_phenology()
        if self.is_before(p.get_julian_day().get_solar_time()):
            p = p.next(-1)
        return p

    def get_julian_day(self) -> JulianDay:
        """
        公历时刻转儒略日
        :return: 儒略日
        """
        return JulianDay.from_ymd_hms(self._day.get_year(), self._day.get_month(), self._day.get_day(), self._hour, self._minute, self._second)

    def subtract(self, target: SolarTime) -> int:
        """
        公历时刻相减，获得相差秒数
        :param target: 公历时刻
        :return: 秒数
        """
        days: int = self._day.subtract(target.get_solar_day())
        cs: int = self._hour * 3600 + self._minute * 60 + self._second
        ts: int = target.get_hour() * 3600 + target.get_minute() * 60 + target.get_second()
        seconds: int = cs - ts
        if seconds < 0:
            seconds += 86400
            days -= 1
        seconds += days * 86400
        return seconds

    def get_lunar_hour(self) -> LunarHour:
        """
        农历时辰
        :return: 农历时辰
        """
        from tyme4py.lunar import LunarDay, LunarHour
        d: LunarDay = self._day.get_lunar_day()
        return LunarHour(d.get_year(), d.get_month(), d.get_day(), self._hour, self._minute, self._second)

    def get_sixty_cycle_hour(self) -> SixtyCycleHour:
        """
        干支时辰
        :return: 干支时辰
        """
        from tyme4py.sixtycycle import SixtyCycleHour
        return SixtyCycleHour.from_solar_time(self)

    def get_phase(self) -> Phase:
        """
        月相
        :return: 月相 Phase。
        """
        month = self.get_lunar_hour().get_lunar_day().get_lunar_month().next(1)
        p = Phase.from_index(month.get_year(), month.get_month_with_leap(), 0)
        while p.get_solar_time().is_after(self):
            p = p.next(-1)
        return p
