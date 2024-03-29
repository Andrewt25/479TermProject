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

  def find_editable_locations(self, source_var):
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
      source_locations = self.find_editable_locations(source_var[0])
      for n in range(1, len(source_locations) + 1):
        location_combinations = list(itertools.combinations(source_locations, r=n))
        for locations_to_modify in location_combinations:
          locations = set([(loc[0], loc[1], loc[2]) for loc in locations_to_modify])
          
          tree = copy.deepcopy(self.ast_obj)
          transformer = Transformer(target_var[1], locations)
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

  def __init__(self, to_variable, locations_to_modify):
    self.to_variable = ast.parse(to_variable).body[0].value
    self.locations_to_modify = locations_to_modify
  
  def visit_Compare(self, node: ast.Compare):
    for idx, _ in enumerate(node.comparators):
      if (node.lineno, node.col_offset, idx) in self.locations_to_modify:
        node.comparators[idx] = self.to_variable

    return self.generic_visit(node)
  
  def visit_For(self, node: ast.For):
    if (node.lineno, node.col_offset, 0) in self.locations_to_modify:
      node.iter = self.to_variable

    return self.generic_visit(node)
  
  def visit_ListComp(self, node: ast.ListComp):
    for idx, _ in enumerate(node.generators):
      if (node.lineno, node.col_offset, idx) in self.locations_to_modify:
        node.generators[idx].iter = self.to_variable
    
    return self.generic_visit(node)
  


    