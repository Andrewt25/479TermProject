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
    for idx, compartor in enumerate(node.comparators):
      if not isinstance(compartor, ast.Attribute) \
        or get_node_hash(compartor) != self.variable:
        return

      self.locations.append((node.lineno, node.col_offset, idx, node))
