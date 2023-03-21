import ast
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from synthesis.util import *


def append(my_dict: dict, item):
  if item in my_dict:
    my_dict[item] += 1
  else:
    my_dict[item] = 0


def append(my_set: set, item):
  if item in my_set:
    raise Exception(f'{item} already exists in {my_set}.')
  my_set.add(item)


class AppendVisitor(ast.NodeTransformer):

  def __init__(self, valid_vars):
    self.valid_vars = valid_vars
    self.import_append = ast.parse('from synthesis.list.methods.append import *').body[0]

  def visit_Module(self, node: ast.Module):
    for body in node.body:
      if isinstance(body, ast.ClassDef):
        node.body.insert(0, self.import_append)
        return self.generic_visit(node)
      
      if is_ast_node_equal(body, self.import_append):
        break
    
    return self.generic_visit(node)

  def visit_Expr(self, node: ast.Expr):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Attribute):
      return node
    
    if node.value.func.attr == 'append' \
      and get_node_hash(node.value.func.value) in self.valid_vars:

      if isinstance(node.value.func.value, ast.Name):
        var = node.value.func.value.id
      else:
        var = 'self.' + node.value.func.value.attr

      if isinstance(node.value.args[0], ast.Constant):
        item = node.value.args[0].value
      if isinstance(node.value.args[0], ast.Name):
        item = node.value.args[0].id

      return ast.parse(f'append({var}, {item})').body[0]

    return node