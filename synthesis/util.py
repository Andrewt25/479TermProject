# import ast


# class ASTKeywordFinder(ast.NodeVisitor):
#   def __init__(self, ast_search_space) -> None:
#     self.ast_search_space = ast_search_space

#   def find_assign_call_id(self, keyword) -> list:
#     visitor = _AssignCallVisitor(keyword)
#     visitor.visit(self.ast_search_space)
#     return visitor.node_matches

#   def find_expr_call_attr(self, keyword) -> list:
#     visitor = _ExprCallAttributeVisitor(keyword)
#     visitor.visit(self.ast_search_space)
#     return visitor.node_matches

#   def find_return_call_attribute_attr(self, keyword) -> list:
#     visitor = _ReturnCallAttributeVisitor(keyword)
#     visitor.visit(self.ast_search_space)
#     return visitor.node_matches



# class _AssignCallVisitor(ast.NodeVisitor):
#   ''' Look for ast.Assign nodes with a function value with a specific id'''
#   def __init__(self, find_value_func_id):
#     self.find_value_func_id = find_value_func_id
#     self.node_matches = list()

#   def visit_Assign(self, node: ast.Assign):
#     if not isinstance(node.value, ast.Call):
#       return

#     if node.value.func.id == self.find_value_func_id:
#       self.node_matches.append(node)


# class _ExprCallAttributeVisitor(ast.NodeVisitor):
#   ''' Look for ast.Expr nodes with a function value with a specific attr'''
#   def __init__(self, find_attr):
#     self.find_attr = find_attr
#     self.node_matches = list()

#   def visit_Expr(self, node: ast.Expr):
#     if not isinstance(node.value, ast.Call):
#       return
    
#     if not isinstance(node.value.func, ast.Attribute):
#       return
    
#     if node.value.func.attr == self.find_attr:
#       self.node_matches.append(node)


# class _ReturnCallAttributeVisitor(ast.NodeVisitor):
#   def __init__(self, find_attr) -> None:
#     self.find_attr = find_attr
#     self.node_matches = list()

#   def visit_Return(self, node: ast.Return):
#     if not isinstance(node.value, ast.Call):
#       return
    
#     if not isinstance(node.value.func, ast.Attribute):
#       return

#     if node.value.func.attr == self.find_attr:
#       self.node_matches.append(node)