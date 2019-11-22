from .Node import Node
from .BooleanNode import BooleanNode
from .EnvironmentVariables import EnvironmentVariables
from .MappingNode import MappingNode, StringMapping
from .NumberNode import IntegerNode
from .StringNode import FlowStyleString, StringNode
from typing import Any, Dict, List, Type, cast

class Step(MappingNode):
  __classes = cast(Dict[str, Type[Node]], {
    'id': FlowStyleString,
    'if': FlowStyleString,
    'name': FlowStyleString,
    'uses': FlowStyleString,
    'run': StringNode,
    'working-directory': FlowStyleString,
    'shell': FlowStyleString,
    'with': StringMapping,
    'env': EnvironmentVariables,
    'continue-on-error': BooleanNode,
    'timeout-minutes': IntegerNode,
  })

  def __init__(self, info: Dict[str, Any]):
    converted: Dict[str, Node] = {}
    for key, value in info.items():
      the_class = type(self).__classes.get(key, None)
      if the_class is None: raise RuntimeError(f"Step configuration named {key} is not supported.")
      converted[key] = the_class(value)
    super().__init__(converted)

  @property
  def key_order(self) -> List[str]:
    return [
      'id',
      'if',
      'name',
      'env',
      'run',
      'shell',
      'working-directory',
      'uses',
      'with',
      'continue-on-error',
      'timeout-minutes',
    ]