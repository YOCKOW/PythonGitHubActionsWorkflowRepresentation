from workflow.Branches_Tags import Branches, Tags
from io import StringIO
from textwrap import dedent
import unittest

class BranchesTagsTests(unittest.TestCase):
  def test_branches(self):
    branches = Branches(["master", "development"])
    self.assertEqual(str(branches.yaml()), dedent("""\
      - master
      - development
    """))

  def test_tags(self):
    tags = Tags(["*", "!no-tests/**"])
    self.assertEqual(str(tags.yaml()), dedent("""\
      - "*"
      - "!no-tests/**"
    """))
