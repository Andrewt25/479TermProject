import ast
from synthesis.util import *
from synthesis.datatypes import *


def program_synthesis_add(my_list: list, key, value):
  my_list.append((key, value))


class AddVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.dict.methods.add import *')
    return self.generic_visit(node)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.targets[0], ast.Subscript) \
      or get_node_hash(node.targets[0].value) != self.valid_var:
      return node

    var = get_attr_variable(node.targets[0].value)
    key = node.targets[0].slice.id
    value = ast.unparse(node.value)
    return ast.parse(f'program_synthesis_add({var}, {key}, {value})').body[0]
