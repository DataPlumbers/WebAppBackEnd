import unittest
import sys
from headers import *

class TestBoardStupid(unittest.TestCase):

    def test_get_headers_FNFE(self):
        self.assertRaises(FileNotFoundError, get_headers, "file_lol.lol")
        self.assertRaises(FileNotFoundError, get_headers, "fake.csv")

if __name__ == '__main__':
    unittest.main()
