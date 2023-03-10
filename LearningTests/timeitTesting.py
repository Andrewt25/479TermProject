import timeit
import ast
import os

from inputVisitor import inputVisitor


def getTests(path:str) -> ast.Module:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
        f.close()
    return tree



def timeFunction(path: str):
    tree = getTests(path)
    treeTwo = getTests(path)

    maxVisitor = inputVisitor(flag='max')
    minVisitor = inputVisitor()
    newTree = ast.fix_missing_locations(maxVisitor.visit(tree))
    minTree = ast.fix_missing_locations(minVisitor.visit(tree))
    #print(ast.dump(tree, indent=2))
    #print(visitor.defNode)
    p = ".\someFunctionTests2.py"
    with open(p, "w") as f:
        f.write(ast.unparse(newTree))
        f.close()

    p = ".\someFunctionTests3.py"
    with open(p, "w") as f:
        f.write(ast.unparse(minTree))
        f.close()

    code = compile(newTree, filename='<String>', mode='exec')
    env = {}
    t = timeit.Timer(lambda: exec(code, env))
    b = timeit.Timer(lambda:os.system('python3 {} {}.perf_test'.format(p,maxVisitor.testClassName)))
    
    #mutate
    #loop
    print(t.timeit(1))
    print(b.timeit(1))