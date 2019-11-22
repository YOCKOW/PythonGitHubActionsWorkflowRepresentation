from workflow.Step import Step
from textwrap import dedent
from unittest import TestCase

class StepTests(TestCase):
  def test_step(self):
    step = Step({
      'name': "Step Name",
      'env': {
        'NAME': 'VALUE'
      },
      'run': "echo $NAME\necho finished",
      'continue-on-error': True,
      'timeout-minutes': 5,
    })
    self.assertEqual(step.yaml(), dedent("""\
      name: Step Name
      env:
        NAME: VALUE
      run: |
        echo $NAME
        echo finished
      continue-on-error: true
      timeout-minutes: 5
    """), step.yaml().__str__())