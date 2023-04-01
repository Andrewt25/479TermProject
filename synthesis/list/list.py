import ast
import copy
from synthesis.datatypes import *
from synthesis.util import *
from .methods.append import *
from .methods.count import *
from .methods.remove import *
from .methods.for_loop import *


class ListTo():

  def __init__(self, ast_obj: ast.AST, target_type: DataType) -> None:
    self.type = DataType.List
    self.ast_obj = ast_obj
    self.target_type = target_type

  def modify_ast(self) -> list:
    if self.target_type == self.type:
      return []

    # Find all variables that is type list
    var_visitor = FindVariableDeclarations(self.type)
    var_visitor.visit(self.ast_obj)
    variables = var_visitor.variables

    trees = list()
    for var in variables:
      tree = copy.deepcopy(self.ast_obj)

      # Modify all variables that is a type list to target data type
      var_transformer = VariableTransformer(var, DataType.List, self.target_type)
      tree = var_transformer.visit(tree)

      append_visitor = AppendVisitor(var, self.target_type)
      tree = append_visitor.visit(tree)
      
      count_visitor = CountVisitor(var, self.target_type)
      tree = count_visitor.visit(tree)

      remove_visitor = RemoveVisitor(var, self.target_type)
      tree = remove_visitor.visit(tree)

      for_visitor = ForVisitor(var, self.target_type)
      tree = for_visitor.visit(tree)

      trees.append(tree)

    return trees




    