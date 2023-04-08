import ast
import unittest
from synthesis.datatypes import *
from synthesis.list.list import *
from test.util import *

class TestListTo(unittest.TestCase):

  def setUp(self):
    filename = 'test/list/input_list.py'
    with open(filename) as f:
      self.input_tree = ast.parse(f.read(), filename=filename)
    self.list_to = ListTo(self.input_tree)

  def test_dict(self):
    filenames = ['test/list/output_dict/output_dict_0.py', 'test/list/output_dict/output_dict_1.py']
    expected_output_tree = get_expected_output_trees(filenames)

    for output_tree in self.list_to.modify_ast(DataType.Dict):
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)

  def test_set(self):
    filenames = ['test/list/output_set/output_set_0.py', 'test/list/output_set/output_set_1.py']
    expected_output_tree = get_expected_output_trees(filenames)

    for output_tree in self.list_to.modify_ast(DataType.Set):
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)

  def test_already_modified(self):
    filename = 'test/list/input_modified_list.py'
    with open(filename) as f:
      input_tree = ast.parse(f.read(), filename=filename)
    list_to = ListTo(input_tree)

    self.assertTrue(len(list_to.modify_ast(DataType.Dict)) == 0)

if __name__ == '__main__':
  unittest.main()