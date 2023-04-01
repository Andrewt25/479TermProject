import ast

def getAST(path:str) -> ast.Module:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
        f.close()
    return tree

def getFileName(path:str):
    return path.split('\\').pop().rstrip('.py')