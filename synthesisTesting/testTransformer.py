import ast
   
class testTransformer(ast.NodeTransformer):
    def __init__(self, fileName:str ,count:int=1):
      self.count=count if count > 0 else 1
      self.fileName = fileName
      self.importNodes = []

    # visiter for functions looks for specific test to mutate
    def visit_FunctionDef(self, node: ast.FunctionDef):
        nodesToCopy = []
        if(node.name == 'perf_test'):
            for n in node.body:
                if(n.__class__ == ast.Assign):
                    n.value = self.__getInput(n.value) 
                if(n.value.__class__ == ast.Call and n.value.func.__class__ == ast.Attribute):
                    if(n.value.func.value.id != 'self'):
                        # record function calls to duplicate
                        nodesToCopy.append(n)
            self.perf_node = node
        # duplicate function calls
        for n in nodesToCopy:
            for i in range(self.count):
             node.body.insert(node.body.index(n), n)
        self.generic_visit(node)
        return node
    
    #strip import reference so able to combine modified program
    #with tests and run as AST
    def visit_Call(self, node: ast.Call):
        if(node.func.__class__ == ast.Attribute):
            if(hasattr(node.func.value, 'id') and node.func.value.id == self.fileName):
                funcName = node.func.attr
                node.func = ast.Name(id=funcName, ctx=ast.Load())
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.testClassName = node.name
        self.testBody = node
        self.generic_visit(node)
        return node
    
    def visit_Import(self, node: ast.Import):
        self.importNodes.append(node)
        self.generic_visit(node)
        return node
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.importNodes.append(node)
        self.generic_visit(node)
        return node
    

    # UTILITY FUNCTIONS
    
    # returns value for constants
    def __getConstantInput(self, nodeType):
        if nodeType == str:
            val = ""
            for i in range(self.count):
                val = val + "a"
            return val
        elif nodeType == int:
            return  1000*self.count 
        return 0

    # add items equal to size to ast list using first item as type to generate input
    # if list is empty uses default constant input
    def __getListInput(self,nodeList):
        size=self.count
        length = len(nodeList)
        nodeType = type(nodeList[0].value) if length > 0 else None
        for i in range(length, length+size):
            node = ast.Constant(self.__getConstantInput(nodeType))
            nodeList.insert(i,node)
        return nodeList

    # Defines behaviour to modify/mock inputs for unit test
    def __getInput(self, node):
        nodeType = type(node)
        if nodeType == ast.Constant:
            node.value = self.__getConstantInput(type(node.value))
        elif hasattr(node, 'elts'):
            node.elts = self.__getListInput(node.elts)
        return node

