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
    print(ast.dump(self.input_tree, indent=2))

  def test_list(self):
    # filenames = ['test/dict/output_dict_0.py', 'test/dict/output_dict_1.py']
    # expected_output_tree = get_expected_output_trees(filenames)

    for output_tree in self.dict_to.modify_ast(DataType.List):
      # self.assertTrue(ast.dump(output_tree) in expected_output_tree)
      print(ast.unparse(output_tree))


if __name__ == '__main__':
  unittest.main()