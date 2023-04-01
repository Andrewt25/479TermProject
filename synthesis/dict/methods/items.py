import ast
from synthesis.util import *
from synthesis.datatypes import *


class ItemsVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Call(self, node: ast.Call):
    if not isinstance(node.func, ast.Attribute) \
      or get_node_hash(node.func.value) != self.valid_var \
      or node.func.attr != 'items':
      return self.generic_visit(node)
  
    var = get_attr_variable(node.func.value)
    new_node = ast.parse(f'{var}').body[0].value
    return self.generic_visit(new_node)
