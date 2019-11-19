from .Node import Node, FlowStyleNode
from .string import Lines, Line
from . import util
import re
from typing import Dict, List

def _key_yaml(key) -> str:
  return util.yaml_from_string(key, force_flow_style=True)[0].raw_string

class MappingNode(Node):
  def __init__(self, some_dict: Dict[str, Node]):
    self._map: Dict[str, Node] = {}
    for key, node in some_dict.items():
      if not isinstance(key, str) or not isinstance(node, Node): raise ValueError("Invalid value for `MappingNode`.")
      self._map[key] = node

  def __getitem__(self, key: str) -> Node:
    return self._map[key]

  def __setitem__(self, key: str, node: Node):
    self._map[key] = node

  def key_order(self) -> List[str]:
    """
    You can define the order of keys used by `yaml`.
    To achieve that, you ought to implement subclasses and this method must be overridden.
    """
    # Default
    return sorted(list(self._map.keys()))

  def yaml(self) -> Lines:
    result: Lines = Lines()
    for key in self.key_order():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml()
      nn = child_lines.count
      if nn < 1: continue
      if nn == 1:
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
    for key in self.key_order():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml()
      assert child_lines.count == 1
      items.append(f"{_key_yaml(key)}: {child_lines[0].raw_string}")
    return Lines([Line("{" + ", ".join(items) + "}")])