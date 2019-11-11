from workflow.SequenceNode import SequenceNode, FlowStyleSequence
from workflow.StringNode import StringNode, FlowStyleString
from workflow.util import indent
from textwrap import dedent
import unittest

class SequenceTests(unittest.TestCase):
  def test_sequence_node(self):
    strings = [StringNode("string0"), StringNode("line1\nline2"), StringNode("last")]
    seq = SequenceNode(strings)
    self.assertEqual(seq.yaml_string() + "\n", dedent("""\
      - string0
      - |
          line1
          line2
      - last
    """))

  def test_flow_style_sequence(self):
    strings = [FlowStyleString("item0"), FlowStyleString("item1"), FlowStyleString("item2")]
    seq = FlowStyleSequence(strings)
    self.assertEqual(seq.yaml_string(), "[item0, item1, item2]")
