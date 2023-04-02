import unittest
import  test.sampleExecutions.dictCheck
from  test.sampleExecutions.sampleStructures.dict import DictStruct

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        b = DictStruct()
        b.add(1,45)
        self.assertTrue(test.sampleExecutions.dictCheck.listIncrements(b, 1))

    def perf_test(self):
        b = DictStruct()
        b.add(1,45)
        self.assertTrue(test.sampleExecutions.dictCheck.listIncrements(b, 1))

if __name__ == '__main__':
    unittest.main()