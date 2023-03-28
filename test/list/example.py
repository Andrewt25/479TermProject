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

  def foo(self):
    d = list()
    d.append(1)
    d.count(1)
    d.remove(1)