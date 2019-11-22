from workflow.Workflow import Workflow
from textwrap import dedent
from unittest import TestCase

class WorkflowTests(TestCase):
  def test_workflow(self):
    workflow = Workflow({
      "name": "Some Workflow",
      "on": "push", 
      "jobs": {
        "job1": {
          "name": "Some Job",
          "strategy": {
            "matrix": {
              "os": ["ubuntu-latest", "macOS-latest"],
            }
          },
          "runs-on": "${{ matrix.os }}",
          "steps": [
            {
              "name": "Some Step",
              "run": "echo Hello"
            }
          ]
        }
      }
    })

    self.assertEqual(workflow.yaml(), dedent("""\
      name: Some Workflow
      "on": push
      jobs:
        job1:
          name: Some Job
          strategy:
            matrix:
              os:
                - ubuntu-latest
                - macOS-latest
          runs-on: ${{ matrix.os }}
          steps:
            - name: Some Step
              run: echo Hello
    """), workflow.yaml())