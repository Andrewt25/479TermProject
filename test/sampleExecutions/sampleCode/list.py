class ListStruct:
  def __init__(self):
    # self.collection = set()
    self.collection = list()

  def add(self, item):
    # self.collection.add(item)
    self.collection.append(item)

  def exist(self, item):
    return item in self.collection

  def find1(self, item):
    if self.exist(item):
      return item
    return None
  
  def delete(self, item):
    if self.exist(item):
      self.collection.remove(item)

  def find2(self, item):
    return item if self.exist(item) else None
