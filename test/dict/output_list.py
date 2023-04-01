from synthesis.dict.methods.values import *
from synthesis.dict.methods.keys import *
from synthesis.dict.methods.get import *
from synthesis.dict.methods.pop import *
from synthesis.dict.methods.remove import *
from synthesis.dict.methods.add_or_update import *

class Example:

    def __init__(self):
        self.dict = list()

    def add(self, key, value):
        psynth_dict_to_list_add_or_update(self.dict, key, value)
        psynth_dict_to_list_add_or_update(self.dict, key, 1)
        psynth_dict_to_list_add_or_update(self.dict, key, 'a')
        psynth_dict_to_list_add_or_update(self.dict, key, 'abc')
        psynth_dict_to_list_add_or_update(self.dict, key, (1, 2))

    def remove(self, key):
        psynth_dict_to_list_remove(self.dict, key)

    def pop(self, key):
        psynth_dict_to_list_pop(self.dict, key)
        result = psynth_dict_to_list_pop(self.dict, key)
        return result

    def get(self, key):
        result = psynth_dict_to_list_get(self.dict, key)
        result = psynth_dict_to_list_get(self.dict, key)
        return result

    def items(self):
        [item for item in self.dict]
        for item in self.dict:
            temp = item
            temp_k = item[0]
            temp_v = item[1]
        for (key, value) in self.dict:
            temp_k = key
            temp_v = value

    def keys(self):
        [key for key in psynth_dict_to_list_keys(self.dict)]
        for key in psynth_dict_to_list_keys(self.dict):
            temp_k = key

    def values(self):
        [value for value in psynth_dict_to_list_values(self.dict)]
        for value in psynth_dict_to_list_values(self.dict):
            temp_v = value