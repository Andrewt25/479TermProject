import sys  
import os
import ast
import timeit
import matplotlib.pyplot as plt
import hashlib

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname((file_path))))

from datatypes import *
from list.list import *
from dict.dict import *
from testTransformer import *


def testDriver(programPath:str, unitPath: str):
    programFileName = getFileName(programPath)

    # Build tests base -> 100 increment 10 at a time 11 total
    performanceTests = []
    encounteredModifications = set()
    
    # Generate n modified versions of suplied unit test incrementing complexity by 10.
    # i.e. dupicating operation 10 times up to n*10 times
    for i in range(101):
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

    '''
    First iteration program runs the generated test against the unmodfied program ast and records results. It then finds the possible changes that can be made
    to the ast and passes asts with those changes into the next iteration.
    Second iteration onwards the test are run against all the asts supplied by the previous iteration using the ast with the smallest growth rate and find asts
    for further exploration
    '''
    while True:
        topIterPerformer = ()
        for modAst in astsToTest:
            # warmup to avoid slow intial runs
            combineAndExecute(copy.deepcopy(modAst), performanceTests[0])
            times = []
            # execute all generated tests against modified program
            for test in performanceTests:
                times = times + combineAndExecute(copy.deepcopy(modAst), test)
            # check for times if none returned execution failed
            if len(times) > 0:
                # set initial on first execution for unmodified program
                if(len(initial) == 0):
                    rate = avgGrowthRate(times)
                    initial = (modAst, times, rate)
                # comparison to find best iteration performer
                topIterPerformer = comparePerformance(topIterPerformer, times, modAst)
        # comparison to find best overall performer
        if(len(topIterPerformer) == 3):
            topPerformer = comparePerformance(topPerformer, topIterPerformer[1], topIterPerformer[0])

        # reset list after tests
        astsToTest = []
        # Find modifications if any for each supported type
        for type in DataType:
            # checks that there were valid results this iteration
            if(len(topIterPerformer) == 3):
                # Get possible changes for supported types
                treeProgram = topIterPerformer[0]
                modListAsts = ListTo(copy.deepcopy(treeProgram)).modify_ast(type)
                astsToTest = astsToTest + modListAsts
                modDictAsts = DictTo(copy.deepcopy(treeProgram)).modify_ast(type)
                astsToTest = astsToTest + modDictAsts
        
        # check for duplicate asts
        for modAst in astsToTest:
            ast_str = ast.dump(modAst)
            hash_obj = hashlib.sha256(ast_str.encode())
            hash = hash_obj.hexdigest()
            if(hash in encounteredModifications):
                astsToTest.remove(modAst)
            else:
                encounteredModifications.add(hash)


        index = index + 1
        # program completes at a depth of 50 or all branches explored
        if astsToTest == [] or index == 10:
            break
    createOutput(initial[1], topPerformer[1])
    writeSuggestion(topPerformer[0])
        
# combines two asts into single ast and execute the results
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
    x = range(len(initial))
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
