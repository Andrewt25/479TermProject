import ast
import copy
from synthesis.datatypes import *
from synthesis.util import *
from .methods.append import *
from .methods.count import *
from .methods.remove import *
from .methods.for_loop import *


class ListTo():

  def __init__(self, ast_obj: ast.AST) -> None:
    self.type = DataType.List
    self.ast_obj = ast_obj
    self.supported_types = { DataType.Dict, DataType.Set }

  def modify_ast(self, target_type: DataType) -> list:
    if target_type == self.type \
      or target_type not in self.supported_types:
      return []

    # Find all variables that is type list
    var_visitor = FindVariableDeclarations(self.type)
    var_visitor.visit(self.ast_obj)
    variables = var_visitor.variables

    trees = list()
    for var in variables:
      check_visitor = CheckVariableIsModifiedVisitor(var)
      check_visitor.visit(self.ast_obj)
      if check_visitor.modified:
        continue
      
      tree = copy.deepcopy(self.ast_obj)

      # Modify all variables that is a type list to target data type
      var_transformer = VariableTransformer(var, self.type, target_type)
      tree = var_transformer.visit(tree)

      append_visitor = AppendVisitor(var, target_type)
      tree = append_visitor.visit(tree)
      
      count_visitor = CountVisitor(var, target_type)
      tree = count_visitor.visit(tree)

      remove_visitor = RemoveVisitor(var, target_type)
      tree = remove_visitor.visit(tree)

      for_visitor = ForVisitor(var, target_type)
      tree = for_visitor.visit(tree)

      trees.append(tree)

    return trees




    