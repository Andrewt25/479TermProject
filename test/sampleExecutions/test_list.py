import unittest
import  test.sampleExecutions.listCheck
from  test.sampleExecutions.sampleCode.list import ListStruct

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        b = ListStruct()
        b.add(45)
        self.assertTrue(test.sampleExecutions.listCheck.listIncrements(b, 45))

    def test_perf(self):
        b = ListStruct()
        itemsToAdd = [45]
        for i in itemsToAdd:
            b.add(i)
        self.assertTrue(test.sampleExecutions.listCheck.listIncrements(b, 45))

if __name__ == '__main__':
    unittest.main()