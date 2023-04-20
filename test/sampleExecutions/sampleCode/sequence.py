from random import randrange
class sequence:
    def __init__(self, n, r):
        self.size = n
        self.range = r
        self.sequence = list() 
        if self.size > 0:
            self.__generateSequence__(self.size)

    def __generateSequence__(self, size):
        for i in range(size):
            n = randrange(self.range)
            self.sequence.append(n)
    
    def hasDigit(self, n):
        if n in self.sequence:
            return True
        else:
            return False
        
    def getDistribution(self):
        count = 0
        for i in range(self.range):
           if self.hasDigit(i):
               count += 1
        return count/self.range
    
    def addToSequence(self, n):
        self.__generateSequence__(n)
        self.size = self.size + n 
