'''
For(
  target=Name(id='item', ctx=Store()),
  iter=Attribute(
    value=Name(id='self', ctx=Load()),
    attr='list',
    ctx=Load()),
'''
import ast
from synthesis.util import *


class ForLoopVisitor(ast.NodeVisitor):
  
  def __init__(self, variable: str) -> None:
    self.variable = variable
    self.locations = list()

  def visit_For(self, node: ast.For):
    if not isinstance(node.iter, ast.Attribute) \
      or get_node_hash(node.iter) != self.variable:
      return

    self.locations.append((node.lineno, node.col_offset, node))