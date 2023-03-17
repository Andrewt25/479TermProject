import timeit
import ast
import subprocess
import os

from inputVisitor import inputVisitor

def getAST(path:str) -> ast.Module:
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
        f.close()
    return tree

def createFilePath(filename:str, ext:str='py'):
    return './' + filename + '.' + ext

def getFileName(path:str):
    return path.split('\\').pop().rstrip('.py')

def createNewFileName(filename:str, flag:str):
    return  filename + flag

def createPythonFile(fileName:str, astTree:ast.Module):
    path = createFilePath(getFileName(fileName))
    with open(path, "w") as f:
        f.write(ast.unparse(astTree))
        f.close()

def cleanupPythonFile(fileName:str):
    path = createFilePath(getFileName(fileName))
    os.remove(path)

def timeFunction(programPath:str, unitPath: str):
    flags = ['min', 'max']

    programFileName = getFileName(programPath)
    unitFileName = getFileName(unitPath)

    for flag in flags:
        newProgramFileName = createNewFileName(programFileName, flag)
        newTestFileName = createNewFileName(unitFileName, flag)
        #get Trees
        treeUnit = getAST(unitPath)
        treeProgram = getAST(programPath)

        #mutate Trees
        visitor = inputVisitor(programFileName, newProgramFileName, flag)
        newTree = ast.fix_missing_locations(visitor.visit(treeUnit))
      
        #create files for testing
        createPythonFile(newTestFileName, newTree)
        createPythonFile(newProgramFileName, treeProgram)
        #perform tests

        input = ['python3', newTestFileName+'.py', visitor.testClassName+'.perf_test']
        timeTest2 = timeit.Timer(lambda:subprocess.run(input, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        print('Flag: {} time:  {}'.format(flag, timeTest2.timeit(10)/10))


        #cleanup
        cleanupPythonFile(newTestFileName)
        cleanupPythonFile(newProgramFileName)
        
    