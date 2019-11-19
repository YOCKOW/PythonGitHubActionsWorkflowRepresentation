from .Node import Node, FlowStyleNode
from .StringNode import StringNode
from .string import Lines, Line
from . import util
from copy import copy
from typing import Dict, List

def _key_yaml(key) -> str:
  return util.yaml_from_string(key, force_flow_style=True)[0].raw_string

class MappingNode(Node):
  def __init__(self, some_dict: Dict[str, Node]):
    self._map: Dict[str, Node] = {}
    for key, node in some_dict.items():
      if not isinstance(key, str) or not isinstance(node, Node): raise ValueError("Invalid value for `MappingNode`.")
      self._map[key] = node
    self.__key_order = sorted(list(self._map.keys()))

  def __getitem__(self, key: str) -> Node:
    return self._map[key]

  def __setitem__(self, key: str, node: Node):
    self._map[key] = node

  @property
  def key_order(self) -> List[str]:
    return copy(self.__key_order)

  @key_order.setter
  def key_order(self, keys: List[str]):
    self.__key_order = copy(keys)

  def _sorted_keys(self) -> List[str]:
    key_priority_dict: Dict[str, int] = {}
    key_order = self.key_order
    nn = len(key_order)
    for ii in range(0, nn):
      key_priority_dict[key_order[ii]] = ii
    return sorted(self._map.keys(), key=lambda key: key_priority_dict.get(key, nn))

  def yaml(self) -> Lines:
    result: Lines = Lines()
    for key in self._sorted_keys():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml()
      nn = child_lines.count
      if nn < 1: continue
      if nn == 1 and (isinstance(child, FlowStyleNode) or isinstance(child, StringNode)):
        result.append(f"{_key_yaml(key)}: {child_lines[0].raw_string}")
      else:
        result.append(f"{_key_yaml(key)}:")
        for line in child_lines:
          line.shift_right()
          result.append(line)
    return result

class FlowStyleMapping(MappingNode, FlowStyleNode):
  def __init__(self, some_dict: Dict[str, FlowStyleNode]):
    new_dict: Dict[str, Node] = {}
    for key, node in some_dict.items():
      if not isinstance(node, FlowStyleNode): raise ValueError("All nodes must be flow style.")
      new_dict[key] = node
    super().__init__(new_dict)

  def yaml(self) -> Lines:
    items: List[str] = []
    for key in self._sorted_keys():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml()
      assert child_lines.count == 1
      items.append(f"{_key_yaml(key)}: {child_lines[0].raw_string}")
    return Lines([Line("{" + ", ".join(items) + "}")])