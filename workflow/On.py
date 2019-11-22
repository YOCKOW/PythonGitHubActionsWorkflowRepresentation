from .Node import Node
from .Events import Event
from .MappingNode import MappingNode
from .SequenceNode import SequenceNode
from .string import Lines
from typing import Any, Dict, List, cast, overload

class On(Node):
  @overload
  def __init__(self, info: str): raise NotImplementedError()

  @overload
  def __init__(self, info: List[str]): raise NotImplementedError()

  @overload
  def __init__(self, info: Dict[str, Any]): raise NotImplementedError()

  def __init__(self, info):
    events = info
    if isinstance(events, str):
      self.__payload = Event.event(events)
    elif isinstance(events, list):
      self.__payload = SequenceNode(list(map(lambda event: cast(Node, Event.event(event)), events)))
    elif isinstance(events, dict):
      events_dict: Dict[str, Node] = {}
      for key, info in events.items():
        assert isinstance(info, dict)
        events_dict[key] = Event.event(key, info)
      self.__payload = MappingNode(events_dict)
      self.__payload.key_order = ['push', 'pull_request'] # What's the best...?
    else:
      raise ValueError("Unexpected Events Data")

  def yaml(self) -> Lines:
    return self.__payload.yaml()