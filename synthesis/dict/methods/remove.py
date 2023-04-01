import ast
from synthesis.util import *
from synthesis.datatypes import *


def program_synthesis_remove(my_list: list, key):
  for idx, k, _ in enumerate(my_list):
    if k == key: # key is unique
      del my_list[idx]
      break


class RemoveVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.remove import *')
    return self.generic_visit(node)

  def visit_Delete(self, node: ast.Delete):
    if not isinstance(node.targets[0], ast.Subscript) \
      or get_node_hash(node.targets[0].value) != self.valid_var:
      return node

    var = get_attr_variable(node.targets[0].value)
    key = node.targets[0].slice.id
    return ast.parse(f'program_synthesis_remove({var}, {key})').body[0]



