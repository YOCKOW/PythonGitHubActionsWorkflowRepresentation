from .string import Lines
from .Node import Node
from .util import yaml_from_number
from numbers import Real, Integral

class NumberNode(Node):
  def __init__(self, info: Real):
    assert isinstance(info, Real)
    self.__number = info

  def yaml(self) -> Lines:
    return yaml_from_number(self.__number)

class IntegerNode(NumberNode):
  def __init__(self, info: Integral):
    assert isinstance(info, Integral)
    super().__init__(info)

