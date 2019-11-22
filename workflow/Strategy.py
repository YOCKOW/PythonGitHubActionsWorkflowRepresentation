from .Node import Node
from .BooleanNode import BooleanNode
from .MappingNode import MappingNode
from .Matrix import Matrix
from .NumberNode import IntegerNode
from typing import Any, Dict, List

class Strategy(MappingNode):
  def __init__(self, info: Dict[str, Any]):
    assert isinstance(info, dict)
    converted: Dict[str, Node] = {}
    for key, value in info.items():
      if key == 'fail-fast':
        assert isinstance(value, bool)
        converted[key] = BooleanNode(value)
      elif key == 'max-parallel':
        assert isinstance(value, int)
        converted[key] = IntegerNode(value)
      elif key == 'matrix':
        assert isinstance(value, dict)
        converted[key] = Matrix(value)
      else:
        raise ValueError(f"Unexpected key named {key} for strategy.")
    super().__init__(converted)

  @property
  def key_order(self) -> List[str]:
    return [
      'fail-fast',
      'max-parallel',
      'matrix',
    ]

