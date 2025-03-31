# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme, AbstractCulture, AbstractCultureDay
from tyme4py.culture import Element, Direction, Zodiac, Terrain, Sound, Ten
from tyme4py.culture.pengzu import PengZuEarthBranch, PengZuHeavenStem, PengZu
from tyme4py.culture.star.ten import TenStar
from tyme4py.enums import YinYang, HideHeavenStemType


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
