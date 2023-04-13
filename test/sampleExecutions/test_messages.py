import unittest
from  test.sampleExecutions.sampleCode.messages import messages

class TestMessages(unittest.TestCase):
    def test_perf(self):
        msgs = messages()
        messagesToAdd = ["some msg"]
        moreMessagesToAdd = ["other_messages"]
        msgs.log(messagesToAdd, True)
        msgs.log(moreMessagesToAdd)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()