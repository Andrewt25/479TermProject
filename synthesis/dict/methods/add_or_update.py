import ast
from synthesis.util import *
from synthesis.datatypes import *


def psynth_dict_to_list_add_or_update(my_list: list, key, value):
  if len(my_list) != 0:
    for idx, item in enumerate(my_list):
      k, _ = item
      if k == key:
        my_list[idx] = (key, value)
        return
  
  my_list.append((key, value)) # If key does not exist



class AddOrUpdateVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.add_or_update import *')
    return self.generic_visit(node)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.targets[0], ast.Subscript) \
      or get_node_hash(node.targets[0].value) != self.valid_var:
      return node

    var = get_attr_variable(node.targets[0].value)
    key = node.targets[0].slice.id
    value = ast.unparse(node.value)
    return ast.parse(f'psynth_dict_to_list_add_or_update({var}, {key}, {value})').body[0]
