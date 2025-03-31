# -*- coding:utf-8 -*-
from __future__ import annotations

from tyme4py import LoopTyme, AbstractCultureDay


class Phenology(LoopTyme):
    """候"""
    NAMES: [str] = ['蚯蚓结', '麋角解', '水泉动', '雁北乡', '鹊始巢', '雉始雊', '鸡始乳', '征鸟厉疾', '水泽腹坚', '东风解冻', '蛰虫始振', '鱼陟负冰', '獭祭鱼', '候雁北', '草木萌动', '桃始华', '仓庚鸣', '鹰化为鸠', '玄鸟至', '雷乃发声', '始电', '桐始华', '田鼠化为鴽', '虹始见', '萍始生', '鸣鸠拂奇羽', '戴胜降于桑', '蝼蝈鸣', '蚯蚓出', '王瓜生', '苦菜秀', '靡草死', '麦秋至', '螳螂生', '鵙始鸣', '反舌无声', '鹿角解', '蜩始鸣', '半夏生', '温风至', '蟋蟀居壁', '鹰始挚', '腐草为萤', '土润溽暑', '大雨行时', '凉风至', '白露降', '寒蝉鸣', '鹰乃祭鸟', '天地始肃', '禾乃登', '鸿雁来', '玄鸟归', '群鸟养羞', '雷始收声', '蛰虫坯户', '水始涸', '鸿雁来宾', '雀入大水为蛤', '菊有黄花', '豺乃祭兽', '草木黄落', '蛰虫咸俯', '水始冰', '地始冻', '雉入大水为蜃', '虹藏不见', '天气上升地气下降', '闭塞而成冬', '鹖鴠不鸣', '虎始交', '荔挺出']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> Phenology:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> Phenology:
        return cls(index)

    def next(self, n: int) -> Phenology:
        return Phenology(self.next_index(n))

    def get_three_phenology(self) -> ThreePhenology:
        """
        :return: 三候
        """
        return ThreePhenology(self.get_index() % 3)


class ThreePhenology(LoopTyme):
    """三候"""
    NAMES: [str] = ['初候', '二候', '三候']
    """名称"""

    def __init__(self, index_or_name: int | str):
        super().__init__(self.NAMES, index_or_name)

    @classmethod
    def from_name(cls, name: str) -> ThreePhenology:
        return cls(name)

    @classmethod
    def from_index(cls, index: int) -> ThreePhenology:
        return cls(index)

    def next(self, n: int) -> ThreePhenology:
        return ThreePhenology(self.next_index(n))

    def get_three_phenology(self) -> ThreePhenology:
        return ThreePhenology(self.get_index() % 3)


class PhenologyDay(AbstractCultureDay):
    """七十二候"""

    def __init__(self, phenology: Phenology, day_index: int):
        super().__init__(phenology, day_index)

    def get_phenology(self) -> Phenology:
        return super().get_culture()
