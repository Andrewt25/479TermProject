import ast


class ListToDict():
  def __init__(self, ast_to_modify) -> None:
    self.ast_to_modify = ast_to_modify

  def find_nodes_to_modify(self) -> list:
    result = list()
    # Find all the variables that are lists.
    # Remove the lists that use invalid operations.
    # Return the lists that can be modified.
    return result

  def modify_ast(self) -> ast:
    nodes_to_modify = self.find_nodes_to_modify()
    for node in nodes_to_modify:
      pass