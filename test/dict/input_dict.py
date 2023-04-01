class Example():

  def __init__(self):
    self.dict = dict()

  def add(self, key, value):
    self.dict[key] = value
    self.dict[key] = 1
    self.dict[key] = 'a'
    self.dict[key] = 'abc'
    self.dict[key] = (1,2)

  def remove(self, key):
    del self.dict[key]

  def pop(self, key):
    self.dict.pop(key)
    result = self.dict.pop(key)
    return result

  # def get(self, key):
  #   result = self.dict.get(key)
  #   return result

  # def items(self):
  #   for item in self.dict.items():
  #     temp = item # tuple
  #     temp_k = item[0]
  #     temp_v = item[1]

  #   for key, value in self.dict.items():
  #     temp_k = key
  #     temp_v = value

  # def keys(self):
  #   for key in self.dict.keys():
  #     temp_k = key # unique

  # def values(self):
  #   for value in self.dict.values():
  #     temp_v = value # duplicates allowed
