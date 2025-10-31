# -*- coding:utf-8 -*-
from __future__ import annotations

from math import floor, ceil
from typing import TYPE_CHECKING

from tyme4py import LoopTyme, AbstractCulture, AbstractCultureDay, AbstractTyme
from tyme4py.culture import Element, Direction, Zodiac, Terrain, Sound, Ten, Twenty, Duty, God, Taboo
from tyme4py.culture.fetus import FetusDay
from tyme4py.culture.pengzu import PengZuEarthBranch, PengZuHeavenStem, PengZu
from tyme4py.culture.star.nine import NineStar
from tyme4py.culture.star.ten import TenStar
from tyme4py.culture.star.twelve import TwelveStar
from tyme4py.eightchar import EightChar
from tyme4py.enums import YinYang, HideHeavenStemType

if TYPE_CHECKING:
    from tyme4py.solar import SolarDay, SolarTime
    from tyme4py.culture.star.twentyeight import TwentyEightStar


class ThreePillars(AbstractCulture):
    """
    三柱
    """
    _year: SixtyCycle
    """年柱"""
    _month: SixtyCycle
    """月柱"""
    _day: SixtyCycle
    """日柱"""

    def __init__(self, year: SixtyCycle | str, month: SixtyCycle | str, day: SixtyCycle | str):
        """
        :param year: 年干支
        :param month: 月干支
        :param day: 日干支
        """
        self._year = year if isinstance(year, SixtyCycle) else SixtyCycle(year)
        self._month = month if isinstance(month, SixtyCycle) else SixtyCycle(month)
        self._day = day if isinstance(day, SixtyCycle) else SixtyCycle(day)

    def get_year(self) -> SixtyCycle:
        """
        年柱
        :return: 干支 SixtyCycle
        """
        return self._year

    def get_month(self) -> SixtyCycle:
        """
        月柱
        :return: 干支 SixtyCycle
        """
        return self._month

    def get_day(self) -> SixtyCycle:
        """
        日柱
        :return:  干支 SixtyCycle
        """
        return self._day

    def get_name(self) -> str:
        return f'{self._year} {self._month} {self._day}'

    def get_solar_days(self, start_year: int, end_year: int) -> list[SolarDay]:
        """
        三柱转公历日列表
        :param start_year: 开始年份，支持1-9999年
        :param end_year: 结束年份，支持1-9999年
        :return: 公历日 SolarDay的列表
        """
        from tyme4py.solar import SolarDay, SolarTerm
        l: [SolarDay] = []
        # 月地支距寅月的偏移值
        m: int = self._month.get_earth_branch().next(-2).get_index()
        # 月天干要一致
        if not HeavenStem((self._year.get_heaven_stem().get_index() + 1) * 2 + m) == self._month.get_heaven_stem():
            return l

        # 1年的立春是辛酉，序号57
        y: int = self._year.next(-57).get_index() + 1
        # 节令偏移值
        m *= 2
        base_year: int = start_year - 1
        if base_year > y:
            y += 60 * int(ceil((base_year - y) / 60.0))

        while y <= end_year:
            # 立春为寅月的开始
            term: SolarTerm = SolarTerm(y, 3)
            # 节令推移，年干支和月干支就都匹配上了
            if m > 0:
                term = term.next(m)

            solar_day: SolarDay = term.get_solar_day()
            if solar_day.get_year() >= start_year:
                # 日干支和节令干支的偏移值
                d: int = self._day.next(-solar_day.get_lunar_day().get_sixty_cycle().get_index()).get_index()
                if d > 0:
                    # 从节令推移天数
                    solar_day = solar_day.next(d)

                # 验证一下
                if solar_day.get_sixty_cycle_day().get_three_pillars() == self:
                    l.append(solar_day)
            y += 60
        return l


class EarthBranch(LoopTyme):
    """地支（地元）"""
    NAMES: [str] = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> EarthBranch:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> EarthBranch:
        return cls(index)

    def next(self, n: int) -> EarthBranch:
        return EarthBranch(self.next_index(n))

    def get_element(self) -> Element:
        """
        :return:五行
        """
        return Element([4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4][self.get_index()])

    def get_yin_yang(self) -> YinYang:
        """
        :return:阴阳
        """
        return YinYang.YANG if self.get_index() % 2 == 0 else YinYang.YIN

    def get_hide_heaven_stem_main(self) -> HeavenStem:
        """
        藏干之本气(主气)
        :return: 天干 HeavenStem
        """
        return HeavenStem([9, 5, 0, 1, 4, 2, 3, 5, 6, 7, 4, 8][self.get_index()])

    def get_hide_heaven_stem_middle(self) -> HeavenStem | None:
        """
        藏干之中气，无中气的返回None
        :return: 天干 HeavenStem
        """
        n: int = [-1, 9, 2, -1, 1, 6, 5, 3, 8, -1, 7, 0][self.get_index()]
        return None if n == -1 else HeavenStem(n)

    def get_hide_heaven_stem_residual(self) -> HeavenStem | None:
        """
        藏干之余气，无余气的返回None
        :return: 天干 HeavenStem
        """
        n: int = [-1, 7, 4, -1, 9, 4, -1, 1, 4, -1, 3, -1][self.get_index()]
        return None if n == -1 else HeavenStem(n)

    def get_hide_heaven_stems(self) -> list[HideHeavenStem]:
        """
        :return: 藏干列表
        """
        l: [HideHeavenStem] = [HideHeavenStem(self.get_hide_heaven_stem_main(), HideHeavenStemType.MAIN)]
        o: HeavenStem | None = self.get_hide_heaven_stem_middle()
        if o:
            l.append(HideHeavenStem(o, HideHeavenStemType.MIDDLE))
        o = self.get_hide_heaven_stem_residual()
        if o:
            l.append(HideHeavenStem(o, HideHeavenStemType.RESIDUAL))
        return l

    def get_zodiac(self) -> Zodiac:
        """
        生肖属相
        :return:生肖 Zodiac
        """
        return Zodiac(self.get_index())

    def get_direction(self) -> Direction:
        """
        :return: 方位 Direction
        """
        return Direction([0, 4, 2, 2, 4, 8, 8, 4, 6, 6, 4, 0][self.get_index()])

    def get_opposite(self) -> EarthBranch:
        """
        六冲
        子午冲，丑未冲，寅申冲，辰戌冲，卯酉冲，巳亥冲。
        :return: 地支 EarthBranch
        """
        return self.next(6)

    def get_ominous(self) -> Direction:
        """
        煞
        逢巳日、酉日、丑日必煞东；
        亥日、卯日、未日必煞西；
        申日、子日、辰日必煞南；
        寅日、午日、戌日必煞北。
        :return: 方位 Direction
        """
        return Direction([8, 2, 0, 6][self.get_index() % 4])

    def get_peng_zu_earth_branch(self) -> PengZuEarthBranch:
        """
        :return: 地支彭祖百忌 PengZuEarthBranch
        """
        return PengZuEarthBranch(self.get_index())

    def get_combine(self) -> EarthBranch:
        """
        六合（子丑合，寅亥合，卯戌合，辰酉合，巳申合，午未合）
        :return: 地支 EarthBranch
        """
        return EarthBranch(1 - self.get_index())

    def get_harm(self) -> EarthBranch:
        """
        六害（子未害、丑午害、寅巳害、卯辰害、申亥害、酉戌害）
        :return: 地支 EarthBranch
        """
        return EarthBranch(19 - self.get_index())

    def combine(self, target: EarthBranch) -> Element | None:
        """
        合化
        子丑合化土，寅亥合化木，卯戌合化火，辰酉合化金，巳申合化水，午未合化火
        :param target: 地支 EarthBranch
        :return: 能合化则返回五行属性，不能合化则返回None
        """
        return Element([2, 2, 0, 1, 3, 4, 2, 2, 4, 3, 1, 0][self.get_index()]) if self.get_combine() == target else None


class HeavenStem(LoopTyme):
    """天干（天元）"""
    NAMES: [str] = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> HeavenStem:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> HeavenStem:
        return cls(index)

    def next(self, n: int) -> HeavenStem:
        return HeavenStem(self.next_index(n))

    def get_element(self) -> Element:
        """
        五行
        :return: 五行
        """
        return Element(self.get_index() // 2)

    def get_yin_yang(self) -> YinYang:
        """
        :return: 阴阳
        """
        return YinYang.YANG if self.get_index() % 2 == 0 else YinYang.YIN

    def get_ten_star(self, target: HeavenStem) -> TenStar:
        """
        十神（生我者，正印偏印。我生者，伤官食神。克我者，正官七杀。我克者，正财偏财。同我者，劫财比肩。）
        :param target: 天干
        :return:十神
        """
        target_index: int = target.get_index()
        offset: int = target_index - self.get_index()
        if self.get_index() % 2 != 0 and target_index % 2 == 0:
            offset += 2
        return TenStar(offset)

    def get_direction(self) -> Direction:
        """
        :return: 方位
        """
        return self.get_element().get_direction()

    def get_joy_direction(self) -> Direction:
        """
        喜神方位（《喜神方位歌》甲己在艮乙庚乾，丙辛坤位喜神安。丁壬只在离宫坐，戊癸原在在巽间。）
        :return: 方位
        """
        return Direction([7, 5, 1, 8, 3][self.get_index() % 5])

    def get_yang_direction(self) -> Direction:
        """
        阳贵神方位（《阳贵神歌》甲戊坤艮位，乙己是坤坎，庚辛居离艮，丙丁兑与乾，震巽属何日，壬癸贵神安。）
        :return: 方位
        """
        return Direction([1, 1, 6, 5, 7, 0, 8, 7, 2, 3][self.get_index()])

    def get_yin_direction(self) -> Direction:
        """
        阴贵神方位（《阴贵神歌》甲戊见牛羊，乙己鼠猴乡，丙丁猪鸡位，壬癸蛇兔藏，庚辛逢虎马，此是贵神方。）
        :return: 方位
        """
        return Direction([7, 0, 5, 6, 1, 1, 7, 8, 3, 2][self.get_index()])

    def get_wealth_direction(self) -> Direction:
        """
        财神方位（《财神方位歌》甲乙东北是财神，丙丁向在西南寻，戊己正北坐方位，庚辛正东去安身，壬癸原来正南坐，便是财神方位真。）
        :return:方位
        """
        return Direction([7, 1, 0, 2, 8][self.get_index() // 2])

    def get_mascot_direction(self) -> Direction:
        """
        福神方位（《福神方位歌》甲乙东南是福神，丙丁正东是堪宜，戊北己南庚辛坤，壬在乾方癸在西。）
        :return:方位
        """
        return Direction([3, 3, 2, 2, 0, 8, 1, 1, 5, 6][self.get_index()])

    def get_peng_zu_heaven_stem(self) -> PengZuHeavenStem:
        """
        :return:天干彭祖百忌
        """
        return PengZuHeavenStem(self.get_index())

    def get_terrain(self, earth_branch: EarthBranch) -> Terrain:
        """
        长生十二神(地势)
        长生十二神可通过不同的组合，得到自坐和星运。
        :param: 地支
        :return：地势(长生十二神)
        """
        earth_branch_index: int = earth_branch.get_index()
        return Terrain([1, 6, 10, 9, 10, 9, 7, 0, 4, 3][self.get_index()] + (earth_branch_index if YinYang.YANG == self.get_yin_yang() else -earth_branch_index))

    def get_combine(self) -> HeavenStem:
        """
        天干五合（甲己合，乙庚合，丙辛合，丁壬合，戊癸合）
        :return: 天干
        """
        return self.next(5)

    def combine(self, target: HeavenStem) -> Element:
        """
        合化（甲己合化土 乙庚合化金 丙辛合化水 丁壬合化木 戊癸合化火）
        :param target: 天干
        :return: 能合化则返回五行属性，不能合化则返回null
        """
        return Element(self.get_index() + 2) if self.get_combine() == target else None


class HideHeavenStem(AbstractCulture):
    """藏干（即人元，司令取天干，分野取天干的五行）"""
    _heaven_stem: HeavenStem
    """天干"""
    _type: HideHeavenStemType
    """藏干类型"""

    def __init__(self, heaven_stem: HeavenStem | str | int, hide_heaven_stem_type: HideHeavenStemType):
        if isinstance(heaven_stem, int) or isinstance(heaven_stem, str):
            self._heaven_stem = HeavenStem(heaven_stem)
        else:
            self._heaven_stem = heaven_stem
        self._type = hide_heaven_stem_type

    def get_name(self) -> str:
        return self._heaven_stem.get_name()

    def get_heaven_stem(self) -> HeavenStem:
        """
        天干
        :return: 天干
        """
        return self._heaven_stem

    def get_type(self) -> HideHeavenStemType:
        """
        藏干类型
        :return: 藏干类型
        """
        return self._type


class HideHeavenStemDay(AbstractCultureDay):
    """人元司令分野（地支藏干+天索引）"""

    def __init__(self, hide_heaven_stem: HideHeavenStem, day_index: int):
        super().__init__(hide_heaven_stem, day_index)

    def get_hide_heaven_stem(self) -> HideHeavenStem:
        """
        :return: 藏干
        """
        return self.get_culture()

    def get_name(self) -> str:
        heaven_stem: HeavenStem = self.get_hide_heaven_stem().get_heaven_stem()
        return f'{heaven_stem.get_name()}{heaven_stem.get_element().get_name()}'


class SixtyCycle(LoopTyme):
    """六十甲子(六十干支周)"""
    _NAMES: [str] = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self._NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> SixtyCycle:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> SixtyCycle:
        return cls(index)

    def next(self, n: int) -> SixtyCycle:
        return SixtyCycle(self.next_index(n))

    def get_heaven_stem(self) -> HeavenStem:
        """
        天干
        :return: 天干
        """
        return HeavenStem(self.get_index() % 10)

    def get_earth_branch(self) -> EarthBranch:
        """
        地支
        :return: 地支
        """
        return EarthBranch(self.get_index() % 12)

    def get_sound(self) -> Sound:
        """
        纳音
        :return: 纳音
        """
        return Sound(self.get_index() // 2)

    def get_peng_zu(self) -> PengZu:
        """
        彭祖百忌
        :return: 彭祖百忌
        """
        return PengZu(self)

    def get_ten(self) -> Ten:
        """
        旬
        :return: 旬
        """
        return Ten((self.get_heaven_stem().get_index() - self.get_earth_branch().get_index()) // 2)

    def get_extra_earth_branches(self) -> list[EarthBranch]:
        """
        旬空(空亡)，因地支比天干多2个，旬空则为每一轮干支一一配对后多出来的2个地支
        :return: 旬空(空亡)
        """
        earth_branch: EarthBranch = EarthBranch(10 + self.get_earth_branch().get_index() - self.get_heaven_stem().get_index())
        return [earth_branch, earth_branch.next(1)]


class SixtyCycleYear(AbstractTyme):
    """
    干支年
    """
    _year: int

    def __init__(self, year: int):
        if year < -1 or year > 9999:
            raise ValueError(f'illegal sixty cycle year: {year}')
        self._year = year

    @classmethod
    def from_year(cls, year: int) -> SixtyCycleYear:
        return cls(year)

    def get_year(self) -> int:
        """
        年
        :return: 返回为干支年数字，范围为-1到9999。
        """
        return self._year

    def get_name(self) -> str:
        """
        :return: {六十甲子}年
        """
        return f'{self.get_sixty_cycle().get_name()}年'

    def next(self, n: int) -> SixtyCycleYear:
        return SixtyCycleYear(self._year + n)

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        干支
        :return: 干支 SixtyCycle
        """
        return SixtyCycle(self._year - 4)

    def get_twenty(self) -> Twenty:
        """
        运
        :return: 返回为运 Twenty。
        """
        return Twenty(floor((self._year - 1864) / 20))

    def get_nine_star(self) -> NineStar:
        """
        九星
        :return: 返回为九星 NineStar。
        """
        return NineStar(63 + self.get_twenty().get_sixty().get_index() * 3 - self.get_sixty_cycle().get_index())

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 返回为方位 Direction。
        """
        return Direction([0, 7, 7, 2, 3, 3, 8, 1, 1, 6, 0, 0][self.get_sixty_cycle().get_earth_branch().get_index()])

    def get_first_month(self) -> SixtyCycleMonth:
        """
        首月（依据五虎遁和正月起寅的规律）
        :return: 干支月
        """
        h: HeavenStem = HeavenStem.from_index((self.get_sixty_cycle().get_heaven_stem().get_index() + 1) * 2)
        return SixtyCycleMonth(self, SixtyCycle.from_name(f'{h.get_name()}寅'))

    def get_months(self) -> list[SixtyCycleMonth]:
        """
        干支月列表
        :return: 干支月列表
        """
        l: [SixtyCycleMonth] = []
        m: SixtyCycleMonth = self.get_first_month()
        l.append(m)
        for i in range(1, 12):
            l.append(m.next(i))
        return l


class SixtyCycleMonth(AbstractTyme):
    """
    干支月
    """
    _year: SixtyCycleYear
    """干支年"""
    _month: SixtyCycle
    """月柱"""

    def __init__(self, year: SixtyCycleYear, month: SixtyCycle):
        """
        :param year: 干支年
        :param month: 干支月
        """
        self._year = year
        self._month = month

    @classmethod
    def from_index(cls, year: int, index: int) -> SixtyCycleMonth:
        return SixtyCycleYear.from_year(year).get_first_month().next(index)

    def get_sixty_cycle_year(self) -> SixtyCycleYear:
        """
        干支年
        :return: 干支年
        """
        return self._year

    def get_year(self) -> SixtyCycle:
        """
        年柱
        :return: 干支
        """
        return self._year.get_sixty_cycle()

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        干支
        :return: 干支
        """
        return self._month

    def get_index_in_year(self) -> int:
        """
        位于当年的索引(0-11)，寅月为0，依次类推
        :return: 返回为数字，范围0到11，寅月为0，依次类推。
        """
        return self._month.get_earth_branch().next(-2).get_index()

    def get_name(self) -> str:
        """
        名称
        :return: 名称
        """
        return f'{self._month}月'

    def __str__(self) -> str:
        return f'{self._year}{self.get_name()}'

    def next(self, n: int) -> SixtyCycleMonth:
        return SixtyCycleMonth(SixtyCycleYear.from_year((self._year.get_year()*12 + self.get_index_in_year() + n) // 12), self._month.next(n))

    def get_first_day(self) -> SixtyCycleDay:
        from tyme4py.solar import SolarTerm
        return SixtyCycleDay.from_solar_day(SolarTerm.from_index(self._year.get_year(), 3+self.get_index_in_year()*2).get_solar_day())

    def get_days(self) -> list[SixtyCycleDay]:
        """
        本月的干支日列表
        :return: 支日列表
        """
        l: [SixtyCycleDay] = []
        d: SixtyCycleDay = self.get_first_day()
        while d.get_sixty_cycle_month() == self:
            l.append(d)
            d = d.next(1)
        return l

    def get_nine_star(self) -> NineStar:
        """
        :return: 九星 NineStar。
        """
        index = self._month.get_earth_branch().get_index()
        if index < 2:
            index += 3
        return NineStar(27 - self.get_year().get_earth_branch().get_index() % 3 * 3 - index)

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 方位 Direction。
        """
        n: int = [7, -1, 1, 3][self._month.get_earth_branch().next(-2).get_index() % 4]
        return self._month.get_heaven_stem().get_direction() if n == -1 else Direction(n)


class SixtyCycleDay(AbstractTyme):
    """干支日"""
    _solar_day: SolarDay
    """公历日"""
    _month: SixtyCycleMonth
    """干支月"""
    _day: SixtyCycle
    """日柱"""

    def __init__(self, solar_day: SolarDay, month: SixtyCycleMonth, day: SixtyCycle):
        """
        :param solar_day: 公历年
        :param month: 干支月
        :param day: 日柱
        """
        self._solar_day = solar_day
        self._month = month
        self._day = day

    @classmethod
    def from_solar_day(cls, solar_day: SolarDay) -> SixtyCycleDay:
        from tyme4py.solar import SolarTerm, SolarDay
        from tyme4py.lunar import LunarYear, LunarMonth, LunarDay
        solar_year: int = solar_day.get_year()
        spring_solar_day: SolarDay = SolarTerm.from_index(solar_year, 3).get_solar_day()
        lunar_day: LunarDay = solar_day.get_lunar_day()
        lunar_year: LunarYear = lunar_day.get_lunar_month().get_lunar_year()
        if lunar_year.get_year() == solar_year:
            if solar_day.is_before(spring_solar_day):
                lunar_year = lunar_year.next(-1)
        elif lunar_year.get_year() < solar_year:
            if not solar_day.is_before(spring_solar_day):
                lunar_year = lunar_year.next(1)
        term: SolarTerm = solar_day.get_term()
        index: int = term.get_index() - 3
        if index < 0 and term.get_solar_day().is_after(spring_solar_day):
            index += 24
        return cls(solar_day, SixtyCycleMonth(SixtyCycleYear.from_year(lunar_year.get_year()), LunarMonth.from_ym(solar_year, 1).get_sixty_cycle().next(int(floor(index * 0.5)))), lunar_day.get_sixty_cycle())

    def get_solar_day(self) -> SolarDay:
        """
        :return: 公历日
        """
        return self._solar_day

    def get_sixty_cycle_month(self) -> SixtyCycleMonth:
        """
        :return: 干支月
        """
        return self._month

    def get_year(self) -> SixtyCycle:
        """
        年柱
        :return: 干支
        """
        return self._month.get_year()

    def get_month(self) -> SixtyCycle:
        """
        月柱
        :return: 干支
        """
        return self._month.get_sixty_cycle()

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        干支
        :return: 干支
        """
        return self._day

    def get_name(self) -> str:
        return f'{self._day}日'

    def __str__(self) -> str:
        return f'{self._month}{self.get_name()}'

    def next(self, n: int) -> SixtyCycleDay:
        return SixtyCycleDay.from_solar_day(self._solar_day.next(n))

    def get_duty(self) -> Duty:
        """
        建除十二值神
        :return: 建除十二值神 Duty。
        """
        return Duty(self._day.get_earth_branch().get_index() - self.get_month().get_earth_branch().get_index())

    def get_twelve_star(self) -> TwelveStar:
        """
        黄道黑道十二神
        :return: 黄道黑道十二神 TwelveStar。
        """
        return TwelveStar(self._day.get_earth_branch().get_index() + (8 - self.get_month().get_earth_branch().get_index() % 6) * 2)

    def get_nine_star(self) -> NineStar:
        """
        九星
        :return: 九星 NineStar。
        """
        from tyme4py.solar import SolarDay, SolarTerm
        d: SolarDay = self._solar_day
        dong_zhi: SolarTerm = SolarTerm(d.get_year(), 0)
        dong_zhi_solar: SolarDay = dong_zhi.get_solar_day()
        xia_zhi_solar: SolarDay = dong_zhi.next(12).get_solar_day()
        dong_zhi_solar2: SolarDay = dong_zhi.next(24).get_solar_day()
        dong_zhi_index: int = dong_zhi_solar.get_lunar_day().get_sixty_cycle().get_index()
        xia_zhi_index: int = xia_zhi_solar.get_lunar_day().get_sixty_cycle().get_index()
        dong_zhi_index2: int = dong_zhi_solar2.get_lunar_day().get_sixty_cycle().get_index()
        solar_shun_bai: SolarDay = dong_zhi_solar.next(60 - dong_zhi_index if dong_zhi_index > 29 else -dong_zhi_index)
        solar_shun_bai2: SolarDay = dong_zhi_solar2.next(60 - dong_zhi_index2 if dong_zhi_index2 > 29 else -dong_zhi_index2)
        solar_ni_zi: SolarDay = xia_zhi_solar.next(60 - xia_zhi_index if xia_zhi_index > 29 else -xia_zhi_index)
        offset: int = 0
        if not d.is_before(solar_shun_bai) and d.is_before(solar_ni_zi):
            offset = d.subtract(solar_shun_bai)
        elif not d.is_before(solar_ni_zi) and d.is_before(solar_shun_bai2):
            offset = 8 - d.subtract(solar_ni_zi)
        elif not d.is_before(solar_shun_bai2):
            offset = d.subtract(solar_shun_bai2)
        elif d.is_before(solar_shun_bai):
            offset = 8 + solar_shun_bai.subtract(d)
        return NineStar(offset)

    def get_jupiter_direction(self) -> Direction:
        """
        太岁方位
        :return: 方位 Direction。
        """
        index: int = self._day.get_index()
        from tyme4py.culture import Element
        return Element(index // 12).get_direction() if index % 12 < 6 else self._month.get_sixty_cycle_year().get_jupiter_direction()

    def get_fetus_day(self) -> FetusDay:
        """
        逐日胎神
        :return:逐日胎神 FetusDay。
        """
        return FetusDay.from_sixty_cycle_day(self)

    def get_twenty_eight_star(self) -> TwentyEightStar:
        """
        二十八宿
        :return: 二十八宿 TwentyEightStar。
        """
        from tyme4py.culture.star.twentyeight import TwentyEightStar
        return TwentyEightStar([10, 18, 26, 6, 14, 22, 2][self._solar_day.get_week().get_index()]).next(-7 * self._day.get_earth_branch().get_index())

    def get_gods(self) -> list[God]:
        """
        神煞列表(吉神宜趋，凶神宜忌)
        :return: 神煞列表
        """
        return God.get_day_gods(self.get_month(), self._day)

    def get_recommends(self) -> list[Taboo]:
        """
        今日 宜
        :return: 宜忌列表
        """
        return Taboo.get_day_recommends(self.get_month(), self._day)

    def get_avoids(self) -> list[Taboo]:
        """
        今日 忌
        :return: 宜忌列表
        """
        return Taboo.get_day_avoids(self.get_month(), self._day)

    def get_hours(self) -> list[SixtyCycleHour]:
        """
        当天的干支时辰列表
        :return: 干支时辰列表
        """
        from tyme4py.solar import SolarDay, SolarTime
        l: [SixtyCycleHour] = []
        d: SolarDay = self._solar_day.next(-1)
        t: SolarTime = SolarTime.from_ymd_hms(d.get_year(), d.get_month(), d.get_day(), 23, 0, 0)
        h: SixtyCycleHour = SixtyCycleHour.from_solar_time(t)
        l.append(h)
        for i in range(0, 11):
            h = h.next(7200)
            l.append(h)
        return l

    def get_three_pillars(self) -> ThreePillars:
        return ThreePillars(self.get_year(), self.get_month(), self.get_sixty_cycle())


class SixtyCycleHour(AbstractTyme):
    """
    干支时辰
    """
    _solar_time: SolarTime
    """公历时刻"""
    _day: SixtyCycleDay
    """干支日"""
    _hour: SixtyCycle
    """时柱"""

    def __init__(self, solar_time: SolarTime):
        from tyme4py.solar import SolarTerm, SolarTime
        from tyme4py.lunar import LunarYear, LunarMonth, LunarDay, LunarHour
        solar_year: int = solar_time.get_year()
        spring_solar_time: SolarTime = SolarTerm.from_index(solar_year, 3).get_julian_day().get_solar_time()
        lunar_hour: LunarHour = solar_time.get_lunar_hour()
        lunar_day: LunarDay = lunar_hour.get_lunar_day()
        lunar_year: LunarYear = lunar_day.get_lunar_month().get_lunar_year()
        if lunar_year.get_year() == solar_year:
            if solar_time.is_before(spring_solar_time):
                lunar_year = lunar_year.next(-1)
        elif lunar_year.get_year() < solar_year:
            if not solar_time.is_before(spring_solar_time):
                lunar_year = lunar_year.next(1)

        term: SolarTerm = solar_time.get_term()
        index: int = term.get_index() - 3
        if index < 0 and term.get_julian_day().get_solar_time().is_after(SolarTerm.from_index(solar_year, 3).get_julian_day().get_solar_time()):
            index += 24
        d: SixtyCycle = lunar_day.get_sixty_cycle()
        if solar_time.get_hour() == 23:
            d = d.next(1)
        y: SixtyCycleYear = SixtyCycleYear.from_year(lunar_year.get_year())
        m: LunarMonth = LunarMonth.from_ym(solar_year, 1)

        self._solar_time = solar_time
        self._day = SixtyCycleDay(solar_time.get_solar_day(), SixtyCycleMonth(y, m.get_sixty_cycle().next(int(floor(index * 0.5)))), d)
        self._hour = lunar_hour.get_sixty_cycle()

    @classmethod
    def from_solar_time(cls, solar_time: SolarTime) -> SixtyCycleHour:
        return cls(solar_time)

    def get_year(self) -> SixtyCycle:
        """
        年柱
        :return: 干支
        """
        return self._day.get_year()

    def get_month(self) -> SixtyCycle:
        """
        月柱
        :return: 干支
        """
        return self._day.get_month()

    def get_day(self) -> SixtyCycle:
        """
        日柱
        :return: 干支
        """
        return self._day.get_sixty_cycle()

    def get_sixty_cycle(self) -> SixtyCycle:
        """
        干支
        :return: 干支
        """
        return self._hour

    def get_sixty_cycle_day(self) -> SixtyCycleDay:
        """
        干支日
        :return: 干支日
        """
        return self._day

    def get_solar_time(self) -> SolarTime:
        """
        公历时刻
        :return: 公历时刻
        """
        return self._solar_time

    def get_name(self) -> str:
        return f'{self._hour}时'

    def __str__(self) -> str:
        return f'{self._day}{self.get_name()}'

    def get_index_in_day(self) -> int:
        """
        位于当天的索引
        :return: 位于当天的索引
        """
        h: int = self._solar_time.get_hour()
        if h == 23:
            return 0
        return (h + 1) // 2

    def next(self, n: int) -> SixtyCycleHour:
        return SixtyCycleHour.from_solar_time(self._solar_time.next(n))

    def get_twelve_star(self) -> TwelveStar:
        """
        黄道黑道十二神
        :return: 黄道黑道十二神 TwelveStar。
        """
        return TwelveStar(self._hour.get_earth_branch().get_index() + (8 - self.get_day().get_earth_branch().get_index() % 6) * 2)

    def get_nine_star(self) -> NineStar:
        """
        九星（时家紫白星歌诀：三元时白最为佳，冬至阳生顺莫差，孟日七宫仲一白，季日四绿发萌芽，每把时辰起甲子，本时星耀照光华，时星移入中宫去，顺飞八方逐细查。夏至阴生逆回首，孟归三碧季加六，仲在九宫时起甲，依然掌中逆轮跨。）
        :return: 九星 NineStar。
        """
        from tyme4py.solar import SolarTerm, SolarDay
        solar: SolarDay = self._solar_time.get_solar_day()
        dong_zhi: SolarTerm = SolarTerm(solar.get_year(), 0)
        earth_branch_index: int = self.get_index_in_day() % 12
        index: int = [8, 5, 2][self.get_day().get_earth_branch().get_index() % 3]
        if (not solar.is_before(dong_zhi.get_julian_day().get_solar_day())) and solar.is_before(dong_zhi.next(12).get_julian_day().get_solar_day()):
            index = 8 + earth_branch_index - index
        else:
            index -= earth_branch_index
        return NineStar(index)

    def get_eight_char(self) -> EightChar:
        """
        八字
        :return: 八字
        """
        return EightChar(self.get_year(), self.get_month(), self.get_day(), self._hour)

    def get_recommends(self) -> list[Taboo]:
        """
        时辰 宜
        :return: 宜忌列表
        """
        return Taboo.get_hour_recommends(self.get_day(), self._hour)

    def get_avoids(self) -> list[Taboo]:
        """
        时辰 忌
        :return: 宜忌列表
        """
        return Taboo.get_hour_avoids(self.get_day(), self._hour)
