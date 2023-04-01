import ast
from synthesis.util import *
from synthesis.datatypes import *


def psynth_dict_to_list_values(my_list: list):
  for _, v in my_list:
    yield v


class ValuesVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.values import *')
    return self.generic_visit(node)

  def visit_Call(self, node: ast.Call):
    if not isinstance(node.func, ast.Attribute) \
      or get_node_hash(node.func.value) != self.valid_var \
      or node.func.attr != 'values':
      return self.generic_visit(node)
  
    var = get_attr_variable(node.func.value)
    new_node = ast.parse(f'psynth_dict_to_list_values({var})').body[0].value
    return self.generic_visit(new_node)
