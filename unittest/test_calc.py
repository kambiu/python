"""
Ref link:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
"""

import unittest
import calc

class TestCalc(unittest.TestCase):

    """
    setUpClass and tearDownClass only run once 
    eg. for database
    """
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    """ this will run before all test cases """
    def setUp(self):
        print("setUp()")
        # other test caes may use self for all test cases
        self.xxx = "xxx"
        pass

    """ this will run after all test cases """
    def tearDown(self):
        print("tearDown()")
        self.yyy = "yyy"
        pass

    def test_add(self):
        # result = calc.add(10, 5)
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, -1), -2)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(3, 999), 1002)

    def test_sub(self):
        # result = calc.add(10, 5)
        self.assertEqual(calc.sub(10, 5), 5)
        self.assertEqual(calc.sub(-1, -1), 0)
        self.assertEqual(calc.sub(-1, 1), -2)
        self.assertEqual(calc.sub(5, 2), 3)

    def test_mul(self):
        # result = calc.add(10, 5)
        self.assertEqual(calc.mul(10, 5), 50)
        self.assertEqual(calc.mul(-1, -1), 1)
        self.assertEqual(calc.mul(-1, 1), -1)
        self.assertEqual(calc.mul(2, 999), 1998)

    def test_div(self):
        # result = calc.add(10, 5)
        self.assertEqual(calc.div(10, 5), 2)
        self.assertEqual(calc.div(-1, -1), 1)
        self.assertEqual(calc.div(-1, 1), -1)
        self.assertEqual(calc.div(5, 2), 2.5)

        # self.assertRaises(ValueError, calc.div, 10, 0)
        with self.assertRaises(ValueError):
            calc.div(10, 0)


if __name__ == "__main__":
    unittest.main()