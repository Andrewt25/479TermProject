import unittest
import LearningTests.someFunction
import LearningTests.someFunction2
import timeit
from LearningTests.otherExamplesAST.example import Example

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        c = 3
        t = "a"
        l = [1]
        b = Example()
        self.assertEqual(len(l), 1)
        self.assertEqual(LearningTests.someFunction.doAthing(b), ('A', 13))

    def perf_test(self):
        c = 3
        t = "a"
        l = [1]
        y = {1,2,3}
        b = Example()
        b.add(45)
        b.exist(45)
        b.delete(46)
        self.assertIsNotNone(LearningTests.someFunction.doAthing(b))

if __name__ == '__main__':
    unittest.main()