from . import BaseObject, Container, Place
from dataclasses import dataclass
from typing import Optional

"""Object"""
@dataclass
class Stem(BaseObject, Container, Place):
    pass


@dataclass
class Tomatoes(BaseObject):
    ripeness: bool
    rottoness: bool
    harvested: bool

    on: Optional[Container]


@dataclass
class Basket(BaseObject, Container):
    on: Optional[Place]


@dataclass
class Tools(BaseObject):
    pass


"""Robot"""
@dataclass
class Robot:
    name:  str
    index: int

    # params
    payload: float = 30
    battery: int = 100

    # discrete value
    holding: Optional[BaseObject]
    harvesting: bool
    navigating: bool
    detecting: bool
    scanning: bool
    loading: Optional[Basket]

    # continuous value
    current_loc: tuple
    end_effector: tuple
    joint_state: tuple
    end_effector_vel: float

    # available actions
    def action_pick(self):
        pass

    def action_harvest(self):
        pass

    def action_scan(self):
        pass



"""Environment"""
class Environment:
    """
    DockStation
    Stems
    PrepareStation
    """
    def __init__(self):
        self.relation_type = ["ADJACENT_TO", "PART_OF", "ON"]

    
