from .Node import Node, FlowStyleNode
from . import util
from copy import copy
from typing import List

def _short_indent() -> str:
  return util.indent(1)[0:(util.INDENT_WIDTH - 1)]

class SequenceNode(Node):
  def __init__(self, some_list: List[Node]):
    if len(some_list) < 1: raise ValueError("List must not be empty.")
    self.children = copy(some_list)

  def yaml_lines(self) -> List[str]:
    result: List[str] = []
    for node in self.children:
      child_lines = node.yaml_lines()
      nn = len(child_lines)
      if nn < 1: continue
      result.append(f"-{_short_indent()}{child_lines[0]}")
      if nn < 2: continue
      result.extend(map(lambda line: f"{util.indent(1)}{line}", child_lines[1:]))
    return result

class FlowStyleSequence(SequenceNode, FlowStyleNode):
  def __init__(self, some_list: List[FlowStyleNode]):
    for node in some_list:
      if not isinstance(node, FlowStyleNode): raise ValueError("All nodes must be flow style.")
    super().__init__(some_list)

  def yaml_lines(self) -> List[str]:
    yaml_strings: List[str] = []
    for node in self.children:
      child_lines = node.yaml_lines()
      assert len(child_lines) == 1, "Flow style output must be one line."
      yaml_strings.append(child_lines[0])
    return [f"[{', '.join(yaml_strings)}]"]


