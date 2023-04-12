'''
Compare(
  left=Name(id='item', ctx=Load()),
  ops=[
    In()],
  comparators=[
    Attribute(
      value=Name(id='self', ctx=Load()),
      attr='list',
      ctx=Load())]))],
'''
import ast
from synthesis.util import *


class CompareVisitor(ast.NodeVisitor):
  
  def __init__(self, variable: str) -> None:
    self.variable = variable
    self.locations = list()

  def visit_Compare(self, node: ast.Compare):
    if not isinstance(node.comparators[0], ast.Attribute) \
      or get_node_hash(node.comparators[0]) != self.variable:
      return

    self.locations.append((node.lineno, node.col_offset, node))

