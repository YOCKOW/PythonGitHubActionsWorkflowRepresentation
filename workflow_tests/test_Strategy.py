from workflow.Strategy import Strategy
from textwrap import dedent
from unittest import TestCase

class StrategyTests(TestCase):
  def test_strategy(self):
    strategy = Strategy({
      'fail-fast': True,
      'max-parallel': 2,
      'matrix': {
        'os': ["ubuntu-16.04", "ubuntu-18.04"],
        'node': [6, 8, 10],
      }
    })
    self.assertEqual(strategy.yaml(), dedent("""\
      fail-fast: true
      max-parallel: 2
      matrix:
        node:
          - 6
          - 8
          - 10
        os:
          - ubuntu-16.04
          - ubuntu-18.04
    """))