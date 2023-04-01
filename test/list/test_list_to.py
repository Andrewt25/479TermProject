import ast
import unittest
from synthesis.datatypes import *
from synthesis.list.list import *
from test.util import *

class TestListTo(unittest.TestCase):

  def setUp(self):
    filename = 'test/list/example.py'
    with open(filename) as f:
      self.input_tree = ast.parse(f.read(), filename=filename)

  def test_dict(self):
    filenames = ['test/list/output_dict_0.py', 'test/list/output_dict_1.py']
    expected_output_tree = get_expected_output_trees(filenames)

    list_to = ListTo(self.input_tree, DataType.Dict)
    trees = list_to.modify_ast()
    for output_tree in trees:
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)

  def test_set(self):
    filenames = ['test/list/output_set_0.py', 'test/list/output_set_1.py']
    expected_output_tree = get_expected_output_trees(filenames)

    list_to = ListTo(self.input_tree, DataType.Set)
    trees = list_to.modify_ast()
    for output_tree in trees:
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)


if __name__ == '__main__':
  unittest.main()