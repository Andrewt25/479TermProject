class Example():

  def __init__(self):
    self.list = list()
    self.dict = dict()

  def append(self, item):
    self.list.append(item)
    self.dict[item] = 1

  def foo(self):
    d = list()
    d.append(1)