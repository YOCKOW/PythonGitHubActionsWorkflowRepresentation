from .Node import Node
from .SequenceNode import SequenceNode
from .StringNode import FlowStyleString
from typing import List

class _StringSequence(SequenceNode):
  def __init__(self, strings: List[str]):
    nodes: List[Node] = []
    for string in strings:
      nodes.append(FlowStyleString(string))
    super().__init__(nodes)

class Branches(_StringSequence): pass

class Tags(_StringSequence): pass
