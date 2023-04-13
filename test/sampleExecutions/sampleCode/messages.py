from random import random

class messages:
    def __init__(self):
        self.set = set()
        self.list = list()

    def addMsg(self, msgs):
        for msg in msgs:
            self.set.add(msg)
            self.list.append(msg)
    
    def log(self, newMsgs, renameDups=False):
        for msg in newMsgs:
            if renameDups:
                if msg in self.set:
                    self.logOne(self.makeUnique(msg))
                else:
                    self.logOne(msg)
            else:
                if msg not in self.list:
                    self.logOne(msg)
                
    def logOne(self, msg):
        self.set.add(msg)
        self.list.append(msg)
    
    def makeUnique(self, msg):
        randomVal = random()
        return msg + "_" + str(hash(randomVal))