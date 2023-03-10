import ast
import timeit
from typing import Callable
# from example import *
# import astunparse

class MyOptimizer(ast.NodeTransformer):
  def visit_Name(self, node: ast.Name):
    if node.id == 'pi':
      result = ast.Num(n=3.14)
      result.lineno = node.lineno
      result.col_offset = node.col_offset
      return result
    elif node.id == 'x':
      result = ast.Num(n=5)
      result.lineno = node.lineno
      result.col_offset = node.col_offset
      return result
    return node
  
def testAST() -> Callable:
   # Original Code, Unexecutable
  tree = ast.parse('y = 2 * pi + x')
  # print(astunparse.unparse(tree))
  print(ast.dump(tree, indent=2))

  # Modified Code, Executable
  optimizer = MyOptimizer()
  tree = optimizer.visit(tree)
  
  # print(astunparse.unparse(tree))
  print(ast.dump(tree, indent=2))

  # Execute code
  code = compile(tree, filename='<String>', mode='exec')
  print(code)
  env = {}
  
  return lambda: exec(code, env)

if __name__ == '__main__':
  # Original Code, Unexecutable
  tree = ast.parse('y = 2 * pi')
  # print(astunparse.unparse(tree))
  print(ast.dump(tree, indent=2))

  # Modified Code, Executable
  optimizer = MyOptimizer()
  tree = optimizer.visit(tree)
  
  # print(astunparse.unparse(tree))
  print(ast.dump(tree, indent=2))

  # Execute code
  code = compile(tree, filename='<String>', mode='exec')
  print(code)
  env = {}
  exec(code, env)
  
  print()
  print(env['y'])

  # filename = 'example.py'
  # with open(filename) as f:
  #   tree = ast.parse(f.read(), filename=filename)
  
  # print(ast.dump(tree, indent=2))
