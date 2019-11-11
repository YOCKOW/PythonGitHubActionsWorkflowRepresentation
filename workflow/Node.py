import io
import os
import re
from typing import Any, List, IO, Optional, Union

class Node:
  """
  An abstract class that represents Workflow's Node.
  """

  def yaml_lines(self) -> List[str]:
    raise RuntimeError("This method must be overridden.")

  def yaml_string(self) -> str:
    # Remove empty lines
    return "\n".join(filter(lambda line: not re.match(r'^\s*$', line), self.yaml_lines()))

  def dump_yaml_string(self, file: Union[os.PathLike, IO[Any]]) -> None:
    # Write YAML to `file`.
    file_handle: Optional[IO[Any]] = None
    should_close: bool = False
    if isinstance(file, io.IOBase):
      file_handle = file
    elif isinstance(file, os.PathLike):
      file_handle = open(file, 'w')
      should_close = True
    else:
      raise ValueError("`file` must be an instance of `PathLike` or `IO`.")

    file_handle.write(self.yaml_string())

    if should_close:
      file_handle.close()


