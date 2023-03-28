import ast
import sys
import os

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path)))))

from synthesis.util import *


def program_synthesis_for_loop(my_dict: dict):
  for key, value in my_dict.items():
    for i in range(value):
      yield key


def program_synthesis_for_loop(my_set: set):
  return my_set


class ForVisitor(ast.NodeTransformer):

  def __init__(self, valid_var):
    self.valid_var = valid_var
    self.import_count = ast.parse('from synthesis.list.methods.for_loop import *').body[0]

  def visit_Module(self, node: ast.Module):
    for body in node.body:
      if isinstance(body, ast.ClassDef):
        node.body.insert(0, self.import_count)
        return self.generic_visit(node)
      
      if is_ast_node_equal(body, self.import_count):
        break
    
    return self.generic_visit(node)

  def visit_For(self, node: ast.For):
    if get_node_hash(node.iter) != self.valid_var:
      return node
    
    var = get_attr_variable(node.iter)
    node.iter = ast.parse(f'program_synthesis_for_loop({var})').body[0].value
    return node
