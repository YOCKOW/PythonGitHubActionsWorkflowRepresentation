from .Node import Node
from .MappingNode import MappingNode
from .StringNode import FlowStyleString
from functools import reduce
from typing import Dict, Tuple

class EnvironmentVariables(MappingNode):
  def __init__(self, env: Dict[str, str]):
    def reducer(dic: Dict[str, Node], key_value: Tuple[str, str]) -> Dict[str, Node]:
      dic[key_value[0]] = FlowStyleString(key_value[1])
      return dic
    converted: Dict[str, Node] = reduce(reducer, env.items(), {})
    super().__init__(converted)