import sys  
import os
import ast
import heapq
import timeit
import matplotlib.pyplot as plt
import hashlib

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname((file_path))))

from datatypes import *
from list.list import *
from dict.dict import *
from testTransformer import *

class TestDriver():
    def __init__(self, programPath: str, unitPath: str):
        self.programPath = programPath
        self.unitPath = unitPath
        self.astId = 0
        self.open_list = list() # working list
        self.close_list = set() # duplicate detection

    def run(self):
        programFileName = getFileName(self.programPath)

        # Build tests base -> 100 increment 10 at a time 11 total
        performanceTests = []
        
        # Generate n modified versions of suplied unit test incrementing complexity by 10.
        # i.e. dupicating operation 10 times up to n*10 times
        for i in range(101):
            transformer =  testTransformer(programFileName, i*10)
            unitTree = getAST(self.unitPath)
            # run transformer to modify tree and collect nodes of interest to be
            # retrieved from transformer
            ast.fix_missing_locations(transformer.visit(unitTree))
            performanceTests.append(transformer)

        rootAst = getAST(self.programPath)
        rootTimes = list()
        heapq.heappush(self.open_list, (0, [], self.astId, rootAst))
        topIterPerformer = []
        testId = 0
        '''
        First iteration program runs the generated test against the unmodfied program ast and records results. It then finds the possible changes that can be made
        to the ast and passes asts with those changes into the next iteration.
        Second iteration onwards the test are run against all the asts supplied by the previous iteration using the ast with the smallest growth rate and find asts
        for further exploration
        '''
        # program completes at a depth of 50 or all branches explored
        while len(self.open_list) != 0:
            _, _, _, modAst = heapq.heappop(self.open_list)
            modAstHash = hash(ast.dump(modAst))
            if modAstHash in self.close_list:
                continue
            else:
                self.close_list.add(modAstHash)

            times = getAstTestRuntimeResults(modAst, performanceTests)
            if len(times) == 0:
                continue

            if len(rootTimes) == 0:
                rootTimes = times

            rate = avgGrowthRate(times)
            heapq.heappush(topIterPerformer, (rate, times, testId, modAst))
            testId += 1

            for type in DataType:
                modListAsts = ListTo(modAst).modify_ast(type)
                self.addAstsToOpenList(rate, modListAsts)

                modDictAsts = DictTo(modAst).modify_ast(type)
                self.addAstsToOpenList(rate, modDictAsts)

        _, topTimes, _,topAst = heapq.heappop(topIterPerformer)
        createOutput(rootTimes, topTimes)
        writeSuggestion(topAst)


    def addAstsToOpenList(self, rate: float, modifiedAsts: list) -> None:
        for modifiedAst in modifiedAsts:
            modifiedAstHash = hash(ast.dump(modifiedAst))
            if modifiedAstHash not in self.close_list:
                self.astId += 1
                heapq.heappush(self.open_list, (rate, [], self.astId, modifiedAst))


def getAstTestRuntimeResults(modAst: ast.AST, performanceTests: list) -> list:
    # warmup to avoid slow intial runs
    combineAndExecute(modAst, performanceTests[0])

    runtime_results = []
    # execute all generated tests against modified program
    for test in performanceTests:
        runtime_results += combineAndExecute(modAst, test)
    return runtime_results


# combines two asts into single ast and execute the results
def combineAndExecute(modAst, test):
    modAst = copy.deepcopy(modAst)
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
        TestDriver(args[0],args[1]).run()
