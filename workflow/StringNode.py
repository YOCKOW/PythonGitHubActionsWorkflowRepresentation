from .Node import Node
from . import util
from typing import List

class StringNode(Node):
  def __init__(self, string: str):
    self.raw_string = string

  def yaml_lines(self) -> List[str]:
    return util.dump_yaml_string(self.raw_string).splitlines()

class FlowStyleString(StringNode):
  def yaml_lines(self) -> List[str]:
    return [util.dump_yaml_string(self.raw_string, force_flow_style=True)]

