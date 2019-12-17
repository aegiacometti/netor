import unittest
from slackbot import verify_host


class TestSource(unittest.TestCase):
    def test_verify_host(self):
        """
        Test verify_host function, should verify if the host is an valid IP and if it is a name its correct resolution
        :return:
        """
        data = ['1.1.1.1', '1.1.1', 'google.com', 'win2019srv']
        result = verify_host(data[0])
        self.assertEqual(result, )


if __name__ == '__main__':
    unittest.main()
