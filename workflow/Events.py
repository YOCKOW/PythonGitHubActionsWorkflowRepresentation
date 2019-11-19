from .EventConfigurations import EventConfiguration
from .Node import Node
from .MappingNode import MappingNode
from .StringNode import FlowStyleString
from .string import Lines
from typing import Any, Dict, Optional, Tuple, Type

# TODO: Validate configurations of each event.

class Event(Node):
  name: str = NotImplemented
  _concrete_classes: Dict[str, Type['Event']] = {}

  @staticmethod
  def event(name: str, info: Optional[Dict[str, Any]] = None) -> 'Event':
    the_class = Event._concrete_classes.get(name, None)
    if the_class is None:
      raise RuntimeError(f"`{name}` is unsupported/unimplemented yet.")
    assert the_class.name == name
    return the_class(info)
  
  def __init__(self, info: Optional[Dict[str, Any]]):
    if info is None:
      self.__payload = FlowStyleString(type(self).name)
    elif isinstance(info, dict):
      configurations: Dict[str, Node] = {}
      for key, value in info.items():
        configurations[key] = EventConfiguration.configuration(key, value)
      self.__payload = MappingNode(configurations)

  def yaml(self) -> Lines:
    return self.__payload.yaml()

class ConcreteEventType(type):
  """ Metaclass for concrete `Event` classes. """
  def __init__(self: Type[Event], name: str, bases: Tuple[type], namespace: Dict[str, Any]):
    super().__init__(name, bases, namespace)
    if hasattr(self, 'name') and isinstance(self.name, str):
      Event._concrete_classes[self.name] = self

class WebhookEvent(Event): pass

class CheckRunEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'check_run'

class CheckSuiteEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'check_suite'

class CreateEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'create'

class DeleteEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'delete'

class DeploymentEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'deployment'

class DeploymentStatusEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'deployment_status'

class ForkEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'fork'

class GollumEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'gollum'

class IssueCommentEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'issue_comment'

class IssuesEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'issues'

class LabelEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'label'

class MemberEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'member'

class MilestoneEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'milestone'

class PageBuildEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'page_build'

class ProjectEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'project'

class ProjectCardEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'project_card'

class ProjectColumnEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'project_column'

class PublicEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'public'

class PullRequestEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'pull_request'

class PullRequestReviewEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'pull_request_review'

class PullRequestReviewCommentEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'pull_request_review_comment'

class PushEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'push'

class ReleaseEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'release'

class StatusEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'status'

class WatchEvent(WebhookEvent, metaclass=ConcreteEventType):
  name: str = 'watch'


##### non-webhook event #####

class ScheduleEvent(Event, metaclass=ConcreteEventType):
  name: str = 'schecule'

class RepositoryDispatchEvent(Event, metaclass=ConcreteEventType):
  name: str = 'repository_dispatch'