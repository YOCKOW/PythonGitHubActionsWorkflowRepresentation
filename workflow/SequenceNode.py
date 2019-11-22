from .Node import Node, FlowStyleNode
from .NumberNode import IntegerNode
from .StringNode import FlowStyleString
from .string import Lines, Line
from copy import copy
from numbers import Integral
from typing import Any, List, Type

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

class NodeSpecifiedSequence(SequenceNode):
  @classmethod
  def node_class(cls) -> Type[Node]: raise NotImplementedError()

  def __init__(self, info: List[Any]):
    assert isinstance(info, list)
    nodes: List[Node] = []
    for something in info:
      node = self.__class__.node_class()(something)
      nodes.append(node)
    super().__init__(nodes)


class StringSequence(NodeSpecifiedSequence):
  @classmethod
  def node_class(cls) -> Type[Node]:
    return FlowStyleString

class IntegerSequence(NodeSpecifiedSequence):
  @classmethod
  def node_class(cls) -> Type[Node]:
    return IntegerNode