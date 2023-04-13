from test.sampleExecutions.sampleCode.dict import DictStruct

def listIncrements(a:DictStruct, start):
    for i in range(len(a.collection)):
        hasVal = a.find1(start+i)
        if(hasVal == None):
            return False
    return True
