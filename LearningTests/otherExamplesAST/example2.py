class Example:
  def __init__(self, a:list):
    # self.collection = set()
    self.collection = a

  def add(self, item):
    # self.collection.add(item)
    self.collection.append(item)

  def exist(self, item):
    return item in self.collection

  def find1(self, item):
    if self.exist(item):
      return item
    return None

  def find2(self, item):
    return item if self.exist(item) else None
