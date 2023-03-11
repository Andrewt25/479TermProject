class List():
  def __init__(self):
    self.input_list = list()
    self.list_a = dict.fromkeys([1,2,3],1)

  def append_input_list(self, item):
    self.input_list.append(item)

  def append_list_a(self, item):
    if item in self.list_a:
      self.list_a[item] += 1
    else:
      self.list_a[item] = 1

  def insert_input_list(self, idx, item):
    self.input_list.insert(0, idx, item)

  def remove_list_a(self, item):
    if self.list_a[item] == 1:
      self.list_a.pop(item)
    self.list_a[item] -= 1

  def clear_input_list(self):
    self.input_list.clear()

  def clear_list_a(self):
    self.list_a.clear()

  def index_input_list_v1(self):
    return self.input_list.index(0)
  
  def index_input_list_v2(self):
    return self.input_list[0]