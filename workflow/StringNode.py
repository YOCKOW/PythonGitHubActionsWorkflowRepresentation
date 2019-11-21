from .Node import Node, FlowStyleNode
from .string import Lines
from . import util
from typing import List

class StringNode(Node):
  def __init__(self, info: str):
    assert isinstance(info, str)
    self.raw_string = info

  def yaml(self) -> Lines:
    return util.yaml_from_string(self.raw_string)

class FlowStyleString(StringNode, FlowStyleNode):
  def yaml(self) -> Lines:
    return util.yaml_from_string(self.raw_string, force_flow_style=True)

