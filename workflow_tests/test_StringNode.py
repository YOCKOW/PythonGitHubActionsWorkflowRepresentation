from workflow.string import Lines
from workflow.StringNode import StringNode, FlowStyleString
import unittest

class StringNodeTests(unittest.TestCase):
  def test_string_node(self):
    node1 = StringNode("string")
    self.assertEqual(str(node1.yaml()).rstrip("\n"), "string")

    node2 = StringNode("line1\nline2")
    self.assertEqual(str(node2.yaml()).rstrip("\n"), f"|\n{Lines.indent(1)}line1\n{Lines.indent(1)}line2")

  def test_flow_style_string(self):
    node = FlowStyleString("line1\nline2\n")
    self.assertEqual(str(node.yaml()).rstrip("\n"), "\"line1\\nline2\\n\"")