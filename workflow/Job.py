from .Node import Node
from .Containers import Container, Services
from .EnvironmentVariables import EnvironmentVariables
from .MappingNode import NodeSpecifiedMapping
from .NumberNode import IntegerNode
from .Step import Step
from .Strategy import Strategy
from .StringNode import FlowStyleString
from .SequenceNode import StringSequence, NodeSpecifiedSequence
from .string import Lines
from typing import Optional, List, Type, Union

class Job(NodeSpecifiedMapping):
  class Needs(Node):
    def __init__(self, info: Union[str, List[str]]):
      if isinstance(info, str):
        self.__payload = FlowStyleString(info)
      elif isinstance(info, list):
        self.__payload = StringSequence(info)
      else:
        raise ValueError("Unxpected value for `needs`.")
    
    def yaml(self) -> Lines:
      return self.__payload.yaml()

  class Steps(NodeSpecifiedSequence):
    @classmethod
    def node_class(cls) -> Type[Node]:
      return Step

  @classmethod
  def node_class(cls, name: str) -> Optional[Type[Node]]:
    return {
      'name': FlowStyleString,
      'needs': Job.Needs,
      'runs-on': FlowStyleString,
      'env': EnvironmentVariables,
      'if': FlowStyleString,
      'steps': Job.Steps,
      'timeout-minutes': IntegerNode,
      'strategy': Strategy,
      'container': Container,
      'services': Services,
    }.get(name, None)

  @property
  def key_order(self) -> List[str]:
    return [
      'if',
      'name',
      'needs',
      'strategy',
      'runs-on',
      'container',
      'services',
      'env',
      'timeout-minutes',
      'steps',
    ]
  
