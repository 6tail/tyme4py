# -*- coding:utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod


class Culture(ABC):
    """传统文化(民俗)"""

    @abstractmethod
    def get_name(self) -> str:
        """
        名称
        :return: 名称
        """
        pass


class Tyme(Culture):
    @abstractmethod
    def next(self, n: int) -> Tyme | None:
        """
        推移
        :param n:推移步数
        :return: 推移后的Tyme
        """
        pass


class AbstractCulture(Culture):
    """传统文化抽象"""

    @abstractmethod
    def get_name(self) -> str:
        pass

    def __str__(self) -> str:
        return self.get_name()

    def __eq__(self, other: Culture) -> bool:
        return other and other.__str__() == self.__str__()

    @staticmethod
    def index_of(index: int, size: int) -> int:
        """
        转换为不超范围的索引
        :param index: 索引
        :param size: 长度大小
        :return: 索引，从0开始
        """
        i: int = index % size
        return i + size if i < 0 else i


class AbstractTyme(AbstractCulture, Tyme):
    """抽象Tyme"""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def next(self, n: int) -> Tyme | None:
        pass


class AbstractCultureDay(AbstractCulture):
    """带天索引的传统文化抽象"""
    _culture: AbstractCulture
    _day_index: int

    def __init__(self, culture: AbstractCulture, day_index: int):
        self._culture = culture
        self._day_index = day_index

    def get_day_index(self) -> int:
        """
        天索引
        :return: 索引
        """
        return self._day_index

    def get_culture(self) -> AbstractCulture:
        return self._culture

    def get_name(self) -> str:
        return self._culture.get_name()

    def __str__(self) -> str:
        return f'{self.get_name()}第{self.get_day_index() + 1}天'


class LoopTyme(AbstractTyme):
    """可轮回的Tyme"""
    _names: []
    """名称列表"""
    _index: int
    """索引，从0开始"""

    def __init__(self, names: [str], index_or_name: int | str):
        """
        :param names: 名称列表
        :param index_or_name: 索引，支持负数，自动轮转; 名称
        """
        self._names = names
        self._index = self._index_of_by(index_or_name)

    def _index_of_by(self, index_or_name: int | str) -> int:
        """
        :param index_or_name: 索引或名称
        :return: 索引
        """
        if isinstance(index_or_name, int):
            return self.index_of(index_or_name, self.get_size())
        else:
            for i in range(0, self.get_size()):
                if index_or_name == self._names[i]:
                    return i
            raise ValueError(f"illegal name: {index_or_name}")

    def get_name(self) -> str:
        """
        名称
        :return: 名称
        """
        return self._names[self._index]

    def get_index(self) -> int:
        """
        索引
        :return: 索引，从0开始
        """
        return self._index

    def get_size(self) -> int:
        """
        数量
        :return: 数量
        """
        return self._names.__len__()

    def next_index(self, n: int) -> int:
        """
        推移后的索引
        :param n: 推移步数
        :return: 索引，从0开始
        """
        return self._index_of_by(self._index + n)

    def steps_to(self, target_index: int) -> int:
        """
        到目标索引的步数
        :param target_index: 目标索引
        :return: 步数
        """
        return self.index_of(target_index - self._index, self.get_size())

    @abstractmethod
    def next(self, n: int) -> LoopTyme | None:
        pass
