import sys  
import os
import ast
import timeit
import matplotlib.pyplot as plt

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname((file_path))))

from datatypes import *
from list.list import *
from testTransformer import *


def testDriver(programPath:str, unitPath: str):
    programFileName = getFileName(programPath)

    # Build tests base -> 100 increment 10 at a time 11 total
    performanceTests = [] 
    

    for i in range(11):
        transformer =  testTransformer(programFileName, i*10 )
        unitTree = getAST(unitPath)
        # run transformer to modify tree and collect nodes of interest to be
        # retrieved from transformer
        ast.fix_missing_locations(transformer.visit(unitTree))
        performanceTests.append(transformer)

    
    astsToTest = [getAST(programPath)]
    topPerformer =()
    initial =()
    index = 1

    while True:
        topIterPerformer = ()
        for modAst in astsToTest:
            # warmup
            combineAndExecute(copy.deepcopy(modAst), performanceTests[0])
            times = []
            for test in performanceTests:
                times = times + combineAndExecute(copy.deepcopy(modAst), test)
                #record time
                #output
            if len(times) > 0:
                if(len(initial) == 0):
                    rate = avgGrowthRate(times)
                    initial = (modAst, times, rate)
                topIterPerformer = comparePerformance(topIterPerformer, times, modAst)

        topPerformer = comparePerformance(topPerformer, topIterPerformer[1], topIterPerformer[0])

        # reset list after tests
        print(len(astsToTest))
        astsToTest = []
        for type in DataType:
            if(len(topIterPerformer) == 3):
                treeProgram = topIterPerformer[0]
                modAsts = ListTo(copy.deepcopy(treeProgram)).modify_ast(type)
                astsToTest = astsToTest + modAsts
                if(len(modAsts) > 0):
                    with open("ast"+type.name+".txt", "w") as f:
                        f.write(ast.unparse(modAsts[0]))
                        f.close()

        index = index + 1
        # program completes at a depth of 50 or all branches explored
        if astsToTest == [] or index == 50:
            break
    print(initial[1], topPerformer[1])
    createOutput(initial[1], topPerformer[1])
    writeSuggestion(topPerformer[0])
        

def combineAndExecute(modAst, test):
    # combine imports and body of modified program and test
    for n in test.importNodes:
        modAst.body.insert(0,n)
    modAst.body.append(test.testBody)

    # add assign and call statement to call specific function when executing ast
    assign = ast.Assign(targets=[ast.Name(id=test.testClassName, ctx=ast.Store())], 
            value =ast.Call(func=ast.Name(id=test.testClassName,ctx=ast.Load()),args=[], keywords=[]))
    call_test = ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(
        id=test.testClassName, ctx=ast.Load()), attr='perf_test', ctx=ast.Load()), args=[], keywords=[] ))
    
    modAst.body.append(assign)
    modAst.body.append(call_test)
    modAst = ast.fix_missing_locations(modAst)

    code = compile(modAst, filename='<ast>', mode='exec')
    env = {}
    t = timeit.Timer(lambda:exec(code, env))
    try:  
        return [t.timeit(10)/10]
    except Exception as e:
        print(e)
        return []
    
def getAST(path:str) -> ast.Module:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
        f.close()
    return tree

def getFileName(path:str):
    return path.split('\\').pop().rstrip('.py')

def comparePerformance(current, times, ast):
    rate = avgGrowthRate(times)
    if(len(current) == 3):
        if( rate < current[2]):
            return (ast, times, rate)
        else:
            return current
    else:
        return (ast, times, rate)

def avgGrowthRate(times):
    growthRates = []
    for i in range(len(times)-1):
        initial = times[i]
        final = times[i+1]
        rate = (final - initial)/initial
        growthRates.append(rate)

    return sum(growthRates)/len(growthRates)

def writeSuggestion(modAst):
    if(not os.path.exists("perf_test_suggested")):
        os.mkdir("perf_test_suggested")
    with open("perf_test_suggested/suggested.py", "w") as f:
        f.write(ast.unparse(modAst))
        f.close()


def createOutput(initial, best):
    x = range(11)
    plt.plot(x, initial, label='Initial')
    plt.plot(x, best, label='Top Performer')
    plt.xlabel('Test iteration')
    plt.ylabel('Avg Time')
    plt.title('Initial vs. Top Performer')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    args = sys.argv[1:]
    if(len(args) != 2):
        print("Unexpected number of arguments expected 2 got", len(args))
    else:
        testDriver(args[0],args[1])
