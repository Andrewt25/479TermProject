import ast
import unittest
from synthesis.list.list_to_dict import *

class TestUtil(unittest.TestCase):

  def setUp(self):
    filename = 'test/list/list_to_dict_output.py'
    with open(filename) as f:
      tree = ast.parse(f.read(), filename=filename)
    # print(ast.dump(tree, indent=2))
    self.list_to_dict = ListToDict(tree)

  def test(self):
    pass


if __name__ == '__main__':
  unittest.main()