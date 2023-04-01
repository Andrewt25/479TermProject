import ast

def getAST(path:str) -> ast.Module:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
        f.close()
    return tree

def getFileName(path:str):
    return path.split('\\').pop().rstrip('.py')

def comparePerformance(current, metric, ast):
    if(len(current) == 2):
        if( metric < current[1]):
            return (ast, metric)
        else:
            return current
    else:
        return (ast, metric)

def avgGrowthRate(times):
    growthRates = []
    for i in range(len(times)-1):
        initial = times[i]
        final = times[i+1]
        rate = (final - initial)/initial
        growthRates.append(rate)

    return sum(growthRates)/len(growthRates)
