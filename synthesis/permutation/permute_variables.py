import ast
import copy
import itertools
from synthesis.datatypes import *
from synthesis.util import *
from .methods.compare import *
from .methods.for_loop import *
from .methods.list_comp import *

class PermuteVariables():

  def __init__(self, ast_obj: ast.AST) -> None:
    self.ast_obj = ast_obj

  def find_data_type_varable(self) -> list:
    variables = list()
    for dataType in DataType:
      var_visitor = FindVariables(dataType)
      var_visitor.visit(self.ast_obj)
      variables += var_visitor.variables
    return variables

  def find_editible_locations(self, source_var):
    result = list()
    for_visitor = ForLoopVisitor(source_var)
    for_visitor.visit(self.ast_obj)
    result += for_visitor.locations

    list_comp_visitor = ListCompVisitor(source_var)
    list_comp_visitor.visit(self.ast_obj)
    result += list_comp_visitor.locations

    compare_visitor = CompareVisitor(source_var)
    compare_visitor.visit(self.ast_obj)
    result += compare_visitor.locations

    return result

  def modify_ast(self) -> list:
    variables = self.find_data_type_varable()
    if len(variables) < 2:
      return []

    trees = list()
    for source_var, target_var in itertools.permutations(variables, r=2):
      # Find all the source variable usages and change them to the target variable
      source_locations = self.find_editible_locations(source_var[0])
      for n in range(1, len(source_locations) + 1):
        locations_to_modify = list(itertools.combinations(source_locations, r=n))
        for locations in locations_to_modify:
          tree = copy.deepcopy(self.ast_obj)
          for location in locations:
            transformer = Transformer(target_var[1], (location[0], location[1]))
            tree = transformer.visit(tree)
          trees.append(tree)

    return trees


class FindVariables(ast.NodeVisitor):

  def __init__(self, data_type: DataType):
    self.variables = set()
    self.data_type = get_data_type_str(data_type)

  def visit_Assign(self, node: ast.Assign):
    if not isinstance(node.value, ast.Call) \
      or not isinstance(node.value.func, ast.Name):
      return
    
    if node.value.func.id != self.data_type:
      return

    attribute = node.targets[0]
    self.variables.add((get_node_hash(attribute), get_attr_variable(attribute)))


class Transformer(ast.NodeTransformer):

  def __init__(self, variable, location_to_modify):
    self.variable = ast.parse(variable).body[0].value
    self.location_to_modify = location_to_modify
  
  def visit_Compare(self, node: ast.Compare):
    if (node.lineno, node.col_offset) != self.location_to_modify:
      return self.generic_visit(node)
    node.comparators[0] = self.variable
    return node
  
  def visit_For(self, node: ast.For):
    if (node.lineno, node.col_offset) != self.location_to_modify:
      return self.generic_visit(node)
    node.iter = self.variable
    return node
    
  def visit_ListComp(self, node: ast.ListComp):
    if (node.lineno, node.col_offset) != self.location_to_modify:
      return self.generic_visit(node)
    node.generators[0].iter = self.variable
    return node
  


    