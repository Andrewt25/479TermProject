import sys  
import os
import ast
import timeit

file_path = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname((file_path))))

from synthesis.datatypes import *
from synthesis.list.list import *
from testTransformer import *
from utils import *


def testDriver(programPath:str, unitPath: str):
    # declerations
    # topPerformer = (ast, time);

    programFileName = getFileName(programPath)

    # Build tests base -> 100 increment 10 at a time 11 total
    performanceTests = [] #revist later better way to scale?
    

    for i in range(11):
        transformer =  testTransformer(programFileName, i*10 )
        unitTree = getAST(unitPath)
        # run transformer to modify tree and collect nodes of interest to be
        # retrieved from transformer
        ast.fix_missing_locations(transformer.visit(unitTree))
        performanceTests.append(transformer)

    
    astsToTest = [getAST(programPath)]
    topPerformer =()
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
                rate = avgGrowthRate(times)
                topIterPerformer = comparePerformance(topIterPerformer, rate, modAst)

        topPerformer = comparePerformance(topPerformer, topIterPerformer[1], topIterPerformer[0])

        # reset list after tests
        print(len(astsToTest))
        astsToTest = []
        for type in DataType:
            if(len(topIterPerformer) == 2):
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
    print(topPerformer[1])
        

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
    with open("astExecute.txt", "w") as f:
        f.write(ast.unparse(modAst))
        f.close()

    code = compile(modAst, filename='<ast>', mode='exec')
    env = {}
    t = timeit.Timer(lambda:exec(code, env))
    try:  
        return [t.timeit(10)/10]
    except:
        return []



if __name__ == '__main__':
    args = sys.argv[1:]
    if(len(args) != 2):
        print("Unexpected number of arguments expected 2 got", len(args))
    else:
        testDriver(args[0],args[1])
        #testDriver('..\LearningTests\otherExamplesAST\example.py', '..\LearningTests\someFunctionTests.py')