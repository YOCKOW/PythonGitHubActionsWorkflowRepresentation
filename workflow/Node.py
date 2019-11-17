import io
import os
import re
from typing import Any, List, IO, Optional, Union, overload
from .string import Lines

class Node:
  """
  An abstract class that represents Workflow's Node.
  """
  
  def yaml(self) -> Lines:
    raise NotImplementedError("This method must be overridden.")

  @overload
  def dump_yaml(self, output: os.PathLike): raise NotImplementedError()

  @overload
  def dump_yaml(self, output: IO[Any]): raise NotImplementedError()

  def dump_yaml(self, output):
    # Write YAML to `file`.
    file_handle: IO[Any]
    should_close: bool = False
    if isinstance(output, io.IOBase):
      file_handle = output
    elif isinstance(output, os.PathLike):
      file_handle = open(output, 'w')
      should_close = True
    else:
      raise ValueError("`file` must be an instance of `PathLike` or `IO`.")

    lines: Lines = self.yaml()
    lines.remove_empty_lines()
    file_handle.write(str(lines))

    if should_close:
      file_handle.close()

  @property
  def is_flow_style(self) -> bool: return False

class FlowStyleNode(Node):
  @property
  def is_flow_style(self) -> bool: return True
