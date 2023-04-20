import unittest
from  test.sampleExecutions.sampleCode.sequence import sequence

class TestMessages(unittest.TestCase):
    def test_perf(self):
        size = 10
        r = 1
        f = sequence(size, r)
        f.getDistribution()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()