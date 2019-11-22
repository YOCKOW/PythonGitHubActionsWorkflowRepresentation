from workflow.EnvironmentVariables import EnvironmentVariables
from textwrap import dedent
from unittest import TestCase

class EnvironmentVariablesTests(TestCase):
  def test_env(self):
    env = EnvironmentVariables({'MY_NAME': 'TARO', 'YOUR_NAME': 'JIRO'})
    self.assertEqual(env.yaml(), dedent("""\
      MY_NAME: TARO
      YOUR_NAME: JIRO
    """))
    