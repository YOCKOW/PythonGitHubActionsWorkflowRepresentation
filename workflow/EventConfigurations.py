from .Node import Node
from .SequenceNode import StringSequence
from .StringNode import FlowStyleString
from typing import Any, Dict, List, Tuple, Type

class EventConfiguration(Node):
  name: str = NotImplemented
  _concrete_classes: Dict[str, Type['EventConfiguration']] = {}

  @staticmethod
  def configuration(name: str, info: Any) -> 'EventConfiguration':
    the_class = EventConfiguration._concrete_classes.get(name, None)
    if the_class is None:
      raise RuntimeError(f"Event Configuration named `{name}` is unsupported/unimplemented yet.")
    assert the_class.name == name
    return the_class(info)

  def __init__(self, info: Any): raise NotImplementedError()
    

class ConcreteEventConfigurationType(type):
  """ Metaclass for concrete `EventConfiguration` classes. """
  def __init__(self: Type[EventConfiguration], name: str, bases: Tuple[type], namespace: Dict[str, Any]):
    super().__init__(name, bases, namespace)
    if hasattr(self, 'name') and isinstance(self.name, str):
      EventConfiguration._concrete_classes[self.name] = self

class Cron(FlowStyleString, EventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'cron'
  def __init__(self, info: str):
    super().__init__(info)

class __StringListEventConfiguration(StringSequence, EventConfiguration):
  def __init__(self, info: List[str]):
    super().__init__(info)

class ActivityTypes(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'types'

class Branches(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'branches'

class BranchesIgnore(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'branches-ignore'

class Paths(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'paths'

class PathsIgnore(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'paths-ignore'

class Tags(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'tags'

class TagsIgnore(__StringListEventConfiguration, metaclass=ConcreteEventConfigurationType):
  name: str = 'tags-ignore'


