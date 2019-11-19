from workflow.Events import Event
from textwrap import dedent
import unittest

class EventsTests(unittest.TestCase):
  def test_check_run(self):
    check_run_0 = Event.event('check_run')
    self.assertEqual(check_run_0.yaml(), "check_run")

    check_run_1 = Event.event('check_run', {'types': ['created', 'rerequested', 'completed', 'requested_action']})
    self.assertEqual(check_run_1.yaml(), dedent("""\
    types:
      - created
      - rerequested
      - completed
      - requested_action
    """), check_run_1.yaml())
