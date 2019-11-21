from .Node import Node, FlowStyleNode
from .StringNode import FlowStyleString
from .string import Lines, Line
from . import util
from copy import copy
from typing import List

def _short_indent() -> str:
  return Lines.indent(1)[0:(Lines.INDENT_WIDTH - 1)]

class SequenceNode(Node):
  def __init__(self, info: List[Node]):
    assert isinstance(info, list)
    if len(info) < 1: raise ValueError("List must not be empty.")
    self.children = copy(info)

  def yaml(self) -> Lines:
    result: Lines = Lines()
    for node in self.children:
      child_lines = node.yaml()
      nn = child_lines.count
      assert nn > 0
      if nn == 1:
        result.append(f"- {child_lines[0].raw_string}")
      else:
        result.append(f"-{_short_indent()}{child_lines[0].raw_string}")
        child_lines.shift_right(1, range(1, nn))
        for ii in range(1, nn):
          result.append(child_lines[ii])
    return result

class FlowStyleSequence(SequenceNode, FlowStyleNode):
  def __init__(self, info: List[FlowStyleNode]):
    new_list: List[Node] = []
    for node in info:
      if not isinstance(node, FlowStyleNode): raise ValueError("All nodes must be flow style.")
      new_list.append(node)
    super().__init__(new_list)

  def yaml(self) -> Lines:
    yaml_strings: List[str] = []
    for node in self.children:
      child_lines = node.yaml()
      assert child_lines.count == 1, "Flow style output must be one line."
      yaml_strings.append(child_lines[0].raw_string)
    return Lines([Line(f"[{', '.join(yaml_strings)}]")])

class StringSequence(SequenceNode):
  def __init__(self, info: List[str]):
    nodes: List[Node] = []
    for string in info:
      nodes.append(FlowStyleString(string))
    super().__init__(nodes)