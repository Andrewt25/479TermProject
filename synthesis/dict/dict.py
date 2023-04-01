import ast
import copy
from synthesis.datatypes import *
from synthesis.util import *
from .methods.add import *
from .methods.remove import *
from .methods.pop import *
from .methods.get import *


class DictTo():

  def __init__(self, ast_obj: ast.AST) -> None:
    self.type = DataType.Dict
    self.ast_obj = ast_obj
    self.supported_types = { DataType.List }

  def modify_ast(self, target_type: DataType) -> list:
    if target_type == self.type \
      or target_type not in self.supported_types:
      return []

    # Find all variables that is type dict
    var_visitor = FindVariableDeclarations(self.type)
    var_visitor.visit(self.ast_obj)
    variables = var_visitor.variables

    trees = list()
    for var in variables:
      tree = copy.deepcopy(self.ast_obj)

      # Modify all variables that is a type dict to target data type
      var_transformer = VariableTransformer(var, self.type, target_type)
      tree = var_transformer.visit(tree)

      add_visitor = AddVisitor(var, target_type)
      tree = add_visitor.visit(tree)
      
      remove_visitor = RemoveVisitor(var, target_type)
      tree = remove_visitor.visit(tree)

      pop_visitor = PopVisitor(var, target_type)
      tree = pop_visitor.visit(tree)

      get_visitor = GetVisitor(var, target_type)
      tree = get_visitor.visit(tree)

      trees.append(tree)

    return trees




    