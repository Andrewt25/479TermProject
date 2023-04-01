import ast

def get_expected_output_trees(filenames: list) -> set:
  expected_output_tree = set()
  for filename in filenames:
    with open(filename) as f:
      expected_tree = ast.parse(f.read(), filename=filename)
      expected_output_tree.add(ast.dump(expected_tree))
  return expected_output_tree