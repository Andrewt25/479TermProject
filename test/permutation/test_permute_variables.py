import ast
import unittest
from synthesis.datatypes import *
from synthesis.permutation.permute_variables import *
from test.util import *

class TestPermuteVariables(unittest.TestCase):

  def setUp(self):
    filename = 'test/permutation/input.py'
    with open(filename) as f:
      self.input_tree = ast.parse(f.read(), filename=filename)
    self.permute_variables = PermuteVariables(self.input_tree)

  def test_permutation(self):
    filenames = [
      'test/permutation/output_0.py',
      'test/permutation/output_1.py',
      'test/permutation/output_2.py',
      'test/permutation/output_3.py',
      'test/permutation/output_4.py',
      'test/permutation/output_5.py',
      'test/permutation/output_6.py',
    ]
    expected_output_tree = get_expected_output_trees(filenames)

    for output_tree in self.permute_variables.modify_ast():
      self.assertTrue(ast.dump(output_tree) in expected_output_tree)

if __name__ == '__main__':
  unittest.main()