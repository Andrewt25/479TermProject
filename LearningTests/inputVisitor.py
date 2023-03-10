import ast
import sys

# returns value for constants
def getConstantInput(nodeType, flag):
    if flag == 'max':
        if nodeType == str:
            return "andy"
        elif nodeType == int:
            return sys.maxsize
    elif flag == 'min':
        if nodeType == str:
            return ""
        elif nodeType == int:
            return ~sys.maxsize      
    return '4'


# add items equal to size to ast list using first item as type to generate input
# if list is empty uses default constant input
def getListInput(nodeList, flag):
    size=2
    length = len(nodeList)
    nodeType = type(nodeList[0]) if length > 0 else None
    for i in range(length, length+size):
       node = ast.Constant(getConstantInput(nodeType, flag))
       nodeList.insert(i,node)

    return nodeList

# Defines behaviour to modify/mock inputs for unit test
def getInput(node, flag):
    nodeType = type(node)
    if nodeType == ast.Constant:
        node.value = getConstantInput(type(node.value), flag)
    elif nodeType == ast.List:
        node.elts = getListInput(node.elts, flag)
    return node
   
class inputVisitor(ast.NodeTransformer):
    def __init__(self, flag:str='min'):
      self.flag=flag
    # visiter for functions looks for specific test to mutate
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        if(node.name == 'perf_test'):
            for n in node.body:
                if(n.__class__ == ast.Assign):

                        n.value = getInput(n.value, self.flag) 
        self.defNode = node
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.testClassName = node.name
        self.generic_visit(node)
        return node
