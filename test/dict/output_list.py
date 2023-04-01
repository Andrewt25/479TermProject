from synthesis.dict.methods.values import *
from synthesis.dict.methods.keys import *
from synthesis.dict.methods.get import *
from synthesis.dict.methods.pop import *
from synthesis.dict.methods.remove import *
from synthesis.dict.methods.add import *

class Example:

    def __init__(self):
        self.dict = list()

    def add(self, key, value):
        program_synthesis_add(self.dict, key, value)
        program_synthesis_add(self.dict, key, 1)
        program_synthesis_add(self.dict, key, 'a')
        program_synthesis_add(self.dict, key, 'abc')
        program_synthesis_add(self.dict, key, (1, 2))

    def remove(self, key):
        program_synthesis_remove(self.dict, key)

    def pop(self, key):
        program_synthesis_pop(self.dict, key)
        result = program_synthesis_pop(self.dict, key)
        return result

    def get(self, key):
        result = program_synthesis_get(self.dict, key)
        result = program_synthesis_get(self.dict, key)
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
        [key for key in program_synthesis_keys(self.dict)]
        for key in program_synthesis_keys(self.dict):
            temp_k = key

    def values(self):
        [value for value in program_synthesis_values(self.dict)]
        for value in program_synthesis_values(self.dict):
            temp_v = value
