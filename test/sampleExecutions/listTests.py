import unittest
import  test.sampleExecutions.listCheck
from  test.sampleExecutions.sampleStructures.list import ListStruct

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        b = ListStruct()
        b.add(45)
        self.assertTrue(test.sampleExecutions.listCheck.listIncrements(b, 45))

    def perf_test(self):
        b = ListStruct()
        b.add(45)
        self.assertTrue(test.sampleExecutions.listCheck.listIncrements(b, 45))

if __name__ == '__main__':
    unittest.main()