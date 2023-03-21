import ast
import copy
import sys  
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from synthesis.datatypes import *
from synthesis.util import *
from .methods.append import *


class ListTo():
  # TODO: Give the user an option to modify only n variables and return m number of ASTs
  def __init__(self, ast_obj, target_type: DataType) -> None:
    self.ast_obj = copy.deepcopy(ast_obj)
    self.target_type = target_type

  def modify_ast(self) -> ast:
    # Find all variables that is type list
    var_visitor = FindVariableDeclarations(DataType.List)
    var_visitor.visit(self.ast_obj)
    variables = var_visitor.variables
    # TODO: Right here we can modify n variables, depending on user input.
    # Deep copy self.ast_obj into a new variable

    # Modify all variables that is a type list to target data type
    var_transformer = VariableTransformer(variables, DataType.List, self.target_type)
    tree = var_transformer.visit(self.ast_obj)

    # Modify all valid appends
    append_visitor = AppendVisitor(variables)
    tree = append_visitor.visit(tree)

    return tree




    