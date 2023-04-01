class Example():

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
    d = list()
    d.append(1)
    d.count(1)
    d.remove(1)
    for item in d:
      pass