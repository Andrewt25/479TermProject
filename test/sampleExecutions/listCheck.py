from test.sampleExecutions.sampleStructures.list import ListStruct

def listIncrements(a:ListStruct, start):
    for i in range(len(a.collection)):
        hasVal = a.find1(start+i)
        if(hasVal == None):
            return False
    return True
