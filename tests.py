import unittest
import cloud
import os


class MyTestCase(unittest.TestCase):
    def test_first(self):
        actual = True
        expected = True
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
