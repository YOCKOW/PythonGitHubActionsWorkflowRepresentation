from workflow.MappingNode import MappingNode, FlowStyleMapping
from workflow.SequenceNode import SequenceNode, FlowStyleSequence
from workflow.StringNode import StringNode, FlowStyleString
from textwrap import dedent
import unittest

class MappingTests(unittest.TestCase):
  def test_mapping_node(self):
    node = MappingNode({
      "key0": StringNode("string"),
      "key1": SequenceNode([
        StringNode("item0"),
        StringNode("item1")
      ]),
      "key2": MappingNode({
        "nested0": StringNode("value0"),
        "nested1": StringNode("value1")
      })
    })
    self.assertEqual(str(node.yaml()), dedent("""\
      key0: string
      key1:
        - item0
        - item1
      key2:
        nested0: value0
        nested1: value1
    """))

  def test_flow_style_mapping(self):
    node = FlowStyleMapping({
      "outer": FlowStyleMapping({
        "inner": FlowStyleSequence([FlowStyleString('item0'), FlowStyleString('item1')])
      })
    })
    self.assertEqual(str(node.yaml()).rstrip("\n"), '{outer: {inner: [item0, item1]}}')

  def test_key_order(self):
    node = FlowStyleMapping({"key0": FlowStyleString("value0"), "key1": FlowStyleString("value1")})
    node.key_order = ['key1', 'key0']
    self.assertEqual(node.yaml(), "{key1: value1, key0: value0}")

