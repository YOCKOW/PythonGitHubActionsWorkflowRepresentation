from typing import Any, overload
from .Node import Node
from .string import Lines
from .util import yaml_from_boolean

class BooleanNode(Node):
  def __init__(self, info):
    assert isinstance(info, bool)
    self.__boolean = info

  def yaml(self) -> Lines:
    return yaml_from_boolean(self.__boolean)