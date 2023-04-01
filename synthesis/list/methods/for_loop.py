import ast
from synthesis.util import *
from synthesis.datatypes import *


def program_synthesis_for_loop(my_dict: dict):
  for key, value in my_dict.items():
    for _ in range(value):
      yield key


class ForVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = { DataType.Set }

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node

    add_import(node, 'from synthesis.list.methods.for_loop import *')
    return self.generic_visit(node)

  def visit_For(self, node: ast.For):
    if get_node_hash(node.iter) != self.valid_var:
      return node
    
    var = get_attr_variable(node.iter)
    node.iter = ast.parse(f'program_synthesis_for_loop({var})').body[0].value
    return node
