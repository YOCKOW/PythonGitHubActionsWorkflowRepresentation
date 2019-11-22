from re import M
from .Node import Node
from .BooleanNode import BooleanNode
from .MappingNode import MappingNode
from .NumberNode import IntegerNode, NumberNode
from .SequenceNode import SequenceNode
from .StringNode import FlowStyleString
from numbers import Real, Integral
from typing import Any, Dict, List, Union, cast

def _node_of_something(something: Any) -> Node:
  if isinstance(something, str):
    return FlowStyleString(something)
  if isinstance(something, Real):
    if isinstance(something, Integral):
      return IntegerNode(something)
    return NumberNode(something)
  if isinstance(something, bool):
    return BooleanNode(something)
  
  if isinstance(something, list):
    nodes: List[Node] = []
    for item in something:
      nodes.append(_node_of_something(item))
    return SequenceNode(nodes)
  if isinstance(something, dict):
    mapping: Dict[str, Node] = {}
    for key, value in something.items():
      assert isinstance(key, str)
      mapping[key] = _node_of_something(value)
    return MappingNode(mapping)
  raise RuntimeError("Unexpected object.")

def _simple_sequence_of_something(some_list: List[Any]) -> SequenceNode:
  nn = len(some_list)
  assert nn > 0
  if nn > 1:
    first_type = type(some_list[0])
    for ii in range(1, nn):
      assert type(some_list[ii]) == first_type, "Different Types are found."
  return cast(SequenceNode, _node_of_something(some_list))

def _simple_mapping(some_dict: Dict[str, Any]) -> MappingNode:
  converted: Dict[str, Node] = {}
  for key, value in some_dict.items():
    assert isinstance(key, str) and not isinstance(value, dict) and not isinstance(value, list)
    converted[key] = _node_of_something(value)
  return MappingNode(converted)

class Matrix(MappingNode):
  def __init__(self, info: Dict[str, Union[List[Any], List[Dict[str, Any]]]]):
    payload: Dict[str, Node] = {}
    for key, value in info.items():
      assert isinstance(value, list)
      if key == 'include' or key == 'exclude':
        combinations: List[Node] = []
        for combination in value:
          assert isinstance(combination, dict)
          combinations.append(_simple_mapping(combination))
        payload[key] = SequenceNode(combinations)
      else:
        payload[key] = _simple_sequence_of_something(value)
    super().__init__(payload)

  @property
  def key_order(self) -> List[str]:
    order: List[str] = sorted(filter(lambda key: key != 'include' and key != 'exclude', self._map.keys()))
    order.append('include')
    order.append('exclude')
    return order