import ast
from synthesis.util import *
from synthesis.datatypes import *


def psynth_list_to_dict_append(my_dict: dict, item):
  if item in my_dict:
    my_dict[item] += 1
  else:
    my_dict[item] = 1


def psynth_list_to_set_append(my_set: set, item):
  if item in my_set:
    raise Exception(f'{item} already exists in {my_set}.')
  my_set.add(item)


class AppendVisitor(ast.NodeTransformer):

  def __init__(self, valid_var, target_type: DataType):
    self.valid_var = valid_var
    self.target_type = target_type
    self.ignored_types = {}

  def visit_Module(self, node: ast.Module):
    if self.target_type in self.ignored_types:
      return node
    add_import(node, 'from synthesis.list.methods.append import *')
    return self.generic_visit(node)

  def visit_Expr(self, node: ast.Expr):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Attribute):
      return node
    
    if node.value.func.attr == 'append' \
      and get_node_hash(node.value.func.value) == self.valid_var:

      var = get_attr_variable(node.value.func.value)
      item = get_args(node.value.args)[0]

      match (self.target_type):
        case DataType.Dict:
          return ast.parse(f'psynth_list_to_dict_append({var}, {item})').body[0]
        case DataType.Set:
          return ast.parse(f'psynth_list_to_set_append({var}, {item})').body[0]

    return node