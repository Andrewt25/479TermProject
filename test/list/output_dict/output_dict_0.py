from synthesis.list.methods.for_loop import *
from synthesis.list.methods.remove import *
from synthesis.list.methods.count import *
from synthesis.list.methods.append import *

class Example:

    def __init__(self):
        self.list = dict()
        self.dict = dict()

    def append(self, item):
        program_synthesis_append(self.list, item)
        self.dict[item] = 1

    def count(self, item):
        program_synthesis_count(self.list, item)

    def remove(self, item):
        program_synthesis_remove(self.list, item)

    def for_loop(self):
        [item for item in program_synthesis_for_loop(self.list)]
        count_items = 0
        for item in program_synthesis_for_loop(self.list):
            count_items += 1

    def foo(self):
        d = list()
        d.append(1)
        d.count(1)
        d.remove(1)
        [item for item in d]
        for item in d:
            pass
