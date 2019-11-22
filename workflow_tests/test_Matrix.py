from workflow.Matrix import Matrix
from textwrap import dedent
from unittest import TestCase

class MatrixTests(TestCase):
  def test_matrix(self):
    matrix = Matrix({
      'os': ["macos-latest", "windows-latest", "ubuntu-18.04"],
      'node': [4, 6, 8, 10],
      'include': [
        {
          'os': "windows-latest",
          'node': 4,
          'npm': 2,
        }
      ],
    })
    self.assertEqual(matrix.yaml(), dedent("""\
      node:
        - 4
        - 6
        - 8
        - 10
      os:
        - macos-latest
        - windows-latest
        - ubuntu-18.04
      include:
        - node: 4
          npm: 2
          os: windows-latest
    """))