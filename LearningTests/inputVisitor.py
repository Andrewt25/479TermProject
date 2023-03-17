import ast
   
class inputVisitor(ast.NodeTransformer):
    def __init__(self, fileName:str, newFileName:str ,flag:str='min'):
      self.flag=flag
      self.fileName = fileName
      self.newFileName = newFileName
    # visiter for functions looks for specific test to mutate
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        if(node.name == 'perf_test'):
            for n in node.body:
                if(n.__class__ == ast.Assign):
                        n.value = self.__getInput(n.value) 
            self.perf_node = node
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node: ast.Attribute) :
        if(node.value.id == self.fileName):
            node.value.id = self.newFileName
        return node
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.testClassName = node.name
        self.generic_visit(node)
        return node
    
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name == self.fileName:
                alias.name = self.newFileName
        self.generic_visit(node)
        return node

    # UTILITY FUNCTIONS
    
    # returns value for constants
    def __getConstantInput(self, nodeType):
        if self.flag == 'max':
            if nodeType == str:
                return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif nodeType == int:
                return 1
        elif self.flag == 'min':
            if nodeType == str:
                return ""
            elif nodeType == int:
                return 0     
        return '4'

    # add items equal to size to ast list using first item as type to generate input
    # if list is empty uses default constant input
    def __getListInput(self,nodeList):
        size=self.__getConstantInput(int)
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

