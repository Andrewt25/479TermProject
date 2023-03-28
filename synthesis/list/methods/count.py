import ast
import sys
import os

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path)))))

from synthesis.util import *


def program_synthesis_count(my_dict: dict, item):
  return my_dict[item] if item in my_dict else 0


def program_synthesis_count(my_set: set, item):
  return 1 if item in my_set else 0


class CountVisitor(ast.NodeTransformer):

  def __init__(self, valid_var):
    self.valid_var = valid_var
    self.import_count = ast.parse('from synthesis.list.methods.count import *').body[0]

  def visit_Module(self, node: ast.Module):
    for body in node.body:
      if isinstance(body, ast.ClassDef):
        node.body.insert(0, self.import_count)
        return self.generic_visit(node)
      
      if is_ast_node_equal(body, self.import_count):
        break
    
    return self.generic_visit(node)

  def visit_Expr(self, node: ast.Expr):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Attribute):
      return node
    
    if node.value.func.attr == 'count' \
      and get_node_hash(node.value.func.value) == self.valid_var:

      var = get_attr_variable(node.value.func.value)
      item = get_args(node.value.args)[0]

      return ast.parse(f'program_synthesis_count({var}, {item})').body[0]

    return node