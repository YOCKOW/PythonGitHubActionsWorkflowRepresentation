from .Node import Node
from .EnvironmentVariables import EnvironmentVariables
from .MappingNode import MappingNode, NodeSpecifiedMapping
from .NumberNode import IntegerNode
from .SequenceNode import SequenceNode, StringSequence
from .StringNode import FlowStyleString
from .string import Lines
from numbers import Integral
from typing import Any, Dict, List, Optional, Type, Union, cast

class Container(NodeSpecifiedMapping):
  class Port(Node):
    def __init__(self, info: Union[Integral, str]):
      if isinstance(info, Integral):
        self.__payload = IntegerNode(info)
      elif isinstance(info, str):
        self.__payload = FlowStyleString(info)
      else:
        raise ValueError("Unexpected value for port.")
    
    def yaml(self) -> Lines:
      return self.__payload.yaml()
  
  class PortSequence(SequenceNode):
    def __init__(self, info: List[Union[Integral, str]]):
      assert isinstance(info, list)
      ports: List[Node] = []
      for port in info:
        ports.append(Container.Port(port))
      super().__init__(ports)

  @classmethod
  def node_class(cls, name: str) -> Optional[Type[Node]]:
    return {
      'image': FlowStyleString,
      'env': EnvironmentVariables,
      'ports': Container.PortSequence,
      'volumes': StringSequence,
      'options': FlowStyleString,
    }.get(name, None)

  @property
  def key_order(self) -> List[str]:
    return [
      'image',
      'env',
      'ports',
      'volumes',
      'options',
    ]

class Services(NodeSpecifiedMapping):
  @classmethod
  def node_class(cls, name: str) -> Optional[Type[Node]]:
    return Container
