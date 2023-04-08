import ast
import unittest
from synthesis.datatypes import *
from synthesis.dict.dict import *
from test.util import *

class TestDictTo(unittest.TestCase):

  def setUp(self):
    filename = 'test/dict/input_dict.py'
    with open(filename) as f:
      self.input_tree = ast.parse(f.read(), filename=filename)
    self.dict_to = DictTo(self.input_tree)

  def test_list(self):
    filenames = ['test/dict/output_list.py']
    expected_output_tree = get_expected_output_trees(filenames)

    for output_tree in self.dict_to.modify_ast(DataType.List):
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)
  
  def test_already_modified(self):
    filename = 'test/dict/input_modified_dict.py'
    with open(filename) as f:
      input_tree = ast.parse(f.read(), filename=filename)
    dict_to = DictTo(input_tree)

    self.assertTrue(len(dict_to.modify_ast(DataType.List)) == 0)

if __name__ == '__main__':
  unittest.main()