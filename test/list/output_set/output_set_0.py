from synthesis.list.methods.remove import *
from synthesis.list.methods.count import *
from synthesis.list.methods.append import *

class Example:

    def __init__(self):
        self.list = set()
        self.dict = dict()

    def append(self, item):
        psynth_list_to_set_append(self.list, item)
        self.dict[item] = 1

    def count(self, item):
        psynth_list_to_set_count(self.list, item)

    def remove(self, item):
        psynth_list_to_set_count(self.list, item)

    def for_loop(self):
        [item for item in self.list]
        count_items = 0
        for item in self.list:
            count_items += 1

    def foo(self):
        d = list()
        d.append(1)
        d.count(1)
        d.remove(1)
        [item for item in d]
        for item in d:
            pass
