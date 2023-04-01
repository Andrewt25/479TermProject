from synthesis.list.methods.remove import *
from synthesis.list.methods.count import *
from synthesis.list.methods.append import *

class Example:

    def __init__(self):
        self.list = list()
        self.dict = dict()

    def append(self, item):
        self.list.append(item)
        self.dict[item] = 1

    def count(self, item):
        self.list.count(item)

    def remove(self, item):
        self.list.remove(item)

    def for_loop(self):
        count_items = 0
        for item in self.list:
            count_items += 1

    def foo(self):
        d = set()
        program_synthesis_append(d, 1)
        program_synthesis_count(d, 1)
        program_synthesis_remove(d, 1)
        for item in d:
            pass
