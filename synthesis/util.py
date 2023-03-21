import ast
from .datatypes import *


def get_data_type_str(data_type: DataType):
  match(data_type):
    case DataType.List:
      return 'list'
    case DataType.Dict:
      return 'dict'
    case DataType.Set:
      return 'set'


def is_ast_node_equal(ast_node_a, ast_node_b):
  node_a = ast.dump(ast_node_a)
  node_b = ast.dump(ast_node_b)
  return node_a == node_b 


def get_node_hash(node: ast):
  node_str = ast.dump(node)
  return ','.join(node_str.split(',')[:-1])


class FindVariableDeclarations(ast.NodeVisitor):

  def __init__(self, data_type: DataType):
    self.variables = set()
    self.data_type = get_data_type_str(data_type)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.value, ast.Call):
      return
    
    if node.value.func.id != self.data_type:
      return

    self.variables.add(get_node_hash(node.targets[0]))


class VariableTransformer(ast.NodeTransformer):

  def __init__(self, variables, from_type: DataType, to_type: DataType):
    self.variables = variables
    self.from_type = get_data_type_str(from_type)
    self.to_type = get_data_type_str(to_type)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.value, ast.Call):
      return node
    
    if node.value.func.id != self.from_type:
      return node
    
    node.value.func.id = self.to_type
    return node