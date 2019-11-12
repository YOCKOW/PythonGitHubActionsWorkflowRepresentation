from .Node import Node, FlowStyleNode
from . import util
import re
from typing import Dict, List

def _key_yaml(key) -> str:
  return util.dump_yaml_string(key, force_flow_style=True)

class MappingNode(Node):
  def __init__(self, some_dict: Dict[str, Node]):
    self._map: Dict[str, Node] = {}
    for key, node in some_dict.items():
      if not isinstance(key, str) or not isinstance(node, Node): raise ValueError("Invalid value for `MappingNode`.")
      self._map[key] = node

  def key_order(self) -> List[str]:
    """
    You can define the order of keys used by `yaml_lines`.
    To achieve that, you ought to implement subclasses and this method must be overridden.
    """
    # Default
    return sorted(list(self._map.keys()))

  def yaml_lines(self) -> List[str]:
    result: List[str] = []
    for key in self.key_order():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml_lines()
      nn = len(child_lines)
      if nn < 1: continue
      if nn == 1:
        result.append(f"{_key_yaml(key)}: {child_lines[0]}")
      else:
        result.append(f"{_key_yaml(key)}:")
        result.extend(map(lambda line: f"{util.indent(1)}{line}", child_lines))
    return result

class FlowStyleMapping(MappingNode, FlowStyleNode):
  def __init__(self, some_dict: Dict[str, FlowStyleNode]):
    for node in some_dict.values():
      if not isinstance(node, FlowStyleNode): raise ValueError("All nodes must be flow style.")
    super().__init__(some_dict)

  def yaml_lines(self) -> List[str]:
    items: List[str] = []
    for key in self.key_order():
      child = self._map.get(key, None)
      if child is None: continue
      child_lines = child.yaml_lines()
      assert len(child_lines) == 1
      items.append(f"{_key_yaml(key)}: {child_lines[0]}")
    return ["{" + ", ".join(items) + "}"]