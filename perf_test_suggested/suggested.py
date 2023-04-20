from synthesis.list.methods.for_loop import *
from synthesis.list.methods.remove import *
from synthesis.list.methods.count import *
from synthesis.list.methods.append import *
from random import random

class messages:

    def __init__(self):
        self.set = set()
        self.list = dict()

    def addMsg(self, msgs):
        for msg in msgs:
            self.set.add(msg)
            psynth_list_to_dict_append(self.list, msg)

    def log(self, newMsgs, renameDups=False):
        for msg in newMsgs:
            if renameDups:
                if msg in self.list:
                    self.logOne(self.makeUnique(msg))
                else:
                    self.logOne(msg)
            elif msg not in self.list:
                self.logOne(msg)

    def logOne(self, msg):
        self.set.add(msg)
        psynth_list_to_dict_append(self.list, msg)

    def makeUnique(self, msg):
        randomVal = random()
        return msg + '_' + str(hash(randomVal))