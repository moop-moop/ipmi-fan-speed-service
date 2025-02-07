import unittest
from my_project.utils import greet

class TestUtils(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

if __name__ == "__main__":
    unittest.main()
