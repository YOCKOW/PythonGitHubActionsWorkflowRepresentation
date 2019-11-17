from workflow.string import Line, Lines
from textwrap import dedent
import unittest

class StringLinesTests(unittest.TestCase):
  def test_line(self):
    line = Line("some line")
    self.assertEqual(str(line), "some line\n")

    line.shift_right()
    self.assertEqual(str(line), "  some line\n")

    line.shift_left()
    self.assertEqual(str(line), "some line\n")

    line += " was modified."
    self.assertEqual(str(line), "some line was modified.\n")

  def test_lines(self):
    lines = Lines(dedent("""\
    line 0
    line 1
    line 2
    line 3
    line 4
    """))
    self.assertEqual(lines.count, 5)

    lines.shift_right(range=range(2,4))
    self.assertEqual(str(lines), dedent("""\
    line 0
    line 1
      line 2
      line 3
    line 4
    """))
