from .Node import Node
from .EnvironmentVariables import EnvironmentVariables
from .MappingNode import MappingNode
from .NumberNode import IntegerNode
from .SequenceNode import SequenceNode, StringSequence
from .StringNode import FlowStyleString
from .string import Lines
from numbers import Integral
from typing import Any, Dict, List, Type, Union, cast

class Container(MappingNode):
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

  __classes = cast(Dict[str, Type[Node]], {
    'image': FlowStyleString,
    'env': EnvironmentVariables,
    'ports': PortSequence,
    'volumes': StringSequence,
    'options': FlowStyleString,
  })

  def __init__(self, info: Dict[str, Any]):
    converted: Dict[str, Node] = {}
    assert isinstance(info, dict)
    for key, value in info.items():
      the_class = type(self).__classes.get(key, None)
      if the_class is None: raise RuntimeError(f"Container configuration named {key} is not supported.")
      converted[key] = the_class(value)
    super().__init__(converted)

  @property
  def key_order(self) -> List[str]:
    return [
      'image',
      'env',
      'ports',
      'volumes',
      'options',
    ]

class Services(MappingNode):
  def __init__(self, info: Dict[str, Dict[str, Any]]):
    converted: Dict[str, Container] = {}
    assert isinstance(info, dict)
    for service_name, container_info in info.items():
      assert isinstance(container_info, dict)
      converted[service_name] = Container(container_info)
    super().__init__(cast(Dict[str, Node], converted))
