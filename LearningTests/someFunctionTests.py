import unittest
import someFunction
from otherExamplesAST.example2 import Example

class TestStringMethods(unittest.TestCase):
    def test_valid(self):
        c = 3
        t = "a"
        l = []
        b = Example(l)
        self.assertEqual(someFunction.doAthing(t, c), ('A', 13))

    def perf_test(self):
        c = 3
        t = "a"
        l = []
        b = Example(l)
        self.assertIsNotNone(someFunction.doAthing(t, c))

if __name__ == '__main__':
    unittest.main()