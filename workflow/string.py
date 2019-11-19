import builtins
from copy import copy, deepcopy
from typing import Any, Dict, Iterable, Iterator, List, Optional, overload

class Line:
  """ Represents a single line string. """

  def __init__(self, string: str, indent_level: int = 0):
    line = string.strip("\n")
    assert "\n" not in line, "`string` must be a single line."
    self.__line = line
    self.__indent_level = indent_level

  def __copy__(self) -> 'Line':
    return Line(self.__line, indent_level=self.__indent_level)

  def __deepcopy__(self, _: Dict[Any, Any]) -> 'Line':
    return self.__copy__()

  @overload
  def __iadd__(self, other: str) -> 'Line': raise NotImplementedError()

  @overload
  def __iadd__(self, other: 'Line') -> 'Line': raise NotImplementedError()

  def __iadd__(self, other) -> 'Line':
    if isinstance(other, str):
      self += Line(other)
    elif isinstance(other, Line):
      self.__line += other.raw_string
    return self

  def __eq__(self, other) -> bool:
    if other is None:
      return False
    if isinstance(other, Line):
      return self.indent_level == other.indent_level and self.raw_string == other.raw_string
    if isinstance(other, str):
      return str(self).rstrip("\n") == other.rstrip("\n")
    return False

  def __ne__(self, other) -> bool:
    return not (self == other)

  def __str__(self) -> str:
    return Lines.indent(self.__indent_level) + self.__line + "\n"

  @property
  def indent_level(self) -> int:
    return self.__indent_level

  @property
  def is_empty(self) -> bool:
    return len(self.__line) == 0

  def __shift(self, level: int) -> None:
    self.__indent_level += level
    if self.__indent_level < 0: self.__indent_level = 0

  def shift_left(self, decreases: int = 1) -> None:
    self.__shift(-decreases)

  def shift_right(self, increases: int = 1) -> None:
    self.__shift(increases)

  @property
  def raw_string(self) -> str:
    return self.__line

class Lines:
  """ Represents multiple lines of string. """

  INDENT_WIDTH: int = 2

  @staticmethod
  def indent(indent_level: int) -> str:
    return " " * (indent_level * Lines.INDENT_WIDTH)

  @overload
  def __init__(self, lines: Optional[str]): raise NotImplementedError()

  @overload
  def __init__(self, lines: Optional[Iterable[Line]]): raise NotImplementedError()

  def __init__(self, lines = None):
    if lines is None:
      self.__lines: List[Line] = []
    elif isinstance(lines, str):
      self.__lines: List[Line] = list(map(lambda line_string: Line(line_string), lines.splitlines()))
    else:
      try:
        _ = iter(lines)
      except TypeError:
        raise ValueError("`lines` must be a `str` or an iterable object whose element is `Line`.")
      else:
        self.__lines: List[Line] = []
        for line in lines:
          assert isinstance(line, Line)
          self.__lines.append(line)

  def __copy__(self) -> 'Lines':
    return Lines(self.__lines)
  
  def __deepcopy__(self, _: Dict[Any, Any]) -> 'Lines':
    lines: List[Line] = []
    for line in self.__lines:
      lines.append(deepcopy(line))
    return Lines(lines)

  def __eq__(self, other) -> bool:
    if other is None: 
      return False
    if isinstance(other, Lines):
      if self.count != other.count:
        return False
      for ii in range(0, self.count):
        if self[ii] != other[ii]: return False
      return True
    if isinstance(other, str):
      return str(self).rstrip("\n") == other.rstrip("\n")
    return False

  def __ne__(self, other) -> bool:
    return not (self == other)

  def __iter__(self) -> Iterator[Line]:
    return iter(self.__lines)

  def __str__(self) -> str:
    return ''.join(map(lambda line: str(line), self.__lines))

  @overload
  def __getitem__(self, subscript: slice) -> Line: raise NotImplementedError()

  @overload
  def __getitem__ (self, subscript: int) -> Line: raise NotImplementedError()

  def __getitem__(self, subscript) -> Line:
    return self.__lines[subscript]

  @overload
  def __setitem___(self, index: int, line: str): raise NotImplementedError()
  
  @overload
  def __setitem__(self, index: int, line: Line): raise NotImplementedError()

  def __setitem__(self, index: int, line):
    if isinstance(line, str):
      self.__lines[index] = Line(line)
    elif isinstance(line, Line):
      self.__lines[index] = line
    else:
      raise ValueError("Unexpected value for line.")

  def append(self, line):
    self.insert(self.count, line)

  @property
  def count(self) -> int:
    return len(self.__lines)

  def extend(self, lines: Iterable[Line]):
    self.__lines.extend(lines)

  @overload
  def insert(self, index: int, line: str): raise NotImplementedError()

  @overload
  def insert(self, index: int, line: Line): raise NotImplementedError()

  def insert(self, index: int, line):
    if isinstance(line, str):
      self.__lines.insert(index, Line(line))
    elif isinstance(line, Line):
      self.__lines.insert(index, copy(line))
    else:
      raise ValueError("Unexpected value for line.")

  def remove_empty_lines(self):
    self.__lines = list(filter(lambda line: not line.is_empty, self.__lines))

  def __range(self, maybeRange: Optional[range]) -> range:
    return maybeRange if maybeRange is not None else range(0, self.count)

  def shift_left(self, decreases: int = 1, range: Optional[range] = None):
    for ii in self.__range(range):
      self.__lines[ii].shift_left(decreases)

  def shift_right(self, increases: int = 1, range: Optional[range] = None):
    for ii in self.__range(range):
      self.__lines[ii].shift_right(increases)

