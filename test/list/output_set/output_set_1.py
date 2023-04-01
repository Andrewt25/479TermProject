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
        [item for item in self.list]
        count_items = 0
        for item in self.list:
            count_items += 1

    def foo(self):
        d = set()
        psynth_list_to_set_append(d, 1)
        psynth_list_to_set_count(d, 1)
        psynth_list_to_set_count(d, 1)
        [item for item in d]
        for item in d:
            pass
