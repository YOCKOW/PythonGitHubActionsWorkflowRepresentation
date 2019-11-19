from workflow.On import On
import unittest
from textwrap import dedent

class OnTests(unittest.TestCase):
  def test_on(self):
    simple_on = On('push')
    self.assertEqual(simple_on.yaml(), "push")

    list_on = On(['push', 'pull_request'])
    self.assertEqual(list_on.yaml(), dedent("""\
      - push
      - pull_request
    """))

    complex_on = On({
      'push': {
        'branches': ['master', 'development']
      },
      'pull_request': {
        'branches': ['*']
      }
    })
    self.assertEqual(complex_on.yaml(), dedent("""\
      push:
        branches:
          - master
          - development
      pull_request:
        branches:
          - "*"
    """))