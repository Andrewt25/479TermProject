from synthesis.list.methods.for_loop import *
from synthesis.list.methods.remove import *
from synthesis.list.methods.count import *
from synthesis.list.methods.append import *

class ListStruct:

    def __init__(self):
        self.collection = dict()

    def add(self, item):
        psynth_list_to_dict_append(self.collection, item)

    def exist(self, item):
        return item in self.collection

    def find1(self, item):
        if self.exist(item):
            return item
        return None

    def delete(self, item):
        if self.exist(item):
            psynth_list_to_dict_count(self.collection, item)

    def find2(self, item):
        return item if self.exist(item) else None