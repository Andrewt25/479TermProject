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

  def get(self, key):
    result = self.dict.get(key)
    result = self.dict[key]
    return result

  def items(self):
    [item for item in self.dict.items()]
    for item in self.dict.items():
      temp = item # tuple
      temp_k = item[0]
      temp_v = item[1]

    for key, value in self.dict.items():
      temp_k = key
      temp_v = value

  def keys(self):
    [key for key in self.dict.keys()]
    for key in self.dict.keys():
      temp_k = key # unique

  def values(self):
    [value for value in self.dict.values()]
    for value in self.dict.values():
      temp_v = value # duplicates allowed

  def key_exists(self, key):
    return key in self.dict
