import unittest
import  test.sampleExecutions.dictCheck
from  test.sampleExecutions.sampleCode.dict import DictStruct

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        b = DictStruct()
        b.add(1,1)
        self.assertTrue(test.sampleExecutions.dictCheck.listIncrements(b, 1))

    def test_perf(self):
        b = DictStruct()
        itemsToAdd = [1]
        for i in itemsToAdd:
            b.add(i,i)
        self.assertTrue(test.sampleExecutions.dictCheck.listIncrements(b, 1))

if __name__ == '__main__':
    unittest.main()