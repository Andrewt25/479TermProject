import ast
from synthesis.util import *
from synthesis.datatypes import *


def psynth_dict_to_list_get(my_list: list, key):
  for k, v in my_list:
    if k == key: # key is unique
      return v


class GetVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.get import *')
    return self.generic_visit(node)

  def visit_Call(self, node: ast.Call):
    if not isinstance(node.func, ast.Attribute) \
      or get_node_hash(node.func.value) != self.valid_var \
      or node.func.attr != 'get':
      return self.generic_visit(node)
  
    var = get_attr_variable(node.func.value)
    key = node.args[0].id
    new_node = ast.parse(f'psynth_dict_to_list_get({var}, {key})').body[0].value
    return self.generic_visit(new_node)

  def visit_Subscript(self, node: ast.Subscript):
    if not isinstance(node.value, ast.Attribute) \
      or get_node_hash(node.value) != self.valid_var:
      return self.generic_visit(node)

    var = get_attr_variable(node.value)
    key = node.slice.id
    new_node = ast.parse(f'psynth_dict_to_list_get({var}, {key})').body[0].value
    return self.generic_visit(new_node)