from .Node import Node
from .EnvironmentVariables import EnvironmentVariables
from .Job import Job
from .MappingNode import NodeSpecifiedMapping
from .On import On
from .StringNode import FlowStyleString
from typing import Optional, List, Type

class Workflow(NodeSpecifiedMapping):
  class Jobs(NodeSpecifiedMapping):
    @classmethod
    def node_class(cls, name: str) -> Optional[Type[Node]]:
      return Job
  
  @classmethod
  def node_class(cls, name: str) -> Optional[Type[Node]]:
    return {
      'name': FlowStyleString,
      'on': On,
      'env': EnvironmentVariables,
      'jobs': Workflow.Jobs,
    }.get(name, None)

  @property
  def key_order(self) -> List[str]:
    return [
      'name',
      'on',
      'env',
      'jobs',
    ]
