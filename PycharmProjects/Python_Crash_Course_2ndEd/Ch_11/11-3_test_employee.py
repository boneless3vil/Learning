
import unittest

from employee import Employee

class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.jonathan = Employee('jonathan', 'baldwin', 249000)

    def test_give_default_raise(self):
        self.jonathan.give_raise()
        self.assertEqual(self.jonathan.salary, 254000)

    def test_give_custom_praise(self):
        """ Test that a customer is works properly."""
        self.jonathan.give_raise(100000)
        self.assertEqual(self.jonathan.salary, 349000)


if __name__ == '__main__':
    unittest.main()

