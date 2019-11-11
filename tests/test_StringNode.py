from workflow.StringNode import StringNode, FlowStyleString
from workflow.util import indent
import unittest

class StringNodeTests(unittest.TestCase):
  def test_string_node(self):
    node1 = StringNode("string")
    self.assertEqual(node1.yaml_string(), "string")

    node2 = StringNode("line1\nline2")
    self.assertEqual(node2.yaml_string(), f"|\n{indent(1)}line1\n{indent(1)}line2")

  def test_flow_style_string(self):
    node = FlowStyleString("line1\nline2\n")
    self.assertEqual(node.yaml_string(), "\"line1\\nline2\\n\"")