class Example():

  def __init__(self):
    self.list = list()
    self.set = set()

  def append(self, item):
    self.list.append(item)
    self.set.add(item)

  def for_loop(self):
    [item for item in self.set]
    count_items = 0
    for item in self.set:
      count_items += 1

  def item_exists(self, item):
    return item in self.set