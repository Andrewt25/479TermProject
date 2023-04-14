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


def get_attr_variable(attribute: ast.Attribute):
  match type(attribute):
    case ast.Name:
      return attribute.id
    case ast.Attribute:
      return f'self.{attribute.attr}'
    case _:
      raise Exception(f'{ast.dump(attribute)} type not found.')


def get_args(args: ast.arguments):
  items = list()
  for arg in args:
    match type(arg):
      case ast.Constant:
        items.append(arg.value)
      case ast.Name:
        items.append(arg.id)
      case _:
        raise Exception(f'{ast.dump(arg)} type not found.')
  return items


def get_value(node):
  match type(node):
    case ast.Constant:
      return node.value
    case ast.Name:
      return node.id
    case _:
      raise Exception(f'{ast.dump(node)} type not found.')


def add_import(node: ast.Module, import_str: str):
  import_node = ast.parse(import_str).body[0]
  for body in node.body:
    if isinstance(body, ast.ClassDef):
      node.body.insert(0, import_node)
      break
    
    if is_ast_node_equal(body, import_node):
      break


class CheckVariableIsModifiedVisitor(ast.NodeVisitor):
  def __init__(self, variable):
    self.variable = variable
    self.modified = False
  
  def visit_Call(self, node: ast.Call):
    if not isinstance(node.func, ast.Name):
      return
    
    if len(node.args) > 0:
      var = get_node_hash(node.args[0])
      if var == self.variable and 'psynth' in node.func.id:
        self.modified = True


class FindVariableDeclarations(ast.NodeVisitor):

  def __init__(self, data_type: DataType):
    self.variables = set()
    self.data_type = get_data_type_str(data_type)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Name):
      return
    
    if node.value.func.id != self.data_type:
      return

    self.variables.add(get_node_hash(node.targets[0]))


class VariableTransformer(ast.NodeTransformer):

  def __init__(self, var, from_type: DataType, to_type: DataType):
    self.var = var
    self.from_type = get_data_type_str(from_type)
    self.to_type = get_data_type_str(to_type)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Name):
      return node
    
    if node.value.func.id != self.from_type:
      return node
    
    if get_node_hash(node.targets[0]) != self.var:
      return node

    node.value.func.id = self.to_type
    return node