import ast
from synthesis.util import *
from synthesis.datatypes import *


def program_synthesis_remove(my_dict: dict, item):
  if item not in my_dict:
    raise Exception(f'{item} does not exist in {my_dict}.')
  my_dict[item] -= 1
  if my_dict[item] == 0:
    del my_dict[item]


def program_synthesis_remove(my_set: set, item):
  if item not in my_set:
    raise Exception(f'{item} does not exists in {my_set}.')
  my_set.remove(item)

def program_synthesis_remove(my_collection, item):
  collectionType = my_collection.__class__
  if(collectionType == dict):
    if item not in my_collection:
        raise Exception(f'{item} does not exist in {my_collection}.')
    my_collection[item] -= 1
    if my_collection[item] == 0:
      del my_collection[item]
  elif(collectionType == set):
    if item not in my_collection:
      raise Exception(f'{item} does not exists in {my_collection}.')
    my_collection.remove(item)


class RemoveVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.list.methods.remove import *')
    return self.generic_visit(node)

  def visit_Expr(self, node: ast.Expr):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Attribute):
      return node
    
    if node.value.func.attr == 'remove' \
      and get_node_hash(node.value.func.value) == self.valid_var:

      var = get_attr_variable(node.value.func.value)
      item = get_args(node.value.args)[0]

      return ast.parse(f'program_synthesis_remove({var}, {item})').body[0]

    return node