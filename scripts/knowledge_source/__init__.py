from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseObject:
    name: str
    index: int = 0
    loc: tuple = (0, 0, 0, 1, 0, 0, 0)


@dataclass
class Container:
    pass


@dataclass
class Place:
    pass