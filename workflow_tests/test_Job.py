from workflow.Job import Job
from textwrap import dedent
from unittest import TestCase

class JobTests(TestCase):
  def test_job(self):
    job = Job({
      'name': 'My Job',
      'needs': ['your-job', 'her-job'],
      'runs-on': 'macOS-latest',
      'steps':[
        {
          'name': 'My First Step',
          'run': "echo Hello"
        }
      ]
    })
    self.assertEqual(job.yaml(), dedent("""\
      name: My Job
      needs:
        - your-job
        - her-job
      runs-on: macOS-latest
      steps:
        - name: My First Step
          run: echo Hello
    """))