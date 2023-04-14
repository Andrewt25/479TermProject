import ast
import copy
from synthesis.datatypes import *
from synthesis.util import *
from .methods.add_or_update import *
from .methods.remove import *
from .methods.pop import *
from .methods.get import *
from .methods.items import *
from .methods.keys import *
from .methods.values import *
from .methods.exists import *

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
      check_visitor = CheckVariableIsModifiedVisitor(var)
      check_visitor.visit(self.ast_obj)
      if check_visitor.modified:
        continue

      tree = copy.deepcopy(self.ast_obj)

      # Modify all variables that is a type dict to target data type
      var_transformer = VariableTransformer(var, self.type, target_type)
      tree = var_transformer.visit(tree)

      add_visitor = AddOrUpdateVisitor(var, target_type)
      tree = add_visitor.visit(tree)
      
      remove_visitor = RemoveVisitor(var, target_type)
      tree = remove_visitor.visit(tree)

      pop_visitor = PopVisitor(var, target_type)
      tree = pop_visitor.visit(tree)

      get_visitor = GetVisitor(var, target_type)
      tree = get_visitor.visit(tree)

      items_visitor = ItemsVisitor(var, target_type)
      tree = items_visitor.visit(tree)

      keys_visitor = KeysVisitor(var, target_type)
      tree = keys_visitor.visit(tree)

      values_visitor = ValuesVisitor(var, target_type)
      tree = values_visitor.visit(tree)

      exists_visitor = ExistsVisitor(var, target_type)
      tree = exists_visitor.visit(tree)

      trees.append(tree)

    return trees




    