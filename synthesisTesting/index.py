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
    index = 1

    while True:
        for modAst in astsToTest:
            # warmup
            combineAndExecute(modAst, performanceTests[0])
            for test in performanceTests:
                combineAndExecute(modAst, test)
                #record time
                #output
        # reset list after tests
        astsToTest = []
        for type in DataType:
            treeProgram = getAST(programPath)
            modAsts = ListTo(treeProgram, type).modify_ast()
            astsToTest = astsToTest + modAsts

        index = index + 1
        # program completes at a depth of 50 or all branches explored
        if astsToTest == [] or index == 50:
            break
        

#TODO handle import issue
    # Potentially append filePath all imports
    # temp copy into working dir

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
    print(t.timeit(10)/10)


if __name__ == '__main__':
    testDriver('..\LearningTests\otherExamplesAST\example.py', '..\LearningTests\someFunctionTests.py')