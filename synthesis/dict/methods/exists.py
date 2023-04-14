import ast
from synthesis.util import *
from synthesis.datatypes import *


def psynth_dict_to_list_exists(my_list: list, key):
  for k, _ in my_list:
    if k == key:
      return True
  return False


class ExistsVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.exists import *')
    return self.generic_visit(node)

  def visit_Compare(self, node: ast.Compare):
    if isinstance(node.ops[0], ast.In) \
      and isinstance(node.comparators[0], ast.Attribute) \
      and get_node_hash(node.comparators[0]) == self.valid_var:
        var = get_attr_variable(node.comparators[0])
        key = get_value(node.left)
        new_node = ast.parse(f'psynth_dict_to_list_exists({var}, {key})').body[0].value
        return self.generic_visit(new_node)

    return self.generic_visit(node)
