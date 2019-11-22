from workflow.EventConfigurations import EventConfiguration
from textwrap import dedent
import unittest

class EventConfigurationsTests(unittest.TestCase):
  def test_branches(self):
    branches = EventConfiguration.configuration('branches', ['master', 'development'])
    self.assertEqual(branches.yaml(), dedent("""\
      - master
      - development
    """))