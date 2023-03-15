import unittest
import someFunction
import timeit
from otherExamplesAST.example2 import Example

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        c = 3
        t = "a"
        l = [1]
        b = Example(l)
        self.assertEqual(someFunction.doAthing(t, c), ('A', 13))

    def perf_test(self):
        c = 3
        t = "a"
        l = [1]
        y = {1,2,3}
        b = Example(l)
        self.assertIsNotNone(someFunction.doAthing(t, c))

if __name__ == '__main__':
    unittest.main()