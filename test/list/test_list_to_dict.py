import ast
import unittest
from synthesis.datatypes import *
from synthesis.list.list import *

class TestUtil(unittest.TestCase):

  def setUp(self):
    filename = 'test/list/example.py'
    with open(filename) as f:
      tree = ast.parse(f.read(), filename=filename)
    # print(ast.dump(tree, indent=2))
    print('##### Before:')
    print(ast.unparse(tree))
    self.list = ListTo(tree, DataType.Dict)
    print('\n##### After:')
    print(ast.unparse(self.list.modify_ast()))

  def test(self):
    pass


if __name__ == '__main__':
  unittest.main()