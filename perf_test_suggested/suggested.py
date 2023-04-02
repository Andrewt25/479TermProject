class DictStruct:

    def __init__(self):
        self.collection = dict()

    def add(self, key, item):
        self.collection[key] = item

    def exist(self, item):
        return item in self.collection

    def getItem(self, key):
        return self.collection.get(key)

    def getKeys(self):
        return self.collection.keys()

    def find1(self, item):
        if self.exist(item):
            return item
        return None

    def pop(self, key):
        if self.exist(key):
            return self.collection.pop(key)

    def remove(self, key):
        del self.collection[key]