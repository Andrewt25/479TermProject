'''
ListComp(
  elt=Name(id='item', ctx=Load()),
  generators=[
    comprehension(
      target=Name(id='item', ctx=Store()),
      iter=Attribute(
        value=Name(id='self', ctx=Load()),
        attr='list',
        ctx=Load()),
      ifs=[],
      is_async=0)])),
'''
import ast
from synthesis.util import *


class ListCompVisitor(ast.NodeVisitor):
  
  def __init__(self, variable: str) -> None:
    self.variable = variable
    self.locations = list()

  def visit_ListComp(self, node: ast.ListComp):
    if len(node.generators) == 0:
      return

    for idx, generator in enumerate(node.generators):
      if not isinstance(generator, ast.comprehension) \
        or get_node_hash(generator.iter) != self.variable:
        return

      self.locations.append((node.lineno, node.col_offset, idx, node))
